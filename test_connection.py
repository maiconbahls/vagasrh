
import pandas as pd
import requests

# The URL provided by the user
SHEET_ID = "1Vmg9SJzq_Hq9u5CpeLgt4X5qJPVai9LGH6ajpsR7m_I"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

print(f"Testing URL: {URL}")

try:
    response = requests.get(URL)
    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response.headers.get('Content-Type')}")
    
    # Check if the content is HTML (login page) or CSV
    content_snippet = response.text[:500]
    print(f"First 500 chars of content:\n{content_snippet}\n")
    
    if "html" in response.headers.get('Content-Type', '').lower() or "<html" in content_snippet.lower():
        print("ERROR: profound issue - The URL returned HTML instead of CSV.")
        print("This usually means the spreadsheet is NOT public (Anyone with the link).")
        print("Action required: Change sharing settings to 'Anyone with the link' can view.")
    else:
        # Try to parse with pandas
        df = pd.read_csv(URL)
        print("\nSUCCESS: Data loaded successfully!")
        print(df.head())

except Exception as e:
    print(f"\nEXCEPTION: {e}")
