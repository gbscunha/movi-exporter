# AI-DEV-SETUP.md — Guia de Auto-Configuração para o Claude Code

> **Para o Claude Code:** este arquivo NÃO é código do projeto. É um guia de
> meta-configuração. Sua tarefa ao ler este arquivo é ajudar a estabelecer (ou
> completar) a estrutura de desenvolvimento assistido por IA descrita abaixo,
> adaptada à stack real deste repositório. **Não crie nada antes de investigar o
> estado atual e me apresentar um plano.** Siga o protocolo da Seção 1.
>
> Depois que a estrutura estiver montada e validada, este arquivo pode ser
> removido do repo (ou mantido em `docs/` como referência do método).

---

## O que você vai montar

Um ambiente de desenvolvimento forte com IA, composto por:

1. **CLAUDE.md** — a constituição do projeto (enxuta, < 150 linhas)
2. **`.claude/skills/xp-cycle/SKILL.md`** — o ciclo de desenvolvimento (TDD/XP)
3. **`.claude/rules/`** — regras modulares (política de skills + convenções)
4. **`.claude/commands/`** — slash commands (`/new-feature`, `/my-verify`)
5. **`.claude/agents/`** — subagent verificador independente
6. **`docs/specs/` e `docs/decisions/`** — specs de feature e ADRs (Spec-Driven)
7. **`CHECKLIST.md` + `JOURNAL.md`** — rastreador de estado vivo (roadmap +
   "Onde estou", atômico) e journal cronológico do "porquê"

Tudo isso serve a um método com princípios fixos (Seção 2) e a um ciclo de
trabalho fixo (Seção 4), traduzidos para a stack específica deste projeto.

---

## SEÇÃO 1 — Protocolo de execução (siga nesta ordem)

### Passo 1 — Investigar (não altere nada ainda)
Antes de propor qualquer coisa, levante o estado real do repositório:

- Qual a stack? (linguagem, framework, gerenciador de pacotes — leia os arquivos
  de manifesto: package.json, .csproj, pyproject.toml, go.mod, Cargo.toml, etc.)
- Quais os comandos reais de dev, test, build, lint?
- Já existe um CLAUDE.md? Já existe alguma pasta `.claude/`? Já há testes?
- Já existe algum rastreador de estado (`CHECKLIST`, `JOURNAL`, ou um proto como
  `KICKOFF`/`ONDE-ESTOU`)?
- É greenfield (projeto novo/vazio) ou brownfield (já em andamento com código)?
- Há convenções já estabelecidas no código existente? (para brownfield: os
  padrões que você observar são o default e DEVEM ser respeitados. Se algum se
  mostrar frágil ou inconsistente, não o substitua por conta própria — aponte o
  problema no plano, proponha a alternativa com o motivo, e espere minha decisão)

### Passo 2 — Classificar o cenário
Determine e me diga qual é o caso:
- **Greenfield puro:** repo vazio ou quase. Você monta tudo do zero.
- **Greenfield com scaffold:** projeto recém-criado (ex: `dotnet new`, `create-
  next-app`), sem estrutura de IA. Monta tudo, alinhado ao scaffold.
- **Brownfield sem IA:** projeto maduro, sem CLAUDE.md nem `.claude/`. Monta a
  estrutura fazendo engenharia reversa dos padrões existentes.
- **Brownfield com IA parcial:** já tem CLAUDE.md e/ou `.claude/`. Você
  COMPLETA o que falta e NÃO sobrescreve o que existe sem me perguntar.

