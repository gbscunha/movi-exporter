"""Perfis de tracker — adaptam o transformer a dialetos diferentes.

Cada fabricante de tracker GPS usa nomenclatura própria nos parâmetros das
mensagens enviadas ao Wialon (ex: Suntech ST380 usa `mode` para ignição em
vez de `in`/`in1`). Em vez de empilhar fallbacks numa lista única que pode
acabar pegando o param errado em outro fabricante, isolamos cada dialeto
em um perfil.

Fluxo:
1. `detect_profile(message)` consulta cada perfil registrado em ordem
2. Primeiro perfil cujo `matches()` retorna True é escolhido
3. Transformer usa esse perfil para extrair ignição, odômetro, voltagens

Adicionar novo tracker = criar novo módulo aqui implementando `TrackerProfile`
e registrar em `registry.py`. Não tocar no `WialonTransformer`.
"""

from src.services.tracker_profiles.base import TrackerProfile
from src.services.tracker_profiles.default import DefaultProfile
from src.services.tracker_profiles.registry import DEFAULT_PROFILES, detect_profile
from src.services.tracker_profiles.suntech import SuntechProfile

__all__ = [
    "DEFAULT_PROFILES",
    "DefaultProfile",
    "SuntechProfile",
    "TrackerProfile",
    "detect_profile",
]
