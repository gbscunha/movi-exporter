Faça uma revisão do código alterado nesta sessão.

Analise nesta ordem:

1. **Wialon API** — flagsMask correto (0, não 65281)? gis_sid separado do sid? URLs dinâmicas? Odômetro convertido de metros?

2. **Dados do export** — campos N/D aplicados corretamente? Nenhum NaN visível? Colunas obrigatórias intactas?

3. **GUI** — chamadas à API passam pelos services? Nenhum acesso direto ao wialon_client da GUI?

4. **Erros** — `except Exception: pass` removidos? Logger sendo usado?

5. **Testes** — novos testes existem para a feature? Estão passando?

6. **Git** — `.env` fora do staging? Arquivos de log fora? Mensagem de commit no formato correto?

Para cada problema: indique arquivo e linha, explique o risco, sugira correção.
