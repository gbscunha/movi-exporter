"""Todo o texto que o usuário lê no app, num lugar só.

Para ajustar uma mensagem, edite aqui — os módulos da GUI não têm texto
embutido (`tests/test_messages.py` garante isso). Uma classe por tela.

Convenções:
- O texto NÃO inclui o espaçamento de ícone: onde o botão precisa de recuo,
  quem usa escreve `text=f"  {SettingsMsg.BTN_SALVAR}"`.
- Texto com valor variável usa chave nomeada e `.format(...)`:
  `SettingsMsg.STATUS_FALHA.format(erro=e)`.
- Nada de nome de arquivo interno (`.env`, `token.json`) em mensagem — é
  detalhe de implementação que não ajuda o cliente.

Fora daqui ficam os logs técnicos (`logger.*`, que vão para o `app.log`) e as
mensagens de exceção dos services — não são texto de interface.
"""


class Common:
    """Textos usados em mais de uma tela."""

    TITULO_ERRO = "Erro"
    TITULO_AVISO = "Aviso"
    BTN_ABRIR_PASTA = "Abrir pasta"

    # Nomes dos meses: texto visível (dropdown e resumos) e também índice —
    # `MESES.index(nome) + 1` dá o número do mês. A ordem importa.
    MESES = [
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]


class AppMsg:
    """Janela principal."""

    TITULO_JANELA = "Movi Exporter v{versao}"
    TITULO_SETUP = "Configuração necessária"
    TEXTO_SETUP = (
        "O token da API Wialon ainda não foi configurado.\n\n"
        "Abra a tela de Configurações para colar seu token e testá-lo "
        "antes de iniciar uma exportação."
    )


class SettingsMsg:
    """Tela de Configurações."""

    TITULO = "Configurações"

    # Rodapé (barra de salvar)
    BTN_SALVAR_ALTERACOES = "Salvar alterações"
    AVISO_NAO_SALVO = "Você tem alterações não salvas"
    TOAST_CONFIG_SALVA = "Configurações salvas"
    ERRO_SALVAR_CONFIG = "Não foi possível salvar: {erro}"

    # Seção Wialon
    SECAO_WIALON = "Wialon API — Conta {conta}"
    LABEL_TOKEN = "Token:"
    PLACEHOLDER_TOKEN = "Cole seu token Wialon aqui"
    BTN_GERAR = "Gerar"
    BTN_SALVAR = "Salvar"
    BTN_TESTAR = "Testar"

    STATUS_SEM_TOKEN = "Status: sem token configurado"
    STATUS_NAO_TESTADO = "Status: Não testado — clique em Testar"
    STATUS_SALVO = "Status: Token salvo com sucesso!"
    STATUS_TESTANDO = "Status: Testando conexão..."
    STATUS_CONECTADO = "Status: Conectado"
    STATUS_CONECTADO_COMO = 'Status: Conectado como "{usuario}"'
    STATUS_FALHA = "Status: Falha — {erro}"

    ERRO_TOKEN_VAZIO_SALVAR = "Cole um token válido antes de salvar."
    ERRO_TOKEN_VAZIO_TESTAR = "Cole um token antes de testar a conexão."
    ERRO_SALVAR_TOKEN = "Não foi possível salvar o token: {erro}"
    TOAST_TOKEN_SALVO = "Token da Conta {conta} salvo"

    # Seção Exportação
    SECAO_EXPORTACAO = "Exportação"
    LABEL_DIRETORIO = "Diretório:"
    LABEL_REGISTROS_POR_PAGINA = "Registros por página:"
    TITULO_ESCOLHER_DIRETORIO = "Selecione o diretório de exportação"

    # Seção Google Drive
    SECAO_DRIVE = "Google Drive"
    LABEL_CREDENCIAIS = "Credenciais:"
    CREDENCIAIS_ENCONTRADAS = "Encontrado"
    CREDENCIAIS_AUSENTES = "Não encontrado"
    CREDENCIAIS_ARQUIVO = "{arquivo} ({situacao})"
    LABEL_ID_PASTA = "ID da pasta no Drive:"
    PLACEHOLDER_ID_PASTA = "ID da pasta no Google Drive"
    TOAST_ID_COPIADO = "ID da pasta copiado"
    TITULO_PASTA_NAO_CONFIGURADA = "Pasta não configurada"
    AVISO_PASTA_NAO_CONFIGURADA = "Informe o ID da pasta do Drive primeiro."

    # Seção Geral
    SECAO_GERAL = "Geral"
    LABEL_TEMA = "Tema:"
    TEMA_ESCURO = "Escuro"
    TEMA_CLARO = "Claro"
    TEMA_SISTEMA = "Sistema"
    TOAST_TEMA_ALTERADO = "Tema alterado para {tema}"


