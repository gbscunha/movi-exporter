"""Perfil padrão — usado quando nenhum perfil específico é detectado.

Reúne os nomes de params mais comuns vistos em mensagens Wialon "genéricas"
(trackers que reportam ao Wialon usando convenções da própria plataforma).
"""

from typing import Any, Dict, List, Optional


class DefaultProfile:
    """Fallback que aceita qualquer mensagem.

    DEVE ser o último na lista de perfis registrados — seu `matches()`
    sempre retorna True, então captura tudo que os perfis específicos
    não pegaram.
    """

    name = "default"

    def matches(self, message: Dict[str, Any]) -> bool:
        return True

    def known_params(self) -> Dict[str, List[str]]:
        # IMPORTANTE: bateria do veículo (~12-28V) e bateria interna do
        # tracker (~4V) são DUAS coisas diferentes e vivem em duas colunas
        # separadas no CSV. Nunca fazer fallback de uma para a outra.
        return {
            "ignition": ["in", "in1", "din1", "ignition", "ign"],
            "fuel_level": [
                "fuel1",
                "fuel2",
                "fuel_level",
                "can_fuel_level",
                "fuel",
                "fls",
            ],
            "rpm": ["rpm", "can_rpm", "engine_rpm", "eng_rpm"],
            # Tensão do veículo (~12-28V) — APENAS pwr_ext, sem fallback.
            "vehicle_voltage": ["pwr_ext"],
            # Bateria interna do tracker (~4V) — bateria backup do dispositivo.
            "internal_battery_voltage": ["pwr_int", "voltage", "battery", "batt"],
            "engine_hours": ["engine_hours", "eng_hours", "horimeter", "eh", "mh"],
        }

    def extract_odometer_meters(self, params: Dict[str, Any]) -> Optional[float]:
        # `is not None` preserva leitura legítima de 0 km (veículo novo) —
        # zero é dado real, não dado ausente.
        for key in ("odometer", "new_mileage", "mileage"):
            value = params.get(key)
            if value is not None:
                return float(value)
        return None
