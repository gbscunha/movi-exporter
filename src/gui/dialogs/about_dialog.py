"""
Diálogo "Sobre" — informações do app, links e verificação de atualização.
"""

import threading
import webbrowser

import customtkinter as ctk

from src.core.logger import logger
from src.gui import __version__, icons
from src.gui.components import toast
from src.gui.design import Colors, Font, Space
from src.gui.messages import AboutMsg
from src.gui.updater import GITHUB_OWNER, GITHUB_REPO, AutoUpdater

_REPO_URL = f"https://github.com/{GITHUB_OWNER}/{GITHUB_REPO}"
_RELEASES_URL = f"{_REPO_URL}/releases"


class AboutDialog(ctk.CTkToplevel):
    """Janela modal com informações do aplicativo."""

    def __init__(self, master):
        super().__init__(master)

        self.title(AboutMsg.TITULO_JANELA)
        self.geometry("420x320")
        self.resizable(False, False)
        self.transient(master)

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=Space.XL, pady=Space.XL)

        ctk.CTkLabel(
            container,
            text=AboutMsg.TITULO,
            font=ctk.CTkFont(size=Font.SIZE_2XL, weight=Font.WEIGHT_BOLD),
        ).pack(anchor="w")

        ctk.CTkLabel(
            container,
            text=AboutMsg.VERSAO.format(versao=__version__),
            font=ctk.CTkFont(size=Font.SIZE_BASE),
            text_color=Colors.MUTED,
        ).pack(anchor="w", pady=(0, Space.MD))

        ctk.CTkLabel(
            container,
            text=AboutMsg.DESCRICAO,
            font=ctk.CTkFont(size=Font.SIZE_BASE),
            justify="left",
        ).pack(anchor="w", pady=(0, Space.LG))

        ctk.CTkButton(
            container,
            text=f"  {AboutMsg.BTN_REPOSITORIO}",
            image=icons.get(icons.LINK, size=16, on_accent=True),
            command=lambda: webbrowser.open(_REPO_URL),
        ).pack(fill="x", pady=Space.XS)

        ctk.CTkButton(
            container,
            text=f"  {AboutMsg.BTN_NOTAS_VERSAO}",
            image=icons.get(icons.LIST, size=16, on_accent=True),
            command=lambda: webbrowser.open(_RELEASES_URL),
        ).pack(fill="x", pady=Space.XS)

        self.update_btn = ctk.CTkButton(
            container,
            text=f"  {AboutMsg.BTN_VERIFICAR}",
            image=icons.get(icons.REFRESH, size=16, on_accent=True),
            command=self._check_updates,
        )
        self.update_btn.pack(fill="x", pady=Space.XS)

        ctk.CTkLabel(
            container,
            text=AboutMsg.LICENCA,
            font=ctk.CTkFont(size=Font.SIZE_SM),
            text_color=Colors.MUTED,
        ).pack(anchor="w", pady=(Space.LG, 0))

        # Centraliza sobre a janela principal e foca.
        self.after(10, self._center_on_master)

    def _center_on_master(self):
        """Posiciona o diálogo no centro da janela principal."""
        try:
            self.grab_set()
        except Exception as e:
            logger.debug(f"Erro ao focar diálogo Sobre: {e}")

    def _check_updates(self):
        """Verifica atualização em background e dá feedback via toast."""
        self.update_btn.configure(
            state="disabled", text=f"  {AboutMsg.BTN_VERIFICANDO}"
        )

        def worker():
            try:
                updater = AutoUpdater()
                has_update, version, url = updater.check_for_updates()
                self.after(0, lambda: self._on_update_result(has_update, version, url))
            except Exception:
                self.after(0, lambda: self._on_update_result(None, None, None))

        threading.Thread(target=worker, daemon=True).start()

    def _on_update_result(self, has_update, version, url):
        """Callback na thread da GUI com o resultado da verificação."""
        self.update_btn.configure(state="normal", text=f"  {AboutMsg.BTN_VERIFICAR}")
        if has_update is None:
            toast.show(AboutMsg.TOAST_FALHA_VERIFICAR, kind="warning")
        elif has_update:
            toast.show(AboutMsg.TOAST_NOVA_VERSAO.format(versao=version), kind="info")
            webbrowser.open(_RELEASES_URL)
        else:
            toast.show(AboutMsg.TOAST_ATUALIZADO, kind="success")
