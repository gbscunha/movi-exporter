# Plano de Implementação — Nome do Motorista (RFID)

> **Origem:** pedido do cliente — coluna "Motorista" sai sempre vazia hoje.
> **Ciclo:** `.claude/skills/xp-cycle.md`
> **Branch:** `feat/motorista-rfid`
> **Regra:** cada fase é autônoma — não quebra o app se parar aqui. Commit ao final de cada fase.

---

## Tabela de acompanhamento

| # | Fase | TDD | Esforço | Status |
|---|------|-----|---------|--------|
| 00 | Validação do formato `rfid_tag` com dado real | — | S | ⬜ Todo |
| 01 | `wialon_client.list_drivers()` — mapa código→nome | 🟢 sim | S | ⬜ Todo |
| 02 | Resolver motorista por registro (transformer + forward-fill) | 🟢 sim | M | ⬜ Todo |
| 03 | Integração no pipeline + export | 🔴 parcial | S | ⬜ Todo |
| 04 | Docs (manual + GUIA) e verificação final | — | S | ⬜ Todo |

**Legenda status:** ⬜ Todo · 🔄 Em andamento · ✅ Concluído · ⏸️ Bloqueado
**Legenda TDD:** 🟢 sim · 🔴 parcial = só nos pontos com lógica testável · — = não aplicável

---

## Contexto

O cliente identifica motoristas por **cartão RFID**. Cada cartão tem um **Código** (ex.: `9310401`) vinculado a um **Nome** (ex.: "ALDO LOPES FURLEY E SILVA") na aba **Motoristas** do Wialon. A unidade tem um sensor **"Motorista"** do tipo *"Vinculação de motorista"* lendo o parâmetro **`rfid_tag`**.

**Como o dado chega na API:**
- Em cada mensagem, `params["rfid_tag"]` traz o **código** do cartão — não o nome.
- O nome vive na lista de motoristas do **Resource** (`drvrs`), onde cada motorista tem `c` (código) e `n` (nome).
- Logo: para preencher a coluna "Motorista" precisamos do mapa `código → nome` + casar com o `rfid_tag` de cada mensagem.

**Bug atual:** `wialon_transformer.py:141` faz `"driver": message.get("drv")`. O campo `drv` **não existe** na mensagem do `messages/load_interval` → coluna sempre vazia.

**Granularidade pedida:** nome do motorista **em cada linha/registro** (não um por veículo).

---

## Decisões e premissas

- **D1 — `rfid_tag` == "Código" do motorista?** Premissa: sim (a tela do Wialon resolve o nome corretamente). Risco: alguns leitores RFID reportam o número em decimal/hex diferente do "Código" digitado. **Bloqueia o início → Fase 00 valida com dado real antes de codar.**
- **D2 — Forward-fill por veículo.** O `rfid_tag` aparece só na mensagem em que o cartão é lido, mas o vínculo persiste até trocar. Para preencher **todas** as linhas, carregamos pra frente o último código visto por veículo — **mesmo padrão já usado** para `last_pwr_ext` e `last_ignition` em `vehicle_service.py:197-209`.
- **D3 — Sem cartão / código desconhecido → `N/D`** (convenção do projeto: nunca `NaN` nem string vazia visível ao cliente).
- **D4 — Resolução do código→nome acontece no momento do resolve** (transformer recebe o mapa pronto), e o **forward-fill é do nome já resolvido** — espelha `last_ignition` (valor final), sem inventar caminho novo.
- **D5 — Param `rfid_tag` hardcoded como chave primária**, com fallback configurável. É 1 cliente em produção; detectar via tipo de sensor ("Vinculação de motorista") é mais robusto porém o `sensor_map` atual não carrega o *tipo* do sensor (`wialon_client.py:299-317`). Decisão: ler `params.get("rfid_tag")` direto, com lista de chaves candidatas para facilitar futura generalização.

**Pré-requisito de ACL:** o token precisa ter permissão de **ver motoristas** no resource (`ADF_ACL_AVL_RES_VIEW_DRIVERS`). Se `list_drivers()` vier vazio/erro, é isso — ajustar no token. Validar na Fase 00.

---

## Fase 00 — Validação do formato `rfid_tag` com dado real

