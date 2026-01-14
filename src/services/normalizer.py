from typing import Dict, List, Any
from datetime import datetime
from src.core.logger import logger


class DataNormalizer:
    """
    Classe responsável por normalizar dados de diferentes sistemas de rastreamento
    para um formato padronizado.

    Atualmente suporta System A, mas está preparada para expansão futura com
    múltiplos sistemas.
    """

    def __init__(self):
        """Inicializa o normalizador com mapeamentos de campos por sistema."""
        self.system_mappings = {
            "system_a": {
                "vehicle_id": "veiculoId",
                "vehicle_name": "nome",
                "plate": "placa",
                "timestamp": "dataHora",
                "latitude": "latitude",
                "longitude": "longitude",
                "speed": "velocidade",
                "odometer": "odometro",
                "ignition": "ignicao",
                "address": "endereco",
                "fuel_level": "nivelCombustivel",
                "rpm": "rpm",
                "battery_voltage": "voltagemBateria",
                "driver": "motorista",
            }
            # Preparado para adicionar system_b, system_c, etc. no futuro
        }

    def normalize_vehicle_list(
        self, raw_data: List[Dict[str, Any]], system: str = "system_a"
    ) -> List[Dict[str, Any]]:
        """
        Normaliza uma lista de veículos para o formato padronizado.

        Args:
            raw_data: Lista de veículos no formato original do sistema
            system: Identificador do sistema de origem (padrão: "system_a")

        Returns:
            Lista de veículos no formato normalizado
        """
        logger.info(f"Normalizando lista de {len(raw_data)} veículos do {system}")

        normalized_vehicles = []

        for vehicle in raw_data:
            try:
                normalized = self._normalize_vehicle(vehicle, system)
                normalized_vehicles.append(normalized)
            except Exception as e:
                logger.error(f"Erro ao normalizar veículo {vehicle}: {e}")
                continue

        logger.success(f"{len(normalized_vehicles)} veículos normalizados com sucesso")
        return normalized_vehicles

    def normalize_history(
        self, raw_data: List[Dict[str, Any]], system: str = "system_a"
    ) -> List[Dict[str, Any]]:
        """
        Normaliza dados históricos de um veículo para o formato padronizado.

        Args:
            raw_data: Lista de registros históricos no formato original do sistema
            system: Identificador do sistema de origem (padrão: "system_a")

        Returns:
            Lista de registros históricos no formato normalizado
        """
        logger.info(f"Normalizando {len(raw_data)} registros históricos do {system}")

        normalized_history = []

        for record in raw_data:
            try:
                normalized = self._normalize_history_record(record, system)
                normalized_history.append(normalized)
            except Exception as e:
                logger.error(f"Erro ao normalizar registro histórico {record}: {e}")
                continue

        logger.success(f"{len(normalized_history)} registros normalizados com sucesso")
        return normalized_history

    def _normalize_vehicle(
        self, vehicle: Dict[str, Any], system: str
    ) -> Dict[str, Any]:
        """
        Normaliza um único veículo para o formato padronizado.

        Args:
            vehicle: Dados do veículo no formato original
            system: Identificador do sistema de origem

        Returns:
            Veículo no formato normalizado
        """
        mapping = self.system_mappings.get(system)

        if not mapping:
            raise ValueError(f"Sistema '{system}' não suportado")

        # Formato padronizado de saída
        normalized = {
            "id": self._get_field(vehicle, mapping.get("vehicle_id", "id")),
            "name": self._get_field(vehicle, mapping.get("vehicle_name", "name")),
            "plate": self._get_field(vehicle, mapping.get("plate", "plate")),
            "system_source": system,
            "raw_data": vehicle,  # Mantém dados originais para referência
        }

        return normalized

    def _normalize_history_record(
        self, record: Dict[str, Any], system: str
    ) -> Dict[str, Any]:
        """
        Normaliza um único registro histórico para o formato padronizado.

        Args:
            record: Registro histórico no formato original
            system: Identificador do sistema de origem

        Returns:
            Registro no formato normalizado
        """
        mapping = self.system_mappings.get(system)

        if not mapping:
            raise ValueError(f"Sistema '{system}' não suportado")

        # Formato padronizado de saída
        normalized = {
            "vehicle_id": self._get_field(record, mapping.get("vehicle_id", "id")),
            "timestamp": self._normalize_timestamp(
                self._get_field(record, mapping.get("timestamp", "timestamp"))
            ),
            "latitude": self._get_field(
                record, mapping.get("latitude", "lat"), default=0.0
            ),
            "longitude": self._get_field(
                record, mapping.get("longitude", "lng"), default=0.0
            ),
            "speed": self._get_field(
                record, mapping.get("speed", "speed"), default=0.0
            ),
            "odometer": self._get_field(
                record, mapping.get("odometer", "odometer"), default=0.0
            ),
            "ignition": self._get_field(
                record, mapping.get("ignition", "ignition"), default=False
            ),
            "address": self._get_field(
                record, mapping.get("address", "address"), default=""
            ),
            "fuel_level": self._get_field(
                record, mapping.get("fuel_level", "fuel_level"), default=None
            ),
            "rpm": self._get_field(
                record, mapping.get("rpm", "rpm"), default=None
            ),
            "battery_voltage": self._get_field(
                record, mapping.get("battery_voltage", "battery_voltage"), default=None
            ),
            "driver": self._get_field(
                record, mapping.get("driver", "driver"), default=None
            ),
            "system_source": system,
            "raw_data": record,  # Mantém dados originais para referência
        }

        return normalized

    def _get_field(
        self, data: Dict[str, Any], field_path: str, default: Any = None
    ) -> Any:
        """
        Extrai um campo dos dados, suportando caminhos aninhados.

        Args:
            data: Dicionário de dados
            field_path: Caminho do campo (ex: "location.lat" ou "lat")
            default: Valor padrão se o campo não existir

        Returns:
            Valor do campo ou valor padrão
        """
        try:
            # Suporta campos aninhados como "location.lat"
            keys = field_path.split(".")
            value = data

            for key in keys:
                value = value[key]

            return value if value is not None else default
        except (KeyError, TypeError):
            return default

    def _normalize_timestamp(self, timestamp: Any) -> str:
        """
        Normaliza diferentes formatos de timestamp para ISO 8601.

        Args:
            timestamp: Timestamp em diversos formatos possíveis

        Returns:
            String no formato ISO 8601 (YYYY-MM-DDTHH:MM:SS)
        """
        if not timestamp:
            return datetime.now().isoformat()

        # Se já é string ISO, retorna
        if isinstance(timestamp, str):
            try:
                # Valida se é um formato válido
                datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                return timestamp
            except ValueError:
                pass

        # Se é timestamp Unix (int ou float)
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp).isoformat()

        # Se é objeto datetime
        if isinstance(timestamp, datetime):
            return timestamp.isoformat()

        # Fallback: retorna timestamp atual
        logger.warning(f"Formato de timestamp não reconhecido: {timestamp}")
        return datetime.now().isoformat()

    def add_system_mapping(self, system_name: str, mapping: Dict[str, str]) -> None:
        """
        Adiciona mapeamento para um novo sistema.

        Args:
            system_name: Nome identificador do sistema
            mapping: Dicionário com mapeamento de campos

        Example:
            normalizer.add_system_mapping("system_b", {
                "vehicle_id": "deviceId",
                "vehicle_name": "deviceName",
                "plate": "licensePlate",
                ...
            })
        """
        self.system_mappings[system_name] = mapping
        logger.info(f"Mapeamento adicionado para o sistema '{system_name}'")

    def get_supported_systems(self) -> List[str]:
        """
        Retorna lista de sistemas suportados.

        Returns:
            Lista com identificadores dos sistemas
        """
        return list(self.system_mappings.keys())
