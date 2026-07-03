# Geocodificação Wialon — endereço a partir de lat/lon

**Última atualização:** 2026-07-03 · **Status: ✅ implementado e funcionando**

A coluna **Localização** é preenchida com o endereço completo (rua, número,
bairro, cidade, UF, CEP, país) quando o export é feito com a opção **"Incluir
endereço"** ligada (opt-in). Sem ela, a coluna sai como `N/D`.

---

## ⚠️ Correção histórica (o que estava errado)

Por muito tempo achamos que o serviço estava **bloqueado por billing** (a chamada
retornava `error=7 = Access denied`). **Isso estava errado.** O serviço sempre
esteve disponível — a chamada é que estava malformada. Eram **3 erros combinados**:

| # | Errado (antigo) | Certo |
|---|-----------------|-------|
| 1 | URL `{gis_geocode}/gis_geocode` | `{gis_geocode}/{host_api}/gis_geocode` (host da API no path) |
| 2 | Autenticava com `gis_sid` | Usa **`uid`** (id do usuário, do login) + sessão |
| 3 | Enviava `search_provider=osm` | **Não envia provider** (a conta tem o seu padrão) |

O `error=7` era o `search_provider` explícito sendo recusado. Prova: sem provider
e com `uid`, a resposta vem com endereços reais.

---

## Receita correta (verificada com token real)

```
POST  {gis_geocode}/{host_api}/gis_geocode
        ex: https://geocode-maps.wialon.us/hst-api.wialon.us/gis_geocode

Corpo (form-encoded):
    coords = [{"lon": -43.359657, "lat": -22.818147}, ...]   (JSON)
    flags  = 1255211008                                       (endereço completo)
    uid    = 401955931                                        (login["user"]["id"])

NÃO enviar: gis_sid, search_provider
```

**De onde vem cada parte (tudo do `token/login`):**
- `{gis_geocode}` → campo `gis_geocode` da resposta de login (URL dinâmica, varia por região — **nunca** hardcodar)
- `{host_api}` → host do `base_url` (ex.: `hst-api.wialon.us`) — vai **dentro do path**
- `uid` → `login["user"]["id"]`

**Resposta:** array de strings na mesma ordem das coords; string vazia = ponto
sem endereço (ex.: meio do oceano) → tratamos como `None` → vira `N/D`.

```json
["Rua Volta Redonda 204, Pavuna, Rio De Janeiro, RJ 21530-200, Brazil", ""]
```

---

## GET × POST (limite de tamanho)

- **GET** coloca `coords` na URL → estoura em **~150 pontos** (HTTP 414 Request-URI
  Too Large).
- **POST** (params no corpo) aceita **milhares** numa tacada. **Usamos POST.**
- Lote de `GEOCODE_BATCH_SIZE = 1000` coords por requisição (folgado e rápido).

---

## Como está implementado

**`WialonClient`** (`src/clients/wialon_client.py`)
- No `authenticate()`: captura `self.uid` (de `login["user"]["id"]`) e monta
  `self.gis_geocode_url = {gis_geocode}/{host_api}/gis_geocode`.
- `get_addresses_batch(coords) -> List[Optional[str]]`: POST em lotes; degrada com
  elegância (sem `uid`/URL, ou erro de rede/API → `None` nas posições afetadas).

**`VehicleService`** (`src/services/vehicle_service.py`)
- `_fill_addresses(records)` (opt-in via `include_addresses`): deduplica as
  coordenadas arredondando a `ADDRESS_COORD_PRECISION = 4` casas (~11 m), consulta
  só as novas e mantém um **cache compartilhado no export** (`_address_cache`). A
  frota repete muito depósito/rota, então o cache poupa a maior parte das chamadas.
- Exemplo real: 5.749 registros → 1.019 coords únicas (~82% de economia), ~8 s.

**Export**
- Coluna já existente ("Localização"); `address` está em `OPTIONAL_SENSOR_COLS`, então
  `None` vira `N/D` automaticamente.
- Ativação: checkbox **"Incluir endereço (mais lento)"** na GUI, ou `--addresses`/`-A`
  no CLI.

---

## Flags de formato de endereço

| Flag | Formato |
|------|---------|
| `1255211008` | Rua, número, cidade, região, país (completo) — **usado** |
| `1073741824` | Rua apenas |

---

## Referências

- Exemplo oficial do SDK: https://sdk.wialon.com/wiki/en/sidebar/remoteapi/codesamples/address_coords
- Sonda de diagnóstico: `scripts/probe_geocode.py` (revalida a receita com token real)
