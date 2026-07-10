# PLANO_MANUAL — Onda 5: Manual do Usuário robusto e self-sufficient

> **Objetivo:** transformar o manual embarcado (`docs/manual/manual.html`) no
> **único documento** que conduz o usuário final do zero ao primeiro relatório —
> instalação, geração de token, Google Drive, variáveis de ambiente e **todas** as
> funcionalidades do app (v1.4.0). **Text-first:** o manual precisa ser 100% útil
> **sem depender de screenshots**.
>
> **Contexto:** 1 cliente em produção (Windows), mantenedor solo. O manual é aberto
> de dentro do app pelo botão **Manual** (rodapé da sidebar) → abre no navegador
> via `src/gui/manual.py`. É o que o cliente realmente vê.

## Diagnóstico (estado atual)

| Documento | Público | Estado | Destino nesta onda |
|-----------|---------|--------|--------------------|
| `docs/manual/manual.html` | Cliente final (embarcado) | Defasado (v1.3.0; sem Motorista/Endereço; 11 placeholders de imagem vazios) | **Fonte única** — recebe tudo |
| `docs/cliente/GUIA_CONFIGURACAO.md` | Cliente (setup) | OK, mas separado do manual | Conteúdo **absorvido** → arquivar/redirect |
| `docs/cliente/USER_GUIDE.md` | Dev / CLI | Drifts (v1.0.0; cita `base_client.py` deletado; `odometer` "N/A"; checklist errado) | Corrigir e marcar como **doc de dev** |

**Fatos verificados no código (contrato a respeitar no texto):**

- App em **v1.4.0** (`src/gui/__init__.py`); manual diz 1.3.0 (hero + rodapé).
- Botão **Gerar** (Configurações) abre `https://hosting.wialon.com/login.html`;
  depois de logar, o token é criado em **Config. da conta → Aplicações → Tokens**
  (`settings.py:20-22, 236-238`). O texto atual do manual descreve um caminho
  inconsistente ("Aplicativos e tokens") — **corrigir**.
- **Salvar** grava no `.env` via `set_env_value` (`settings.py:240-263`); **Testar**
  valida e mostra "Conectado como…". Ou seja, o usuário **não precisa** editar o
  `.env` à mão para o token — o app faz isso.
- Variáveis de ambiente (`core/config.py:41-53`): `WIALON_TOKEN`, `WIALON_TOKEN_2`,
  `WIALON_BASE_URL`, `EXPORT_DIR`, `WIALON_PAGE_SIZE`, `GOOGLE_DRIVE_CREDENTIALS_FILE`
  (default `./client_secrets.json`), `GOOGLE_DRIVE_FOLDER_ID`, `APP_THEME`.
- Export tem o checkbox **"Incluir endereço (mais lento)"** (default off,
  `export.py:202`) → coluna **Localização**. Coluna **Motorista** vem do RFID.
  Ambas caem para `N/D` quando não há dado/permissão.
- Requisito da coluna **Motorista**: token com ACL de **ver motoristas** + cartão
  com **"Código" preenchido** no Wialon (senão a coluna inteira vira `N/D`).
- `docs/wialon/TOKEN_AUTORIZACAO.md` — **referenciado no `CLAUDE.md` mas não existe**
  (drift a corrigir na Fase 5).

## Princípios desta onda

