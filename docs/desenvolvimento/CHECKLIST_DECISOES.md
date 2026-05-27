# Checklist de Decisões — Movi Exporter App

> **Status:** ✅ Checklist preenchido em 2026-05-22 via CLI.
> Veja a análise completa em [`ANALISE_MELHORIAS.md`](ANALISE_MELHORIAS.md).

---

## 🎯 Features aprovadas

| ID | Item | Status | Notas |
|----|------|--------|-------|
| F1 | **Editar Token Wialon pela GUI** — campo editável + show/hide + botões "Gerar", "Salvar", "Testar" | ✅ Onda 1 | |
| F2 | **Suporte a 2 contas Wialon** — `WIALON_TOKEN_2`; seletor condicional no Export; segunda seção em Settings; mesma pasta Drive; subpastas separadas | ✅ Onda 1 | Nomes = usernames retornados pela API Wialon (automático) |

> **Decisão F2:** opção B1 (dois tokens fixos). Descartados: app separado, n perfis. F1 + F2 juntas (compartilham `env_writer.py`).
> **Nomes das contas:** username real da API (ex: `movi` / `lcmovi_mgr`), sem configuração manual.

---

## 📊 Decisões sobre dados do export

| Campo | Decisão | Detalhe |
|-------|---------|---------|
| **Odômetro** | ✅ Manter + corrigir | Ler `odometer` dos params brutos + converter metros→km. Hoje hardcoded `None` |
| **Tensão da Bateria** | ✅ Manter + corrigir | Remover fallback `voltage` (bateria interna). Corrigir `flagsMask=0` para capturar msgs data-only com `pwr_ext` |
| **RPM / Combustível** | ✅ Manter | Já funciona via sensor_map para veículos com CAN bus. Veículos básicos ficam N/D |
| **Horas de Motor / Motorista** | ✅ Manter | Idem — funciona onde há sensor |
| **Localização (endereço)** | ⏳ Aguardar admin | `gis_geocode` não habilitado. Solicitar ao admin Wialon. Código pronto em `docs/wialon/GEOCODIFICACAO.md` |
| **Valores vazios (sem sensor)** | ✅ Usar `"N/D"` | Trocar `NaN` por `"N/D"` para campos sem sensor configurado. Apenas nas colunas que **nunca** terão dado para aquele veículo |

> **Contexto:** a conta `movi` tem rastreadores avançados (CAN bus — RPM, combustível, odômetro reais). A conta `lcmovi_mgr` tem 713 rastreadores básicos (GPS only — sem CAN bus). Colunas de sensores ficam `N/D` para a conta básica. Comportamento correto e esperado.

---

## 🐛 Onda 1 — v1.1.0

### Bugs

| ID | Item | Status | Esforço |
|----|------|--------|---------|
| C1 | Fix `uploaded_count` → `uploaded_files` — crash da GUI ao fim de upload com Drive | ✅ Fazer | XS |
| C2/U2 | Fix `_show_error` — trocar `CTkInputDialog` por `messagebox.showerror` | ✅ Fazer | XS |
| C4 | Propagar `WIALON_PAGE_SIZE` para o client (hoje ignorado) | ✅ Fazer | XS |
| C7 | Logar erros engolidos por `except Exception: pass` | ✅ Fazer | XS |
| C5 | `HTTPClientError` em `base_client.py` | ❌ Não agora | XS |

### Limpeza de código morto

| ID | Item | Status | Esforço |
|----|------|--------|---------|
| C3 | Remover `get_full_history` (nunca usado) | ✅ Fazer | XS |
| C8 | Remover `SystemAClient` + mapping `system_a` + vars `.env` legadas | ✅ Fazer | S |

### Testes e CI

