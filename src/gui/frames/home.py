"""
Tela inicial (Home).
"""

import customtkinter as ctk
import threading
from typing import Optional

from src.services.vehicle_service import VehicleService


class HomeFrame(ctk.CTkFrame):
    """Tela inicial com status e ações rápidas."""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.service: Optional[VehicleService] = None
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Título
        self.title = ctk.CTkLabel(
            self,
            text="Bem-vindo ao Movi Exporter",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="w")
        
        # Subtítulo
        self.subtitle = ctk.CTkLabel(
            self,
            text="Exportação automatizada de dados de veículos Wialon",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 30), sticky="w")
        
        # Cards de status
        self._create_status_cards()
        
        # Ações rápidas
        self._create_quick_actions()
    
    def _create_status_cards(self):
        """Cria os cards de status."""
        cards_frame = ctk.CTkFrame(self)
        cards_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Card: Conexão Wialon
        self.wialon_card = StatusCard(
            cards_frame,
            title="Wialon API",
            value="Verificando...",
        )
        self.wialon_card.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Card: Veículos
        self.vehicles_card = StatusCard(
            cards_frame,
            title="Veículos",
            value="--",
        )
        self.vehicles_card.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Card: Google Drive
        self.drive_card = StatusCard(
            cards_frame,
            title="Google Drive",
            value="Verificando...",
        )
        self.drive_card.grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        # Verificar status em background
        self._check_status_async()
    
    def _create_quick_actions(self):
        """Cria botões de ações rápidas."""
        actions_label = ctk.CTkLabel(
            self,
            text="Ações Rápidas",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        actions_label.grid(row=3, column=0, columnspan=2, pady=(20, 10), sticky="w")
        
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=4, column=0, columnspan=2, sticky="ew")
        
        # Botão: Testar Conexão
        self.btn_test = ctk.CTkButton(
            actions_frame,
            text="🔄  Testar Conexões",
            width=200,
            height=45,
            command=self._check_status_async
        )
        self.btn_test.grid(row=0, column=0, padx=5, pady=5)
        
        # Botão: Listar Veículos
        self.btn_list = ctk.CTkButton(
            actions_frame,
            text="📋  Ver Veículos",
            width=200,
            height=45,
            command=self._show_vehicles
        )
        self.btn_list.grid(row=0, column=1, padx=5, pady=5)
    
    def _check_status_async(self):
        """Verifica status das conexões em background."""
        def check():
            # Wialon
            try:
                self.service = VehicleService()
                wialon_ok = self.service.test_connection()
                
                self.after(0, lambda: self.wialon_card.set_value(
                    "Conectado ✅" if wialon_ok else "Desconectado ❌",
                    "success" if wialon_ok else "error"
                ))
                
                # Veículos (se conectou)
                if wialon_ok:
                    vehicles = self.service.list_vehicles()
                    self.after(0, lambda: self.vehicles_card.set_value(
                        str(len(vehicles)),
                        "success"
                    ))
                else:
                    self.after(0, lambda: self.vehicles_card.set_value("--", "error"))
                    
            except Exception as e:
                self.after(0, lambda: self.wialon_card.set_value("Erro ❌", "error"))
                self.after(0, lambda: self.vehicles_card.set_value("--", "error"))
            
            # Google Drive
            try:
                from src.services.uploader import DriveUploader
                uploader = DriveUploader()
                drive_ok = uploader.test_connection()
                
                self.after(0, lambda: self.drive_card.set_value(
                    "Conectado ✅" if drive_ok else "Não configurado",
                    "success" if drive_ok else "warning"
                ))
            except Exception:
                self.after(0, lambda: self.drive_card.set_value("Não configurado", "warning"))
        
        thread = threading.Thread(target=check, daemon=True)
        thread.start()
    
    def _show_vehicles(self):
        """Mostra lista de veículos em uma janela."""
        if not self.service:
            return
        
        try:
            vehicles = self.service.list_vehicles()
            
            # Criar janela de listagem
            window = ctk.CTkToplevel(self)
            window.title("Veículos Disponíveis")
            window.geometry("600x400")
            window.transient(self.winfo_toplevel())
            
            # Textbox com lista
            textbox = ctk.CTkTextbox(window, width=560, height=350)
            textbox.pack(padx=20, pady=20, fill="both", expand=True)
            
            # Header
            header = f"{'ID':>12} | {'Nome':<30} | {'Placa':<15}\n"
            header += "=" * 60 + "\n"
            textbox.insert("end", header)
            
            # Dados
            for v in vehicles:
                line = f"{v['id']:>12} | {v['name']:<30} | {v.get('plate', ''):<15}\n"
                textbox.insert("end", line)
            
            textbox.insert("end", f"\nTotal: {len(vehicles)} veículos")
            textbox.configure(state="disabled")
            
        except Exception as e:
            self._show_error(f"Erro ao listar veículos: {e}")
    
    def _show_error(self, message: str):
        """Mostra mensagem de erro."""
        dialog = ctk.CTkInputDialog(text=message, title="Erro")


class StatusCard(ctk.CTkFrame):
    """Card de status reutilizável."""
    
    def __init__(self, master, title: str, value: str, icon: str = "", **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        
        # Ícone + Título
        header = ctk.CTkLabel(
            self,
            text=f"{icon}  {title}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        header.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        # Valor
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.value_label.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")
    
    def set_value(self, value: str, status: str = "normal"):
        """Atualiza o valor do card."""
        self.value_label.configure(text=value)
        
        colors = {
            "success": "#2ecc71",
            "error": "#e74c3c",
            "warning": "#f39c12",
            "normal": None
        }
        
        color = colors.get(status)
        if color:
            self.value_label.configure(text_color=color)
