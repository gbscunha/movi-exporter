# PLANO_REFACTOR — Onda 4: Refatoração e Limpeza

> **Objetivo:** eliminar lixo e código morto, remover o único acoplamento de
> arquitetura existente e aplicar Clean Code / SOLID nos pontos de maior ROI —
> **sem alterar o comportamento do app em produção**.
>
> **Contexto:** 1 cliente em produção (Windows), mantenedor solo. As escolhas
> abaixo são deliberadamente **pragmáticas**: refatorar onde há ganho real,
> evitar over-engineering.

## Princípios desta onda

- **Comportamento preservado.** Nenhuma mudança visível ao cliente. Toda fase
  parte de testes verdes e termina em testes verdes.
- **Faseado e seguro.** O refactor mais arriscado (núcleo do export) fica por
  último, com testes de caracterização escritos *antes* de mexer.
- **Uma fase = um branch = um commit** (Conventional Commits, PT-BR, frase única).
- **Reversível.** Docs concluídos são *arquivados* (não deletados); o git
  preserva o histórico de tudo.

## Regras de execução (por fase)

1. **Branch** a partir da `main`: `refactor/<nome-curto>` (ou `chore/`, `docs/`).
2. **Implementar** apenas o escopo da fase.
3. **Verificar** (gate obrigatório antes de commitar):
   - `pytest -q` — todos verdes
   - `ruff check src/` — zero erros
   - Se mudou dados do export: abrir o arquivo gerado e conferir colunas/valores
   - Se mudou GUI: abrir o app e testar o caminho principal
4. **Commit** + abrir PR.
5. **Atualizar status** na tabela abaixo (⬜ → ✅).

## Status geral

| Fase | Descrição | Risco | Status |
|------|-----------|-------|--------|
| 0 | Rede de segurança (baseline) | — | ✅ Feito (testes/lint; export real pendente no cliente) |
| 1 | Limpeza de lixo e código morto | Baixo | ✅ Feito |
| 2 | Arquivar docs concluídos + pinar dependências | Baixo | ✅ Feito |
| 3 | `service_factory` — remover acoplamento GUI→client | Baixo/Médio | ⬜ Todo |
| 4 | Dedup do `exporter.py` (−~400 linhas) | Médio | ⬜ Todo |
| 5 | Constantes nomeadas + helpers + fix de `except` | Baixo | ⬜ Todo |
| 6 | Quebrar `export_monthly_data()` (com testes de caracterização) | **Alto** | ⬜ Todo |
| 7 | Varredura final de comentários óbvios | Baixo | ⬜ Todo |

---

## Fase 0 — Rede de segurança (baseline)

Estabelecer o ponto verde de referência antes de qualquer mudança.

- [ ] `pytest -q` verde e registrar nº de testes
- [ ] `ruff check src/` sem erros
- [ ] Abrir a GUI e rodar **um export real** (conta 1) → guardar o CSV/XLSX
      gerado como *baseline* para comparação nas Fases 4 e 6
- [ ] Confirmar que a `main` está limpa e que cada fase parte dela

---

## Fase 1 — Limpeza de lixo e código morto

**Branch:** `refactor/limpeza`

Código morto **confirmado** (`base_client.py` só é referenciado pelo próprio
`__init__.py`; nenhum teste o importa).

- [ ] Deletar `src/clients/base_client.py` (146 linhas, `BaseClient` /
      `StatefulClient` nunca usados)
- [ ] Limpar `src/clients/__init__.py` — remover import e `__all__` de
      `BaseClient`/`StatefulClient` e a linha do docstring que os cita
- [ ] Adicionar `.ruff_cache/` ao `.gitignore` (hoje fora do ignore)
- [ ] (Opcional, não-git) limpar lixo local: `app*.log`, `.DS_Store`,
      `__pycache__/`, `.ruff_cache/`, `.pytest_cache/`

**Verificação:** `pytest -q` + `ruff check src/`; confirmar que
`from src.clients import WialonClient` ainda funciona.

---

## Fase 2 — Arquivar docs concluídos + pinar dependências

**Branch:** `docs/arquivo-e-pin-deps`

⚠️ **Cuidado crítico:** `PLANO_ONDA_1.md` é referenciado pelo `CLAUDE.md`
(linhas 14, 83, 103), pela skill `.claude/skills/nova-fase/SKILL.md` e por
`.claude/skills/xp-cycle.md`. Arquivar sem atualizar essas referências
**quebra a skill `/nova-fase`**.

