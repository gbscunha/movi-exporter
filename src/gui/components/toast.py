"""Toast/snackbar — avisos temporários no canto da janela.

Substitui (parcialmente) os popups nativos do tkinter para mensagens leves
(informação, sucesso, aviso) que não exigem ação do usuário. Erros graves e
confirmações continuam usando messagebox modal.

O ToastManager é criado uma vez pelo app e compartilhado com os frames (como
o AccountState). Cada toast aparece no canto inferior direito, empilha acima
dos anteriores e some sozinho após alguns segundos.
"""

from typing import List, Optional

import customtkinter as ctk

from src.gui import icons
from src.gui.design import Colors, Space


# Estilo por tipo de toast: (cor de destaque, ícone).
_KIND_STYLE = {
    "info": (Colors.INFO, icons.CIRCLE_CHECK),
    "success": (Colors.SUCCESS, icons.CIRCLE_CHECK),
    "warning": (Colors.WARNING, icons.TRIANGLE_WARNING),
}

_DEFAULT_DURATION_MS = 3500
_MARGIN = 20  # distância das bordas da janela
_GAP = 8  # espaço vertical entre toasts empilhados


class Toast(ctk.CTkFrame):
    """Um único cartão de notificação."""

    def __init__(self, master, message: str, kind: str):
        super().__init__(master, corner_radius=8, border_width=2)

        color, icon = _KIND_STYLE.get(kind, _KIND_STYLE["info"])
        self.configure(border_color=color)

        # Barra de acento colorida à esquerda.
        accent = ctk.CTkFrame(self, width=4, fg_color=color, corner_radius=2)
        accent.grid(row=0, column=0, sticky="ns", padx=(Space.SM, 0), pady=Space.SM)

        ctk.CTkLabel(
            self,
            text=f"  {message}",
            image=icons.get(icon, size=16, color=color),
            compound="left",
            anchor="w",
        ).grid(row=0, column=1, padx=(Space.SM, Space.MD), pady=Space.SM, sticky="w")


class ToastManager:
    """Gerencia a fila e o posicionamento dos toasts sobre a janela."""

    def __init__(self, root: ctk.CTk):
        self._root = root
        self._active: List[Toast] = []

    def show(
        self,
        message: str,
        kind: str = "info",
        duration_ms: int = _DEFAULT_DURATION_MS,
    ) -> None:
        """Exibe um toast. `kind` ∈ {info, success, warning}."""
        toast = Toast(self._root, message, kind)
        self._active.append(toast)
        self._reposition()
        self._root.after(duration_ms, lambda: self._dismiss(toast))

    def _dismiss(self, toast: Toast) -> None:
        if toast in self._active:
            self._active.remove(toast)
            toast.destroy()
            self._reposition()

    def _reposition(self) -> None:
        """Empilha os toasts ativos no canto inferior direito, de baixo p/ cima."""
        offset = _MARGIN
        # O mais novo fica embaixo; empilha os anteriores acima dele.
        for toast in reversed(self._active):
            toast.update_idletasks()
            height = toast.winfo_reqheight()
            toast.place(relx=1.0, rely=1.0, x=-_MARGIN, y=-offset, anchor="se")
            offset += height + _GAP


# Singleton opcional — o app seta via set_manager() e frames usam show().
_manager: Optional[ToastManager] = None


def set_manager(manager: ToastManager) -> None:
    """Registra o ToastManager global (chamado pelo app na inicialização)."""
    global _manager
    _manager = manager


def show(message: str, kind: str = "info", duration_ms: int = _DEFAULT_DURATION_MS) -> None:
    """Atalho para exibir um toast pelo manager global, se houver.

    Seguro chamar mesmo sem manager configurado (ex: testes headless): vira no-op.
    """
    if _manager is not None:
        _manager.show(message, kind, duration_ms)
