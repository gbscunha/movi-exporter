# CLAUDE.md

App desktop Python que extrai dados mensais de rastreamento veicular da Wialon e exporta para CSV/Excel com upload opcional ao Google Drive. 1 cliente em produção (Windows). Mantenedor solo.

## Estrutura

```
src/core/        — config, logger, env_writer
src/clients/     — wialon_client (stateful), base_client
src/services/    — vehicle_service, wialon_transformer, normalizer, exporter, uploader
src/gui/         — app, frames/, components/, dialogs/, updater
src/cli/         — main
tests/           — pytest
docs/desenvolvimento/  — PLANO_ONDA_1.md, CHECKLIST_DECISOES.md
docs/wialon/           — TOKEN_AUTORIZACAO.md, GEOCODIFICACAO.md
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
python scripts/build.py               # build local
git tag v1.x.x && git push origin v1.x.x   # trigger CI → release
```

## Convenções

- Código e comentários em inglês; UI e mensagens em português brasileiro
- Type hints em toda interface pública
- `N/D` para campos de sensor sem dado — nunca `NaN` nem string vazia visível ao cliente
- Sem comentários óbvios — comentar apenas o *porquê* de algo não-óbvio

## Wialon API — regras críticas

Consulte `.claude/skills/wialon-api.md` para referência completa. Regras que nunca quebram:

- API é **stateful** — usa `sid`, NÃO Bearer token
- Login retorna **dois** session IDs: `eid` (API) e `gis_sid` (GIS) — usar o correto para cada chamada
- URLs de GIS são **dinâmicas** — vêm no login, nunca hardcoded
- `flagsMask=0` em `messages/load_interval` para capturar todos os tipos (incluindo data-only com `pwr_ext`)
- Odômetro vem em **metros** — sempre converter para km (÷ 1000)
- `pwr_ext` = tensão do veículo (~12-28V); `voltage` = bateria interna do tracker (~4V) — são coisas diferentes

**Token:** `docs/wialon/TOKEN_AUTORIZACAO.md` — gerado via formulário web, NÃO via API.

## Git

- Branch por feature: `feat/nome-curto` ou `fix/nome-curto`
- Commits em português, Conventional Commits: `tipo(escopo): descrição`
- Tipos: `feat`, `fix`, `refactor`, `test`, `chore`, `docs`, `ci`
- Escopos úteis: `wialon`, `gui`, `export`, `drive`, `ci`, `settings`
- Nunca commitar direto na `main`
- `git add` sempre com arquivos específicos — nunca `git add .`
- Nunca commitar `.env`, `credentials.json`, `token.json`, `*.log`

## Verificação

Antes de declarar qualquer tarefa concluída:
1. `pytest -q` — todos os testes passam
2. `ruff check src/` — zero erros
3. GUI abre e a feature funciona (testar o caminho principal manualmente)
4. Se mudou dados do export: abrir o arquivo gerado e confirmar colunas/valores
5. Se mudou `wialon_client.py`: testar com token real e conferir `app.log`

## Testes

- Focar em `normalizer` (mapping wialon), `exporter` (colunas, N/D) e `wialon_client` (paginação, re-auth)
- Usar `requests-mock` para mockar chamadas Wialon — sem gastar quota real
- Sem testes de GUI (CustomTkinter, ROI baixo)
- Descrições em PT-BR: `test_normaliza_timestamp_unix_para_iso()`

## Ciclo de desenvolvimento

Consulte `.claude/skills/xp-cycle.md` para o ciclo completo.
Resumo: **Consultar plano → Implementar fase → Verificar → Commitar → Atualizar status no PLANO_ONDA_1.md**

Skills disponíveis: `/nova-fase` (executa próxima fase do plano) · `/review` (revisa código da sessão)

## Não faça

- **NÃO use `flagsMask=65281`** — filtra mensagens data-only e perde `pwr_ext`
- **NÃO use `self.sid` para chamadas GIS** — usar `self.gis_sid`
- **NÃO hardcode URL de geocodificação** — vem do login em `data["gis_geocode"]`
- **NÃO use `voltage` como fallback de `battery_voltage`** — é bateria interna do tracker
- **NÃO hardcode `"odometer": None`** — ler de `params.get("odometer")` e converter m→km
- **NÃO adicione dependências sem perguntar** — PyInstaller é sensível a imports inesperados
- **NÃO use `git add .`** — pode incluir `.env` ou logs
- **NÃO deixe `except Exception: pass`** — sempre `logger.debug(f"Erro: {e}")`
- **NÃO acesse API Wialon diretamente da GUI** — passar pelos services
- **NÃO commite direto na `main`**

## Compactação

Quando o contexto for compactado, preservar:
- Fase atual do `PLANO_ONDA_1.md` e status de cada item
- Arquivos modificados na sessão ainda não commitados
- Decisões arquiteturais tomadas e erros encontrados
