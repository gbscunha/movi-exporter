"""
Diálogo de atualização disponível.
"""

import customtkinter as ctk
import threading
from typing import Optional

from src.gui.design import Colors
from src.gui.updater import AutoUpdater


class UpdateDialog(ctk.CTkToplevel):
    """Diálogo que informa sobre atualização disponível."""
    
    def __init__(self, master, version: str, download_url: Optional[str] = None):
        super().__init__(master)
        
        self.version = version
        self.download_url = download_url
        self.updater = AutoUpdater()
        self.updater.latest_version = version
        self.updater.download_url = download_url
        
        # Configuração da janela
        self.title("Atualização Disponível")
        self.geometry("450x300")
        self.resizable(False, False)
        
        # Centralizar
        self.transient(master)
        self.grab_set()
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        
        self._create_content()
    
    def _create_content(self):
        """Cria o conteúdo do diálogo."""
        # Ícone
        icon_label = ctk.CTkLabel(
            self,
            text="🎉",
            font=ctk.CTkFont(size=48)
        )
        icon_label.grid(row=0, column=0, pady=(20, 10))
        
        # Título
        title_label = ctk.CTkLabel(
            self,
            text="Nova Versão Disponível!",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=1, column=0, pady=(0, 10))
        
        # Versão
        from src.gui import __version__
        version_label = ctk.CTkLabel(
            self,
            text=f"Versão atual: {__version__}  →  Nova versão: {self.version}",
            font=ctk.CTkFont(size=13)
        )
        version_label.grid(row=2, column=0, pady=(0, 20))
        
        # Barra de progresso (escondida inicialmente)
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=3, column=0, sticky="ew", padx=40)
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="",
            font=ctk.CTkFont(size=11)
        )
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.set(0)
        
        # Botões
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=4, column=0, pady=20)
        
        self.update_btn = ctk.CTkButton(
            buttons_frame,
            text="📥  Baixar e Instalar",
            width=150,
            height=40,
            command=self._start_download
        )
        self.update_btn.grid(row=0, column=0, padx=10)
        
        self.later_btn = ctk.CTkButton(
            buttons_frame,
            text="Depois",
            width=100,
            height=40,
            fg_color="transparent",
            border_width=1,
            command=self.destroy
        )
        self.later_btn.grid(row=0, column=1, padx=10)
    
    def _start_download(self):
        """Inicia o download da atualização."""
        if not self.download_url:
            self._show_error("URL de download não disponível")
            return
        
        # Mostrar progresso
        self.progress_label.grid(row=0, column=0, pady=(0, 5))
        self.progress_bar.grid(row=1, column=0, sticky="ew")
        
        self.update_btn.configure(state="disabled", text="Baixando...")
        self.later_btn.configure(state="disabled")
        
        def download():
            def progress_callback(downloaded, total):
                percent = downloaded / total if total else 0
                self.after(0, lambda: self._update_progress(percent, downloaded, total))
            
            installer_path = self.updater.download_update(progress_callback)
            
            if installer_path:
                self.after(0, lambda: self._install(installer_path))
            else:
                self.after(0, lambda: self._show_error("Falha no download"))
        
        thread = threading.Thread(target=download, daemon=True)
        thread.start()
    
    def _update_progress(self, percent: float, downloaded: int, total: int):
        """Atualiza a barra de progresso."""
        self.progress_bar.set(percent)
        
        mb_downloaded = downloaded / (1024 * 1024)
        mb_total = total / (1024 * 1024)
        
        self.progress_label.configure(
            text=f"Baixando... {mb_downloaded:.1f} MB / {mb_total:.1f} MB"
        )
    
    def _install(self, installer_path: str):
        """Inicia a instalação."""
        self.progress_label.configure(text="Iniciando instalação...")
        self.update_btn.configure(text="Instalando...")
        
        self.updater.install_update(installer_path)
    
    def _show_error(self, message: str):
        """Mostra mensagem de erro."""
        self.progress_label.configure(text=f"❌ {message}", text_color=Colors.ERROR)
        self.progress_label.grid(row=0, column=0, pady=(0, 5))
        
        self.update_btn.configure(state="normal", text="📥  Tentar Novamente")
        self.later_btn.configure(state="normal")
