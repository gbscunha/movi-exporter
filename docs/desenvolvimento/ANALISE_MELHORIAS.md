# Análise de Melhorias — Movi Exporter App

**Data:** 2026-05-22
**Versão analisada:** 1.0.2
**Contexto:** App desktop Python (CustomTkinter + PyInstaller) distribuído via GitHub Releases. Mantenedor solo. Cliente real em produção (Windows). Filosofia: pragmatismo, anti-overengineering.

---

## Sumário Executivo

A base está **sólida**. Boa separação em camadas (`core`/`clients`/`services`/`gui`), uso de Protocols, dataclasses, hierarquia de exceções. Não precisa de refactor estrutural.

Os ganhos reais estão em **3 frentes**:

1. **Bugs latentes e duplicação cirúrgica** — pequenas correções que evitam crash em produção
2. **Sustentabilidade** — testes reais, CI com validação, versionamento confiável
3. **UX do cliente** — pequenas mudanças com alto impacto na percepção ("não está quebrado")

Pendentes desta sessão:
- **Feature F1 — Edição do token Wialon pela GUI** — encaixa direto no item de UX (Settings hoje é só decorativa) e elimina o suporte recorrente.
- **Feature F2 — Suporte a múltiplas contas Wialon** — cliente solicitou segunda conta; mesma pasta Drive, mesmo formato. Decisão: B1 (dois tokens fixos, seletor condicional no Export).

---

## 1. Clean Code

### 🔴 Alto impacto (bugs ou problemas concretos)

| # | Onde | Problema | Esforço |
|---|------|----------|---------|
| C1 | `gui/frames/export.py:363` | `result.upload_result.uploaded_count` não existe — quebra UI ao fim de upload | XS |
| C2 | `gui/frames/home.py:189` | `_show_error` usa `CTkInputDialog` (pede input) em vez de mensagem; nunca chamado com `.show()` | XS |
| C3 | `clients/wialon_client.py:515` | `get_full_history` nunca é chamado — dead code | XS |
| C4 | `core/config.py:30` + `wialon_client.py:433` | `WIALON_PAGE_SIZE` lido no settings mas não chega ao client | XS |
| C5 | `clients/base_client.py:59,78` | `raise Exception(...)` genérico — quebra `except` granular | XS |
| C6 | `services/exporter.py:173-699` | Os 6 métodos `export_*_to_{csv,excel}` são ~95% idênticos. Bloco `clean_record` (15 campos) replicado 4×. ~400 linhas removíveis | M |
| C7 | `vehicle_service.py:377-378` + `home.py:135-150` | `except Exception: pass` engole erros silenciosamente | XS |

### 🟡 Médio impacto

| # | Onde | Problema | Esforço |
|---|------|----------|---------|
| C8 | `clients/system_a_client.py` (todo) + `normalizer.py` + `.env` | Dead code legado (`SystemAClient`). Variáveis no `.env`, mapping no normalizer, métodos em português | S |
| C9 | `wialon_client.py:232, 270, 468-469` | Magic numbers nos flags Wialon (`8392713`, `4096`, `65281`) | S |
| C10 | `services/uploader.py:94-140` | `_get_credentials` mistura I/O, refresh, browser e save sem catch de `RefreshError` | S |
| C11 | `wialon_client.py:243-247` | `list_vehicles` muta dict da API com chaves `_plate`, `_brand` — contrato implícito | S |
| C12 | `wialon_client.py:304-340` | `_extract_base_param` reimplementa busca de operador (15 linhas) — `re.split` resolve em 2 | XS |

### 🟢 Baixo impacto (cosmético, deixar para próxima iteração)

| # | Onde | Observação |
|---|------|------------|
| C13 | `normalizer.py:240-262` | `_normalize_timestamp` retorna `datetime.now()` em fallback — mascara dados ruins |
| C14 | Vários | Imports dentro de função sem motivo (não há ciclo) |
| C15 | `cli/main.py:50` | Texto fala em "Service Account" mas implementação é OAuth |
| C16 | `cli/main.py:88+` | Parâmetro `format` sombreia builtin |
| C17 | `services/exporter.py:111` | Filename com acento (`Histórico_Padrão`) — risco de portabilidade |

