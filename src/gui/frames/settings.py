"""
Tela de Configurações.
"""

import os
import threading
import webbrowser
from tkinter import messagebox

import customtkinter as ctk

from src.clients.wialon_client import WialonClient, WialonError
from src.core.config import settings
from src.core.env_writer import set_env_value
from src.core.logger import logger

# Página de login do Wialon. Depois de logado, o usuário gera o token
# em Configurações da conta → Aplicações → Tokens.
URL_AUTORIZACAO_WIALON = "https://hosting.wialon.com/login.html"


class SettingsFrame(ctk.CTkFrame):
    """Tela de configurações do aplicativo."""

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)

        # Configurar grid
        self.grid_columnconfigure(0, weight=1)

        # Título
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

        # Seções
        self._create_wialon_section(account=1)
        self._create_wialon_section(account=2)
        self._create_export_section()
        self._create_drive_section()
        self._create_appearance_section()

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

        # Título
        title = ctk.CTkLabel(
            section,
            text=f"🔌  Wialon API — Conta {account}",
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

        toggle_btn = ctk.CTkButton(
            section,
            text="👁",
            width=36,
            command=lambda a=account: self._toggle_token_visibility(a),
        )
        toggle_btn.grid(row=1, column=2, padx=2, pady=10)

        open_btn = ctk.CTkButton(
            section,
            text="🔗 Gerar",
            width=80,
            command=self._open_wialon_auth_page,
        )
        open_btn.grid(row=1, column=3, padx=2, pady=10)

        save_btn = ctk.CTkButton(
            section,
            text="💾 Salvar",
            width=90,
            command=lambda a=account: self._save_wialon_token(a),
        )
        save_btn.grid(row=1, column=4, padx=2, pady=10)

        test_btn = ctk.CTkButton(
            section,
            text="🔍 Testar",
            width=90,
            command=lambda a=account: self._test_wialon_token(a),
        )
        test_btn.grid(row=1, column=5, padx=(2, 15), pady=10)

        # Status
        status_label = ctk.CTkLabel(
            section,
            text="Status: (não testado)",
            text_color="gray",
            font=ctk.CTkFont(size=12),
        )
        status_label.grid(
            row=2, column=0, columnspan=6, padx=15, pady=(0, 15), sticky="w"
        )

        # Salva referência aos widgets desta conta para uso nos callbacks.
        self._token_widgets[account] = {
            "entry": entry,
            "test_btn": test_btn,
            "status_label": status_label,
            "visible": False,
        }

        # Aliases para compatibilidade com testes/smoke da Fase 10 (Conta 1).
        if account == 1:
            self.token_entry = entry
            self.token_toggle_btn = toggle_btn
            self.token_open_btn = open_btn
            self.token_save_btn = save_btn
            self.token_test_btn = test_btn
            self.token_status_label = status_label

    def _toggle_token_visibility(self, account: int):
        """Alterna entre mostrar e esconder o token da conta dada."""
        w = self._token_widgets[account]
        w["visible"] = not w["visible"]
        w["entry"].configure(show="" if w["visible"] else "*")

    def _open_wialon_auth_page(self):
        """Abre a página de login do Wialon no navegador."""
        webbrowser.open(URL_AUTORIZACAO_WIALON)

    def _save_wialon_token(self, account: int):
        """Grava o token da conta dada no .env e recarrega as configurações."""
        w = self._token_widgets[account]
        token = w["entry"].get().strip()
        if not token:
            messagebox.showwarning(
                "Token vazio", "Cole um token válido antes de salvar."
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

        w["status_label"].configure(
            text="Status: 💾 Token salvo no .env", text_color="#2ecc71"
        )

    def _test_wialon_token(self, account: int):
        """Testa o token da conta dada chamando authenticate() em background."""
        w = self._token_widgets[account]
        token = w["entry"].get().strip()
        if not token:
            messagebox.showwarning(
                "Token vazio", "Cole um token antes de testar a conexão."
            )
            return

        w["status_label"].configure(
            text="Status: 🔄 Testando conexão...", text_color="gray"
        )
        w["test_btn"].configure(state="disabled")

        def worker():
            try:
                client = WialonClient(token=token)
                client.authenticate()
                username = getattr(client, "username", "") or ""
                client.logout()
                self.after(0, self._on_token_test_ok, account, username)
            except WialonError as e:
                self.after(0, self._on_token_test_fail, account, str(e))
            except Exception as e:
                logger.debug(f"Erro inesperado ao testar token: {e}")
                self.after(0, self._on_token_test_fail, account, str(e))

        threading.Thread(target=worker, daemon=True).start()

    def _on_token_test_ok(self, account: int, username: str):
        """Callback executado na thread da GUI após teste bem-sucedido."""
        w = self._token_widgets[account]
        if username:
            text = f"Status: ✅ Conectado como \"{username}\""
        else:
            text = "Status: ✅ Conectado"
        w["status_label"].configure(text=text, text_color="#2ecc71")
        w["test_btn"].configure(state="normal")

    def _on_token_test_fail(self, account: int, error: str):
        """Callback executado na thread da GUI após teste falhar."""
        w = self._token_widgets[account]
        w["status_label"].configure(
            text=f"Status: ❌ Falha — {error}", text_color="#e74c3c"
        )
        w["test_btn"].configure(state="normal")

    def _create_export_section(self):
        """Cria seção de configuração de exportação."""
        section = ctk.CTkFrame(self.scroll_frame)
        section.pack(fill="x", pady=(0, 15))
        section.grid_columnconfigure(1, weight=1)

        # Título
        title = ctk.CTkLabel(
            section, text="📁  Exportação", font=ctk.CTkFont(size=16, weight="bold")
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

        self.browse_btn = ctk.CTkButton(
            section, text="📂", width=40, command=self._browse_export_dir
        )
        self.browse_btn.grid(row=1, column=2, padx=(5, 15), pady=10)

        # Page size
        ctk.CTkLabel(section, text="Registros por página:").grid(
            row=2, column=0, padx=(15, 10), pady=(10, 15), sticky="w"
        )

        page_size = str(settings.WIALON_PAGE_SIZE or 1000)

        self.page_size_entry = ctk.CTkEntry(section, width=100)
        self.page_size_entry.grid(row=2, column=1, padx=10, pady=(10, 15), sticky="w")
        self.page_size_entry.insert(0, page_size)

    def _create_drive_section(self):
        """Cria seção de configuração do Google Drive."""
        section = ctk.CTkFrame(self.scroll_frame)
        section.pack(fill="x", pady=(0, 15))
        section.grid_columnconfigure(1, weight=1)

        # Título
        title = ctk.CTkLabel(
            section, text="☁️  Google Drive", font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 10), sticky="w")

        # Arquivo de credenciais
        ctk.CTkLabel(section, text="Credenciais:").grid(
            row=1, column=0, padx=(15, 10), pady=10, sticky="w"
        )

        creds_file = settings.GOOGLE_DRIVE_CREDENTIALS_FILE or "./client_secrets.json"
        file_exists = os.path.exists(creds_file)

        status = "✅ Encontrado" if file_exists else "❌ Não encontrado"
        status_color = "#2ecc71" if file_exists else "#e74c3c"

        self.creds_label = ctk.CTkLabel(
            section, text=f"{creds_file} ({status})", text_color=status_color
        )
        self.creds_label.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="w")

        # Folder ID
        ctk.CTkLabel(section, text="Pasta ID:").grid(
            row=2, column=0, padx=(15, 10), pady=(10, 15), sticky="w"
        )

        folder_id = settings.GOOGLE_DRIVE_FOLDER_ID or ""
        masked_folder = folder_id[:15] + "..." if len(folder_id) > 15 else folder_id

        self.folder_entry = ctk.CTkEntry(
            section, width=350, placeholder_text="ID da pasta no Google Drive"
        )
        self.folder_entry.grid(row=2, column=1, padx=10, pady=(10, 15), sticky="w")
        self.folder_entry.insert(0, masked_folder)

    def _create_appearance_section(self):
        """Cria seção de aparência."""
        section = ctk.CTkFrame(self.scroll_frame)
        section.pack(fill="x", pady=(0, 15))
        section.grid_columnconfigure(1, weight=1)

        # Título
        title = ctk.CTkLabel(
            section, text="🎨  Aparência", font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")

        # Tema
        ctk.CTkLabel(section, text="Tema:").grid(
            row=1, column=0, padx=(15, 10), pady=(10, 15), sticky="w"
        )

        self.theme_var = ctk.StringVar(value="dark")
        self.theme_menu = ctk.CTkOptionMenu(
            section,
            values=["dark", "light", "system"],
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

    def _change_theme(self, theme: str):
        """Muda o tema da aplicação."""
        ctk.set_appearance_mode(theme)
