"""Testes do arquivo único de mensagens da interface.

Spec: `docs/specs/mensagens-centralizadas.md`. A varredura abaixo é o que
impede texto novo de nascer embutido num frame.
"""

import ast
import re
from pathlib import Path

from src.gui import messages

GUI_DIR = Path(__file__).resolve().parent.parent / "src" / "gui"

# Módulos ainda não migrados — a lista encolhe a cada fatia do refactor e fica
# vazia na última. Enquanto um módulo está aqui, a varredura o ignora; assim
# cada fatia fecha verde e o que já migrou fica protegido.
NAO_MIGRADOS: set[str] = set()

# Chamadas que recebem texto do usuário, e em QUAIS posições. Inspecionar só
# o primeiro argumento deixava passar o corpo de `showerror(titulo, texto)` e
# os helpers que recebem a mensagem numa posição diferente.
ARGUMENTOS_DE_TEXTO = {
    "show": [0],  # toast.show(mensagem, kind=...)
    "showerror": [0, 1],
    "showwarning": [0, 1],
    "showinfo": [0, 1],
    "askyesno": [0, 1],
    "_log": [0],  # log de progresso da exportação
    "_set_token_status": [1],  # (conta, mensagem, cor, ícone)
    "_show_error": [0],
    "_show_warning": [0],
    "set_status": [0],  # barra de status
    "insert": [1],  # textbox.insert(indice, texto)
    "title": [0],  # título de janela
}


def _tem_letra(valor: str) -> bool:
    """True se a string é texto de verdade (e não `""`, `"●"`, `"🎉"`)."""
    return any(c.isalpha() for c in valor)


def _literais_de_texto(no: ast.AST) -> list[str]:
    """Extrai o texto literal de uma constante ou f-string."""
    if isinstance(no, ast.Constant) and isinstance(no.value, str):
        return [no.value]
    if isinstance(no, ast.JoinedStr):
        return [
            parte.value
            for parte in no.values
            if isinstance(parte, ast.Constant) and isinstance(parte.value, str)
        ]
    if isinstance(no, ast.List):
        # `values=[...]` de dropdowns e abas.
        return [t for item in no.elts for t in _literais_de_texto(item)]
    return []


def _textos_embutidos(caminho: Path) -> list[str]:
    """Textos de UI escritos direto no módulo, em vez de virem de messages."""
    arvore = ast.parse(caminho.read_text(encoding="utf-8"))
    achados: list[str] = []

    for no in ast.walk(arvore):
        if not isinstance(no, ast.Call):
            continue

        for keyword in no.keywords:
            if keyword.arg in ("text", "placeholder_text", "values"):
                achados += _literais_de_texto(keyword.value)

        nome = no.func.attr if isinstance(no.func, ast.Attribute) else None
        for posicao in ARGUMENTOS_DE_TEXTO.get(nome, []):
            if posicao < len(no.args):
                achados += _literais_de_texto(no.args[posicao])

    return [t for t in achados if _tem_letra(t)]


def _constantes(classe) -> dict[str, str]:
    return {
        nome: valor
        for nome, valor in vars(classe).items()
        if not nome.startswith("_") and isinstance(valor, str)
    }


def _classes_de_mensagem() -> list[type]:
    return [
        obj
        for nome, obj in vars(messages).items()
        if isinstance(obj, type) and not nome.startswith("_")
    ]


def test_nao_ha_texto_embutido_na_gui():
    """Nenhum módulo já migrado escreve texto de UI direto no código."""
    pendencias: dict[str, list[str]] = {}

    for caminho in sorted(GUI_DIR.rglob("*.py")):
        relativo = caminho.relative_to(GUI_DIR).as_posix()
        if relativo in NAO_MIGRADOS or relativo == "messages.py":
            continue
        embutidos = _textos_embutidos(caminho)
        if embutidos:
            pendencias[relativo] = embutidos

    assert not pendencias, f"texto de UI fora de messages.py: {pendencias}"


def test_nenhuma_constante_vazia():
    """Toda mensagem tem conteúdo — chave sem texto vira tela em branco."""
    for classe in _classes_de_mensagem():
        for nome, valor in _constantes(classe).items():
            assert valor.strip(), f"{classe.__name__}.{nome} está vazia"


def test_format_strings_sao_usadas_com_as_chaves_certas():
    """Toda chave `{x}` declarada é passada no `.format(...)` correspondente.

    Pega o erro típico do refactor: renomear a chave na constante e esquecer
    do ponto de uso (que só apareceria em runtime, na tela do cliente).
    """
    # {(Classe, CONSTANTE): [chaves passadas em cada `.format(...)`]}
    usos: dict[tuple[str, str], list[set[str]]] = {}

    for caminho in GUI_DIR.rglob("*.py"):
        arvore = ast.parse(caminho.read_text(encoding="utf-8"))
        for no in ast.walk(arvore):
            if not (isinstance(no, ast.Call) and isinstance(no.func, ast.Attribute)):
                continue
            if no.func.attr != "format":
                continue
            alvo = no.func.value
            if not (
                isinstance(alvo, ast.Attribute) and isinstance(alvo.value, ast.Name)
            ):
                continue
            chave = (alvo.value.id, alvo.attr)
            usos.setdefault(chave, []).append({kw.arg for kw in no.keywords})

    for classe in _classes_de_mensagem():
        for nome, valor in _constantes(classe).items():
            chaves = set(re.findall(r"\{(\w+)", valor))
            if not chaves:
                continue

            formatacoes = usos.get((classe.__name__, nome))
            assert formatacoes, (
                f"{classe.__name__}.{nome} tem chaves {chaves} e nunca é formatada"
            )
            for passadas in formatacoes:
                assert chaves == passadas, (
                    f"{classe.__name__}.{nome} declara {chaves} mas recebeu {passadas}"
                )


def test_referencias_a_mensagens_existem():
    """Toda `XxxMsg.CONSTANTE` citada na GUI existe de fato no módulo.

    O lint pega import faltando, mas não pega constante inexistente: isso só
    apareceria em runtime, na tela do cliente.
    """
    classes = {c.__name__: c for c in _classes_de_mensagem()}
    quebradas: list[str] = []

    for caminho in GUI_DIR.rglob("*.py"):
        if caminho.name == "messages.py":
            continue
        arvore = ast.parse(caminho.read_text(encoding="utf-8"))
        for no in ast.walk(arvore):
            if not (isinstance(no, ast.Attribute) and isinstance(no.value, ast.Name)):
                continue
            classe = classes.get(no.value.id)
            if classe is not None and not hasattr(classe, no.attr):
                relativo = caminho.relative_to(GUI_DIR).as_posix()
                quebradas.append(f"{relativo}:{no.lineno} {no.value.id}.{no.attr}")

    assert not quebradas, f"referências inexistentes em messages.py: {quebradas}"
