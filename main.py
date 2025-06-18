import os
import subprocess

folder_path = r"D:\\Filmy"
item_list = os.listdir(folder_path)

# Vytvoříme úplné cesty
items_with_paths = [os.path.join(folder_path, item) for item in item_list]

# Funkce pro určení klíče při řazení
folders_list = []
files_list = []

def sort_list(item):
    if os.path.isdir(item):
        return 0
    elif os.path.isfile(item):
        return 1
    else:
        pass

for item in items_with_paths:
    if sort_list(item) == 0:
        folders_list.append(os.path.basename(item))
    else:
        files_list.append(os.path.basename(item))

print(folders_list)
print(files_list)
# Sestavení příkazu pro ffprobe
command = [
    'ffprobe', 
    '-v', 'error', 
    '-select_streams', 'v:0', 
    '-show_entries', 'stream=codec_name', 
    '-of', 'default=noprint_wrappers=1:nokey=1', 
    item
]

for item in items_with_paths:
    print(os.path.basename(item)os.path.basename(item))
    # Spuštění příkazu
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Výpis kodeku
    if result.returncode == 0:
        print(f"Codec: {result.stdout.strip()} - ", os.path.basename(item))
    else:
        print(f"ERROR: {result.stderr.strip()} - ", os.path.basename(item))
