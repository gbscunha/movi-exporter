"""Interface comum dos perfis de tracker."""

from typing import Any, Dict, List, Optional, Protocol, runtime_checkable


@runtime_checkable
class TrackerProfile(Protocol):
    """Adapta extração de params de uma mensagem Wialon ao dialeto de um tracker.

    Cada fabricante (Suntech, Queclink, Teltonika...) tende a usar nomes
    diferentes para os mesmos conceitos. Em vez de empilhar fallbacks numa
    lista única (que pode pegar o param errado), cada dialeto vive em um
    perfil isolado.
    """

    name: str

    def matches(self, message: Dict[str, Any]) -> bool:
        """Retorna True se esta mensagem pertence ao dialeto deste perfil.

        Implementações devem inspecionar `message["p"]` em busca de
        identificadores conhecidos (ex: `model`, `rep_type`).
        """
        ...

    def known_params(self) -> Dict[str, List[str]]:
        """Mapping `campo_normalizado → lista de params candidatos`.

        Campos esperados: `ignition`, `fuel_level`, `rpm`,
        `vehicle_voltage`, `internal_battery_voltage`, `engine_hours`.
        """
        ...

    def extract_odometer_meters(self, params: Dict[str, Any]) -> Optional[float]:
        """Extrai odômetro em metros (cada tracker pode usar param próprio)."""
        ...

    def resolve_ignition_event(self, params: Dict[str, Any]) -> Optional[bool]:
        """Traduz um evento de ignição (quando há) em estado on/off.

        OPCIONAL — perfis cujo tracker reporta ignição só por evento de
        transição (ex.: Suntech `alert_id` 33/34) implementam isto. Retorna
        True (ligou), False (desligou) ou None (sem evento de ignição). O
        transformer só consulta isto quando o sinal contínuo está ausente.
        """
        ...
