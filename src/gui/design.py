"""Design tokens — fonte única para cores, espaçamentos e tipografia da GUI.

Antes deste módulo, cores hex viviam espalhadas e divergentes pelos frames
(dois verdes diferentes para "sucesso", dois vermelhos para "erro", etc).
Centralizar aqui garante consistência visual e facilita ajustes futuros
(ex: auditoria de light mode — item #11 do backlog).

Uso:
    from src.gui.design import Colors, Space, Font

    label.configure(text_color=Colors.SUCCESS)
    button.grid(padx=Space.MD, pady=Space.SM)
    ctk.CTkFont(size=Font.SIZE_LG, weight=Font.WEIGHT_BOLD)
"""


class Colors:
    """Cores semânticas. Tons escolhidos para bom contraste no tema escuro."""

    SUCCESS = "#2ecc71"  # verde — operação bem-sucedida, conectado
    WARNING = "#f39c12"  # amarelo/laranja — atenção, não testado, sem dados
    ERROR = "#e74c3c"  # vermelho — falha, desconectado
    INFO = "#3498db"  # azul — informação neutra
    MUTED = "#888888"  # cinza — texto secundário, placeholders


class Space:
    """Espaçamentos em pixels (padding/margin). Escala consistente."""

    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 24
    XXL = 32


class Font:
    """Tamanhos e pesos de fonte."""

    SIZE_SM = 11
    SIZE_BASE = 13
    SIZE_MD = 14
    SIZE_LG = 16
    SIZE_XL = 20
    SIZE_2XL = 28

    WEIGHT_NORMAL = "normal"
    WEIGHT_BOLD = "bold"


class Border:
    """Raios de borda."""

    RADIUS_SM = 6
    RADIUS_MD = 8
    RADIUS_LG = 12
