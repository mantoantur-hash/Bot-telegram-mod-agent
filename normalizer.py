# ======================================================================
#  normalizer.py
#  Funções de normalização de texto. NÃO PRECISA EDITAR ESTE ARQUIVO.
#  Aqui mora a lógica que detecta tentativas de burlar o filtro,
#  como "p a l a v r a", "p.a.l.a.v.r.a", "pal4vr4", "PORRA" etc.
# ======================================================================

import re
import unicodedata

# Mapa de caracteres "leetspeak" / símbolos parecidos com letras
LEET_MAP = {
    "4": "a", "@": "a", "^": "a",
    "3": "e", "€": "e",
    "1": "i", "!": "i", "|": "i",
    "0": "o", "()": "o",
    "5": "s", "$": "s",
    "7": "t", "+": "t",
    "8": "b",
    "9": "g",
    "vv": "w",
}


def remove_accents(text: str) -> str:
    """Remove acentos: 'é' -> 'e', 'ção' -> 'cao' etc."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def apply_leet(text: str) -> str:
    """Troca caracteres leetspeak simples (1 caractere) pela letra equivalente."""
    return "".join(LEET_MAP.get(ch, ch) for ch in text)


def normalize_basic(text: str) -> str:
    """
    Normalização leve: minúsculas + sem acento + leetspeak.
    Preserva espaços e pontuação (usada para checagem de palavra inteira).
    """
    if not text:
        return ""
    text = text.lower()
    text = remove_accents(text)
    text = apply_leet(text)
    return text


def normalize_compact(text: str) -> str:
    """
    Normalização agressiva: remove TUDO que não é letra/número.
    Usada apenas na checagem anti-burla, para pegar separações tipo
    'c u z @ 0', 'p.a.l.a.v.r.a', 'p_a_l_a_v_r_a'.
    """
    text = normalize_basic(text)
    return re.sub(r"[^a-z0-9]", "", text)


def tokenize(text: str) -> list:
    """Quebra o texto normalizado em palavras (tokens) alfanuméricos."""
    basic = normalize_basic(text)
    return re.findall(r"[a-z0-9]+", basic)
