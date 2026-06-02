"""Perfil para trackers Jimi/Concox (VL03 e similares).

Jimi (China, mesma família da Concox) é fabricante OEM de trackers GPS,
muito populares no Brasil em frotas leves via dispositivos OBD-II
plug-and-play (Jimi VL03 é o exemplo emblemático).

Diferente do Suntech (que usa `rep_type='STT'` e `model` numérico),
Jimi NÃO popula esses campos de forma identificável. A detecção é feita
por uma combinação de params únicos do protocolo Jimi:

    serial         → contador incremental por mensagem
    gps_real_up    → flag de validade GPS
    data_mode      → modo de reporte (heartbeat, ignição, alarme...)

Essa combinação aparece em TODAS as mensagens GPS do Jimi VL03 e
NUNCA foi vista em outros fabricantes (Suntech, Wialon-genérico).
Validado em 430 mensagens reais (CVM0H79, Conta 2, cliente Movi).

Mapeamento de params:

    acc       (0/1)   → ignição
    pwr_ext   (~14V)  → tensão do veículo (mesmo nome do padrão Wialon)
    voltage   (~6V)   → bateria interna do tracker (NÃO confundir com
                        `voltage` do padrão Wialon onde já é tracker)

Odômetro: Jimi VL03 na config padrão NÃO reporta. Se aparecer (variantes
OBD report), tentar `obd_mileage` e `mileage` como fallback.
"""

from typing import Any, Dict, List, Optional


class JimiProfile:
    """Detecta e mapeia mensagens de trackers Jimi/Concox (VL03 e similares)."""

    name = "jimi"

    # Combinação assinatura do protocolo Jimi. Os 3 aparecem juntos em
    # TODAS as msgs GPS do VL03 e não em outros fabricantes observados.
    # Exigir os 3 evita falsos positivos com trackers que tenham só `acc`.
    _SIGNATURE_PARAMS = {"serial", "gps_real_up", "data_mode"}

    def matches(self, message: Dict[str, Any]) -> bool:
        params = message.get("p", {}) or {}
        return self._SIGNATURE_PARAMS.issubset(params.keys())

    def known_params(self) -> Dict[str, List[str]]:
        return {
            # Jimi usa `acc` (accessory/key) para ignição. 1=ligada, 0=desligada.
            "ignition": ["acc"],
            "fuel_level": [],  # VL03 nessa config não reporta.
            "rpm": [],  # VL03 nessa config não reporta.
            # Tensão do veículo: mesmo nome do padrão Wialon — Jimi reporta
            # em msg data-only separada (propagação pwr_ext da Fase 04 cobre).
            "vehicle_voltage": ["pwr_ext"],
            # Bateria interna do tracker. CUIDADO: o Suntech também tem
            # `voltage` mas com semântica diferente. O perfil isolado garante
            # que cada um vai pra coluna correta.
            "internal_battery_voltage": ["voltage"],
            "engine_hours": [],
        }

    def extract_odometer_meters(self, params: Dict[str, Any]) -> Optional[float]:
        # VL03 OBD pode reportar `obd_mileage` ou `mileage` em variantes
        # OBD-report (não vistas no QA, mas é a convenção Jimi).
        # `odometer` aceito como fallback caso admin configure sensor manual.
        for key in ("obd_mileage", "mileage", "odometer"):
            value = params.get(key)
            if value is not None:
                return float(value)
        return None
