import os
import subprocess

folder_path = r"D:\\Filmy"
item_list = os.listdir(folder_path)

# Creation of full patch for files/items
items_with_paths = [os.path.join(folder_path, item) for item in item_list]

# Seznamy pro uložení všech názvů složek a souborů
# Lists to save all names of folders and files
folders_list = []
files_list = []

# Function for sorting folder/file
def sort_list(item):
    if os.path.isdir(item):
        return 0
    elif os.path.isfile(item):
        return 1
    else:
        pass

# Insert of items into lists
for item in items_with_paths:
    if sort_list(item) == 0:
        folders_list.append(os.path.basename(item))
    else:
        files_list.append(os.path.basename(item))

print(folders_list)
print(files_list)

# Setup of ffprobe command to return codec type
command = [
    'ffprobe', 
    '-v', 'error', 
    '-select_streams', 'v:0', 
    '-show_entries', 'stream=codec_name', 
    '-of', 'default=noprint_wrappers=1:nokey=1', 
    item
]

# Show of codecs of individual items
for item in items_with_paths:
    print(os.path.basename(item)os.path.basename(item))
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print(f"Codec: {result.stdout.strip()} - ", os.path.basename(item))
    else:
        print(f"ERROR: {result.stderr.strip()} - ", os.path.basename(item))
