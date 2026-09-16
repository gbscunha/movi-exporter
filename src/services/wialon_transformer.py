"""
Transformador de mensagens Wialon para formato intermediário.

Esta classe isola toda a lógica específica de transformação de dados
da API Wialon, seguindo o Princípio da Responsabilidade Única (SRP).

Estratégia em duas camadas:
- **Sensor map** — sensores que o admin configurou no Wialon (com fórmula).
  Caminho preferencial: o admin sabe melhor que param representa o quê.
- **Tracker profiles** — fallback quando o sensor map não cobre. O perfil
  certo é detectado por mensagem (model/rep_type) e fornece os nomes de
  params nativos do fabricante. Adicionar suporte a tracker novo = criar
  arquivo em `src/services/tracker_profiles/` sem mexer aqui.
"""

from typing import Any, Callable, Dict, List, Optional

from src.clients.protocols import TrackingClient
from src.services.tracker_profiles import (
    DEFAULT_PROFILES,
    TrackerProfile,
    detect_profile,
)


# Tipo para handlers de sensores: (raw_value, calculated_value) -> resolved_value
SensorHandler = Callable[[Any, Optional[float]], Any]


class WialonTransformer:
    """Transforma mensagens brutas da Wialon para formato intermediário.

    Esta é a única classe que conhece a estrutura "raw" da Wialon. Sai daqui
    um dict com chaves estáveis usadas pelo resto da pipeline.
    """

    # Strategy Pattern: handlers para cada tipo de sensor.
    # Cada handler recebe (raw_value, calculated_value) e retorna o valor resolvido.
    SENSOR_HANDLERS: Dict[str, SensorHandler] = {
        "ignition": lambda v, _: bool(v) if v is not None else None,
        "fuel_level": lambda v, calc: calc if calc is not None else v,
        "rpm": lambda v, calc: calc if calc is not None else v,
        "vehicle_voltage": lambda v, calc: calc if calc is not None else v,
        "internal_battery_voltage": lambda v, calc: calc if calc is not None else v,
        "engine_hours": lambda v, calc: calc if calc is not None else v,
    }

    # Campos de sensores que o transformer suporta
    SENSOR_FIELDS = [
        "ignition",
        "fuel_level",
        "rpm",
        "vehicle_voltage",
        "internal_battery_voltage",
        "engine_hours",
    ]

    # Params que carregam o código do cartão RFID do motorista, em ordem de
    # preferência. Hoje só `rfid_tag`; a lista facilita generalizar depois sem
    # mexer na lógica (ver D5 do PLANO_MOTORISTA_RFID.md).
    DRIVER_PARAM_KEYS = ["rfid_tag"]

    def __init__(
        self,
        client: TrackingClient,
        profiles: Optional[List[TrackerProfile]] = None,
    ):
        """Inicializa o transformer.

        Args:
            client: Cliente de rastreamento para aplicar fórmulas de sensores
            profiles: Lista de perfis de tracker. Default = registro global
                      (Suntech + DefaultProfile). Permitir override é útil
                      em testes e em pipelines com clientes especiais.
        """
        self.client = client
        self.profiles = profiles or DEFAULT_PROFILES

    def transform_message(
        self,
        message: Dict[str, Any],
        vehicle_id: int,
        sensor_map: Dict[str, Dict[str, Any]],
        driver_map: Optional[Dict[str, str]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Transforma mensagem bruta da Wialon para formato intermediário.

        Busca dados em ordem de prioridade:
        1. Via `sensor_map` (sensores configurados pelo admin no Wialon, com
           fórmulas). Caminho preferencial.
        2. Via perfil de tracker detectado (Suntech, default, ...) — usado
           quando o admin não configurou sensor pra aquele campo.

        Args:
            message: Mensagem bruta da API Wialon
            vehicle_id: ID do veículo
            sensor_map: Mapa de sensores do veículo
                        Formato: {param_base: {"name": str, "formula": str}}
            driver_map: Mapa {código RFID: nome} para resolver o motorista da
                        mensagem (de `WialonClient.list_drivers`). Default vazio
                        (motorista fica None) para não quebrar chamadas antigas.

        Returns:
            Dicionário com dados transformados, ou `None` se a mensagem
            for data-only (sem GPS).
        """
        # Extrai posição — mensagens data-only (sem GPS) não viram linha no export.
        pos = message.get("pos") or {}
        if not pos:
            return None

        # Detecta o perfil de tracker (uma vez por mensagem).
        profile = detect_profile(message, self.profiles)

        # Extrai parâmetros (dados de sensores)
        params = message.get("p", {}) or {}

        # Resolve sensores via sensor_map (com fórmulas)
        sensor_values = self._resolve_sensors_from_map(params, sensor_map)

        # Aplica fallback de parâmetros conhecidos para valores não resolvidos
        sensor_values = self._apply_param_fallbacks(params, sensor_values, profile)

        # Ignição por EVENTO: algumas mensagens não trazem o sinal contínuo de
        # ignição (`in`/`mode`), só o evento de transição (ex.: Suntech ALT
        # alert_id 33=liga/34=desliga). O perfil traduz o evento em on/off.
        if sensor_values.get("ignition") is None:
            resolver = getattr(profile, "resolve_ignition_event", None)
            if resolver is not None:
                sensor_values["ignition"] = resolver(params)

        # Odômetro vem em metros; converter para km.
        odometer_m = profile.extract_odometer_meters(params)
        odometer_km = round(odometer_m / 1000, 2) if odometer_m is not None else None

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
            "vehicle_voltage": sensor_values.get("vehicle_voltage"),
            "internal_battery_voltage": sensor_values.get("internal_battery_voltage"),
            "engine_hours": sensor_values.get("engine_hours"),
            "driver": self._resolve_driver(params, driver_map),
            "address": None,  # Requer geocodificação reversa (não implementado)
            "raw_data": message,  # Preserva dados originais
        }

        return transformed

    def _resolve_driver(
        self,
        params: Dict[str, Any],
        driver_map: Optional[Dict[str, str]],
    ) -> Optional[str]:
        """Resolve o nome do motorista a partir do código RFID da mensagem.

        Lê o código das chaves candidatas (`DRIVER_PARAM_KEYS`) e casa com o
        mapa {código: nome}. Retorna `None` (não `"N/D"`) quando não há cartão
        ou o código é desconhecido — o `N/D` é responsabilidade da camada de
        export, como nos demais sensores.
        """
        if not driver_map:
            return None

        for key in self.DRIVER_PARAM_KEYS:
            raw = params.get(key)
            # `0`/""/None = sem cartão lido nesta mensagem.
            if raw in (None, "", 0, "0"):
                continue
            code = str(raw).strip()
            # Ponto único de ajuste se a Fase 00 mostrar que o `rfid_tag` chega
            # em formato diferente do "Código" (ex.: hex/decimal): normalizar
            # `code` aqui antes do lookup.
            name = driver_map.get(code)
            if name:
                return name

        return None

    def _resolve_sensors_from_map(
        self,
        params: Dict[str, Any],
        sensor_map: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Resolve valores de sensores usando o sensor_map.

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
            resolved = self._resolve_sensor_value(
                sensor_name, param_value, calculated_value
            )

            if resolved is not None and sensor_name in sensor_values:
                sensor_values[sensor_name] = resolved

        return sensor_values

    def _resolve_sensor_value(
        self,
        sensor_name: str,
        raw_value: Any,
        calculated: Optional[float],
    ) -> Any:
        """Resolve o valor de um sensor usando o handler apropriado.

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
        profile: TrackerProfile,
    ) -> Dict[str, Any]:
        """Aplica fallback de parâmetros do perfil para valores não resolvidos.

        Args:
            params: Parâmetros da mensagem Wialon
            sensor_values: Valores já resolvidos via sensor_map
            profile: Perfil de tracker detectado pra esta mensagem

        Returns:
            Dicionário com valores atualizados incluindo fallbacks
        """
        known_params = profile.known_params()

        for field in self.SENSOR_FIELDS:
            if sensor_values.get(field) is not None:
                continue

            # Ignição vira bool; demais campos passam pelo handler do sensor.
            converter = bool if field == "ignition" else None
            candidate_keys = known_params.get(field, [])
            sensor_values[field] = self._get_param_fallback(
                params, candidate_keys, converter
            )

        return sensor_values

    def _get_param_fallback(
        self,
        params: Dict[str, Any],
        candidate_keys: List[str],
        converter: Optional[Callable] = None,
    ) -> Optional[Any]:
        """Busca o primeiro param presente em `candidate_keys`.

        Args:
            params: Dicionário de parâmetros da mensagem
            candidate_keys: Nomes de params a tentar, em ordem de preferência
            converter: Função opcional para converter o valor (ex: bool)

        Returns:
            Valor encontrado ou None se nenhum candidato existir
        """
        for key in candidate_keys:
            if key in params and params[key] is not None:
                value = params[key]
                return converter(value) if converter else value

        return None
