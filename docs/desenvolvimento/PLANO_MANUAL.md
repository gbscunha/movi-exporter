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
- Fluxo de token **confirmado pelo mantenedor**: botão **Gerar** abre o login da
  Wialon; após logar, o **token volta na própria URL** (após `access_token=`) e é
  copiado para o app. O comentário em `settings.py:20-22` sugeria criar o token em
  "Config. da conta → Aplicações → Tokens", mas **não é** o fluxo usado. O botão
  está **correto** — sem fix de código. Corrigido no manual na Fase 2.
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
| 1 | Recursos v1.4.0: Motorista + Localização + "Entendendo o relatório" | Baixo | ✅ Feito |
| 2 | Configuração inicial completa (token, fluxo real, self-sufficient) | Baixo | ✅ Feito |
| 3 | Google Drive + variáveis de ambiente (`.env`) | Baixo | ✅ Feito |
| 4 | Telas restantes (Geral/tema, atualizações, Home) + FAQ final | Baixo | ✅ Feito |
| 5 | Consolidar docs de apoio (arquivar GUIA, corrigir USER_GUIDE, CLAUDE.md) | Baixo | ✅ Feito |

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
      retrabalho. (Os 11 `div.placeholder` antigos e a CSS órfã `.shot .placeholder`
      foram removidos — 1 na Fase 3 e os 10 restantes numa varredura final ao fim
      da onda.)
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

- [x] **Passo "Fazer exportação":** checkbox **"Incluir endereço (mais lento)"**
      adicionado às opções — ativa a coluna Localização, deixa o export mais
      demorado (geocodificação) e vem **desmarcado** por padrão.
- [x] **Nova seção "Entendendo o relatório"** (step 8): tabela das **18 colunas** do
      arquivo em PT-BR na ordem real, uma linha por coluna, incluindo **Motorista**
      e **Localização**. Traduções conferidas 1:1 contra `exporter.py:71-95`.
- [x] Explicou a coluna **Motorista** (box + FAQ): RFID; `N/D` sem cartão, sem
      "Código" ou sem ACL de ver motoristas.
- [x] Explicou a coluna **Localização** (box + FAQ): endereço geocodificado; só se
      o checkbox foi marcado; sem endereço mapeado → `N/D`.
- [x] **FAQ:** duas entradas novas ("coluna Motorista vazia — como preencher?" e
      "coluna Localização vazia — por quê?"). FAQ passou de 7 → 9 itens.

**Verificação:** ✅ 18 linhas na tabela; script cruzou as 20 traduções do
`exporter.py` → nenhuma faltando; `<section>` balanceado (10/10); `pytest -q` (237)
verde; `ruff check src/` limpo; manual reaberto no navegador.

---

## Fase 2 — Configuração inicial completa (token, self-sufficient)

**Branch:** `docs/manual-token`

Reescrever o passo do token com o **fluxo real**, para o usuário conseguir do zero.

- [x] **Fluxo do token corrigido** — o passo 2.2 mandava criar token em
      "Configurações da conta → Aplicativos e tokens" (errado). Fluxo real
      (confirmado pelo mantenedor):
  1. Configurações → seção **Wialon API — Conta 1** → botão **Gerar** (abre o login
     da Wialon no navegador).
  2. Logar e autorizar.
  3. A Wialon devolve o **token na barra de endereços**, após `access_token=`.
  4. Copiar esse trecho da URL e colar no app.