| ID | Item | Status | Esforço |
|----|------|--------|---------|
| T1 | Reescrever `tests/` com pytest + asserts reais (normalizer + exporter) | ✅ Fazer | S |
| T2 | Criar `ci.yml` com pytest + ruff em push/PR | ✅ Fazer | S |
| T4 | Sincronizar versão: CI valida `tag == __version__`; spec injeta dinâmico | ✅ Fazer | S |
| T5 | Pinar `requirements.txt` com pip-tools | ✅ Fazer | S |
| T11 | `upx=False` no spec (antivírus) | ✅ Fazer | XS |
| T3 | Fix auto-updater macOS | ❌ Só cliente Windows | S |

### UX

| ID | Item | Status | Esforço |
|----|------|--------|---------|
| U7/U8 | Corrigir campos mascarados no Settings (sai junto com F1) | ✅ Fazer | XS |
| U12 | Mês por nome — Janeiro...Dezembro no seletor | ✅ Fazer | XS |
| U3 | Botão "Abrir pasta de exports" após export | ✅ Fazer | S |
| U5 | Onboarding: token vazio no startup → direciona para Settings | ✅ Fazer | S |

---

## 🎨 Onda 2 — v1.2.0

| ID | Item | Status | Esforço |
|----|------|--------|---------|
| U4 | Progresso real — "Processando 3/47: Caminhão XYZ" em vez de barra infinita | ✅ Fazer | M |
| U6 | Mensagens de erro amigáveis — 401 → "Token expirado", stack só no log | ✅ Fazer | S |
| U9 | Persistir últimas escolhas (mês/ano/formato/upload) entre sessões | ✅ Fazer | S |
| U10 | Confirmação antes de sobrescrever export existente | ✅ Fazer | S |
| U11 | Desabilitar UI durante export | ❌ Não agora | S |
| U13 | Release notes no UpdateDialog | ❌ Não agora | XS |
| U14 | Tela "Sobre" + verificar atualizações manual | ❌ Não agora | XS |
| T6 | Resolver caminhos relativos (.env/credentials) no binário | ❌ Não agora | M |

---

## 🔧 Onda 3 — v1.3.0+

| ID | Item | Status | Esforço |
|----|------|--------|---------|
| C6 | Deduplicar `exporter.py` (~400 linhas → helpers) | ✅ Fazer | M |
| T7 | Testes do `WialonClient` com mocks (paginação + re-auth) | ✅ Fazer | M |
| T12 | Release notes curadas (parar de mostrar "chore: downgrade" ao cliente) | ✅ Fazer | S |
| C9 | Constantes nomeadas para flags Wialon | ❌ Não agora | S |
| C10 | Refactor `_get_credentials` | ❌ Não agora | S |
| C11 | Normalizar retorno de `list_vehicles` | ❌ Não agora | S |
| T8 | Edge cases do normalizer | ❌ Não agora | S |
| T13 | `pyproject.toml` | ❌ Não agora | S |
| T14 | Dependabot | ❌ Não agora | XS |

---

## ❌ Fora de escopo (todas as ondas)

| Item | Por quê |
|------|---------|
| Code signing Windows / Notarization macOS | Custo sem retorno com 1 cliente |
| Sentry/Datadog | Log local suficiente |
| Testes de UI Tkinter | ROI baixo |
| Migração de framework GUI | App funcional |
| Multi-idioma | 1 cliente, pt-BR |
| App separado para 2ª conta | Double maintenance — decidido F2 no app atual |
| Sistema de n perfis Wialon | Só 2 contas — overengineering |
| Redesign visual completo | Cosmético |
| Rollback de update | Auto-updater simples OK |

---

## 📋 Resumo das Ondas

| Onda | Versão | Conteúdo principal |
|------|--------|--------------------|
| **1** | v1.1.0 | F1 + F2 (features cliente) + bugs + CI/testes + UX básico |
| **2** | v1.2.0 | Progresso real, erros amigáveis, persistência de escolhas |
| **3** | v1.3.0+ | Deduplicação, testes Wialon, release notes |
