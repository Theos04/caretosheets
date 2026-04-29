import os
from dbfread import DBF

DBF_FOLDER = r"D:\caretosheets\extracted_rar"

for filename in os.listdir(DBF_FOLDER):
    if filename.lower().endswith(".dbf"):
        path = os.path.join(DBF_FOLDER, filename)
        try:
            dbf = DBF(path, encoding='latin1')
            rows = list(dbf)
            print(f"{filename}: {len(rows)} rows")
        except Exception as e:
            print(f"{filename}: Failed ({e})")
