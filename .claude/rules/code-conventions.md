# Convenções de código — Movi Exporter

Derivadas do código existente. Em caso de dúvida, imitar o módulo vizinho.
Regras críticas da Wialon ficam na skill `wialon-api`; o ciclo fica em `xp-cycle`.

## Idioma

- **Identificadores** (módulos, classes, funções, variáveis): inglês.
- **Docstrings, comentários, UI, mensagens de log e de erro, testes**: português
  brasileiro. (É o padrão real do código; não "traduzir" módulos legados.)
- Comentar só o **porquê** não-óbvio (limiar, ordem que importa, bug histórico).
  Nunca comentar o quê — o código já diz.

## Layout e camadas

```
src/core/      config (settings), logger (loguru → app.log), env_writer, service_factory
src/clients/   wialon_client (stateful, único cliente real) + protocols (TrackingClient)
src/services/  vehicle_service (orquestra) → wialon_transformer → normalizer → exporter
               uploader (Drive), export_history, tracker_profiles/ (perfis por fabricante)
src/gui/       app, frames/, components/, dialogs/, theme/design/icons, updater
src/cli/       main (mesmos services, sem GUI)
tests/         pytest, espelha src por módulo: tests/test_<modulo>.py
```

**Sentido das dependências (não inverter):**
`gui`/`cli` → `core/service_factory` → `services` → `clients` → rede.

- GUI e CLI **nunca** importam `src.clients`; obtêm um `VehicleService` via
  `build_vehicle_service(account, export_dir)` em `src/core/service_factory.py`.
- Services dependem do `Protocol` `TrackingClient` (`src/clients/protocols.py`),
  não de `WialonClient` concreto — permite mock em teste.
- Config só via `from src.core.config import settings`; segredos só no `.env`.

## Como criar um recurso novo

| Quero… | Faço… |
|--------|-------|
| Nova coluna no export | Spec em `docs/specs/` → transformer (`wialon_transformer.py`) → normalizer (mapping) → exporter (`OPTIONAL_SENSOR_COLS` + `COLUMN_TRANSLATIONS`) → golden test atualizado → manual do usuário (`docs/manual/manual.html`) |
| Suporte a outro tracker | Novo módulo em `src/services/tracker_profiles/`, herdando `TrackerProfile` (`base.py`); registrar em `registry.py::DEFAULT_PROFILES` **antes** do `DefaultProfile` |
| Nova chamada à Wialon | Método em `WialonClient` (usa `self._request(svc, params)`, `sid`/`gis_sid` corretos) → expor no `TrackingClient` se services precisarem → teste com `requests-mock` |
| Nova tela/ação na GUI | Frame em `src/gui/frames/`, lógica pura testável em módulo separado (ex.: `validation.py`, `account_state.py`); trabalho pesado em `threading.Thread(daemon=True)` e volta à UI com `self.after(0, ...)` |
| Novo comando CLI | Subcomando em `src/cli/main.py` usando os mesmos services |

## Erros e logs

- Exceções de domínio herdam de `WialonError` (`WialonAuthError`,
  `WialonValidationError`). Services deixam subir; GUI/CLI traduzem para
  mensagem em PT-BR ao usuário.
- `from src.core.logger import logger` (loguru). Nunca `print` fora do CLI.
- **Nunca** `except Exception: pass`. Mínimo: `logger.debug(f"Erro ao X: {e}")`.
  Se precisar de `# noqa: BLE001`, justificar na mesma linha.
- Falhas parciais por veículo não abortam o export inteiro — logar e seguir.

## Dados

- Sensor sem dado → `"N/D"` **no exporter** (`exporter.py` substitui
  `None`/`""`). Transformer e normalizer devolvem `None`, nunca `"N/D"`,
  `0`, `NaN` ou `""` — mascarar cedo esconde bugs.
- Odômetro em km (API dá metros). Timestamps: unix → ISO local.
- Deduplicar/cachear o que é caro (geocode, lista de motoristas, sensores por
  veículo) no escopo do export, nunca em disco.

## Estilo

- Python alvo: **3.12** (CI e build). O venv local pode ser mais novo (3.14) —
  não usar sintaxe/lib que só exista acima de 3.12.
- Type hints em toda interface pública (`typing.Dict/List/Optional` é o padrão
  do código; manter consistência no arquivo que está editando).
- `ruff check src/` com regras default (E/F), versão pinada no CI (`0.15.14`).
  Não adicionar config de ruff/pyproject sem decisão explícita.
- Constantes de módulo em `UPPER_SNAKE` com comentário do porquê do valor.
- Imports: stdlib → terceiros → `src.*`, em blocos separados.
- Sem dependências novas sem perguntar (PyInstaller quebra com import
  inesperado). Se aprovada: `requirements.in` → `pip-compile` → `requirements.txt`.

## Testes

- `pytest -q` na raiz (`pytest.ini` já aponta `pythonpath=.`).
- Nomes descritivos em PT-BR: `test_parse_vehicle_ids_ignora_espacos()`.
- Wialon sempre mockada com `requests-mock`; nunca token real em teste.
- Fixtures compartilhadas em `tests/conftest.py` (`ctk_root` para widgets;
  pula sem display).
- Mudou coluna/valor de export → atualizar o golden
  (`tests/test_vehicle_service_export_golden.py`) **conscientemente**, com a
  spec justificando.
