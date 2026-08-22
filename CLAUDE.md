# CLAUDE.md

App desktop Python que extrai dados mensais de rastreamento veicular da Wialon e exporta para CSV/Excel com upload opcional ao Google Drive. 1 cliente em produção (Windows). Mantenedor solo.

## Estrutura

```
src/core/        — config, logger, env_writer, service_factory
src/clients/     — wialon_client (stateful), protocols
src/services/    — vehicle_service, wialon_transformer, normalizer, exporter, uploader, tracker_profiles/
src/gui/         — app, frames/, components/, dialogs/, updater
src/cli/         — main
tests/           — pytest
CHECKLIST.md / JOURNAL.md — estado vivo e história (pessoais, gitignored — ver "Estado do projeto")
docs/specs/            — specs de feature (o "quê", DADO/QUANDO/ENTÃO)
docs/decisions/        — ADRs (o "porquê")
docs/desenvolvimento/  — PLANO_*.md das ondas 1–5 (concluídos, registro) + TEMPLATE_CHECKLIST.md
docs/arquivo/          — planos e docs históricos concluídos
docs/wialon/           — GEOCODIFICACAO.md
docs/manual/           — manual.html (manual do usuário final, embarcado)
docs/cliente/          — USER_GUIDE.md (guia técnico/CLI)
docs/wialon-api-docs/  — documentação oficial da API Wialon
```

## Comandos

```bash
source venv/bin/activate              # ativar venv
pip install -r requirements.txt       # dependências
python -m src.gui.main                # rodar GUI
python -m src.cli.main test           # testar conexão Wialon
pytest -q                             # testes
ruff check src/                       # lint
ruff format src/ tests/               # formatter (CI roda --check)
python scripts/build.py               # build local
git tag v1.x.x && git push origin v1.x.x   # trigger CI → release (valida __version__ = tag)
```

Python **3.12** em tudo (venv, CI, build) — criar o venv com `python3.12 -m venv venv` (macOS: `brew install python@3.12 python-tk@3.12`); não usar sintaxe/lib acima de 3.12. `ruff` está pinado em `0.15.14` no CI.

## Convenções

- Identificadores em inglês; docstrings, comentários, UI, mensagens e testes em português brasileiro
- Type hints em toda interface pública
- `N/D` para campos de sensor sem dado — nunca `NaN` nem string vazia visível ao cliente
- Sem comentários óbvios — comentar apenas o *porquê* de algo não-óbvio

## Wialon API — regras críticas

A skill `wialon-api` (`.claude/skills/wialon-api/SKILL.md`) tem a referência completa — carregar antes de tocar `wialon_client`/`transformer`. Regras que nunca quebram:

- API é **stateful** — usa `sid`, NÃO Bearer token
- Login retorna **dois** session IDs: `eid` (API) e `gis_sid` (GIS) — usar o correto para cada chamada
- URLs de GIS são **dinâmicas** — vêm no login, nunca hardcoded
- `flagsMask=0` em `messages/load_interval` para capturar todos os tipos (incluindo data-only com `pwr_ext`)
- Odômetro vem em **metros** — sempre converter para km (÷ 1000)
- `pwr_ext` = tensão do veículo (~12-28V); `voltage` = bateria interna do tracker (~4V) — são coisas diferentes
- **Motorista:** `params["rfid_tag"]` = código do cartão RFID → casar com `c` (Código) do motorista no resource (`drvrs`). A lista vem de `core/search_items` em `avl_resource` com flag `256` (Drivers). O nome usa **forward-fill por veículo** (o vínculo persiste entre mensagens). Requer ACL de ver motoristas no token; sem ela, coluna vira `N/D`
- **Endereço (geocode):** `POST {gis_geocode}/{host_api}/gis_geocode` com `coords`+`flags=1255211008`+`uid` (de `login["user"]["id"]`). Host da API **dentro do path**; **não** enviar `gis_sid` nem `search_provider` (o `error=7` é o provider recusado, NÃO billing). POST (GET estoura em ~150 coords). Deduplicar coords (~4 casas) e cachear no export

**Token:** gerado via fluxo de autorização web do Wialon (login → o token volta na URL, após `access_token=`), **NÃO** via API. Passo a passo no manual do cliente (`docs/manual/manual.html`, seção 2).

