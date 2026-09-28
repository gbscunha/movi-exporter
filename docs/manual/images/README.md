# Imagens do manual

Os arquivos desta pasta são referenciados por `docs/manual/manual.html`. Enquanto
um print não existe, a figura correspondente **some** do manual (o `onerror` de
cada `<img>` esconde a figura), e o texto continua completo — nenhuma informação
vive só na imagem.

Salve cada print com exatamente o nome da tabela abaixo, em PNG.

## Como tirar

- **Tema do app:** escuro (o padrão), que é como o cliente vê.
- **Janela:** cerca de 1280×800. Para os recortes, capture só a área citada.
- **Tarjar:** token, e-mail e IDs de pasta com **tarja sólida** (retângulo cheio),
  nunca desfoque — desfoque pode ser revertido.
- **Sem informação nova:** o print ilustra o que o texto já diz.
- **Peso:** comprima antes de commitar (o PyInstaller empacota esta pasta dentro
  do `.exe`).

## Prints do manual

| Arquivo | Seção | O que capturar |
|---|---|---|
| `inicio-tour-janela.png` | Visão geral | Janela inteira na tela **Início**, com o menu lateral visível |
| `inicio-windows-aviso.png` | Primeiros passos | Aviso azul do Windows já expandido em **Mais informações**, mostrando **Executar assim mesmo** |
| `token-wialon-login.png` | Conectar sua conta Wialon | Página de login da Wialon aberta pelo botão **Gerar** |
| `token-wialon-url.png` | Conectar sua conta Wialon | Barra de endereços do navegador depois do login, com `access_token=` visível e **o token tarjado** |
| `token-config-conectado.png` | Conectar sua conta Wialon | Recorte da seção **Wialon API — Conta 1** com o status "Conectado como…" (token escondido pelo campo) |
| `conta2-seletor.png` | Adicionar uma segunda conta | Recorte do menu lateral com o seletor **Conta** aberto, mostrando o **nome de usuário** de cada conta (tarjar se o nome identificar alguém) |
| `drive-id-pasta.png` | Enviar para o Google Drive | Barra de endereços do Drive com o trecho depois de `/folders/` destacado (**ID tarjado**) |
| `drive-config.png` | Enviar para o Google Drive | Recorte da seção **Google Drive** com "Encontrado" em verde e o ID preenchido (**tarjado**) |
| `drive-google-autorizar.png` | Enviar para o Google Drive | Tela do Google pedindo autorização de acesso, no primeiro envio |
| `exportar-opcoes.png` | Exportar um mês | Tela **Exportar** antes de iniciar: mês, ano, formato e o bloco **OPÇÕES** |
| `exportar-escolher-veiculos.png` | Exportar um mês | Modo **Escolher manualmente** com busca preenchida e o contador de selecionados |
| `exportar-progresso.png` | Exportar um mês | Aba **Progresso** durante a exportação: barra, registro e o botão **Parar** |
| `exportar-concluida.png` | Exportar um mês | Registro com "EXPORTAÇÃO CONCLUÍDA" e a lista de arquivos gerados |
| `arquivos-pasta-mes.png` | Encontrar os arquivos | Explorador do Windows em `exports\AAAA-MM\` com os arquivos à vista |
| `arquivos-excel.png` | Encontrar os arquivos | Um relatório aberto no Excel, mostrando o cabeçalho e algumas linhas |
| `inicio-resumo.png` | Acompanhar pela tela Início | Recorte do bloco **Resumo de Exportações** com uma última exportação preenchida |

## Se um print não existir

Nada quebra: a figura simplesmente não aparece. Dá para entregar o manual com
parte das imagens e completar depois — basta salvar o arquivo com o nome certo
nesta pasta.
