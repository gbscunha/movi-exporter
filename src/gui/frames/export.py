"""
Tela de Exportação.
"""

import customtkinter as ctk
import threading
from datetime import datetime
from typing import Callable, Optional, List

from src.services.vehicle_service import VehicleService


class ExportFrame(ctk.CTkFrame):
    """Tela de configuração e execução de exportação."""
    
    def __init__(self, master, status_callback: Optional[Callable] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.status_callback = status_callback
        self.service: Optional[VehicleService] = None
        self.vehicles: List[dict] = []
        self.is_exporting = False
        
        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Título
        self.title = ctk.CTkLabel(
            self,
            text="Exportar Dados",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title.grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        # Configurações
        self._create_config_section()
        
        # Seleção de veículos
        self._create_vehicles_section()
        
        # Log de progresso
        self._create_progress_section()
        
        # Botões de ação
        self._create_action_buttons()
    
    def _create_config_section(self):
        """Cria seção de configuração."""
        config_frame = ctk.CTkFrame(self)
        config_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        config_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Mês
        ctk.CTkLabel(config_frame, text="Mês:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        now = datetime.now()
        default_month = now.month - 1 if now.month > 1 else 12
        
        self.month_var = ctk.StringVar(value=str(default_month))
        self.month_menu = ctk.CTkOptionMenu(
            config_frame,
            values=[str(i) for i in range(1, 13)],
            variable=self.month_var,
            width=80
        )
        self.month_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Ano
        ctk.CTkLabel(config_frame, text="Ano:").grid(row=0, column=2, padx=10, pady=10, sticky="w")
        
        default_year = now.year if now.month > 1 else now.year - 1
        
        self.year_var = ctk.StringVar(value=str(default_year))
        self.year_entry = ctk.CTkEntry(config_frame, textvariable=self.year_var, width=80)
        self.year_entry.grid(row=0, column=3, padx=10, pady=10, sticky="w")
        
        # Formato
        ctk.CTkLabel(config_frame, text="Formato:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        
        self.format_var = ctk.StringVar(value="xlsx")
        self.format_menu = ctk.CTkOptionMenu(
            config_frame,
            values=["csv", "xlsx", "both"],
            variable=self.format_var,
            width=100
        )
        self.format_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Opções
        self.consolidated_var = ctk.BooleanVar(value=True)
        self.consolidated_check = ctk.CTkCheckBox(
            config_frame,
            text="Gerar arquivo consolidado",
            variable=self.consolidated_var
        )
        self.consolidated_check.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky="w")
        
        # Upload Drive
        self.upload_var = ctk.BooleanVar(value=False)
        self.upload_check = ctk.CTkCheckBox(
            config_frame,
            text="Upload para Google Drive",
            variable=self.upload_var
        )
        self.upload_check.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")
    
    def _create_vehicles_section(self):
        """Cria seção de seleção de veículos."""
        vehicles_frame = ctk.CTkFrame(self)
        vehicles_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        vehicles_frame.grid_columnconfigure(1, weight=1)
        
        # Label
        ctk.CTkLabel(
            vehicles_frame,
            text="Veículos:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Opção: Todos ou Específicos
        self.all_vehicles_var = ctk.BooleanVar(value=True)
        
        self.all_radio = ctk.CTkRadioButton(
            vehicles_frame,
            text="Todos os veículos",
            variable=self.all_vehicles_var,
            value=True,
            command=self._toggle_vehicle_selection
        )
        self.all_radio.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        self.specific_radio = ctk.CTkRadioButton(
            vehicles_frame,
            text="Selecionar veículos",
            variable=self.all_vehicles_var,
            value=False,
            command=self._toggle_vehicle_selection
        )
        self.specific_radio.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        
        # Botão carregar
        self.load_btn = ctk.CTkButton(
            vehicles_frame,
            text="🔄 Carregar",
            width=100,
            command=self._load_vehicles
        )
        self.load_btn.grid(row=0, column=3, padx=10, pady=10)
        
        # Lista de veículos (scrollable)
        self.vehicles_scroll = ctk.CTkScrollableFrame(vehicles_frame, height=120)
        self.vehicles_scroll.grid(row=1, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        self.vehicles_scroll.grid_remove()  # Escondido inicialmente
        
        self.vehicle_checkboxes: dict[int, ctk.CTkCheckBox] = {}
    
    def _create_progress_section(self):
        """Cria seção de log de progresso."""
        progress_frame = ctk.CTkFrame(self)
        progress_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 15))
        progress_frame.grid_columnconfigure(0, weight=1)
        progress_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(
            progress_frame,
            text="Progresso:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.log_text = ctk.CTkTextbox(progress_frame, height=150)
        self.log_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        # Barra de progresso
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)
    
    def _create_action_buttons(self):
        """Cria botões de ação."""
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=4, column=0, sticky="e")
        
        self.export_btn = ctk.CTkButton(
            actions_frame,
            text="▶️  Iniciar Exportação",
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._start_export
        )
        self.export_btn.grid(row=0, column=0, padx=5)
    
    def _toggle_vehicle_selection(self):
        """Alterna visibilidade da lista de veículos."""
        if self.all_vehicles_var.get():
            self.vehicles_scroll.grid_remove()
        else:
            self.vehicles_scroll.grid()
            if not self.vehicles:
                self._load_vehicles()
    
    def _load_vehicles(self):
        """Carrega lista de veículos."""
        self.load_btn.configure(state="disabled", text="Carregando...")
        
        def load():
            try:
                if not self.service:
                    self.service = VehicleService()
                
                self.vehicles = self.service.list_vehicles()
                self.after(0, self._populate_vehicle_list)
                
            except Exception as e:
                self.after(0, lambda: self._log(f"❌ Erro ao carregar veículos: {e}"))
            finally:
                self.after(0, lambda: self.load_btn.configure(state="normal", text="🔄 Carregar"))
        
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def _populate_vehicle_list(self):
        """Popula a lista de veículos com checkboxes."""
        # Limpar checkboxes existentes
        for widget in self.vehicles_scroll.winfo_children():
            widget.destroy()
        self.vehicle_checkboxes.clear()
        
        # Criar checkboxes
        for i, v in enumerate(self.vehicles):
            var = ctk.BooleanVar(value=True)
            cb = ctk.CTkCheckBox(
                self.vehicles_scroll,
                text=f"{v['name']} ({v.get('plate', 'N/A')})",
                variable=var
            )
            cb.grid(row=i // 3, column=i % 3, padx=5, pady=2, sticky="w")
            self.vehicle_checkboxes[v['id']] = cb
        
        self._log(f"✅ {len(self.vehicles)} veículos carregados")
    
    def _get_selected_vehicle_ids(self) -> Optional[List[int]]:
        """Retorna IDs dos veículos selecionados ou None para todos."""
        if self.all_vehicles_var.get():
            return None
        
        selected = []
        for vid, cb in self.vehicle_checkboxes.items():
            if cb.get():
                selected.append(vid)
        
        return selected if selected else None
    
    def _start_export(self):
        """Inicia a exportação."""
        if self.is_exporting:
            return
        
        self.is_exporting = True
        self.export_btn.configure(state="disabled", text="⏳ Exportando...")
        self.progress_bar.set(0)
        self.log_text.delete("1.0", "end")
        
        # Parâmetros
        month = int(self.month_var.get())
        year = int(self.year_var.get())
        format_type = self.format_var.get()
        consolidated = self.consolidated_var.get()
        upload = self.upload_var.get()
        vehicle_ids = self._get_selected_vehicle_ids()
        
        self._log(f"📅 Exportando: {month:02d}/{year}")
        self._log(f"📁 Formato: {format_type}")
        
        def export():
            try:
                if not self.service:
                    self.service = VehicleService()
                
                self._log("🔌 Conectando ao Wialon...")
                
                result = self.service.export_monthly_data(
                    month=month,
                    year=year,
                    vehicle_ids=vehicle_ids,
                    export_format=format_type,
                    consolidated=consolidated,
                    upload_to_drive=upload,
                )
                
                self.after(0, lambda: self.progress_bar.set(1))
                
                # Resultado
                self._log("")
                self._log("=" * 50)
                self._log("✅ EXPORTAÇÃO CONCLUÍDA")
                self._log("=" * 50)
                self._log(f"Veículos: {result.processed_vehicles}/{result.total_vehicles}")
                self._log(f"Registros: {result.total_records}")
                self._log(f"Taxa de sucesso: {result.success_rate:.1f}%")
                
                if result.exported_files:
                    self._log("")
                    self._log("Arquivos gerados:")
                    for f in result.exported_files:
                        self._log(f"  📄 {f}")
                
                if result.errors:
                    self._log("")
                    self._log("Erros:")
                    for e in result.errors:
                        self._log(f"  ❌ {e}")
                
                if self.status_callback:
                    self.status_callback(f"Exportação concluída: {result.processed_vehicles} veículos", "success")
                
            except Exception as e:
                self._log(f"\n❌ Erro na exportação: {e}")
                if self.status_callback:
                    self.status_callback(f"Erro: {e}", "error")
            finally:
                self.after(0, self._reset_export_button)
        
        thread = threading.Thread(target=export, daemon=True)
        thread.start()
    
    def _reset_export_button(self):
        """Reseta o estado do botão de exportação."""
        self.is_exporting = False
        self.export_btn.configure(state="normal", text="▶️  Iniciar Exportação")
    
    def _log(self, message: str):
        """Adiciona mensagem ao log."""
        def update():
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
        
        self.after(0, update)
