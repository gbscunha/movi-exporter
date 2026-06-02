"""Registro e detecção de perfis."""

from typing import Any, Dict, List, Set, Tuple

from src.core.logger import logger
from src.services.tracker_profiles.base import TrackerProfile
from src.services.tracker_profiles.default import DefaultProfile
from src.services.tracker_profiles.jimi import JimiProfile
from src.services.tracker_profiles.suntech import SuntechProfile

# Ordem importa: perfis específicos primeiro, fallback genérico no fim.
# Para adicionar suporte a outro tracker, criar novo módulo aqui e
# adicionar a instância antes do DefaultProfile.
DEFAULT_PROFILES: List[TrackerProfile] = [
    SuntechProfile(),
    JimiProfile(),
    DefaultProfile(),
]

# Combinações `(model, rep_type)` já avistadas caindo no DefaultProfile.
# Serve para logar warning UMA vez por combinação descoberta — caso contrário
# inundaríamos o `app.log` com milhares de linhas iguais (1 por mensagem).
#
# Estado em escopo de módulo (= processo). Reset acontece naturalmente em
# cada execução do app/CLI, o que é o comportamento desejado: o usuário vê
# o warning uma vez por sessão.
_UNKNOWN_TRACKERS_SEEN: Set[Tuple[Any, Any]] = set()


def _maybe_warn_unknown_tracker(message: Dict[str, Any]) -> None:
    """Loga warning quando uma combinação `(model, rep_type)` nova cai no
    DefaultProfile. Sinal de que existe tracker em uso que merece perfil próprio.

    Sem isso, problemas como o do Suntech (CSV silenciosamente errado para
    330 veículos por meses) ficam invisíveis até alguém abrir o arquivo.
    """
    params = message.get("p", {}) or {}
    model = params.get("model")
    rep_type = params.get("rep_type")

    # Mensagens sem nenhum identificador útil — não vale logar (provavelmente
    # mensagem data-only ou tracker antigo sem metadados).
    if model is None and rep_type is None:
        return

    key = (model, rep_type)
    if key in _UNKNOWN_TRACKERS_SEEN:
        return

    _UNKNOWN_TRACKERS_SEEN.add(key)
    logger.warning(
        f"Tracker desconhecido caiu no perfil padrão: model={model!r}, "
        f"rep_type={rep_type!r}. Colunas como ignição/odômetro podem aparecer "
        f"como N/D no CSV. Considere criar um perfil específico em "
        f"src/services/tracker_profiles/."
    )


def detect_profile(
    message: Dict[str, Any],
    profiles: List[TrackerProfile] = DEFAULT_PROFILES,
) -> TrackerProfile:
    """Retorna o primeiro perfil cujo `matches()` aceita a mensagem.

    `DefaultProfile` no fim garante que sempre há um match (ele sempre
    retorna True), então a função nunca lança.

    Side effect: se a mensagem cair no DefaultProfile mas tiver `model`
    ou `rep_type` populados (indicando que é um tracker identificável),
    loga warning uma vez por combinação descoberta.
    """
    for profile in profiles:
        if profile.matches(message):
            if isinstance(profile, DefaultProfile):
                _maybe_warn_unknown_tracker(message)
            return profile
    # Defensivo — não deve acontecer se DefaultProfile estiver na lista.
    return profiles[-1]


def reset_unknown_tracker_cache() -> None:
    """Limpa o cache de trackers desconhecidos já avistados.

    Útil em testes para isolar cenários. Em produção, o cache reseta
    naturalmente a cada processo.
    """
    _UNKNOWN_TRACKERS_SEEN.clear()
