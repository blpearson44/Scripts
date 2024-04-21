import re
import os

def remove_dbfolder(file_path: str):
    if not file_path.endswith('.md'):
        return f'Skipping {file_path}'
    with open(file_path, 'r') as file:
        content = file.read()
    pattern = r'yaml:dbfolder'
    if re.search(pattern, content):
        os.remove(file_path)
        return f"Removed {file_path}"
    return f"Skipping {file_path}"

def remove_all_dbfolder(folder: str):
    if folder.endswith(".git") or folder.endswith(".obsidian"):
        return f"Skipping {folder}"
    if not os.path.isdir(folder):
        raise ValueError(f"Error, {folder} is not a folder!")
    print(f">>>>>Recursively searching through {folder}")
    for file in os.listdir(folder):
        if os.path.isdir(f"{folder}/{file}"):
            print(remove_all_dbfolder(f"{folder}/{file}"))
            continue
        print(remove_dbfolder(f"{folder}/{file}"))
    return f"Finished searching through {folder}"

myfolder = "/home/ben/Spiderverse"

print(remove_all_dbfolder(myfolder))
