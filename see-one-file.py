import dbf

table = dbf.Table(r"D:\caretosheets\extracted_rar\ACCOUNT.DBF")
table.open()
for record in table:
    print(record)
table.close()
