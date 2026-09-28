# Spec — Nome do usuário no seletor de conta

> **Status:** em andamento
> **Branch:** `feat/nome-usuario-no-seletor`
> **Fatia no CHECKLIST:** Backlog → "Nome do usuário no seletor de conta"
> **ADR relacionado:** —

## Problema / motivação

Com duas contas configuradas, o menu lateral mostra "Conta 1" e "Conta 2". Quem
opera não tem como saber qual login da Wialon está por trás de cada uma — e
trocar de conta às cegas leva a exportar o mês errado, da frota errada.

## Objetivo

O seletor mostra **quem está autenticado** em cada conta (o username da Wialon),
usando a autenticação que o app já faz. Sem chamada de rede nova e sem mexer na
organização das pastas de exportação.

## Fora de escopo

- Buscar os nomes no boot autenticando os dois tokens (gastaria dois logins por
  abertura); o nome chega pela autenticação que já acontece.
- Apelido digitado pelo usuário.
- Mostrar o nome fora do seletor (tela Início, cabeçalho do relatório, nome de
  arquivo).
- Renomear as subpastas de exportação — ver "Invariante" abaixo.

## Invariante (o que não pode quebrar)

`exports/AAAA-MM/Conta 1/` e `Conta 2/` continuam com esse nome. O rótulo de
pasta (`AccountState.label`, usado em `export.py::_account_label` e em
`home.py::_active_account_label`) é **contrato de disco**: mudá-lo deixaria os
exports antigos órfãos no "Resumo de Exportações" e criaria duas convenções de
pasta na máquina do cliente. O nome do usuário é dado **só de exibição**.

## Critérios de aceitação

```
DADO   que a Conta 1 nunca foi autenticada neste computador
QUANDO o app abre com as duas contas configuradas
ENTÃO  o seletor mostra "Conta 1" e "Conta 2", e continua habilitado
```

```
DADO   que a tela Início autenticou a Conta 1 como "lcmovi_mgr"
QUANDO a autenticação termina
ENTÃO  o item da Conta 1 no seletor passa a mostrar "lcmovi_mgr", sem recarregar
       o app, e o nome é gravado para as próximas aberturas
```

```
DADO   que o usuário clica em Testar na Conta 2 e a Wialon responde "lcmovi_adm"
QUANDO o teste termina com sucesso
ENTÃO  o nome fica gravado e o seletor passa a mostrá-lo
```

```
DADO   que os dois tokens pertencem ao mesmo usuário "lcmovi_mgr"
QUANDO o seletor é montado
ENTÃO  os itens ficam "lcmovi_mgr (Conta 1)" e "lcmovi_mgr (Conta 2)" —
        nunca dois itens idênticos, que quebrariam a seleção
```

```
DADO   qualquer nome exibido no seletor
QUANDO uma exportação roda
ENTÃO  os arquivos continuam indo para `exports/AAAA-MM/Conta N/` e o
       "Resumo de Exportações" continua encontrando os exports antigos
```

```
DADO   que a autenticação falha (token inválido ou sem internet)
QUANDO o app abre
ENTÃO  o seletor mostra o último nome conhecido (ou "Conta N", se nunca houve)
       e permanece habilitado, para o usuário poder trocar para a outra conta
```

## Impacto nos dados do export

Nenhum. Nomes de pasta, colunas e nomes de arquivo inalterados. Golden test não muda.

## Wialon

Nenhuma chamada nova. O username já vem do `login` (`user.nm`), hoje exposto em
`WialonClient.username` e usado por `authenticate_token` na tela de
Configurações. Será preciso expô-lo pelo `VehicleService` (a GUI não fala com
`src.clients`) e declará-lo no `Protocol` `TrackingClient`.

## Novas chaves de configuração

| Chave | Para quê |
|---|---|
| `WIALON_USER` | Último username autenticado da Conta 1 (cache de exibição) |
| `WIALON_USER_2` | Idem, Conta 2 |

Não são segredo e não afetam a autenticação: se apagadas, o app volta a mostrar
"Conta N" até autenticar de novo.

## Verificação manual

Abrir o app com duas contas: conferir que o seletor mostra os nomes (ou "Conta
N" na primeira vez), que trocar de conta continua refletindo em Início e
Exportar, e que uma exportação de teste cai em `exports/AAAA-MM/Conta N/`.
Conferir também com a internet desligada.

## Riscos e perguntas abertas

- O username da Wialon costuma ser técnico (`lcmovi_mgr`), não um nome de
  pessoa. Se ficar ruim na prática, o caminho é o apelido manual (fora de
  escopo aqui).
- O manual (`docs/manual/manual.html`, seção "Adicionar uma segunda conta") diz
  que o seletor mostra "Conta 1 e Conta 2"; precisa ser atualizado junto, e o
  print `conta2-seletor.png` refeito.