- [ ] Criar `docs/arquivo/`
- [ ] `git mv` para `docs/arquivo/` os planos concluídos / históricos:
  - `PLANO_ONDA_1.md`, `PLANO_ONDA_2.md`, `PLANO_ONDA_3.md`
  - `RETOMADA.md` (auto-marcado "apagar quando Onda 3 fechar")
  - `ANALISE_MELHORIAS.md`, `CHECKLIST_DECISOES.md`, `BACKLOG_ONDA_2.md`
  - `exporter_usage.md`, `normalizer_usage.md` (duplicam docstrings)
  - `docs/STATUS-PROJETO-API-WAILON-110626.html` (snapshot órfão)
- [ ] **Manter** em `docs/desenvolvimento/`: `PLANO_MOTORISTA_RFID.md` (feature
      futura) e este `PLANO_REFACTOR.md` (plano ativo)
- [ ] Repontar referências para o **plano ativo** (`PLANO_REFACTOR.md`):
  - `CLAUDE.md` (linhas 14, 83, 103)
  - `.claude/skills/nova-fase/SKILL.md`
  - `.claude/skills/xp-cycle.md`
- [ ] **Pinar** dependências: `pip-compile requirements.in` → `requirements.txt`
      com versões exatas das já instaladas no venv (não fazer upgrade)

**Verificação:** `pip install -r requirements.txt` num venv limpo instala sem
conflito; a skill `/nova-fase` aponta para um plano válido; `pytest -q`.

---

## Fase 3 — `service_factory` (remover acoplamento GUI→client)

**Branch:** `refactor/service-factory`

Única violação de arquitetura real: 3 frames da GUI importam e instanciam
`WialonClient` direto (viola `CLAUDE.md:97`). O CLI já tem o padrão correto
(`build_service()` em `cli/main.py:26-47`) — vamos extrair e reusar.

- [ ] Criar `src/core/service_factory.py` com
      `build_vehicle_service(account: int = 1, export_dir: str | None = None) -> VehicleService`
      (mover a lógica de seleção de conta/token do CLI para cá)
- [ ] `cli/main.py` passa a importar do factory (remover `build_service` local)
- [ ] `gui/frames/export.py`: usar o factory; remover `from src.clients...`
- [ ] `gui/frames/home.py`: idem
- [ ] `gui/frames/settings.py`: usar o factory e o serviço para testar conexão
      (`VehicleService.test_connection()`) em vez de `WialonClient().authenticate()`
- [ ] Garantir que **nenhum** arquivo em `src/gui/` importe `src.clients`
- [ ] Novo teste `tests/test_service_factory.py` (conta 1, conta 2, conta 2 sem
      token → erro)

**Verificação:** `pytest -q`; `grep -rn "src.clients" src/gui` deve voltar vazio;
abrir GUI e testar conexão (conta 1 e conta 2) + um export.

---

## Fase 4 — Dedup do `exporter.py`

**Branch:** `refactor/exporter-dedup`

~400 linhas duplicadas: 3 pares CSV/Excel idênticos que só diferem na linha
`df.to_csv(...)` vs `df.to_excel(...)`.

- [ ] Extrair `_write_dataframe(df, file_path, fmt)` central (encapsula
      `to_csv` com `encoding="utf-8-sig"` e `to_excel` com `engine="openpyxl"`)
- [ ] **Manter as assinaturas públicas** (`export_vehicles_to_csv/excel`,
      `export_history_to_csv/excel`, `export_consolidated_history_to_csv/excel`)
      como wrappers finos delegando a um método genérico — assim o
      `vehicle_service.py` não precisa mudar
- [ ] Preservar exatamente: `N/D`, `EXCEL_MAX_ROWS`, ordem/tradução de colunas,
      nomes de arquivo
- [ ] Efeito colateral: a unificação já remove a maioria dos comentários óbvios
      duplicados (`# Cria DataFrame`, `# Define caminho de saída`, etc.)

