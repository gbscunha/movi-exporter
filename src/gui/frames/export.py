"""
Tela de Exportação.

Exibe configurações de exportação e log de progresso em tempo real
capturando mensagens do loguru durante o processamento.
"""

import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
from typing import Callable, List, Optional

import customtkinter as ctk

from src.clients.wialon_client import WialonClient
from src.core.config import settings
from src.core.logger import GUILogHandler, logger
from src.gui.account_state import AccountState
from src.services.vehicle_service import VehicleService

# Nomes dos meses em português brasileiro — usados no dropdown.
MESES = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]


class ExportFrame(ctk.CTkFrame):
    """Tela de configuração e execução de exportação."""
    
    # Cores para diferentes níveis de log
    LOG_COLORS = {
        "DEBUG": "#888888",
        "INFO": "#FFFFFF",
        "SUCCESS": "#4CAF50",
        "WARNING": "#FFC107",
        "ERROR": "#F44336",
        "CRITICAL": "#FF5722",
    }
    
    def __init__(
        self,
        master,
        status_callback: Optional[Callable] = None,
        account_state: Optional[AccountState] = None,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.status_callback = status_callback
        self.account_state = account_state
        self.service: Optional[VehicleService] = None
        self.vehicles: List[dict] = []
        self.is_exporting = False
        self._log_handler: Optional[GUILogHandler] = None

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

        # Reage à troca de conta feita na sidebar (estado global).
        if self.account_state is not None:
            self.account_state.register(self._on_account_changed)
    
    def _create_config_section(self):
        """Cria seção de configuração.

        Layout em grid 4 colunas (label | campo | label | campo), linhas:
          linha 0: Mês        | Ano
          linha 1: Formato
          linha 2: Opções (checkboxes)

        O seletor de conta vive na sidebar (estado global), não mais aqui.
        """
        config_frame = ctk.CTkFrame(self)
        config_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        config_frame.grid_columnconfigure((1, 3), weight=1)

        now = datetime.now()

        # --- Linha 0: Mês | Ano ---
        ctk.CTkLabel(config_frame, text="Mês:").grid(
            row=0, column=0, padx=(10, 6), pady=10, sticky="w"
        )
        # Default: mês anterior (relatórios geralmente são do mês fechado).
        default_month_idx = (now.month - 2) % 12  # zero-based
        self.month_var = ctk.StringVar(value=MESES[default_month_idx])
        self.month_menu = ctk.CTkOptionMenu(
            config_frame,
            values=MESES,
            variable=self.month_var,
            width=140,
        )
        self.month_menu.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="w")

        ctk.CTkLabel(config_frame, text="Ano:").grid(
            row=0, column=2, padx=(10, 6), pady=10, sticky="w"
        )
        # Ano como dropdown dos últimos 5 anos — evita digitação inválida (#12).
        default_year = now.year if now.month > 1 else now.year - 1
        year_values = [str(default_year - i) for i in range(5)]
        self.year_var = ctk.StringVar(value=str(default_year))
        self.year_menu = ctk.CTkOptionMenu(
            config_frame,
            values=year_values,
            variable=self.year_var,
            width=100,
        )
        self.year_menu.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="w")

        # --- Linha 1: Formato | Conta ---
        ctk.CTkLabel(config_frame, text="Formato:").grid(
            row=1, column=0, padx=(10, 6), pady=10, sticky="w"
        )
        self.format_var = ctk.StringVar(value="xlsx")
        self.format_menu = ctk.CTkOptionMenu(
            config_frame,
            values=["csv", "xlsx", "both"],
            variable=self.format_var,
            width=140,
        )
        self.format_menu.grid(row=1, column=1, padx=(0, 10), pady=10, sticky="w")

        # --- Linha 2: Opções (checkboxes) ---
        self.consolidated_var = ctk.BooleanVar(value=True)
        self.consolidated_check = ctk.CTkCheckBox(
            config_frame,
            text="Gerar arquivo consolidado",
            variable=self.consolidated_var,
        )
        self.consolidated_check.grid(
            row=2, column=0, columnspan=2, padx=10, pady=(4, 12), sticky="w"
        )

        self.upload_var = ctk.BooleanVar(value=False)
        self.upload_check = ctk.CTkCheckBox(
            config_frame,
            text="Upload para Google Drive",
            variable=self.upload_var,
        )
        self.upload_check.grid(
            row=2, column=2, columnspan=2, padx=10, pady=(4, 12), sticky="w"
        )

    def _on_account_changed(self, account: int):
        """Reage à troca de conta global feita na sidebar.

        Limpa o serviço/veículos em cache (forçando reautenticação com o token
        correto) e o log. Se o usuário estava no modo "Selecionar veículos",
        recarrega a lista automaticamente para não deixar a tela "presa" com
        veículos da conta anterior (#04).
        """
        self.service = None
        self.vehicles = []
        for widget in self.vehicles_scroll.winfo_children():
            widget.destroy()
        self.vehicle_checkboxes.clear()
        # Limpa o log para não misturar mensagens de contas diferentes (#25).
        self._clear_log()
        self._log(f"Conta alterada para {self._account_label()}.", "INFO")

        # Auto-load se o usuário está escolhendo veículos manualmente (#04).
        if not self.all_vehicles_var.get():
            self._load_vehicles()

    def _account(self) -> int:
        """Conta selecionada (1 ou 2), do estado global."""
        return self.account_state.account if self.account_state else 1

    def _account_label(self) -> str:
        """Nome humano da conta selecionada."""
        return self.account_state.label if self.account_state else "Conta 1"

    def _build_service(self) -> VehicleService:
        """Cria um VehicleService usando o token da conta selecionada."""
        if self._account() == 2 and settings.WIALON_TOKEN_2:
            client = WialonClient(token=settings.WIALON_TOKEN_2)
            return VehicleService(client=client)
        return VehicleService()
    
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
        
        # Header com título e contador
        header_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header_frame,
            text="Progresso:",
            font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, sticky="w")
        
        self.progress_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#888888"
        )
        self.progress_label.grid(row=0, column=1, sticky="e")
        
        self.log_text = ctk.CTkTextbox(progress_frame, height=200)
        self.log_text.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        # Configurar tags de cores para diferentes níveis de log
        # CTkTextbox usa tkinter Text internamente
        self._configure_log_tags()
        
        # Barra de progresso — escondida quando não há export rodando (#27).
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)
        self.progress_bar.grid_remove()  # idle: oculta
    
    def _configure_log_tags(self):
        """Configura tags de cor para o textbox."""
        # Acessa o widget tkinter interno do CTkTextbox
        text_widget = self.log_text._textbox
        for level, color in self.LOG_COLORS.items():
            text_widget.tag_configure(level, foreground=color)
    
    def _create_action_buttons(self):
        """Cria botões de ação."""
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=4, column=0, sticky="e")

        self.open_folder_btn = ctk.CTkButton(
            actions_frame,
            text="📂  Abrir pasta",
            width=140,
            height=45,
            command=self._open_export_folder,
        )
        self.open_folder_btn.grid(row=0, column=0, padx=5)

        self.export_btn = ctk.CTkButton(
            actions_frame,
            text="▶️  Iniciar Exportação",
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._start_export,
        )
        self.export_btn.grid(row=0, column=1, padx=5)

    def _open_export_folder(self):
        """Abre a pasta de exportação do mês/ano atualmente selecionados.

        Se a subpasta do mês ainda não existir, abre o diretório base.
        """
        try:
            month = MESES.index(self.month_var.get()) + 1
            year = int(self.year_var.get())
        except (ValueError, IndexError):
            messagebox.showerror("Erro", "Mês/ano inválidos.")
            return

        base = Path(settings.EXPORT_DIR or "./exports")
        target = base / f"{year}-{month:02d}"
        path = target if target.exists() else base
        path.mkdir(parents=True, exist_ok=True)

        try:
            if sys.platform == "win32":
                subprocess.Popen(["explorer", str(path)])
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except Exception as e:
            logger.debug(f"Erro ao abrir pasta: {e}")
            messagebox.showerror("Erro", f"Não foi possível abrir a pasta: {e}")
    
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
        # Limpa o log para não acumular mensagens de carregamentos anteriores (#25).
        self._clear_log()
        self._log("🔌 Conectando ao Wialon...", "INFO")
        
        def load():
            try:
                if not self.service:
                    self.service = self._build_service()

                self._log("📡 Buscando lista de veículos...", "INFO")
                self.vehicles = self.service.list_vehicles()
                self.after(0, self._populate_vehicle_list)
                
            except Exception as e:
                self._log(f"Erro ao carregar veículos: {e}", "ERROR")
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
        
        self._log(f"{len(self.vehicles)} veículos carregados", "SUCCESS")
    
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
        # Mostra a barra de progresso durante o export (#27).
        self.progress_bar.grid()
        self.progress_bar.set(0)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        self._clear_log()
        self.progress_label.configure(text="Iniciando...")
        
        # Parâmetros
        month = MESES.index(self.month_var.get()) + 1
        year = int(self.year_var.get())
        format_type = self.format_var.get()
        consolidated = self.consolidated_var.get()
        upload = self.upload_var.get()
        vehicle_ids = self._get_selected_vehicle_ids()
        
        self._log(f"📅 Exportando: {month:02d}/{year}", "INFO")
        self._log(f"📁 Formato: {format_type}", "INFO")
        if vehicle_ids:
            self._log(f"🚗 Veículos selecionados: {len(vehicle_ids)}", "INFO")
        else:
            self._log("🚗 Todos os veículos", "INFO")
        self._log("", "INFO")
        
        # Registra handler de logs para capturar output do serviço
        self._setup_log_handler()
        
        def export():
            try:
                if not self.service:
                    self.service = self._build_service()

                # Subpasta por conta só quando há duas contas configuradas.
                account_name = (
                    self._account_label() if settings.WIALON_TOKEN_2 else None
                )

                result = self.service.export_monthly_data(
                    month=month,
                    year=year,
                    vehicle_ids=vehicle_ids,
                    export_format=format_type,
                    consolidated=consolidated,
                    upload_to_drive=upload,
                    account_name=account_name,
                )
                
                # Para barra de progresso e define como completo
                self.after(0, self._set_progress_complete)

                # Caso especial: processou veículos mas nenhum dado no período.
                # "Taxa de sucesso 100%" com 0 registros confunde — destacamos
                # que não houve entrega e sugerimos a causa provável (#32).
                if result.total_records == 0:
                    self._log("", "WARNING")
                    self._log("═" * 50, "WARNING")
                    self._log("⚠️  NENHUM DADO DISPONÍVEL PARA O PERÍODO", "WARNING")
                    self._log("═" * 50, "WARNING")
                    self._log(
                        f"Veículos processados: {result.processed_vehicles}/{result.total_vehicles}",
                        "INFO",
                    )
                    self._log("Possíveis causas:", "INFO")
                    self._log("  • Veículos inativos no período selecionado", "INFO")
                    self._log("  • Limite de retenção de histórico da conta Wialon", "INFO")
                    self._log("  • Mês/ano muito antigos", "INFO")
                    self.after(
                        0, lambda: self.progress_label.configure(text="Sem dados")
                    )
                    if self.status_callback:
                        self.status_callback(
                            "Exportação sem dados para o período", "warning"
                        )
                else:
                    # Resultado final
                    self._log("", "INFO")
                    self._log("═" * 50, "SUCCESS")
                    self._log("EXPORTAÇÃO CONCLUÍDA", "SUCCESS")
                    self._log("═" * 50, "SUCCESS")
                    self._log(f"Veículos: {result.processed_vehicles}/{result.total_vehicles}", "INFO")
                    self._log(f"Registros: {result.total_records}", "INFO")
                    self._log(f"Taxa de sucesso: {result.success_rate:.1f}%", "INFO")

                    if result.exported_files:
                        self._log("", "INFO")
                        self._log("Arquivos gerados:", "INFO")
                        for f in result.exported_files:
                            self._log(f"  📄 {f}", "SUCCESS")

                    if result.upload_result:
                        ur = result.upload_result
                        self._log("", "INFO")
                        self._log(f"Upload: {ur.uploaded_files}/{ur.total_files} arquivos", "INFO")

                    if result.errors:
                        self._log("", "WARNING")
                        self._log("Erros:", "WARNING")
                        for e in result.errors:
                            self._log(f"  {e}", "ERROR")

                    if self.status_callback:
                        self.status_callback(f"Exportação concluída: {result.processed_vehicles} veículos", "success")
                
            except Exception as e:
                self._log(f"\n❌ Erro na exportação: {e}", "ERROR")
                if self.status_callback:
                    self.status_callback(f"Erro: {e}", "error")
            finally:
                self._teardown_log_handler()
                self.after(0, self._reset_export_button)
        
        thread = threading.Thread(target=export, daemon=True)
        thread.start()
    
    def _set_progress_complete(self):
        """Define a barra de progresso como completa."""
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1)
        self.progress_label.configure(text="Concluído")
    
    def _reset_export_button(self):
        """Reseta o estado do botão de exportação."""
        self.is_exporting = False
        self.export_btn.configure(state="normal", text="▶️  Iniciar Exportação")
        # Garante que a barra de progresso está parada e a esconde (#27).
        try:
            self.progress_bar.stop()
            self.progress_bar.configure(mode="determinate")
            self.progress_bar.grid_remove()
        except Exception as e:
            logger.debug(f"Erro ao resetar barra de progresso: {e}")

    def _clear_log(self):
        """Limpa o textbox de log (thread-safe via after)."""
        self.after(0, lambda: self.log_text.delete("1.0", "end"))
    
    def _log(self, message: str, level: str = "INFO"):
        """
        Adiciona mensagem ao log com cor baseada no nível.
        
        Args:
            message: Texto a exibir
            level: Nível do log (DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL)
        """
        def update():
            text_widget = self.log_text._textbox
            # Insere texto com tag de cor
            text_widget.insert("end", message + "\n", level)
            self.log_text.see("end")
        
        self.after(0, update)
    
    def _setup_log_handler(self):
        """Configura handler para capturar logs do loguru."""
        def on_log(message: str, level: str):
            self._log(message, level)
        
        self._log_handler = GUILogHandler(callback=on_log, min_level="INFO")
        self._log_handler.register()
    
    def _teardown_log_handler(self):
        """Remove handler de logs."""
        if self._log_handler:
            self._log_handler.unregister()
            self._log_handler = None
