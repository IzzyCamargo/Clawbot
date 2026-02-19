---
name: gerador-de-fluxos-n8n
description: Criar workflows de automação compatíveis com n8n (gerar JSON completo e importável), explicar o funcionamento de cada node, e desenhar fluxogramas (Mermaid/ASCII). Use quando o usuário pedir para desenhar/gerar um fluxo do n8n, criar um workflow reutilizável/editável, documentar nodes/credenciais/dependências, ou converter uma ideia em um JSON de workflow do n8n. Não executar o fluxo; apenas criar.
---

# Gerador de Fluxos n8n

## Regra de confirmação (obrigatória)
Antes de atender qualquer solicitação de criação de workflow, **pedir confirmação explícita** do usuário com uma frase curta (ex.: “Confirma que eu devo gerar um workflow n8n agora?”).

## Regras do escopo (obrigatórias)
- **NUNCA executar** workflows. Apenas projetar e gerar.
- **NUNCA gerar JSON parcial**: sempre produzir o JSON completo do workflow n8n.
- **SEMPRE usar nodes oficiais do n8n** (n8n-nodes-base e nodes oficiais do n8n).
- **SEMPRE listar credenciais/dependências** e indicar onde configurar no n8n.
- Fluxos devem ser **reutilizáveis e editáveis** (evitar hardcode quando possível; preferir parâmetros/expressões).

## Persistência local do JSON (obrigatória)
- Sempre que gerar um workflow, **salvar um arquivo `.json`** dentro de `jsons/` no workspace do Claudio.
- O arquivo deve conter o **JSON completo** do workflow (o mesmo que foi entregue na resposta).
- Usar um **nome único por projeto**, em formato slug (sem espaços/emoji) e com data/hora, por exemplo:
  - `n8n-drive-to-pdf-2026-02-05-123900.json`
- Após salvar, **informar o caminho** do arquivo ao usuário.
- Se houver ambiente gráfico, **tentar abrir a pasta** `jsons/` (ex.: via `xdg-open`). Se não houver, apenas instruir o comando `cd`.

## Padrão obrigatório de resposta
A resposta deve seguir **exatamente** esta ordem:

1. 📌 Título do fluxo
2. 🧠 Visão geral do fluxo
3. 🔄 Explicação de cada node (em ordem de execução)
4. 🗂️ Fluxograma do fluxo (preferência Mermaid; se não der, ASCII)
5. 📦 JSON completo do workflow n8n

## Checklist de qualidade (antes de finalizar)
- O JSON tem: `name`, `nodes[]`, `connections`, `settings`, `active`.
- Todos os nodes citados na explicação existem no JSON e estão conectados corretamente.
- Credenciais: indicar **nome do tipo** (ex.: Postgres, HTTP Bearer, OpenAI) e **onde** no n8n o usuário configura.
- Nada “mágico”: se depender de URL/API/env, declarar.

## Referências
- Para padrões de estrutura e exemplos reais do seu ambiente (LangChain nodes, memory, Supabase/Postgres, módulos), ler: `references/padroes-n8n.md`.
- Comunidade n8n (para pesquisar casos/erros comuns e boas práticas): https://community.n8n.io/