class ValidationMsg:
    """Erros de validação de campo (módulo `validation.py`)."""

    DIRETORIO_OBRIGATORIO = "Informe um diretório de exportação."
    TOKEN_OBRIGATORIO = "Cole um token antes de continuar."


class ExportMsg:
    """Tela Exportar — campos, opções e botões."""

    TITULO = "Exportar Dados"

    LABEL_MES = "Mês:"
    LABEL_ANO = "Ano:"
    LABEL_FORMATO = "Formato:"

    GRUPO_OPCOES = "OPÇÕES"
    OPCAO_CONSOLIDADO = "Gerar arquivo consolidado"
    OPCAO_UPLOAD = "Upload para Google Drive"
    OPCAO_ENDERECO = "Incluir endereço (mais lento)"

    ABA_VEICULOS = "Veículos"
    ABA_PROGRESSO = "Progresso"

    MODO_TODOS = "Todos os veículos"
    MODO_MANUAL = "Escolher manualmente"
    BTN_CARREGAR = "Carregar"
    BTN_CARREGANDO = "Carregando..."
    PLACEHOLDER_BUSCA = "🔍  Buscar por nome, placa ou ID"

    BTN_MARCAR_TODOS = "Marcar todos"
    BTN_LIMPAR_TODOS = "Limpar todos"
    BTN_MARCAR_FILTRADOS = "Marcar filtrados"
    BTN_LIMPAR_FILTRADOS = "Limpar filtrados"
    CONTADOR_SELECAO = "{marcados} de {total} selecionados"
    CONTADOR_SELECAO_FILTRO = (
        "{marcados} de {total} selecionados · {filtrados} no filtro"
    )
    VEICULO_COM_PLACA = "{nome}  ·  {placa}"

    LABEL_PROGRESSO = "Progresso:"
    BTN_INICIAR = "Iniciar Exportação"
    BTN_PARAR = "Parar"
    BTN_PARANDO = "Parando..."

    # Estados curtos mostrados ao lado de "Progresso:"
    ESTADO_INICIANDO = "Iniciando..."
    ESTADO_CANCELANDO = "Cancelando..."
    ESTADO_CANCELADO = "Cancelado"
    ESTADO_CONCLUIDO = "Concluído"
    ESTADO_SEM_DADOS = "Sem dados"
    ESTADO_PROCESSANDO = "Processando {atual}/{total} — {veiculo}"

    # Confirmação antes de iniciar
    TITULO_CONFIRMAR = "Confirmar exportação"
    RESUMO_CONFIRMACAO = (
        "Mês/Ano:  {mes} / {ano}\n"
        "Formato:  {formato}\n"
        "Veículos:  {alvo}\n"
        "Consolidado:  {consolidado}\n"
        "Incluir endereço:  {endereco}\n"
        "Upload Google Drive:  {upload}\n\n"
        "Iniciar a exportação?"
    )
    ALVO_SELECIONADOS = "{quantidade} veículo(s) selecionado(s)"
    SIM = "sim"
    NAO = "não"

    TITULO_SEM_SELECAO = "Nenhum veículo selecionado"
    AVISO_SEM_SELECAO = "Marque ao menos um veículo ou escolha 'Todos os veículos'."
    ERRO_MES_ANO = "Mês/ano inválidos."
    ERRO_ABRIR_PASTA = "Não foi possível abrir a pasta: {erro}"
    ERRO_SALVAR_LOG = "Não foi possível salvar o log: {erro}"

    TITULO_SALVAR_LOG = "Salvar log"
    ARQUIVO_TEXTO = "Arquivo de texto"
    NOME_PADRAO_LOG = "movi-exporter-log.txt"

    TOAST_LOG_COPIADO = "Log copiado"
    TOAST_LOG_SALVO = "Log salvo"
    TOAST_LOG_VAZIO = "Log vazio — nada para salvar"
    TOAST_SEM_DADOS = "Nenhum dado disponível para o período"
    TOAST_CONCLUIDA = "Exportação concluída — {registros} registros"
    TOAST_CANCELADA = "Exportação cancelada"

    STATUS_CONCLUIDA = "Exportação concluída: {veiculos} veículos"
    STATUS_SEM_DADOS = "Exportação sem dados para o período"
    STATUS_CANCELADA = "Exportação cancelada"
    STATUS_ERRO = "Erro: {erro}"


