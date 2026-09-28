# Spec — Mensagens da interface em arquivo único

> **Status:** rascunho
> **Branch:** `refactor/mensagens-centralizadas`
> **Fatia no CHECKLIST:** Backlog → "Mensagens da interface em arquivo único"
> **ADR relacionado:** —

## Problema / motivação

Ao revisar os prints do manual, o mantenedor encontrou uma mensagem ruim para o
cliente final — "Status: Token salvo no .env" cita um arquivo que o usuário não
precisa conhecer — e não tinha onde revisar as demais: hoje todo texto visível
está embutido no meio do código da GUI, espalhado em 8 módulos.

Inventário atual (`src/gui/`):

| Tipo | Quantidade |
|---|---|
| Rótulos de botões e labels (`text=`) | 97 |
| Toasts (`toast.show`) | 15 |
| Caixas de diálogo (`messagebox.*`) | 8 |
| Linhas do log de exportação (`self._log`) | 44 |
| Placeholders de campo | 3 |

Sem um lugar único, revisar o texto que o cliente lê exige caçar string por
string, e o manual pode divergir do app sem ninguém perceber — foi o que
aconteceu antes (`docs/specs/manual-usuario.md`).

## Objetivo

Um arquivo `src/gui/messages.py` que o mantenedor abre para ler e ajustar
**todo** o texto visível do app, sem entrar na lógica das telas. A GUI passa a
referenciar constantes; nenhum texto novo nasce embutido num frame.

## Fora de escopo

- Internacionalização (i18n) — o app continua só em PT-BR, sem catálogo nem
  mecanismo de tradução. O arquivo é fonte única, não camada de idioma.
- Mensagens de log técnico (`logger.*`, `app.log`) — são para diagnóstico, não
  para o cliente, e ficam onde estão.
- Exceções de domínio (`WialonError` e derivadas) em `src/clients`/`src/services`.
- Redesenho de telas, mudança de fluxo ou de layout.
- Revisar o conteúdo de todas as mensagens — só as que forem obviamente ruins
  para o cliente (ver Critérios).

## Critérios de aceitação

```
DADO   o app rodando
QUANDO o usuário salva o token na tela de Configurações
ENTÃO  a mensagem de status é "Status: Token salvo com sucesso"
       (sem menção a .env)
```

```
DADO   qualquer módulo de src/gui/
QUANDO se procura por texto visível ao usuário embutido no código
ENTÃO  não há literal de UI fora de `messages.py` — os módulos referenciam
       constantes (teste automatizado varre `text=`, `toast.show`,
       `messagebox.*` e `self._log` procurando string literal)
```

```
DADO   o manual do usuário
QUANDO um rótulo citado nele é renomeado em `messages.py`
ENTÃO  `test_rotulos_citados_existem_na_gui` falha apontando o rótulo
       (o teste passa a ler as constantes, não mais um regex no fonte)
```

```
DADO   as telas Início, Exportar, Configurações, Sobre e o diálogo de
       atualização
QUANDO abertas depois do refactor
ENTÃO  exibem exatamente os mesmos textos de antes (salvo as correções
       declaradas), sem placeholder não substituído nem chave faltando
```

## Impacto nos dados do export

Nenhum. Só texto de interface. O golden test não muda.

## Wialon

Nenhum.

## Correções de texto declaradas

| Onde | Antes | Depois |
|---|---|---|
| Configurações → status do token | `Status: Token salvo no .env` | `Status: Token salvo com sucesso` |

Qualquer outra mudança de texto precisa ser listada aqui antes de entrar.

## Verificação manual

Abrir o app e percorrer as cinco telas (Início, Exportar, Configurações, Sobre,
diálogo de atualização), conferindo que nada virou texto vazio, chave crua ou
`{placeholder}` não substituído. Rodar uma exportação pequena para ver o log de
progresso completo (início, progresso, conclusão) e um cancelamento.

## Riscos e perguntas abertas

- Refactor amplo sem testes de tela: mitigado fatiando por módulo (uma fatia =
  um módulo = um commit verificável) e pela varredura automatizada.
- Mensagens com valores interpolados (contagens, nomes de veículo) viram
  format strings; risco de placeholder errado — o teste de varredura confere
  que toda constante formatada é usada com as chaves que declara.
- O manual (`docs/manual/manual.html`) cita rótulos literalmente; se algum texto
  mudar além do declarado acima, o manual precisa mudar junto.
