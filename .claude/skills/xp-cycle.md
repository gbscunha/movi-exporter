# Ciclo de Desenvolvimento — Movi Exporter

Pair programming humano + IA orientado ao plano atômico.

```
Planejar → Implementar → Verificar → Refatorar → Commitar → Documentar
```

---

## Etapa 1 — Planejar (humano decide, IA investiga)

Antes de escrever qualquer código:

1. Identificar a próxima fase ⬜ no `docs/desenvolvimento/PLANO_REFACTOR.md`
2. Ler todos os arquivos que serão modificados (nunca editar de memória)
3. Confirmar o escopo: o que muda, quais arquivos, qual o risco

**Regra:** se a fase envolve mais de 5 arquivos ou mudança arquitetural não coberta pelo plano, propor um sub-plano e esperar aprovação antes de prosseguir.

---

## Etapa 2 — Teste primeiro (Red) — quando aplicável

Antes de implementar, escrever o teste que descreve o comportamento esperado.

**Obrigatório para:**
- Features novas do zero (lógica de negócio — services, transformers, writers)
- Bug fixes — escrever o teste que reproduz o bug antes de corrigi-lo
- Transformações de dados (normalizer, transformer, exporter)

**Não se aplica:**
- Mudanças de GUI (CustomTkinter é difícil de testar)
- Remoção de dead code
- Infra (CI, spec, requirements)

```bash
pytest -q   # novos testes devem FALHAR aqui — confirma que testam algo real
```

Se o teste passa antes de implementar, ele não está testando nada útil — reescreva.

---

## Etapa 3 — Implementar (Green)

Executar exatamente o que está descrito na fase — nem mais, nem menos.

- Uma fase por vez. Não misturar com outras fases
- Para fases de dados Wialon: consultar `.claude/skills/wialon-api.md` antes de implementar
- Não inventar soluções não descritas no plano sem perguntar

```bash
pytest -q   # todos os testes devem passar aqui
```

---

## Etapa 4 — Verificar

```bash
pytest -q                 # todos os testes passam
ruff check src/           # zero erros de lint
```

- Abrir o app e testar o caminho principal manualmente
- Se mudou dados do export: abrir o arquivo gerado e conferir colunas e valores
- Se mudou `wialon_client.py`: testar com token real e conferir `app.log`

**Regra:** não avançar se qualquer item falhar. Diagnosticar e corrigir antes do commit.

---

## Etapa 5 — Refatorar

Com a implementação funcionando, revisar o código:

- Há duplicação que pode ser extraída?
- Os nomes de variáveis e funções estão claros?
- Segue os padrões do projeto (ver CLAUDE.md)?
- Algum `except Exception: pass` foi introduzido?
- Campos de sensor retornam `"N/D"` corretamente quando ausentes?

Rodar `pytest -q` novamente após qualquer mudança. Testes continuam passando.

**Regra:** nunca refatorar com testes falhando. Corrija os testes primeiro.

---

## Etapa 6 — Commitar

```bash
git add <arquivos-específicos>   # nunca git add .
git commit -m "tipo(escopo): descrição em imperativo"
```

Exemplos:
```
fix(wialon): ler odômetro do param bruto e converter metros para km
feat(gui): adicionar campo editável de token com toggle show/hide
refactor: remover SystemA e get_full_history não utilizados
ci: adicionar workflow de validação em push e pull_request
```

**Regra:** commits pequenos, um por fase. Nunca acumular uma onda inteira num commit gigante.

---

## Etapa 7 — Documentar

Atualizar o status na tabela do `PLANO_REFACTOR.md` (⬜ → ✅).

Se durante a implementação surgiu:
- Um obstáculo inesperado (ex: parâmetro Wialon com comportamento diferente)
- Uma decisão arquitetural não prevista
- Um padrão novo descoberto
- Um erro que o Claude cometeu e pode repetir

→ Atualizar o `CLAUDE.md` ou o skill relevante **agora**, antes da próxima sessão.

**Regra:** se você teve que explicar algo ao Claude durante a sessão e vai precisar explicar de novo no futuro, documente agora.

---

## Diagrama

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. PLANEJAR      Identificar fase, ler arquivos                │
│       ↓                                                         │
│  2. TESTE (Red)   Features novas, bugs e transformações         │
│                   Teste deve FALHAR antes de implementar        │
│       ↓                                                         │
│  3. IMPLEMENTAR   Mínimo para testes passarem (Green)           │
│       ↓                                                         │
│  4. VERIFICAR     pytest + ruff + GUI + export                  │
│       ↓                                                         │
│  5. REFATORAR     Melhorar com testes como rede de segurança    │
│       ↓                                                         │
│  6. COMMITAR      Pequeno, descritivo, em português             │
│       ↓                                                         │
│  7. DOCUMENTAR    Atualizar PLANO_REFACTOR.md + CLAUDE.md     │
│       ↓                                                         │
│  ← próxima fase ←──────────────────────────────────────────── │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quando parar e perguntar

- Decisão arquitetural não coberta pelo plano
- Arquivo inesperado encontrado que pode ser afetado
- Teste falhando por razão não óbvia após 2 tentativas
- Escopo da fase parece maior do que documentado

---

## Anti-patterns — o que não fazer

- **Implementar sem escrever o teste primeiro.** Para features novas e bugs, o Red vem antes do Green — sem exceção.
- **Escrever testes que já passam.** O Red existe para confirmar que o teste detecta falha real.
- **Implementar sem ler os arquivos.** Sempre ler antes de editar.
- **Misturar fases.** Se a Fase 03 não terminou, não começar a 04.
- **Commitar sem verificar.** O checklist existe para ser seguido.
- **Usar `git add .`** — pode incluir `.env`, `credentials.json` ou `*.log`.
- **Commit gigante.** Se tem mais de ~300 linhas alteradas, provavelmente deveria ter sido dividido.
- **Refatorar com testes falhando.** Corrija os testes primeiro.
- **Pular a documentação.** O CLAUDE.md é a memória do projeto. Se não documentou, o Claude vai cometer o mesmo erro na próxima sessão.
- **Deixar o Claude rodar no automático sem revisar.** A IA é o copiloto. O humano é o piloto. Sempre.
- **Hardcodar `flagsMask=65281` ou URL de geocodificação.** Ver regras críticas no CLAUDE.md e no `wialon-api.md`.
- **Usar `voltage` como tensão do veículo.** É a bateria interna do tracker (~4V), não a bateria do veículo.
