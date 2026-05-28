# Retomada — Onde paramos (2026-05-27 noite)

> Documento temporário para retomar amanhã. Apagar quando concluído.

## Status do branch

- **Branch:** `feat/melhorias-v1` (NÃO foi feito push ainda)
- **Working tree:** clean após próximo commit
- **Último commit:** `d54157b docs: marca Fase 16 concluída e atualiza backlog Onda 2`

## Onda 1 — completa ✅

Todas as 16 fases concluídas e commitadas. `__version__ = 1.1.0`. Testes: 55 passando, ruff clean.

## QA manual revelou problemas no CSV real (frota Suntech do cliente)

Durante o QA, exportei VTR05 (Conta 1, Abril/2026). O CSV mostrou problemas que **NÃO foram corrigidos** pela Fase 16. Investiguei e identifiquei a causa raiz:

### Descobertas

1. **Tracker é Suntech ST380** (`model: 197`, `rep_type: 'STT'`)
2. **Admin Wialon configurou 4 sensores corretamente** EXCETO:
   - Sensor "Ignição" aponta pra param `in` → **`in` não existe nas msgs Suntech** → sensor inerte
3. **Suntech usa nomenclatura própria** para params críticos:
   - `mode` (0/1) = ignição (não `in`/`in1`/`din1`)
   - `m_asgn1` = odômetro em metros (não `odometer`/`mileage`)
   - `s_asgn1` = tensão do veículo (admin já configurou bem)
   - `s_asgn2` = bateria interna do tracker (admin configurou bem)
4. **Bug nosso:** `_normalize_sensor_name` confunde "Bateria do dispositivo" → mapeia pra `vehicle_voltage` (deveria `internal_battery_voltage`) porque pega "bateria" antes de chegar em "dispositivo"

### Próxima sessão — 3 fixes XS (decididos, prontos pra implementar)

São itens **#37, #38, #39** no `BACKLOG_ONDA_2.md` (todos 🔴 XS):

1. **#37** — `src/clients/wialon_client.py` → `_normalize_sensor_name`:
   ```python
   # Adicionar ANTES dos mappings ambíguos ("bateria", "battery"):
   "bateria do dispositivo": "internal_battery_voltage",
   "bateria do rastreador": "internal_battery_voltage",
   "device battery": "internal_battery_voltage",
   "tracker battery": "internal_battery_voltage",
   ```

2. **#38** — `src/services/wialon_transformer.py` → `KNOWN_PARAMS`:
   ```python
   # Adicionar "mode" no final da lista de ignição (Suntech ST380):
   "ignition": ["in", "in1", "din1", "ignition", "ign", "mode"],
   ```

3. **#39** — `src/services/wialon_transformer.py` → extração do odômetro:
   ```python
   odometer_m = next(
       (params[k] for k in ("odometer", "new_mileage", "mileage", "m_asgn1")
        if params.get(k) is not None),
       None,
   )
   ```

### Testes a adicionar

- `tests/test_pipeline_integration.py`:
  - Cenário Suntech: msg com `mode=1`, `s_asgn1=28.65`, `m_asgn1=240131878` → CSV mostra `Ignição=Ligado`, `Tensão do Veículo=28.65V`, `Odômetro=240131.88km`
  - Cenário Suntech parado: `mode=0` → `Ignição=Desligado`
- `tests/test_wialon_client.py`:
  - `_normalize_sensor_name("Bateria do dispositivo")` → `"internal_battery_voltage"`
  - `_normalize_sensor_name("Bateria do veículo")` → `"vehicle_voltage"`

### Como validar amanhã

1. Implementar as 3 mudanças + testes
2. `pytest -q` (esperar ~58+ passando) + `ruff check src/`
3. Re-exportar VTR05 via CLI:
   ```bash
   PYTHONPATH=. python -m src.cli.main export -m 4 -y 2026 -v 401987846 --no-consolidated
   ```
4. Confirmar no CSV:
   - `Ignição=Ligado` quando `Velocidade > 0`
   - `Ignição=Desligado` quando `Velocidade = 0`
   - `Tensão do Veículo (V)` ≈ 28V (andando) ou 25V (parado)
   - `Bateria Interna (V)` ≈ 4.1V
   - `Odômetro (km)` ≈ 240.131 (valor real, não N/D)
5. Considerar **Fase 17** no `PLANO_ONDA_1.md`: "Suporte a tracker Suntech ST380"
6. Bumpar pra `1.1.1`? Ou manter `1.1.0` (ainda não pusheamos)?
7. Push do branch

## Recursos úteis pra debug

Script de debug está em `/tmp/debug_vtr05.py` (provavelmente vai ser limpo se reiniciar a máquina). Pra recriar:

```bash
PYTHONPATH=. python -c "
from src.clients.wialon_client import WialonClient
c = WialonClient(); c.authenticate()
data = c._request('core/search_item', {'id': 401987846, 'flags': 4096})
for sid, s in data.get('item', {}).get('sens', {}).items():
    print(f'[{sid}] {s.get(\"n\")!r} -> {s.get(\"p\")!r}')
"
```

## Backlog Onda 2

40 itens no `docs/desenvolvimento/BACKLOG_ONDA_2.md`. Os itens 37-40 são os Suntech-related descobertos hoje. Os outros 36 são UI/UX descobertos no QA da GUI.

## Coisas que NÃO foram feitas (intencionalmente)

- ❌ Push do branch para o remoto
- ❌ Merge em `main`
- ❌ Tag `v1.1.0`

(Tudo isso depende de decidir se os fixes Suntech entram em `v1.1.0` ou viram `v1.1.1`)