**Verificação:** `pytest -q` (`test_exporter`, `test_exporter_nd`,
`test_pipeline_integration`); **gerar um export real e comparar colunas/valores
com o baseline da Fase 0** (regra `CLAUDE.md` de verificação #4).

---

## Fase 5 — Constantes nomeadas + helpers + fix de `except`

**Branch:** `refactor/constantes-helpers`

- [ ] Nomear o flag mágico do Wialon (`8392713` = `1 + 8 + 4096 + 8388608`) em
      constantes documentadas no `wialon_client.py`
- [ ] Nomear limiares de tensão trocada (`10V` / `6V`) e timeouts (`30` / `60`)
- [ ] Extrair helper `_open_system_folder()` compartilhado (hoje duplicado entre
      `export.py` e `home.py`)
- [ ] Corrigir o único `except Exception: pass` real
      (`gui/dialogs/about_dialog.py:91` → `logger.debug(...)`)
- [ ] (Opcional, com cuidado) renomear variáveis de 1 letra pontuais
      (`v`→`vehicle`, `w`→`widgets`)

> Nota: a alegação de "34 `except` mascarando bugs" foi **verificada e
> descartada** — apenas 1 engole o erro; os demais já logam, como o `CLAUDE.md`
> exige. Não tratar como problema sistêmico.

**Verificação:** `pytest -q` + `ruff check src/`; testar um export real.

---

## Fase 6 — Quebrar `export_monthly_data()` (alto risco — por último)

**Branch:** `refactor/vehicle-service-split`

`vehicle_service.export_monthly_data()` tem ~220 linhas e mistura auth, filtro,
detecção de placa duplicada, loop de processamento, normalização, export
individual, consolidado, upload e log. É o **coração da produção** → blindar
com testes antes de tocar.

- [ ] **PRIMEIRO**: escrever testes de caracterização (golden) que capturam a
      saída atual a partir de fixtures mockadas (veículos, histórico, N/D,
      placa duplicada, tensão trocada, conta sem dados)
- [ ] Só então extrair sub-métodos privados, ex.:
  - `_resolve_and_filter_vehicles(...)`
  - `_detect_duplicate_plates(...)`
  - `_process_vehicle(...)` (histórico → normaliza → export individual)
  - `_export_consolidated(...)`
  - `_maybe_upload(...)`
- [ ] (Se houver fôlego) aplicar a mesma extração em
      `gui/frames/export.py::_start_export()` (~140 linhas)

**Verificação reforçada:** testes de caracterização verdes; **comparar o arquivo
exportado (colunas e valores) antes vs. depois** com o baseline da Fase 0;
teste manual de export real para conta 1 e conta 2.

---

## Fase 7 — Varredura final de comentários óbvios

**Branch:** `refactor/limpeza-comentarios`

Aplicar a regra do `CLAUDE.md` ("comentar apenas o *porquê* de algo não-óbvio").
Feita **por último** para limpar o estado final de uma vez — as Fases 4 (dedup)
e 6 (extração) já eliminam boa parte dos comentários óbvios como efeito colateral.

**Estado atual:** o código já é bem comentado no geral — **sem código morto
comentado** e apenas 4 divisores decorativos. O alvo são os comentários que só
repetem o que a linha seguinte já diz.

### Rubrica de decisão

**✅ MANTER — o "porquê" não-óbvio** (exemplos reais, NÃO tocar):
- `exporter.py:18-19` — limite rígido de linhas do `.xlsx`
- `exporter.py:38-41` — razão do `N/D` (cliente vê "sem dado" vs célula vazia)
- `exporter.py:88` — "duas medidas de tensão distintas — NÃO unificar"
- `vehicle_service.py:193-195` — propagação de `pwr_ext`
- `vehicle_service.py:202-206` — carry-forward de ignição (Suntech model 170)
- `vehicle_service.py:217-220` — sanity-check de tensão trocada
- `export.py:47-49` — bug de cor do log no tema claro
- Qualquer comentário com referência a issue `(#NN)` ou que justifique um default

**🗑️ REMOVER — apenas repete o código** (exemplos reais):
- `# Cria DataFrame` antes de `df = pd.DataFrame(...)`
- `# Define caminho de saída`, `# Garante que o diretório existe`
- `# Exporta para CSV` antes de `df.to_csv(...)`
- `# Título`, `# Configurações`, `# Botões de ação` (rótulos óbvios em `export.py`)
- `# Primeiro dia do mês às 00:00:00` antes do código que faz exatamente isso
- `# Obtém mapa de sensores (com cache)` antes de `get_sensors(...)`
- Os 4 divisores decorativos (`# ====`, `# ----`)

### Checklist

- [ ] Varrer arquivos restantes (não cobertos por dedup/extração): `home.py`,
      `settings.py`, `wialon_client.py`, `cli/main.py`, `tracker_profiles/`,
      `sidebar.py`, `app.py`, `icons.py`
- [ ] Remover comentários que só repetem a linha seguinte (rubrica acima)
- [ ] **Na dúvida, manter** — preferir falso-negativo a apagar um "porquê" útil
- [ ] Não tocar em docstrings de interface pública (type hints + docstring são
      contrato, não comentário óbvio)

**Verificação:** `pytest -q` + `ruff check src/` (comentários não mudam
comportamento — gate é só garantir que nada foi cortado no meio do código).

---

## NÃO fazer nesta onda (over-engineering para o contexto)

- ❌ `CredentialProvider` plugável (só 2 tokens em env, nunca mudam)
- ❌ `Exporter` como Strategy para formatos além de CSV/XLSX (não há demanda)
- ❌ `Uploader` como `Protocol` / DI container (instanciação direta basta)
- ❌ Múltiplas camadas de DTO / logging estruturado

> O *port* que importa — `TrackingClient` (Protocol) — **já existe e é usado**.
> Suportar outro fornecedor seria adicionar um adapter, sem mexer nos services.