- [x] **Salvar e testar:** seção 2.3 (Salvar grava o token; Testar → "Conectado
      como…") já estava correta — mantida.
- [x] Box **"Onde está o token?"** apontando o `access_token=` na URL.
- [x] Box **"Para a coluna Motorista funcionar"** (ACL de ver motoristas +
      "Código" do cartão) — cross-link com a Fase 1.
- [x] **Segunda conta:** já coberta pela seção 5 do manual — mantida.

**Verificação:** ✅ `grep "Aplicativos e tokens"` = 0 (texto errado removido);
`access_token=` presente; `<section>` 10/10; `pytest -q` (237) verde; `ruff` limpo;
manual reaberto. Fluxo validado com o mantenedor.

---

## Fase 3 — Google Drive + variáveis de ambiente

**Branch:** `docs/manual-drive-env`

Absorver o conteúdo do `GUIA_CONFIGURACAO.md` para o manual ser self-sufficient.

- [x] **Seção Google Drive (opcional)** completa (4.1 o que precisa · 4.2 achar o
      ID da pasta · 4.3 configurar no app · box de subpastas por conta):
  - O que é preciso: arquivo `client_secrets.json` (**solicitar ao desenvolvedor**)
    na mesma pasta do `.exe`, e o **ID da pasta** de destino.
  - Como pegar o **ID da pasta**: abrir a pasta no Drive e copiar o trecho da URL
    (`.../folders/<ESTE_ID>`).
  - Onde configurar no app (seção Google Drive das Configurações) e o que os status
    "Encontrado"/"ID da pasta" significam.
  - Subpastas por conta (`Conta 1/`, `Conta 2/`) no envio automático.
- [x] **Nova seção "Variáveis de ambiente" (seção 9, avançado)** — referência para
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

**Verificação:** ✅ as 8 variáveis do `config.py` conferidas 1:1 na tabela (script);
`<section>` 11/11; âncora `#env` com TOC + seção; `pytest -q` (237) verde; `ruff`
limpo; manual reaberto. Placeholder da figura do Drive removido (limpeza incremental).

---

## Fase 4 — Telas restantes + FAQ final

**Branch:** `docs/manual-cobertura`

Fechar a cobertura de **todas** as funcionalidades e revisar o FAQ.

- [x] **Configurações (Geral + Exportação):** nova **seção 10 "Preferências e
      atualizações"** — tema Escuro/Claro/Sistema (lembrado) e o slider "Registros
      por página" (100–5000, padrão 1000). Também corrigi a faixa do page size na
      tabela da Fase 3 (estava "500–2000"; o slider real é **100–5000**).
- [x] **Tela inicial (Home):** já coberta pela seção 3 (Resumo de exportações com
      abrir pasta + sugestão de mês + estatísticas do ano; botões Testar Conexões /
      Ver Veículos) — mantida.
- [x] **Atualizações do app:** seção 10 (botão Sobre + verificação automática) +
      FAQ "Como sei se saiu uma versão nova?".
- [x] **FAQ final:** cobertura conferida (0 registros, N/D, tensões, token, aviso
      do Windows, tema, manual, Motorista/Localização); +1 item de atualização
      (FAQ 9 → 10).
- [x] **Suporte:** rodapé do manual já é neutro ("entre em contato com o suporte").
      Placeholders (email/WhatsApp `XX`) vivem no `GUIA_CONFIGURACAO` → Fase 5.

**Verificação:** ✅ page size 100–5000 (não 500–2000); `#prefs` com TOC + seção;
`<section>` 12/12; FAQ 10 itens; `pytest -q` (237) verde; `ruff` limpo; manual
reaberto e lido de ponta a ponta sem imagens.

---

## Fase 5 — Consolidar docs de apoio

**Branch:** `docs/manual-consolidacao`

Agora que o manual é a fonte única, alinhar o resto da documentação.

- [x] **`GUIA_CONFIGURACAO.md` arquivado** em `docs/arquivo/` (decisão do
      mantenedor). Conteúdo já absorvido nas Fases 2–3; manual é a fonte única.
- [x] **`USER_GUIDE.md`** marcado no topo como doc **dev/CLI** e drifts corrigidos:
      `base_client.py` removido da árvore; rodapé `1.0.0/Jan 2025` → v1.4.0;
      `odometer` "N/A" → `params` (m→km); flags `--upload/-u`, `--addresses/-A`,
      `--account/-a` adicionadas; checklist com Upload Drive concluído; fluxo de
      token (4.3) repontado para o manual.
- [x] **`CLAUDE.md`:** referência fantasma a `TOKEN_AUTORIZACAO.md` **repontada
      para o manual** (decisão do mantenedor) — na linha do Token e na lista de
      estrutura (que agora inclui `docs/manual/` e `docs/cliente/`). Mesma correção
      em `.claude/skills/wialon-api.md`.
- [x] **`PLANO_MOTORISTA_RFID.md`:** Fase 04 já concluída na v1.4.0 — mantido como
      registro histórico (a menção ao GUIA descreve o que foi feito na época).

**Verificação:** ✅ `grep TOKEN_AUTORIZACAO` limpo em `CLAUDE.md`/skills/docs ativos
(resta só uma string de permissão em `settings.local.json`); `base_client` = 0 no
USER_GUIDE; GUIA em `docs/arquivo/`; flags CLI presentes; `pytest -q` (237) verde;
`ruff check src/` limpo.

---

## NÃO fazer nesta onda (fora de escopo)

- ❌ **Capturar/produzir screenshots reais** — decisão explícita de ir *text-first*.
  Os slots ficam prontos para receber imagens depois, sem retrabalho.
- ❌ Gerar PDF ou versão impressa do manual (o HTML embarcado basta).
- ❌ Internacionalização (só PT-BR, 1 cliente).
- ❌ Documentar a API Wialon para o cliente final (isso é dev — fica no
  `docs/wialon-api-docs/` e no `USER_GUIDE.md`).
- ❌ Mudar o mecanismo de abertura do manual (`manual.py` já resolve dev + bundle).
