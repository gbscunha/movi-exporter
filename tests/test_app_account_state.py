"""Testes do AccountState (Fase 05 da Onda 2)."""

import pytest

from src.gui.account_state import AccountState


def test_conta_inicial_padrao_e_1():
    assert AccountState().account == 1


def test_conta_inicial_customizada():
    assert AccountState(initial=2).account == 2


def test_label_humano():
    assert AccountState(1).label == "Conta 1"
    assert AccountState(2).label == "Conta 2"


def test_set_account_notifica_listener():
    state = AccountState(1)
    recebidos = []
    state.register(recebidos.append)

    state.set_account(2)

    assert recebidos == [2]
    assert state.account == 2


def test_set_account_mesmo_valor_nao_notifica():
    """Reselecionar a conta atual não deve disparar rebuild."""
    state = AccountState(1)
    recebidos = []
    state.register(recebidos.append)

    state.set_account(1)

    assert recebidos == []


def test_multiplos_listeners_todos_notificados():
    state = AccountState(1)
    a, b = [], []
    state.register(a.append)
    state.register(b.append)

    state.set_account(2)

    assert a == [2]
    assert b == [2]


def test_unregister_para_de_notificar():
    state = AccountState(1)
    recebidos = []
    state.register(recebidos.append)
    state.unregister(recebidos.append)  # função diferente — não remove nada

    # Registra a MESMA referência e remove
    cb = recebidos.append
    state.register(cb)
    state.unregister(cb)
    state.set_account(2)

    assert recebidos == []


def test_register_idempotente():
    """Registrar o mesmo callback duas vezes não dispara em dobro."""
    state = AccountState(1)
    recebidos = []
    cb = recebidos.append
    state.register(cb)
    state.register(cb)

    state.set_account(2)

    assert recebidos == [2]


def test_set_account_invalido_levanta():
    state = AccountState(1)
    with pytest.raises(ValueError):
        state.set_account(3)


def test_listener_que_descadastra_nao_recebe():
    state = AccountState(1)
    chamadas = {"a": 0, "b": 0}

    def a(_):
        chamadas["a"] += 1

    def b(_):
        chamadas["b"] += 1

    state.register(a)
    state.register(b)
    state.unregister(a)
    state.set_account(2)

    assert chamadas == {"a": 0, "b": 1}


def test_label_de_pasta_nao_muda_com_nome_de_usuario():
    """`label` nomeia a subpasta de export — nome de usuário não pode afetá-lo.

    Contrato de disco: `exports/AAAA-MM/Conta 1/`. Se mudasse, os exports
    antigos sumiriam do "Resumo de Exportações" (spec nome-usuario-no-seletor).
    """
    state = AccountState(1)
    state.set_username(1, "lcmovi_mgr")
    state.set_username(2, "lcmovi_adm")

    assert state.label == "Conta 1"
    state.set_account(2)
    assert state.label == "Conta 2"


def test_display_label_cai_para_conta_n_sem_nome():
    """Sem nome conhecido, o seletor mostra o rótulo neutro."""
    state = AccountState(1)
    assert state.display_label(1) == "Conta 1"
    assert state.display_label(2) == "Conta 2"


def test_display_label_usa_nome_quando_conhecido():
    state = AccountState(1)
    state.set_username(1, "lcmovi_mgr")

    assert state.display_label(1) == "lcmovi_mgr"
    assert state.display_label(2) == "Conta 2"


def test_display_label_desempata_nomes_iguais():
    """Dois itens idênticos quebrariam a seleção do dropdown."""
    state = AccountState(1)
    state.set_username(1, "lcmovi_mgr")
    state.set_username(2, "lcmovi_mgr")

    assert state.display_label(1) == "lcmovi_mgr (Conta 1)"
    assert state.display_label(2) == "lcmovi_mgr (Conta 2)"


def test_set_username_notifica_listeners():
    """A sidebar precisa saber que o nome chegou para atualizar os itens."""
    state = AccountState(1)
    chamadas = []
    state.register_username_listener(lambda: chamadas.append(True))

    state.set_username(1, "lcmovi_mgr")
    assert len(chamadas) == 1

    # Mesmo nome de novo não notifica (evita rebuild à toa).
    state.set_username(1, "lcmovi_mgr")
    assert len(chamadas) == 1


def test_set_username_ignora_vazio():
    """Autenticação sem nome não apaga o que já era conhecido."""
    state = AccountState(1)
    state.set_username(1, "lcmovi_mgr")
    state.set_username(1, "")

    assert state.display_label(1) == "lcmovi_mgr"
