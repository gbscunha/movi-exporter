# Decisões arquiteturais (ADRs)

Registro do **porquê** das decisões estruturais do Movi Exporter — contexto,
decisão, alternativas rejeitadas e consequências. Uma decisão = um arquivo,
numerado, nunca editado depois de aceito (substituir por um ADR novo e marcar o
antigo como "substituída por").

Criar a partir de [`ADR-template.md`](ADR-template.md). O "quê" das features
fica em [`../specs/`](../specs/); o estado corrente fica no `CHECKLIST.md`
(pessoal) e a cronologia no `JOURNAL.md` (pessoal).

| ADR | Título | Status | Data |
|-----|--------|--------|------|
| [0001](ADR-0001-estrutura-dev-ia.md) | Adotar estrutura de desenvolvimento assistido por IA | aceita | 2026-08-21 |

## Decisões anteriores a este registro

As decisões das ondas 1–5 (dois tokens fixos, `flagsMask=0`, odômetro m→km,
`N/D`, `service_factory`, tracker profiles, motorista via RFID, geocode via
POST etc.) estão documentadas em:

- [`docs/arquivo/CHECKLIST_DECISOES.md`](../arquivo/CHECKLIST_DECISOES.md) — checklist de decisões de 2026-05-22
- [`docs/arquivo/ANALISE_MELHORIAS.md`](../arquivo/ANALISE_MELHORIAS.md) — análise que originou as ondas
- `docs/arquivo/PLANO_ONDA_*.md` e `docs/desenvolvimento/PLANO_*.md` — racional por fase
- `CLAUDE.md` → "Wialon API — regras críticas" e "Não faça" — as regras resultantes

Não serão reescritas como ADRs retroativamente, salvo necessidade pontual.