**Objetivo:** confirmar D1 (código == `rfid_tag`) e o pré-requisito de ACL **antes** de escrever código, evitando retrabalho.
**TDD:** — (investigação).

### Plano

- Rodar um export curto (1 veículo que tenha motorista vinculado, intervalo de 1 dia) com token real.
- Inspecionar `app.log` / `raw_data` das mensagens: confirmar que `params["rfid_tag"]` existe e qual o valor.
- Comparar o valor com o campo "Código" do motorista na tela do Wialon (ex.: `9310401`).
- Testar `core/search_items` em `avl_resource` com `flags = 1 + 256` e conferir se `item["drvrs"]` retorna os motoristas com `c` e `n` (valida ACL do token).

### Saída

- ✅ Confirmado: `rfid_tag` == `c` → segue o plano como está.
- ⚠️ Divergente (hex/decimal/CRC): ajustar a normalização do código na Fase 02 (ex.: `int()`, zero-pad, ou casar por outro campo). Documentar o de-para aqui.

---

## Fase 01 — `wialon_client.list_drivers()`

**Objetivo:** novo método que devolve o mapa `{código: nome}` de todos os motoristas dos resources da conta.
**TDD:** 🟢 sim — `requests-mock` com payload de `drvrs`, sem gastar quota real.

### Plano

**`src/clients/wialon_client.py`** ← NOVO método:

```python
def list_drivers(self) -> Dict[str, str]:
    """Mapa {código RFID: nome} de todos os motoristas dos resources.

    O código (`c`) casa com o param `rfid_tag` das mensagens. Usado para
    resolver o nome do motorista de cada registro no export.
    """
```

- `core/search_items` com `itemsType: "avl_resource"`, `flags: 1 + 256` (base + Drivers), `propName: "sys_name"`, paginação como em `list_vehicles`.
- Para cada resource, percorrer `item.get("drvrs", {})` → cada motorista tem `c` (código) e `n` (nome).
- Montar `{str(c): n}` ignorando códigos vazios. Logar `len(map)` em debug.
- Cache opcional na instância (`self._drivers_cache`) — a lista muda pouco e é reusada por todos os veículos no mesmo export.

### Testes — `tests/test_wialon_client.py`

- `test_list_drivers_monta_mapa_codigo_para_nome()` — payload com 2 resources, N motoristas → mapa correto.
- `test_list_drivers_ignora_codigo_vazio()` — motorista sem `c` não entra no mapa.
- `test_list_drivers_resource_sem_drivers_retorna_vazio()` — `drvrs` ausente não quebra.
- `test_list_drivers_pagina_resultados()` — se aplicável à paginação.

### Verificação

- `pytest -q` verde · `ruff check src/` limpo.
- Smoke com token real: `list_drivers()` retorna mapa não-vazio (valida ACL).

---

## Fase 02 — Resolver motorista por registro (transformer + forward-fill)

**Objetivo:** preencher `record["driver"]` com o **nome** do motorista em cada linha, com forward-fill por veículo.
**TDD:** 🟢 sim — transformer e forward-fill são lógica pura, fáceis de testar.

### Plano

**`src/services/wialon_transformer.py`:**

- `transform_message(...)` ganha um parâmetro novo `driver_map: Dict[str, str]` (default `{}` para não quebrar chamadas existentes).
- Trocar a linha 141:
  ```python
  "driver": message.get("drv"),                 # ❌ sempre vazio
  ```
  por:
  ```python
  "driver": self._resolve_driver(params, driver_map),
  ```
- Novo helper `_resolve_driver(params, driver_map)`:
  - Lê o código de `params` tentando, em ordem, as chaves candidatas (`DRIVER_PARAM_KEYS = ["rfid_tag"]`).
  - Normaliza o código (str; tratar `0`/vazio como "sem cartão" → `None`).
  - Retorna `driver_map.get(codigo)` (nome) ou `None` se não houver código/match. **`None` aqui**, não `"N/D"` — o "N/D" é responsabilidade da camada de export, como nos demais sensores.

**`src/services/vehicle_service.py` — `process_vehicle_history` (linha ~142):**

