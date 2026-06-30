# ======================================================================
#  CONFIGURAÇÃO DO BOT DE MODERAÇÃO
#  Edite SOMENTE este arquivo no dia a dia. Os outros arquivos não
#  precisam ser mexidos. Salve o arquivo e reinicie o bot para aplicar.
#  Deixar qualquer lista/valor vazio NÃO quebra o bot.
# ======================================================================

# ----------------------------------------------------------------------
# 1) TOKEN DO BOT (pegue com o @BotFather no Telegram)
# ----------------------------------------------------------------------
BOT_TOKEN = "COLE_SEU_TOKEN_AQUI"


# ----------------------------------------------------------------------
# 2) ADMINISTRADORES
# Coloque aqui o ID numérico (não o @usuario) dos admins que NUNCA
# devem ser moderados pelo bot. Para descobrir seu ID, fale com o bot
# @userinfobot no Telegram.
# ----------------------------------------------------------------------
ADMIN_IDS = [
    # 123456789,
]

# ID de um canal/grupo (numérico, geralmente começa com -100) onde o
# bot envia um log de cada ação de moderação. Deixe None para desativar.
LOG_CHANNEL_ID = None


# ----------------------------------------------------------------------
# 3) ANTI-SPAM / FLOOD (mensagens em excesso ou repetidas)
# ----------------------------------------------------------------------
# Quantas mensagens em SPAM_TIME_WINDOW segundos são consideradas spam.
SPAM_MAX_MESSAGES = 5
SPAM_TIME_WINDOW = 6          # segundos

# Quantas mensagens IDÊNTICAS seguidas (copy/paste) são permitidas
# antes de contar como spam.
SPAM_MAX_DUPLICATES = 3


# ----------------------------------------------------------------------
# 4) PUNIÇÕES (quantas infrações até mutar / banir)
# Toda vez que o bot detecta palavra proibida, link proibido ou spam,
# soma 1 infração para o usuário NAQUELE grupo.
# ----------------------------------------------------------------------
WARN_LIMIT_BEFORE_MUTE = 2     # a partir desta quantidade -> muta
WARN_LIMIT_BEFORE_BAN = 4      # a partir desta quantidade -> bane
MUTE_DURATION_MINUTES = 15     # duração do mute em minutos

DELETE_INFRACTING_MESSAGE = True     # apaga a mensagem que infringiu a regra
AUTO_DELETE_WARNING_SECONDS = 20     # apaga o aviso do bot depois de X segundos (0 = nunca apaga)


# ----------------------------------------------------------------------
# 5) LINKS
# ----------------------------------------------------------------------
BLOCK_LINKS = True                  # bloqueia http(s)://, www. etc.
BLOCK_TELEGRAM_INVITES = True       # bloqueia links t.me/ e convites de grupo/canal

# Domínios que SÃO permitidos mesmo com BLOCK_LINKS = True.
# Exemplo: ["youtube.com", "youtu.be", "seusite.com.br"]
ALLOWED_DOMAINS = [
    # "youtube.com",
    # "instagram.com",
]


# ----------------------------------------------------------------------
# 6) FILTRO INTELIGENTE ANTI-BURLA
# Detecta tentativas de driblar o filtro como "c u z @ 0", "p.a.l.a.v.r.a",
# "pal4vr4", "P-O-R-R-A" etc, convertendo o texto para uma forma "limpa"
# antes de comparar com a lista de palavras proibidas.
# ----------------------------------------------------------------------
STRICT_ANTI_EVASION = True

# Palavras com menos letras que isso NÃO entram na checagem anti-burla
# (evita bloquear palavras inocentes que têm 2-3 letras em comum com
# uma palavra proibida). A checagem normal (palavra inteira) continua
# valendo para qualquer tamanho.
MIN_WORD_LENGTH_FOR_EVASION_CHECK = 4


