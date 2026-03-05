def read_file(file_path: str):
    with open(file_path, "r", encoding="UTF-8") as file:
        return file.read()