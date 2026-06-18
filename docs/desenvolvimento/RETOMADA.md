# Retomada — Onde paramos (2026-06-16 madrugada)

> Documento temporário. Apagar quando a Onda 3 fechar.

## Status do branch

- **Branch:** `feat/onda-3` (NÃO foi feito push ainda)
- **Working tree:** limpo (tudo commitado)
- **Base:** `main` está na v1.2.0 (Onda 2 já mergeada + release publicada)
- **Versão atual no código:** ainda `1.2.0` (bump pra 1.3.0 só no fim da Onda 3)

## Onda 3 (v1.3.0) — Experiência Visual

Plano completo: `docs/desenvolvimento/PLANO_ONDA_3.md`

| Fase | Tema | Status |
|------|------|--------|
| 01 | Ícones FontAwesome | ✅ |
| 02 | Light mode + Toast | ✅ |
| 03 | Identidade Movi + freeze + seleção de veículos (4 pedidos do cliente) | ✅ |
| 04 | Home com conteúdo + Sidebar polish + diálogo "Sobre" (#07, #09, #23) | ⬜ **próxima** |
| 05 | Resto do Export (#14 progresso real, #13 checkboxes agrupados, #17 toolbar do log) | ⬜ |
| 06 | Settings polish (#20 alterações não salvas, #21 validação inline) | ⬜ |
| 07 | Atalhos de teclado (#22) | ⬜ |

**Testes:** 167 passando · ruff limpo.

## O que foi entregue nesta sessão (resumo)

1. **FontAwesome** — emojis de chrome substituídos por ícones (CTkImage via Pillow). `src/gui/icons.py`. Pillow virou dependência.
2. **Light mode** — `APP_THEME` persistido no .env; dropdown Escuro/Claro/Sistema. Fix de contraste da sidebar inativa. Fix das cores do log (INFO sumia no claro).
3. **Toast/snackbar** — `src/gui/components/toast.py`. Info/sucesso + aviso de export sem dados.
4. **Paleta Movi** — vermelho #FF0E10 via `src/gui/theme.py`. Logo na sidebar (`assets/movi-logo.png`, já commitada).
5. **Freeze ao trocar conta** — resolvido: estado de seleção separado da renderização, cap de 120 + "Mostrar mais".
6. **Seleção de veículos (#15)** — busca por nome/placa/ID, marcar/desmarcar filtrados, contador, default nenhum.
7. **Suntech model 170** — perfil ampliado (ALT/UEX), bug "Bateria dispositivo"→interna corrigido, slots deixam de ser chutados (vêm do sensor_map; m_asgn1=odô só no model 197).

## Descobertas técnicas importantes (não esquecer)

- **Slots Suntech `s_asgn`/`m_asgn` variam por modelo.** ST380 (197): s_asgn1=veículo, m_asgn1=odômetro. model 170: s_asgn1=interna, m_asgn1≠odômetro. Por isso o perfil NÃO chuta mais os slots — confia no sensor_map do admin (correto por dispositivo). Se aparecer 3º modelo Suntech, mesma lógica vale.
- **Cliente tem 3+ tipos de tracker:** Suntech ST380 (197), Jimi VL03, Suntech model 170. O aviso #41 (tracker desconhecido no DefaultProfile) está ativo e foi quem revelou o model 170 — fica de olho no `app.log` se aparecer outro `model=`/`rep_type=` desconhecido.

## Decisão de produto pendente (perguntei, cliente não respondeu)

- **Linhas com "Tensão do Veículo = 0"** no BPO1J33 (model 170): o device enviou `s_asgn2=0` (provável corte de energia externa). Hoje mostramos **0** (dado real). Cliente pode querer trocar por **N/D**. Decisão dele — sem ação até confirmar.

## Validações feitas (confiáveis)

- Export cobre o **mês inteiro** (testado: VTR05/Abril → dados dos dias 1 a 28, 23.052 msgs, intervalo pedido 01/04 00:00 → 30/04 23:59). App NÃO precisa estar aberto no período; lê histórico armazenado na Wialon.
- Voltagens corretas no BPO1J33 após fix (Bateria Interna 3.8V, Veículo 12.x).

## Limpeza pendente (opcional)

- Exports de teste em `exports/2026-04/` e `exports/2026-05/` — posso apagar (são gitignored, só ocupam disco).
- Scripts de debug em `/tmp/` (somem ao reiniciar a máquina).

## Próximos passos quando voltar

1. **(rápido) QA visual com a logo** — abrir o app (`source venv/bin/activate && python -m src.gui.main`) e ver a logo na sidebar + tema vermelho em dark/light.
2. **Fase 04** — Home com conteúdo útil (último export, sugestão de mês), sidebar polish (separadores, footer clicável), diálogo "Sobre".
3. Ou, se quiser entregar logo: **fechar a Onda 3 aqui** (bump 1.3.0 + push + PR + merge + tag) — já tem muito valor acumulado.

## NÃO feito (intencional)

- ❌ Push do branch `feat/onda-3`
- ❌ Bump de versão pra 1.3.0
- ❌ PR / merge / tag
