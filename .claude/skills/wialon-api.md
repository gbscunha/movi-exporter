# Wialon API — Referência Técnica

## Autenticação

Fluxo stateful — cada sessão segue:

```
token/login → eid (sid) + gis_sid + URLs dinâmicas
    ↓
core/search_items  (usa sid)
core/search_item   (usa sid)
messages/load_interval (usa sid)
    ↓
gis_geocode  (usa gis_sid — session diferente!)
    ↓
core/logout
```

### Campos do login
```json
{
  "eid": "...",           // sid para chamadas de API
  "gis_sid": "...",       // sid para chamadas GIS — diferente!
  "gis_geocode": "https://geocode-maps.wialon.us",  // URL dinâmica
  "gis_search":  "https://search-maps.wialon.us",
  "base_url":    "https://hst-api.wialon.us",       // host regional
  "au": { "nm": "movi" } // username da conta
}
```

Salvar: `self.sid`, `self.gis_sid`, `self.uid` (`user.id`), `self.gis_geocode_url`, `self.base_url`, `self.username`.

## Mensagens (`messages/load_interval`)

```python
params = {
    "itemId": vehicle_id,
    "timeFrom": unix_ts,
    "timeTo": unix_ts,
    "flags": 1,
    "flagsMask": 0,        # 0 = todos os tipos. NÃO usar 65281
    "loadCount": 1000,
}
```

**`flagsMask=65281` filtra mensagens data-only** — onde vem `pwr_ext`. Sempre usar `flagsMask=0`.

### Tipos de mensagem e o que cada uma contém

| Tipo | `pos` | Params típicos |
|------|-------|---------------|
| Posição (GPS) | presente | `acc`, `speed`, sensores CAN |
| Data-only | ausente | `pwr_ext` (tensão do veículo) |
| Evento | presente ou ausente | `alarm`, alertas |

Mensagens sem `pos` → não viram linha no export, mas seus params devem ser aproveitados (ex: propagar `pwr_ext` para o próximo registro GPS).

## Parâmetros brutos (campo `p`)

| Param | Significado | Conversão |
|-------|-------------|-----------|
| `odometer` | odômetro em **metros** | ÷ 1000 → km |
| `pwr_ext` | tensão veículo (V) | direto (~12-28V) |
| `voltage` | bateria interna do tracker (V) | ~4V — NÃO usar como tensão do veículo |
| `power` | tensão em mV | ÷ 1000 → V (formula: `power*const0.001`) |
| `acc` | ignição (0/1) | bool |
| `fuel_lvl` | combustível bruto | formula: `fuel_lvl*const55/const255` |
| `io_2_94` | RPM bruto | formula: `io_2_94*const0.25` |
| `can_distance` | distância CAN em metros | ÷ 1000 → km |

## Sensores (`core/search_item` com `flags=4096`)

```python
params = {"id": vehicle_id, "flags": 4096}
# Retorna item["sens"] — dict de sensores configurados
```

Cada sensor tem:
- `n` — nome (ex: "RPM do motor")
- `p` — fórmula (ex: "io_2_94*const0.25")
- `t` — tipo (ex: "engine rpm")

Extrair parâmetro base da fórmula: primeiro token antes de `*`, `/`, `+`, `-`.

## Flags de `core/search_items`

```python
FLAGS_LIST_VEHICLES = (
    1          # geral
    | 8        # custom fields
    | 4096     # sensores
    | 8388608  # profile fields (placa, marca, modelo)
)
```

## Geocodificação (`gis_geocode`)

```
POST {gis_geocode}/{host_api}/gis_geocode    ← host da API DENTRO do path
    coords = [{"lon": -43.29, "lat": -22.87}]  (JSON, no corpo)
    flags  = 1255211008                        (endereço completo)
    uid    = {login["user"]["id"]}             ← uid, NÃO gis_sid nem provider
```

Retorna array de strings na mesma ordem das coordenadas (vazio = sem endereço).
- **POST**, não GET — o GET estoura em ~150 coords (HTTP 414). POST engole milhares.
- `error=7` NÃO é billing — é o `search_provider` explícito sendo recusado. Não
  envie provider nem `gis_sid`; use `uid` + sessão.
Ver `docs/wialon/GEOCODIFICACAO.md` para a receita completa e o porquê.

## Paginação do histórico

```python
while True:
    data = _request("messages/load_interval", params)
    messages = data.get("messages", [])
    if not messages:
        break
    last = messages[-1]
    new_last_time = last.get("t", last_time)
    same_time_count = sum(1 for m in messages if m.get("t") == new_last_time)
    if new_last_time == last_time and len(messages) < page_size:
        yield messages; break
    params["lastTime"] = new_last_time
    params["lastCount"] = same_time_count
    yield messages
    if len(messages) < page_size:
        break
```

## Códigos de erro relevantes

| Código | Significado | Ação |
|--------|-------------|------|
| 1 | Sessão expirada | Re-autenticar |
| 4 | Parâmetros inválidos | Revisar params |
| 7 | Acesso negado | Verificar permissões/billing |
| 8 | Token inválido | Gerar novo token (fluxo no manual: `docs/manual/manual.html`, seção 2) |
| 9 | Servidor indisponível | Retry |

## Duas contas

| | Conta 1 | Conta 2 |
|-|---------|---------|
| Username | `movi` | `lcmovi_mgr` |
| Env var | `WIALON_TOKEN` | `WIALON_TOKEN_2` |
| Rastreadores | Avançados (CAN bus) | Básicos (GPS only) |
| Dados | RPM, combustível, odômetro, motorista | Posição, ignição, pwr_ext (57% da frota) |
| Export | `exports/YYYY-MM/movi/` | `exports/YYYY-MM/lcmovi_mgr/` |
