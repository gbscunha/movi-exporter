# Spec — <nome curto da feature>

> **Status:** rascunho | aprovada | implementada | descartada
> **Branch:** `feat/<slug>`
> **Fatia no CHECKLIST:** <link/linha>
> **ADR relacionado:** `docs/decisions/ADR-XXXX-...md` (se houver)

Copie este arquivo para `docs/specs/<slug>.md`. A spec descreve o **quê** e o
**critério de pronto** — não o como. Critérios precisam ser testáveis: cada
DADO/QUANDO/ENTÃO vira (pelo menos) um teste ou um passo de verificação manual.

## Problema / motivação

Quem pediu, qual dor resolve, o que acontece hoje. Uma ou duas frases.

## Objetivo

O que muda para o usuário final (ou para o mantenedor) quando isso estiver pronto.

## Fora de escopo

O que **não** será feito nesta entrega, explicitamente — evita escopo crescer
durante a implementação.

## Critérios de aceitação

```
DADO   <estado inicial / dados de entrada>
QUANDO <ação>
ENTÃO  <resultado observável e verificável>
```

Repetir para cada comportamento, incluindo o caminho de erro
(ex.: "DADO que o token não tem ACL de motoristas, QUANDO exporta,
ENTÃO a coluna Motorista vem `N/D` e o app.log registra um warning").

## Impacto nos dados do export

| Item | Antes | Depois |
|------|-------|--------|
| Colunas (nome/ordem) | | |
| Valor quando sem dado | | `N/D` |
| Golden test | | atualizar? sim/não |

Se não mexe no export, escrever "Nenhum".

## Wialon

Chamadas/parâmetros novos ou alterados; flags; sessão (`sid`/`gis_sid`);
volume de requisições e cache. Se não toca a Wialon, "Nenhum".

## Verificação manual

O que o humano precisa abrir/rodar para dar o aceite (GUI, arquivo gerado,
token real, `app.log`).

## Riscos e perguntas abertas

- ...
