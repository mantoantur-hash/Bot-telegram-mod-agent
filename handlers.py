# ======================================================================
#  handlers.py
#  Handlers do Telegram: o que o bot faz quando chega uma mensagem.
#  NÃO PRECISA EDITAR ESTE ARQUIVO.
# ======================================================================

import logging
import time

from telegram import Update, ChatPermissions
from telegram.error import TelegramError
from telegram.ext import ContextTypes

import config
import filters
import storage

logger = logging.getLogger(__name__)

MUTED_PERMISSIONS = ChatPermissions(
    can_send_messages=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False,
)

REASON_LABELS = {
    "palavra_proibida": "palavra proibida",
    "link_proibido": "link/convite proibido",
    "flood": "excesso de mensagens (flood)",
    "duplicada": "mensagens repetidas",
}


async def moderate_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler principal. Tudo dentro de try/except para que UM erro
    em UMA mensagem nunca derrube o bot inteiro."""
    try:
        msg = update.effective_message
        if not msg or not msg.text:
            return

        chat = update.effective_chat
        user = update.effective_user
        if chat is None or user is None:
            return

        # bots e admins configurados não são moderados
        if user.is_bot:
            return
        if user.id in config.ADMIN_IDS:
            return
        # só modera em grupos/supergrupos, nunca em chat privado
        if chat.type not in ("group", "supergroup"):
            return

        text = msg.text
        reason = None
        evidence = None

        bad_word = filters.contains_blocked_word(text)
        if bad_word:
            reason = "palavra_proibida"
            evidence = bad_word
        elif filters.contains_link(text):
            reason = "link_proibido"
        else:
            spam_reason = filters.check_spam(chat.id, user.id, text, time.time())
            if spam_reason:
                reason = spam_reason

        if not reason:
            return

        await _apply_punishment(update, context, chat, user, reason, evidence)

    except Exception:
        # nunca deixa uma exceção travar o processamento de mensagens
        logger.exception("Erro ao moderar mensagem (ignorado, bot continua rodando).")


async def _apply_punishment(update, context, chat, user, reason, evidence):
    if config.DELETE_INFRACTING_MESSAGE:
        try:
            await update.effective_message.delete()
        except TelegramError as e:
            logger.warning("Não consegui apagar a mensagem: %s", e)

    count = storage.add_infraction(chat.id, user.id)
    label = REASON_LABELS.get(reason, reason)
    action_text = None

    if count >= config.WARN_LIMIT_BEFORE_BAN:
        try:
            await context.bot.ban_chat_member(chat.id, user.id)
            action_text = (
                f"🚫 {user.mention_html()} foi <b>BANIDO</b> do grupo.\n"
                f"Motivo: {label}."
            )
        except TelegramError as e:
            logger.error("Erro ao banir usuário %s no chat %s: %s", user.id, chat.id, e)

    elif count >= config.WARN_LIMIT_BEFORE_MUTE:
        until = int(time.time()) + config.MUTE_DURATION_MINUTES * 60
        try:
            await context.bot.restrict_chat_member(
                chat.id, user.id, permissions=MUTED_PERMISSIONS, until_date=until
            )
            action_text = (
                f"🔇 {user.mention_html()} foi <b>MUTADO</b> por "
                f"{config.MUTE_DURATION_MINUTES} minuto(s).\nMotivo: {label}."
            )
        except TelegramError as e:
            logger.error("Erro ao mutar usuário %s no chat %s: %s", user.id, chat.id, e)

    else:
        action_text = (
            f"⚠️ {user.mention_html()} recebeu um aviso "
            f"({count}/{config.WARN_LIMIT_BEFORE_BAN}).\nMotivo: {label}."
        )

    if action_text:
        try:
            sent = await context.bot.send_message(chat.id, action_text, parse_mode="HTML")
            if config.AUTO_DELETE_WARNING_SECONDS and context.application.job_queue:
                context.application.job_queue.run_once(
                    _delete_message_job,
                    config.AUTO_DELETE_WARNING_SECONDS,
                    data={"chat_id": chat.id, "message_id": sent.message_id},
                )
        except TelegramError as e:
            logger.error("Erro ao enviar aviso no chat %s: %s", chat.id, e)

    if config.LOG_CHANNEL_ID:
        try:
            await context.bot.send_message(
                config.LOG_CHANNEL_ID,
                f"👤 Usuário: {user.id} (@{user.username or 'sem_usuario'})\n"
                f"💬 Chat: {chat.id} ({chat.title or chat.type})\n"
                f"📌 Motivo: {label}\n"
                f"🔎 Evidência: {evidence or '-'}\n"
                f"🔢 Infrações acumuladas: {count}",
            )
        except TelegramError as e:
            logger.warning("Erro ao enviar log: %s", e)


async def _delete_message_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    data = context.job.data
    try:
        await context.bot.delete_message(data["chat_id"], data["message_id"])
    except TelegramError:
        pass


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    user = update.effective_user
    count = storage.get_infractions(chat.id, user.id)
    await update.message.reply_text(f"Suas infrações registradas neste grupo: {count}")


async def cmd_resetwarns(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat = update.effective_chat
    requester = update.effective_user

    if requester.id not in config.ADMIN_IDS:
        await update.message.reply_text(
            "Apenas administradores configurados em ADMIN_IDS podem usar este comando."
        )
        return

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Responda à mensagem do usuário com /resetwarns para zerar as infrações dele."
        )
        return

    target = update.message.reply_to_message.from_user
    storage.reset_infractions(chat.id, target.id)
    await update.message.reply_text(f"Infrações de {target.first_name} foram zeradas.")
