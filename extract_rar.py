import os
import rarfile

# Source folder (where your .rar files are)
source_dir = r"D:\CAREBKUP"

# Destination folder (where you want extracted content)
dest_dir = r"D:\caretosheets\extracted_rar"
os.makedirs(dest_dir, exist_ok=True)

# WinRAR path (update if installed elsewhere)
rarfile.UNRAR_TOOL = r"C:\Program Files\WinRAR\UnRAR.exe"

# Track all found file types
file_types = set()

# Step 1: Loop through all .rar files
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith(".rar"):
            rar_path = os.path.join(root, file)
            print(f"🔹 Extracting: {rar_path}")
            try:
                with rarfile.RarFile(rar_path) as rf:
                    rf.extractall(dest_dir)
                print(f"✅ Extracted to: {dest_dir}")
            except Exception as e:
                print(f"❌ Failed to extract {file}: {e}")
                continue

# Step 2: Walk through the extracted folder to detect file types
for root, dirs, files in os.walk(dest_dir):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext:
            file_types.add(ext)

# Step 3: Print summary
print("\n✅ All extractions completed!")
print("📂 File types found in extracted_rar:")
for ftype in sorted(file_types):
    print(f"  • {ftype}")
