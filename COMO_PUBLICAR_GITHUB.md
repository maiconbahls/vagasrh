# 🚀 Como Publicar no GitHub - Guia Passo a Passo

## 📝 PASSO 1: Criar Repositório no GitHub

1. **Acesse o GitHub**: https://github.com
2. **Faça login** na sua conta
3. Clique no botão **"+"** no canto superior direito
4. Selecione **"New repository"**
5. Preencha:
   - **Repository name**: `dashboard-vagas-cocal` (ou outro nome que preferir)
   - **Description**: `Dashboard de Gestão de Vagas - Cocal RH`
   - **Visibilidade**: 
     - ✅ **Private** (recomendado - só você e quem você convidar verá)
     - ⚠️ Public (qualquer pessoa pode ver)
   - **NÃO** marque "Add a README file" (já temos um)
   - **NÃO** marque "Add .gitignore" (já temos um)
6. Clique em **"Create repository"**

---

## 💻 PASSO 2: Comandos para Enviar o Código

Depois de criar o repositório, o GitHub mostrará uma página com comandos. 

**Copie a URL do seu repositório** (algo como: `https://github.com/SEU_USUARIO/dashboard-vagas-cocal.git`)

Agora execute estes comandos no terminal (PowerShell):

### 2.1 - Inicializar Git (se ainda não foi feito)

```powershell
cd "c:\Users\maicon.bahls\Cocal\Recursos Humanos - PRIVADO\PROGRAMAS - MAICON\PHYTON\VAGAS_DENISE"
git init
```

### 2.2 - Adicionar todos os arquivos

```powershell
git add .
```

### 2.3 - Fazer o primeiro commit

```powershell
git commit -m "Initial commit - Dashboard Vagas Cocal com Google Sheets"
```

### 2.4 - Renomear branch para main

```powershell
git branch -M main
```

### 2.5 - Conectar ao repositório do GitHub

**⚠️ IMPORTANTE: Substitua `SEU_USUARIO` e `NOME_DO_REPO` pela URL que você copiou!**

```powershell
git remote add origin https://github.com/SEU_USUARIO/NOME_DO_REPO.git
```

Exemplo:
```powershell
git remote add origin https://github.com/maiconbahls/dashboard-vagas-cocal.git
```

### 2.6 - Enviar para o GitHub

```powershell
git push -u origin main
```

**Pode pedir usuário e senha do GitHub:**
- **Usuário**: seu username do GitHub
- **Senha**: use um **Personal Access Token** (não a senha normal)
  - Para criar token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
  - Marque a opção **"repo"**
  - Copie o token e use como senha

---

## ✅ PASSO 3: Verificar se Funcionou

1. Acesse seu repositório no GitHub
2. Você deve ver todos os arquivos:
   - ✅ `app_streamlit.py`
   - ✅ `requirements.txt`
   - ✅ `README.md`
   - ✅ `.streamlit/config.toml`
   - ✅ `.gitignore`
   - ❌ `.streamlit/secrets.toml` (NÃO deve aparecer - é secreto!)

---

## 🔄 Para Atualizar o Código Depois

Sempre que fizer alterações e quiser atualizar no GitHub:

```powershell
git add .
git commit -m "Descrição da alteração"
git push
```

---

## ☁️ PRÓXIMO PASSO: Deploy no Streamlit Cloud

Depois de publicar no GitHub, siga o arquivo **`CONFIGURACAO.md`** na seção de Deploy no Streamlit Cloud!

---

## 🆘 Problemas Comuns

### "Git não é reconhecido como comando"
→ Instale o Git: https://git-scm.com/download/win

### "Permission denied"
→ Use Personal Access Token ao invés da senha

### "Remote origin already exists"
→ Execute: `git remote remove origin` e tente novamente o passo 2.5

### "Nothing to commit"
→ Você já fez commit de tudo, pode ir direto para o push (passo 2.6)

---

## 📞 Precisa de Ajuda?

Se tiver algum erro, me mande a mensagem de erro que te ajudo a resolver!
