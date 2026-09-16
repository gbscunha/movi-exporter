---
name: my-verify
description: Verificação independente de uma entrega no Movi Exporter — delega ao agente code-reviewer, que roda pytest/ruff de verdade, confere as invariantes (Wialon, N/D, GUI→services, segredos) e compara o que foi entregue com a spec/CHECKLIST. Use após commitar uma fatia, quando o usuário pedir "/my-verify", "verifica isso" ou "confere a entrega".
---

# /my-verify — verificação independente

Nunca confiar no relato de quem implementou (inclusive você mesmo). Um agente
separado roda os comandos e lê a saída real.

## 1. Delimitar o que verificar

- Escopo padrão: diff da branch atual contra a `main`
  (`git diff main...HEAD --stat` + `git diff main...HEAD`). Se `$ARGUMENTS`
  trouxer arquivos/commits/spec, usar isso.
- Localizar a spec correspondente em `docs/specs/` (se existir) e a fatia no
  `CHECKLIST.md`. São o contrato do "quê".

## 2. Delegar ao agente `code-reviewer`

Lançar o subagent `code-reviewer` (`.claude/agents/code-reviewer.md`) com:

- O diff (ou a lista de arquivos) e o caminho da spec/fatia do CHECKLIST.
- A instrução explícita: **rodar** `venv/bin/python -m pytest -q` e
  `venv/bin/ruff check src/`, colar a última linha de saída de cada um; não
  aceitar "passou" sem saída.
- A checklist de invariantes da skill `xp-cycle`.
- Pedir três listas: **bloqueantes**, **a mais** (entregue sem estar na
  spec/plano), **a menos** (critério da spec sem implementação ou sem teste).

## 3. Consolidar

Apresentar ao humano, nesta ordem:

1. Resultado real dos comandos (linha de saída).
2. Bloqueantes — arquivo:linha, risco, correção sugerida.
3. A mais / a menos em relação à spec.
4. Avisos (não bloqueiam): estilo, nomes, oportunidades de refactor.
5. Veredito: **pronto para fechar** ou **voltar para o ciclo** (com o que falta).

Se houver bloqueante, **não** atualizar CHECKLIST/JOURNAL como concluído —
marcar `[~]` e registrar o que falta no JOURNAL.
