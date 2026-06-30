# 🛡️ Bot de Moderação para Telegram

Bot completo, leve e robusto para grupos do Telegram. Remove/pune
automaticamente: palavrões (PT/ES/EN), links e convites não
autorizados, e spam/flood de mensagens. Feito para **nunca travar**:
qualquer erro inesperado é capturado e registrado em log, sem derrubar
o bot.

---

## 📁 Arquivos

| Arquivo | O que é | Precisa editar? |
|---|---|---|
| `config.py` | **Todas** as configurações: token, palavras, tempos, punições | ✅ Sim, é o único que você mexe |
| `bot.py` | Inicia o bot | ❌ Não |
| `handlers.py` | Ações de moderação (apagar, mutar, banir, avisar) | ❌ Não |
| `filters.py` | Detecção de spam, links e palavras (com anti-burla) | ❌ Não |
| `normalizer.py` | Limpeza/normalização de texto (leetspeak, acentos) | ❌ Não |
| `storage.py` | Salva quantas infrações cada pessoa tem | ❌ Não |
| `infractions.json` | Criado automaticamente, guarda as infrações | ❌ Não |

---

## 🚀 Como colocar para rodar

1. **Crie o bot** no Telegram: fale com **@BotFather**, use `/newbot`,
   copie o token gerado.
2. **Cole o token** em `config.py`, na linha:
   ```python
   BOT_TOKEN = "COLE_SEU_TOKEN_AQUI"
   ```
3. **Instale as dependências** (Python 3.10 ou superior):
   ```bash
   pip install -r requirements.txt
   ```
4. **Adicione o bot ao seu grupo** e **torne-o administrador** com as
   permissões:
   - Apagar mensagens
   - Banir usuários
   - Restringir membros (necessário para mutar)
5. **Rode o bot**:
   ```bash
   python bot.py
   ```
6. Pronto. Mande uma palavra da lista no grupo para testar — a
   mensagem some e o usuário recebe um aviso.

### Manter rodando 24h (Linux/VPS)
```bash
nohup python bot.py > bot.log 2>&1 &
```
Ou use `systemd`, `pm2` ou `screen`/`tmux` para reiniciar
automaticamente caso o servidor reinicie.

---

## ✏️ Como editar tudo (sempre em `config.py`)

### Adicionar palavra proibida
Abra `config.py`, vá até `BLOCKED_WORDS` e preencha uma das 11 linhas
vazias no formato `("português", "espanhol", "inglês")`:
```python
("vagabundo", "vago", "loser"),
```
Pode deixar espanhol/inglês em branco: `("palavra", "", ""),` — funciona
normalmente.

### Liberar uma palavra que foi bloqueada por engano
Adicione em `WHITELIST_WORDS`:
```python
WHITELIST_WORDS = [
    "cuiaba",
]
```

### Mudar quantas mensagens até considerar spam
```python
SPAM_MAX_MESSAGES = 5     # 5 mensagens...
SPAM_TIME_WINDOW = 6      # ...em 6 segundos = spam
```

### Mudar quando muta / bane
```python
WARN_LIMIT_BEFORE_MUTE = 2   # 2ª infração = mute
WARN_LIMIT_BEFORE_BAN = 4    # 4ª infração = ban
MUTE_DURATION_MINUTES = 15   # quanto tempo dura o mute
```

### Permitir um site específico mesmo bloqueando links
```python
BLOCK_LINKS = True
ALLOWED_DOMAINS = ["youtube.com", "meusite.com.br"]
```

### Os "11 espaços extras"
No fim de `config.py` existem `EXTRA_CUSTOM_1` até `EXTRA_CUSTOM_11`.
São listas em branco para você usar como quiser (mais uma lista de
palavras, domínios, apelidos proibidos etc.) sem precisar tocar no
resto do código. Se colocar palavras simples (texto) dentro delas, elas
**já são bloqueadas automaticamente**, junto com `BLOCKED_WORDS`.

Depois de qualquer edição em `config.py`, **salve o arquivo e reinicie
o bot** (`Ctrl + C` e rode `python bot.py` de novo).

---

## 🧠 Como funciona o filtro anti-burla

Antes de comparar com a lista de palavras proibidas, o bot:
1. Converte tudo para minúsculas e remove acentos.
2. Troca símbolos parecidos com letras: `@`→a, `3`→e, `1`/`!`→i, `0`→o,
   `5`/`$`→s, `7`→t, `8`→b, `9`→g.
3. Remove espaços, pontos, traços e underlines para pegar tentativas
   como `c u z @ 0`, `p.a.l.a.v.r.a`, `p_a_l_a_v_r_a`.
4. Só aplica esse passo 3 em palavras com 4+ letras (configurável em
   `MIN_WORD_LENGTH_FOR_EVASION_CHECK`) — isso evita bloquear palavras
   inocentes que só têm 2-3 letras em comum com algo proibido.
5. Antes de bloquear, sempre confere se a palavra não está na
   `WHITELIST_WORDS`.

Esse equilíbrio (passo 4 + whitelist) é o que evita dois problemas
opostos: deixar passar palavrão disfarçado **e** banir gente que não
fez nada de errado.

---

## ❓ Problemas comuns (e por que este bot não sofre com eles)

- **"Trava/engasga com muita gente mandando mensagem ao mesmo tempo"**
  → O bot é assíncrono (`async/await`) e cada mensagem é processada de
  forma independente, sem bloquear as outras.
- **"Buga e para de responder do nada"** → Todo o processamento de
  mensagem fica dentro de um `try/except`. Se algo inesperado
  acontecer (ex.: usuário sem permissão, erro de rede), o erro é só
  registrado no log — o bot continua rodando normalmente.
- **"Funciona só no começo e depois trava"** → `drop_pending_updates`
  evita acumular uma fila gigante de mensagens antigas ao reiniciar, e
  o histórico de spam usa `deque` com tamanho fixo (não cresce
  infinitamente e não consome memória sem limite).
- **"Perde as infrações se reiniciar o bot"** → As infrações ficam
  salvas em `infractions.json`, recarregadas automaticamente ao
  iniciar.
- **"Bot não consegue mutar/banir"** → Confirme que o bot é
  **administrador** do grupo com permissão de restringir/banir
  membros. Sem isso, o Telegram recusa a ação (o erro fica registrado
  no log, mas o bot não cai).

---

## 💬 Comandos disponíveis no grupo

- `/status` — mostra quantas infrações você tem no grupo.
- `/resetwarns` — (responder à mensagem da pessoa) zera as infrações
  dela. Só funciona para quem está em `ADMIN_IDS`.

---

## ⚠️ Sobre a lista de palavras

A lista que já vem pronta em `config.py` cobre xingamentos e insultos
comuns em português, espanhol e inglês. Ela **não** inclui
propositalmente ofensas raciais, homofóbicas ou religiosas — se você
quiser bloquear esse tipo de termo no seu grupo, adicione manualmente
seguindo o mesmo formato `("palavra_pt", "palabra_es", "word_en")`.
