# ADR-0001 — Adotar estrutura de desenvolvimento assistido por IA (specs, ADRs, CHECKLIST/JOURNAL, skills)

- **Data:** 2026-08-21
- **Status:** aceita
- **Origem:** guia `AI-DEV-SETUP.md` (arquivado em `docs/arquivo/AI-DEV-SETUP.md`)

## Contexto

O projeto já tinha `CLAUDE.md`, um ciclo (`xp-cycle`) e planos por onda
(`docs/desenvolvimento/PLANO_*.md`) com tabelas de status. Funcionou para as
ondas 1–5, mas: (a) cada onda recriava um plano-rastreador próprio e a skill
`/nova-fase` apontava para um plano já 100% concluído; (b) o "porquê" das
decisões ficava espalhado em planos arquivados; (c) `xp-cycle.md` e
`wialon-api.md` eram arquivos soltos, sem frontmatter — não eram carregados
automaticamente; (d) não havia verificação independente do trabalho da IA.

Restrições: mantenedor solo, 1 cliente em produção, brownfield — preservar o
que existe e as convenções reais do código.

## Decisão

1. **Estado vivo separado da história:** `CHECKLIST.md` (estado corrente:
   "Onde estou" + roadmap atômico + gavetas) e `JOURNAL.md` (entries datadas,
   append-only). Ambos **pessoais** (gitignored), no root. Um
   `docs/desenvolvimento/TEMPLATE_CHECKLIST.md` versionado permite recriar o
   CHECKLIST num clone novo.
2. **Spec-driven:** o "quê" de cada feature vai em `docs/specs/<slug>.md`
   (critérios DADO/QUANDO/ENTÃO). O "porquê" estrutural vai em **ADRs formais**
   em `docs/decisions/`.
3. **Skills como mecanismo único** de comandos: `/new-feature`, `/my-verify`,
   `/review`, `xp-cycle`, `wialon-api` em `.claude/skills/<nome>/SKILL.md` com
   frontmatter. Sem `.claude/commands/`. Rules em `.claude/rules/`, agente
   verificador em `.claude/agents/code-reviewer.md`.
4. **`/nova-fase` aposentada.** O "próximo passo" vive em "Onde estou".
5. **Convenção de idioma alinhada ao código real:** identificadores em inglês;
   docstrings, comentários, UI e mensagens em PT-BR.

## Alternativas rejeitadas

| Alternativa | Por que não |
|-------------|-------------|
| Rota leve de ADR (gaveta "Dívidas arquiteturais" + JOURNAL, sem `docs/decisions/`) | O dono preferiu ADR formal para ter as alternativas rejeitadas registradas num lugar estável e versionado. |
| CHECKLIST/JOURNAL versionados no repo | O dono preferiu mantê-los pessoais — roadmap e pendências não precisam ir para o repositório. |
| `.claude/commands/` para slash commands | O repo já havia migrado commands → skills; duas estruturas para a mesma coisa confundem. |
| Repontar `/nova-fase` para o CHECKLIST | Redundante com `/new-feature` + "Onde estou". |
| Manter "comentários em inglês" no CLAUDE.md | Contradizia ~todos os módulos; regra que o código não segue só gera ruído. |
| Retro-escrever ADRs das decisões das ondas 1–5 | Fora de escopo; a história está em `docs/arquivo/CHECKLIST_DECISOES.md` e nos planos arquivados. Fica como item opcional no CHECKLIST. |

## Consequências

- Positivas: toda sessão abre no mesmo ponto ("Onde estou"); skills carregam
  sozinhas quando relevantes; verificação por agente independente; o "quê" e o
  "porquê" persistem além do chat.
- Negativas / dívidas: CHECKLIST/JOURNAL não acompanham o repo — num clone novo
  é preciso recriá-los do template (histórico fica na máquina de origem).
  Mais arquivos para manter vivos (o passo 7 do ciclo existe para isso).
- Revisitar se: outro dev entrar no projeto (aí versionar CHECKLIST/JOURNAL),
  ou se a cerimônia de spec/ADR se mostrar pesada demais para fixes pontuais
  (o ciclo já permite pular a spec em bug pontual).
