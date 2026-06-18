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
    # Modelos Suntech conhecidos. A detecção por rep_type (abaixo) é a rede
    # principal, já que toda a família usa o protocolo "Universal".
    SUNTECH_MODELS = {170, 197}

    # Report types do protocolo Universal da Suntech. Além do STT (status),
    # os dispositivos enviam alertas (ALT), emergência (EMG), eventos (EVT/ALV)
    # e dados expandidos/RFID (UEX). Todos são Suntech e devem usar este perfil.
    SUNTECH_REPORT_TYPES = {"STT", "EMG", "EVT", "ALT", "ALV", "UEX", "BLE", "HBR"}

    def matches(self, message: Dict[str, Any]) -> bool:
        params = message.get("p", {}) or {}
        if params.get("model") in self.SUNTECH_MODELS:
            return True
        if params.get("rep_type") in self.SUNTECH_REPORT_TYPES:
            return True
        return False

    def known_params(self) -> Dict[str, List[str]]:
        # Só assumimos o que é CONSISTENTE no protocolo Suntech: `mode` é a
        # ignição (1=ligado, 0=desligado) nas mensagens STT. Voltagens e
        # odômetro vivem em slots `s_asgn`/`m_asgn` cujo significado VARIA por
        # modelo/firmware (ex: no ST380 s_asgn1=veículo; no model 170 s_asgn1=
        # interna). Por isso NÃO chutamos esses slots aqui — eles vêm do
        # sensor_map configurado pelo admin, que é correto por dispositivo.
        return {
            "ignition": ["mode"],
            "fuel_level": [],
            "rpm": [],
            "vehicle_voltage": [],
            "internal_battery_voltage": [],
            "engine_hours": [],
        }

    def extract_odometer_meters(self, params: Dict[str, Any]) -> Optional[float]:
        # `m_asgn1` é odômetro em metros — VALIDADO apenas no ST380 (model 197,
        # ex: 240.131.878 m). Em outros modelos o slot tem outro significado
        # (no model 170, m_asgn1 são valores pequenos, não quilometragem), então
        # só confiamos nele para o 197. Demais: nome simbólico se o admin mapeou.
        if params.get("model") == 197 and params.get("m_asgn1") is not None:
            return float(params["m_asgn1"])
        for key in ("odometer", "mileage"):
            value = params.get(key)
            if value is not None:
                return float(value)
        return None
