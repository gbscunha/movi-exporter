Implemente a próxima fase pendente do `docs/desenvolvimento/PLANO_ONDA_1.md`.

Siga este ciclo:

1. **CONSULTAR** — Leia o PLANO_ONDA_1.md e identifique a próxima fase com status ⬜ Todo.
   Leia todos os arquivos que serão modificados antes de qualquer edição.

2. **IMPLEMENTAR** — Execute exatamente o que está descrito na fase, nem mais nem menos.
   Uma fase por vez. Não misture com outras fases.

3. **VERIFICAR** — Antes de commitar:
   - `pytest -q` — todos os testes passam
   - `ruff check src/` — zero erros
   - Confirme que o app ainda abre normalmente

4. **COMMITAR** — Use a mensagem de commit sugerida no plano.
   Formato: `tipo(escopo): descrição em imperativo`

5. **ATUALIZAR** — Marque a fase como ✅ na tabela do PLANO_ONDA_1.md e commite a atualização.