---

## 2. Testes, CI/CD, Build

### 🔴 Alto impacto

| # | Onde | Problema | Esforço |
|---|------|----------|---------|
| T1 | `tests/test_*.py` | Não são testes reais — `logger.info` sem `assert`. `test_normalizer.py` ainda tem `sys.path.insert(0, "/Users/gbscunha/dev/movi_exporter_app/src")` hardcoded | S |
| T2 | `.github/workflows/build.yml` | CI só builda em tag. Não roda testes, lint nem type-check. Não há proteção pré-merge | S |
| T3 | `src/gui/updater.py:75` | Updater só procura `.exe`/`.msi` — usuário macOS nunca recebe atualização (falha silenciosa) | S |
| T4 | `movi_exporter.spec:108-109` | `CFBundleVersion` hardcoded `1.0.0` — versão divergente do `__version__` | S |
| T5 | `requirements.txt` | Zero versões pinadas — qualquer release de dep pode quebrar build/runtime sem aviso | S |
| T6 | `core/config.py:33` + `services/uploader.py:121` | Paths `./credentials.json` são relativos ao `cwd`. No `.app`/`.exe` o cwd geralmente não é a pasta do binário — quebra setup do cliente | M |

### 🟡 Médio impacto

| # | Onde | Problema | Esforço |
|---|------|----------|---------|
| T7 | Sem teste do `WialonClient` | Paginação, re-auth, parsing — maior superfície de bug, zero coverage. Mocks via `responses`/`requests-mock` (sem gastar quota) | M |
| T8 | Normalizer testado, mas sem `assert` real | Cobrir timestamp int/str/ISO, lat/lng=0, raw_data preservado | S |
| T9 | CI Python 3.12 vs dev 3.14 | Bug 3.14-only só aparece em prod | XS |
| T10 | Sem smoke test do binário | PyInstaller pode quebrar `hiddenimports` e binário só crasha no cliente | S |
| T11 | `movi_exporter.spec:86` | `upx=True` — antivírus marcam como falso positivo. Sem assinatura, pior ainda | XS |
| T12 | `.github/workflows/build.yml:112` | `generate_release_notes: true` mostra commits "chore: downgrade version" ao cliente | S |

### 🟢 Baixo impacto

| # | Onde | Observação |
|---|------|------------|
| T13 | Sem `pyproject.toml` | Metadata espalhada (versão, deps, config). Útil mas opcional |
| T14 | Sem Dependabot / `pip-audit` | Vulnerabilidades de deps invisíveis. Habilitar é grátis |
| T15 | `app.log` em `cwd` | Mesmo problema do T6 — logs do cliente vão pra lugar inesperado |
| T16 | Tamanho do binário | `collect_submodules('google')` puxa Google universe. ~80-120MB final |
| T17 | `notarization` macOS / code signing Windows | $99/ano cada. Só faz sentido se cliente reclamar do SmartScreen — hoje ele só vê 1× |

---

## 3. UX/UI

### 🔴 Alto impacto (impacto direto no cliente)

| # | Onde | Problema | Esforço |
|---|------|----------|---------|
| U1 | `frames/settings.py` | Campos parecem editáveis (Token, folder ID, export dir) mas nada salva. Cliente vai mudar, fechar, abrir e achar que está bugado. **Esta é a feature pendente** | M |
| U2 | `frames/home.py:189` | `_show_error` mostra diálogo de input em vez de mensagem (mesma raiz do C2) | XS |
| U3 | `frames/export.py` | Após export, paths aparecem no log mas cliente não-técnico não navega até lá. Sem botão "Abrir pasta" | S |
| U4 | `frames/export.py` | Barra de progresso é indeterminada — em export de 10 min cliente acha que travou | M |
| U5 | `app.py` | Sem onboarding na primeira execução: token vazio = home mostra "Erro ❌" silencioso | S |
| U6 | `frames/export.py` | Stack trace cru no log em qualquer falha (ex: `HTTPError: 401 Unauthorized`) — cliente assusta | S |

