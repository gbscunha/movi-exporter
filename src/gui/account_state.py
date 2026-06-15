"""Estado global da conta Wialon selecionada.

Antes, o seletor de conta vivia dentro do frame de Exportação e a Home não
reagia à troca. Centralizar o estado aqui permite que a sidebar troque a
conta e tanto a Home quanto o Export respondam (padrão observer).

Uso:
    state = AccountState()
    state.register(lambda acc: print(f"mudou para {acc}"))
    state.set_account(2)   # notifica os listeners
"""

from typing import Callable, List

# Tipo do callback de mudança de conta: recebe o número da conta (1 ou 2).
AccountListener = Callable[[int], None]


class AccountState:
    """Mantém a conta ativa (1 ou 2) e notifica observadores na troca."""

    def __init__(self, initial: int = 1):
        self._account: int = initial
        self._listeners: List[AccountListener] = []

    @property
    def account(self) -> int:
        """Conta atualmente selecionada (1 ou 2)."""
        return self._account

    @property
    def label(self) -> str:
        """Nome humano da conta — usado em subpastas e mensagens."""
        return f"Conta {self._account}"

    def register(self, listener: AccountListener) -> None:
        """Inscreve um callback para ser chamado quando a conta mudar."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def unregister(self, listener: AccountListener) -> None:
        """Remove um callback previamente inscrito (no-op se não existir)."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def set_account(self, account: int) -> None:
        """Define a conta ativa e notifica os listeners.

        Não faz nada (nem notifica) se a conta for igual à atual — evita
        rebuilds desnecessários de serviço quando o usuário reseleciona o
        mesmo valor no dropdown.
        """
        if account not in (1, 2):
            raise ValueError(f"Conta inválida: {account!r}. Use 1 ou 2.")
        if account == self._account:
            return
        self._account = account
        for listener in list(self._listeners):
            listener(account)
