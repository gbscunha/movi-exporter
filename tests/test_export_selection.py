"""Testes da seleção de veículos do Export (Onda 3 Fase 03 — #15)."""

import customtkinter as ctk

from src.gui.frames.export import ExportFrame


def _frame_with_vehicles(ctk_root, n=300):
    ef = ExportFrame(ctk_root)
    ef.vehicles = [
        {"id": i, "name": f"VTR{i:04d}", "plate": "" if i % 3 else f"ABC{i:04d}"}
        for i in range(n)
    ]
    ef.all_vehicles_var.set(False)
    ef._populate_vehicle_list()
    return ef


def test_default_nenhum_marcado(ctk_root):
    """Ao carregar, nenhum veículo vem marcado (#15a)."""
    ef = _frame_with_vehicles(ctk_root)
    assert sum(ef._selection.values()) == 0


def test_render_limitado_ao_max(ctk_root):
    """Não renderiza mais que _MAX_RENDER checkboxes (evita freeze, #3)."""
    ef = _frame_with_vehicles(ctk_root, n=839)
    rendered = sum(1 for k in ef.vehicle_checkboxes if isinstance(k, int))
    assert rendered == ef._MAX_RENDER


def test_busca_por_placa(ctk_root):
    ef = _frame_with_vehicles(ctk_root)
    ef.search_var.set("abc0123")
    rendered = sum(1 for k in ef.vehicle_checkboxes if isinstance(k, int))
    assert rendered == 1


def test_busca_por_id(ctk_root):
    ef = _frame_with_vehicles(ctk_root)
    ef.search_var.set("250")  # id 250 e qualquer outro que contenha "250"
    ids = [v["id"] for v in ef.vehicles if ef._matches_search(v, "250")]
    assert 250 in ids


def test_busca_vazia_casa_todos(ctk_root):
    ef = _frame_with_vehicles(ctk_root, n=10)
    assert all(ef._matches_search(v, "") for v in ef.vehicles)


def test_marcar_todos_filtrados(ctk_root):
    """'Marcar todos' atua só sobre o resultado da busca atual."""
    ef = _frame_with_vehicles(ctk_root)
    ef.search_var.set("abc0123")
    ef._set_filtered_selection(True)
    assert sum(ef._selection.values()) == 1
    assert ef._selection[123] is True


def test_desmarcar_todos(ctk_root):
    ef = _frame_with_vehicles(ctk_root)
    ef.search_var.set("")
    ef._set_filtered_selection(True)
    assert sum(ef._selection.values()) == 300
    ef._set_filtered_selection(False)
    assert sum(ef._selection.values()) == 0


def test_get_selected_ids_modo_todos_retorna_none(ctk_root):
    ef = _frame_with_vehicles(ctk_root)
    ef.all_vehicles_var.set(True)
    assert ef._get_selected_vehicle_ids() is None


def test_get_selected_ids_retorna_marcados(ctk_root):
    ef = _frame_with_vehicles(ctk_root)
    ef._selection[5] = True
    ef._selection[10] = True
    assert sorted(ef._get_selected_vehicle_ids()) == [5, 10]


def test_get_selected_ids_nenhum_marcado_retorna_none(ctk_root):
    """Modo específico mas 0 marcados → None (o _start_export valida antes)."""
    ef = _frame_with_vehicles(ctk_root)
    assert ef._get_selected_vehicle_ids() is None


def test_append_carrega_proximo_lote(ctk_root):
    """Scroll infinito: _append_next_batch renderiza +_MAX_RENDER sem buscar."""
    ef = _frame_with_vehicles(ctk_root, n=839)
    assert sum(1 for k in ef.vehicle_checkboxes if isinstance(k, int)) == ef._MAX_RENDER
    ef._append_next_batch()
    assert (
        sum(1 for k in ef.vehicle_checkboxes if isinstance(k, int))
        == 2 * ef._MAX_RENDER
    )


def test_nova_busca_reseta_lote(ctk_root):
    """Mudar a busca volta ao primeiro lote."""
    ef = _frame_with_vehicles(ctk_root, n=839)
    ef._append_next_batch()
    ef._append_next_batch()
    ef._on_search_changed()  # busca vazia, mas re-renderiza do primeiro lote
    assert sum(1 for k in ef.vehicle_checkboxes if isinstance(k, int)) == ef._MAX_RENDER


def test_label_com_e_sem_placa(ctk_root):
    ef = ExportFrame(ctk_root)
    assert "ABC1234" in ef._vehicle_label(
        {"id": 1, "name": "VTR01", "plate": "ABC1234"}
    )
    # Sem placa, mostra só o nome
    assert ef._vehicle_label({"id": 2, "name": "VTR02", "plate": ""}) == "VTR02"


def test_label_nome_igual_placa_nao_duplica(ctk_root):
    """Nome == placa não deve virar 'X · X' — mostra só o nome."""
    ef = ExportFrame(ctk_root)
    assert (
        ef._vehicle_label({"id": 3, "name": "SRX6A12", "plate": "SRX6A12"}) == "SRX6A12"
    )
