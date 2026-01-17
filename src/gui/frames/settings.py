"""
Tela de Configurações.
"""

import customtkinter as ctk
import os

from src.core.config import settings


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
        """Cria seção de configuração do Wialon."""
        # Frame da seção
        section = ctk.CTkFrame(self.scroll_frame)
        section.pack(fill="x", pady=(0, 15))
        section.grid_columnconfigure(1, weight=1)

        # Título
        title = ctk.CTkLabel(
            section, text="🔌  Wialon API", font=ctk.CTkFont(size=16, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 10), sticky="w")

        # Token
        ctk.CTkLabel(section, text="Token:").grid(
            row=1, column=0, padx=(15, 10), pady=10, sticky="w"
        )

        token_value = settings.WIALON_TOKEN or ""
        masked_token = "*" * 20 if token_value else "(não configurado)"

        self.token_entry = ctk.CTkEntry(
            section, width=400, placeholder_text="Cole seu token Wialon aqui"
        )
        self.token_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.token_entry.insert(0, masked_token if token_value else "")

        ctk.CTkLabel(
            section,
            text="⚠️ O token é carregado do arquivo .env",
            text_color="gray",
            font=ctk.CTkFont(size=11),
        ).grid(row=2, column=0, columnspan=3, padx=15, pady=(0, 15), sticky="w")

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