- **Text-first.** Todo o conteúdo é compreensível **sem imagens**. Os slots de
  imagem degradam de forma **invisível** (nada de caixas hachuradas "insira imagem
  aqui"). Imagens podem entrar depois, opcionalmente, sem retrabalho.
- **Single source of truth.** O usuário final não precisa de nenhum outro arquivo
  além do manual embarcado para se virar sozinho.
- **Preciso.** Todo passo confere com o comportamento real do app (fluxos, labels,
  nomes de variável). Nada de instrução "de memória".
- **Faseado e atômico.** Cada fase = uma branch = um commit; cada fase deixa o
  manual **abrível e coerente** (nada pela metade). Docs não alteram comportamento
  do app → risco baixo.

## Regras de execução (por fase)

1. **Branch** a partir da `main`: `docs/manual-<nome-curto>`.
2. **Implementar** apenas o escopo da fase.
3. **Verificar** (gate obrigatório):
   - Abrir `docs/manual/manual.html` no navegador → renderiza, layout íntegro,
     links do índice funcionam, **lê bem sem imagens**.
   - `pytest -q` verde e `ruff check src/` limpo (garante que nada no app quebrou;
     docs não deveriam afetar, mas é o gate padrão do projeto).
   - Se tocou `src/gui/manual.py` ou o build: confirmar que `open_manual()` acha o
     arquivo e que o bundle PyInstaller inclui `docs/manual/`.
4. **Commit** (Conventional Commits, PT-BR, frase única) + PR.
5. **Atualizar status** na tabela abaixo (⬜ → ✅).

## Status geral

| Fase | Descrição | Risco | Status |
|------|-----------|-------|--------|
| 0 | Fundação text-first + bump v1.4.0 | Baixo | ✅ Feito |
| 1 | Recursos v1.4.0: Motorista + Localização + "Entendendo o relatório" | Baixo | ⬜ Todo |
| 2 | Configuração inicial completa (token, fluxo real, self-sufficient) | Baixo | ⬜ Todo |
| 3 | Google Drive + variáveis de ambiente (`.env`) | Baixo | ⬜ Todo |
| 4 | Telas restantes (Geral/tema, atualizações, Home) + FAQ final | Baixo | ⬜ Todo |
| 5 | Consolidar docs de apoio (arquivar GUIA, corrigir USER_GUIDE, CLAUDE.md) | Baixo | ⬜ Todo |

---

## Fase 0 — Fundação text-first + bump de versão

**Branch:** `docs/manual-fundacao`

Preparar o terreno **sem adicionar conteúdo novo** — só a estrutura que sustenta o
resto da onda.

- [x] **Degradação invisível das imagens:** `onerror` dos 11 slots trocado para
      **ocultar o `figure` inteiro** (`this.closest('figure').style.display='none'`)
      quando a imagem não existe. Sem screenshots, o manual não mostra nenhum
      placeholder — só o texto. As `<img>` + `<figcaption>` permanecem no markup:
      se um dia caírem imagens em `docs/manual/img/`, renderizam com legenda, sem
      retrabalho. (Os `div.placeholder` antigos ficaram inertes — serão removidos
      pelas Fases 1–4 conforme cada seção é reescrita.)
- [x] **Bump de versão:** hero e rodapé de `1.3.0` → `1.4.0`.
- [x] **Índice cresce por fase** (decisão refinada): em vez de âncoras órfãs
      "em breve", cada Fase 1–4 adiciona sua entrada no `nav.toc` **junto** com a
      seção real. Assim a `main` fica coerente a cada PR (sem link apontando para
      seção inexistente).

**Verificação:** ✅ manual abre sem caixas de placeholder, versão 1.4.0 visível;
`grep closest('figure')` = 11 slots, 0 resíduos do `onerror` antigo; `pytest -q`
(237) verde; `ruff check src/` limpo.

---

## Fase 1 — Recursos da v1.4.0: Motorista + Localização

**Branch:** `docs/manual-v140`

Documentar as duas features-título da última release, hoje **ausentes**.

- [ ] **Passo "Fazer exportação":** adicionar o checkbox **"Incluir endereço (mais
      lento)"** à lista de opções — explicar que ativa a coluna Localização e deixa
      o export mais demorado (geocodificação), e que vem **desmarcado** por padrão.
- [ ] **Nova seção "Entendendo o relatório"** (a que faltava): tabela de **todas as
      colunas** do arquivo em PT-BR, com uma linha por coluna e o que significa —
      incluindo **Motorista** e **Localização**. Espelhar a tradução real
      (`exporter.py:71-95`).
