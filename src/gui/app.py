"""
Aplicação principal da GUI do Movi Exporter.
"""

import threading
from tkinter import messagebox
from typing import Optional

import customtkinter as ctk

from src.core.config import settings
from src.gui import __version__
from src.gui.account_state import AccountState
from src.gui.components.status_bar import StatusBar
from src.gui.frames.export import ExportFrame
from src.gui.frames.home import HomeFrame
from src.gui.frames.settings import SettingsFrame
from src.gui.frames.sidebar import SidebarFrame
from src.gui.updater import AutoUpdater


class MoviExporterApp(ctk.CTk):
    """Janela principal da aplicação."""
    
    def __init__(self):
        super().__init__()
        
        # Configuração da janela
        self.title(f"Movi Exporter v{__version__}")
        self.geometry("1100x700")
        self.minsize(900, 600)
        
        # Tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Frames
        self.frames: dict[str, ctk.CTkFrame] = {}
        self.current_frame: Optional[str] = None

        # Estado global da conta Wialon selecionada (compartilhado entre
        # sidebar, Home e Export). A sidebar muda; os frames reagem.
        self.account_state = AccountState()

        # Criar componentes
        self._create_sidebar()
        self._create_main_area()
        self._create_status_bar()
        
        # Iniciar na tela Home
        self.show_frame("home")

        # Onboarding — se o token Wialon não foi configurado, orienta o usuário
        # a abrir Settings antes de tentar exportar.
        if not settings.WIALON_TOKEN:
            self.after(300, self._show_setup_notice)

        # Verificar atualizações em background
        self._check_updates_async()
    
    def _create_sidebar(self):
        """Cria a barra lateral de navegação."""
        self.sidebar = SidebarFrame(
            self,
            on_navigate=self.show_frame,
            account_state=self.account_state,
            width=200
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

    def _create_main_area(self):
        """Cria a área principal com os frames."""
        # Container principal
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Criar frames — Home e Export recebem o estado de conta compartilhado.
        self.frames["home"] = HomeFrame(
            self.main_container, account_state=self.account_state
        )
        self.frames["export"] = ExportFrame(
            self.main_container,
            status_callback=self.update_status,
            account_state=self.account_state,
        )
        self.frames["settings"] = SettingsFrame(self.main_container)

        # Posicionar todos os frames (só um visível por vez)
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")
    
    def _create_status_bar(self):
        """Cria a barra de status."""
        self.status_bar = StatusBar(self)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
    
    def show_frame(self, name: str):
        """Mostra um frame específico."""
        if name in self.frames:
            self.frames[name].tkraise()
            self.current_frame = name
            self.sidebar.set_active(name)
    
    def update_status(self, message: str, status_type: str = "info"):
        """Atualiza a barra de status."""
        self.status_bar.set_status(message, status_type)
    
    def _check_updates_async(self):
        """Verifica atualizações em background."""
        def check():
            updater = AutoUpdater()
            has_update, version, url = updater.check_for_updates()
            
            if has_update:
                self.after(0, lambda: self._show_update_dialog(version, url))
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
    
    def _show_update_dialog(self, version: str, download_url: str):
        """Mostra diálogo de atualização disponível."""
        from src.gui.dialogs.update_dialog import UpdateDialog
        dialog = UpdateDialog(self, version, download_url)
        dialog.grab_set()

    def _show_setup_notice(self):
        """Avisa o usuário que falta configurar o token Wialon."""
        messagebox.showinfo(
            "Configuração necessária",
            "O token da API Wialon ainda não foi configurado.\n\n"
            "Abra a tela de Configurações para colar seu token e testá-lo "
            "antes de iniciar uma exportação.",
        )
        self.show_frame("settings")


def run():
    """Inicia a aplicação."""
    app = MoviExporterApp()
    app.mainloop()


if __name__ == "__main__":
    run()
