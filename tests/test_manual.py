"""Testes do manual do usuário: localizador (Onda 3 Fase 04 — #52) e integridade.

Os testes de integridade existem porque o manual já descreveu botões que tinham
sido renomeados no app (spec `docs/specs/manual-usuario.md`): quando um rótulo
muda na GUI, o teste falha e aponta o termo a corrigir no manual.
"""

import re
from pathlib import Path

from src.gui import manual

# Rótulos que o manual cita como nomes de botões/opções da interface. Cada um
# precisa existir literalmente no fonte da GUI — é o que pega a divergência.
ROTULOS_DA_GUI = [
    "Testar Conexões",
    "Ver Veículos",
    "Todos os veículos",
    "Escolher manualmente",
    "Limpar todos",
    "Gerar arquivo consolidado",
    "Upload para Google Drive",
    "Incluir endereço (mais lento)",
    "Iniciar Exportação",
    "Abrir pasta",
    "Salvar alterações",
]


def _html() -> str:
    path = manual.manual_path()
    assert path is not None
    return path.read_text(encoding="utf-8")


def _fontes_da_gui() -> str:
    raiz = Path(__file__).resolve().parent.parent / "src" / "gui"
    return "\n".join(p.read_text(encoding="utf-8") for p in raiz.rglob("*.py"))


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


def test_indice_nao_tem_ancora_quebrada():
    """Todo link interno do manual aponta para uma seção que existe."""
    html = _html()
    ancoras = set(re.findall(r'href="#([^"]+)"', html))
    ids = set(re.findall(r'id="([^"]+)"', html))

    assert ancoras, "o manual deveria ter índice com links internos"
    assert ancoras <= ids, f"âncoras sem seção correspondente: {sorted(ancoras - ids)}"


def test_figuras_usam_images_e_degradam_sem_arquivo():
    """Imagens ficam em `images/`, têm alt curto e somem enquanto não existem.

    Os prints são tirados pelo humano depois; até lá o `onerror` esconde a
    figura para o manual não exibir ícone de imagem quebrada.
    """
    html = _html()
    imgs = re.findall(r"<img\b[^>]*>", html)

    assert imgs, "o manual deveria ter figuras (mesmo que os prints ainda faltem)"
    for img in imgs:
        src = re.search(r'src="([^"]*)"', img)
        assert src and src.group(1).startswith("images/"), (
            f"imagem fora de images/: {img}"
        )
        alt = re.search(r'alt="([^"]*)"', img)
        assert alt and alt.group(1).strip(), f"imagem sem alt descritivo: {img}"
        assert "onerror" in img, f"imagem sem fallback onerror: {img}"


def test_rotulos_citados_existem_na_gui():
    """Rótulos que o manual cita precisam existir no fonte da GUI."""
    html = _html()
    fontes = _fontes_da_gui()

    for rotulo in ROTULOS_DA_GUI:
        assert rotulo in fontes, f"rótulo não existe mais na GUI: {rotulo!r}"
        assert rotulo in html, f"rótulo da GUI não citado no manual: {rotulo!r}"
