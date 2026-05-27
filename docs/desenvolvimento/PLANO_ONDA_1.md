# Plano de Implementação — Onda 1 (v1.1.0)

> **Referência de decisões:** [`CHECKLIST_DECISOES.md`](CHECKLIST_DECISOES.md)
> **Ciclo:** `.claude/skills/xp-cycle.md`
> **Regra:** cada fase é autônoma — não quebra o app se parar aqui. Commitar ao final de cada fase.

---

## Tabela de acompanhamento

| # | Fase | Grupo | TDD | Esforço | Status | Arquivos principais |
|---|------|-------|-----|---------|--------|---------------------|
| 01 | Limpeza de código morto | C | — | S | ✅ Concluído | `system_a_client.py`, `normalizer.py`, `config.py`, `.env` |
| 02 | Bugs rápidos da GUI | B | 🔴 parcial | XS | ✅ Concluído | `export.py`, `home.py`, `vehicle_service.py` |
| 03 | Odômetro — ler do param bruto | A | 🔴 sim | XS | ✅ Concluído | `wialon_transformer.py` |
| 04 | `pwr_ext` — flagsMask + propagação | A | 🔴 sim | S | ✅ Concluído | `wialon_client.py`, `vehicle_service.py`, `wialon_transformer.py` |
| 05 | Bateria — remover fallback interno | A | 🔴 sim | XS | ✅ Concluído | `wialon_transformer.py` |
| 06 | Geocodificação — gis_sid dinâmico | A | — | XS | ✅ Concluído | `wialon_client.py` |
| 07 | Export — valores `N/D` | A | 🔴 sim | XS | ✅ Concluído | `exporter.py` |
| 08 | `env_writer.py` — novo módulo | D | 🔴 sim | S | ⬜ Todo | `src/core/env_writer.py` ← NOVO |
| 09 | `config.py` — reload + TOKEN_2 | D+E | 🔴 sim | XS | ⬜ Todo | `config.py` |
| 10 | F1 — Token Wialon pela GUI | D | — | M | ⬜ Todo | `settings.py` |
| 11 | F2 — Segunda conta: capturar username | E | 🔴 sim | XS | ⬜ Todo | `wialon_client.py` |
| 12 | F2 — Segunda conta: Settings + Export | E | — | M | ⬜ Todo | `settings.py`, `export.py`, `exporter.py` |
| 13 | UX — Mês por nome + Abrir pasta + Onboarding | F | — | S | ⬜ Todo | `export.py`, `app.py` |
| 14 | Testes — reescrever com pytest | G | — | S | ⬜ Todo | `tests/`, `pytest.ini` |
| 15 | CI — workflows + version sync + deps | G | — | S | ⬜ Todo | `ci.yml`, `build.yml`, `spec`, `requirements` |

**Legenda status:** ⬜ Todo · 🔄 Em andamento · ✅ Concluído · ⏸️ Bloqueado
**Legenda TDD:** 🔴 sim = escrever teste antes de implementar · 🔴 parcial = só nos bugs com lógica testável · — = não aplicável

---

## Fase 01 — Limpeza de código morto

**Objetivo:** remover System A e método não usado antes de qualquer outra mudança.
**TDD:** não aplicável — remoção de código, sem comportamento novo.

**Deletar:**
- `src/clients/system_a_client.py`

**Editar:**

`src/services/normalizer.py`
- Remover o bloco `"system_a": {...}` do `system_mappings`

`src/core/config.py`
- Remover `SYSTEM_A_BASE_URL` e `SYSTEM_A_TOKEN`

`.env` e `.env.example`
- Remover linhas `SYSTEM_A_*`

`src/clients/wialon_client.py`
- Deletar método `get_full_history` (~linhas 515–534)

`docs/desenvolvimento/normalizer_usage.md` e `exporter_usage.md`
- Remover referências ao System A

**Commit:** `refactor: remove SystemA legacy code and unused get_full_history`

---

## Fase 02 — Bugs rápidos da GUI

**Objetivo:** corrigir 4 bugs que causam crashes ou comportamentos errados.
**TDD:** 🔴 parcial — C1 e C4 têm lógica testável; C2 e C7 são mudanças de GUI/logging.

### 🔴 Testes primeiro (Red) — C1 e C4

