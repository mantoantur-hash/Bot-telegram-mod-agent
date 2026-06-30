# ======================================================================
#  filters.py
#  Lógica de detecção (spam, links, palavras proibidas + anti-burla).
#  NÃO PRECISA EDITAR ESTE ARQUIVO — as listas ficam todas em config.py
# ======================================================================

import re

import config
import storage
from normalizer import normalize_basic, tokenize


def _build_blocked_set() -> set:
    words = set()
    for tup in config.BLOCKED_WORDS:
        for w in tup:
            w = (w or "").strip().lower()
            if w:
                words.add(normalize_basic(w))

    # junta também os 11 espaços extras, caso o usuário tenha colocado
    # palavras simples (strings) neles
    extras = []
    for i in range(1, 12):
        extras.extend(getattr(config, f"EXTRA_CUSTOM_{i}", []) or [])
    for w in extras:
        if isinstance(w, str):
            w = w.strip().lower()
            if w:
                words.add(normalize_basic(w))

    return words


def _build_whitelist_set() -> set:
    out = set()
    for w in config.WHITELIST_WORDS:
        w = (w or "").strip().lower()
        if w:
            out.add(normalize_basic(w))
    return out


def reload_word_lists() -> None:
    """Recarrega as listas de palavras a partir do config.py.
    Chamada automaticamente quando o módulo é importado."""
    global BLOCKED_SET, WHITELIST_SET, MULTIWORD_PHRASES
    BLOCKED_SET = _build_blocked_set()
    WHITELIST_SET = _build_whitelist_set()
    # frases com mais de uma palavra (ex: "filho da puta") precisam de
    # checagem própria, já que não são um único token
    MULTIWORD_PHRASES = {w for w in BLOCKED_SET if " " in w}


BLOCKED_SET: set = set()
WHITELIST_SET: set = set()
MULTIWORD_PHRASES: set = set()
reload_word_lists()


_EVASION_PATTERN_CACHE = {}


def _evasion_pattern(word: str):
    """Constrói (e cacheia) um regex que detecta a palavra escrita com
    separadores entre as letras, ex.: 'p o r r a', 'p.o.r.r.a', 'p_o_r_r_a'.
    Exige limite de borda (não pode estar grudado em outra letra/número),
    o que evita pegar a palavra escondida dentro de outra palavra normal
    (ex.: 'porra' dentro de 'esporra' não bate, pois ali não há nenhum
    separador entre as letras)."""
    cached = _EVASION_PATTERN_CACHE.get(word)
    if cached is not None:
        return cached
    sep = r"[^a-z0-9]{1,3}"  # 1 a 3 caracteres de separação entre cada letra
    body = sep.join(re.escape(ch) for ch in word)
    pattern = re.compile(r"(?<![a-z0-9])" + body + r"(?![a-z0-9])")
    _EVASION_PATTERN_CACHE[word] = pattern
    return pattern


def contains_blocked_word(text: str):
    """Retorna a palavra/frase proibida encontrada, ou None se estiver tudo certo."""
    if not text:
        return None

    basic = normalize_basic(text)

    # 1) Frases com várias palavras (ex.: "filho da puta")
    for phrase in MULTIWORD_PHRASES:
        if phrase in WHITELIST_SET:
            continue
        if phrase in basic:
            return phrase

    # 2) Checagem de palavra inteira (rápida e sem falso positivo em
    #    substrings de palavras legítimas). Também já cobre leetspeak
    #    simples tipo "p0rr4" -> "porra", pois o leetspeak é aplicado
    #    na normalização antes de tokenizar.
    tokens = tokenize(text)
    token_set = set(tokens)
    for word in BLOCKED_SET:
        if " " in word:
            continue  # já tratado acima
        if word in WHITELIST_SET:
            continue
        if word in token_set:
            return word

    # 3) Checagem anti-burla: pega SOMENTE quando há separadores
    #    artificiais entre as letras (espaço, ponto, underline, símbolo).
    #    Palavras "coladas" dentro de outra palavra normal (ex.: "porra"
    #    dentro de "esporra") NÃO disparam aqui, porque ali não existe
    #    nenhum separador entre as letras.
    if config.STRICT_ANTI_EVASION:
        for word in BLOCKED_SET:
            if " " in word:
                continue
            if len(word) < config.MIN_WORD_LENGTH_FOR_EVASION_CHECK:
                continue
            if word in WHITELIST_SET:
                continue
            if _evasion_pattern(word).search(basic):
                return word

    return None


_FULL_URL_RE = re.compile(r"(?:https?://|www\.)\S+", re.IGNORECASE)
_INVITE_RE = re.compile(r"(t\.me/|telegram\.me/|telegram\.dog/)", re.IGNORECASE)


def contains_link(text: str) -> bool:
    if not text or not config.BLOCK_LINKS:
        return False

    urls = _FULL_URL_RE.findall(text)
    for url in urls:
        allowed = False
        for domain in config.ALLOWED_DOMAINS:
            if domain and domain.lower() in url.lower():
                allowed = True
                break
        if not allowed:
            return True

    if config.BLOCK_TELEGRAM_INVITES and _INVITE_RE.search(text):
        return True

    return False


def check_spam(chat_id, user_id, text: str, timestamp: float):
    """Retorna 'flood', 'duplicada' ou None."""
    history = storage.record_message(chat_id, user_id, text, timestamp)

    recent = [t for t, _ in history if timestamp - t <= config.SPAM_TIME_WINDOW]
    if len(recent) >= config.SPAM_MAX_MESSAGES:
        return "flood"

    if config.SPAM_MAX_DUPLICATES and text.strip():
        last_n = list(history)[-config.SPAM_MAX_DUPLICATES:]
        if len(last_n) == config.SPAM_MAX_DUPLICATES:
            texts = {t for _, t in last_n}
            if len(texts) == 1:
                return "duplicada"

    return None