# ----------------------------------------------------------------------
# 7) LISTA DE PALAVRAS PROIBIDAS
# Formato de cada linha:   ("palavra em português", "en español", "in english")
# - Pode deixar espanhol/inglês em branco "" se não souber a tradução.
# - NÃO use ponto e vírgula, só vírgula entre as palavras.
# - Para adicionar uma nova palavra, copie uma linha vazia lá embaixo
#   e preencha. Não precisa apagar as linhas vazias que sobrarem.
# - Letras maiúsculas/minúsculas não importam, o bot ignora isso.
# ----------------------------------------------------------------------
BLOCKED_WORDS = [
    # ---- português            ---- espanhol            ---- inglês
    ("caralho",                 "carajo",                "fuck"),
    ("merda",                   "mierda",                "shit"),
    ("porra",                   "verga",                 "damn"),
    ("puta",                    "puta",                  "whore"),
    ("vagabunda",               "zorra",                 "slut"),
    ("vadia",                   "perra",                 "bitch"),
    ("corno",                   "cornudo",               "cuckold"),
    ("babaca",                  "pendejo",               "jerk"),
    ("otario",                  "tonto",                 "fool"),
    ("escroto",                 "asqueroso",             "scumbag"),
    ("desgraçado",              "maldito",               "damned"),
    ("arrombado",               "imbecil",               "asshole"),
    ("filho da puta",           "hijo de puta",          "son of a bitch"),
    ("vai se foder",            "vete a la mierda",      "fuck off"),
    ("idiota",                  "idiota",                "idiot"),
    ("imbecil",                 "imbecil",               "imbecile"),
    ("retardado",               "retrasado",             "retarded"),
    ("burro",                   "burro",                 "dumbass"),
    ("seu lixo",                "basura",                "trash"),
    ("vagabundo",               "vago",                  "loser"),

    # Slurs raciais, homofóbicos, religiosos etc não vêm prontos de
    # propósito. Se quiser bloquear algum, adicione na mesma estrutura
    # acima: ("palavra_pt", "palabra_es", "word_en"),

    # ---------------- 11 ESPAÇOS LIVRES PARA VOCÊ EDITAR ----------------
    ("", "", ""),
    ("", "", ""),
    ("", "", ""),
    ("", "", ""),
    ("", "", ""),
    ("", "", ""),
    ("", "", ""),
    ("", "", ""),
    ("", "", ""),
    ("", "", ""),
    ("", "", ""),
]


# ----------------------------------------------------------------------
# 8) LISTA BRANCA (palavras que parecem proibidas mas são inocentes)
# Se o filtro bloquear algo errado por engano, coloque a palavra aqui
# e ela nunca mais será bloqueada, mesmo que contenha pedaços de
# palavras da lista acima.
# Exemplo: "Cuiabá" contém "cu", "passei" contém "ass" em inglês etc.
# ----------------------------------------------------------------------
WHITELIST_WORDS = [
    # "cuiaba",
    # "classico",
]


# ----------------------------------------------------------------------
# 9) 11 ESPAÇOS EXTRAS PARA SUAS PRÓPRIAS FUNÇÕES/REGRAS
# Use como quiser: outra lista de palavras, lista de domínios extras,
# lista de IDs, apelidos proibidos etc. Ficar vazio ("[]") NUNCA causa
# erro nem trava o bot — o código já está preparado para isso.
# ----------------------------------------------------------------------
EXTRA_CUSTOM_1 = []
EXTRA_CUSTOM_2 = []
EXTRA_CUSTOM_3 = []
EXTRA_CUSTOM_4 = []
EXTRA_CUSTOM_5 = []
EXTRA_CUSTOM_6 = []
EXTRA_CUSTOM_7 = []
EXTRA_CUSTOM_8 = []
EXTRA_CUSTOM_9 = []
EXTRA_CUSTOM_10 = []
EXTRA_CUSTOM_11 = []

# Se você usar EXTRA_CUSTOM_1 até EXTRA_CUSTOM_11 para colocar PALAVRAS
# (strings simples, sem tupla), elas também passam a ser bloqueadas
# automaticamente junto com BLOCKED_WORDS. Exemplo:
# EXTRA_CUSTOM_1 = ["palavraproibida1", "palavraproibida2"]
