"""
Barra lateral de navegação.
"""

from pathlib import Path
from typing import Callable, Optional

import customtkinter as ctk

from src.core.config import settings
from src.gui import __version__, icons
from src.gui.account_state import AccountState
from src.gui.design import Colors
from src.gui.messages import SidebarMsg

# Logo opcional — se o PNG existir em assets, é exibido no topo da sidebar;
# senão, cai no texto "Movi Exporter".
_LOGO_PATH = Path(__file__).parent.parent / "assets" / "movi-logo.png"


class SidebarFrame(ctk.CTkFrame):
    """Barra lateral com navegação principal."""

    def __init__(
        self,
        master,
        on_navigate: Callable[[str], None],
        account_state: Optional[AccountState] = None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.on_navigate = on_navigate
        self.account_state = account_state
        self.buttons: dict[str, ctk.CTkButton] = {}
        self.active_button: Optional[str] = None

        # Cores: acento ativo = vermelho Movi; texto theme-aware para os
        # botões transparentes ficarem legíveis no claro e no escuro (#1).
        self.active_color = Colors.PRIMARY
        self.hover_color = Colors.PRIMARY_HOVER
        self.normal_color = "transparent"
        self.nav_text_color = ("gray10", "gray90")

        # Grid: a linha 20 é o espaçador flexível que empurra o grupo de
        # rodapé (ações + versão) para baixo, separado da navegação no topo.
        self.grid_rowconfigure(20, weight=1)

        # --- Topo: logo ---
        self._create_logo()
        self._create_separator(row=1)

        # --- Grupo: navegação ---
        self._create_nav_button("home", f"  {SidebarMsg.NAV_INICIO}", icons.HOME, row=2)
        self._create_nav_button(
            "export", f"  {SidebarMsg.NAV_EXPORTAR}", icons.FILE_EXPORT, row=3
        )
        self._create_nav_button(
            "settings", f"  {SidebarMsg.NAV_CONFIGURACOES}", icons.GEAR, row=4
        )

        # --- Grupo: conta (só aparece se houver Conta 2 configurada) ---
        if self.account_state is not None and settings.WIALON_TOKEN_2:
            self._create_separator(row=5)
            self._create_account_selector(row=6)

        # --- Rodapé: ações (abaixo do espaçador) ---
        self._create_separator(row=21)
        self._create_action_button(
            f"  {SidebarMsg.ACAO_MANUAL}", icons.BOOK, self._open_manual, row=22
        )
        self._create_action_button(
            f"  {SidebarMsg.ACAO_SOBRE}", icons.INFO_CIRCLE, self._open_about, row=23
        )

        # Versão (no rodapé) — clicável, abre as notas de versão.
        self.version_button = ctk.CTkButton(
            self,
            text=SidebarMsg.VERSAO.format(versao=__version__),
            font=ctk.CTkFont(size=11),
            text_color="gray",
            fg_color="transparent",
            hover_color=self.hover_color,
            height=24,
            command=self._open_release_notes,
        )
        self.version_button.grid(row=24, column=0, padx=20, pady=(4, 12))

    def _create_separator(self, row: int):
        """Linha fina divisória entre grupos da sidebar."""
        sep = ctk.CTkFrame(self, height=1, fg_color=("gray80", "gray30"))
        sep.grid(row=row, column=0, padx=16, pady=8, sticky="ew")

    def _create_logo(self):
        """Exibe a logo Movi (imagem) no topo, ou o título textual se ausente."""
        if _LOGO_PATH.exists():
            try:
                from PIL import Image

                img = Image.open(_LOGO_PATH)
                # Escala para ~160px de largura mantendo proporção.
                w, h = img.size
                target_w = 160
                target_h = max(1, round(h * target_w / w))
                logo_img = ctk.CTkImage(
                    light_image=img, dark_image=img, size=(target_w, target_h)
                )
                self.logo_label = ctk.CTkLabel(self, image=logo_img, text="")
                self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
                return
            except Exception as e:  # noqa: BLE001 — fallback para texto
                from src.core.logger import logger

                logger.debug(f"Falha ao carregar logo, usando texto: {e}")

        self.logo_label = ctk.CTkLabel(
            self,
            text=SidebarMsg.TITULO,
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

    def _create_account_selector(self, row: int):
        """Cria o seletor de conta (label + dropdown)."""
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=row, column=0, padx=10, pady=(20, 5), sticky="ew")

        ctk.CTkLabel(
            container,
            text=SidebarMsg.LABEL_CONTA,
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w",
        ).grid(row=0, column=0, padx=6, pady=(0, 2), sticky="w")

        self.account_var = ctk.StringVar()
        self.account_menu = ctk.CTkOptionMenu(
            container,
            variable=self.account_var,
            command=self._on_account_selected,
        )
        self.account_menu.grid(row=1, column=0, padx=6, sticky="ew")
        container.grid_columnconfigure(0, weight=1)

        self._refresh_account_labels()
        # O nome só é conhecido depois que a conta autentica (boot da Home ou
        # botão Testar), então os itens são remontados quando ele chega.
        self.account_state.register_username_listener(self._refresh_account_labels)

    def _refresh_account_labels(self):
        """(Re)monta os itens do seletor com o nome de quem está autenticado.

        Chamado sempre na thread da GUI — quem descobre o nome volta com
        `after(0, ...)` antes de avisar o estado.
        """
        labels = self.account_state.labels()
        self.account_menu.configure(values=list(labels.values()))
        self.account_var.set(labels[self.account_state.account])

    def _on_account_selected(self, value: str):
        """Traduz a seleção do dropdown e propaga ao estado global."""
        if self.account_state is None:
            return
        self.account_state.set_account(self.account_state.account_for_label(value))

    def _create_nav_button(self, name: str, text: str, icon: str, row: int):
        """Cria um botão de navegação com ícone FontAwesome."""
        button = ctk.CTkButton(
            self,
            text=text,
            image=icons.get(icon, size=18),
            font=ctk.CTkFont(size=14),
            anchor="w",
            height=40,
            corner_radius=8,
            fg_color=self.normal_color,
            hover_color=self.hover_color,
            # Texto theme-aware: botão é transparente quando inativo, então o
            # texto branco global não serve (sumia no modo claro — bug #1).
            text_color=self.nav_text_color,
            command=lambda: self._on_click(name),
        )
        button.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        self.buttons[name] = button

    def _create_action_button(self, text: str, icon: str, command, row: int):
        """Botão de ação do rodapé (Manual, Sobre) — sem estado ativo."""
        button = ctk.CTkButton(
            self,
            text=text,
            image=icons.get(icon, size=16),
            font=ctk.CTkFont(size=13),
            anchor="w",
            height=34,
            corner_radius=8,
            fg_color=self.normal_color,
            hover_color=self.hover_color,
            text_color=self.nav_text_color,
            command=command,
        )
        button.grid(row=row, column=0, padx=10, pady=3, sticky="ew")
        return button

    def _open_manual(self):
        """Abre o manual do usuário no navegador."""
        from src.gui.components import toast
        from src.gui.manual import open_manual

        if not open_manual():
            toast.show(SidebarMsg.TOAST_MANUAL_NAO_ENCONTRADO, kind="warning")

    def _open_about(self):
        """Abre o diálogo Sobre."""
        from src.gui.dialogs.about_dialog import AboutDialog

        AboutDialog(self.winfo_toplevel())

    def _open_release_notes(self):
        """Abre as notas de versão no navegador."""
        import webbrowser

        from src.gui.updater import GITHUB_OWNER, GITHUB_REPO

        webbrowser.open(f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}/releases")

    def _on_click(self, name: str):
        """Handler de clique no botão."""
        self.set_active(name)
        self.on_navigate(name)

    def set_active(self, name: str):
        """Define o botão ativo."""
        # Reset todos
        for btn_name, btn in self.buttons.items():
            if btn_name == name:
                btn.configure(fg_color=self.active_color)
            else:
                btn.configure(fg_color=self.normal_color)

        self.active_button = name
