# Plano de Implementação — Onda 3 (v1.3.0)

> **Referência:** [`BACKLOG_ONDA_2.md`](BACKLOG_ONDA_2.md)
> **Ciclo:** `.claude/skills/xp-cycle.md`
> **Tema:** Experiência Visual — fundação de ícones/tema/feedback + redesign das telas.
> **Branch:** `feat/onda-3`
> **Regra:** cada fase é autônoma — não quebra o app se parar aqui. Commit ao final de cada fase.

---

## Tabela de acompanhamento

| # | Fase | Itens backlog | TDD | Esforço | Status |
|---|------|---------------|-----|---------|--------|
| 01 | Fundação: ícones (FontAwesome) | #03 | 🔴 parcial | S | ✅ Concluído |
| 02 | Fundação: light mode + toast | #11, #10 | 🔴 parcial | M | ✅ Concluído |
| 03 | Home + Sidebar + Sobre | #07, #09, #23 | 🔴 parcial | M | ⬜ Todo |
| 04 | Redesign do Export | #15, #14, #13, #17 | 🔴 parcial | M | ⬜ Todo |
| 05 | Settings polish | #20, #21 | — | S | ⬜ Todo |
| 06 | Atalhos de teclado | #22 | — | S | ⬜ Todo |

**Total estimado:** ~3-4 dias de trabalho focado · 13 itens do backlog fechados.

**Legenda status:** ⬜ Todo · 🔄 Em andamento · ✅ Concluído · ⏸️ Bloqueado
**Legenda TDD:** 🔴 parcial = só nos pontos com lógica testável · — = não aplicável (GUI pura)

---

## Por que esta ordem

Os emojis (🔌 💾 🔍 📂 ▶️…) são o que mais destoa visualmente e renderizam diferente entre Windows e macOS. Trocá-los por uma icon font **primeiro** (Fase 01) faz com que todo refinamento posterior já nasça consistente. Light mode e toast (Fase 02) são *cross-cutting* (afetam todas as telas) e consomem os design tokens da Onda 2. As telas (Fases 03-05) vêm por último, já usando toda a fundação.

---

## Fora do escopo desta onda (ficam pra Onda 4)

- **#19** 🔴 Drive reautenticar (bug — adiado por decisão; cliente não usa upload ativamente)
- **#24** Histórico de exports persistente (feature L — depende do #07 consolidado)
- **#16** Confirmação export longo (feature)
- **#31** EXPORT_DIR absoluto · **#44** PyInstaller onedir · **#45** Gatekeeper docs (técnicos/build)
- **#43** Validar família Suntech completa (depende de dado real)
- **#46** Bump actions Node 24 (aguardando upstream)

---

## Fase 01 — Fundação: ícones (FontAwesome)

**Objetivo:** substituir emojis por FontAwesome 6 Free Solid (icon font TTF). Vetorial, consistente Win/macOS, segue cor do tema.
**TDD:** 🔴 parcial — testes no helper de resolução de glifos/registro de fonte (não na renderização).

### Item: #03

### Plano

**Bundle da fonte:**
- `src/gui/assets/fontawesome-solid.ttf` (FontAwesome 6 Free Solid, ~150KB, licença SIL OFL)

**`src/gui/icons.py`** ← NOVO:
- Função `register_icon_font()` — registra o TTF em runtime. No Windows precisa de `ctypes` + `AddFontResourceEx`; macOS/Linux o Tk lê direto.
- `ICON_FONT(size)` — helper que retorna `CTkFont(family="Font Awesome 6 Free", size=size)`.
- Constantes nomeadas dos codepoints usados: `FA_PLUG`, `FA_EYE`, `FA_EYE_SLASH`, `FA_SAVE`, `FA_SEARCH`, `FA_FOLDER_OPEN`, `FA_PLAY`, `FA_REFRESH`, `FA_LIST`, `FA_GEAR`, `FA_HOME`, `FA_UPLOAD`, `FA_CLOUD`, `FA_CHECK`, `FA_XMARK`, `FA_TRIANGLE_WARNING`, `FA_COPY`, `FA_LINK`...

**Substituição dos emojis** (texto `"🔌 Wialon"` → `f"{FA_PLUG}  Wialon"` com `font=ICON_FONT(...)`):
- `sidebar.py` (🏠 📤 ⚙️)
- `settings.py` (🔌 👁 🔗 💾 🔍 ☁️ 📋 ⚙️)
- `export.py` (📂 ▶️ 🔄 + ícones de log)
- `home.py` (🔄 📋)

**`movi_exporter.spec`** — incluir o TTF em `datas`.

### Testes

`tests/test_icons.py`:
- Constantes de codepoint são strings de 1 caractere no range FontAwesome
- `register_icon_font()` não levanta em ambiente sem display (mock do ctypes no Windows)

**Decisão pendente:** confirmar a paleta exata de ícones (mapear cada emoji → glifo) — fazer no início da fase.

**Commit:** `feat(icons): replace emojis with FontAwesome icon font`

---

## Fase 02 — Fundação: light mode + toast

**Objetivo:** (a) auditar e habilitar o tema claro de verdade; (b) substituir `messagebox` nativo por toast/snackbar custom no estilo do app.
**TDD:** 🔴 parcial — lógica do gerenciador de toast (fila, auto-dismiss) é testável; renderização não.

