"""
Tela de Configurações.
"""

import os
import threading
import webbrowser
from tkinter import messagebox

import customtkinter as ctk

from src.core.config import settings
from src.core.env_writer import set_env_value
from src.core.logger import logger
from src.core.service_factory import WialonError, authenticate_token
from src.gui import icons
from src.gui.components import toast
from src.gui.design import Colors

# Página de login do Wialon. Depois de logado, o usuário gera o token
# em Configurações da conta → Aplicações → Tokens.
URL_AUTORIZACAO_WIALON = "https://hosting.wialon.com/login.html"


class SettingsFrame(ctk.CTkFrame):
    """Tela de configurações do aplicativo."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)

        self.title = ctk.CTkLabel(
            self, text="Configurações", font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title.grid(row=0, column=0, pady=(0, 20), sticky="w")

        # Container com scroll para as seções
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.scroll_frame.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Estado dos campos de cada conta — preenchido por _create_wialon_section.
        self._token_widgets: dict[int, dict] = {}

        # Valores atualmente persistidos (baseline) dos campos editáveis sem
        # botão próprio. Comparados com o que está na tela para detectar
        # "alterações não salvas" (#20).
        self._saved_export_dir = settings.EXPORT_DIR or "./exports"
        self._saved_page_size = settings.WIALON_PAGE_SIZE or 1000

        # Seções
        self._create_wialon_section(account=1)
        self._create_wialon_section(account=2)
        self._create_export_section()
        self._create_drive_section()
        self._create_appearance_section()

        # Rodapé fixo com o botão "Salvar alterações" (#20).
        self._create_save_bar()
        self._recompute_dirty()

    def _create_save_bar(self):
        """Cria a barra inferior fixa com o botão 'Salvar alterações'.

        Fica fora do scroll para estar sempre visível. O botão só habilita
        quando há alterações pendentes nos campos sem salvar-próprio
        (diretório de exportação e registros por página).
        """
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=2, column=0, sticky="ew", pady=(4, 0))
        bar.grid_columnconfigure(0, weight=1)

        self.unsaved_label = ctk.CTkLabel(
            bar,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=Colors.WARNING,
            image=icons.get(icons.TRIANGLE_WARNING, size=14, color=Colors.WARNING),
            compound="left",
        )
        self.unsaved_label.grid(row=0, column=0, sticky="e", padx=(0, 12))

        self.save_changes_btn = ctk.CTkButton(
            bar,
            text="  Salvar alterações",
            image=icons.get(icons.SAVE, size=16, on_accent=True),
            width=170,
            command=self._save_changes,
        )
        self.save_changes_btn.grid(row=0, column=1, sticky="e")

    def _env_key_for_account(self, account: int) -> str:
        """Retorna o nome da variável de ambiente para a conta dada (1 ou 2)."""
        return "WIALON_TOKEN" if account == 1 else "WIALON_TOKEN_2"

    def _token_for_account(self, account: int) -> str:
        """Retorna o token atualmente carregado para a conta dada."""
        if account == 1:
            return settings.WIALON_TOKEN or ""
        return settings.WIALON_TOKEN_2 or ""

    def _create_wialon_section(self, account: int = 1):
        """Cria seção de configuração do Wialon para uma das duas contas.

        Permite editar, gerar, salvar e testar o token sem reiniciar o app.
        """
        # Frame da seção
        section = ctk.CTkFrame(self.scroll_frame)
        section.pack(fill="x", pady=(0, 15))
        section.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            section,
            text=f"  Wialon API — Conta {account}",
            image=icons.get(icons.PLUG, size=18),
            compound="left",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        title.grid(row=0, column=0, columnspan=6, padx=15, pady=(15, 10), sticky="w")

        # Linha do token + botões
        ctk.CTkLabel(section, text="Token:").grid(
            row=1, column=0, padx=(15, 10), pady=10, sticky="w"
        )

        entry = ctk.CTkEntry(
            section,
            width=320,
            show="*",
            placeholder_text="Cole seu token Wialon aqui",
        )
        entry.grid(row=1, column=1, padx=(0, 5), pady=10, sticky="we")
        existing = self._token_for_account(account)
        if existing:
            entry.insert(0, existing)

        self._eye_icon = icons.get(icons.EYE, size=16, on_accent=True)
        self._eye_slash_icon = icons.get(icons.EYE_SLASH, size=16, on_accent=True)
        toggle_btn = ctk.CTkButton(
            section,
            text="",
            image=self._eye_icon,
            width=36,
            command=lambda a=account: self._toggle_token_visibility(a),
        )
        toggle_btn.grid(row=1, column=2, padx=2, pady=10)

        open_btn = ctk.CTkButton(
            section,
            text=" Gerar",
            image=icons.get(icons.LINK, size=16, on_accent=True),
            width=90,
            command=self._open_wialon_auth_page,
        )
        open_btn.grid(row=1, column=3, padx=2, pady=10)

        save_btn = ctk.CTkButton(
            section,
            text=" Salvar",
            image=icons.get(icons.SAVE, size=16, on_accent=True),
            width=100,
            command=lambda a=account: self._save_wialon_token(a),
        )
        save_btn.grid(row=1, column=4, padx=2, pady=10)

        test_btn = ctk.CTkButton(
            section,
            text=" Testar",
            image=icons.get(icons.SEARCH, size=16, on_accent=True),
            width=100,
            command=lambda a=account: self._test_wialon_token(a),
        )
        test_btn.grid(row=1, column=5, padx=(2, 15), pady=10)

        # Status. Quando há token salvo mas ainda não testado, usamos amarelo
        # (#28) para chamar atenção que vale clicar em Testar. Sem token, fica
        # cinza neutro (não há o que testar ainda).
        status_label = ctk.CTkLabel(
            section,
            text="",
            font=ctk.CTkFont(size=12),
            compound="left",
        )
        status_label.grid(
            row=2, column=0, columnspan=6, padx=15, pady=(0, 15), sticky="w"
        )

        # Salva referência aos widgets desta conta para uso nos callbacks.
        self._token_widgets[account] = {
            "entry": entry,
            "test_btn": test_btn,
            "toggle_btn": toggle_btn,
            "status_label": status_label,
            "visible": False,
        }

        # Estado inicial do status.
        if existing:
            self._set_token_status(
                account,
                "Status: Não testado — clique em Testar",
                Colors.WARNING,
                icons.TRIANGLE_WARNING,
            )
        else:
            self._set_token_status(account, "Status: sem token configurado", Colors.MUTED)

        # Aliases para compatibilidade com testes/smoke da Fase 10 (Conta 1).
        if account == 1:
            self.token_entry = entry
            self.token_toggle_btn = toggle_btn
            self.token_open_btn = open_btn
            self.token_save_btn = save_btn
            self.token_test_btn = test_btn
            self.token_status_label = status_label

    def _set_token_status(self, account, text, color, icon=None):
        """Atualiza o label de status com texto, cor e (opcional) ícone."""
        widgets = self._token_widgets[account]
        img = icons.get(icon, size=14, color=color) if icon else None
        widgets["status_label"].configure(text=text, text_color=color, image=img)

    def _toggle_token_visibility(self, account: int):
        """Alterna entre mostrar e esconder o token da conta dada."""
        widgets = self._token_widgets[account]
        widgets["visible"] = not widgets["visible"]
        widgets["entry"].configure(show="" if widgets["visible"] else "*")
        # Troca o ícone do botão (olho aberto/riscado) conforme a visibilidade.
        widgets["toggle_btn"].configure(
            image=self._eye_slash_icon if widgets["visible"] else self._eye_icon
        )

    def _open_wialon_auth_page(self):
        """Abre a página de login do Wialon no navegador."""
        webbrowser.open(URL_AUTORIZACAO_WIALON)

    def _save_wialon_token(self, account: int):
        """Grava o token da conta dada no .env e recarrega as configurações."""
        widgets = self._token_widgets[account]
        token = widgets["entry"].get().strip()
        if not token:
            self._set_token_status(
                account, "Cole um token válido antes de salvar.",
                Colors.ERROR, icons.TRIANGLE_WARNING,
            )
            return

        env_key = self._env_key_for_account(account)
        try:
            set_env_value(env_key, token)
            settings.reload()
        except Exception as e:
            logger.debug(f"Erro ao salvar {env_key}: {e}")
            messagebox.showerror("Erro", f"Não foi possível salvar o token: {e}")
            return

        self._set_token_status(
            account, "Status: Token salvo no .env", Colors.SUCCESS, icons.SAVE
        )
        toast.show(f"Token da Conta {account} salvo", kind="success")

    def _test_wialon_token(self, account: int):
        """Testa o token da conta dada chamando authenticate() em background."""
        widgets = self._token_widgets[account]
        token = widgets["entry"].get().strip()
        if not token:
            self._set_token_status(
                account, "Cole um token antes de testar a conexão.",
                Colors.ERROR, icons.TRIANGLE_WARNING,
            )
            return

        self._set_token_status(
            account, "Status: Testando conexão...", Colors.MUTED, icons.REFRESH
        )
        widgets["test_btn"].configure(state="disabled")

        def worker():
            try:
                username = authenticate_token(token)
                self.after(0, self._on_token_test_ok, account, username)
            except WialonError as e:
                self.after(0, self._on_token_test_fail, account, str(e))
            except Exception as e:
                logger.debug(f"Erro inesperado ao testar token: {e}")
                self.after(0, self._on_token_test_fail, account, str(e))

        threading.Thread(target=worker, daemon=True).start()

    def _on_token_test_ok(self, account: int, username: str):
        """Callback executado na thread da GUI após teste bem-sucedido."""
        if username:
            text = f"Status: Conectado como \"{username}\""
        else:
            text = "Status: Conectado"
        self._set_token_status(account, text, Colors.SUCCESS, icons.CIRCLE_CHECK)
        self._token_widgets[account]["test_btn"].configure(state="normal")

    def _on_token_test_fail(self, account: int, error: str):
        """Callback executado na thread da GUI após teste falhar."""
        self._set_token_status(
            account, f"Status: Falha — {error}", Colors.ERROR, icons.CIRCLE_XMARK
        )
        self._token_widgets[account]["test_btn"].configure(state="normal")

    def _create_export_section(self):
        """Cria seção de configuração de exportação."""
        section = ctk.CTkFrame(self.scroll_frame)
        section.pack(fill="x", pady=(0, 15))
        section.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            section, text="  Exportação", image=icons.get(icons.FOLDER, size=18),
            compound="left", font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 10), sticky="w")

        # Diretório de exportação
        ctk.CTkLabel(section, text="Diretório:").grid(
            row=1, column=0, padx=(15, 10), pady=10, sticky="w"
        )

        export_dir = settings.EXPORT_DIR or "./exports"

        self.export_dir_entry = ctk.CTkEntry(section, width=350)
        self.export_dir_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.export_dir_entry.insert(0, export_dir)
        # Cor de borda padrão, para restaurar após um erro de validação.
        self._entry_default_border = self.export_dir_entry.cget("border_color")
        # Recalcula "alterações não salvas" a cada tecla digitada.
        self.export_dir_entry.bind("<KeyRelease>", lambda _e: self._recompute_dirty())

        self.browse_btn = ctk.CTkButton(
            section, text="", image=icons.get(icons.FOLDER_OPEN, size=16, on_accent=True),
            width=40, command=self._browse_export_dir
        )
        self.browse_btn.grid(row=1, column=2, padx=(5, 4), pady=10)

        # Ponto laranja indicando que este campo tem alteração não salva (#20).
        self.export_dir_dot = ctk.CTkLabel(
            section, text="●", text_color=Colors.WARNING,
            font=ctk.CTkFont(size=16), width=16,
        )
        self.export_dir_dot.grid(row=1, column=3, padx=(0, 15), pady=10)
        self.export_dir_dot.grid_remove()  # escondido até haver alteração

        # Erro de validação inline, abaixo do campo (#21).
        self.export_dir_error = ctk.CTkLabel(
            section, text="", text_color=Colors.ERROR, font=ctk.CTkFont(size=12),
            compound="left",
        )
        self.export_dir_error.grid(
            row=2, column=1, columnspan=3, padx=10, pady=(0, 4), sticky="w"
        )
        self.export_dir_error.grid_remove()

        # Page size — slider de 100 a 5000 (passo 100) em vez de campo de
        # texto livre, evitando valores inválidos (#18).
        ctk.CTkLabel(section, text="Registros por página:").grid(
            row=3, column=0, padx=(15, 10), pady=(10, 15), sticky="w"
        )

        page_size = settings.WIALON_PAGE_SIZE or 1000

        slider_row = ctk.CTkFrame(section, fg_color="transparent")
        slider_row.grid(row=3, column=1, columnspan=3, padx=10, pady=(10, 15), sticky="w")

        self.page_size_var = ctk.IntVar(value=page_size)
        self.page_size_slider = ctk.CTkSlider(
            slider_row,
            from_=100,
            to=5000,
            number_of_steps=49,  # (5000-100)/100
            variable=self.page_size_var,
            width=240,
            command=self._on_page_size_change,
        )
        self.page_size_slider.grid(row=0, column=0, padx=(0, 12))

        self.page_size_value_label = ctk.CTkLabel(
            slider_row, text=str(page_size), width=50, font=ctk.CTkFont(weight="bold")
        )
        self.page_size_value_label.grid(row=0, column=1)

        self.page_size_dot = ctk.CTkLabel(
            slider_row, text="●", text_color=Colors.WARNING,
            font=ctk.CTkFont(size=16), width=16,
        )
        self.page_size_dot.grid(row=0, column=2, padx=(8, 0))
        self.page_size_dot.grid_remove()

    def _on_page_size_change(self, value: float):
        """Atualiza o label numérico ao arrastar o slider de page size."""
        self.page_size_value_label.configure(text=str(int(value)))
        self._recompute_dirty()

    def _recompute_dirty(self):
        """Recalcula campos alterados e atualiza pontos + botão do rodapé (#20)."""
        dir_changed = self.export_dir_entry.get().strip() != self._saved_export_dir
        size_changed = int(self.page_size_var.get()) != self._saved_page_size

        self._toggle_dot(self.export_dir_dot, dir_changed)
        self._toggle_dot(self.page_size_dot, size_changed)

        # Some que o campo voltou a ser válido enquanto o usuário digita.
        if self.export_dir_entry.get().strip():
            self.export_dir_error.grid_remove()
            self.export_dir_entry.configure(border_color=self._entry_default_border)

        any_changed = dir_changed or size_changed
        self.save_changes_btn.configure(state="normal" if any_changed else "disabled")
        self.unsaved_label.configure(
            text="Você tem alterações não salvas" if any_changed else ""
        )

    @staticmethod
    def _toggle_dot(dot, show: bool):
        """Mostra/esconde um ponto-indicador de alteração."""
        if show:
            dot.grid()
        else:
            dot.grid_remove()

    def _save_changes(self):
        """Valida e persiste diretório de exportação e registros por página (#20/#21)."""
        from src.gui.validation import validate_export_dir

        export_dir = self.export_dir_entry.get().strip()
        error = validate_export_dir(export_dir)
        if error:
            self.export_dir_error.configure(text=error)
            self.export_dir_error.grid()
            self.export_dir_entry.configure(border_color=Colors.ERROR)
            return

        self.export_dir_error.grid_remove()
        self.export_dir_entry.configure(border_color=self._entry_default_border)

        page_size = int(self.page_size_var.get())
        try:
            set_env_value("EXPORT_DIR", export_dir)
            set_env_value("WIALON_PAGE_SIZE", str(page_size))
            settings.reload()
        except Exception as e:
            logger.debug(f"Erro ao salvar configurações: {e}")
            messagebox.showerror("Erro", f"Não foi possível salvar: {e}")
            return

        self._saved_export_dir = export_dir
        self._saved_page_size = page_size
        self._recompute_dirty()
        toast.show("Configurações salvas", kind="success")

    def _create_drive_section(self):
        """Cria seção de configuração do Google Drive."""
        section = ctk.CTkFrame(self.scroll_frame)
        section.pack(fill="x", pady=(0, 15))
        section.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            section, text="  Google Drive", image=icons.get(icons.CLOUD, size=18),
            compound="left", font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 10), sticky="w")

        # Arquivo de credenciais
        ctk.CTkLabel(section, text="Credenciais:").grid(
            row=1, column=0, padx=(15, 10), pady=10, sticky="w"
        )

        creds_file = settings.GOOGLE_DRIVE_CREDENTIALS_FILE or "./client_secrets.json"
        file_exists = os.path.exists(creds_file)

        status = "Encontrado" if file_exists else "Não encontrado"
        status_color = Colors.SUCCESS if file_exists else Colors.ERROR
        status_icon = icons.CIRCLE_CHECK if file_exists else icons.CIRCLE_XMARK

        self.creds_label = ctk.CTkLabel(
            section,
            text=f"{creds_file} ({status})",
            text_color=status_color,
            image=icons.get(status_icon, size=14, color=status_color),
            compound="left",
        )
        self.creds_label.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        # ID da pasta no Drive — mostrado por completo (não é segredo) com
        # botões de copiar e abrir no navegador (#29).
        ctk.CTkLabel(section, text="ID da pasta no Drive:").grid(
            row=2, column=0, padx=(15, 10), pady=(10, 15), sticky="w"
        )

        folder_id = settings.GOOGLE_DRIVE_FOLDER_ID or ""

        self.folder_entry = ctk.CTkEntry(
            section, width=300, placeholder_text="ID da pasta no Google Drive"
        )
        self.folder_entry.grid(row=2, column=1, padx=10, pady=(10, 15), sticky="w")
        if folder_id:
            self.folder_entry.insert(0, folder_id)

        self.folder_copy_btn = ctk.CTkButton(
            section, text="", image=icons.get(icons.COPY, size=16, on_accent=True),
            width=40, command=self._copy_folder_id
        )
        self.folder_copy_btn.grid(row=2, column=2, padx=(0, 4), pady=(10, 15))

        self.folder_open_btn = ctk.CTkButton(
            section, text="", image=icons.get(icons.LINK, size=16, on_accent=True),
            width=40, command=self._open_drive_folder
        )
        self.folder_open_btn.grid(row=2, column=3, padx=(0, 15), pady=(10, 15))

    def _copy_folder_id(self):
        """Copia o ID da pasta do Drive para a área de transferência."""
        folder_id = self.folder_entry.get().strip()
        if not folder_id:
            return
        self.clipboard_clear()
        self.clipboard_append(folder_id)
        toast.show("ID da pasta copiado", kind="success")

    def _open_drive_folder(self):
        """Abre a pasta do Drive no navegador a partir do ID."""
        folder_id = self.folder_entry.get().strip()
        if not folder_id:
            messagebox.showwarning(
                "Pasta não configurada", "Informe o ID da pasta do Drive primeiro."
            )
            return
        webbrowser.open(f"https://drive.google.com/drive/folders/{folder_id}")

    def _create_appearance_section(self):
        """Cria seção 'Geral' — preferências do app.

        Renomeada de 'Aparência' para 'Geral' (#30) pra acomodar futuras
        preferências (idioma, escala da UI, atalhos) além do tema.
        """
        section = ctk.CTkFrame(self.scroll_frame)
        section.pack(fill="x", pady=(0, 15))
        section.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            section, text="  Geral", image=icons.get(icons.GEAR, size=18),
            compound="left", font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")

        # Tema
        ctk.CTkLabel(section, text="Tema:").grid(
            row=1, column=0, padx=(15, 10), pady=(10, 15), sticky="w"
        )

        # Inicia com o tema salvo (padrão "dark"). Rótulos em PT-BR no menu,
        # mapeados para os valores que o CustomTkinter entende.
        self._theme_labels = {"dark": "Escuro", "light": "Claro", "system": "Sistema"}
        self._theme_values = {v: k for k, v in self._theme_labels.items()}
        current = settings.APP_THEME if settings.APP_THEME in self._theme_labels else "dark"

        self.theme_var = ctk.StringVar(value=self._theme_labels[current])
        self.theme_menu = ctk.CTkOptionMenu(
            section,
            values=list(self._theme_labels.values()),
            variable=self.theme_var,
            command=self._change_theme,
            width=150,
        )
        self.theme_menu.grid(row=1, column=1, padx=10, pady=(10, 15), sticky="w")

    def _browse_export_dir(self):
        """Abre diálogo para selecionar diretório."""
        from tkinter import filedialog

        directory = filedialog.askdirectory(
            title="Selecione o diretório de exportação",
            initialdir=self.export_dir_entry.get(),
        )

        if directory:
            self.export_dir_entry.delete(0, "end")
            self.export_dir_entry.insert(0, directory)
            self._recompute_dirty()

    def _change_theme(self, label: str):
        """Aplica o tema escolhido e persiste a preferência no .env."""
        theme = self._theme_values.get(label, "dark")
        ctk.set_appearance_mode(theme)
        try:
            set_env_value("APP_THEME", theme)
            settings.reload()
            toast.show(f"Tema alterado para {label}", kind="info")
        except Exception as e:
            logger.debug(f"Erro ao salvar tema: {e}")
