# Plano de Implementação — Onda 2 (v1.2.0)

> **Referência:** [`BACKLOG_ONDA_2.md`](BACKLOG_ONDA_2.md)
> **Ciclo:** `.claude/skills/xp-cycle.md`
> **Estratégia:** mista equilibrada — 1 bug crítico + dívida técnica urgente + ~10 quick wins + foundation visual + 1 refactor estrutural (sidebar com estado global).
> **Branch:** `feat/onda-2`
> **Regra:** cada fase é autônoma — não quebra o app se parar aqui. Commit ao final de cada fase.

---

## Tabela de acompanhamento

| # | Fase | Itens backlog | TDD | Esforço | Status |
|---|------|---------------|-----|---------|--------|
| 01 | Bugs e dívida CI urgente | #05, #46, #36 | 🔴 parcial | S | ✅ Concluído |
| 02 | Quick wins — Export | #25, #26, #27, #12, #32 | — | S | ✅ Concluído |
| 03 | Quick wins — Settings | #28, #29, #30, #18 | — | S | ✅ Concluído |
| 04 | Design tokens (foundation) | #06 | 🔴 parcial | S | ✅ Concluído |
| 05 | Seletor de conta global na sidebar | #01, #04 | 🔴 parcial | M | ⬜ Todo |
| 06 | Cards refinados na Home | #08 (depende #06) | — | S | ⬜ Todo |

**Total estimado:** ~10h de trabalho focado · 15 itens do backlog fechados.

**Legenda status:** ⬜ Todo · 🔄 Em andamento · ✅ Concluído · ⏸️ Bloqueado
**Legenda TDD:** 🔴 sim = teste antes de implementar · 🔴 parcial = só nos pontos com lógica testável · — = não aplicável

---

## Fora do escopo desta onda (ficam pra Onda 3)

Trabalhos grandes que precisam de fundação ou bloco próprio:

- **#03** FontAwesome (precisa de carregamento custom de TTF + handling Win32 via ctypes)
- **#07** Home com conteúdo útil (precisa do histórico #24 antes)
- **#19** Drive reauth (M)
- **#14** Progresso real (M — precisa propagar callback no service)
- **#15** Seleção repensada (S)
- **#10** Toast/snackbar (substitui messagebox em todo lugar)
- **#11** Light mode auditado (depende #06 estar consolidado)
- **#20, #21** Validação inline + indicador "alterações não salvas"
- **#44, #45** PyInstaller onedir + instruções Gatekeeper
- **#16, #17, #22, #23, #24** Features novas
- **#31** EXPORT_DIR absoluto (precisa migração cuidadosa)
- **#43** Validar família Suntech completa (quando aparecer veículo real de outro modelo)

---

## Fase 01 — Bugs e dívida CI urgente

**Objetivo:** fechar bug real do `_show_vehicles`, atualizar GitHub Actions antes da deprecação Node 20 (16/jun/2026) e dar suporte a `--account` no CLI (que faltou na Onda 1).
**TDD:** 🔴 parcial — testes só onde tem lógica testável (CLI flag).

### Itens

- **#05** — `_show_vehicles` em `home.py:158` silencia se `self.service` ainda é None. Reproduzível em rede lenta clicando "Ver Veículos" antes do boot terminar.
- **#46** — Atualizar actions para versões compatíveis com Node 24 (`checkout@v4` → `@v5`, `setup-python@v5` → `@v6`, `upload/download-artifact@v4` → `@v5`, `softprops/action-gh-release@v1` → `@v2`).
- **#36** — Adicionar `--account 1|2` no `src/cli/main.py`. Quando especificado, instancia `WialonClient(token=settings.WIALON_TOKEN_2)` e passa `account_name="Conta X"` para o export.

### Plano

**`src/gui/frames/home.py`** — `_show_vehicles`:
- Se `self.service is None`, mostrar `messagebox.showwarning("Aguarde", "Conexão ainda inicializando...")` em vez de retornar silenciosamente
- Bônus: desabilitar `btn_list` enquanto `service is None`, reabilitar após `_check_status_async` completar

**`.github/workflows/ci.yml`** e **`build.yml`**:
- Bump das actions conforme acima
- Rodar build local pra confirmar que ainda funciona

**`src/cli/main.py`**:
- Novo arg `--account` (choices `1`, `2`) com default `1`
- Função `cmd_test`, `cmd_list`, `cmd_export` aceitam parâmetro `account`
- Helper `_build_service(account: int) -> VehicleService` que escolhe o token e seta `account_name`

### Testes

`tests/test_cli.py` ← NOVO:
- `parse_vehicle_ids` (já existente, mas sem teste)
- `--account 2` instancia WialonClient com `WIALON_TOKEN_2`
- `--account` inválido → erro de validação