class ExportLog:
    """Linhas do registro de progresso da exportação (aba Progresso)."""

    SEPARADOR = "═" * 50

    CONTA_ALTERADA = "Conta alterada para {conta}."
    CONECTANDO = "🔌 Conectando ao Wialon..."
    BUSCANDO_VEICULOS = "📡 Buscando lista de veículos..."
    VEICULOS_CARREGADOS = "{quantidade} veículos carregados"
    ERRO_CARREGAR_VEICULOS = "Erro ao carregar veículos: {erro}"

    PERIODO = "📅 Exportando: {mes:02d}/{ano}"
    FORMATO = "📁 Formato: {formato}"
    ENDERECO_INCLUIDO = "📍 Endereço: incluído (geocodificação ativada)"
    VEICULOS_SELECIONADOS = "🚗 Veículos selecionados: {quantidade}"
    TODOS_OS_VEICULOS = "🚗 Todos os veículos"

    CANCELAMENTO_SOLICITADO = (
        "⏹️  Cancelamento solicitado — encerrando após o veículo atual..."
    )

    TITULO_CONCLUIDA = "EXPORTAÇÃO CONCLUÍDA"
    VEICULOS = "Veículos: {processados}/{total}"
    REGISTROS = "Registros: {registros}"
    TAXA_SUCESSO = "Taxa de sucesso: {taxa:.1f}%"
    ARQUIVOS_GERADOS = "Arquivos gerados:"
    ARQUIVO = "  📄 {arquivo}"
    UPLOAD = "Upload: {enviados}/{total} arquivos"
    ERROS = "Erros:"
    ERRO_ITEM = "  {erro}"
    ERRO_EXPORTACAO = "\n❌ Erro na exportação: {erro}"

    TITULO_SEM_DADOS = "⚠️  NENHUM DADO DISPONÍVEL PARA O PERÍODO"
    VEICULOS_PROCESSADOS = "Veículos processados: {processados}/{total}"
    POSSIVEIS_CAUSAS = "Possíveis causas:"
    CAUSA_INATIVOS = "  • Veículos inativos no período selecionado"
    CAUSA_RETENCAO = "  • Limite de retenção de histórico da conta Wialon"
    CAUSA_PERIODO_ANTIGO = "  • Mês/ano muito antigos"

    TITULO_CANCELADA = "⏹️  EXPORTAÇÃO CANCELADA"
    PROCESSADOS_ANTES_DE_PARAR = "Processados antes de parar: {processados}/{total}"
    ARQUIVOS_PARCIAIS = (
        "Arquivos parciais gerados: {quantidade} "
        "(consolidado e upload não foram executados)"
    )


