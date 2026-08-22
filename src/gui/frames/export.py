"""
Tela de Exportação.

Exibe configurações de exportação e log de progresso em tempo real
capturando mensagens do loguru durante o processamento.
"""

import threading
from collections import namedtuple
from datetime import datetime
from pathlib import Path
from tkinter import messagebox
from typing import Callable, List, Optional

import customtkinter as ctk

from src.core.config import settings
from src.core.logger import GUILogHandler, logger
from src.core.service_factory import build_vehicle_service
from src.gui import icons
from src.gui.account_state import AccountState
from src.gui.components import toast
from src.gui.design import Colors, Font, Space
from src.gui.system_utils import open_system_folder
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

# Parâmetros de exportação lidos dos widgets (na thread da GUI) e repassados
# ao worker em background.
_ExportParams = namedtuple(
    "_ExportParams",
    "month year format_type consolidated upload include_addresses vehicle_ids",
)


class ExportFrame(ctk.CTkFrame):
    """Tela de configuração e execução de exportação."""

    # Cores do log por nível, como pares [claro, escuro] — a tag do tkinter
    # aceita só uma cor, então resolvemos a do tema atual em _configure_log_tags.
    # No claro, INFO era branco e sumia no fundo claro (bug reportado).
    LOG_COLORS = {
        "DEBUG": ["#7A7A7A", "#888888"],
        "INFO": ["#1A1A1A", "#DCE4EE"],  # texto principal — adapta ao tema
        "SUCCESS": ["#1E8E4E", "#4CAF50"],
        "WARNING": ["#B26A00", "#FFC107"],
        "ERROR": ["#C62828", "#F44336"],
        "CRITICAL": ["#C62828", "#FF5722"],
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
        # Sinaliza o pedido de cancelamento do export em andamento (botão Parar).
        self._cancel_event = threading.Event()

        # Configurar grid. A área central (row 3) alterna entre a vista de
        # Veículos e a de Progresso (mesma célula) via o segmented no row 2.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.title = ctk.CTkLabel(
            self, text="Exportar Dados", font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title.grid(row=0, column=0, pady=(0, 20), sticky="w")

        self._create_config_section()
        self._create_view_toggle()
        self._create_vehicles_section()
        self._create_progress_section()
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

        # --- Linha 2: sub-card "Opções" agrupando os checkboxes (#13) ---
        options_card = ctk.CTkFrame(config_frame)
        options_card.grid(
            row=2, column=0, columnspan=4, padx=10, pady=(4, 12), sticky="ew"
        )

        ctk.CTkLabel(
            options_card,
            text="OPÇÕES",
            font=ctk.CTkFont(size=Font.SIZE_SM, weight=Font.WEIGHT_BOLD),
            text_color=Colors.MUTED,
        ).grid(
            row=0, column=0, columnspan=2, padx=Space.MD, pady=(Space.SM, 2), sticky="w"
        )

        self.consolidated_var = ctk.BooleanVar(value=True)
        self.consolidated_check = ctk.CTkCheckBox(
            options_card,
            text="Gerar arquivo consolidado",
            variable=self.consolidated_var,
        )
        self.consolidated_check.grid(
            row=1, column=0, padx=Space.MD, pady=(0, Space.SM), sticky="w"
        )

        self.upload_var = ctk.BooleanVar(value=False)
        self.upload_check = ctk.CTkCheckBox(
            options_card,
            text="Upload para Google Drive",
            variable=self.upload_var,
        )
        self.upload_check.grid(
            row=1, column=1, padx=Space.MD, pady=(0, Space.SM), sticky="w"
        )

        # Geocodificação é opt-in: adiciona chamadas de API e tempo ao export.
        self.include_addresses_var = ctk.BooleanVar(value=False)
        self.include_addresses_check = ctk.CTkCheckBox(
            options_card,
            text="Incluir endereço (mais lento)",
            variable=self.include_addresses_var,
        )
        self.include_addresses_check.grid(
            row=2, column=0, columnspan=2, padx=Space.MD, pady=(0, Space.SM), sticky="w"
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
        self._selection = {}
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
        return build_vehicle_service(account=self._account())

    def _create_view_toggle(self):
        """Alternador entre a vista de seleção de veículos e a de progresso.

        As duas vistas dividem a mesma célula do grid (row 3); só uma aparece
        por vez. Ao iniciar um export, trocamos para 'Progresso' e ficamos lá.
        """
        self.view_var = ctk.StringVar(value="Veículos")
        self.view_toggle = ctk.CTkSegmentedButton(
            self,
            values=["Veículos", "Progresso"],
            variable=self.view_var,
            command=self._switch_view,
        )
        self.view_toggle.grid(row=2, column=0, sticky="w", pady=(0, 12))

    def _show_view(self, value: str) -> None:
        """Troca a vista programaticamente (mantém o segmented em sincronia)."""
        self.view_var.set(value)
        self._switch_view(value)

    def _switch_view(self, value: str) -> None:
        """Mostra a vista pedida ('Veículos' ou 'Progresso') e esconde a outra."""
        if value == "Progresso":
            self.vehicles_frame.grid_remove()
            self.progress_frame.grid()
        else:
            self.progress_frame.grid_remove()
            self.vehicles_frame.grid()

    # Tamanho do lote renderizado por vez. A lista carrega mais ao rolar (scroll
    # infinito) — renderizar tudo de uma vez congelava a GUI com 800+ veículos.
    _MAX_RENDER = 120

    def _create_vehicles_section(self):
        """Vista 'Veículos': modo (todos / manual), busca e lista rolável.

        Estado de seleção (`self._selection`: id→bool) é separado da renderização:
        a lista carrega em lotes ao rolar (scroll infinito), o que mantém a tela
        fluida mesmo com milhares de veículos.
        """
        self.vehicles_frame = ctk.CTkFrame(self)
        self.vehicles_frame.grid(row=3, column=0, sticky="nsew")
        self.vehicles_frame.grid_columnconfigure(0, weight=1)
        self.vehicles_frame.grid_rowconfigure(2, weight=1)  # a lista ocupa o resto

        # --- Linha 0: modo (radios) + Carregar ---
        mode_row = ctk.CTkFrame(self.vehicles_frame, fg_color="transparent")
        mode_row.grid(row=0, column=0, padx=12, pady=(12, 4), sticky="ew")
        mode_row.grid_columnconfigure(2, weight=1)

        self.all_vehicles_var = ctk.BooleanVar(value=True)
        self.all_radio = ctk.CTkRadioButton(
            mode_row,
            text="Todos os veículos",
            variable=self.all_vehicles_var,
            value=True,
            command=self._toggle_vehicle_selection,
        )
        self.all_radio.grid(row=0, column=0, padx=(0, 16), pady=4, sticky="w")

        self.specific_radio = ctk.CTkRadioButton(
            mode_row,
            text="Escolher manualmente",
            variable=self.all_vehicles_var,
            value=False,
            command=self._toggle_vehicle_selection,
        )
        self.specific_radio.grid(row=0, column=1, padx=0, pady=4, sticky="w")

        self.load_btn = ctk.CTkButton(
            mode_row,
            text=" Carregar",
            image=icons.get(icons.REFRESH, size=16, on_accent=True),
            width=110,
            command=self._load_vehicles,
        )
        self.load_btn.grid(row=0, column=3, padx=0, pady=4, sticky="e")

        # --- Linha 1: busca + ações em massa (discretas) + contador ---
        # Só visível no modo "Escolher manualmente".
        self.vehicles_toolbar = ctk.CTkFrame(
            self.vehicles_frame, fg_color="transparent"
        )
        self.vehicles_toolbar.grid(row=1, column=0, padx=12, pady=(0, 6), sticky="ew")
        self.vehicles_toolbar.grid_columnconfigure(0, weight=1)

        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._on_search_changed())
        self.search_entry = ctk.CTkEntry(
            self.vehicles_toolbar,
            textvariable=self.search_var,
            placeholder_text="🔍  Buscar por nome, placa ou ID",
        )
        self.search_entry.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        # Ações em massa como texto discreto (não competem com a lista).
        self.mark_all_btn = ctk.CTkButton(
            self.vehicles_toolbar,
            text="Marcar todos",
            width=120,
            fg_color="transparent",
            hover=False,
            text_color=Colors.PRIMARY,
            command=lambda: self._set_filtered_selection(True),
        )
        self.mark_all_btn.grid(row=0, column=1, padx=0)

        self.unmark_all_btn = ctk.CTkButton(
            self.vehicles_toolbar,
            text="Limpar todos",
            width=120,
            fg_color="transparent",
            hover=False,
            text_color=Colors.MUTED,
            command=lambda: self._set_filtered_selection(False),
        )
        self.unmark_all_btn.grid(row=0, column=2, padx=(0, 10))

        self.selection_count_label = ctk.CTkLabel(
            self.vehicles_toolbar,
            text="",
            font=ctk.CTkFont(size=Font.SIZE_SM, weight=Font.WEIGHT_BOLD),
        )
        self.selection_count_label.grid(row=0, column=3, padx=0)

        # --- Linha 2: lista rolável (ocupa o espaço restante da vista) ---
        self.vehicles_scroll = ctk.CTkScrollableFrame(self.vehicles_frame)
        self.vehicles_scroll.grid(row=2, column=0, padx=12, pady=(0, 12), sticky="nsew")
        self.vehicles_scroll.grid_columnconfigure((0, 1), weight=1)
        self._wire_infinite_scroll()

        # Estado: seleção por id (fonte da verdade), checkboxes e cache do filtro.
        self._selection: dict[int, bool] = {}
        self.vehicle_checkboxes: dict[int, ctk.CTkCheckBox] = {}
        self._matches: list[dict] = []  # resultado do filtro atual
        self._rendered_count = 0  # quantos itens do filtro já estão na tela

        # Começa escondido (modo "Todos" é o default).
        self.vehicles_toolbar.grid_remove()
        self.vehicles_scroll.grid_remove()

    def _wire_infinite_scroll(self) -> None:
        """Carrega o próximo lote quando o scroll chega perto do fim.

        Envolve o `yscrollcommand` do canvas interno do CTkScrollableFrame para
        detectar a posição (pega tanto a roda do mouse quanto arrastar a barra).
        """
        try:
            scroll_set = self.vehicles_scroll._scrollbar.set

            def _on_yscroll(first, last):
                scroll_set(first, last)
                if float(last) >= 0.985:
                    self.after_idle(self._maybe_load_more)

            self.vehicles_scroll._parent_canvas.configure(yscrollcommand=_on_yscroll)
        except Exception as e:
            logger.debug(f"Scroll infinito indisponível: {e}")

    def _create_progress_section(self):
        """Cria seção de log de progresso."""
        # Mesma célula (row 3) da vista de Veículos — alternadas pelo segmented.
        # Começa escondida (a vista padrão é 'Veículos').
        self.progress_frame = progress_frame = ctk.CTkFrame(self)
        progress_frame.grid(row=3, column=0, sticky="nsew")
        progress_frame.grid_columnconfigure(0, weight=1)
        progress_frame.grid_rowconfigure(1, weight=1)
        progress_frame.grid_remove()

        # Header com título, contador e toolbar do log (#17)
        header_frame = ctk.CTkFrame(progress_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="ew")
        header_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header_frame, text="Progresso:", font=ctk.CTkFont(weight="bold")
        ).grid(row=0, column=0, sticky="w")

        self.progress_label = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=Colors.MUTED,
        )
        self.progress_label.grid(row=0, column=1, sticky="e", padx=(0, Space.SM))

        # Toolbar: limpar · copiar · salvar o log (útil p/ suporte).
        toolbar = ctk.CTkFrame(header_frame, fg_color="transparent")
        toolbar.grid(row=0, column=2, sticky="e")
        ctk.CTkButton(
            toolbar,
            text="",
            image=icons.get(icons.TRASH, size=14),
            width=30,
            command=self._clear_log,
        ).grid(row=0, column=0, padx=2)
        ctk.CTkButton(
            toolbar,
            text="",
            image=icons.get(icons.COPY, size=14),
            width=30,
            command=self._copy_log,
        ).grid(row=0, column=1, padx=2)
        ctk.CTkButton(
            toolbar,
            text="",
            image=icons.get(icons.SAVE, size=14),
            width=30,
            command=self._save_log,
        ).grid(row=0, column=2, padx=2)

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
        """Configura as tags de cor do log conforme o tema atual.

        Reaplicar as tags atualiza retroativamente o texto já inserido (o
        tkinter recolore tudo que usa a tag), então chamar isto após uma troca
        de tema corrige logs antigos também. Índice 0 = claro, 1 = escuro.
        """
        idx = 0 if ctk.get_appearance_mode() == "Light" else 1
        text_widget = self.log_text._textbox
        for level, pair in self.LOG_COLORS.items():
            text_widget.tag_configure(level, foreground=pair[idx])

    def _create_action_buttons(self):
        """Cria botões de ação."""
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.grid(row=4, column=0, sticky="e")

        self.open_folder_btn = ctk.CTkButton(
            actions_frame,
            text="  Abrir pasta",
            image=icons.get(icons.FOLDER_OPEN, size=18, on_accent=True),
            width=140,
            height=45,
            command=self._open_export_folder,
        )
        self.open_folder_btn.grid(row=0, column=0, padx=5)

        self.export_btn = ctk.CTkButton(
            actions_frame,
            text="  Iniciar Exportação",
            image=icons.get(icons.PLAY, size=18, on_accent=True),
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._start_export,
        )
        self.export_btn.grid(row=0, column=1, padx=5)
        # Cores originais do botão (tema) — para restaurar após o estado 'Parar'.
        self._export_btn_fg = self.export_btn.cget("fg_color")
        self._export_btn_hover = self.export_btn.cget("hover_color")

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
            open_system_folder(path)
        except Exception as e:
            logger.debug(f"Erro ao abrir pasta: {e}")
            messagebox.showerror("Erro", f"Não foi possível abrir a pasta: {e}")

    def _toggle_vehicle_selection(self):
        """Alterna visibilidade da barra de seleção de veículos."""
        if self.all_vehicles_var.get():
            self.vehicles_toolbar.grid_remove()
            self.vehicles_scroll.grid_remove()
        else:
            self.vehicles_toolbar.grid()
            self.vehicles_scroll.grid()
            if not self.vehicles:
                self._load_vehicles()
            else:
                self._render_vehicle_list()

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
                self.after(
                    0, lambda: self.load_btn.configure(state="normal", text=" Carregar")
                )

        thread = threading.Thread(target=load, daemon=True)
        thread.start()

    def _populate_vehicle_list(self):
        """Inicializa o estado de seleção após carregar os veículos.

        Default: nenhum marcado (#15) — quem quer todos usa o radio "Todos os
        veículos". O usuário marca só os que precisa, podendo buscar antes.
        """
        self._selection = {vehicle["id"]: False for vehicle in self.vehicles}
        self._log(f"{len(self.vehicles)} veículos carregados", "SUCCESS")
        self._render_vehicle_list()

    def _vehicle_label(self, vehicle: dict) -> str:
        """Texto do checkbox: nome; placa só quando difere do nome.

        Muitos veículos são cadastrados com o nome igual à placa — mostrar
        "ABC1234 · ABC1234" só polui. Nesse caso, exibe só o nome.
        """
        name = str(vehicle.get("name") or "").strip()
        plate = (vehicle.get("plate") or "").strip()
        if plate and plate != name:
            return f"{name}  ·  {plate}"
        return name

    def _matches_search(self, vehicle: dict, query: str) -> bool:
        """True se o veículo casa com a busca (nome, placa ou id)."""
        if not query:
            return True
        haystack = f"{vehicle.get('name', '')} {vehicle.get('plate', '')} {vehicle.get('id', '')}".lower()
        return query in haystack

    def _on_search_changed(self):
        """Nova busca recomeça a renderização do primeiro lote."""
        self._render_vehicle_list()

    def _render_vehicle_list(self):
        """Renderiza o filtro atual do zero (primeiro lote); o resto vem ao rolar.

        Renderizar em lotes evita o congelamento que existia ao montar centenas
        de checkboxes de uma vez. `_maybe_load_more` acrescenta os próximos
        conforme o usuário rola (scroll infinito).
        """
        for widget in self.vehicles_scroll.winfo_children():
            widget.destroy()
        self.vehicle_checkboxes.clear()

        query = self.search_var.get().strip().lower()
        self._matches = [
            vehicle for vehicle in self.vehicles if self._matches_search(vehicle, query)
        ]
        self._rendered_count = 0
        self._append_next_batch()

        self._update_bulk_button_labels()
        self._update_selection_count()
        # Se o primeiro lote não encheu a viewport, segue carregando até encher.
        self.after(60, self._fill_if_short)

    def _append_next_batch(self):
        """Acrescenta o próximo lote de checkboxes ao fim da lista (sem recriar)."""
        start = self._rendered_count
        end = min(start + self._MAX_RENDER, len(self._matches))
        for i in range(start, end):
            vehicle = self._matches[i]
            vid = vehicle["id"]
            var = ctk.BooleanVar(value=self._selection.get(vid, False))
            cb = ctk.CTkCheckBox(
                self.vehicles_scroll,
                text=self._vehicle_label(vehicle),
                variable=var,
                command=lambda vid=vid, var=var: self._on_checkbox_toggle(vid, var),
            )
            cb.grid(row=i // 2, column=i % 2, padx=5, pady=2, sticky="w")
            self.vehicle_checkboxes[vid] = cb
        self._rendered_count = end

    def _maybe_load_more(self):
        """Carrega o próximo lote se o scroll chegou perto do fim."""
        if self._rendered_count >= len(self._matches):
            return
        try:
            last = self.vehicles_scroll._parent_canvas.yview()[1]
        except Exception:
            last = 1.0
        if last >= 0.97:
            self._append_next_batch()

    def _fill_if_short(self):
        """Garante itens suficientes para a lista poder rolar (caso lote curto)."""
        if self._rendered_count >= len(self._matches):
            return
        try:
            last = self.vehicles_scroll._parent_canvas.yview()[1]
        except Exception:
            return
        # yview retorna (0.0, 1.0) quando não há o que rolar → carrega mais.
        if last >= 0.999:
            self._append_next_batch()
            self.after(60, self._fill_if_short)

    def _on_checkbox_toggle(self, vid: int, var: "ctk.BooleanVar"):
        """Atualiza o estado de seleção quando um checkbox é marcado/desmarcado."""
        self._selection[vid] = bool(var.get())
        self._update_selection_count()

    def _set_filtered_selection(self, value: bool):
        """Marca/desmarca todos os veículos que casam com a busca atual."""
        query = self.search_var.get().strip().lower()
        for vehicle in self.vehicles:
            if self._matches_search(vehicle, query):
                self._selection[vehicle["id"]] = value
        # Reflete nos checkboxes visíveis sem recriar tudo.
        for vid, cb in self.vehicle_checkboxes.items():
            if isinstance(vid, int) and isinstance(cb, ctk.CTkCheckBox):
                cb.select() if self._selection.get(vid) else cb.deselect()
        self._update_selection_count()

    def _update_selection_count(self):
        """Atualiza o rótulo 'X de Y selecionados' (+ nº no filtro, se buscando)."""
        total = len(self._selection)
        marcados = sum(1 for sel in self._selection.values() if sel)
        query = self.search_var.get().strip().lower()
        if query:
            filtrados = sum(
                1 for vehicle in self.vehicles if self._matches_search(vehicle, query)
            )
            self.selection_count_label.configure(
                text=f"{marcados} de {total} selecionados · {filtrados} no filtro"
            )
        else:
            self.selection_count_label.configure(
                text=f"{marcados} de {total} selecionados"
            )

    def _update_bulk_button_labels(self):
        """Deixa explícito o alvo dos botões: 'todos' sem busca, 'filtrados' com.

        Com uma busca ativa, marcar/desmarcar agem só sobre os resultados — o
        que diferencia do modo 'Todos os veículos' (radio) e remove a ambiguidade.
        """
        if self.search_var.get().strip():
            self.mark_all_btn.configure(text="Marcar filtrados")
            self.unmark_all_btn.configure(text="Limpar filtrados")
        else:
            self.mark_all_btn.configure(text="Marcar todos")
            self.unmark_all_btn.configure(text="Limpar todos")

    def _get_selected_vehicle_ids(self) -> Optional[List[int]]:
        """Retorna IDs dos veículos selecionados ou None para todos."""
        if self.all_vehicles_var.get():
            return None

        selected = [vid for vid, sel in self._selection.items() if sel]
        return selected if selected else None

    def _start_export(self):
        """Inicia a exportação em background (após validação e confirmação)."""
        if self.is_exporting:
            return
        if not self._has_valid_selection():
            return

        params = self._read_export_params()
        if not self._confirm_export(params):
            return

        self._prepare_export_ui()
        self._log_export_params(params)
        self._setup_log_handler()

        thread = threading.Thread(target=self._run_export, args=(params,), daemon=True)
        thread.start()

    def _confirm_export(self, params: "_ExportParams") -> bool:
        """Mostra um resumo e pede confirmação antes de iniciar (#3).

        Barreira barata contra export com mês/formato/seleção errados — não
        toca no serviço, só confirma a intenção.
        """
        if params.vehicle_ids:
            alvo = f"{len(params.vehicle_ids)} veículo(s) selecionado(s)"
        else:
            alvo = "Todos os veículos"
        resumo = (
            f"Mês/Ano:  {MESES[params.month - 1]} / {params.year}\n"
            f"Formato:  {params.format_type}\n"
            f"Veículos:  {alvo}\n"
            f"Consolidado:  {'sim' if params.consolidated else 'não'}\n"
            f"Incluir endereço:  {'sim' if params.include_addresses else 'não'}\n"
            f"Upload Google Drive:  {'sim' if params.upload else 'não'}\n\n"
            "Iniciar a exportação?"
        )
        return messagebox.askyesno("Confirmar exportação", resumo)

    def _has_valid_selection(self) -> bool:
        """No modo 'Selecionar veículos', exige ao menos um marcado (#15e).

        Evita rodar um export que não faz nada — avisa e aborta se nada marcado.
        """
        if not self.all_vehicles_var.get() and not any(self._selection.values()):
            messagebox.showwarning(
                "Nenhum veículo selecionado",
                "Marque ao menos um veículo ou escolha 'Todos os veículos'.",
            )
            return False
        return True

    def _prepare_export_ui(self) -> None:
        """Prepara a UI ao iniciar: troca para a vista Progresso (#2), o botão
        por 'Parar' (#3) e mostra a barra de progresso (#27)."""
        self.is_exporting = True
        self._cancel_event.clear()
        self._show_view("Progresso")
        # O botão de ação vira 'Parar' (cinza) e passa a cancelar o export.
        self.export_btn.configure(
            text="  Parar",
            image=icons.get(icons.CIRCLE_XMARK, size=18, on_accent=True),
            fg_color=Colors.MUTED,
            hover_color="#6d6d6d",
            command=self._request_cancel,
        )
        self.progress_bar.grid()
        self.progress_bar.set(0)
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        self._clear_log()
        self.progress_label.configure(text="Iniciando...")

    def _request_cancel(self) -> None:
        """Pede o cancelamento do export em andamento (botão 'Parar')."""
        self._cancel_event.set()
        self.export_btn.configure(text="  Parando...", state="disabled")
        self.progress_label.configure(text="Cancelando...")
        self._log(
            "⏹️  Cancelamento solicitado — encerrando após o veículo atual...",
            "WARNING",
        )

    def _read_export_params(self) -> "_ExportParams":
        """Lê os parâmetros de exportação dos widgets (na thread da GUI)."""
        return _ExportParams(
            month=MESES.index(self.month_var.get()) + 1,
            year=int(self.year_var.get()),
            format_type=self.format_var.get(),
            consolidated=self.consolidated_var.get(),
            upload=self.upload_var.get(),
            include_addresses=self.include_addresses_var.get(),
            vehicle_ids=self._get_selected_vehicle_ids(),
        )

    def _log_export_params(self, params: "_ExportParams") -> None:
        """Loga o cabeçalho do export (período, formato, veículos)."""
        self._log(f"📅 Exportando: {params.month:02d}/{params.year}", "INFO")
        self._log(f"📁 Formato: {params.format_type}", "INFO")
        if params.include_addresses:
            self._log("📍 Endereço: incluído (geocodificação ativada)", "INFO")
        if params.vehicle_ids:
            self._log(f"🚗 Veículos selecionados: {len(params.vehicle_ids)}", "INFO")
        else:
            self._log("🚗 Todos os veículos", "INFO")
        self._log("", "INFO")

    def _run_export(self, params: "_ExportParams") -> None:
        """Worker em background: constrói o serviço, roda o export e trata o resultado."""
        try:
            if not self.service:
                self.service = self._build_service()

            # Subpasta por conta só quando há duas contas configuradas.
            account_name = self._account_label() if settings.WIALON_TOKEN_2 else None

            result = self.service.export_monthly_data(
                month=params.month,
                year=params.year,
                vehicle_ids=params.vehicle_ids,
                export_format=params.format_type,
                consolidated=params.consolidated,
                upload_to_drive=params.upload,
                include_addresses=params.include_addresses,
                on_progress=self._on_export_progress,
                account_name=account_name,
                should_cancel=self._cancel_event.is_set,
            )

            if result.cancelled:
                self._handle_export_cancelled(result)
            else:
                self.after(0, self._set_progress_complete)
                if result.total_records == 0:
                    self._handle_export_no_data(result)
                else:
                    self._handle_export_success(result)

        except Exception as e:
            self._log(f"\n❌ Erro na exportação: {e}", "ERROR")
            if self.status_callback:
                self.status_callback(f"Erro: {e}", "error")
        finally:
            self._teardown_log_handler()
            self.after(0, self._reset_export_button)

    def _handle_export_no_data(self, result) -> None:
        """Processou veículos mas nenhum dado no período — destaca isso (#32).

        "Taxa de sucesso 100%" com 0 registros confunde; sinalizamos a
        não-entrega e sugerimos a causa provável.
        """
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
        self.after(0, lambda: self.progress_label.configure(text="Sem dados"))
        if self.status_callback:
            self.status_callback("Exportação sem dados para o período", "warning")
        self.after(
            0,
            lambda: toast.show("Nenhum dado disponível para o período", kind="warning"),
        )

    def _handle_export_success(self, result) -> None:
        """Loga o resultado final (arquivos, upload, erros) e notifica sucesso."""
        self._log("", "INFO")
        self._log("═" * 50, "SUCCESS")
        self._log("EXPORTAÇÃO CONCLUÍDA", "SUCCESS")
        self._log("═" * 50, "SUCCESS")
        self._log(
            f"Veículos: {result.processed_vehicles}/{result.total_vehicles}", "INFO"
        )
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
            self.status_callback(
                f"Exportação concluída: {result.processed_vehicles} veículos", "success"
            )
        self.after(
            0,
            lambda: toast.show(
                f"Exportação concluída — {result.total_records} registros",
                kind="success",
            ),
        )

    def _handle_export_cancelled(self, result) -> None:
        """Export interrompido pelo usuário — informa o parcial já gerado."""
        self.after(0, lambda: self.progress_label.configure(text="Cancelado"))
        self._log("", "WARNING")
        self._log("═" * 50, "WARNING")
        self._log("⏹️  EXPORTAÇÃO CANCELADA", "WARNING")
        self._log("═" * 50, "WARNING")
        self._log(
            f"Processados antes de parar: "
            f"{result.processed_vehicles}/{result.total_vehicles}",
            "INFO",
        )
        if result.exported_files:
            self._log(
                f"Arquivos parciais gerados: {len(result.exported_files)} "
                "(consolidado e upload não foram executados)",
                "INFO",
            )
        if self.status_callback:
            self.status_callback("Exportação cancelada", "warning")
        self.after(0, lambda: toast.show("Exportação cancelada", kind="warning"))

    def _on_export_progress(self, current: int, total: int, vehicle_name: str):
        """Callback chamado pelo serviço a cada veículo (thread de trabalho).

        Na primeira chamada, troca a barra indeterminada (pulsando) por uma
        barra determinada e passa a refletir a fração real (atual/total).
        """

        def update():
            # Primeira vez: para o "pulsar" e vira barra de progresso real.
            if self.progress_bar.cget("mode") != "determinate":
                self.progress_bar.stop()
                self.progress_bar.configure(mode="determinate")
            fraction = current / total if total else 0
            self.progress_bar.set(fraction)
            self.progress_label.configure(
                text=f"Processando {current}/{total} — {vehicle_name}"
            )

        self.after(0, update)

    def _set_progress_complete(self):
        """Define a barra de progresso como completa."""
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1)
        self.progress_label.configure(text="Concluído")

    def _reset_export_button(self):
        """Restaura o botão para 'Iniciar Exportação' (a vista fica em Progresso)."""
        self.is_exporting = False
        self.export_btn.configure(
            state="normal",
            text="  Iniciar Exportação",
            image=icons.get(icons.PLAY, size=18, on_accent=True),
            fg_color=self._export_btn_fg,
            hover_color=self._export_btn_hover,
            command=self._start_export,
        )
        # Garante que a barra de progresso está parada e a esconde (#27).
        try:
            self.progress_bar.stop()
            self.progress_bar.configure(mode="determinate")
            self.progress_bar.grid_remove()
        except Exception as e:
            logger.debug(f"Erro ao resetar barra de progresso: {e}")

    def _clear_log(self):
        """Limpa o textbox de log (thread-safe via after).

        Reaplica as tags de cor para acompanhar o tema atual — assim, se o
        usuário trocou de tema, o próximo log já sai com as cores corretas.
        """

        def _do():
            self.log_text.delete("1.0", "end")
            self._configure_log_tags()

        self.after(0, _do)

    def _copy_log(self):
        """Copia todo o texto do log para a área de transferência."""
        conteudo = self.log_text.get("1.0", "end").strip()
        if not conteudo:
            return
        self.clipboard_clear()
        self.clipboard_append(conteudo)
        toast.show("Log copiado", kind="success")

    def _save_log(self):
        """Salva o log num arquivo .txt escolhido pelo usuário."""
        from tkinter import filedialog

        conteudo = self.log_text.get("1.0", "end").strip()
        if not conteudo:
            toast.show("Log vazio — nada para salvar", kind="warning")
            return
        path = filedialog.asksaveasfilename(
            title="Salvar log",
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt")],
            initialfile="movi-exporter-log.txt",
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(conteudo)
            toast.show("Log salvo", kind="success")
        except Exception as e:
            logger.debug(f"Erro ao salvar log: {e}")
            messagebox.showerror("Erro", f"Não foi possível salvar o log: {e}")

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
