# Spec — Manual do usuário refeito

> **Status:** rascunho
> **Branch:** `docs/manual-usuario`
> **Fatia no CHECKLIST:** Backlog → "Manual do usuário refeito"
> **ADR relacionado:** —

## Problema / motivação

O manual atual (`docs/manual/manual.html`) cresceu por acréscimo ao longo das
ondas 1–5: mistura passo a passo com referência avançada (variáveis de ambiente
como "passo 9"), descreve botões que mudaram de nome e afirma comportamentos que
o código não faz. Nenhuma das 11 imagens que ele referencia existe.

Divergências verificadas no código:

| O manual diz | O código faz |
|---|---|
| Upload separa `Conta 1/` e `Conta 2/` no Drive | Separação só local (`exporter.py:124`); Drive recebe tudo em `AAAA-MM/` (`uploader.py:280`) |
| "Selecionar veículos", "Desmarcar todos", "Mostrar mais" | "Escolher manualmente", "Limpar todos", scroll infinito (`export.py`) |
| Token só precisa ser refeito se expirar (sem dizer quando) | `Gerar` abre `login.html` sem parâmetros; pela doc da Wialon o padrão é 30 dias |
| — (não menciona) | Botão **Parar**, confirmação antes de exportar, abas Veículos/Progresso, salvar log, consolidado sempre em CSV, autorização do Google no primeiro upload, seletor de conta só aparece ao reabrir o app |

## Objetivo

Um manual que o cliente consegue seguir sozinho, do download ao relatório aberto,
e no qual ele encontra a resposta pelo sintoma quando algo dá errado. Estrutura
em cinco grupos (Começar · Configurar · Usar · Referência · Ajuda), tarefa por
seção, com lugares marcados para os prints.

## Fora de escopo

- Corrigir o upload do Drive para separar por conta — vai para o Backlog.
- Mudar a URL do botão **Gerar** (duração/acesso do token) — vai para o Backlog.
- Tirar os prints (é do humano) e indexar as imagens reais — fatia seguinte.
- Traduzir ou refazer `docs/cliente/USER_GUIDE.md` (guia técnico/CLI); só o
  ponteiro de seção dele é atualizado.
- Manual de macOS — o cliente em produção é Windows.

## Critérios de aceitação

```
DADO   o manual aberto no navegador
QUANDO clico em qualquer item do índice lateral
ENTÃO  existe uma seção com aquele id (nenhuma âncora quebrada)
```

```
DADO   que os prints ainda não foram tirados
QUANDO abro o manual
ENTÃO  cada figura ausente some (onerror) e o texto permanece completo e
       suficiente por si — nenhuma informação existe só na imagem
```

```
DADO   o manual e o código da GUI
QUANDO um rótulo citado no manual é renomeado no app
ENTÃO  o teste de rótulos falha apontando o termo divergente
```

```
DADO   a seção "Enviar para o Google Drive"
QUANDO o leitor procura onde os arquivos aparecem
ENTÃO  o manual diz que o Drive recebe tudo na pasta do mês (`AAAA-MM/`) e que
       a separação por conta acontece só na pasta local
```

```
DADO   a seção "Resolver problemas"
QUANDO o export volta com menos dias do que o mês tem
ENTÃO  o manual explica o limite de retenção de histórico da conta Wialon e
       orienta exportar logo após o fechamento do mês
```

## Impacto nos dados do export

Nenhum. Só documentação.

## Wialon

Nenhuma chamada nova. O manual descreve o fluxo de token (login web → token na
URL após `access_token=`) e a permissão de ver motoristas, sem cravar prazo de
validade.

## Verificação manual

- `pytest -q` e `ruff check src/` / `ruff format --check src/ tests/`
- Abrir `docs/manual/manual.html` no navegador: navegar pelo índice, conferir
  que nenhuma figura ausente deixa buraco e que o texto se sustenta sem imagem
- Abrir o app (`python -m src.gui.main`) → **Manual** no rodapé do menu lateral
- Conferir os rótulos citados contra as telas reais do app

## Riscos e perguntas abertas

- E-mail de suporte ainda não informado — o manual entra com `[e-mail de suporte]`
  até ser substituído.
- Validade real do token do cliente não observada; texto fica neutro
  ("quando o Testar falhar, gere outro").