```python
# tests/test_vehicle_service.py

def test_upload_result_usa_uploaded_files():
    """C1 — garante que UploadResult tem uploaded_files, não uploaded_count."""
    from src.services.uploader import UploadResult
    result = UploadResult(uploaded_files=["exports/veiculo.csv"], failed_files=[])
    assert hasattr(result, "uploaded_files")
    assert len(result.uploaded_files) == 1

def test_page_size_propagado_ao_get_history(mocker):
    """C4 — garante que WIALON_PAGE_SIZE chega ao client."""
    from src.services.vehicle_service import VehicleService
    mock_client = mocker.MagicMock()
    mock_client.get_history.return_value = iter([[]])
    svc = VehicleService(client=mock_client)
    svc._process_vehicle_history(vehicle_id=1, time_from=0, time_to=1, sensor_map={})
    call_kwargs = mock_client.get_history.call_args
    assert call_kwargs is not None
    assert "page_size" in call_kwargs.kwargs or len(call_kwargs.args) >= 4
```

```bash
pytest -q   # deve FALHAR aqui
```

### ✅ Implementar (Green)

**`src/gui/frames/export.py`**
```python
# Bug C1 — linha ~363
# Antes:
ur.uploaded_count
# Depois:
len(ur.uploaded_files)
```

**`src/gui/frames/home.py`**
```python
# Bug C2 — _show_error()
# Antes:
CTkInputDialog(text=message, title="Erro")
# Depois:
import tkinter.messagebox as mb
mb.showerror("Erro", message)
```

**`src/services/vehicle_service.py`**
```python
# Bug C4 — passar page_size ao chamar get_history
page_size = settings.WIALON_PAGE_SIZE or 1000
for page in self.client.get_history(vehicle_id, t_from, t_to, page_size=page_size):
    ...

# Bug C7 — logar erros engolidos
except Exception as e:
    logger.debug(f"Erro: {e}")
```

**Commit:** `fix: upload crash, error dialog, page_size propagation and silent exceptions`

---

## Fase 03 — Odômetro: ler do param bruto

**Objetivo:** remover o `None` hardcoded e ler o odômetro real da API.
**TDD:** 🔴 sim — transformação pura, input→output definível.

### 🔴 Testes primeiro (Red)

```python
# tests/test_wialon_transformer.py

def test_odometro_converte_metros_para_km():
    """Odômetro vem em metros da API — deve sair em km."""
    transformer = WialonTransformer(client=mock_client)
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"odometer": 8661339}
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["odometer"] == 8661.339

def test_odometro_nulo_quando_param_ausente():
    msg = {"t": 1700000000, "pos": {"y": -22.87, "x": -43.29, "s": 0}, "p": {}}
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["odometer"] is None

def test_odometro_fallback_para_new_mileage():
    msg = {"t": 1700000000, "pos": {"y": -22.87, "x": -43.29, "s": 0},
           "p": {"new_mileage": 5000000}}
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["odometer"] == 5000.0
```

```bash
pytest -q   # deve FALHAR aqui
```

### ✅ Implementar (Green)

**`src/services/wialon_transformer.py`**
```python
# Antes — linha ~115:
"odometer": None,  # Wialon não retorna odômetro direto nas mensagens

# Depois:
odometer_m = (params.get("odometer")
              or params.get("new_mileage")
              or params.get("mileage"))
"odometer": round(odometer_m / 1000, 2) if odometer_m else None,
```

**Commit:** `fix: read odometer from raw params and convert meters to km`

---

## Fase 04 — `pwr_ext`: flagsMask + propagação

**Objetivo:** capturar mensagens data-only com `pwr_ext` e propagar para registros GPS.
**TDD:** 🔴 sim — lógica de propagação é testável de forma isolada.

### 🔴 Testes primeiro (Red)

```python
# tests/test_vehicle_service.py

def test_transformer_retorna_none_para_mensagem_sem_pos():
    """Mensagens sem GPS não devem virar linha no export."""
    msg = {"t": 1700000000, "pos": None, "p": {"pwr_ext": 14.2}}
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record is None

def test_pwr_ext_propagado_para_proximo_registro_gps():
    """pwr_ext de mensagem data-only deve aparecer no próximo registro com GPS."""
    msgs = [
        {"t": 1700000000, "pos": None, "p": {"pwr_ext": 14.2}},
        {"t": 1700000001, "pos": {"y": -22.87, "x": -43.29, "s": 30}, "p": {}},
    ]
    records = process_messages(msgs, vehicle_id=1, sensor_map={})
    assert len(records) == 1
    assert records[0]["battery_voltage"] == 14.2
```

