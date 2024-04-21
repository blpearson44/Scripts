import re
import os

def get_uid(file_path: str):
    if not file_path.endswith('.md'):
        print(f"{file_path} Not a markdown file. Skipping...")
    try:
        with open(file_path, 'r', encoding = 'utf-8') as file:
            content = file.read()
    except FileNotFoundError:
        print(f'File not found: {file_path}')
        return

    date_pattern = r'^date: (\d{4})-(\d{2})-(\d{2})'

    date_match = re.search(date_pattern, content, re.MULTILINE)

    patharr = file_path.split('/')
    title, extension = patharr[-1].split('.')

    # Aliases
    aliases_pattern = r'^aliases:\n(?:\s+-\s+.*\n)*'
    aliases = re.search(aliases_pattern, content, re.MULTILINE)
    alias_arr = None

    if aliases:
        alias_pattern = r'^\s+-\s+(.*)$'
        alias_arr = re.findall(alias_pattern, aliases.group(0), re.MULTILINE)

    if not alias_arr:
        print(f"Adding alias {title}...")
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for count, line in enumerate(lines):
            if line == "date:\n":
                lines.insert(count - 1, f"  - {title}\n")
                lines.insert(count - 2, "aliases:\n")
                with open(file_path, 'w') as file:
                    file.writelines(lines)
                break

    if alias_arr and title not in alias_arr :
        print(f"Adding alias {title}...")
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for count, line in enumerate(lines):
            if line == "aliases:\n":
                lines.insert(count + 1, f"  - {title}\n")
                with open(file_path, 'w') as file:
                    file.writelines(lines)
                break



    if date_match:
        new_filename = f'{date_match.group(1)}{date_match.group(2)}{date_match.group(3)}-{title.replace(" ", "-")}.{extension}'
    else:
        new_filename = f'20240417-{title.replace(" ", "-")}.{extension}'
    new_filepath = file_path.replace(f'{title}.{extension}', new_filename)

    if not os.path.exists(new_filepath):
        os.rename(file_path, new_filepath)
    else:
        print(f"The file {new_filepath} exists!")

def rename_files(folder: str):
    if not os.path.isdir(folder):
        raise ValueError(f"{folder} not a directory!")
    for file in os.listdir(folder):
        path = f'{folder}/{file}'
        if not file.endswith('.md'):
            print(f'Skipping {path}')
            continue
        print(f'Renaming {path}...')
        get_uid(path)

rename_files('/home/ben/Spiderverse')
