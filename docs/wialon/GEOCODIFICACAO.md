# Geocodificação Wialon — Status e Implementação

**Última atualização:** 2026-05-22

---

## Status atual

A coluna **Localização** nos arquivos exportados está **vazia** porque o serviço `gis_geocode` não está habilitado para a conta (`error=7 = Access denied`).

**Isso é uma questão de licença/billing**, não técnica. O código está pronto.

---

## O que foi descoberto (2026-05-22)

A resposta do `token/login` já retorna tudo que precisamos:

```json
{
  "eid": "...",
  "gis_sid": "4d126fa8af81514a",
  "gis_geocode": "https://geocode-maps.wialon.us",
  "gis_search": "https://search-maps.wialon.us",
  "gis_render": "https://render-maps.wialon.us",
  "gis_routing": "https://routing-maps.wialon.us"
}
```

**Importante:**
- `gis_sid` é diferente do `sid` principal — usar o `gis_sid` nas chamadas GIS
- A URL `gis_geocode` varia por conta/região — sempre usar a URL dinâmica do login, nunca hardcoded
- O código atual tinha ambos os bugs: usava `sid` errado e URL hardcoded

---

## Como habilitar

Solicitar ao **administrador da conta Wialon** (quem gerencia o contrato/licença):

> *"Precisamos habilitar o serviço de geocodificação (`gis_geocode`) para a conta. É necessário ativar no plano."*

Não é possível habilitar via API nem pelo painel de usuário comum — é configuração de conta/billing do lado Wialon.

---

## Endpoint (quando habilitado)

```
GET https://geocode-maps.wialon.us/gis_geocode
    ?coords=[{"lon":-43.29,"lat":-22.87},{"lon":-46.63,"lat":-23.55}]
    &flags=1255211008
    &gis_sid=<GIS_SESSION_ID_DO_LOGIN>
    &search_provider=osm
    &lang=pt
```

**Parâmetros:**

| Parâmetro | Obrigatório | Descrição |
|-----------|-------------|-----------|
| `coords` | Sim | Array JSON de coordenadas `[{"lon": float, "lat": float}]` |
| `flags` | Sim | Formato do endereço — usar `1255211008` (rua, casa, cidade, região, país) |
| `gis_sid` | Sim | **Session ID GIS** do login (campo `gis_sid`, não `eid`) |
| `search_provider` | Sim | Provedor: `osm`, `google`, `sygic`, `yandex`, `here`, `trimble` |
| `lang` | Não | Idioma — usar `pt` |

**Resposta (array na mesma ordem das coordenadas):**
```json
["Rua Exemplo, 100, Niterói, RJ, Brasil", "Av. Paulista, 1000, São Paulo, SP, Brasil"]
```

---

## Código pronto para implementar

### 1. Salvar `gis_sid` e `gis_geocode` no `WialonClient`

```python
# Em authenticate() — wialon_client.py
self.gis_sid = data.get("gis_sid")
self.gis_geocode_url = data.get("gis_geocode")
```

### 2. Método de geocodificação em batch

```python
def get_addresses_batch(
    self, coordinates: List[Dict[str, float]], provider: str = "osm"
) -> List[Optional[str]]:
    if not coordinates or not self.gis_sid or not self.gis_geocode_url:
        return [None] * len(coordinates)

    coords = [{"lon": c["lon"], "lat": c["lat"]} for c in coordinates]

    try:
        response = self._session.get(
            f"{self.gis_geocode_url}/gis_geocode",
            params={
                "coords": json.dumps(coords),
                "flags": 1255211008,
                "gis_sid": self.gis_sid,
                "search_provider": provider,
                "lang": "pt",
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "error" in data:
            logger.warning(f"Geocodificação indisponível: error={data['error']}")
            return [None] * len(coordinates)

        return [addr if addr else None for addr in data]

    except requests.RequestException as e:
        logger.warning(f"Erro na geocodificação: {e}")
        return [None] * len(coordinates)
```

### 3. Integração no `VehicleService`

Após coletar todos os registros de um veículo, agrupar coordenadas únicas e buscar endereços em batch (1 requisição por ~100m de precisão):

```python
# Agrupa coordenadas únicas por ~100m
unique_coords = {}
for record in all_records:
    lat, lon = record.get("latitude"), record.get("longitude")
    if lat and lon:
        key = (round(lat, 3), round(lon, 3))
        if key not in unique_coords:
            unique_coords[key] = {"lat": lat, "lon": lon}

# Busca endereços em batch
coords_list = list(unique_coords.values())
addresses = self.client.get_addresses_batch(coords_list)

# Aplica ao mapa
address_map = {
    (round(c["lat"], 3), round(c["lon"], 3)): addr
    for c, addr in zip(coords_list, addresses)
}

# Preenche nos registros
for record in all_records:
    lat, lon = record.get("latitude"), record.get("longitude")
    if lat and lon:
        key = (round(lat, 3), round(lon, 3))
        record["address"] = address_map.get(key)
```

---

## Flags de formato de endereço

| Flag | Formato |
|------|---------|
| `1255211008` | Rua, casa, cidade, região, país (completo) |
| `1241513984` | Rua e casa |

---

## Provedores disponíveis

- `osm` — OpenStreetMap (gratuito, boa cobertura Brasil)
- `google` — Google Maps
- `sygic` — Sygic
- `yandex` — Yandex
- `here` — HERE Maps
- `trimble` — Trimble
