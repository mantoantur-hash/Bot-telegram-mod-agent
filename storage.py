# ======================================================================
#  storage.py
#  Guarda infrações dos usuários em um arquivo JSON (sobrevive a
#  reinícios do bot) e o histórico recente de mensagens em memória
#  (usado só para detectar spam/flood, não precisa persistir).
#  NÃO PRECISA EDITAR ESTE ARQUIVO.
# ======================================================================

import json
import os
import threading
from collections import deque, defaultdict

INFRACTIONS_FILE = os.path.join(os.path.dirname(__file__), "infractions.json")

_lock = threading.Lock()

# (chat_id, user_id) -> deque[(timestamp, texto)]
_message_history = defaultdict(lambda: deque(maxlen=20))

# "chat_id:user_id" -> quantidade de infrações
_infractions = {}


def _key(chat_id, user_id) -> str:
    return f"{chat_id}:{user_id}"


def load() -> None:
    """Carrega infrações salvas em disco. Se o arquivo não existir ou
    estiver corrompido, simplesmente começa do zero (nunca quebra)."""
    global _infractions
    if os.path.exists(INFRACTIONS_FILE):
        try:
            with open(INFRACTIONS_FILE, "r", encoding="utf-8") as f:
                _infractions = json.load(f)
        except Exception:
            _infractions = {}
    else:
        _infractions = {}


def save() -> None:
    with _lock:
        try:
            with open(INFRACTIONS_FILE, "w", encoding="utf-8") as f:
                json.dump(_infractions, f)
        except Exception:
            # Nunca derruba o bot por erro de disco/permissão.
            pass


def record_message(chat_id, user_id, text: str, timestamp: float) -> deque:
    history = _message_history[(chat_id, user_id)]
    history.append((timestamp, text))
    return history


def get_history(chat_id, user_id) -> deque:
    return _message_history[(chat_id, user_id)]


def add_infraction(chat_id, user_id) -> int:
    k = _key(chat_id, user_id)
    with _lock:
        _infractions[k] = _infractions.get(k, 0) + 1
        count = _infractions[k]
    save()
    return count


def get_infractions(chat_id, user_id) -> int:
    return _infractions.get(_key(chat_id, user_id), 0)


def reset_infractions(chat_id, user_id) -> None:
    k = _key(chat_id, user_id)
    with _lock:
        _infractions.pop(k, None)
    save()
