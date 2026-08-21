---
name: xp-cycle
description: Ciclo de desenvolvimento do Movi Exporter (Plan → Red → Green → Refactor → Commit → Documentar). Use SEMPRE que for implementar uma feature, corrigir um bug ou refatorar código neste repositório — mesmo que o usuário não peça explicitamente. Define o gate de verificação (pytest + ruff + GUI), as invariantes que nenhum teste pode violar e como fechar a entrega no CHECKLIST.md/JOURNAL.md.
---

# Ciclo de Desenvolvimento — Movi Exporter

Pair programming humano + IA orientado a fatias pequenas e verificáveis.
O humano é o piloto; a IA é o copiloto. Sempre.

```
Planejar → Teste (Red) → Implementar (Green) → Verificar → Refatorar → Commitar → Documentar
```

---

## Etapa 1 — Planejar (humano decide, IA investiga)

Antes de escrever qualquer código:

1. Ler **"Onde estou"** no `CHECKLIST.md` (root) — é a âncora de continuidade:
   fase atual, último concluído, em andamento, próximo passo
2. Se a feature tem spec em `docs/specs/`, ler a spec (critérios DADO/QUANDO/ENTÃO).
   Se não tem e a mudança é mais que um fix pontual, criar a spec a partir de
   `docs/specs/FEATURE-template.md` **antes** de planejar
3. Ler todos os arquivos que serão modificados (nunca editar de memória)
4. Confirmar o escopo: o que muda, quais arquivos, qual o risco
5. Entrar em Plan Mode e esperar aprovação do humano

**Regra:** se a fatia envolve mais de 5 arquivos ou mudança arquitetural não
coberta pela spec, propor um sub-plano (e um ADR em `docs/decisions/` se for
decisão estrutural) e esperar aprovação antes de prosseguir.

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

Executar exatamente o que está descrito na fatia — nem mais, nem menos.

- Uma fatia por vez. Não misturar com outras fatias
- Para mudanças em dados Wialon: consultar a skill `wialon-api`
  (`.claude/skills/wialon-api/SKILL.md`) antes de implementar
- Seguir `.claude/rules/code-conventions.md`
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
- Conferir a **checklist de invariantes** (abaixo)

**Regra:** não avançar se qualquer item falhar. Diagnosticar e corrigir antes do commit.

Após o commit, rodar `/my-verify`: um agente independente (`code-reviewer`)
re-executa os comandos e confere a entrega contra a spec e as invariantes.
Nunca aceitar "funciona" por relato — só por saída real.

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

**Regra:** commits pequenos, um por fatia. Nunca acumular uma onda inteira num
commit gigante. Mensagem = uma frase, sem corpo, sem trailers.

---

## Etapa 7 — Documentar (fecha a entrega)

Sempre, a cada entrega — é o que mantém o estado vivo:

1. **`CHECKLIST.md`** — atualizar só "Onde estou" + marcar o checkbox da fatia
   (`[ ]` → `[x]`, ou `[~]` se parcial). **Nunca** acrescentar blocos "Estado em
   DD-MM" no CHECKLIST — ele guarda estado, não história
2. **`JOURNAL.md`** — acrescentar uma entry datada no topo: branch, o que foi
   feito, decisões com racional (e alternativas rejeitadas), verificação real
   (saída de pytest/ruff)

Se durante a implementação surgiu:
- Um obstáculo inesperado (ex: parâmetro Wialon com comportamento diferente)
  → skill `wialon-api` ou `CLAUDE.md`
- Uma decisão arquitetural não prevista → ADR em `docs/decisions/`
- Um padrão novo descoberto → `.claude/rules/code-conventions.md`
- Um erro que o Claude cometeu e pode repetir → "Não faça" do `CLAUDE.md`
- Mudança no "quê" da feature → atualizar a spec em `docs/specs/`

→ Atualizar **agora**, antes da próxima sessão.

**Regra:** se você teve que explicar algo ao Claude durante a sessão e vai
precisar explicar de novo no futuro, documente agora.

---

## Stack de testes

| Camada | Ferramenta | Onde | Observação |
|--------|-----------|------|------------|
| Unidade (normalizer, transformer, exporter, tracker_profiles) | `pytest` | `tests/test_<modulo>.py` | Foco principal — lógica de dados |
| Cliente Wialon (paginação, re-auth, erros) | `pytest` + `requests-mock` | `tests/test_wialon_client.py` | Nunca gastar quota real em teste |
| Integração do pipeline | `pytest` | `tests/test_pipeline_integration.py`, `test_vehicle_service_export_golden.py` | Transformer → normalizer → exporter; golden file |
| Config / env / CLI | `pytest` | `tests/test_config.py`, `test_env_writer.py`, `test_cli.py` | |
| GUI (lógica pura: validação, tema, ícones, estado) | `pytest` (fixture `ctk_root`) | `tests/test_validation.py`, `test_theme.py`, `test_icons.py` | Pula sem display (CI headless) |
| GUI (telas, fluxo) | **manual** | — | CustomTkinter: ROI baixo para automatizar |
| Export real | **manual** com token real | `exports/` + `app.log` | Obrigatório se mudou `wialon_client.py` ou colunas |