**Commit:** `fix: home silent fail + cli --account + bump GitHub Actions to v5/v6`

---

## Fase 02 — Quick wins de Export

**Objetivo:** 5 melhorias pequenas mas visíveis na tela de Export.
**TDD:** não aplicável — mudanças de GUI/layout.

### Itens

- **#25** — Log acumula entre execuções: limpar `log_text` ao trocar de conta e ao carregar veículos (não só ao iniciar export)
- **#26** — Linhas do `_create_config_section` desalinhadas: reorganizar em grid consistente 2×N
- **#27** — Esconder `progress_bar` quando `is_exporting=False` via `grid_remove()`
- **#12** — Ano como dropdown (`CTkOptionMenu` com últimos 5 anos) em vez de `CTkEntry` aceitando texto livre
- **#32** — Quando `total_records == 0`, mostrar aviso destacado: "⚠️ Nenhum dado disponível para o período" em vez de "✅ Taxa de sucesso 100.0%" enganoso

### Plano

**`src/gui/frames/export.py`**:
- `_load_vehicles` e `_on_account_changed` chamam `self.log_text.delete("1.0", "end")` antes de começar
- Reorganizar `_create_config_section` — colunas explícitas: Mês | Ano | Formato | Conta (se #01) | Opções (#13 será na próxima onda)
- `_set_progress_idle()` e `_show_progress_running()` escondem/mostram a barra
- Mês já é OptionMenu (Fase 13 Onda 1); converter ano com lista `[year_atual - i for i in range(5)]`
- Após export: se `result.total_records == 0`, log entry destacado em WARNING (amarelo) substituindo o "EXPORTAÇÃO CONCLUÍDA"

**Commit:** `feat(export): quick wins — clean log on context switch, year dropdown, hide idle progress, empty result warning`

---

## Fase 03 — Quick wins de Settings

**Objetivo:** 4 melhorias rápidas na Settings.
**TDD:** não aplicável.

### Itens

- **#28** — Status do token "(não testado)" muito sutil (cinza). Mudar para `⚠️ Não testado` em amarelo no estado inicial
- **#29** — "Pasta ID" → "ID da pasta no Drive"; adicionar botão 📋 ao lado do entry; bônus: link "🔗 Abrir no Drive" → `https://drive.google.com/drive/folders/<id>`
- **#30** — Seção "Aparência" → "Geral" (pra crescer com idioma, escala, atalhos futuros)
- **#18** — `page_size` como `CTkSlider` (range 100-5000, step 100) com label mostrando o valor

### Plano

**`src/gui/frames/settings.py`**:
- `token_status_label` inicializar com texto amarelo `#f39c12` em vez de cinza
- Helper `_create_copy_to_clipboard_button(text_provider)` reutilizável
- Folder ID: 3 widgets — Entry + Botão Copiar + Botão Abrir
- `_create_appearance_section` → `_create_general_section`
- `page_size_entry` → `page_size_slider` + `page_size_value_label`

**Commit:** `feat(settings): quick wins — status visibility, folder id helpers, page size slider, rename Aparência→Geral`

---

## Fase 04 — Design tokens (foundation)

**Objetivo:** criar `src/gui/design.py` centralizando cores semânticas + espaçamentos + tipografia. Base pra todas as melhorias visuais futuras.
**TDD:** 🔴 parcial — testes nas funções helper (`get_color`, ajuste de tema).

### Itens

- **#06** — Design tokens

### Plano

**`src/gui/design.py`** ← NOVO:

```python
"""Design tokens — fonte única para cores, espaçamentos e tipografia."""

# Cores semânticas (modo dark, padrão atual)
class Colors:
    SUCCESS = "#2ecc71"
    WARNING = "#f39c12"
    ERROR   = "#e74c3c"
    MUTED   = "#888888"
    INFO    = "#4cb5f9"

# Espaçamentos (em px)
class Space:
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 24
    XXL = 32

# Tipografia
class Font:
    SIZE_SM   = 11
    SIZE_BASE = 13
    SIZE_LG   = 16
    SIZE_XL   = 20
    SIZE_2XL  = 28

    WEIGHT_NORMAL = "normal"
    WEIGHT_BOLD   = "bold"

# Bordas
class Border:
    RADIUS_SM = 6
    RADIUS_MD = 8
    RADIUS_LG = 12
```

**Substituição inicial** — apenas as cores hex que já existem hardcoded:
- `home.py` (`StatusCard.set_value`): hex de success/error/warning → `Colors.SUCCESS` etc
- `settings.py` (token status, Drive creds label): mesmo
- `export.py` (LOG_COLORS): manter como está (níveis de log são caso específico, não muda)

Não fazer renomeação massiva agora — design tokens criados, próximas fases vão consumir.

### Testes

`tests/test_design_tokens.py`:
- `Colors.SUCCESS` é string hex válida
- Espaçamentos são int positivos crescentes
- Tipografia tem tamanhos coerentes

**Commit:** `feat(design): add design tokens module and migrate hex colors from frames`

---

## Fase 05 — Seletor de conta global na sidebar

**Objetivo:** mover o dropdown "Conta 1 / Conta 2" de dentro do frame Export para a sidebar, com estado compartilhado no app. Home passa a responder à troca também.
**TDD:** 🔴 parcial — testes da lógica de notificação entre app e frames.

### Itens

- **#01** — Mover seletor pra sidebar (estado global)
- **#04** — Feedback quando troca de conta (decidimos: auto-load se "Selecionar veículos" ativo, mensagem clara caso contrário)

### Plano

**`src/gui/app.py`**:
- `self.current_account: int = 1` como estado global
- `self.account_changed_callbacks: list[Callable[[int], None]] = []`
- Método `set_account(account: int)` que atualiza estado e chama callbacks
- Método `register_account_listener(cb)` que frames usam pra se inscrever

**`src/gui/frames/sidebar.py`**:
- Bloco "Conta" abaixo da navegação (condicional a `WIALON_TOKEN_2`)
- Visual: label "Conta:" + `CTkOptionMenu` ["Conta 1", "Conta 2"]
- Mudança chama `app.set_account(N)`

**`src/gui/frames/export.py`**:
- Remover dropdown local de conta (cleanup)
- `_build_service()` lê `self.master.master.current_account` (ou via callback registrado)
- Em `_on_account_changed`: limpa cache + log + se "Selecionar veículos" ativo, dispara `_load_vehicles` automaticamente

**`src/gui/frames/home.py`**:
- Registra listener no app
- Ao trocar de conta: rebuild `self.service` com token correto e re-roda `_check_status_async`

### Testes

`tests/test_app_account_state.py`:
- `set_account(2)` notifica callbacks registrados
- Cada frame chamado com novo valor
- Frame que se descadastra não recebe mais

**Commit:** `feat: global account selector in sidebar with broadcast to Home and Export`

---

## Fase 06 — Cards refinados na Home

**Objetivo:** aplicar design tokens (Fase 04) nos `StatusCard` da Home. Valor numérico vira protagonista, rótulo fica mais discreto.
**TDD:** não aplicável — mudança visual.

### Itens

- **#08** — Cards de status refinados

### Plano

**`src/gui/frames/home.py`** — refactor do `StatusCard`:
- Rótulo: `Font.SIZE_SM`, `Colors.MUTED`
- Valor: `Font.SIZE_XL`, `Font.WEIGHT_BOLD` (era `SIZE_LG`)
- Padding consistente com `Space.MD` e `Space.LG`
- Status (cor do valor): `Colors.SUCCESS/WARNING/ERROR` via método `set_value(value, status)`

### Antes vs depois (visual)

```
ANTES (atual):                DEPOIS:
┌──────────────────┐          ┌──────────────────┐
│ Wialon API       │          │ WIALON API       │  ← uppercase, muted
│ Conectado ✅      │          │                  │
└──────────────────┘          │ Conectado        │  ← peso bold, maior
                              └──────────────────┘
```

Ainda sem ícones (Fase #03 da Onda 3 vai trazer FontAwesome).

**Commit:** `feat(home): refine status cards with design tokens and typography hierarchy`

---

## Resumo de arquivos por fase

| Fase | Criados | Editados |
|------|---------|----------|
| 01 | `tests/test_cli.py` | `home.py`, `ci.yml`, `build.yml`, `cli/main.py` |
| 02 | — | `frames/export.py` |
| 03 | — | `frames/settings.py` |
| 04 | `src/gui/design.py`, `tests/test_design_tokens.py` | `home.py`, `settings.py` |
| 05 | `tests/test_app_account_state.py` | `app.py`, `frames/sidebar.py`, `frames/export.py`, `frames/home.py` |
| 06 | — | `frames/home.py` |

## Versão alvo

`__version__ = "1.2.0"` — bump no fim da Onda 2, antes do push da tag. Critérios SemVer:
- Refactor estrutural (sidebar com estado global) = mudança de comportamento visível
- Novos campos de configuração na GUI (slider, dropdowns, etc) = features
- Nada de breaking change no CSV ou na API pública

## Critério de pronto pra cada fase

1. `pytest -q` verde
2. `ruff check src/` clean
3. App abre via `python -m src.gui.main` e fluxo afetado funciona manualmente
4. Se fase mexeu em dados do export → CSV inspecionado
5. Commit feito com mensagem do plano
