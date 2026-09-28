"""Estado global da conta Wialon selecionada.

Antes, o seletor de conta vivia dentro do frame de Exportação e a Home não
reagia à troca. Centralizar o estado aqui permite que a sidebar troque a
conta e tanto a Home quanto o Export respondam (padrão observer).

Uso:
    state = AccountState()
    state.register(lambda acc: print(f"mudou para {acc}"))
    state.set_account(2)   # notifica os listeners
"""

from typing import Callable, Dict, List

from src.gui.messages import SidebarMsg

# Tipo do callback de mudança de conta: recebe o número da conta (1 ou 2).
AccountListener = Callable[[int], None]

# Callback de "o nome de alguma conta mudou" — sem argumentos, porque quem
# escuta (a sidebar) relê os rótulos das duas contas de uma vez.
UsernameListener = Callable[[], None]


class AccountState:
    """Mantém a conta ativa (1 ou 2) e notifica observadores na troca.

    Guarda também o username autenticado de cada conta, usado **só para
    exibição** no seletor. O rótulo de pasta (`label`) é outro conceito e não
    muda: ele nomeia `exports/AAAA-MM/Conta N/` e filtra o histórico.
    """

    def __init__(self, initial: int = 1):
        self._account: int = initial
        self._listeners: List[AccountListener] = []
        self._usernames: Dict[int, str] = {}
        self._username_listeners: List[UsernameListener] = []

    @property
    def account(self) -> int:
        """Conta atualmente selecionada (1 ou 2)."""
        return self._account

    @property
    def label(self) -> str:
        """Rótulo da conta ativa — usado em subpastas de export e mensagens.

        **Contrato de disco:** é o nome da subpasta (`exports/AAAA-MM/Conta 1/`)
        e o filtro do "Resumo de Exportações". Não incorporar o username aqui,
        ou os exports antigos ficam órfãos.
        """
        return SidebarMsg.CONTA.format(numero=self._account)

    def username(self, account: int) -> str:
        """Último username autenticado da conta, ou string vazia."""
        return self._usernames.get(account, "")

    def set_username(self, account: int, username: str) -> None:
        """Registra o username de uma conta e avisa quem exibe o seletor.

        Ignora valor vazio (uma autenticação que não devolveu nome não deve
        apagar o que já se sabia) e repetição (evita rebuild à toa).
        """
        username = (username or "").strip()
        if not username or self._usernames.get(account) == username:
            return

        self._usernames[account] = username
        for listener in list(self._username_listeners):
            listener()

    def display_label(self, account: int) -> str:
        """Como a conta aparece no seletor: o username, se conhecido.

        Quando as duas contas têm o mesmo username (dois tokens do mesmo
        usuário), acrescenta o número: dois itens idênticos quebrariam a
        seleção do dropdown.
        """
        nome = self.username(account)
        if not nome:
            return SidebarMsg.CONTA.format(numero=account)

        outra = 2 if account == 1 else 1
        if self.username(outra) == nome:
            return SidebarMsg.CONTA_DESEMPATE.format(nome=nome, numero=account)
        return nome

    def register_username_listener(self, listener: UsernameListener) -> None:
        """Inscreve um callback para quando o username de alguma conta mudar."""
        if listener not in self._username_listeners:
            self._username_listeners.append(listener)

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
