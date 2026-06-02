"""Registro e detecção de perfis."""

from typing import Any, Dict, List

from src.services.tracker_profiles.base import TrackerProfile
from src.services.tracker_profiles.default import DefaultProfile
from src.services.tracker_profiles.suntech import SuntechProfile

# Ordem importa: perfis específicos primeiro, fallback genérico no fim.
# Para adicionar suporte a outro tracker, criar novo módulo aqui e
# adicionar a instância antes do DefaultProfile.
DEFAULT_PROFILES: List[TrackerProfile] = [
    SuntechProfile(),
    DefaultProfile(),
]


def detect_profile(
    message: Dict[str, Any],
    profiles: List[TrackerProfile] = DEFAULT_PROFILES,
) -> TrackerProfile:
    """Retorna o primeiro perfil cujo `matches()` aceita a mensagem.

    `DefaultProfile` no fim garante que sempre há um match (ele sempre
    retorna True), então a função nunca lança.
    """
    for profile in profiles:
        if profile.matches(message):
            return profile
    # Defensivo — não deve acontecer se DefaultProfile estiver na lista.
    return profiles[-1]
