"""
Cliente para integração com a API Wialon Hosting.

A API Wialon é stateful e baseada em sessão (sid), NÃO usa Bearer Token.
Este cliente implementa:
- Autenticação via token com armazenamento de sessão
- Reautenticação automática em caso de sessão expirada
- Listagem de veículos (units)
- Resolução de sensores por veículo
- Busca de histórico com paginação
"""

import json
import re
from typing import Any, Dict, List, Optional, Iterator
from datetime import datetime
from urllib.parse import urlparse

import requests

from src.core.config import settings
from src.core.logger import logger


class WialonError(Exception):
    """Exceção base para erros da API Wialon."""

    def __init__(self, message: str, error_code: Optional[int] = None):
        self.error_code = error_code
        super().__init__(message)


class WialonAuthError(WialonError):
    """Erro de autenticação/sessão inválida."""

    pass


class WialonValidationError(WialonError):
    """Erro de validação de parâmetros (error=4)."""

    pass


class WialonClient:
    """
    Cliente para API Wialon Hosting.

    Gerencia sessão stateful com reautenticação automática.
    """

    BASE_URL = "https://hst-api.wialon.com/wialon/ajax.html"

    # Códigos de erro da API Wialon
    ERROR_INVALID_SESSION = 1
    ERROR_INVALID_PARAMS = 4

    # Configurações de paginação
    DEFAULT_PAGE_SIZE = 1000
    MAX_RETRIES = 3

    # Timeouts de requisição HTTP (segundos). Login é rápido; chamadas de dados
    # (search/messages) podem demorar mais com frotas grandes.
    AUTH_TIMEOUT = 30
    REQUEST_TIMEOUT = 60

    # Flags de busca da API Wialon (bitmask). O flag de dados de unidade combina
    # geral + custom fields + sensores + profile fields.
    UNIT_FLAG_GENERAL = 1
    UNIT_FLAG_CUSTOM_FIELDS = 8
    UNIT_FLAG_SENSORS = 4096
    UNIT_FLAG_PROFILE_FIELDS = 8388608
    UNIT_DATA_FLAGS = (
        UNIT_FLAG_GENERAL
        | UNIT_FLAG_CUSTOM_FIELDS
        | UNIT_FLAG_SENSORS
        | UNIT_FLAG_PROFILE_FIELDS
    )  # = 8392713

    # Flags de busca de resource (avl_resource). O de motoristas combina base
    # (geral) + Drivers, necessário para o campo `drvrs` vir preenchido.
    RESOURCE_FLAG_BASE = 1
    RESOURCE_FLAG_DRIVERS = 256
    RESOURCE_DRIVERS_FLAGS = RESOURCE_FLAG_BASE | RESOURCE_FLAG_DRIVERS  # = 257

    # Geocodificação (gis_geocode). Flag do formato de endereço completo:
    # rua, número, cidade, região, país. A chamada usa `uid` (id do usuário do
    # login) + sessão — NÃO gis_sid nem search_provider (ver GEOCODIFICACAO.md).
    GEOCODE_FLAGS = 1255211008
    # coords vão no corpo do POST — o GET estoura em ~150 (HTTP 414). Com POST
    # a API aceita milhares; 1000 é folgado e mantém a resposta rápida.
    GEOCODE_BATCH_SIZE = 1000

    def __init__(self, token: Optional[str] = None):
        """
        Inicializa o cliente Wialon.

        Args:
            token: Token de acesso Wialon (usa settings.WIALON_TOKEN se não fornecido)
        """
        self.token = token or settings.WIALON_TOKEN
        self.sid: Optional[str] = None
        self.gis_sid: Optional[str] = None
        self.gis_geocode_url: Optional[str] = None
        # ID do usuário (do login) — usado como credencial nas chamadas GIS.
        self.uid: Optional[int] = None
        self.username: str = ""
        self.base_url: str = self.BASE_URL
        self._session = requests.Session()
        # Cache do mapa {código RFID: nome}. A lista de motoristas muda pouco e
        # é reusada por todos os veículos no mesmo export.
        self._drivers_cache: Optional[Dict[str, str]] = None

        if not self.token:
            raise WialonError("Token Wialon não configurado")

        logger.info("WialonClient inicializado")

    def authenticate(self) -> Dict[str, Any]:
        """
        Realiza autenticação na API Wialon via token/login.

        Returns:
            Dados da resposta de login incluindo user info

        Raises:
            WialonAuthError: Se a autenticação falhar
        """
        logger.info("Iniciando autenticação Wialon...")

        params = {"token": self.token}

        try:
            response = self._session.get(
                self.BASE_URL,
                params={"svc": "token/login", "params": json.dumps(params)},
                timeout=self.AUTH_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()

            # Verifica erro na resposta
            if isinstance(data, dict) and "error" in data:
                error_code = data.get("error")
                raise WialonAuthError(
                    f"Falha na autenticação: error={error_code}", error_code=error_code
                )

            # Extrai session id (eid)
            self.sid = data.get("eid")

            if not self.sid:
                raise WialonAuthError("Resposta de login não contém session id (eid)")

            # Atualiza base_url se retornado (pode ser diferente por região)
            # Prioriza base_url (URL completa) sobre host (pode ser IP inacessível)
            if "base_url" in data:
                base = data["base_url"].rstrip("/")
                self.base_url = f"{base}/wialon/ajax.html"
            elif "host" in data:
                self.base_url = f"https://{data['host']}/wialon/ajax.html"

            # Salva sessão e URL de geocodificação para uso futuro.
            # URLs de GIS são dinâmicas — devem vir do login, nunca hardcoded.
            # A URL de geocode inclui o HOST da API no path:
            #   {gis_geocode}/{host_api}/gis_geocode
            # (formato do SDK oficial — sem esse segmento a chamada falha).
            self.gis_sid = data.get("gis_sid")
            gis_geocode = data.get("gis_geocode", "")
            if gis_geocode:
                api_host = urlparse(self.base_url).netloc
                self.gis_geocode_url = (
                    f"{gis_geocode.rstrip('/')}/{api_host}/gis_geocode"
                )

            # ID do usuário — credencial das chamadas GIS (campo `user.id`).
            user_obj = data.get("user")
            if isinstance(user_obj, dict):
                self.uid = user_obj.get("id")

            # Captura nome da conta — campo "au" pode vir como dict {"nm": "..."}
            # ou como string direto, dependendo da versão da API.
            user = data.get("au", {})
            if isinstance(user, dict):
                self.username = user.get("nm", "")
            elif isinstance(user, str):
                self.username = user

            logger.success("Autenticação bem-sucedida. Session ID obtido.")
            logger.debug(f"Base URL: {self.base_url}")

            return data

        except requests.RequestException as e:
            raise WialonAuthError(f"Erro de rede na autenticação: {e}")

    def _ensure_authenticated(self) -> None:
        """Garante que existe uma sessão ativa, autenticando se necessário."""
        if not self.sid:
            self.authenticate()

    def _request(self, svc: str, params: Dict[str, Any], retry_count: int = 0) -> Any:
        """
        Executa uma requisição à API Wialon.

        Args:
            svc: Nome do serviço (ex: "core/search_items")
            params: Parâmetros da requisição
            retry_count: Contador interno de retentativas

        Returns:
            Dados da resposta (JSON parsed)

        Raises:
            WialonError: Em caso de erro da API
            WialonAuthError: Se sessão expirar e reautenticação falhar
            WialonValidationError: Se parâmetros forem inválidos
        """
        self._ensure_authenticated()

        try:
            response = self._session.get(
                self.base_url,
                params={"svc": svc, "params": json.dumps(params), "sid": self.sid},
                timeout=self.REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()

            # Verifica erro na resposta
            if isinstance(data, dict) and "error" in data:
                error_code = data.get("error")

                # Sessão inválida - tenta reautenticar
                if error_code == self.ERROR_INVALID_SESSION:
                    if retry_count < self.MAX_RETRIES:
                        logger.warning("Sessão expirada, reautenticando...")
                        self.sid = None
                        self.authenticate()
                        return self._request(svc, params, retry_count + 1)
                    else:
                        raise WialonAuthError(
                            "Sessão expirada e máximo de retentativas excedido",
                            error_code=error_code,
                        )

                # Erro de validação de parâmetros
                if error_code == self.ERROR_INVALID_PARAMS:
                    raise WialonValidationError(
                        f"Parâmetros inválidos para {svc}: {params}",
                        error_code=error_code,
                    )

                # Outro erro
                raise WialonError(
                    f"Erro na API Wialon: error={error_code}", error_code=error_code
                )

            return data

        except requests.RequestException as e:
            raise WialonError(f"Erro de rede: {e}")

    def extract_profile_field(
        self, item: Dict[str, Any], field_name: str
    ) -> Optional[str]:
        """
        Extrai um campo específico dos profile fields de um item.

        Args:
            item: Item retornado pela API (veículo)
            field_name: Nome do campo (ex: "registration_plate")

        Returns:
            Valor do campo ou None se não encontrado
        """
        pflds = item.get("pflds", {})
        for field_data in pflds.values():
            if field_data.get("n") == field_name:
                return field_data.get("v")
        return None

    def _extract_plate(self, item: Dict[str, Any]) -> Optional[str]:
        """Placa do veículo: profile field, com fallback pro nome da unidade.

        Prioriza o profile field `registration_plate` (fonte oficial). Se ele
        vier vazio, usa o nome da unidade (`nm`) — nesta frota (Conta 1 e
        Conta 2) o nome da unidade na Wialon já É a placa; sem esse fallback,
        contas que não preenchem o profile field ficam com `N/D` e o arquivo
        exportado cai pro ID do veículo no nome em vez da placa.
        """
        plate = self.extract_profile_field(item, "registration_plate")
        if plate:
            return plate

        name = (item.get("nm") or "").strip()
        if name:
            logger.debug(
                f"Veículo {item.get('id')}: sem registration_plate — "
                f"usando nome da unidade '{name}' como placa (fallback)."
            )
            return name

        return None

    def list_vehicles(self) -> List[Dict[str, Any]]:
        """
        Lista todos os veículos (units) disponíveis.

        Returns:
            Lista de veículos com id, nome e outros atributos
        """
        logger.info("Buscando lista de veículos...")

        params = {
            "spec": {
                "itemsType": "avl_unit",
                "propName": "sys_name",
                "propValueMask": "*",
                "sortType": "sys_name",
            },
            "force": 1,
            "flags": self.UNIT_DATA_FLAGS,
            "from": 0,
            "to": 0,  # 0 = todos os itens
        }

        data = self._request("core/search_items", params)

        # Extrai lista de items
        items = data.get("items", [])

        # Enriquece cada item com dados extraídos dos profile fields
        for item in items:
            item["_plate"] = self._extract_plate(item)
            item["_brand"] = self.extract_profile_field(item, "brand")
            item["_model"] = self.extract_profile_field(item, "model")
            item["_vin"] = self.extract_profile_field(item, "vin")

        logger.success(f"{len(items)} veículos encontrados")

        return items

    def list_drivers(self) -> Dict[str, str]:
        """Mapa {código RFID: nome} de todos os motoristas dos resources.

        O código (`c`) casa com o param `rfid_tag` das mensagens. Usado para
        resolver o nome do motorista de cada registro no export.

        Requer que o token tenha ACL de ver motoristas no resource
        (`ADF_ACL_AVL_RES_VIEW_DRIVERS`); sem ela, `drvrs` vem vazio e o mapa
        resulta vazio (a coluna Motorista vira N/D no export).

        Resultado é cacheado na instância — a lista muda pouco e é reusada por
        todos os veículos no mesmo export.
        """
        if self._drivers_cache is not None:
            return self._drivers_cache

        logger.info("Buscando lista de motoristas (resources)...")

        params = {
            "spec": {
                "itemsType": "avl_resource",
                "propName": "sys_name",
                "propValueMask": "*",
                "sortType": "sys_name",
            },
            "force": 1,
            "flags": self.RESOURCE_DRIVERS_FLAGS,
            "from": 0,
            "to": 0,  # 0 = todos os resources
        }

        data = self._request("core/search_items", params)
        items = data.get("items", []) or []

        drivers: Dict[str, str] = {}
        for resource in items:
            # `drvrs` normalmente é um dict {id: {c, n, ...}}; alguns retornos
            # trazem lista. Tratamos ambos para não depender da forma.
            drvrs = resource.get("drvrs") or {}
            driver_entries = drvrs.values() if isinstance(drvrs, dict) else drvrs
            for driver in driver_entries:
                code = str(driver.get("c", "") or "").strip()
                name = driver.get("n")
                if code and name:
                    drivers[code] = name

        logger.debug(f"{len(drivers)} motoristas mapeados")

        self._drivers_cache = drivers
        return drivers

    def get_addresses_batch(
        self, coordinates: List[Dict[str, float]]
    ) -> List[Optional[str]]:
        """Geocodificação reversa: converte coordenadas em endereços.

        Recebe uma lista `[{"lon": float, "lat": float}, ...]` e devolve uma
        lista de mesmo tamanho e ordem com o endereço de cada ponto (ou `None`
        quando não há endereço / a chamada falha).

        Usa POST (o GET estoura o limite de URL em ~150 pontos) contra
        `{gis_geocode}/{host_api}/gis_geocode`, autenticando por `uid` + sessão.
        As coordenadas são processadas em lotes de `GEOCODE_BATCH_SIZE`.

        Degrada com elegância: sem `gis_geocode_url`/`uid`, ou em erro de rede/
        API, retorna `None` nas posições afetadas — o export nunca quebra por
        causa do endereço (a coluna vira N/D).
        """
        if not coordinates:
            return []

        if not self.gis_geocode_url or not self.uid:
            logger.warning(
                "Geocodificação indisponível (sem gis_geocode_url/uid) — "
                "endereços virão como N/D."
            )
            return [None] * len(coordinates)

        results: List[Optional[str]] = []
        for start in range(0, len(coordinates), self.GEOCODE_BATCH_SIZE):
            chunk = coordinates[start : start + self.GEOCODE_BATCH_SIZE]
            results.extend(self._geocode_chunk(chunk))
        return results

    def _geocode_chunk(self, chunk: List[Dict[str, float]]) -> List[Optional[str]]:
        """Geocodifica um único lote via POST. Retorna None por item em falha."""
        coords = [{"lon": c["lon"], "lat": c["lat"]} for c in chunk]
        try:
            response = self._session.post(
                self.gis_geocode_url,
                data={
                    "coords": json.dumps(coords),
                    "flags": self.GEOCODE_FLAGS,
                    "uid": self.uid,
                },
                timeout=self.REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and "error" in data:
                logger.warning(f"Geocodificação retornou error={data.get('error')}")
                return [None] * len(chunk)

            if not isinstance(data, list):
                logger.warning(f"Geocodificação: resposta inesperada ({type(data)})")
                return [None] * len(chunk)

            # Normaliza tamanho e converte strings vazias em None.
            out: List[Optional[str]] = [addr or None for addr in data]
            if len(out) != len(chunk):
                logger.warning(
                    f"Geocodificação: {len(out)} endereços para {len(chunk)} coords"
                )
                out = (out + [None] * len(chunk))[: len(chunk)]
            return out

        except (requests.RequestException, ValueError) as e:
            logger.warning(f"Erro na geocodificação: {e}")
            return [None] * len(chunk)

    def get_vehicle_sensors(self, vehicle_id: int) -> Dict[str, Dict[str, Any]]:
        """
        Obtém mapa de sensores de um veículo.

        A API Wialon retorna dados brutos (ex: io_23) que precisam ser
        mapeados para nomes legíveis (ex: fuel_level) através dos sensores.
        Sensores podem ter fórmulas (ex: io_2_94*const0.25) que são parseadas.

        Args:
            vehicle_id: ID do veículo na Wialon

        Returns:
            Dicionário mapeando parâmetro base -> info do sensor
            Exemplo: {"io_2_94": {"name": "rpm", "formula": "io_2_94*const0.25"}}
        """
        logger.debug(f"Buscando sensores do veículo {vehicle_id}...")

        params = {"id": vehicle_id, "flags": self.UNIT_FLAG_SENSORS}

        data = self._request("core/search_item", params)

        if not data or "item" not in data:
            logger.warning(f"Veículo {vehicle_id} não encontrado ou sem dados")
            return {}

        item = data["item"]
        sensors = item.get("sens", {})

        # Cria mapa de parâmetro base -> info do sensor
        sensor_map = {}
        for sensor_id, sensor_data in sensors.items():
            formula = sensor_data.get(
                "p", ""
            )  # Fórmula completa (ex: io_2_94*const0.25)
            name = sensor_data.get("n", "")  # Nome do sensor

            if formula and name:
                # Normaliza nome do sensor para snake_case
                normalized_name = self._normalize_sensor_name(name)

                # Extrai parâmetro base da fórmula
                base_param = self._extract_base_param(formula)

                if base_param:
                    sensor_map[base_param] = {
                        "name": normalized_name,
                        "formula": formula,
                    }

        logger.debug(f"Veículo {vehicle_id}: {len(sensor_map)} sensores mapeados")

        return sensor_map

    def _extract_base_param(self, formula: str) -> Optional[str]:
        """
        Extrai o parâmetro base de uma fórmula de sensor Wialon.

        Exemplos:
        - "io_2_94*const0.25" -> "io_2_94"
        - "can_rpm/const8" -> "can_rpm"
        - "fuel_lvl*const55/const255" -> "fuel_lvl"
        - "io_1_409" -> "io_1_409"

        Args:
            formula: Fórmula do sensor (campo "p")

        Returns:
            Parâmetro base ou None se não conseguir extrair
        """
        if not formula:
            return None

        # Remove espaços
        formula = formula.strip()

        # Encontra o primeiro operador (*,/,+,-)
        operators = ["*", "/", "+", "-"]
        min_pos = len(formula)

        for op in operators:
            pos = formula.find(op)
            if pos != -1 and pos < min_pos:
                min_pos = pos

        # Se encontrou operador, pega o que vem antes
        if min_pos < len(formula):
            return formula[:min_pos].strip()

        # Se não tem operador, a fórmula é só o parâmetro
        return formula

    def apply_sensor_formula(self, raw_value: Any, formula: str) -> Optional[float]:
        """
        Aplica a fórmula de um sensor Wialon ao valor bruto.

        Exemplos de fórmulas suportadas:
        - "io_2_94*const0.25" -> raw_value * 0.25
        - "can_rpm/const8" -> raw_value / 8
        - "fuel_lvl*const55/const255" -> raw_value * 55 / 255
        - "power*const0.001" -> raw_value * 0.001

        Args:
            raw_value: Valor bruto do parâmetro
            formula: Fórmula do sensor

        Returns:
            Valor calculado ou None se falhar
        """
        if raw_value is None:
            return None

        try:
            result = float(raw_value)

            # Encontra todas as operações const (ex: *const0.25, /const8)
            operations = re.findall(r"([*/+-])const([\d.]+)", formula)

            for op, const_str in operations:
                const_value = float(const_str)

                if op == "*":
                    result = result * const_value
                elif op == "/":
                    if const_value != 0:
                        result = result / const_value
                elif op == "+":
                    result = result + const_value
                elif op == "-":
                    result = result - const_value

            return result

        except (ValueError, TypeError) as e:
            logger.debug(
                f"Erro ao aplicar fórmula '{formula}' ao valor '{raw_value}': {e}"
            )
            return None

    def _normalize_sensor_name(self, name: str) -> str:
        """
        Normaliza nome de sensor para identificador padronizado.

        Tenta mapear nomes comuns para campos padrão:
        - Ignição, Ignicao -> ignition
        - Combustível, Fuel -> fuel_level
        - RPM -> rpm
        - Voltagem, Bateria -> battery_voltage
        - Horas Motor -> engine_hours
        """
        name_lower = name.lower()

        # Bateria/tensão é decidida por PALAVRA-CHAVE (não frase exata), porque
        # os admins variam muito a nomenclatura: "Bateria do dispositivo",
        # "Bateria dispositivo", "Bateria interna"... Se houver qualquer pista
        # de "interno/dispositivo/rastreador", é a bateria do tracker (~4V);
        # caso contrário, assume tensão do veículo (~12-28V).
        battery_terms = (
            "bateria",
            "battery",
            "voltagem",
            "voltage",
            "tensão",
            "tensao",
        )
        if any(t in name_lower for t in battery_terms):
            internal_hints = (
                "interna",
                "interno",
                "dispositivo",
                "rastreador",
                "device",
                "tracker",
                "backup",
            )
            if any(h in name_lower for h in internal_hints):
                return "internal_battery_voltage"
            return "vehicle_voltage"

        # Demais sensores — match por substring, do mais específico ao genérico.
        mappings = {
            "ignicao": "ignition",
            "ignição": "ignition",
            "ignition": "ignition",
            "combustivel": "fuel_level",
            "combustível": "fuel_level",
            "fuel": "fuel_level",
            "nivel combustivel": "fuel_level",
            "rpm": "rpm",
            "rotacao": "rpm",
            "horas motor": "engine_hours",
            "engine hours": "engine_hours",
            "horimetro": "engine_hours",
            "horímetro": "engine_hours",
        }

        for key, value in mappings.items():
            if key in name_lower:
                return value

        # Se não encontrou, retorna nome original em snake_case
        return name.lower().replace(" ", "_").replace("-", "_")

    def get_history(
        self,
        vehicle_id: int,
        time_from: int,
        time_to: int,
        page_size: int = DEFAULT_PAGE_SIZE,
    ) -> Iterator[List[Dict[str, Any]]]:
        """
        Busca histórico de mensagens de um veículo em páginas.

        Retorna um generator para evitar carregar todo o mês em memória.

        Args:
            vehicle_id: ID do veículo
            time_from: Timestamp Unix início
            time_to: Timestamp Unix fim
            page_size: Quantidade de mensagens por página

        Yields:
            Páginas de mensagens (lista de dicts)
        """
        logger.info(
            f"Buscando histórico do veículo {vehicle_id} "
            f"de {datetime.fromtimestamp(time_from)} "
            f"a {datetime.fromtimestamp(time_to)}"
        )

        # Variáveis de paginação
        last_time = time_from
        last_count = 0
        total_messages = 0
        page_num = 0

        while True:
            page_num += 1

            params = {
                "itemId": vehicle_id,
                "timeFrom": last_time,
                "timeTo": time_to,
                "flags": 1,  # Mensagens com posição
                "flagsMask": 0,  # captura todos os tipos de mensagem (inclui data-only com pwr_ext)
                "loadCount": page_size,
            }

            # Adiciona parâmetros de paginação após primeira página
            if last_count > 0:
                params["lastTime"] = last_time
                params["lastCount"] = last_count

            logger.debug(f"Veículo {vehicle_id} - Página {page_num}, desde {last_time}")

            data = self._request("messages/load_interval", params)

            messages = data.get("messages", [])

            if not messages:
                logger.debug(f"Veículo {vehicle_id} - Sem mais mensagens")
                break

            total_messages += len(messages)

            # Atualiza cursores de paginação
            last_message = messages[-1]
            new_last_time = last_message.get("t", last_time)

            # Conta mensagens com mesmo timestamp para lastCount
            same_time_count = sum(1 for m in messages if m.get("t") == new_last_time)

            # Detecta fim da paginação
            if new_last_time == last_time and len(messages) < page_size:
                yield messages
                break

            last_time = new_last_time
            last_count = same_time_count

            yield messages

            # Se recebemos menos que o page_size, terminamos
            if len(messages) < page_size:
                break

        logger.success(
            f"Veículo {vehicle_id}: {total_messages} mensagens em {page_num} páginas"
        )

    def logout(self) -> bool:
        """
        Encerra a sessão Wialon.

        Returns:
            True se logout bem-sucedido
        """
        if not self.sid:
            return True

        try:
            self._request("core/logout", {})
            self.sid = None
            logger.info("Logout Wialon realizado")
            return True
        except WialonError:
            self.sid = None
            return False

    def __enter__(self):
        """Suporte a context manager."""
        self.authenticate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Encerra sessão ao sair do context manager."""
        self.logout()
        return False
