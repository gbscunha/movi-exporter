"""Testes do localizador do manual (Onda 3 Fase 04 — #52)."""

from src.gui import manual


def test_manual_path_encontra_html_no_projeto():
    """Em desenvolvimento, manual.html deve ser encontrado a partir do projeto."""
    path = manual.manual_path()
    assert path is not None
    assert path.name == "manual.html"
    assert path.exists()


def test_candidate_paths_inclui_projeto_e_bundle():
    candidates = manual._candidate_paths()
    # Sempre há ao menos o caminho do projeto (dev).
    assert any(c.name == "manual.html" for c in candidates)