### 🟡 Médio impacto

| # | Onde | Problema | Esforço |
|---|------|----------|---------|
| U7 | `frames/settings.py:63` | Token é inserido como `"*" * 20` literal no Entry — usuário edita e sobrescreve o real | XS |
| U8 | `frames/settings.py:151` | `folder_id` truncado com `...` vira valor do Entry | XS |
| U9 | `frames/export.py` | Sem persistência de últimas escolhas (mês/ano/formato/upload) | S |
| U10 | `frames/export.py` | Sem confirmação para sobrescrever export existente | S |
| U11 | `frames/export.py` | UI inteira fica clicável durante export — pode quebrar estado | S |
| U12 | `frames/export.py` | Mês como número (1-12) — cliente brasileiro pensa por nome | XS |
| U13 | `dialogs/update_dialog.py` | Não mostra release notes (apesar de já vir da API) | XS |
| U14 | `app.py` | Sem "Verificar atualizações" manual, sem tela "Sobre", sem link de contato | XS |
| U15 | Iconografia | Commit recente removeu ícones do Home, mas Sidebar/Settings/Botões ainda têm emojis — inconsistente | XS |

### 🟢 Baixo impacto

| # | Observação |
|---|------------|
| U16 | Sem atalho de teclado para "Iniciar Exportação" (`Ctrl+E`) |
| U17 | `year_entry` aceita qualquer string sem validação |
| U18 | Cards "Verificando..." sem animação visual |
| U19 | Janela não restaura geometria entre execuções |
| U20 | Log textbox sem "Copiar log" / "Exportar log" — útil para suporte |
| U21 | StatusBar mostra hora do sistema (informação que o SO já dá) |

---

## 4. Skills Sugeridas

Pesquisei em https://www.skills.sh/ e filtrei por relevância real ao projeto. Skills são bibliotecas de instruções para o Claude — instaladas via `/skill install`.

### Vale a pena

| Skill | Por quê |
|-------|---------|
| **tdd** | Vai casar com o item T1 (escrever testes pytest reais). Bom para parar de procrastinar testes |
| **github-actions-docs** | Útil ao configurar o `ci.yml` (T2) e ajustar `build.yml` |
| **improve-codebase-architecture** | Especificamente quando formos atacar C6 (deduplicação do exporter) |
| **diagnose** | Para os 2-3 bugs latentes (C1, C2, C7) |

### Não compensa agora

- **sentry-cli** — só faria sentido com múltiplos clientes/instalações. Hoje 1 cliente, log local resolve
- **browser-use** — testes E2E de UI Tkinter são dolorosos; ROI baixo
- **mcp-builder** — não precisa criar MCP novo
- **caveman** (refactoring agressivo) — risco maior que benefício em produto em produção

### Não precisa instalar

Os skills `requesting-code-review` / `receiving-code-review` são bons mas você já tem o `/review` e `/ultrareview` integrados no Claude Code.

---

## 5. Features Pendentes

### F1 — Edição do Token Wialon pela GUI

Reconfirmado pela análise UX (item U1). Elimina suporte recorrente.

**Escopo** (tela Configurações → seção Wialon API):

1. Campo de token editável com toggle 👁️ "mostrar/ocultar"
2. Botão **🔗 Gerar token** — abre navegador na URL de autorização Wialon
3. Botão **💾 Salvar** — persiste no `.env` e recarrega `settings` em memória (sem restart)
4. Botão **🔍 Testar conexão** — chama `WialonClient.authenticate()` e mostra ✅/❌

**Arquivos:**
- `src/gui/frames/settings.py`
- `src/core/env_writer.py` (NOVO)
- `src/core/config.py` (adicionar `reload()`)

**Esforço:** M (~2-3h)

---

### F2 — Suporte a Múltiplas Contas Wialon

