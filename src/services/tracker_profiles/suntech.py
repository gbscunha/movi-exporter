"""Perfil para trackers Suntech (família ST380, model 197+).

Suntech (Coreia do Sul) é fabricante OEM de trackers veiculares. Suas mensagens
chegam ao Wialon com `rep_type='STT'` e usam slots de "assignments" no lugar
de nomes simbólicos:

    s_asgn1, s_asgn2, ...  → sensores analógicos (voltagens, temperaturas)
    m_asgn1, m_asgn2, ...  → contadores/medidores (odômetro, horímetro)

Por convenção da indústria brasileira (validado em frota real do cliente),
o firmware padrão atribui:

    s_asgn1 → tensão do veículo (~12-28V)
    s_asgn2 → bateria interna do tracker (~4V)
    m_asgn1 → odômetro em metros

Ignição NÃO vem em `in`/`in1` (esses params nem existem nas msgs Suntech).
Vem em `mode` (1 = motor ligado, 0 = motor desligado).
"""

from typing import Any, Dict, List, Optional


class SuntechProfile:
    """Detecta e mapeia mensagens de trackers Suntech."""

    name = "suntech"

    # `model` 197 é o ST380. Famílias próximas (ST300, ST340) também usam
    # `rep_type='STT'` — manter o match por rep_type como rede de segurança.
    SUNTECH_MODELS = {197}

    def matches(self, message: Dict[str, Any]) -> bool:
        params = message.get("p", {}) or {}
        if params.get("model") in self.SUNTECH_MODELS:
            return True
        if params.get("rep_type") == "STT":
            return True
        return False

    def known_params(self) -> Dict[str, List[str]]:
        return {
            # Suntech ST380 não envia `in`/`in1`/`din1`. Ignição vem via
            # `mode` (1 = motor ligado, 0 = desligado). Confirmado no QA:
            # mensagens com vel > 0 sempre têm `mode=1`, parado sempre `mode=0`.
            "ignition": ["mode"],
            "fuel_level": [],  # Frota atual não reporta combustível.
            "rpm": [],  # Frota atual não reporta RPM.
            "vehicle_voltage": ["s_asgn1"],
            "internal_battery_voltage": ["s_asgn2"],
            "engine_hours": [],  # `m_asgn2`/`m_asgn3` ainda não decodificados.
        }

    def extract_odometer_meters(self, params: Dict[str, Any]) -> Optional[float]:
        # Suntech: odômetro em `m_asgn1` (em metros). Aceitar `odometer`
        # como fallback caso admin tenha configurado sensor manualmente
        # apontando para esse nome simbólico no Wialon.
        for key in ("m_asgn1", "odometer"):
            value = params.get(key)
            if value is not None:
                return float(value)
        return None