```bash
pytest -q   # deve FALHAR aqui
```

### ✅ Implementar (Green)

**`src/clients/wialon_client.py`** → `get_history()`
```python
"flagsMask": 0,  # captura todos os tipos de mensagem
```

**`src/services/wialon_transformer.py`** → `transform_message()`
- Retornar `None` se `pos` for vazio (mensagem sem GPS não vira linha no export)

**`src/services/vehicle_service.py`** → loop de processamento
```python
last_pwr_ext = None
for page in self.client.get_history(...):
    for msg in page:
        params = msg.get("p", {}) or {}
        if "pwr_ext" in params:
            last_pwr_ext = params["pwr_ext"]
        record = transformer.transform_message(msg, ...)
        if record is None:
            continue
        if record.get("battery_voltage") is None and last_pwr_ext is not None:
            record["battery_voltage"] = last_pwr_ext
        records.append(record)
```

**Commit:** `fix: fetch all message types to capture pwr_ext and propagate to GPS records`

---

## Fase 05 — Bateria: remover fallback da bateria interna

**Objetivo:** não retornar 4.1V (bateria do tracker) como se fosse tensão do veículo.
**TDD:** 🔴 sim — comportamento de fallback é testável.

### 🔴 Testes primeiro (Red)

```python
# tests/test_wialon_transformer.py

def test_battery_voltage_nao_usa_voltage_interno():
    """'voltage' é bateria interna do tracker — não deve preencher battery_voltage."""
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"voltage": 4157}  # bateria interna ~4.1V
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["battery_voltage"] is None  # não deve usar voltage como fallback

def test_battery_voltage_usa_pwr_ext():
    """pwr_ext é a tensão real do veículo."""
    msg = {
        "t": 1700000000,
        "pos": {"y": -22.87, "x": -43.29, "s": 0},
        "p": {"pwr_ext": 12.6}
    }
    record = transformer.transform_message(msg, vehicle_id=1, sensor_map={})
    assert record["battery_voltage"] == 12.6
```

```bash
pytest -q   # deve FALHAR aqui
```

### ✅ Implementar (Green)

**`src/services/wialon_transformer.py`**
```python
# Antes:
"battery_voltage": ["pwr_ext", "pwr_int", "voltage", "battery", "power", "batt"],

# Depois:
"battery_voltage": ["pwr_ext", "pwr_int", "power", "batt"],
```

**Commit:** `fix: remove internal battery fallback from battery_voltage resolution`

---

## Fase 06 — Geocodificação: gis_sid dinâmico

**Objetivo:** preparar o código para quando o serviço for habilitado na conta.
**TDD:** não aplicável — mudança preparatória pequena, sem lógica nova testável isoladamente.

**`src/clients/wialon_client.py`** → `__init__()` e `authenticate()`
```python
# __init__
self.gis_sid: Optional[str] = None
self.gis_geocode_url: Optional[str] = None

# authenticate() — após obter data do login
self.gis_sid = data.get("gis_sid")
gis_geocode = data.get("gis_geocode", "")
if gis_geocode:
    self.gis_geocode_url = f"{gis_geocode.rstrip('/')}/gis_geocode"
```

**Commit:** `fix: save gis_sid and dynamic geocode URL from login response`

---

## Fase 07 — Export: valores `N/D`

**Objetivo:** substituir `None` por `"N/D"` nas colunas de sensores opcionais.
**TDD:** 🔴 sim — comportamento de exportação é testável via arquivo gerado.

### 🔴 Testes primeiro (Red)

```python
# tests/test_exporter.py

def test_colunas_opcionais_sem_dado_exportam_nd(tmp_path):
    """Campos de sensor ausentes devem aparecer como N/D no CSV."""
    record = {
        "vehicle_id": 1, "vehicle_name": "Teste", "plate": "TST-0001",
        "timestamp": "2026-04-01T10:00:00",
        "latitude": -22.87, "longitude": -43.29,
        "speed": 0, "ignition": True,
        "odometer": None, "fuel_level": None, "rpm": None,
        "battery_voltage": None, "engine_hours": None,
        "driver": None, "address": None,
    }
    exporter = DataExporter(base_dir=str(tmp_path))
    path = exporter.export_history_to_csv([record], vehicle_name="Teste", month=4, year=2026)
    import pandas as pd
    df = pd.read_csv(path)
    assert df["Odômetro (km)"].iloc[0] == "N/D"
    assert df["RPM"].iloc[0] == "N/D"

def test_colunas_obrigatorias_nao_recebem_nd(tmp_path):
    """Latitude, longitude, velocidade e ignição nunca recebem N/D."""
    # ... mesmo setup
    assert df["Latitude"].iloc[0] != "N/D"
    assert df["Velocidade (km/h)"].iloc[0] != "N/D"
```