- Carregar `driver_map` uma vez (via `VehicleService`, ver Fase 03) e passar ao `transform_message`.
- Adicionar forward-fill **espelhando** o de `last_ignition` (linhas 207-209):
  ```python
  driver = transformed.get("driver")
  if driver is None:
      transformed["driver"] = last_driver
  else:
      last_driver = driver
  ```
  Inicializar `last_driver = None` no começo do loop do veículo.

### Testes

**`tests/test_wialon_transformer.py`:**
- `test_resolve_motorista_por_rfid_tag()` — `rfid_tag` no mapa → nome.
- `test_motorista_codigo_desconhecido_retorna_none()` — código fora do mapa → `None`.
- `test_motorista_sem_rfid_tag_retorna_none()` — sem o param → `None`.
- `test_mapa_de_motoristas_vazio_nao_quebra()` — `driver_map={}` → `None`.

**`tests/test_vehicle_service.py` (ou onde estiver o forward-fill):**
- `test_forward_fill_motorista_preenche_linhas_sem_tag()` — sequência [tap A, sem tag, sem tag, tap B] → [A, A, A, B].
- `test_forward_fill_motorista_reinicia_por_veiculo()` — não vaza motorista de um veículo para outro.

### Verificação

- `pytest -q` verde · `ruff check src/` limpo.

---

## Fase 03 — Integração no pipeline + export

**Objetivo:** ligar o `driver_map` ao fluxo de export e confirmar a coluna no arquivo gerado.
**TDD:** 🔴 parcial — fiação; o valor já é coberto pelas Fases 01-02.

### Plano

**`src/services/vehicle_service.py`:**
- Método/cache `get_drivers()` análogo a `get_vehicle_sensors` (`vehicle_service.py:127`) — chama `client.list_drivers()` uma vez e cacheia.
- Em `export_monthly_data` (linha ~274), carregar o mapa **uma vez** antes do loop de veículos (linha ~346) e repassar a `process_vehicle_history` → `transform_message`.
- Se `list_drivers()` falhar (ACL/erro), logar warning e seguir com mapa vazio — export **não pode** quebrar por causa do motorista (degradação graciosa → coluna vira `N/D`).

**`src/services/exporter.py`:**
- Confirmar que a coluna "Motorista" (`exporter.py:92`) e o campo `record.get("driver")` (linhas 412/509/608/710) já aplicam `N/D` quando `None`. Ajustar só se necessário.

### Verificação (CLAUDE.md)

1. `pytest -q` — todos verdes.
2. `ruff check src/` — zero erros.
3. GUI abre, roda um export real e a coluna **Motorista** aparece preenchida com nomes.
4. **Abrir o arquivo gerado** (CSV/Excel) e conferir: linhas do "tap" e as seguintes (forward-fill) com o nome certo; linhas sem cartão = `N/D`.
5. Como mexeu em `wialon_client.py`: testar com token real e conferir `app.log`.

---

## Fase 04 — Docs e verificação final

**Objetivo:** refletir a feature na documentação do cliente e dev.
**TDD:** —

### Plano

- **`docs/cliente/GUIA_CONFIGURACAO.md`** — nota curta: a coluna Motorista depende de o token ter permissão de ver motoristas e de os cartões estarem com "Código" preenchido.
- **`docs/cliente/USER_GUIDE.md`** / manual HTML embarcado — mencionar a coluna Motorista no export.
- **`CLAUDE.md` (regras Wialon)** — adicionar:
  - `rfid_tag` = código do cartão RFID → casar com `c` (Código) do motorista no resource (`drvrs`).
  - Lista de motoristas vem de `core/search_items` em `avl_resource` com flag `256` (Drivers).
  - Motorista usa forward-fill por veículo (vínculo persiste entre mensagens).
- Atualizar status deste plano.

---

## Fora de escopo

- **Múltiplos motoristas por mensagem** (sensor de vinculação múltipla) — o cliente usa 1 cartão por vez.
- **Suporte a vínculo manual** (`get_driver_bindings`) — só seria necessário se o cliente parasse de usar RFID.
- **Coluna de código do cartão** separada do nome — só nome por enquanto; adicionar depois se pedido.
- **Botão "Desconectar/Trocar conta" do Drive** — feature separada já discutida, não relacionada.
