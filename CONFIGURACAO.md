# 🚀 GUIA DE CONFIGURAÇÃO - Google Sheets + Streamlit

## 📋 Pré-requisitos

1. Planilha do Google Sheets criada ✅
2. Conta no Streamlit Cloud (https://streamlit.io/cloud)
3. Conta no GitHub

---

## 🔧 PASSO 1: Configurar Permissões da Planilha

### Opção A: Planilha Pública (Somente Leitura) - MAIS SIMPLES

1. Abra sua planilha: https://docs.google.com/spreadsheets/d/1Vmg9SJzq_Hq9u5CpeLgt4X5qJPVai9LGH6ajpsR7m_I/edit
2. Clique em **"Compartilhar"** (canto superior direito)
3. Clique em **"Alterar para qualquer pessoa com o link"**
4. Selecione **"Leitor"**
5. Clique em **"Concluído"**

⚠️ **LIMITAÇÃO**: Com essa opção, a área ADMIN não conseguirá salvar dados (somente visualização)

### Opção B: Service Account (Leitura + Escrita) - RECOMENDADO

Para permitir que o app EDITE a planilha:

1. **Criar Service Account no Google Cloud:**
   - Acesse: https://console.cloud.google.com/
   - Crie um novo projeto (ou use existente)
   - Ative a **Google Sheets API**
   - Vá em **"Credenciais"** → **"Criar Credenciais"** → **"Conta de Serviço"**
   - Baixe o arquivo JSON com as credenciais

2. **Compartilhar a planilha com o Service Account:**
   - Copie o email da service account (algo como: `nome@projeto.iam.gserviceaccount.com`)
   - Abra sua planilha do Google Sheets
   - Clique em **"Compartilhar"**
   - Cole o email da service account
   - Dê permissão de **"Editor"**
   - Clique em **"Enviar"**

3. **Configurar as credenciais localmente:**
   - Abra o arquivo `.streamlit/secrets.toml`
   - Descomente as linhas e preencha com os dados do JSON baixado

---

## 🖥️ PASSO 2: Testar Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar o app
streamlit run app_streamlit.py
```

O app abrirá em: http://localhost:8501

---

## 📦 PASSO 3: Publicar no GitHub

```bash
# Inicializar repositório (se ainda não foi feito)
git init

# Adicionar arquivos
git add .

# Commit
git commit -m "Dashboard Vagas Cocal - Integração Google Sheets"

# Criar repositório no GitHub e conectar
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git

# Enviar para GitHub
git push -u origin main
```

⚠️ **IMPORTANTE**: O arquivo `.streamlit/secrets.toml` NÃO deve ir para o GitHub (já está no .gitignore)

---

## ☁️ PASSO 4: Deploy no Streamlit Cloud

1. Acesse: https://share.streamlit.io/
2. Clique em **"New app"**
3. Conecte sua conta do GitHub
4. Selecione:
   - **Repository**: seu repositório
   - **Branch**: main
   - **Main file path**: app_streamlit.py
5. Clique em **"Advanced settings"**
6. Cole o conteúdo do arquivo `.streamlit/secrets.toml` na seção **"Secrets"**
7. Clique em **"Deploy!"**

---

## 🔐 Configuração de Secrets no Streamlit Cloud

Se você escolheu a **Opção B (Service Account)**, cole isso nos Secrets:

```toml
[connections.gsheets]
spreadsheet = "https://docs.google.com/spreadsheets/d/1Vmg9SJzq_Hq9u5CpeLgt4X5qJPVai9LGH6ajpsR7m_I/edit?usp=sharing"

[gcp_service_account]
type = "service_account"
project_id = "SEU_PROJECT_ID"
private_key_id = "SUA_PRIVATE_KEY_ID"
private_key = "-----BEGIN PRIVATE KEY-----\nSUA_CHAVE_PRIVADA\n-----END PRIVATE KEY-----\n"
client_email = "seu-service-account@seu-projeto.iam.gserviceaccount.com"
client_id = "SEU_CLIENT_ID"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/seu-service-account%40seu-projeto.iam.gserviceaccount.com"
```

Se você escolheu a **Opção A (Pública)**, deixe os Secrets vazios ou apenas com:

```toml
# Planilha pública - sem credenciais necessárias
```

---

## ✅ Checklist Final

- [ ] Planilha configurada (pública OU service account)
- [ ] App testado localmente
- [ ] Código enviado para GitHub
- [ ] Secrets configurados no Streamlit Cloud
- [ ] App deployado com sucesso

---

## 🆘 Troubleshooting

### Erro: "Permission denied"
→ Verifique se compartilhou a planilha com o email da service account

### Erro: "API not enabled"
→ Ative a Google Sheets API no Google Cloud Console

### Erro: "Invalid credentials"
→ Verifique se copiou corretamente o JSON da service account

---

## 📞 Próximos Passos

Depois de configurado:
1. Teste adicionar dados pela área ADMIN
2. Verifique se os gráficos atualizam automaticamente
3. Compartilhe o link do Streamlit Cloud com sua equipe!
