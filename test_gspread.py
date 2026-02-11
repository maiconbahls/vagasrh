
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import toml

# Mock st.secrets for local testing
try:
    secrets = toml.load(".streamlit/secrets.toml")
    # This is a hack to mock st.secrets
    class Secrets(dict):
        def __getattr__(self, name):
            return self.get(name)
    
    # st.secrets = Secrets(secrets) # This might not work as st.secrets is read-only or special
except:
    pass

# Direct test if possible
try:
    # URL from app.py
    GSHEET_URL = "https://docs.google.com/spreadsheets/d/1Vmg9SJzq_Hq9u5CpeLgt4X5qJPVai9LGH6ajpsR7m_I/edit?usp=sharing"
    
    # We can't easily mock st.connection without a running streamlit context
    # but we can try to use gspread directly to verify access
    import gspread
    from google.oauth2 import service_account
    
    secrets = toml.load(".streamlit/secrets.toml")
    creds_info = secrets["gcp_service_account"]
    if "\\n" in creds_info["private_key"]:
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")
        
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = service_account.Credentials.from_service_account_info(creds_info, scopes=scopes)
    client = gspread.authorize(creds)
    
    sh = client.open_by_url(GSHEET_URL)
    ws = sh.worksheet("FlowData")
    data = ws.get_all_records()
    print(f"Data found: {len(data)} rows")
    if len(data) > 0:
        print("First row:", data[0])
except Exception as e:
    print(f"Error: {e}")
