"""
Tela inicial (Home).
"""

import threading
from datetime import datetime
from pathlib import Path
from typing import Optional

import customtkinter as ctk

from src.core.config import settings
from src.core.logger import logger
from src.core.service_factory import build_vehicle_service
from src.gui import icons
from src.gui.account_state import AccountState
from src.gui.design import Border, Colors, Font, Space
from src.gui.frames.export import MESES  # nomes dos meses (fonte única)
from src.gui.system_utils import open_system_folder
from src.services import export_history
from src.services.vehicle_service import VehicleService


class HomeFrame(ctk.CTkFrame):
    """Tela inicial com status e ações rápidas."""

    def __init__(self, master, account_state: Optional[AccountState] = None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.account_state = account_state
        self.service: Optional[VehicleService] = None

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
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

        # Resumo de exportações (última exportação, sugestão, stats do ano)
        self._create_export_summary()

        # Verificar status em background. Importante chamar DEPOIS dos botões
        # serem criados — `_check_status_async` desabilita `btn_list` enquanto
        # roda (#05).
        self._check_status_async()

        # Reage à troca de conta na sidebar: revalida status com o novo token.
        if self.account_state is not None:
            self.account_state.register(self._on_account_changed)

    def _on_account_changed(self, _account: int):
        """Recarrega o status e o resumo quando a conta global muda.

        `_check_status_async` recria o `self.service` do zero, que por sua vez
        usa o token da conta agora ativa (resolvido em `_build_service`).
        """
        self.service = None
        self._check_status_async()
        self._refresh_export_summary()

    def _active_account_label(self) -> Optional[str]:
        """Label da conta ativa para filtrar exports, ou None (conta única).

        Só faz sentido filtrar por conta quando há uma segunda conta
        configurada — caso contrário os exports ficam direto na pasta do mês.
        """
        if self.account_state is not None and settings.WIALON_TOKEN_2:
            return self.account_state.label
        return None
    
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
        
        # Card: Google Drive
        self.drive_card = StatusCard(
            cards_frame,
            title="Google Drive",
            value="Verificando...",
        )
        self.drive_card.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Card: Veículos
        self.vehicles_card = StatusCard(
            cards_frame,
            title="Veículos",
            value="--",
        )
        self.vehicles_card.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

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
            text="  Testar Conexões",
            image=icons.get(icons.REFRESH, size=18, on_accent=True),
            width=200,
            height=45,
            command=self._check_status_async
        )
        self.btn_test.grid(row=0, column=0, padx=5, pady=5)

        # Botão: Listar Veículos. Começa desabilitado e é habilitado quando
        # _check_status_async conclui — evita o silent fail relatado no QA
        # quando o usuário clica antes do boot terminar (#05).
        self.btn_list = ctk.CTkButton(
            actions_frame,
            text="  Ver Veículos",
            image=icons.get(icons.LIST, size=18, on_accent=True),
            width=200,
            height=45,
            command=self._show_vehicles,
            state="disabled",
        )
        self.btn_list.grid(row=0, column=1, padx=5, pady=5)

    # Resumo de exportações (#07)
    def _create_export_summary(self):
        """Cria a seção 'Resumo de Exportações' e a popula."""
        label = ctk.CTkLabel(
            self,
            text="Resumo de Exportações",
            font=ctk.CTkFont(size=Font.SIZE_LG, weight=Font.WEIGHT_BOLD),
        )
        label.grid(row=5, column=0, columnspan=2, pady=(Space.XL, Space.SM), sticky="w")

        self.summary_frame = ctk.CTkFrame(self, corner_radius=Border.RADIUS_MD)
        self.summary_frame.grid(row=6, column=0, columnspan=2, sticky="ew")
        self.summary_frame.grid_columnconfigure(0, weight=1)

        self._refresh_export_summary()

    def _refresh_export_summary(self):
        """Recarrega o conteúdo do resumo lendo as pastas de export."""
        for widget in self.summary_frame.winfo_children():
            widget.destroy()

        base = settings.EXPORT_DIR or "./exports"
        account = self._active_account_label()
        last = export_history.last_export(base, account)

        row = 0
        if last is None:
            ctk.CTkLabel(
                self.summary_frame,
                text="Nenhuma exportação realizada ainda.",
                text_color=Colors.MUTED,
            ).grid(row=row, column=0, padx=Space.LG, pady=Space.LG, sticky="w")
        else:
            # Bloco "Última exportação"
            info = ctk.CTkFrame(self.summary_frame, fg_color="transparent")
            info.grid(row=row, column=0, padx=Space.LG, pady=Space.MD, sticky="ew")
            info.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(
                info,
                text="ÚLTIMA EXPORTAÇÃO",
                font=ctk.CTkFont(size=Font.SIZE_SM, weight=Font.WEIGHT_BOLD),
                text_color=Colors.MUTED,
            ).grid(row=0, column=0, sticky="w")

            periodo = f"{MESES[last.month - 1]}/{last.year}"
            if last.account:
                periodo += f"  ·  {last.account}"
            ctk.CTkLabel(
                info,
                text=periodo,
                font=ctk.CTkFont(size=Font.SIZE_XL, weight=Font.WEIGHT_BOLD),
            ).grid(row=1, column=0, sticky="w")

            quando = last.last_modified.strftime("%d/%m/%Y %H:%M")
            ctk.CTkLabel(
                info,
                text=f"{last.file_count} arquivo(s)  ·  {quando}",
                font=ctk.CTkFont(size=Font.SIZE_BASE),
                text_color=Colors.MUTED,
            ).grid(row=2, column=0, sticky="w")

            ctk.CTkButton(
                info,
                text="  Abrir pasta",
                image=icons.get(icons.FOLDER_OPEN, size=16, on_accent=True),
                width=130,
                command=lambda p=last.folder: self._open_folder(p),
            ).grid(row=0, column=1, rowspan=3, padx=(Space.LG, 0))
            row += 1

        # Sugestão de mês não exportado
        suggestion = export_history.suggest_unexported_month(
            base, datetime.now(), account
        )
        if suggestion is not None:
            sy, sm = suggestion
            ctk.CTkLabel(
                self.summary_frame,
                text=f"Você ainda não exportou {MESES[sm - 1]}/{sy}.",
                image=icons.get(icons.TRIANGLE_WARNING, size=14, color=Colors.WARNING),
                compound="left",
                text_color=Colors.WARNING,
                font=ctk.CTkFont(size=Font.SIZE_BASE),
            ).grid(row=row, column=0, padx=Space.LG, pady=(0, Space.SM), sticky="w")
            row += 1

        # Estatísticas do ano corrente
        ano = datetime.now().year
        n_exports, n_files = export_history.year_stats(base, ano, account)
        if n_exports:
            stats = f"Em {ano}: {n_exports} exportação(ões), {n_files} arquivo(s)."
            ctk.CTkLabel(
                self.summary_frame,
                text=stats,
                font=ctk.CTkFont(size=Font.SIZE_BASE),
                text_color=Colors.MUTED,
            ).grid(row=row, column=0, padx=Space.LG, pady=(0, Space.MD), sticky="w")

    def _open_folder(self, path):
        """Abre uma pasta no explorador de arquivos do sistema."""
        path = Path(path)
        if not path.exists():
            return
        try:
            open_system_folder(path)
        except Exception as e:
            logger.debug(f"Erro ao abrir pasta: {e}")

    def _build_service(self) -> VehicleService:
        """Cria um VehicleService usando o token da conta selecionada."""
        account = self.account_state.account if self.account_state is not None else 1
        return build_vehicle_service(account=account)

    def _check_status_async(self):
        """Verifica status das conexões em background."""
        # Desabilita "Ver Veículos" enquanto reinicializa — habilitamos
        # de volta no fim do worker (com ou sem sucesso, contanto que
        # exista um service utilizável para o botão).
        self.btn_list.configure(state="disabled")

        def check():
            wialon_ok = False
            # Wialon
            try:
                self.service = self._build_service()
                wialon_ok = self.service.test_connection()

                self.after(0, lambda: self.wialon_card.set_value(
                    "Conectado" if wialon_ok else "Desconectado",
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

            except Exception:
                self.after(0, lambda: self.wialon_card.set_value("Erro", "error"))
                self.after(0, lambda: self.vehicles_card.set_value("--", "error"))

            # Google Drive
            try:
                from src.services.uploader import DriveUploader
                uploader = DriveUploader()
                drive_ok = uploader.test_connection()

                self.after(0, lambda: self.drive_card.set_value(
                    "Conectado" if drive_ok else "Não configurado",
                    "success" if drive_ok else "warning"
                ))
            except Exception:
                self.after(0, lambda: self.drive_card.set_value("Não configurado", "warning"))

            # Habilita "Ver Veículos" só se a conexão Wialon foi bem sucedida.
            # Se falhou, deixa desabilitado — clicar não levaria a nada útil.
            if wialon_ok:
                self.after(0, lambda: self.btn_list.configure(state="normal"))

        thread = threading.Thread(target=check, daemon=True)
        thread.start()

    def _show_vehicles(self):
        """Mostra lista de veículos em uma janela."""
        # Defesa em profundidade: o botão começa desabilitado e só é habilitado
        # após _check_status_async — mas algum estado inconsistente ainda pode
        # cair aqui, então tratamos explicitamente.
        if not self.service:
            self._show_warning(
                "Conexão ainda inicializando. Aguarde alguns segundos e tente novamente."
            )
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
        import tkinter.messagebox as mb
        mb.showerror("Erro", message)

    def _show_warning(self, message: str):
        """Mostra aviso (warning, não erro)."""
        import tkinter.messagebox as mb
        mb.showwarning("Aviso", message)


class StatusCard(ctk.CTkFrame):
    """Card de status reutilizável.

    Hierarquia tipográfica: rótulo discreto em maiúsculas (muted, pequeno) e
    valor como protagonista (grande, bold). Cores e espaçamentos vêm dos
    design tokens (Fase 04).
    """

    def __init__(self, master, title: str, value: str, icon: str = "", **kwargs):
        super().__init__(master, corner_radius=Border.RADIUS_MD, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        # Rótulo — discreto, maiúsculas para diferenciar do valor.
        label_text = f"{icon}  {title.upper()}" if icon else title.upper()
        header = ctk.CTkLabel(
            self,
            text=label_text,
            font=ctk.CTkFont(size=Font.SIZE_SM, weight=Font.WEIGHT_BOLD),
            text_color=Colors.MUTED,
        )
        header.grid(
            row=0, column=0, padx=Space.LG, pady=(Space.LG, Space.XS), sticky="w"
        )

        # Valor — protagonista do card.
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=ctk.CTkFont(size=Font.SIZE_XL, weight=Font.WEIGHT_BOLD),
        )
        self.value_label.grid(
            row=1, column=0, padx=Space.LG, pady=(0, Space.LG), sticky="w"
        )

    # Mapeia status → (cor, ícone FontAwesome). "normal" não tem ícone.
    _STATUS_STYLE = {
        "success": (Colors.SUCCESS, icons.CIRCLE_CHECK),
        "error": (Colors.ERROR, icons.CIRCLE_XMARK),
        "warning": (Colors.WARNING, icons.TRIANGLE_WARNING),
        "normal": (None, None),
    }

    def set_value(self, value: str, status: str = "normal"):
        """Atualiza o valor do card com cor e ícone semânticos.

        O ícone (verde/vermelho/amarelo) aparece à esquerda do texto, no lugar
        dos emojis inline que existiam antes (✅❌⚠️).
        """
        self.value_label.configure(text=value)

        color, icon = self._STATUS_STYLE.get(status, (None, None))
        if color:
            self.value_label.configure(text_color=color)
        if icon:
            self.value_label.configure(
                image=icons.get(icon, size=18, color=color), compound="left"
            )
        else:
            self.value_label.configure(image=None)
