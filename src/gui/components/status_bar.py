"""
Barra de status da aplicação.
"""

import customtkinter as ctk
from datetime import datetime

from src.gui.design import Colors


class StatusBar(ctk.CTkFrame):
    """Barra de status no rodapé da aplicação."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, height=30, **kwargs)
        
        self.grid_columnconfigure(1, weight=1)
        
        # Ícone de status
        self.status_icon = ctk.CTkLabel(
            self,
            text="●",
            font=ctk.CTkFont(size=10),
            text_color=Colors.SUCCESS  # Verde por padrão
        )
        self.status_icon.grid(row=0, column=0, padx=(10, 5), pady=5)
        
        # Mensagem
        self.status_label = ctk.CTkLabel(
            self,
            text="Pronto",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.status_label.grid(row=0, column=1, sticky="w", pady=5)
        
        # Hora
        self.time_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.time_label.grid(row=0, column=2, padx=10, pady=5)
        
        self._update_time()
    
    def set_status(self, message: str, status_type: str = "info"):
        """
        Define a mensagem de status.
        
        Args:
            message: Mensagem a exibir
            status_type: Tipo do status (info, success, warning, error)
        """
        colors = {
            "info": Colors.INFO,
            "success": Colors.SUCCESS,
            "warning": Colors.WARNING,
            "error": Colors.ERROR,
        }

        color = colors.get(status_type, colors["info"])
        
        self.status_icon.configure(text_color=color)
        self.status_label.configure(text=message)
    
    def _update_time(self):
        """Atualiza o relógio."""
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.configure(text=now)
        self.after(1000, self._update_time)
