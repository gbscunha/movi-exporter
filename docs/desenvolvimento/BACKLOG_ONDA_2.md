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
| 01 | 🟡 | S | ✅ | ~~Seletor de conta na sidebar~~ — **Resolvido na Fase 05 da Onda 2**. `AccountState` (observer) compartilhado entre sidebar/Home/Export. Dropdown removido do Export, movido pra sidebar (condicional a TOKEN_2). 10 testes. | QA manual v1.1.0 |
| 03 | 🟢 | S | ✅ | ~~Substituir emojis por icon font (FontAwesome 6 Free Solid)~~ — **Resolvido na Fase 01 da Onda 3**. Glifos renderizados como CTkImage via Pillow (não fonte direta — permite ícone+texto no mesmo botão), com cache e variantes light/dark. TTF vendorizado (414KB, SIL OFL) + spec atualizado. Emojis de chrome (botões/títulos/status) substituídos em sidebar/home/export/settings; emojis de log mantidos (conteúdo de textbox). Pillow adicionado às deps. 6 testes. | QA manual v1.1.0 |
| 04 | 🟡 | XS | ✅ | ~~Trocar de conta limpa cache silenciosamente~~ — **Resolvido na Fase 05 da Onda 2**. Ao trocar de conta: log mostra "Conta alterada para Conta X"; se modo "Selecionar veículos" está ativo, recarrega a lista automaticamente (opção híbrida). | QA manual v1.1.0 |
| 05 | 🔴 | XS | ✅ | ~~`_show_vehicles` silencia se `self.service` ainda é None~~ — **Resolvido na Fase 01 da Onda 2**. `btn_list` começa desabilitado e é habilitado só quando `_check_status_async` conclui com sucesso. Fallback com `_show_warning` se algum estado inconsistente cair lá. | Code review v1.1.0 |
| 06 | 🟢 | S | ✅ | ~~UI/A — Design tokens~~ — **Resolvido na Fase 04 da Onda 2**. `src/gui/design.py` com Colors/Space/Font/Border. Hex semânticos migrados em home, settings, status_bar e update_dialog. 6 testes. | QA manual v1.1.0 |
| 07 | 🟢 | M | ⬜ | **UI/B — Home com conteúdo útil** — preencher a área vazia abaixo dos botões: card "Última exportação" (mês · timestamp · qtd registros · botão abrir pasta), sugestão "Você ainda não exportou Maio/2026" baseado em pastas existentes, quick stats anuais. Hoje a Home tem ~60% de espaço em branco. | QA manual v1.1.0 |
| 08 | 🟢 | S | ✅ | ~~UI/C — Cards de status refinados~~ — **Resolvido na Fase 06 da Onda 2**. Rótulo muted em maiúsculas (SIZE_SM), valor protagonista (SIZE_XL bold), espaçamentos via tokens. Ícone à esquerda fica para quando #03 (FontAwesome) entrar. | QA manual v1.1.0 |
| 09 | 🟢 | XS | ⬜ | **UI/D — Sidebar polish** — separadores entre grupos (navegação · conta · ações), hover states mais visíveis nos itens inativos, ícones consistentes (depende #03). Footer "v1.1.0" clicável → abre release notes no browser. | QA manual v1.1.0 |
| 10 | 🟡 | M | ⬜ | **UI/E — Feedback in-frame (toast/snackbar)** — substituir `tkinter.messagebox.show*` (popup nativo macOS, quebra estética dark do CTk) por componente de toast/snackbar custom no canto da janela. Spinner inline para "Verificando..." em vez de texto estático. | QA manual v1.1.0 |
| 11 | 🟢 | S | ⬜ | **UI/F — Light mode auditado** — hoje `app.py` força `set_appearance_mode("dark")`. Settings tem dropdown de tema mas várias cores estão hardcoded em hex (verde `#2ecc71`, vermelho `#e74c3c`...) que ficam mal em light mode. Auditar usando design tokens (#06). | QA manual v1.1.0 |
| 12 | 🟡 | XS | ✅ | ~~Export: Ano como dropdown/stepper~~ — **Resolvido na Fase 02 da Onda 2**. `CTkOptionMenu` com últimos 5 anos. | QA manual v1.1.0 |
| 13 | 🟢 | S | ⬜ | **Export: Checkboxes agrupados** — "Gerar consolidado" + "Upload para Drive" soltos no `_create_config_section`. Mover para sub-card "Opções" com label, melhor alinhamento. | QA manual v1.1.0 |
| 14 | 🟡 | M | ⬜ | **Export: Progresso real (não indeterminado)** — hoje `progress_bar.configure(mode="indeterminate")` fica pulsando. `VehicleService.export_monthly_data` já loop por veículos — emitir callback `on_progress(current, total)` pro frame mostrar "Processando 12/330 — Caminhão XYZ" + barra real. | QA manual v1.1.0 |
| 15 | 🟡 | S | ⬜ | **Export: Seleção de veículos repensada** — hoje 330 veículos em scroll, todos pré-marcados, e pra exportar 1 só tem que desmarcar 329. Mudanças: (a) **default "nenhum marcado"** quando radio "Selecionar veículos" é ativado (quem quer todos usa o outro radio "Todos os veículos"), (b) `CTkEntry` de busca por nome/placa filtrando em runtime, (c) botões "Marcar todos" / "Desmarcar todos" agindo só sobre os visíveis após filtro, (d) contador "X de Y selecionados", (e) validação: se 0 marcados ao clicar Iniciar, avisa antes de chamar API. | QA manual v1.1.0 |
| 16 | 🔵 | S | ⬜ | **Export: Confirmação para operação longa** — antes de iniciar, mostrar dialog "Vai processar 330 veículos em Abril/2026, estimativa ~12min, ok?". Estimativa baseada em qtd × média histórica. | QA manual v1.1.0 |
| 17 | 🟢 | S | ⬜ | **Export: Toolbar do log** — pequena barra acima do `log_text` com botões: 🗑 Limpar · 📋 Copiar · 💾 Salvar como `.txt`. Útil pra suporte (cliente envia o log do erro). | QA manual v1.1.0 |
| 18 | 🟡 | XS | ✅ | ~~Settings: Page size como slider/stepper~~ — **Resolvido na Fase 03 da Onda 2**. `CTkSlider` 100–5000 (passo 100) com label do valor ao lado. | QA manual v1.1.0 |
| 19 | 🔴 | M | ⬜ | **Settings: Google Drive sem botão reautenticar** — seção Drive é só leitura ("Encontrado" / "Não encontrado"). Se `token.json` expirar/corromper, usuário fica preso. Adicionar botão "🔄 Reautenticar" que dispara `DriveUploader.authenticate()` em background + status visual. | QA manual v1.1.0 |
| 20 | 🟡 | S | ⬜ | **Settings: Indicador "alterações não salvas"** — usuário edita campos mas nem todos têm botão salvar (EXPORT_DIR, page_size, folder_id…). Mostrar bullet alaranjado ao lado do label do campo modificado e botão flutuante "Salvar alterações" no rodapé da tela. | QA manual v1.1.0 |
| 21 | 🟢 | S | ⬜ | **Settings: Validação inline** — campos vazios/inválidos sinalizam erro embaixo do input (borda vermelha + texto curto). Atualmente só dá `messagebox` no clique em Salvar. | QA manual v1.1.0 |
| 22 | 🔵 | S | ⬜ | **Atalhos de teclado globais** — `Cmd/Ctrl+S` salvar configurações · `Cmd/Ctrl+,` settings · `Cmd/Ctrl+R` testar conexão · `Cmd/Ctrl+E` foco no botão Exportar · `Cmd/Ctrl+1/2/3` navegar entre tabs. Registrar via `self.bind_all`. | QA manual v1.1.0 |
| 23 | 🔵 | XS | ⬜ | **Diálogo "Sobre"** — acessível pela sidebar (footer da versão clicável, depende #09). Mostra: versão · link GitHub · créditos · licença · botão "Verificar atualizações" (já existe AutoUpdater). | QA manual v1.1.0 |
| 24 | 🔵 | L | ⬜ | **Histórico de exports persistente** — armazenar (SQLite ou JSON) últimos N exports com: mês/ano · conta · timestamp · qtd arquivos · status · path. Aparece como tabela na Home (item #07) com ações "abrir pasta" / "re-exportar". | QA manual v1.1.0 |
| 25 | 🟡 | XS | ✅ | ~~Export: Log do progresso acumula entre execuções~~ — **Resolvido na Fase 02 da Onda 2**. Helper `_clear_log()` chamado ao trocar de conta, carregar veículos e iniciar export. | QA manual v1.1.0 |
| 26 | 🟡 | XS | ✅ | ~~Export: Linhas do config desalinhadas~~ — **Resolvido na Fase 02 da Onda 2**. Grid 4 colunas consistente: linha 0 Mês/Ano, linha 1 Formato/Conta, linha 2 checkboxes. | QA manual v1.1.0 |
| 27 | 🟢 | XS | ✅ | ~~Export: Esconder progress bar idle~~ — **Resolvido na Fase 02 da Onda 2**. `grid_remove()` no idle, `grid()` ao iniciar export, escondida de novo no reset. | QA manual v1.1.0 |
| 28 | 🟡 | XS | ✅ | ~~Settings: Status do token muito sutil~~ — **Resolvido na Fase 03 da Onda 2**. Com token salvo mostra "⚠️ Não testado — clique em 🔍 Testar" em amarelo; sem token, cinza "sem token configurado". | QA manual v1.1.0 |
| 29 | 🟢 | XS | ✅ | ~~Settings: Renomear "Pasta ID" → "ID da pasta no Drive"~~ — **Resolvido na Fase 03 da Onda 2**. ID mostrado completo + botão 📋 Copiar + botão 🔗 Abrir no Drive. | QA manual v1.1.0 |
| 30 | 🔵 | XS | ✅ | ~~Settings: Renomear seção "Aparência" → "Geral"~~ — **Resolvido na Fase 03 da Onda 2**. Seção agora "⚙️ Geral", pronta para acomodar futuras prefs. | QA manual v1.1.0 |
| 31 | 🟡 | S | ⬜ | **EXPORT_DIR padrão deveria ser absoluto** — hoje default é `./exports` (relativo ao cwd). No app instalado via PyInstaller, o cliente abre o `.app`/`.exe` e o arquivo vai pra um lugar não óbvio (pasta do bundle, Library, Documents...). Mudar default pra `~/Documents/MoviExporter/exports/` (ou equivalente Windows via `Path.home()`). Migração: se já existe `./exports` com arquivos, manter; senão, usar o novo default. | QA manual v1.1.0 |
| 32 | 🟡 | XS | ✅ | ~~"Sucesso 100%" com zero registros confunde~~ — **Resolvido na Fase 02 da Onda 2**. Quando `total_records == 0`, log mostra bloco WARNING "⚠️ NENHUM DADO DISPONÍVEL" com causas prováveis, em vez de "EXPORTAÇÃO CONCLUÍDA". Status bar recebe nível "warning". | QA manual v1.1.0 (export Jan/2026) |
| 33 | 🔴 | XS | ✅ | ~~`pwr_int` ainda no fallback de `battery_voltage`~~ — **Resolvido na Fase 16 da Onda 1** com separação em 2 colunas (`vehicle_voltage` / `internal_battery_voltage`). | QA manual v1.1.0 (CSV VTR05 abr/2026) |
| 34 | 🔴 | S | ✅ | ~~Defaults do `DataNormalizer` mascaram `None` antes do `_fill_nd`~~ — **Resolvido na Fase 16 da Onda 1** (odometer e address agora `default=None`). | QA manual v1.1.0 (CSV VTR05 abr/2026) |
| 35 | 🟡 | XS | ✅ | ~~`_fill_nd` só checa `None`, não strings vazias~~ — **Resolvido na Fase 16 da Onda 1** (agora cobre `None` e `""`). | QA manual v1.1.0 |
| 36 | 🟢 | XS | ✅ | ~~CLI não tem flag de conta~~ — **Resolvido na Fase 01 da Onda 2**. Subcomandos `test`, `list` e `export` aceitam `--account 1|2`. Helper `build_service(account, export_dir)` centraliza a lógica. Export com Conta 2 (ou ambas configuradas) usa subpasta `Conta X/`. 9 testes novos em `test_cli.py`. | QA manual v1.1.0 |
| 37 | 🔴 | XS | ✅ | ~~`_normalize_sensor_name` confunde "Bateria do dispositivo"~~ — **Resolvido na Fase 17 da Onda 1**. Mappings específicos ("bateria do dispositivo", "bateria do rastreador", "device battery", "tracker battery") agora vêm antes dos ambíguos. | QA manual v1.1.0 |
| 38 | 🔴 | XS | ✅ | ~~Fallback Suntech para ignição (`mode`)~~ — **Resolvido na Fase 17 da Onda 1** via `SuntechProfile`. Validado em produção: 21.813 linhas do VTR05, agora 20.382 "Ligado" / 1.431 "Desligado" (antes era 100% Desligado). | QA manual v1.1.0 |
| 39 | 🔴 | XS | ✅ | ~~Fallback Suntech para odômetro (`m_asgn1`)~~ — **Resolvido na Fase 17 da Onda 1** via `SuntechProfile`. Validado em produção: odômetro 240.099 → 248.090 km no VTR05/abr-2026. | QA manual v1.1.0 |
| 40 | 🟢 | M | ✅ | ~~Perfis de tracker~~ — **Resolvido na Fase 17 da Onda 1**. Arquitetura `tracker_profiles/` criada com `SuntechProfile` + `DefaultProfile`. | QA manual v1.1.0 |
| 41 | 🟢 | XS | ✅ | ~~Logar warning quando tracker desconhecido cair no DefaultProfile~~ — **Resolvido**. `registry.py` agora loga uma vez por combinação `(model, rep_type)` quando msg cai no DefaultProfile com identificador populado. Cache module-level (resetável via `reset_unknown_tracker_cache()` em testes). 5 testes cobrindo cenários. | Discussão Fase 17 |
| 42 | 🟢 | S | ✅ | ~~Perfil JimiProfile (Jimi VL03)~~ — **Resolvido na Fase 18 da Onda 1**. Detecção por signature `serial`+`gps_real_up`+`data_mode` (validado em 430 msgs do CVM0H79). Mapping: `acc`→ignição, `pwr_ext`→tensão veículo, `voltage`→bateria interna. Validado em produção: 258 linhas, 246 Ligado / 12 Desligado, voltagens 12.9-14.4V. | Cliente Movi 2026-06-02 (Matheus, ID 402289789) |
| 43 | 🟢 | XS | ⬜ | **Validar família Suntech completa** — cliente confirmou que usa Suntech 4300/4315/340U/8300/8310 além do ST380. Arquitetura atual cobre via `rep_type='STT'`, mas séries 8xxx podem ter CAN/BLE com params extras (RPM, combustível) ainda não mapeados. Quando rodar export real de cada série, capturar mensagem e expandir `SuntechProfile.known_params()` se necessário. | Cliente Movi 2026-06-02 |
| 44 | 🟡 | S | ⬜ | **Migrar PyInstaller onefile → onedir no spec** — PyInstaller 6.20 já avisa: `Onefile mode in combination with macOS .app bundles ... will become an error in v7.0`. Atualizar `movi_exporter.spec` para `onedir` (gera pasta com binário + assets em vez de 1 arquivo único). Validar que build/Windows continua funcionando + atualizar `build.yml` se necessário. | Build local v1.1.0 (2026-06-02) |
| 45 | 🟡 | S | ⬜ | **Instruções de Gatekeeper macOS no README/release** — app não-assinado é bloqueado pelo Gatekeeper ao baixar de Releases. Mensagem típica: "can't be opened because Apple cannot check for malicious software". Workarounds: (a) "Botão direito → Open" na 1ª vez, (b) `xattr -dr com.apple.quarantine MoviExporter.app`. Adicionar seção no README + texto no body da release. Considerar Apple Developer cert ($99/ano) se cliente quiser distribuição mais ampla. | QA Mac do cliente |
| 46 | 🟢 | XS | 🔄 | **Atualizar GitHub Actions para Node.js 24** — Fase 01 da Onda 2 bumpou checkout/setup-python (Node 24 ok). Mas no release v1.2.0 o GitHub ainda avisou que `upload-artifact@v5`, `download-artifact@v5` e `action-gh-release@v2` rodam internamente em Node 20 (essas actions ainda não migraram). Reavaliar quando saírem versões Node-24; ou setar `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true` no workflow como mitigação. | Aviso CI release v1.1.0 / v1.2.0 |

---

## Notas

- Dívida técnica conhecida (não vai para a Onda 2 a menos que vire problema):
  - `requirements.txt` ainda não está pinado via `pip-compile` — `requirements.in` está pronto, basta rodar.
  - `docs/wialon/TOKEN_AUTORIZACAO.md` referenciado no CLAUDE.md não existe — criar quando tiver flow OAuth ou só remover a menção.