```bash
pytest -q   # deve FALHAR aqui
```

### ✅ Implementar (Green)

**`src/services/exporter.py`**
```python
OPTIONAL_SENSOR_COLS = [
    "odometer", "fuel_level", "rpm",
    "battery_voltage", "engine_hours", "driver", "address"
]

def _fill_nd(record: dict) -> dict:
    for col in OPTIONAL_SENSOR_COLS:
        if record.get(col) is None:
            record[col] = "N/D"
    return record
```

**Commit:** `feat: replace None with N/D for unavailable sensor columns in export`

---

## Fase 08 — `env_writer.py`: novo módulo

**Objetivo:** criar helper que escreve no `.env` preservando ordem e comentários.
**TDD:** 🔴 sim — módulo novo do zero, comportamento 100% testável.

### 🔴 Testes primeiro (Red)

```python
# tests/test_env_writer.py

from src.core.env_writer import set_env_value

def test_cria_arquivo_env_se_nao_existe(tmp_path):
    env_file = tmp_path / ".env"
    set_env_value("WIALON_TOKEN", "abc123", env_path=str(env_file))
    assert env_file.read_text() == "WIALON_TOKEN=abc123\n"

def test_atualiza_chave_existente(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("WIALON_TOKEN=antigo\nEXPORT_DIR=./exports\n")
    set_env_value("WIALON_TOKEN", "novo", env_path=str(env_file))
    content = env_file.read_text()
    assert "WIALON_TOKEN=novo" in content
    assert "EXPORT_DIR=./exports" in content  # preservou outras linhas

def test_insere_chave_nova_no_final(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("EXPORT_DIR=./exports\n")
    set_env_value("WIALON_TOKEN_2", "xyz789", env_path=str(env_file))
    lines = env_file.read_text().splitlines()
    assert "WIALON_TOKEN_2=xyz789" in lines

def test_preserva_comentarios(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("# Wialon\nWIALON_TOKEN=antigo\n")
    set_env_value("WIALON_TOKEN", "novo", env_path=str(env_file))
    assert "# Wialon" in env_file.read_text()
```

```bash
pytest -q   # deve FALHAR aqui
```

### ✅ Implementar (Green)

**`src/core/env_writer.py`** ← NOVO
```python
from pathlib import Path
import re

def set_env_value(key: str, value: str, env_path: str = ".env") -> None:
    """Atualiza KEY=value no .env. Cria o arquivo se não existir."""
    path = Path(env_path)
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []

    pattern = re.compile(rf"^{re.escape(key)}\s*=")
    new_line = f"{key}={value}"
    updated = False

    for i, line in enumerate(lines):
        if pattern.match(line):
            lines[i] = new_line
            updated = True
            break

    if not updated:
        lines.append(new_line)

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
```

**Commit:** `feat: add env_writer module for safe .env updates`

---

## Fase 09 — `config.py`: reload() + WIALON_TOKEN_2

**Objetivo:** suportar recarregamento em memória e segunda conta.
**TDD:** 🔴 sim — comportamento do reload é testável.

### 🔴 Testes primeiro (Red)

```python
# tests/test_config.py

def test_reload_carrega_novo_token(tmp_path, monkeypatch):
    """settings.reload() deve refletir mudança no .env sem reiniciar."""
    env_file = tmp_path / ".env"
    env_file.write_text("WIALON_TOKEN=antigo\n")
    monkeypatch.chdir(tmp_path)

    from src.core.config import Settings
    s = Settings()
    assert s.WIALON_TOKEN == "antigo"

    env_file.write_text("WIALON_TOKEN=novo\n")
    s.reload()
    assert s.WIALON_TOKEN == "novo"

def test_wialon_token_2_vazio_por_padrao():
    from src.core.config import settings
    assert hasattr(settings, "WIALON_TOKEN_2")
    # Se não configurado, deve ser string vazia
    assert isinstance(settings.WIALON_TOKEN_2, str)
```