### Passo 3 — Propor o plano (esperar aprovação)
Entre em Plan Mode. Apresente:
- O cenário identificado e a stack detectada
- A lista exata de arquivos que você vai criar
- Para brownfield: o que você vai preservar e o que vai adicionar
- Os comandos da stack que vão preencher os pontos de tradução
- **A decisão ADR:** `docs/decisions/` formal ou a rota leve (gaveta "Dívidas
  arquiteturais" do CHECKLIST + JOURNAL) — ver 3.8/3.9
- **A decisão de versionamento** do CHECKLIST/JOURNAL: commitado no repo ou
  pessoal (gitignore)
- Qualquer outra decisão que precise de mim (ex: framework de teste, se não houver)

**PARE aqui e espere minha aprovação antes de criar qualquer arquivo.**

### Passo 4 — Construir (incremental)
Após aprovação, crie os arquivos na ordem da Seção 3. Ao terminar cada bloco,
me mostre o que criou antes de seguir. Não gere tudo de uma vez sem checkpoint.

### Passo 5 — Validar
- Confirme que os comandos no CLAUDE.md realmente funcionam nesta máquina/stack.
- Rode `grep -rn "{{" .` para garantir que nenhum placeholder ficou por preencher.
- Se criou referências entre arquivos (ex: CLAUDE.md → xp-cycle, CLAUDE.md →
  CHECKLIST), confirme que os caminhos existem e não vão quebrar futuras sessões.

---

## SEÇÃO 2 — Princípios do método (não-negociáveis)

Estes princípios guiam TODAS as decisões de estrutura. Internalize-os:

1. **CLAUDE.md enxuto.** Alvo < 150 linhas no root. Cada linha deve MUDAR seu
   comportamento. Se uma linha é só informativa e você a inferiria lendo o código,
   ela não entra. Detalhe vai em rules/skills/specs, nunca inflando o root.

2. **Progressive disclosure.** Informação detalhada é carregada sob demanda.
   Skills carregam quando relevantes; rules ativam por escopo; specs entram quando
   a feature começa. Não empurre tudo para o contexto de uma vez.

3. **Spec como infraestrutura.** O gargalo não é escrever código — é saber o que
   construir. Specs (o "quê") e ADRs (o "porquê") são versionados e persistentes,
   não descartados após o planejamento.

4. **TDD com pair programming.** Plan → Test (Red) → Implement (Green) → Refactor
   → Commit → Documentar. O humano é o piloto; você é o copiloto. Sempre.
   (Exceção consciente: se o projeto define outra estratégia de teste — ex:
   verificação manual até certa fase — o xp-cycle reflete ISSO, não um TDD que
   não acontece. Honestidade do documento acima de pureza do método.)

5. **Verificação independente.** Um agente separado verifica o trabalho do
   implementador. Nunca confie no relato de que algo funciona — rode e confira a
   saída real.

6. **Documento vivo.** A cada erro repetido, padrão novo ou decisão, atualize o
   arquivo relevante. O CLAUDE.md melhora com o uso.

7. **Regras do projeto vencem.** Skills externas e ferramentas complementam, nunca
   sobrescrevem, as regras deste projeto.

8. **Estado vivo separado da história.** O estado corrente (roadmap, "onde estou")
   fica num `CHECKLIST.md` curto e estável; a história datada (o que foi feito e
   por quê) vai append-only pro `JOURNAL.md`. A cada entrega, atualiza-se o estado
   e acrescenta-se a história — nunca se infla o CHECKLIST com registros datados.
   É o que mantém o mapa legível enquanto o histórico cresce sem limite.

---

## SEÇÃO 3 — O que criar (conteúdo de cada arquivo)

Traduza todos os pontos marcados com 🔧 para a stack detectada no Passo 1.

### 3.1 — CLAUDE.md (root)
Estrutura-alvo (adapte, mantendo < 150 linhas):
- **Abertura:** 2-4 linhas — o que o projeto é, stack principal, idioma.
- **Estrutura:** árvore simplificada dos diretórios de topo.
- **Comandos** 🔧: dev, test, build, lint reais desta stack. Inclua qualquer
  pegadinha de ambiente (ex: versão de runtime, PATH, variável necessária).
- **Convenções:** só o que você NÃO infere do código. Nada que o linter já cobre.
- **Git:** branch por feature; Conventional Commits; `git add` específico (NUNCA
  `git add .`); nunca commitar segredos/build/`.env`.
- **Verificação:** o gate antes de concluir (rodar test + build + lint) 🔧.
- **Ciclo de Desenvolvimento:** referência a `.claude/skills/xp-cycle/SKILL.md` +
  resumo de uma linha do ciclo.
- **Estado do projeto:** uma linha apontando que toda sessão abre lendo "Onde
  estou" no `CHECKLIST.md` e fecha registrando no `JOURNAL.md`.
- **Skills do ecossistema:** referência a `.claude/rules/skills-policy.md`.
- **Não faça:** guardrails específicos do projeto (cresce com o uso).
- **Compactação:** o que preservar quando o contexto for resumido.

### 3.2 — `.claude/skills/xp-cycle/SKILL.md`
- Frontmatter YAML com `name: xp-cycle` e uma `description` escrita para
  AUTO-INVOCAÇÃO (deixe claro: usar sempre que implementar feature, corrigir bug
  ou refatorar).
- As 6 etapas do ciclo (Plan → Red → Green → Refactor → Commit → Documentar),
  com os comandos de teste/build/lint desta stack 🔧.
- Tabela de stack de testes 🔧 (camada → ferramenta → localização dos testes).
- Checklist de invariantes do projeto (preencha com as invariantes que
  levantarmos — isolamento de dados, acesso, segredos, regras críticas).
- Seção de anti-patterns (implementar antes de testar, commit gigante, refatorar
  com testes falhando, `git add .`, rodar no automático sem revisar o plano,
  fechar entrega sem atualizar CHECKLIST/JOURNAL).

### 3.3 — `.claude/rules/skills-policy.md`
Política de descoberta/uso de skills externas (genérica, mesma para todo projeto):
gate de confirmação obrigatório antes de instalar; auditar o SKILL.md antes;
escopo no projeto e versionado; as regras do projeto vencem em conflito.

### 3.4 — `.claude/rules/code-conventions.md`
Convenções específicas desta stack/projeto 🔧: estrutura de arquivos, padrão de
criação de novo recurso, acesso a dados, tratamento de erros, "sempre faça /
nunca faça" da linguagem. Para brownfield: derive do código existente.

### 3.5 — `.claude/commands/new-feature.md`
Slash command que dispara o ciclo completo: recebe a descrição da feature, entra
em Plan Mode, escreve testes primeiro, implementa, refatora, sugere commit,
documenta (CHECKLIST + JOURNAL). Referencia o xp-cycle.

### 3.6 — `.claude/commands/my-verify.md`
Slash command de verificação independente: usa um subagent para revisar contra as
invariantes, rodar os testes de verdade, e checar o que foi entregue a mais e a
menos.

### 3.7 — `.claude/agents/code-reviewer.md`
Subagent verificador cético (frontmatter com name, description, tools; opcional
`model` para usar o modelo mais forte disponível). Nunca confia no relato; roda
os comandos e lê a saída real. Reporta com arquivo, linha, severidade e correção.

### 3.8 — `docs/specs/` e `docs/decisions/`
Crie `docs/specs/` e, se ajudar, um `FEATURE-template.md`. A spec cobre o "quê"
(com critérios de aceitação testáveis no formato DADO/QUANDO/ENTÃO).

**`docs/decisions/` (ADRs formais) é condicional** — só crie se a rota ADR formal
tiver sido escolhida no plano (Passo 3). Em projeto solo/pequeno, o padrão é a
rota leve: a gaveta "Dívidas arquiteturais" do CHECKLIST + o JOURNAL cobrem o
"porquê" e `docs/decisions/` NÃO é criado. Se a rota formal for escolhida, o ADR
cobre o "porquê" com as alternativas rejeitadas. Não crie as duas estruturas "por
garantia" — escolha uma e registre a escolha no JOURNAL.

### 3.9 — `CHECKLIST.md` + `JOURNAL.md` (estado vivo + journal)
O par que separa **estado** (onde estamos) de **história** (o que aconteceu). Um
serve à leitura diária; o outro à arqueologia sob demanda. Não confundir com
specs/ADRs (3.8): spec = o "quê" de uma feature, pra frente; CHECKLIST = o estado
corrente do projeto inteiro; JOURNAL = o "porquê", cronológico.

**`CHECKLIST.md` — estado corrente (alvo curto, ~250 linhas, estável):**
- **Bloco de protocolo no topo** — como ler e como atualizar o próprio arquivo (é
  o que impede que ele apodreça entre sessões/pessoas/IA). Regra central: toda
  entrega mexe só em "Onde estou" + o checkbox e gera entry datada no JOURNAL —
  NUNCA inflar o CHECKLIST com "Estado em DD-MM".
- **"Onde estou"** — âncora de continuidade (fase atual, último concluído, em
  andamento, próximo passo). É a primeira coisa que uma sessão nova lê.
- **Roadmap com checkboxes atômicos** 🔧 — por fase/fatia/entregável, na
  granularidade das fatias TDD. Estados: `[ ]` a fazer, `[x]` feito, `[~]` parcial.
- **Gavetas de contexto vivo:** "Carona no próximo PR" (mudanças pequenas demais
  pra PR próprio), "Pendências operacionais" (infra fora do código), "Dívidas
  arquiteturais conhecidas" (o que decidimos NÃO fazer agora e por quê), "Anotações
  (padrões permanentes)" (convenções duráveis que não cabem inflando o CLAUDE.md).

**`JOURNAL.md` — história datada (append-only, mais recente no topo):**
- Cabeçalho fixo dizendo: estado vivo fica no CHECKLIST; este arquivo responde
  "por que essa decisão foi tomada?".
- Uma entry por entrega: data + branch + o que foi feito + **decisões com racional**
  (e alternativas rejeitadas) + verificação (test/build/lint reais).

**A regra que liga os dois (o truque):** a cada entrega, atualize o *estado* no
CHECKLIST e *acrescente* a história no JOURNAL. Essa descarga é o que mantém o
CHECKLIST pequeno enquanto a história cresce sem limite — sem ela, o checklist
vira um log ilegível em meses.

**Semear:** greenfield → CHECKLIST a partir do roadmap inicial + JOURNAL vazio com
o cabeçalho. Brownfield → se já existe um rastreador (CHECKLIST/JOURNAL, ou um
proto como KICKOFF/ONDE-ESTOU), **gradue/complete** em vez de recriar; preserve o
histórico. Versionar ou manter pessoal (gitignore) é decisão do dono do repo —
pergunte no Passo 3.

---

## SEÇÃO 4 — O ciclo de trabalho (após o setup)

Uma vez montada a estrutura, toda sessão abre lendo **"Onde estou"** no
`CHECKLIST.md`, e todo trabalho de feature segue:

```
1. SPEC      Escrever/atualizar a spec da feature em docs/specs/
             (com critérios de aceitação testáveis)
   ↓
2. PLAN      Plan Mode: investigar, propor plano, esperar aprovação do humano
   ↓
3. TEST      Escrever os testes primeiro (Red) — devem falhar
   (Red)     [ou a estratégia de verificação definida pelo projeto]
   ↓
4. IMPLEMENT Código mínimo para passar (Green)
   ↓
5. REFACTOR  Melhorar com os testes protegendo
   ↓
6. COMMIT    Pequeno, específico, Conventional Commits, git add seletivo
   ↓
7. VERIFY    /my-verify — agente independente confere contra invariantes
   ↓
8. DOCUMENT  Atualizar CHECKLIST.md ("Onde estou" + checkbox) e o JOURNAL.md
             (entry datada); e CLAUDE.md/specs/ADR se surgiu padrão ou decisão
```

> **O passo 8 é o que mantém o par CHECKLIST/JOURNAL vivo:** o CHECKLIST guarda só
> o estado corrente (curto, estável) e o JOURNAL absorve a história datada — nunca
> inflar o CHECKLIST com "Estado em DD-MM".

---

## SEÇÃO 5 — Regras de adaptação por cenário

**Se GREENFIELD:** você tem liberdade para montar a estrutura ideal. Ainda assim,
proponha o plano antes. Sugira decisões abertas (ex: framework de teste) em vez
de assumir. Semeie o `CHECKLIST.md` a partir do roadmap inicial e abra um
`JOURNAL.md` vazio (só com o cabeçalho de uso).

**Se BROWNFIELD:** a regra de ouro é PRESERVAR. O objetivo é fazer você seguir os
padrões que o projeto JÁ tem, não impor novos. Especificamente:
- NÃO sobrescreva um CLAUDE.md existente — complemente ou me pergunte.
- Derive as convenções do código real, não de um ideal. Sugerir uma melhoria é
  permitido; adotá-la sem minha aprovação, não.
- Se o projeto já referencia arquivos (mesmo em formato antigo), me avise da
  divergência e proponha a correção — não quebre referências silenciosamente.
- Não introduza o ciclo com um big-bang de refatoração. A estrutura serve à
  PRÓXIMA feature; o código existente fica como está até haver motivo para mudar.
- Se já existe um rastreador de estado (`CHECKLIST`/`JOURNAL`, ou um proto como
  `KICKOFF`/`ONDE-ESTOU`), **gradue/complete** em vez de recriar do zero —
  preserve o histórico já registrado.

**Se as invariantes não estiverem claras:** pergunte. "O que neste projeto nenhum
teste pode violar?" é a pergunta que revela isolamento de dados, controle de
acesso, exigências legais e regras críticas. Não invente invariantes; extraia-as
de mim ou do código.

---

## SEÇÃO 6 — Ponto de partida

Comece agora pelo **Passo 1 da Seção 1**: investigue o repositório e me diga o que
encontrou (stack, comandos, cenário, rastreador de estado existente, estado atual
da estrutura de IA). Só então proponha o plano. Não crie nenhum arquivo antes da
minha aprovação.