class HomeMsg:
    """Tela Início."""

    TITULO = "Bem-vindo ao Movi Exporter"
    SUBTITULO = "Exportação automatizada de dados de veículos Wialon"

    GRUPO_ACOES = "Ações Rápidas"
    BTN_TESTAR_CONEXOES = "Testar Conexões"
    BTN_VER_VEICULOS = "Ver Veículos"

    CARD_WIALON = "Wialon API"
    CARD_DRIVE = "Google Drive"
    CARD_VEICULOS = "Veículos"
    CARD_VERIFICANDO = "Verificando..."
    CARD_CONECTADO = "Conectado"
    CARD_DESCONECTADO = "Desconectado"
    CARD_ERRO = "Erro"
    CARD_NAO_CONFIGURADO = "Não configurado"
    CARD_SEM_VALOR = "--"

    GRUPO_RESUMO = "Resumo de Exportações"
    SEM_EXPORTACOES = "Nenhuma exportação realizada ainda."
    ULTIMA_EXPORTACAO = "ÚLTIMA EXPORTAÇÃO"
    PERIODO = "{mes}/{ano}"
    PERIODO_COM_CONTA = "{mes}/{ano}  ·  {conta}"
    ARQUIVOS_E_DATA = "{quantidade} arquivo(s)  ·  {quando}"
    MES_NAO_EXPORTADO = "Você ainda não exportou {mes}/{ano}."
    ESTATISTICAS_ANO = "Em {ano}: {exportacoes} exportação(ões), {arquivos} arquivo(s)."

    TITULO_LISTA_VEICULOS = "Veículos Disponíveis"
    LISTA_COLUNA_ID = "ID"
    LISTA_COLUNA_NOME = "Nome"
    LISTA_COLUNA_PLACA = "Placa"
    LISTA_TOTAL = "\nTotal: {quantidade} veículos"
    ERRO_LISTAR_VEICULOS = "Erro ao listar veículos: {erro}"
    AVISO_CONEXAO_INICIALIZANDO = (
        "Conexão ainda inicializando. Aguarde alguns segundos e tente novamente."
    )


class SidebarMsg:
    """Menu lateral."""

    TITULO = "Movi Exporter"
    VERSAO = "v{versao}"

    NAV_INICIO = "Início"
    NAV_EXPORTAR = "Exportar"
    NAV_CONFIGURACOES = "Configurações"
    ACAO_MANUAL = "Manual"
    ACAO_SOBRE = "Sobre"

    LABEL_CONTA = "Conta"
    CONTA = "Conta {numero}"
    TOAST_MANUAL_NAO_ENCONTRADO = "Manual não encontrado"


class StatusBarMsg:
    """Barra de status (rodapé da janela)."""

    PRONTO = "Pronto"


class AboutMsg:
    """Diálogo Sobre."""

    TITULO_JANELA = "Sobre o Movi Exporter"
    TITULO = "Movi Exporter"
    VERSAO = "Versão {versao}"
    DESCRICAO = (
        "Exportação mensal de dados de rastreamento\nveicular da Wialon para CSV/Excel."
    )
    BTN_REPOSITORIO = "Repositório no GitHub"
    BTN_NOTAS_VERSAO = "Notas de versão"
    BTN_VERIFICAR = "Verificar atualizações"
    BTN_VERIFICANDO = "Verificando..."
    LICENCA = "Licença de uso interno · Movi Solutions"

    TOAST_FALHA_VERIFICAR = "Não foi possível verificar atualizações"
    TOAST_NOVA_VERSAO = "Nova versão disponível: {versao}"
    TOAST_ATUALIZADO = "Você já está na versão mais recente"


class UpdateMsg:
    """Diálogo de atualização disponível."""

    TITULO_JANELA = "Atualização Disponível"
    TITULO = "Nova Versão Disponível!"
    COMPARACAO_VERSOES = "Versão atual: {atual}  →  Nova versão: {nova}"
    BTN_BAIXAR = "Baixar e Instalar"
    BTN_DEPOIS = "Depois"
    BTN_BAIXANDO = "Baixando..."
    BTN_INSTALANDO = "Instalando..."
    BTN_TENTAR_NOVAMENTE = "Tentar Novamente"
    PROGRESSO_DOWNLOAD = "Baixando... {baixado:.1f} MB / {total:.1f} MB"
    INICIANDO_INSTALACAO = "Iniciando instalação..."
    ERRO_SEM_URL = "URL de download não disponível"
    ERRO_DOWNLOAD = "Falha no download"
