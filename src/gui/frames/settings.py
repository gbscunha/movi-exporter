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

        # Seções
        self._create_wialon_section()
        self._create_export_section()
        self._create_drive_section()
        self._create_appearance_section()

    def _create_wialon_section(self):
        """Cria seção de configuração do Wialon — Conta 1.

        Permite editar, gerar, salvar e testar o token sem reiniciar o app.
        """
        # Frame da seção
        section = ctk.CTkFrame(self.scroll_frame)
        section.pack(fill="x", pady=(0, 15))
        section.grid_columnconfigure(1, weight=1)

        # Título
        title = ctk.CTkLabel(
            section,
            text="🔌  Wialon API — Conta 1",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        title.grid(row=0, column=0, columnspan=6, padx=15, pady=(15, 10), sticky="w")

        # Linha do token + botões
        ctk.CTkLabel(section, text="Token:").grid(
            row=1, column=0, padx=(15, 10), pady=10, sticky="w"
        )

        self.token_entry = ctk.CTkEntry(
            section,
            width=320,
            show="*",
            placeholder_text="Cole seu token Wialon aqui",
        )
        self.token_entry.grid(row=1, column=1, padx=(0, 5), pady=10, sticky="we")
        if settings.WIALON_TOKEN:
            self.token_entry.insert(0, settings.WIALON_TOKEN)

        self._token_visible = False
        self.token_toggle_btn = ctk.CTkButton(
            section, text="👁", width=36, command=self._toggle_token_visibility
        )
        self.token_toggle_btn.grid(row=1, column=2, padx=2, pady=10)

        self.token_open_btn = ctk.CTkButton(
            section,
            text="🔗 Gerar",
            width=80,
            command=self._open_wialon_auth_page,
        )
        self.token_open_btn.grid(row=1, column=3, padx=2, pady=10)

        self.token_save_btn = ctk.CTkButton(
            section, text="💾 Salvar", width=90, command=self._save_wialon_token
        )
        self.token_save_btn.grid(row=1, column=4, padx=2, pady=10)

        self.token_test_btn = ctk.CTkButton(
            section, text="🔍 Testar", width=90, command=self._test_wialon_token
        )
        self.token_test_btn.grid(row=1, column=5, padx=(2, 15), pady=10)

        # Status
        self.token_status_label = ctk.CTkLabel(
            section,
            text="Status: (não testado)",
            text_color="gray",
            font=ctk.CTkFont(size=12),
        )
        self.token_status_label.grid(
            row=2, column=0, columnspan=6, padx=15, pady=(0, 15), sticky="w"
        )

    def _toggle_token_visibility(self):
        """Alterna entre mostrar e esconder o token."""
        self._token_visible = not self._token_visible
        self.token_entry.configure(show="" if self._token_visible else "*")

    def _open_wialon_auth_page(self):
        """Abre a página de login do Wialon no navegador."""
        webbrowser.open(URL_AUTORIZACAO_WIALON)

    def _save_wialon_token(self):
        """Grava o token no .env e recarrega as configurações em memória."""
        token = self.token_entry.get().strip()
        if not token:
            messagebox.showwarning(
                "Token vazio", "Cole um token válido antes de salvar."
            )
            return

        try:
            set_env_value("WIALON_TOKEN", token)
            settings.reload()
        except Exception as e:
            logger.debug(f"Erro ao salvar token Wialon: {e}")
            messagebox.showerror("Erro", f"Não foi possível salvar o token: {e}")
            return

        self.token_status_label.configure(
            text="Status: 💾 Token salvo no .env", text_color="#2ecc71"
        )

    def _test_wialon_token(self):
        """Testa o token atual chamando authenticate() em background."""
        token = self.token_entry.get().strip()
        if not token:
            messagebox.showwarning(
                "Token vazio", "Cole um token antes de testar a conexão."
            )
            return

        self.token_status_label.configure(
            text="Status: 🔄 Testando conexão...", text_color="gray"
        )
        self.token_test_btn.configure(state="disabled")

        def worker():
            try:
                client = WialonClient(token=token)
                client.authenticate()
                username = getattr(client, "username", "") or ""
                client.logout()
                self.after(0, self._on_token_test_ok, username)
            except WialonError as e:
                self.after(0, self._on_token_test_fail, str(e))
            except Exception as e:
                logger.debug(f"Erro inesperado ao testar token: {e}")
                self.after(0, self._on_token_test_fail, str(e))

        threading.Thread(target=worker, daemon=True).start()

    def _on_token_test_ok(self, username: str):
        """Callback executado na thread da GUI após teste bem-sucedido."""
        if username:
            text = f"Status: ✅ Conectado como \"{username}\""
        else:
            text = "Status: ✅ Conectado"
        self.token_status_label.configure(text=text, text_color="#2ecc71")
        self.token_test_btn.configure(state="normal")

    def _on_token_test_fail(self, error: str):
        """Callback executado na thread da GUI após teste falhar."""
        self.token_status_label.configure(
            text=f"Status: ❌ Falha — {error}", text_color="#e74c3c"
        )
        self.token_test_btn.configure(state="normal")

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
