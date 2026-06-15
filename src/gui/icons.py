"""Ícones FontAwesome renderizados como CTkImage.

Por que imagem e não fonte de ícone direta: no CustomTkinter um widget usa
uma única fonte, então não dá para misturar glifo (icon font) + texto no
mesmo botão. Renderizando o glifo para uma imagem (via Pillow) e usando o
parâmetro `image=` do CTkButton/CTkLabel, ícone e texto convivem nativamente.

Os glifos são renderizados sob demanda e cacheados por (codepoint, tamanho,
cor_light, cor_dark). Cada CTkImage carrega duas variantes de cor (clara e
escura) para acompanhar o tema — preparado para o light mode (Onda 3 Fase 2).

Uso:
    from src.gui import icons
    botao = ctk.CTkButton(parent, text="Salvar", image=icons.get(icons.SAVE))
    label = ctk.CTkLabel(parent, text="", image=icons.get(icons.CIRCLE_CHECK,
                                                          color=Colors.SUCCESS))
"""

from pathlib import Path
from typing import Dict, Optional, Tuple

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

from src.core.logger import logger

# Caminho da fonte vendorizada (FontAwesome 6 Free Solid, licença SIL OFL).
_FONT_PATH = Path(__file__).parent / "assets" / "fontawesome-solid.ttf"

# Tamanho padrão dos ícones em pixels.
DEFAULT_SIZE = 18

# Cores padrão para tema escuro/claro quando nenhuma cor é passada.
# Renderizamos a glifo em ambas e o CTkImage troca conforme o appearance mode.
_DEFAULT_DARK = "#dce4ee"  # quase-branco (tema escuro)
_DEFAULT_LIGHT = "#1a1a1a"  # quase-preto (tema claro)

# ---------------------------------------------------------------------------
# Codepoints (FontAwesome 6 Free Solid). Validados como renderizáveis.
# Nomes seguem o ícone, não o emoji que substituem.
# ---------------------------------------------------------------------------
PLUG = ""
EYE = ""
EYE_SLASH = ""
SAVE = ""  # floppy-disk
SEARCH = ""  # magnifying-glass
FOLDER_OPEN = ""
FOLDER = ""
PLAY = ""
REFRESH = ""  # arrows-rotate
LIST = ""
GEAR = ""
HOME = ""  # house
FILE_EXPORT = ""
UPLOAD = ""
CLOUD = ""
CIRCLE_CHECK = ""
CIRCLE_XMARK = ""
TRIANGLE_WARNING = ""  # triangle-exclamation
COPY = ""
LINK = ""  # arrow-up-right-from-square (abrir externo)
TRUCK = ""
CALENDAR = ""

# Cache de fontes por tamanho e de imagens por (cp, size, dark, light).
_font_cache: Dict[int, ImageFont.FreeTypeFont] = {}
_image_cache: Dict[Tuple[str, int, str, str], ctk.CTkImage] = {}


def _font(size: int) -> ImageFont.FreeTypeFont:
    """Carrega (e cacheia) a fonte FontAwesome no tamanho dado."""
    if size not in _font_cache:
        _font_cache[size] = ImageFont.truetype(str(_FONT_PATH), size)
    return _font_cache[size]


def _render(codepoint: str, size: int, color: str) -> Image.Image:
    """Renderiza um glifo centralizado numa imagem RGBA quadrada."""
    font = _font(size)
    # Caixa um pouco maior que o tamanho para não cortar glifos largos.
    canvas = int(size * 1.25)
    img = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Centraliza usinando a bounding box real do glifo.
    bbox = draw.textbbox((0, 0), codepoint, font=font)
    glyph_w = bbox[2] - bbox[0]
    glyph_h = bbox[3] - bbox[1]
    x = (canvas - glyph_w) / 2 - bbox[0]
    y = (canvas - glyph_h) / 2 - bbox[1]
    draw.text((x, y), codepoint, font=font, fill=color)
    return img


def get(
    codepoint: str,
    size: int = DEFAULT_SIZE,
    color: Optional[str] = None,
    color_light: Optional[str] = None,
) -> ctk.CTkImage:
    """Retorna um CTkImage do ícone, cacheado.

    Args:
        codepoint: constante deste módulo (ex: icons.SAVE)
        size: lado da imagem em pixels
        color: cor para o tema escuro (default: quase-branco). Se `color` for
               passado e `color_light` não, usa a mesma cor nos dois temas —
               útil para ícones semânticos (success/error) que têm cor fixa.
        color_light: cor para o tema claro (default: quase-preto)

    Returns:
        CTkImage com variantes clara e escura.
    """
    dark = color or _DEFAULT_DARK
    light = color_light or (color if color else _DEFAULT_LIGHT)

    key = (codepoint, size, dark, light)
    if key not in _image_cache:
        _image_cache[key] = ctk.CTkImage(
            light_image=_render(codepoint, size, light),
            dark_image=_render(codepoint, size, dark),
            size=(size, size),
        )
    return _image_cache[key]


def is_available() -> bool:
    """True se a fonte FontAwesome está presente no bundle."""
    return _FONT_PATH.exists()


def _warn_if_missing() -> None:
    if not is_available():
        logger.warning(
            f"Fonte FontAwesome não encontrada em {_FONT_PATH}. "
            "Ícones não serão exibidos."
        )


_warn_if_missing()