**Contexto:** cliente solicitou segunda conta Wialon. Mesma pasta Drive, mesmo formato. "Tanto faz" como implementado.

**Decisão tomada: B1 (dois tokens fixos, seletor condicional)**

Descartados:
- **App separado** — double maintenance forever para dev solo
- **Sistema de perfis genérico (n contas)** — overengineering; só existem 2 contas
- **Export simultâneo** — pode vir depois como incremento simples

**Escopo B1:**

| O que | Detalhe |
|-------|---------|
| `.env` | Adicionar `WIALON_TOKEN_2` (opcional — se vazio, feature fica invisível) |
| Settings | Segunda seção "Conta 2" com mesmos botões de F1 (gerar/salvar/testar) |
| Export | `CTkOptionMenu` "Conta: [Conta 1 ▾]" que **só aparece se `WIALON_TOKEN_2` estiver configurado** |
| Drive | Mesma pasta (`GOOGLE_DRIVE_FOLDER_ID`) para ambas |
| Exports locais | Subpastas separadas: `exports/conta1/` e `exports/conta2/` (evita sobrescrever) |
| `VehicleService` | Já aceita `WialonClient(token=...)` — sem mudança necessária |

**Arquivos adicionais:**
- `src/core/config.py` — `WIALON_TOKEN_2: str` + lógica de selecionar token ativo
- `src/gui/frames/export.py` — seletor de conta
- `src/gui/frames/settings.py` — segunda seção de token

**Esforço:** M (~2-3h, aproveita toda infra da F1)

**Recomendação:** implementar F1 e F2 juntas na mesma onda — compartilham o `env_writer.py` e a seção de token no Settings.

---

## 6. Recomendação de Ordem de Execução

Sugiro **3 ondas**, cada uma terminando com release versionado:

### Onda 1 — Bugs + Features do cliente (v1.1.0)
- C1-C7 (bugs latentes)
- T1-T5 (testes pytest reais + CI com lint/test + pin requirements + sync version)
- **F1** (editar token pela GUI)
- **F2** (suporte a duas contas Wialon)
- U2 (fix do dialog de erro — sai junto com C2)

**Ganho:** zero crashes silenciosos, CI útil, cliente opera os dois logins sem te ligar.

### Onda 2 — UX cliente (v1.2.0)
- U3, U4, U5, U6 (botão abrir pasta, progresso real, onboarding, mensagens amigáveis)
- T6 (paths corretos para .env/credentials no binário)
- U7-U12 (ajustes pequenos do Settings, persistência de escolhas)

**Ganho:** cliente percebe diferença grande, suporte cai.

### Onda 3 — Manutenibilidade (v1.3.0+)
- C6 (deduplicação do exporter)
- T7-T10 (testes Wialon, smoke test, alinhar Python)
- T11-T12 (upx off, release notes curadas)
- Pyproject.toml + Dependabot

**Ganho:** sustentabilidade futura.

### O que cortar do radar

- Notarização/code signing: só se cliente reclamar
- Sentry/Datadog: só se passar de 1 cliente
- Testes de GUI Tkinter: continua dispensável
- Multi-idioma, redesign visual, tema toggle dinâmico: fora de escopo

---

## Apêndice — Pontos fortes da base atual

Para registro, vale notar o que **não** precisa mexer:

- ✅ Hierarquia `WialonError` → `WialonAuthError` / `WialonValidationError` com `error_code`
- ✅ Uso de `Protocol` para tipagem do `TrackingClient`
- ✅ `dataclass` para `ExportResult`, `VehicleStats`, `UploadResult`
- ✅ Separação `WialonClient` (HTTP) vs `WialonTransformer` (parsing) vs `Normalizer` (estrutura)
- ✅ Generator `get_history` evitando carregar mês inteiro em memória
- ✅ Auto-update via GitHub Releases (modelo simples e funcional)
- ✅ Logger com rotação automática
- ✅ Type hints em quase toda interface pública

O projeto está num bom ponto para crescer com tranquilidade. Os ajustes são pontuais.
