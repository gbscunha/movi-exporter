"""Testes do ToastManager (Onda 3 Fase 02)."""

from src.gui.components import toast
from src.gui.components.toast import ToastManager


def test_show_adiciona_toast_ativo(ctk_root):
    mgr = ToastManager(ctk_root)
    mgr.show("Olá", kind="success", duration_ms=99999)
    assert len(mgr._active) == 1


def test_multiplos_toasts_empilham(ctk_root):
    mgr = ToastManager(ctk_root)
    mgr.show("Um", duration_ms=99999)
    mgr.show("Dois", duration_ms=99999)
    mgr.show("Três", duration_ms=99999)
    assert len(mgr._active) == 3


def test_dismiss_remove_toast(ctk_root):
    mgr = ToastManager(ctk_root)
    mgr.show("Some já", duration_ms=99999)
    t = mgr._active[0]
    mgr._dismiss(t)
    assert mgr._active == []


def test_kind_invalido_usa_info(ctk_root):
    """Tipo desconhecido não deve quebrar — cai no estilo 'info'."""
    mgr = ToastManager(ctk_root)
    mgr.show("Qualquer", kind="inexistente", duration_ms=99999)
    assert len(mgr._active) == 1


def test_show_global_sem_manager_e_noop():
    """toast.show() sem manager configurado não deve levantar (headless/testes)."""
    toast.set_manager(None)
    toast.show("ninguém vê")  # não deve levantar


def test_show_global_usa_manager_configurado(ctk_root):
    mgr = ToastManager(ctk_root)
    toast.set_manager(mgr)
    try:
        toast.show("via global", kind="info", duration_ms=99999)
        assert len(mgr._active) == 1
    finally:
        toast.set_manager(None)