```bash
pytest -q   # deve FALHAR aqui
```

### ✅ Implementar (Green)

**`src/core/config.py`**
```python
WIALON_TOKEN_2: str = os.getenv("WIALON_TOKEN_2", "")

def reload(self) -> None:
    load_dotenv(override=True)
    self.WIALON_TOKEN = os.getenv("WIALON_TOKEN", "")
    self.WIALON_TOKEN_2 = os.getenv("WIALON_TOKEN_2", "")
    self.EXPORT_DIR = os.getenv("EXPORT_DIR", "./exports")
    self.WIALON_PAGE_SIZE = int(os.getenv("WIALON_PAGE_SIZE", "1000"))
    self.GOOGLE_DRIVE_CREDENTIALS_FILE = os.getenv("GOOGLE_DRIVE_CREDENTIALS_FILE", "./client_secrets.json")
    self.GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
```

**Commit:** `feat: add WIALON_TOKEN_2 and settings.reload() for live config updates`

---

## Fase 10 — F1: Token Wialon pela GUI

**Objetivo:** permitir editar, gerar e testar o token da Conta 1 diretamente na interface.
**TDD:** não aplicável — mudança de GUI (CustomTkinter). Testar manualmente.

**`src/gui/frames/settings.py`** → `_create_wialon_section()`

Nova UI:
```
🔌 Wialon API — Conta 1
Token: [••••••••••••••••••] [👁] [🔗 Gerar] [💾 Salvar] [🔍 Testar]
Status: ✅ Conectado como "movi"
```

- Campo `CTkEntry(show="*")` carregado com token real
- Botão 👁️ alterna `show=""` / `show="*"`
- Botão 🔗 abre `webbrowser.open(URL_AUTORIZACAO_WIALON)`
- Botão 💾 → `env_writer.set_env_value("WIALON_TOKEN", value)` + `settings.reload()`
- Botão 🔍 → `WialonClient(token=entry_value).authenticate()` → atualiza label de status

**Commit:** `feat(F1): add Wialon token editing, generation and testing in Settings`

---

## Fase 11 — F2: Capturar username no login

**Objetivo:** saber o nome real da conta para exibir no seletor.
**TDD:** 🔴 sim — feature nova com comportamento testável via mock.

### 🔴 Testes primeiro (Red)

```python
# tests/test_wialon_client.py

def test_authenticate_salva_username(requests_mock):
    """Username da conta deve ser salvo após autenticação."""
    requests_mock.get(
        "https://hst-api.wialon.com/wialon/ajax.html",
        json={"eid": "abc123", "au": {"nm": "movi"}, "gis_sid": "xyz", "base_url": "https://hst-api.wialon.com"}
    )
    client = WialonClient(token="fake_token")
    client.authenticate()
    assert client.username == "movi"

def test_authenticate_salva_gis_sid(requests_mock):
    requests_mock.get(..., json={"eid": "abc", "gis_sid": "gis_abc", "base_url": "..."})
    client = WialonClient(token="fake_token")
    client.authenticate()
    assert client.gis_sid == "gis_abc"
```

```bash
pytest -q   # deve FALHAR aqui
```

### ✅ Implementar (Green)

**`src/clients/wialon_client.py`**
```python
# __init__
self.username: str = ""

# authenticate() — após obter data
user = data.get("au", {})
if isinstance(user, dict):
    self.username = user.get("nm", "")
elif isinstance(user, str):
    self.username = user
```

**Commit:** `feat(F2): capture Wialon username from login response`

---

## Fase 12 — F2: Segunda conta: Settings + Export + subpastas

**Objetivo:** UI completa para segunda conta e seletor condicional no Export.
**TDD:** não aplicável — mudança de GUI. Testar manualmente.

**`src/gui/frames/settings.py`**
- Adicionar `_create_wialon_section_2()` com mesma UI da Conta 1
- Usa `WIALON_TOKEN_2` no `env_writer`

**`src/gui/frames/export.py`**
```python
if settings.WIALON_TOKEN_2:
    self.account_menu = ctk.CTkOptionMenu(
        self, values=["Conta 1", "Conta 2"],
        variable=self.account_var
    )
```

**`src/services/exporter.py`**
```python
# Subpasta por conta
export_dir = Path(self.base_dir) / f"{year}-{month:02d}" / account_name
```