- [ ] Explicar a coluna **Motorista**: vem do cartão RFID lido pelo veículo; sai
      `N/D` quando não há cartão na linha, quando o cartão está sem "Código", ou
      quando o token não tem permissão de ver motoristas.
- [ ] Explicar a coluna **Localização**: endereço geocodificado das coordenadas;
      só preenchida se o checkbox foi marcado; pontos sem endereço mapeado → `N/D`.
- [ ] **FAQ:** adicionar "Por que a coluna Motorista está vazia/N/D?" e "Por que
      não aparece o endereço?" apontando causa + como corrigir.

**Verificação:** conferir os nomes de coluna contra `exporter.py` (contrato de
colunas); manual abre e as duas seções/FAQ leem bem sem imagem.

---

## Fase 2 — Configuração inicial completa (token, self-sufficient)

**Branch:** `docs/manual-token`

Reescrever o passo do token com o **fluxo real**, para o usuário conseguir do zero.

- [ ] **Corrigir o fluxo do token** (hoje inconsistente). Caminho real:
  1. Configurações → seção **Wialon API — Conta 1** → botão **Gerar**.
  2. Abre `https://hosting.wialon.com/login.html` → logar com usuário/senha.
  3. Na Wialon: **Configurações da conta → Aplicações → Tokens → Criar**, validade
     **Ilimitado**, com acesso de **leitura** aos veículos **e a motoristas**
     (para a coluna Motorista funcionar).
  4. Copiar o token gerado.
- [ ] **Salvar e testar no app:** colar no campo Token → **Salvar** (grava no `.env`
      automaticamente) → **Testar** (mostra "Conectado como…" em verde). Deixar
      explícito que **não** é preciso editar arquivo nenhum à mão para o token.
- [ ] Dica do **botão de olho** (mostrar/ocultar token) — manter.
- [ ] **Segunda conta (opcional):** mesma coisa na seção "Conta 2"; explicar o
      **seletor de conta na sidebar** e as subpastas `Conta 1/` e `Conta 2/`.
- [ ] Nota de **ACL de motoristas** ligada aqui (o token precisa dela para a coluna
      Motorista) — cross-link com a Fase 1.

**Verificação:** seguir o passo a passo contra o app real (botão Gerar abre a URL
certa; Salvar → `.env`; Testar → "Conectado como…").

---

## Fase 3 — Google Drive + variáveis de ambiente

**Branch:** `docs/manual-drive-env`

Absorver o conteúdo do `GUIA_CONFIGURACAO.md` para o manual ser self-sufficient.

- [ ] **Seção Google Drive (opcional)** completa:
  - O que é preciso: arquivo `client_secrets.json` (**solicitar ao desenvolvedor**)
    na mesma pasta do `.exe`, e o **ID da pasta** de destino.
  - Como pegar o **ID da pasta**: abrir a pasta no Drive e copiar o trecho da URL
    (`.../folders/<ESTE_ID>`).
  - Onde configurar no app (seção Google Drive das Configurações) e o que os status
    "Encontrado"/"ID da pasta" significam.
  - Subpastas por conta (`Conta 1/`, `Conta 2/`) no envio automático.
- [ ] **Nova seção "Variáveis de ambiente (arquivo `.env`)"** — referência para
      quem quiser ajustes avançados:
  - Como criar o `.env` no Windows (Bloco de Notas → "Todos os arquivos" → `.env`,
    sem `.txt`) — passo do `GUIA_CONFIGURACAO`.
  - Tabela de **todas** as variáveis (`config.py:41-53`): `WIALON_TOKEN`,
    `WIALON_TOKEN_2`, `WIALON_BASE_URL`, `EXPORT_DIR`, `WIALON_PAGE_SIZE`,
    `GOOGLE_DRIVE_CREDENTIALS_FILE`, `GOOGLE_DRIVE_FOLDER_ID`, `APP_THEME` — com
    obrigatório/opcional, default e descrição.
  - Deixar claro: **token e ID da pasta o app já grava sozinho** pelas
    Configurações; editar o `.env` à mão só é necessário para as vars avançadas
    (`EXPORT_DIR`, `WIALON_PAGE_SIZE`).

