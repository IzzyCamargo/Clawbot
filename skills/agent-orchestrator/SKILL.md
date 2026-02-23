# Skill: agent-orchestrator

## Visão Geral

Esta skill define o **orquestrador de agentes** do ecossistema do Lord Israel.

Objetivo:
- Dado um pedido do usuário (via Claudio), decidir **qual agente especializado** deve cuidar da tarefa.
- Centralizar a lógica de roteamento em um lugar declarativo (`agents/router.yaml`), versionado no Clawbot.

Ela **não executa a task final**; apenas responde:
- qual agente deve ser acionado;
- qual rota casou;
- quais sinais (palavras-chave / intenção) motivaram a decisão.

Quem executa a task é:
- o próprio Claudio (sessão principal), que então spawnará ou chamará o agente correto.

---

## Arquitetura

### Arquivos principais

- `agents/router.yaml` (no workspace e no repo Clawbot)
  - Define as rotas de alto nível:
    - nome da rota (ex.: "criação de agente");
    - agente responsável (slug);
    - critérios de match (keywords, intents simples).

- `skills/agent-orchestrator/` (esta pasta)
  - `SKILL.md` (este documento de especificação).
  - (futuro) `scripts/route.mjs` ou similar, se quisermos implementar a lógica em script.

---

## Contrato da Skill

### Entrada

Estrutura conceitual (lado do Claudio):

```jsonc
{
  "task_text": "texto bruto do pedido do usuário",
  "context": {
    "channel": "webchat | whatsapp | ...",
    "user": "Lord Israel",
    "hints": ["opcional: tipo de coisa que o Claudio já sabe que é"]
  }
}
```

Na prática, o Claudio pode chamar esta skill passando apenas o `task_text` e contexto mínimo.

### Saída

A skill deve devolver algo neste espírito:

```jsonc
{
  "agent_slug": "infinty-mamaco",
  "route_name": "inovação / novos agentes / especialização",
  "confidence": 0.85,
  "matched_keywords": ["novos agentes", "especializar agente"],
  "notes": "Roteado para Infinty Mamaco porque o pedido fala de criação de novos agentes e especialização estrutural."
}
```

Se nenhuma rota bater razoavelmente, pode devolver:

```jsonc
{
  "agent_slug": null,
  "route_name": null,
  "confidence": 0.0,
  "matched_keywords": [],
  "notes": "Nenhuma rota bateu com segurança; Claudio deve tratar diretamente ou perguntar ao usuário."
}
```

---

## Lógica de Roteamento (versão 0)

1. **Carregar `agents/router.yaml`**
   - Ler a chave `routing`.
   - Cada entrada contém:

     ```yaml
     - name: "..."
       agent: "slug"
       match:
         intents: [opcional]
         keywords: [lista de frases/palavras]
     ```

2. **Normalizar o `task_text`**
   - Lowercase.
   - Remover acentuação (opcional).

3. **Matching por keywords**
   - Para cada rota:
     - verificar quantas `keywords` aparecem no `task_text`.
   - Calcular uma pontuação simples (por exemplo: número de keywords encontradas / total de keywords da rota).

4. **Escolha da rota**
   - Selecionar a rota com maior pontuação.
   - Se a pontuação máxima for zero, retornar `agent_slug: null`.
   - Opcional: usar um limiar (ex.: `> 0`) para considerar a rota minimamente confiável.

5. **Retornar estrutura de decisão**
   - `agent_slug` = slug da rota selecionada.
   - `route_name` = nome da rota.
   - `confidence` = pontuação calculada (0.0–1.0 simples).
   - `matched_keywords` = lista de keywords que bateram.

---

## Agentes Suportados (versão inicial)

O roteador, via `agents/router.yaml`, deve saber lidar com:

- `hr-from-hell` (criação de agente)
- `infinty-mamaco` (inovação / novos agentes / especialização)
- `latrel` (segurança & compliance)
- `i-cant-take-it-anymore` (análise de performance de agentes)
- `i-hate-my-boss` (governança & hierarquia)
- `git-trickster` (versionamento Git / Clawbot)
- `the-chinese-firewall` (arquitetura estrutural de agentes)

Quando novos agentes forem criados, **eles devem ser adicionados também** em:
- `agents/*.md` e `agents/*.agent.yaml` (ficha + spec),
- `docs/agent-society.md` (documentação da sociedade),
- `agents/router.yaml` (roteamento).

Isso evita ter que "reencontrar" a lógica depois.

---

## Integração com o Claudio (sessão principal)

Comportamento desejado do Claudio:

1. Receber um pedido do Lord Israel.
2. Passar o `task_text` para a skill `agent-orchestrator`.
3. Analisar a resposta:
   - Se `agent_slug` ≠ null e `confidence` razoável:
     - Carregar o prompt do agente (`agents/<slug>.md` e/ou `<slug>.agent.yaml`).
     - Spawnar uma sessão daquele agente para executar a tarefa.
     - Agir como proxy: resumir/entregar o resultado ao Lord Israel.
   - Se `agent_slug` = null ou dúvida:
     - Perguntar ao Lord Israel se ele quer tratar como [opção A] ou [opção B], ou resolver ele mesmo.

Nesta versão, a skill em si é só o **decisor de roteamento**; a execução e o spawn ficam a cargo do Claudio e de futuras skills específicas (por exemplo, uma skill dedicada para Git Trickster, se necessário).

---

## Futuras Extensões

- Usar embeddings / matching semântico em vez de apenas keywords.
- Adicionar pesos diferentes por keyword.
- Suportar múltiplos agentes candidatos (para tarefas compostas).
- Registrar as decisões de roteamento em log (para análise futura pelo `I cant take it anymore`).

Por enquanto, a prioridade é: **ter um roteador simples, claro e versionado** para que o Claudio possa começar a agir como proxy inteligente dos agentes.