## Git

- Branch por feature: `feat/nome-curto` ou `fix/nome-curto`
- Commits em português, Conventional Commits: `tipo(escopo): descrição`
- Tipos: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`, `ci`
- Escopos úteis: `wialon`, `gui`, `export`, `drive`, `ci`, `settings`
- **Mensagem de commit = uma única frase curta** — sem corpo, sem trailers
- **NUNCA incluir `Co-Authored-By` ou qualquer trailer** nas mensagens de commit
- Nunca commitar direto na `main`
- `git add` sempre com arquivos específicos — nunca `git add .`
- Nunca commitar `.env`, `credentials.json`, `token.json`, `*.log`

## Verificação

Antes de declarar qualquer tarefa concluída:
1. `pytest -q` — todos os testes passam
2. `ruff check src/` — zero erros
3. `ruff format --check src/ tests/` — nada a reformatar
4. GUI abre e a feature funciona (testar o caminho principal manualmente)
5. Se mudou dados do export: abrir o arquivo gerado e confirmar colunas/valores
6. Se mudou `wialon_client.py`: testar com token real e conferir `app.log`

## Testes

- Focar em `normalizer` (mapping wialon), `exporter` (colunas, N/D) e `wialon_client` (paginação, re-auth)
- Usar `requests-mock` para mockar chamadas Wialon — sem gastar quota real
- Sem testes de GUI (CustomTkinter, ROI baixo)
- Descrições em PT-BR: `test_normaliza_timestamp_unix_para_iso()`

## Ciclo de desenvolvimento

Skill `xp-cycle` (`.claude/skills/xp-cycle/SKILL.md`) — obrigatória em feature, bug e refactor.
Resumo: **Spec → Plan Mode → Teste (Red) → Implementar (Green) → Verificar → Refatorar → Commitar → `/my-verify` → CHECKLIST + JOURNAL**

Comandos: `/new-feature <descrição>` (ciclo completo) · `/my-verify` (agente independente roda testes e confere invariantes) · `/review` (checklist rápido inline)
Convenções detalhadas: `.claude/rules/code-conventions.md`.

## Estado do projeto

Toda sessão **abre lendo "Onde estou" no `CHECKLIST.md`** e **fecha registrando uma entry no `JOURNAL.md`** (estado no CHECKLIST, história no JOURNAL — nunca inflar o CHECKLIST com "Estado em DD-MM"). Ambos são pessoais (gitignored); se não existirem nesta máquina, recriar de `docs/desenvolvimento/TEMPLATE_CHECKLIST.md`. O "quê" de cada feature vai em `docs/specs/`; decisões estruturais viram ADR em `docs/decisions/`.

## Skills do ecossistema

Skills externas só com confirmação, auditadas e versionadas no projeto — política em `.claude/rules/skills-policy.md`. Regras deste projeto vencem sempre.

## Não faça

- **NÃO use `flagsMask=65281`** — filtra mensagens data-only e perde `pwr_ext`
- **NÃO use `self.sid` para chamadas GIS** — usar `self.gis_sid`
- **NÃO hardcode URL de geocodificação** — vem do login em `data["gis_geocode"]` (+ host da API no path)
- **NÃO use `gis_sid` nem `search_provider` no geocode** — use `uid` + sessão (POST); `error=7` é o provider recusado, não billing
- **NÃO use `voltage` como fallback de `battery_voltage`** — é bateria interna do tracker
- **NÃO hardcode `"odometer": None`** — ler de `params.get("odometer")` e converter m→km
- **NÃO adicione dependências sem perguntar** — PyInstaller é sensível a imports inesperados
- **NÃO use `git add .`** — pode incluir `.env` ou logs
- **NÃO deixe `except Exception: pass`** — sempre `logger.debug(f"Erro: {e}")`
- **NÃO acesse API Wialon diretamente da GUI** — passar pelos services
- **NÃO commite direto na `main`**

## Compactação

Quando o contexto for compactado, preservar:
- "Onde estou" do `CHECKLIST.md` e a fatia/spec em andamento
- Arquivos modificados na sessão ainda não commitados
- Decisões arquiteturais tomadas e erros encontrados