### Itens: #11, #10

### Plano

**Light mode (#11):**
- `app.py` hoje força `set_appearance_mode("dark")`. Ler o tema salvo (persistir em `.env` via `env_writer`? ou settings).
- Garantir que os design tokens funcionem em ambos os modos. CustomTkinter suporta cor por tupla `(light, dark)` — avaliar migrar `Colors` para tuplas ou usar `ThemeManager`.
- Auditar cada tela em light mode e corrigir contrastes ruins.

**Toast/snackbar (#10):**
- `src/gui/components/toast.py` ← NOVO — componente que aparece no canto inferior, auto-some após N segundos, empilha múltiplos.
- Gerenciador `ToastManager` no app, exposto aos frames (similar ao `AccountState`).
- Substituir `messagebox.showinfo/showwarning/showerror` por toasts onde fizer sentido (manter messagebox só para confirmações bloqueantes reais).
- Spinner inline em "Verificando..." na Home (em vez de texto estático).

**Commit:** `feat(ui): light mode audit and toast/snackbar feedback system`

---

## Fase 03 — Home + Sidebar + Sobre

**Objetivo:** preencher a Home (hoje ~60% vazia), polir a sidebar e adicionar diálogo "Sobre".
**TDD:** 🔴 parcial — lógica de "última exportação" (ler pastas) e "sugestão de mês" é testável.

### Itens: #07, #09, #23

### Plano

**Home (#07):**
- Card "Última exportação": ler `EXPORT_DIR`, achar pasta mais recente, mostrar mês · timestamp · qtd arquivos · botão "Abrir pasta".
- Sugestão: "Você ainda não exportou {mês}/{ano}" baseado em quais pastas existem.
- Quick stats anuais (total de arquivos/exports no ano corrente).
- Helper `src/services/export_history.py` (leitura de pastas — sem persistência ainda; #24 fica pra Onda 4).

**Sidebar (#09):**
- Separadores entre grupos (navegação · conta · ações).
- Hover states mais visíveis nos itens inativos.
- Footer da versão clicável → abre release notes no browser.

**Sobre (#23):**
- `src/gui/dialogs/about_dialog.py` ← NOVO — versão · link GitHub · licença · botão "Verificar atualizações" (reusa AutoUpdater).
- Acessível pelo footer da sidebar.

**Commit:** `feat(home): useful dashboard content, sidebar polish and About dialog`

---

## Fase 04 — Redesign do Export

**Objetivo:** resolver a maior dor de UX do app (seleção de 330 veículos) + progresso real + organização visual.
**TDD:** 🔴 parcial — filtro de veículos e cálculo de progresso são testáveis.

### Itens: #15, #14, #13, #17

### Plano

**Seleção de veículos repensada (#15):**
- Default "nenhum marcado" ao ativar "Selecionar veículos".
- Campo de busca por nome/placa filtrando em runtime.
- Botões "Marcar todos" / "Desmarcar todos" (sobre os filtrados).
- Contador "X de Y selecionados".
- Validação: 0 selecionados ao iniciar → avisa antes de chamar a API.

**Progresso real (#14):**
- `VehicleService.export_monthly_data` emite callback `on_progress(current, total, vehicle_name)`.
- Barra determinada + label "Processando 12/330 — Caminhão XYZ".

**Checkboxes agrupados (#13):**
- "Gerar consolidado" + "Upload Drive" num sub-card "Opções".

**Toolbar do log (#17):**
- Botões acima do log: Limpar · Copiar · Salvar como `.txt`.

**Commit:** `feat(export): smart vehicle selection, real progress and log toolbar`

---

## Fase 05 — Settings polish

**Objetivo:** feedback de edição não salva e validação inline.
**TDD:** não aplicável — GUI.

### Itens: #20, #21

### Plano

- **#20** Indicador "alterações não salvas": bullet alaranjado ao lado de campos modificados; botão flutuante "Salvar alterações" no rodapé.
- **#21** Validação inline: campos inválidos/vazios mostram erro embaixo do input (borda + texto curto), em vez de só `messagebox` no clique.

**Commit:** `feat(settings): unsaved-changes indicator and inline validation`

---

## Fase 06 — Atalhos de teclado

**Objetivo:** atalhos globais para ações frequentes.
**TDD:** não aplicável — bindings de GUI.

### Item: #22

### Plano

- `Cmd/Ctrl+S` salvar configurações
- `Cmd/Ctrl+,` ir para Settings
- `Cmd/Ctrl+R` testar conexão
- `Cmd/Ctrl+E` foco no botão Exportar
- `Cmd/Ctrl+1/2/3` navegar entre as telas
- Registrar via `self.bind_all` no app; documentar no diálogo "Sobre".

**Commit:** `feat(ui): global keyboard shortcuts`

---

## Versão alvo

`__version__ = "1.3.0"` — bump no fim da onda. SemVer: várias features visíveis, sem breaking change.

## Critério de pronto por fase

1. `pytest -q` verde
2. `ruff check src/` clean
3. App abre via `python -m src.gui.main` e a tela afetada funciona manualmente
4. Commit com a mensagem do plano
5. Atualizar status no PLANO_ONDA_3.md e fechar itens no BACKLOG_ONDA_2.md