**Commit:** `feat(F2): second account support with conditional selector and separate export folders`

---

## Fase 13 — UX: mês por nome + abrir pasta + onboarding

**Objetivo:** três melhorias de UX agrupadas por serem pequenas.
**TDD:** não aplicável — mudanças de GUI. Testar manualmente.

**Mês por nome** (`src/gui/frames/export.py`):
```python
MESES = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho",
         "Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
month_int = MESES.index(self.month_var.get()) + 1
```

**Abrir pasta** (`src/gui/frames/export.py`):
```python
def _open_export_folder(self, path: str):
    if sys.platform == "win32":
        subprocess.Popen(["explorer", path])
    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])
```

**Onboarding** (`src/gui/app.py`):
```python
if not settings.WIALON_TOKEN:
    self._show_setup_notice()
```

**Commit:** `feat: month names, open exports folder button, and empty token onboarding`

---

## Fase 14 — Testes: reescrever com pytest

**Objetivo:** converter testes existentes (sem assert) para pytest real.
**TDD:** não aplicável — esta fase É a escrita de testes.

**`tests/test_normalizer.py`**
- Remover `sys.path.insert` hardcoded
- Converter para `test_*` com `assert`
- Focar no mapping `wialon` (não `system_a`)

**`tests/test_exporter.py`**
- Idem — assert no CSV/Excel gerado (colunas, N/D, estrutura de pastas)

**`pytest.ini`** ← NOVO
```ini
[pytest]
pythonpath = .
testpaths = tests
```

**Commit:** `test: rewrite tests with pytest and real assertions focused on Wialon mapping`

---

## Fase 15 — CI: workflows + version sync + deps + UPX

**Objetivo:** fechar a onda com infraestrutura sólida.
**TDD:** não aplicável — configuração de CI/infra.

**`.github/workflows/ci.yml`** ← NOVO
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt pytest ruff
      - run: pytest -q
      - run: ruff check src/
```

**`.github/workflows/build.yml`**
```yaml
- name: Validar versão
  run: |
    APP_VER=$(python -c "from src.gui import __version__; print(__version__)")
    TAG_VER="${GITHUB_REF_NAME#v}"
    if [ "$APP_VER" != "$TAG_VER" ]; then
      echo "ERRO: __version__=$APP_VER mas tag=$TAG_VER"; exit 1
    fi
```

**`movi_exporter.spec`**
```python
import sys; sys.path.insert(0, '.')
from src.gui import __version__
# Usar __version__ em CFBundleVersion e CFBundleShortVersionString
upx=False,
```

**`requirements.in`** ← NOVO
```
requests
python-dotenv
loguru
pandas
openpyxl
google-auth
google-auth-oauthlib
google-api-python-client
customtkinter
pyinstaller
packaging
```

**Commit:** `ci: add CI workflow, version validation, pin requirements and disable UPX`

---

## Resumo de arquivos por fase

| Fase | TDD | Criados | Editados | Deletados |
|------|-----|---------|----------|-----------|
| 01 | — | — | `normalizer.py`, `config.py`, `.env`, `.env.example`, docs | `system_a_client.py` |
| 02 | 🔴 parcial | — | `export.py`, `home.py`, `vehicle_service.py` | — |
| 03 | 🔴 | — | `wialon_transformer.py` | — |
| 04 | 🔴 | — | `wialon_client.py`, `vehicle_service.py`, `wialon_transformer.py` | — |
| 05 | 🔴 | — | `wialon_transformer.py` | — |
| 06 | — | — | `wialon_client.py` | — |
| 07 | 🔴 | — | `exporter.py` | — |
| 08 | 🔴 | `env_writer.py`, `test_env_writer.py` | — | — |
| 09 | 🔴 | `test_config.py` | `config.py` | — |
| 10 | — | — | `settings.py` | — |
| 11 | 🔴 | `test_wialon_client.py` | `wialon_client.py` | — |
| 12 | — | — | `settings.py`, `export.py`, `exporter.py` | — |
| 13 | — | — | `export.py`, `app.py` | — |
| 14 | — | `pytest.ini` | `tests/test_normalizer.py`, `tests/test_exporter.py` | — |
| 15 | — | `ci.yml`, `requirements.in` | `build.yml`, `movi_exporter.spec`, `requirements.txt` | — |
