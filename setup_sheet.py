
import toml
import pandas as pd
from google.oauth2 import service_account
import gspread

def setup_sheet():
    print("Lendo credenciais...")
    try:
        secrets = toml.load(".streamlit/secrets.toml")
        
        # Extrair informações
        spreadsheet_url = secrets["connections"]["gsheets"]["spreadsheet"]
        creds_info = secrets["gcp_service_account"]
        
        # Ajustar chave privada se necessário (converter \n para quebras de linha reais)
        if "\\n" in creds_info["private_key"]:
            creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")

    except Exception as e:
        print(f"Erro ao ler secrets.toml: {e}")
        return

    print("Autenticando no Google...")
    try:
        # Escopos necessários
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = service_account.Credentials.from_service_account_info(
            creds_info, scopes=scopes
        )
        client = gspread.authorize(creds)
    except Exception as e:
        print(f"Erro na autenticação: {e}")
        return

    print(f"Abrindo planilha: {spreadsheet_url}...")
    try:
        sh = client.open_by_url(spreadsheet_url)
    except Exception as e:
        print(f"Erro ao abrir planilha: {e}")
        print("Verifique se o email da conta de serviço tem acesso de EDITOR na planilha.")
        print(f"Email: {creds_info.get('client_email')}")
        return

    # Definir dados iniciais
    data = {
        "Mes_Ref": ["Dezembro", "Janeiro", "Fevereiro"],
        "Estado": ["SP", "SP", "SP"],
        "Entrada": [10, 15, 20],
        "Saida": [2, 5, 8],
        "Saldo_Inicial": [100, 0, 0] # 0 para ser calculado depois se quiser, ou fixo
    }
    df = pd.DataFrame(data)
    
    # Adicionar dados de MS também para evitar erro de falta de dados
    df_ms = pd.DataFrame({
        "Mes_Ref": ["Dezembro", "Janeiro", "Fevereiro"],
        "Estado": ["MS", "MS", "MS"],
        "Entrada": [5, 8, 12],
        "Saida": [1, 3, 4],
        "Saldo_Inicial": [50, 0, 0] 
    })
    df_final = pd.concat([df, df_ms], ignore_index=True)

    worksheet_name = "FlowData"
    
    try:
        ws = sh.worksheet(worksheet_name)
        print(f"Aba '{worksheet_name}' já existe. Atualizando dados...")
    except gspread.WorksheetNotFound:
        print(f"Aba '{worksheet_name}' não encontrada. Criando...")
        ws = sh.add_worksheet(title=worksheet_name, rows=100, cols=20)

    # Limpar e atualizar
    ws.clear()
    
    # Escrever cabeçalhos e dados
    # gspread espera lista de listas. Header é a primeira lista.
    params = [df_final.columns.values.tolist()] + df_final.values.tolist()
    
    ws.update(range_name="A1", values=params)
    
    print("SUCESSO! Planilha atualizada e formatada.")
    print("Agora atualize seu aplicativo no Streamlit Cloud.")

if __name__ == "__main__":
    setup_sheet()
