# Padrões n8n (base local)

Use como inspiração de estilo e estrutura (sem copiar credenciais reais):

## 1) Orquestrador determinístico (chat)
Padrões observados no exemplo "Orquestrador Determinístico com Trava de Rota":
- Trigger: `n8n-nodes-base.chatTrigger` ou webhook/chat equivalente.
- Normalização: `n8n-nodes-base.set` para mapear `chatInput` -> campo de trabalho.
- Memória: `@n8n/n8n-nodes-langchain.memoryBufferWindow` (quando aplicável).
- Orquestração: `@n8n/n8n-nodes-langchain.agent` + várias `agentTool`.
- Conexões: `ai_languageModel`, `ai_tool`, `ai_memory`.
- Regra: roteamento determinístico (um agente por vez), sem loops.

## 2) Atendimento completo (webhook + histórico)
Padrões observados no exemplo "🤖 IA Atendimento":
- Entrada: `n8n-nodes-base.webhook`.
- Filtros defensivos: ignore grupos, ignore mensagens antigas.
- Modularização: `n8n-nodes-base.executeWorkflow` para sub-workflows.
- Persistência: `n8n-nodes-base.postgres` / `n8n-nodes-base.supabase` para histórico.
- Transformações: `n8n-nodes-base.code` para montar objetos.
- Switch por tipo de mensagem: `n8n-nodes-base.switch`.

## Boas práticas para gerar workflows reutilizáveis
- Evitar dados fixos (telefones, IDs, URLs específicas) quando o objetivo for reutilização.
- Usar expressões `={{ ... }}` e campos de entrada.
- Definir claramente credenciais necessárias por node (Postgres, Supabase, HTTP, OpenAI/Gemini etc.).
- Documentar “onde configurar” no n8n: Credentials + variáveis de ambiente + parâmetros do node.

## Checklist de export/import
- O JSON exportado deve ser importável via UI do n8n (Workflow -> Import from file).
- Manter `connections` consistente com os `name` dos nodes.
- Não depender de `id` fixo: o n8n pode regenerar IDs ao importar; o essencial são `name` + `connections`.