**Verificação:** conferir nomes/defaults das variáveis contra `config.py` e
`.env.example`; manual abre e as duas seções leem bem sem imagem.

---

## Fase 4 — Telas restantes + FAQ final

**Branch:** `docs/manual-cobertura`

Fechar a cobertura de **todas** as funcionalidades e revisar o FAQ.

- [ ] **Configurações → Geral:** tema **Escuro/Claro/Sistema** (lembrado entre
      sessões) e o controle de **tamanho de página** (page size) da busca de
      histórico — o que é e quando mexer.
- [ ] **Tela inicial (Home):** detalhar o bloco **Resumo de exportações** (última
      exportação + botão abrir pasta, sugestão do próximo mês, estatísticas do ano)
      e os botões **Testar Conexões** / **Ver Veículos**.
- [ ] **Atualizações do app:** botão **Sobre** (versão, links) e a verificação
      automática de nova versão (como o app avisa e o que fazer).
- [ ] **FAQ final:** revisar/reordenar; garantir cobertura de: 0 registros, `N/D`,
      Tensão do Veículo vs. Bateria Interna, token não precisa reconfigurar, aviso
      do Windows, tema, onde abrir o manual, Motorista/Localização (das Fases 1–2).
- [ ] **Suporte:** rodapé com canal de contato (substituir placeholders do
      `GUIA_CONFIGURACAO` por um texto neutro combinado com o mantenedor).

**Verificação:** varrer o app tela a tela e confirmar que cada função aparece no
manual; manual abre e lê como um documento completo, coerente, sem imagens.

---

## Fase 5 — Consolidar docs de apoio

**Branch:** `docs/manual-consolidacao`

Agora que o manual é a fonte única, alinhar o resto da documentação.

- [ ] **`docs/cliente/GUIA_CONFIGURACAO.md`:** conteúdo já absorvido (Fases 2–3) →
      **arquivar** em `docs/arquivo/` **ou** reduzir a um redirect curto de uma
      linha apontando para o manual. (Decisão do mantenedor no PR.)
- [ ] **`docs/cliente/USER_GUIDE.md`** (doc de **dev/CLI**): corrigir drifts —
  - remover `base_client.py` da árvore (deletado na Onda 4);
  - versão/rodapé `1.0.0 / Jan 2025` → atual;
  - `odometer` "N/A" → lido de `params` (m→km) — conferir com `CLAUDE.md`;
  - tabela de flags do CLI: incluir `--upload/-u`, `--addresses/-A`, `--account/-a`;
  - checklist "Funcionalidades planejadas": Upload Drive já está pronto.
  - marcar no topo que é **doc técnico/CLI** (não o manual do cliente).
- [ ] **`CLAUDE.md`:** a referência a `docs/wialon/TOKEN_AUTORIZACAO.md` (inexistente)
      — recriar o arquivo **ou** repontar para a seção de token do manual.
- [ ] Atualizar `PLANO_MOTORISTA_RFID.md` Fase 04 (docs) e este plano (status).

**Verificação:** `grep -rn "base_client" docs/` volta vazio (ou só histórico
arquivado); `grep -rn "TOKEN_AUTORIZACAO" CLAUDE.md` aponta para algo que existe;
`pytest -q` + `ruff check src/`.

---

## NÃO fazer nesta onda (fora de escopo)

- ❌ **Capturar/produzir screenshots reais** — decisão explícita de ir *text-first*.
  Os slots ficam prontos para receber imagens depois, sem retrabalho.
- ❌ Gerar PDF ou versão impressa do manual (o HTML embarcado basta).
- ❌ Internacionalização (só PT-BR, 1 cliente).
- ❌ Documentar a API Wialon para o cliente final (isso é dev — fica no
  `docs/wialon-api-docs/` e no `USER_GUIDE.md`).
- ❌ Mudar o mecanismo de abertura do manual (`manual.py` já resolve dev + bundle).
