---
name: new-feature
description: Dispara o ciclo completo para uma feature, bug ou refactor no Movi Exporter — spec → Plan Mode → teste (Red) → implementação (Green) → refactor → commit → CHECKLIST/JOURNAL. Use quando o usuário pedir "/new-feature <descrição>", "implementa X", "corrige Y" ou "vamos fazer Z".
---

# /new-feature — ciclo completo de uma entrega

Entrada: `$ARGUMENTS` = descrição curta da feature/bug/refactor. Se vazia, perguntar.

Siga a skill `xp-cycle` à risca. Este comando só encadeia as etapas:

## 1. Contexto (sem escrever código)

1. Ler **"Onde estou"** no `CHECKLIST.md`. Se a tarefa não está no roadmap,
   avisar e propor onde encaixar (ou se vai para "Backlog").
2. Se a mudança toca a Wialon (client, transformer, geocode, motorista), carregar
   a skill `wialon-api` antes de qualquer coisa.
3. Ler `.claude/rules/code-conventions.md`.

## 2. Spec (o "quê")

- Mudança mais que pontual → criar `docs/specs/<slug>.md` a partir de
  `docs/specs/FEATURE-template.md`, com critérios **DADO / QUANDO / ENTÃO**
  testáveis e "Fora de escopo" explícito.
- Bug pontual → o critério de aceitação é o próprio teste que reproduz o bug;
  pode pular a spec e registrar no JOURNAL.
- Decisão estrutural (nova camada, nova dependência, mudança de contrato do
  export) → rascunhar ADR em `docs/decisions/` a partir do `ADR-template.md`.

## 3. Plan Mode

Entrar em Plan Mode. Apresentar: arquivos a tocar, testes que serão escritos
primeiro, risco, impacto em colunas do export, se precisa de token real para
validar. **Esperar aprovação.** Plano > 5 arquivos → quebrar em fatias.

## 4. Red → Green → Refactor

- Escrever os testes primeiro (`tests/test_<modulo>.py`, nomes em PT-BR,
  `requests-mock` para Wialon). Rodar `pytest -q` e **mostrar a falha**.
- Implementar o mínimo. `pytest -q` verde. `ruff check src/` limpo.
- Refatorar com os testes protegendo. Conferir a checklist de invariantes da
  `xp-cycle`.
- GUI ou export mudaram → pedir ao humano que abra o app / o arquivo gerado
  (não dá para automatizar aqui) e registrar o resultado.

## 5. Commit

Branch `feat/<slug>` ou `fix/<slug>` a partir da `main`. `git add` por arquivo.
Mensagem: uma frase, Conventional Commits em PT-BR, sem corpo, sem trailers.
Sugerir a mensagem e **esperar o humano confirmar** antes de commitar.

## 6. Verificar

Rodar `/my-verify` (agente independente). Corrigir o que ele apontar como
bloqueante antes de fechar.

## 7. Documentar (obrigatório)

1. `CHECKLIST.md`: atualizar "Onde estou" + checkbox da fatia. Nada de
   "Estado em DD-MM".
2. `JOURNAL.md`: entry datada no topo (branch, o que, decisões + alternativas
   rejeitadas, verificação real).
3. Se surgiu padrão/regra/erro repetível → `CLAUDE.md`, rule ou skill relevante.
4. Se mudou comportamento visível ao cliente → `docs/manual/manual.html`.

Terminar com um resumo: o que foi entregue, o que ficou de fora e por quê,
e qual é o próximo passo segundo o CHECKLIST.
