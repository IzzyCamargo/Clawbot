# Guia para clonar o “Claudio” (OpenClaw) em outra máquina/usuário

Este documento serve para você replicar **as configurações e o setup** que fizemos aqui, para outra pessoa ter um OpenClaw “igual” (mesmo padrão de uso, mesmas skills do workspace, mesmo comando de start no terminal).

> Importante (segurança): **NÃO copie tokens/credenciais** (gateway token, credenciais do WhatsApp, OAuth, etc.). Cada instalação deve gerar/autorizar as próprias credenciais.

---

## 0) O que foi configurado aqui (resumo)

- Workspace do agente em:
  - `/home/ti/Documentos/projects/claudio`
- Gateway local em loopback:
  - `ws://127.0.0.1:18789`
  - Service: `systemd --user` (enabled + running)
- Um comando único no terminal:
  - `start-claaudio` **NÃO** (o nome correto é) → `start-claudio`
  - abre o **TUI** (chat no terminal) via `openclaw tui`
- PATH ajustado para:
  - `~/.local/bin` (onde fica o `start-claudio`)
  - `~/.npm-global/bin` (onde ficam `clawhub` e `obsidian-cli`)
- Skills habilitadas (relevantes):
  - `github` (via `gh`)
  - `clawhub` (via `clawhub` CLI)
  - `obsidian` (via `obsidian-cli`)
  - skill de workspace: `gerador-de-fluxos-n8n`
- Pasta de persistência de workflows n8n:
  - `jsons/` dentro do workspace

---

## 1) Instalar OpenClaw na outra máquina

Siga o método recomendado por você/ambiente (npm/nvm). O requisito é ter o comando `openclaw` funcionando:

```bash
openclaw --version
```

> Nota: aqui o `openclaw` está vindo do Node + npm global do OpenClaw.

---

## 2) Criar/ativar o Gateway como serviço (para não rodar “install daemon” todo dia)

Rodar 1x:

```bash
openclaw gateway install
openclaw gateway start
openclaw gateway status
```

Isso cria o serviço:
- `~/.config/systemd/user/openclaw-gateway.service`

---

## 3) Definir o workspace do agente (para ficar em Documentos/projects)

Escolha um caminho (exemplo):

```bash
mkdir -p ~/Documentos/projects/claudio
openclaw config set agents.defaults.workspace "$HOME/Documentos/projects/claudio"
openclaw gateway restart
openclaw config get agents.defaults.workspace
```

---

## 4) Copiar somente o que é “safe” do nosso workspace

Você pode copiar **o workspace** (skills e regras), mas **não** copiar `~/.openclaw` inteiro.

### 4.1) Copiar pasta do workspace (recomendado)
Copie estas pastas/arquivos do repositório `/home/ti/Documentos/projects/claudio` para o novo workspace:

- `skills/gerador-de-fluxos-n8n/` (skill custom)
- `SOUL.md`, `USER.md`, `AGENTS.md`, `TOOLS.md` (opcional)
- `MEMORY.md` e `memory/` (opcional — contém contexto pessoal)
- `jsons/` (opcional — templates/exports n8n)

> Se a outra pessoa for um usuário diferente, **eu recomendo não copiar** `MEMORY.md` e `memory/` (privacidade).

---

## 5) Instalar as dependências das skills (github/clawhub/obsidian)

### 5.1) GitHub CLI (gh) via apt

```bash
sudo apt-get update
sudo apt-get install -y gh

gh --version
```

### 5.2) Configurar npm global no usuário (sem sudo)

```bash
mkdir -p ~/.npm-global
npm config set prefix "$HOME/.npm-global"
```

### 5.3) Instalar CLIs via npm

```bash
npm install -g clawhub obsidian-cli
```

O pacote `obsidian-cli` pode instalar o binário como `obsidian`.
Garanta um alias/symlink `obsidian-cli`:

```bash
ln -sf "$HOME/.npm-global/bin/obsidian" "$HOME/.npm-global/bin/obsidian-cli"
```

---

## 6) Garantir PATH para qualquer terminal (bash)

No `~/.bashrc`, garantir:

```bash
# OpenClaw: ensure ~/.local/bin is on PATH (for start-claudio, etc.)
if [ -d "$HOME/.local/bin" ] ; then
  case ":$PATH:" in
    *:"$HOME/.local/bin":*) ;;
    *) PATH="$HOME/.local/bin:$PATH" ;;
  esac
fi

# OpenClaw: npm global prefix (clawhub, obsidian-cli, etc.)
if [ -d "$HOME/.npm-global/bin" ] ; then
  case ":$PATH:" in
    *:"$HOME/.npm-global/bin":*) ;;
    *) PATH="$HOME/.npm-global/bin:$PATH" ;;
  esac
fi
```

E (opcional, mas ajuda login shell) criar `~/.bash_profile` que carrega profile + bashrc:

```bash
# ~/.bash_profile
if [ -f "$HOME/.profile" ]; then . "$HOME/.profile"; fi
if [ -f "$HOME/.bashrc" ]; then . "$HOME/.bashrc"; fi
```

---

## 7) Criar o comando único `start-claudio`

Crie o arquivo `~/.local/bin/start-claudio`:

```bash
mkdir -p ~/.local/bin
nano ~/.local/bin/start-claudio
chmod +x ~/.local/bin/start-claudio
```

Conteúdo recomendado (chat apenas no terminal, sem abrir Control):

```bash
#!/usr/bin/env bash
set -euo pipefail

export NODE_NO_WARNINGS=1

TOKEN="$(openclaw config get gateway.auth.token 2>/dev/null || true)"
export OPENCLAW_GATEWAY_TOKEN="$TOKEN"

openclaw gateway start >/dev/null 2>&1 || true

if ! openclaw tui --session main --token "$TOKEN"; then
  echo
  echo "[ERRO] Não consegui conectar o TUI ao Gateway."
  echo "URL tokenizada (não abre navegador automaticamente):"
  openclaw dashboard --no-open || true
  exit 1
fi
```

Teste:

```bash
start-claudio
```

---

## 8) Validar que as skills ficaram prontas

```bash
openclaw skills check
```

Esperado: `github`, `clawhub`, `obsidian` como **ready** (desde que `gh`, `clawhub`, `obsidian-cli` estejam no PATH).

---

## 9) Importante: o que NÃO deve ser copiado

Não copie para outra pessoa:
- `~/.openclaw/openclaw.json` inteiro (ele contém `gateway.auth.token`)
- `~/.openclaw/credentials/` (tokens e credenciais de canais)
- qualquer coisa do WhatsApp já linkado

A outra pessoa deve rodar o onboarding/configurar credenciais no próprio ambiente.

---

## 10) (Opcional) Export “limpo” do config

Se você quiser um `openclaw.json` modelo, crie manualmente um arquivo **sem** o token do gateway e sem credenciais, contendo só:
- `agents.defaults.workspace`
- `agents.defaults.model.primary`
- `gateway.port`, `gateway.mode`, `gateway.bind`, `gateway.auth.mode` (mas não o token)

E deixe o token ser gerado pelo `openclaw onboard/configure`.
