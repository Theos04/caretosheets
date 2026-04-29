from dbfread import DBF
import pandas as pd
import os

folder = r"D:\caretosheets\extracted_rar"

for file in os.listdir(folder):
    if file.lower().endswith(".dbf"):
        path = os.path.join(folder, file)
        print(f"🔹 Reading {file} ...")
        dbf = DBF(path, encoding='latin1')  # or 'utf-8' if needed
        df = pd.DataFrame(iter(dbf))
        print(df.head())  # Preview first few rows
        df.to_csv(path.replace('.dbf', '.csv'), index=False)
        print(f"✅ Saved {file} as CSV")
