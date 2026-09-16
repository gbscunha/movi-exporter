# CHECKLIST — estado vivo do Movi Exporter

> **Template versionado.** O `CHECKLIST.md` real fica no **root** e é pessoal
> (gitignored). Num clone novo: `cp docs/desenvolvimento/TEMPLATE_CHECKLIST.md CHECKLIST.md`
> e preencha "Onde estou" a partir do último JOURNAL/commit. Crie também um
> `JOURNAL.md` no root com o cabeçalho descrito no fim deste arquivo.

## Protocolo (como ler e como atualizar este arquivo)

- **Toda sessão abre aqui**, lendo "Onde estou". É a âncora de continuidade.
- **Toda entrega** mexe em exatamente duas coisas neste arquivo: o bloco
  "Onde estou" e o checkbox da fatia entregue. E gera **uma entry datada no
  `JOURNAL.md`** (mais recente no topo).
- **NUNCA** acrescentar blocos "Estado em DD-MM", logs ou histórico aqui. Estado
  vive aqui; história vive no JOURNAL. É o que mantém este arquivo curto (~250 linhas).
- Checkboxes: `[ ]` a fazer · `[x]` feito · `[~]` parcial (diga o que falta).
- Granularidade: uma fatia = um commit verificável (TDD quando aplicável).
- Gavetas no fim são contexto vivo — podar quando deixar de valer.
- O "quê" de uma feature fica em `docs/specs/`; o "porquê" estrutural em
  `docs/decisions/`. Aqui só o ponteiro.

---

## Onde estou

- **Versão em produção:** vX.Y.Z
- **Fase atual:**
- **Último concluído:**
- **Em andamento:**
- **Próximo passo:**
- **Bloqueado por:** nada

---

## Roadmap

### <Fase / onda>
- [ ] <fatia atômica> — spec: `docs/specs/<slug>.md`

### Backlog (a definir)
- [ ] ...

---

## Gavetas

### Carona no próximo PR
Mudanças pequenas demais para PR próprio — pegar junto com a próxima entrega.
- ...

### Pendências operacionais
Infra/ambiente fora do código (máquina do cliente, CI, tokens, Drive).
- ...

### Dívidas arquiteturais conhecidas
O que decidimos **não** fazer agora. Só o ponteiro — o racional está no ADR.
- ... → `docs/decisions/ADR-XXXX`

### Anotações (padrões permanentes)
Convenções duráveis que não merecem inflar o CLAUDE.md.
- ...

---

## Cabeçalho do JOURNAL.md (copiar ao criar)

```
# JOURNAL — história datada do Movi Exporter

> Estado vivo (onde estou, roadmap) fica no `CHECKLIST.md`. Este arquivo é
> append-only, **mais recente no topo**, e responde "por que essa decisão foi
> tomada?". Uma entry por entrega: data · branch · o que foi feito · decisões
> com racional (e alternativas rejeitadas) · verificação real (pytest/ruff).

---

## AAAA-MM-DD — <título> (`branch`)
**Feito:** ...
**Decisões:** ...
**Verificação:** pytest → ... · ruff → ...
**Próximo:** ...
```
