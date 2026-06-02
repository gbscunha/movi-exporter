# Backlog Onda 2

> Itens descobertos durante o QA manual da v1.1.0 (após conclusão da Onda 1).
> Capturados na ordem em que aparecem — priorização e agrupamento em fases vem depois.

## Convenções

- **Severidade:** 🔴 bug · 🟡 UX ruim · 🟢 melhoria · 🔵 idéia
- **Esforço:** XS (<30min) · S (<2h) · M (<1d) · L (>1d)
- **Status:** ⬜ Todo · 🔄 Em andamento · ✅ Concluído · ⏸️ Adiado

---

## Itens

| # | Sev | Esforço | Status | Descrição | Origem |
|---|-----|---------|--------|-----------|--------|
| 01 | 🟡 | S | ⬜ | **Seletor de conta na sidebar** — hoje vive dentro do frame de Export e a Home não responde à troca. Mover pra sidebar como estado global do app. Remove o dropdown da tela de Export. | QA manual v1.1.0 |
| 03 | 🟢 | S | ⬜ | **Substituir emojis por icon font (FontAwesome 6 Free Solid)** — emojis renderizam inconsistente entre Win/macOS. Adotar **FontAwesome Free Solid** (1 TTF, ~150KB) — mantenedor já conhece de outros projetos. Vetor perfeito + cor seguindo o tema do CTk. Helper `src/gui/icons.py` com constantes nomeadas (`FA_SAVE`, `FA_EYE`...). No Windows precisa registrar via `ctypes` + `AddFontResourceEx`. Atualizar PyInstaller spec. Sem novas deps pip. ~15-18 ícones únicos. | QA manual v1.1.0 |
| 04 | 🟡 | XS | ⬜ | **Trocar de conta limpa cache silenciosamente** — usuário não percebe que precisa clicar 🔄 Carregar de novo. Opções: (a) auto-load, (b) mensagem "Clique 🔄 para carregar a Conta X" no scroll de veículos, ou (c) híbrido (auto-load se "Selecionar veículos" ativo). Decidir junto com #01 (seletor na sidebar). | QA manual v1.1.0 |
| 05 | 🔴 | XS | ⬜ | **`_show_vehicles` silencia se `self.service` ainda é None** — `home.py:158` faz `if not self.service: return` sem feedback. Reproduzível se usuário clica "Ver Veículos" antes do `_check_status_async` do boot terminar (rede lenta). Mostrar "Aguarde a conexão inicializar..." ou desabilitar o botão até `service` estar pronto. | Code review v1.1.0 |
| 06 | 🟢 | S | ⬜ | **UI/A — Design tokens** — criar `src/gui/design.py` centralizando cores semânticas (success/warning/error/muted), espaçamentos (`SPACE_SM`, `SPACE_MD`...), pesos de fonte e tamanhos. Base para todas as outras melhorias visuais. Substitui hex hardcoded espalhado pelos frames. | QA manual v1.1.0 |
| 07 | 🟢 | M | ⬜ | **UI/B — Home com conteúdo útil** — preencher a área vazia abaixo dos botões: card "Última exportação" (mês · timestamp · qtd registros · botão abrir pasta), sugestão "Você ainda não exportou Maio/2026" baseado em pastas existentes, quick stats anuais. Hoje a Home tem ~60% de espaço em branco. | QA manual v1.1.0 |
| 08 | 🟢 | S | ⬜ | **UI/C — Cards de status refinados** — ícone à esquerda (depende #03), hierarquia tipográfica: rótulo `text-sm muted`, valor numérico em peso bold e tamanho maior ("330" deve ser o protagonista do card). Status com cor semântica (depende #06). | QA manual v1.1.0 |
| 09 | 🟢 | XS | ⬜ | **UI/D — Sidebar polish** — separadores entre grupos (navegação · conta · ações), hover states mais visíveis nos itens inativos, ícones consistentes (depende #03). Footer "v1.1.0" clicável → abre release notes no browser. | QA manual v1.1.0 |
| 10 | 🟡 | M | ⬜ | **UI/E — Feedback in-frame (toast/snackbar)** — substituir `tkinter.messagebox.show*` (popup nativo macOS, quebra estética dark do CTk) por componente de toast/snackbar custom no canto da janela. Spinner inline para "Verificando..." em vez de texto estático. | QA manual v1.1.0 |
| 11 | 🟢 | S | ⬜ | **UI/F — Light mode auditado** — hoje `app.py` força `set_appearance_mode("dark")`. Settings tem dropdown de tema mas várias cores estão hardcoded em hex (verde `#2ecc71`, vermelho `#e74c3c`...) que ficam mal em light mode. Auditar usando design tokens (#06). | QA manual v1.1.0 |
| 12 | 🟡 | XS | ⬜ | **Export: Ano como dropdown/stepper** — hoje é `CTkEntry` aceitando "abc". Trocar por `CTkOptionMenu` (últimos 5 anos) ou `CTkSpinbox`. Validar input no `_start_export` também. | QA manual v1.1.0 |
| 13 | 🟢 | S | ⬜ | **Export: Checkboxes agrupados** — "Gerar consolidado" + "Upload para Drive" soltos no `_create_config_section`. Mover para sub-card "Opções" com label, melhor alinhamento. | QA manual v1.1.0 |
| 14 | 🟡 | M | ⬜ | **Export: Progresso real (não indeterminado)** — hoje `progress_bar.configure(mode="indeterminate")` fica pulsando. `VehicleService.export_monthly_data` já loop por veículos — emitir callback `on_progress(current, total)` pro frame mostrar "Processando 12/330 — Caminhão XYZ" + barra real. | QA manual v1.1.0 |
| 15 | 🟡 | S | ⬜ | **Export: Seleção de veículos repensada** — hoje 330 veículos em scroll, todos pré-marcados, e pra exportar 1 só tem que desmarcar 329. Mudanças: (a) **default "nenhum marcado"** quando radio "Selecionar veículos" é ativado (quem quer todos usa o outro radio "Todos os veículos"), (b) `CTkEntry` de busca por nome/placa filtrando em runtime, (c) botões "Marcar todos" / "Desmarcar todos" agindo só sobre os visíveis após filtro, (d) contador "X de Y selecionados", (e) validação: se 0 marcados ao clicar Iniciar, avisa antes de chamar API. | QA manual v1.1.0 |
| 16 | 🔵 | S | ⬜ | **Export: Confirmação para operação longa** — antes de iniciar, mostrar dialog "Vai processar 330 veículos em Abril/2026, estimativa ~12min, ok?". Estimativa baseada em qtd × média histórica. | QA manual v1.1.0 |
| 17 | 🟢 | S | ⬜ | **Export: Toolbar do log** — pequena barra acima do `log_text` com botões: 🗑 Limpar · 📋 Copiar · 💾 Salvar como `.txt`. Útil pra suporte (cliente envia o log do erro). | QA manual v1.1.0 |
| 18 | 🟡 | XS | ⬜ | **Settings: Page size como slider/stepper** — `CTkEntry` aceitando texto. Trocar por `CTkSlider` (range 100–5000, step 100) com label mostrando o valor. | QA manual v1.1.0 |
| 19 | 🔴 | M | ⬜ | **Settings: Google Drive sem botão reautenticar** — seção Drive é só leitura ("Encontrado" / "Não encontrado"). Se `token.json` expirar/corromper, usuário fica preso. Adicionar botão "🔄 Reautenticar" que dispara `DriveUploader.authenticate()` em background + status visual. | QA manual v1.1.0 |
| 20 | 🟡 | S | ⬜ | **Settings: Indicador "alterações não salvas"** — usuário edita campos mas nem todos têm botão salvar (EXPORT_DIR, page_size, folder_id…). Mostrar bullet alaranjado ao lado do label do campo modificado e botão flutuante "Salvar alterações" no rodapé da tela. | QA manual v1.1.0 |
| 21 | 🟢 | S | ⬜ | **Settings: Validação inline** — campos vazios/inválidos sinalizam erro embaixo do input (borda vermelha + texto curto). Atualmente só dá `messagebox` no clique em Salvar. | QA manual v1.1.0 |
| 22 | 🔵 | S | ⬜ | **Atalhos de teclado globais** — `Cmd/Ctrl+S` salvar configurações · `Cmd/Ctrl+,` settings · `Cmd/Ctrl+R` testar conexão · `Cmd/Ctrl+E` foco no botão Exportar · `Cmd/Ctrl+1/2/3` navegar entre tabs. Registrar via `self.bind_all`. | QA manual v1.1.0 |
| 23 | 🔵 | XS | ⬜ | **Diálogo "Sobre"** — acessível pela sidebar (footer da versão clicável, depende #09). Mostra: versão · link GitHub · créditos · licença · botão "Verificar atualizações" (já existe AutoUpdater). | QA manual v1.1.0 |
| 24 | 🔵 | L | ⬜ | **Histórico de exports persistente** — armazenar (SQLite ou JSON) últimos N exports com: mês/ano · conta · timestamp · qtd arquivos · status · path. Aparece como tabela na Home (item #07) com ações "abrir pasta" / "re-exportar". | QA manual v1.1.0 |
| 25 | 🟡 | XS | ⬜ | **Export: Log do progresso acumula entre execuções** — `log_text.delete("1.0", "end")` só é chamado em `_start_export`. Ao **carregar veículos** novamente (ou trocar de conta), o log mantém entradas antigas. Vi no QA: "715 veículos" + "330 veículos" no mesmo painel. Limpar ao trocar de conta e ao carregar veículos. | QA manual v1.1.0 |
| 26 | 🟡 | XS | ⬜ | **Export: Linhas do config desalinhadas** — Mês+Ano (2 cols), Formato+Consolidado+Conta (3 cols), Upload sozinho. Reorganizar em grid consistente 2×N: linha 1 = Mês/Ano, linha 2 = Formato/Conta (quando aplicável), linha 3 = Opções (checkboxes agrupados — depende #13). | QA manual v1.1.0 |
| 27 | 🟢 | XS | ⬜ | **Export: Esconder progress bar idle** — `progress_bar` fica visível com leve fração mesmo sem export rodando. `pack_forget()`/`grid_remove()` quando `is_exporting=False`, mostrar novamente ao iniciar. | QA manual v1.1.0 |
| 28 | 🟡 | XS | ⬜ | **Settings: Status do token muito sutil** — "Status: (não testado)" mesma cor que rótulos, parece desabilitado. Mudar para `⚠️ Não testado` em amarelo (ou auto-testar ao abrir Settings se token presente). Alinha com #21 (validação inline). | QA manual v1.1.0 |
| 29 | 🟢 | XS | ⬜ | **Settings: Renomear "Pasta ID" → "ID da pasta no Drive"** e adicionar botão 📋 Copiar ao lado do entry (texto truncado é frustrante). Bônus: link clicável "🔗 Abrir no Drive" → `https://drive.google.com/drive/folders/<id>`. | QA manual v1.1.0 |
| 30 | 🔵 | XS | ⬜ | **Settings: Renomear seção "Aparência" → "Geral"** e estruturar pra acomodar mais prefs (tema, idioma futuro, escala da UI, atalhos). Hoje 1 dropdown sozinho em seção inteira. | QA manual v1.1.0 |
| 31 | 🟡 | S | ⬜ | **EXPORT_DIR padrão deveria ser absoluto** — hoje default é `./exports` (relativo ao cwd). No app instalado via PyInstaller, o cliente abre o `.app`/`.exe` e o arquivo vai pra um lugar não óbvio (pasta do bundle, Library, Documents...). Mudar default pra `~/Documents/MoviExporter/exports/` (ou equivalente Windows via `Path.home()`). Migração: se já existe `./exports` com arquivos, manter; senão, usar o novo default. | QA manual v1.1.0 |
| 32 | 🟡 | XS | ⬜ | **"Sucesso 100%" com zero registros confunde** — quando todos os veículos retornam vazio, log mostra `Veículos processados: 330/330` + `Total de registros: 0` + `Taxa de sucesso: 100.0%` + `Arquivos gerados: 0`. Tecnicamente sucesso (nenhum erro), na prática zero entrega. Adicionar destaque tipo "⚠️ Nenhum dado disponível para o período — pode ser limite de retenção da conta Wialon ou veículos inativos." quando `total_records == 0`. | QA manual v1.1.0 (export Jan/2026) |
| 33 | 🔴 | XS | ✅ | ~~`pwr_int` ainda no fallback de `battery_voltage`~~ — **Resolvido na Fase 16 da Onda 1** com separação em 2 colunas (`vehicle_voltage` / `internal_battery_voltage`). | QA manual v1.1.0 (CSV VTR05 abr/2026) |
| 34 | 🔴 | S | ✅ | ~~Defaults do `DataNormalizer` mascaram `None` antes do `_fill_nd`~~ — **Resolvido na Fase 16 da Onda 1** (odometer e address agora `default=None`). | QA manual v1.1.0 (CSV VTR05 abr/2026) |
| 35 | 🟡 | XS | ✅ | ~~`_fill_nd` só checa `None`, não strings vazias~~ — **Resolvido na Fase 16 da Onda 1** (agora cobre `None` e `""`). | QA manual v1.1.0 |
| 36 | 🟢 | XS | ⬜ | **CLI não tem flag de conta** — `src/cli/main.py` instancia `VehicleService()` sem opção, sempre usa `WIALON_TOKEN` (Conta 1). Adicionar `--account 1|2` que escolhe `WIALON_TOKEN` ou `WIALON_TOKEN_2` e passa `account_name="Conta X"` pro export. Útil pra testes via terminal sem depender da GUI. | QA manual v1.1.0 |
| 37 | 🔴 | XS | ✅ | ~~`_normalize_sensor_name` confunde "Bateria do dispositivo"~~ — **Resolvido na Fase 17 da Onda 1**. Mappings específicos ("bateria do dispositivo", "bateria do rastreador", "device battery", "tracker battery") agora vêm antes dos ambíguos. | QA manual v1.1.0 |
| 38 | 🔴 | XS | ✅ | ~~Fallback Suntech para ignição (`mode`)~~ — **Resolvido na Fase 17 da Onda 1** via `SuntechProfile`. Validado em produção: 21.813 linhas do VTR05, agora 20.382 "Ligado" / 1.431 "Desligado" (antes era 100% Desligado). | QA manual v1.1.0 |
| 39 | 🔴 | XS | ✅ | ~~Fallback Suntech para odômetro (`m_asgn1`)~~ — **Resolvido na Fase 17 da Onda 1** via `SuntechProfile`. Validado em produção: odômetro 240.099 → 248.090 km no VTR05/abr-2026. | QA manual v1.1.0 |
| 40 | 🟢 | M | ✅ | ~~Perfis de tracker~~ — **Resolvido na Fase 17 da Onda 1**. Arquitetura `tracker_profiles/` criada com `SuntechProfile` + `DefaultProfile`. | QA manual v1.1.0 |
| 41 | 🟢 | XS | ✅ | ~~Logar warning quando tracker desconhecido cair no DefaultProfile~~ — **Resolvido**. `registry.py` agora loga uma vez por combinação `(model, rep_type)` quando msg cai no DefaultProfile com identificador populado. Cache module-level (resetável via `reset_unknown_tracker_cache()` em testes). 5 testes cobrindo cenários. | Discussão Fase 17 |
| 42 | 🟢 | S | ✅ | ~~Perfil JimiProfile (Jimi VL03)~~ — **Resolvido na Fase 18 da Onda 1**. Detecção por signature `serial`+`gps_real_up`+`data_mode` (validado em 430 msgs do CVM0H79). Mapping: `acc`→ignição, `pwr_ext`→tensão veículo, `voltage`→bateria interna. Validado em produção: 258 linhas, 246 Ligado / 12 Desligado, voltagens 12.9-14.4V. | Cliente Movi 2026-06-02 (Matheus, ID 402289789) |
| 43 | 🟢 | XS | ⬜ | **Validar família Suntech completa** — cliente confirmou que usa Suntech 4300/4315/340U/8300/8310 além do ST380. Arquitetura atual cobre via `rep_type='STT'`, mas séries 8xxx podem ter CAN/BLE com params extras (RPM, combustível) ainda não mapeados. Quando rodar export real de cada série, capturar mensagem e expandir `SuntechProfile.known_params()` se necessário. | Cliente Movi 2026-06-02 |

---

## Notas

- Dívida técnica conhecida (não vai para a Onda 2 a menos que vire problema):
  - `requirements.txt` ainda não está pinado via `pip-compile` — `requirements.in` está pronto, basta rodar.
  - `docs/wialon/TOKEN_AUTORIZACAO.md` referenciado no CLAUDE.md não existe — criar quando tiver flow OAuth ou só remover a menção.