Comandos: `pytest -q` · `ruff check src/` · `python -m src.gui.main` ·
`python -m src.cli.main test`. Rodar com o `venv` ativo.

---

## Checklist de invariantes (nenhuma entrega pode violar)

- [ ] **Wialon stateful:** `sid` para API, `gis_sid` para GIS; URLs vêm do login
- [ ] `flagsMask=0` em `messages/load_interval` (nunca `65281`)
- [ ] Odômetro convertido m → km; `pwr_ext` ≠ `voltage` (sem fallback)
- [ ] Geocode: POST, `uid` + sessão, sem `gis_sid`/`search_provider`, coords deduplicadas
- [ ] Campos de sensor ausentes → `"N/D"` (nunca `NaN`, `None` ou vazio visível)
- [ ] Colunas do export existentes preservadas (ordem e nome) — mudança = spec + golden atualizado
- [ ] GUI nunca importa `src.clients` — passa por `core/service_factory` → services
- [ ] Nenhum `except Exception: pass` — sempre `logger.debug(f"...: {e}")`
- [ ] Nenhum segredo no staging: `.env`, `credentials.json`, `client_secrets.json`, `token.json`, `*.log`
- [ ] Nenhuma dependência nova sem perguntar (PyInstaller)
- [ ] `__version__` em `src/gui/__init__.py` bate com a tag ao lançar release

---

## Diagrama

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  1. PLANEJAR      Ler CHECKLIST + spec, ler arquivos, Plan Mode │
│       ↓                                                         │
│  2. TESTE (Red)   Features novas, bugs e transformações         │
│                   Teste deve FALHAR antes de implementar        │
│       ↓                                                         │
│  3. IMPLEMENTAR   Mínimo para testes passarem (Green)           │
│       ↓                                                         │
│  4. VERIFICAR     pytest + ruff + GUI + export + /my-verify     │
│       ↓                                                         │
│  5. REFATORAR     Melhorar com testes como rede de segurança    │
│       ↓                                                         │
│  6. COMMITAR      Pequeno, descritivo, em português             │
│       ↓                                                         │
│  7. DOCUMENTAR    CHECKLIST (estado) + JOURNAL (história)       │
│       ↓                                                         │
│  ← próxima fatia ←─────────────────────────────────────────── │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quando parar e perguntar

- Decisão arquitetural não coberta pela spec/plano
- Arquivo inesperado encontrado que pode ser afetado
- Teste falhando por razão não óbvia após 2 tentativas
- Escopo da fatia parece maior do que documentado
- Invariante que parece precisar ser quebrada

---

## Anti-patterns — o que não fazer

- **Implementar sem escrever o teste primeiro.** Para features novas e bugs, o Red vem antes do Green — sem exceção.
- **Escrever testes que já passam.** O Red existe para confirmar que o teste detecta falha real.
- **Implementar sem ler os arquivos.** Sempre ler antes de editar.
- **Misturar fatias.** Se a fatia atual não terminou, não começar a próxima.
- **Commitar sem verificar.** O checklist existe para ser seguido.
- **Usar `git add .`** — pode incluir `.env`, `credentials.json` ou `*.log`.
- **Commit gigante.** Se tem mais de ~300 linhas alteradas, provavelmente deveria ter sido dividido.
- **Refatorar com testes falhando.** Corrija os testes primeiro.
- **Pular a documentação.** O CLAUDE.md é a memória do projeto. Se não documentou, o Claude vai cometer o mesmo erro na próxima sessão.
- **Fechar entrega sem atualizar CHECKLIST + JOURNAL.** A próxima sessão abre cega e refaz o que já foi feito.
- **Inflar o CHECKLIST com "Estado em DD-MM".** História datada vai para o JOURNAL; o CHECKLIST guarda só o estado corrente.
- **Rodar no automático sem revisar o plano.** Plan Mode existe para o humano aprovar antes do código.
- **Deixar o Claude rodar no automático sem revisar.** A IA é o copiloto. O humano é o piloto. Sempre.
- **Hardcodar `flagsMask=65281` ou URL de geocodificação.** Ver regras críticas no CLAUDE.md e na skill `wialon-api`.
- **Usar `voltage` como tensão do veículo.** É a bateria interna do tracker (~4V), não a bateria do veículo.
