# 📊 Dashboard de Vagas - Cocal

Dashboard interativo para gestão e análise de vagas de emprego, desenvolvido com Streamlit e integrado ao Google Sheets.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=google-sheets&logoColor=white)

## 🚀 Funcionalidades

### 📈 Dashboard Principal
- **Visualização em tempo real** dos dados do Google Sheets
- **Filtros por estado**: Consolidado Geral, São Paulo (SP), Mato Grosso do Sul (MS)
- **Métricas principais**:
  - Volume Total de Vagas
  - Contratações Realizadas
  - Backlog de Posições Abertas
  - SLA Médio de Fechamento
- **Gráficos interativos**:
  - Waterfall Chart (Fluxo de Vagas)
  - Gauge de Eficiência
  - Evolução Comparativa por Estado

### 🔐 Área Administrativa
- **Edição de dados** diretamente na interface
- **Sincronização automática** com Google Sheets
- **Download de backup** em Excel
- **Upload de planilhas** para atualização em massa
- **Recálculo automático** de saldos

## 🎨 Design

- **Tema Dark Premium** com cores institucionais da Cocal
- **Paleta de cores**:
  - Verde Cocal: `#76B82A`
  - Laranja Cocal: `#EF7D00`
  - Azul Cocal: `#30515F`
- **Tipografia moderna**: Outfit + JetBrains Mono
- **Animações suaves** e efeitos glassmorphism

## 📦 Instalação Local

### Pré-requisitos
- Python 3.8+
- Conta Google com acesso à planilha

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/SEU_USUARIO/VAGAS_DENISE.git
cd VAGAS_DENISE
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure o Google Sheets**
   - Siga o guia completo em [`CONFIGURACAO.md`](CONFIGURACAO.md)
   - Configure o arquivo `.streamlit/secrets.toml`

4. **Execute o app**
```bash
streamlit run app_streamlit.py
```

O app abrirá em `http://localhost:8501`

## 🔧 Configuração do Google Sheets

### Opção 1: Planilha Pública (Somente Leitura)

1. Torne sua planilha pública
2. Não precisa configurar secrets
3. ⚠️ Área Admin não funcionará (somente visualização)

### Opção 2: Service Account (Recomendado)

1. Crie um Service Account no Google Cloud
2. Compartilhe a planilha com o email da service account
3. Configure `.streamlit/secrets.toml` com as credenciais

**Guia completo**: [`CONFIGURACAO.md`](CONFIGURACAO.md)

## ☁️ Deploy no Streamlit Cloud

1. Faça push do código para o GitHub
2. Acesse [Streamlit Cloud](https://share.streamlit.io/)
3. Conecte seu repositório
4. Cole as credenciais na seção **Secrets**
5. Deploy! 🚀

## 📊 Estrutura da Planilha

A planilha do Google Sheets deve ter as seguintes colunas:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `Mes_Ref` | Texto | Mês de referência (ex: "Janeiro", "Fevereiro") |
| `Estado` | Texto | Estado (SP ou MS) |
| `Entrada` | Número | Quantidade de novas vagas abertas |
| `Saida` | Número | Quantidade de vagas fechadas |
| `Saldo_Inicial` | Número | Saldo inicial do mês |

## 🛠️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)** - Framework web para Python
- **[Pandas](https://pandas.pydata.org/)** - Manipulação de dados
- **[Plotly](https://plotly.com/)** - Gráficos interativos
- **[st-gsheets-connection](https://github.com/streamlit/gsheets-connection)** - Integração Google Sheets
- **[XlsxWriter](https://xlsxwriter.readthedocs.io/)** - Geração de Excel

## 📁 Estrutura do Projeto

```
VAGAS_DENISE/
├── .streamlit/
│   ├── config.toml          # Configurações do Streamlit
│   └── secrets.toml         # Credenciais (NÃO commitar!)
├── app_streamlit.py         # Aplicação principal
├── requirements.txt         # Dependências Python
├── CONFIGURACAO.md          # Guia de configuração completo
├── README.md               # Este arquivo
└── .gitignore              # Arquivos ignorados pelo Git
```

## 🔐 Segurança

- ⚠️ **NUNCA** commite o arquivo `.streamlit/secrets.toml` no Git
- O `.gitignore` já está configurado para proteger seus secrets
- Use variáveis de ambiente ou Streamlit Secrets para credenciais

## 📝 Senha da Área Admin

A senha padrão da área administrativa é: **`gestao`**

Para alterar, edite a linha 685 em `app_streamlit.py`:
```python
if senha_input == "gestao":  # Altere aqui
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 📄 Licença

Este projeto é de uso interno da Cocal.

## 👨‍💻 Autor

Desenvolvido por Maicon Bahls - Recursos Humanos Cocal

---

**📞 Suporte**: Em caso de dúvidas, consulte o arquivo [`CONFIGURACAO.md`](CONFIGURACAO.md) ou entre em contato com o desenvolvedor.
