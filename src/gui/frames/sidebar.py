"""
Barra lateral de navegação.
"""

import customtkinter as ctk
from typing import Callable, Optional

from src.gui import __version__


class SidebarFrame(ctk.CTkFrame):
    """Barra lateral com navegação principal."""
    
    def __init__(self, master, on_navigate: Callable[[str], None], **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_navigate = on_navigate
        self.buttons: dict[str, ctk.CTkButton] = {}
        self.active_button: Optional[str] = None
        
        # Cores
        self.active_color = "#1f538d"
        self.hover_color = "#14375e"
        self.normal_color = "transparent"
        
        # Configurar grid
        self.grid_rowconfigure(10, weight=1)  # Espaço flexível
        
        # Logo/Título
        self.logo_label = ctk.CTkLabel(
            self,
            text="🚗 Movi Exporter",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Botões de navegação
        self._create_nav_button("home", "🏠  Início", row=1)
        self._create_nav_button("export", "📤  Exportar", row=2)
        self._create_nav_button("settings", "⚙️  Configurações", row=3)
        
        # Versão (no rodapé)
        self.version_label = ctk.CTkLabel(
            self,
            text=f"v{__version__}",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.version_label.grid(row=11, column=0, padx=20, pady=10)
    
    def _create_nav_button(self, name: str, text: str, row: int):
        """Cria um botão de navegação."""
        button = ctk.CTkButton(
            self,
            text=text,
            font=ctk.CTkFont(size=14),
            anchor="w",
            height=40,
            corner_radius=8,
            fg_color=self.normal_color,
            hover_color=self.hover_color,
            command=lambda: self._on_click(name)
        )
        button.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        self.buttons[name] = button
    
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
