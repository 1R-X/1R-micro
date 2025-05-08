import os

TEXT_EXTENSIONS = {".py", ".txt", ".json", ".yaml", ".yml", ".md", ".html", ".js", ".ts", ".css", ".ini"}
EXCLUDE_DIRS = {"venv", ".git", "__pycache__"}

def is_text_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    return ext in TEXT_EXTENSIONS

def create_archive(base_dir, archive_path="archive.txt"):
    with open(archive_path, "w", encoding="utf-8") as archive:
        for root, dirs, files in os.walk(base_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                file_path = os.path.join(root, file)
                if not is_text_file(file_path):
                    continue

                rel_path = os.path.relpath(file_path, base_dir)
                archive.write(f"\n>>> FILE: {rel_path} <<<\n")
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        archive.write(f.read())
                except Exception as e:
                    archive.write(f"[ERROR READING FILE: {e}]\n")
                archive.write(f"\n>>> END FILE <<<\n")

    print(f"✅ Archive created: {archive_path}")

if __name__ == "__main__":
    create_archive(base_dir=".")
