# ======================================================================
#  bot.py
#  Arquivo principal. Rode com:  python bot.py
#  NÃO PRECISA EDITAR ESTE ARQUIVO — todas as opções estão em config.py
# ======================================================================

import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters as tg_filters

import config
import storage
import handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
# deixa a biblioteca do telegram menos "tagarela" no log, sem perder erros
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger("bot_moderacao")


async def on_error(update: object, context) -> None:
    """Handler global de erro: registra no log e NUNCA derruba o bot."""
    logger.error("Erro não tratado no update %s:", update, exc_info=context.error)


def main() -> None:
    storage.load()

    if not config.BOT_TOKEN or "COLE_SEU_TOKEN" in config.BOT_TOKEN:
        raise SystemExit(
            "Configure o BOT_TOKEN em config.py (linha BOT_TOKEN = ...) antes de rodar o bot."
        )

    app = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .build()
    )

    app.add_handler(
        MessageHandler(tg_filters.TEXT & ~tg_filters.COMMAND, handlers.moderate_message)
    )
    app.add_handler(CommandHandler("status", handlers.cmd_status))
    app.add_handler(CommandHandler("resetwarns", handlers.cmd_resetwarns))
    app.add_error_handler(on_error)

    logger.info("Bot de moderação iniciado. Pressione Ctrl+C para parar.")
    # drop_pending_updates evita reprocessar uma fila enorme de mensagens
    # antigas acumuladas enquanto o bot estava offline (causa comum de
    # bots "engasgarem" logo ao iniciar)
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES,
        close_loop=False,
    )


if __name__ == "__main__":
    main()
