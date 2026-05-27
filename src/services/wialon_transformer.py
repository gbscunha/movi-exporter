"""
Transformador de mensagens Wialon para formato intermediário.

Esta classe isola toda a lógica específica de transformação de dados
da API Wialon, seguindo o Princípio da Responsabilidade Única (SRP).

O Strategy Pattern é usado para resolver valores de sensores,
permitindo adicionar novos tipos de sensores sem modificar a lógica
principal (Open/Closed Principle - OCP).
"""

from typing import Any, Callable, Dict, Optional

from src.clients.protocols import TrackingClient


# Tipo para handlers de sensores: (raw_value, calculated_value) -> resolved_value
SensorHandler = Callable[[Any, Optional[float]], Any]


class WialonTransformer:
    """
    Transforma mensagens brutas da Wialon para formato intermediário.

    Responsabilidades:
    - Extrair dados de posição das mensagens
    - Resolver valores de sensores via sensor_map e fórmulas
    - Buscar parâmetros conhecidos como fallback
    - Montar dicionário transformado com campos padronizados
    """

    # Parâmetros conhecidos para busca direta nas mensagens
    # Mapeamento: campo normalizado -> lista de parâmetros possíveis na API
    KNOWN_PARAMS: Dict[str, list[str]] = {
        "ignition": ["in", "in1", "din1", "ignition", "ign"],
        "fuel_level": ["fuel1", "fuel2", "fuel_level", "can_fuel_level", "fuel", "fls"],
        "rpm": ["rpm", "can_rpm", "engine_rpm", "eng_rpm"],
        "battery_voltage": [
            "pwr_ext",
            "pwr_int",
            "voltage",
            "battery",
            "power",
            "batt",
        ],
        "engine_hours": ["engine_hours", "eng_hours", "horimeter", "eh", "mh"],
    }

    # Strategy Pattern: handlers para cada tipo de sensor
    # Cada handler recebe (raw_value, calculated_value) e retorna o valor resolvido
    SENSOR_HANDLERS: Dict[str, SensorHandler] = {
        "ignition": lambda v, _: bool(v) if v is not None else None,
        "fuel_level": lambda v, calc: calc if calc is not None else v,
        "rpm": lambda v, calc: calc if calc is not None else v,
        "battery_voltage": lambda v, calc: calc if calc is not None else v,
        "engine_hours": lambda v, calc: calc if calc is not None else v,
    }

    # Campos de sensores que o transformer suporta
    SENSOR_FIELDS = ["ignition", "fuel_level", "rpm", "battery_voltage", "engine_hours"]

    def __init__(self, client: TrackingClient):
        """
        Inicializa o transformer.

        Args:
            client: Cliente de rastreamento para aplicar fórmulas de sensores
        """
        self.client = client

    def transform_message(
        self,
        message: Dict[str, Any],
        vehicle_id: int,
        sensor_map: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Transforma mensagem bruta da Wialon para formato intermediário.

        Esta é a única função que conhece a estrutura da Wialon.
        O resultado é um dicionário com campos padronizados.

        Busca dados de duas formas:
        1. Via sensor_map (sensores configurados no Wialon, com fórmulas)
        2. Via KNOWN_PARAMS (parâmetros conhecidos diretamente nas mensagens)

        Args:
            message: Mensagem bruta da API Wialon
            vehicle_id: ID do veículo
            sensor_map: Mapa de sensores do veículo
                        Formato: {param_base: {"name": str, "formula": str}}

        Returns:
            Dicionário com dados transformados
        """
        # Extrai posição
        pos = message.get("pos", {}) or {}

        # Extrai parâmetros (dados de sensores)
        params = message.get("p", {}) or {}

        # Resolve sensores via sensor_map (com fórmulas)
        sensor_values = self._resolve_sensors_from_map(params, sensor_map)

        # Aplica fallback de parâmetros conhecidos para valores não resolvidos
        sensor_values = self._apply_param_fallbacks(params, sensor_values)

        # Odômetro vem em metros; converter para km.
        odometer_m = (
            params.get("odometer")
            or params.get("new_mileage")
            or params.get("mileage")
        )
        odometer_km = round(odometer_m / 1000, 2) if odometer_m else None

        # Monta registro transformado
        transformed = {
            "vehicle_id": vehicle_id,
            "timestamp": message.get("t"),  # Unix timestamp
            "latitude": pos.get("y"),
            "longitude": pos.get("x"),
            "speed": pos.get("s") or pos.get("sp"),  # Velocidade
            "odometer": odometer_km,
            "ignition": sensor_values.get("ignition"),
            "fuel_level": sensor_values.get("fuel_level"),
            "rpm": sensor_values.get("rpm"),
            "battery_voltage": sensor_values.get("battery_voltage"),
            "engine_hours": sensor_values.get("engine_hours"),
            "driver": message.get("drv"),  # Motorista vinculado
            "address": None,  # Requer geocodificação reversa (não implementado)
            "raw_data": message,  # Preserva dados originais
        }

        return transformed

    def _resolve_sensors_from_map(
        self,
        params: Dict[str, Any],
        sensor_map: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Resolve valores de sensores usando o sensor_map.

        Args:
            params: Parâmetros da mensagem Wialon
            sensor_map: Mapa de sensores do veículo

        Returns:
            Dicionário com valores resolvidos por nome de sensor
        """
        sensor_values: Dict[str, Any] = {field: None for field in self.SENSOR_FIELDS}

        for param_key, param_value in params.items():
            sensor_info = sensor_map.get(param_key)

            if not sensor_info:
                continue

            sensor_name = sensor_info.get("name", "")
            formula = sensor_info.get("formula", "")

            # Aplica a fórmula do sensor ao valor bruto
            calculated_value = self.client.apply_sensor_formula(param_value, formula)

            # Usa o handler apropriado para resolver o valor
            resolved = self._resolve_sensor_value(sensor_name, param_value, calculated_value)

            if resolved is not None and sensor_name in sensor_values:
                sensor_values[sensor_name] = resolved

        return sensor_values

    def _resolve_sensor_value(
        self,
        sensor_name: str,
        raw_value: Any,
        calculated: Optional[float],
    ) -> Any:
        """
        Resolve o valor de um sensor usando o handler apropriado (Strategy Pattern).

        Args:
            sensor_name: Nome do sensor (ex: "ignition", "fuel_level")
            raw_value: Valor bruto do parâmetro
            calculated: Valor calculado após aplicar fórmula (ou None)

        Returns:
            Valor resolvido pelo handler, ou fallback para calculated/raw_value
        """
        handler = self.SENSOR_HANDLERS.get(sensor_name)

        if handler:
            return handler(raw_value, calculated)

        # Fallback para sensores não mapeados
        return calculated if calculated is not None else raw_value

    def _apply_param_fallbacks(
        self,
        params: Dict[str, Any],
        sensor_values: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Aplica fallback de parâmetros conhecidos para valores não resolvidos.

        Args:
            params: Parâmetros da mensagem Wialon
            sensor_values: Valores já resolvidos via sensor_map

        Returns:
            Dicionário com valores atualizados incluindo fallbacks
        """
        for field in self.SENSOR_FIELDS:
            if sensor_values.get(field) is not None:
                continue

            # Determina o converter baseado no tipo de sensor
            converter = bool if field == "ignition" else None

            sensor_values[field] = self._get_param_fallback(params, field, converter)

        return sensor_values

    def _get_param_fallback(
        self,
        params: Dict[str, Any],
        param_type: str,
        converter: Optional[Callable] = None,
    ) -> Optional[Any]:
        """
        Busca valor de parâmetro como fallback quando não há sensor configurado.

        Args:
            params: Dicionário de parâmetros da mensagem
            param_type: Tipo de parâmetro (chave em KNOWN_PARAMS)
            converter: Função opcional para converter o valor (ex: bool)

        Returns:
            Valor encontrado ou None se não existir
        """
        for key in self.KNOWN_PARAMS.get(param_type, []):
            if key in params and params[key] is not None:
                value = params[key]
                return converter(value) if converter else value

        return None
