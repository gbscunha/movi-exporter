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
import time
from typing import Any, Dict, List, Optional, Iterator
from datetime import datetime

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

    def __init__(self, token: Optional[str] = None):
        """
        Inicializa o cliente Wialon.

        Args:
            token: Token de acesso Wialon (usa settings.WIALON_TOKEN se não fornecido)
        """
        self.token = token or settings.WIALON_TOKEN
        self.sid: Optional[str] = None
        self.base_url: str = self.BASE_URL
        self._session = requests.Session()

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
                timeout=30,
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

            logger.success(f"Autenticação bem-sucedida. Session ID obtido.")
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
                timeout=60,
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

    def extract_profile_field(self, item: Dict[str, Any], field_name: str) -> Optional[str]:
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
            "flags": 8392713,  # 1 + 8 + 4096 + 8388608 (geral + custom fields + sensores + profile fields)
            "from": 0,
            "to": 0,  # 0 = todos os itens
        }

        data = self._request("core/search_items", params)

        # Extrai lista de items
        items = data.get("items", [])

        # Enriquece cada item com dados extraídos dos profile fields
        for item in items:
            item["_plate"] = self.extract_profile_field(item, "registration_plate")
            item["_brand"] = self.extract_profile_field(item, "brand")
            item["_model"] = self.extract_profile_field(item, "model")
            item["_vin"] = self.extract_profile_field(item, "vin")

        logger.success(f"{len(items)} veículos encontrados")

        return items

    def get_vehicle_sensors(self, vehicle_id: int) -> Dict[str, str]:
        """
        Obtém mapa de sensores de um veículo.

        A API Wialon retorna dados brutos (ex: io_23) que precisam ser
        mapeados para nomes legíveis (ex: fuel_level) através dos sensores.

        Args:
            vehicle_id: ID do veículo na Wialon

        Returns:
            Dicionário mapeando parâmetro bruto -> nome do sensor
            Exemplo: {"io_23": "fuel_level", "io_1": "ignition"}
        """
        logger.debug(f"Buscando sensores do veículo {vehicle_id}...")

        params = {"id": vehicle_id, "flags": 4096}  # Flag para obter sensores

        data = self._request("core/search_item", params)

        if not data or "item" not in data:
            logger.warning(f"Veículo {vehicle_id} não encontrado ou sem dados")
            return {}

        item = data["item"]
        sensors = item.get("sens", {})

        # Cria mapa de parâmetro -> nome do sensor
        sensor_map = {}
        for sensor_id, sensor_data in sensors.items():
            param = sensor_data.get("p", "")  # Parâmetro de origem (ex: io_23)
            name = sensor_data.get("n", "")  # Nome do sensor

            if param and name:
                # Normaliza nome do sensor para snake_case
                normalized_name = self._normalize_sensor_name(name)
                sensor_map[param] = normalized_name

        logger.debug(f"Veículo {vehicle_id}: {len(sensor_map)} sensores mapeados")

        return sensor_map

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

        # Mapeamentos conhecidos
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
            "voltagem": "battery_voltage",
            "bateria": "battery_voltage",
            "battery": "battery_voltage",
            "voltage": "battery_voltage",
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
                "flagsMask": 65281,
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

    def get_full_history(
        self, vehicle_id: int, time_from: int, time_to: int
    ) -> List[Dict[str, Any]]:
        """
        Busca histórico completo (conveniente para volumes menores).

        ATENÇÃO: Para grandes volumes, use get_history() com generator.

        Args:
            vehicle_id: ID do veículo
            time_from: Timestamp Unix início
            time_to: Timestamp Unix fim

        Returns:
            Lista completa de mensagens
        """
        all_messages = []
        for page in self.get_history(vehicle_id, time_from, time_to):
            all_messages.extend(page)
        return all_messages

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
