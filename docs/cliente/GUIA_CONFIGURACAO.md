# 📖 Guia de Configuração - Movi Exporter

## 📁 Estrutura de Arquivos

Na mesma pasta do `MoviExporter.exe`, você precisa ter:

```
📁 MoviExporter/
├── MoviExporter.exe        ← O programa
├── .env                    ← Arquivo de configuração (criar)
└── client_secrets.json     ← Só se usar Google Drive
```

---

## 🔧 Passo 1: Criar o arquivo `.env`

### No Windows:

1. Abra o **Bloco de Notas**
2. Cole o conteúdo abaixo:

```
WIALON_TOKEN=SEU_TOKEN_AQUI
EXPORT_DIR=./exports
GOOGLE_DRIVE_FOLDER_ID=
```

3. Vá em **Arquivo → Salvar Como**
4. Em "Tipo", selecione **"Todos os arquivos (*.*)"**
5. Em "Nome do arquivo", digite: `.env` (com o ponto na frente!)
6. Salve na **mesma pasta** do `MoviExporter.exe`

### ⚠️ Importante:
- O arquivo deve se chamar exatamente `.env` (com ponto, sem extensão .txt)
- Não use aspas no token
- Não deixe espaços antes ou depois do `=`

---

## 🔑 Passo 2: Obter o Token do Wialon

1. Acesse o **Wialon** (seu sistema de rastreamento)
2. Clique no seu **nome de usuário** (canto superior direito)
3. Vá em **"Configurações do Usuário"**
4. Clique em **"Tokens de Acesso"** ou **"Access Tokens"**
5. Clique em **"Criar"** ou **"Create"**
6. Configure:
   - **Nome:** MoviExporter
   - **Validade:** Ilimitado
7. Clique em **Criar**
8. **Copie o token** que aparece
9. Cole no arquivo `.env` no lugar de `SEU_TOKEN_AQUI`

> **Coluna "Motorista" no export (cartão RFID):** para o nome do motorista sair
> preenchido, o token precisa ter permissão de **ver motoristas** (ao criar o
> token, marque o acesso aos recursos/motoristas) e cada cartão RFID precisa
> estar com o campo **"Código" preenchido** na aba **Motoristas** do Wialon.
> Sem isso, a coluna sai como `N/D` — o restante do export funciona normalmente.

---

## ☁️ Passo 3: Google Drive (Opcional)

Se você quer enviar os arquivos automaticamente para o Google Drive:

### Obter o ID da Pasta:

1. Abra o **Google Drive** no navegador
2. Entre na pasta onde quer salvar os arquivos
3. Olhe a **URL** na barra de endereço:
   ```
   https://drive.google.com/drive/folders/1a2B3c4D5e6F7g8H9i
                                         └──────────────────┘
                                          Este é o ID da pasta
   ```
4. Copie esse ID
5. Cole no arquivo `.env`:
   ```
   GOOGLE_DRIVE_FOLDER_ID=1a2B3c4D5e6F7g8H9i
   ```

### Arquivo de Credenciais:

Você também precisa do arquivo `client_secrets.json`. 
**Solicite ao desenvolvedor** se não tiver este arquivo.

---

## ✅ Verificação Final

Seu arquivo `.env` deve ficar assim:

```
WIALON_TOKEN=5e8f9a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9
EXPORT_DIR=./exports
GOOGLE_DRIVE_FOLDER_ID=1a2B3c4D5e6F7g8H9i
```

(Os valores acima são exemplos - use os seus!)

---

## 🚀 Pronto!

Agora é só abrir o `MoviExporter.exe` e usar!

---

## ❓ Problemas Comuns

| Problema | Solução |
|----------|---------|
| "Erro na conexão Wialon" | Verifique se o token está correto |
| "Google Drive não configurado" | Verifique o GOOGLE_DRIVE_FOLDER_ID |
| Arquivo .env não funciona | Certifique-se que salvou como "Todos os arquivos" e não .txt |

---

## 📞 Suporte

Se tiver dúvidas, entre em contato:
- **Email:** seu_email@exemplo.com
- **WhatsApp:** (XX) XXXXX-XXXX
