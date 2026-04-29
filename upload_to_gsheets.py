import os
import pandas as pd
from dbfread import DBF
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

# === CONFIG ===
DBF_FOLDER = r"D:\CAREBKUP"
SHEET_NAME = "data_master"
CREDENTIALS_FILE = "service_account.json"

# === AUTHENTICATION ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME)
ws = sheet.sheet1

print("📊 Existing rows:", len(ws.get_all_values()))

# === HELPER FUNCTION ===
def dbf_to_dataframe(file_path):
    try:
        dbf = DBF(file_path, encoding='latin1')  # No ignore_errors
        rows = list(dbf)
        if not rows:
            print(f"⚠️ Skipped {os.path.basename(file_path)} (empty table)")
            return None
        df = pd.DataFrame(rows)
        df = df.applymap(lambda x: str(x) if isinstance(x, (date, bytes)) else x)
        return df
    except Exception as e:
        print(f"❌ Failed to read {os.path.basename(file_path)}: {e}")
        return None

# === PROCESS DBF FILES ===
for filename in os.listdir(DBF_FOLDER):
    if filename.lower().endswith(".dbf"):
        file_path = os.path.join(DBF_FOLDER, filename)
        size = os.path.getsize(file_path)
        if size < 500:
            print(f"⚠️ Skipping {filename} (too small or corrupted)")
            continue

        print(f"📂 Processing {filename} ({size} bytes)")
        df = dbf_to_dataframe(file_path)

        if df is not None and not df.empty:
            print(f"📤 Uploading {len(df)} rows from {filename} in chunks...")
            try:
                for i in range(0, len(df), 1000):
                    chunk = df.iloc[i:i + 1000]
                    ws.append_rows(chunk.values.tolist(), value_input_option="RAW")
            except Exception as e:
                print(f"❌ Upload failed for {filename}: {e}")
        else:
            print(f"⚠️ No valid data in {filename}")

print("\n✅ All valid DBF files uploaded successfully!")
