import os
import subprocess
import ffmpeg

# Users input of folder path, where should be stored files for conversion.
user_folder = input("Please input folder path with files for conversion: ")

# Testing if the input path is valid.
if os.path.isdir(user_folder):
    pass
else:
    print("The inserted folder path do NOT exist.")

item_list = os.listdir(user_folder)

# Creation of full patch for files/items.
items_with_paths = [os.path.join(user_folder, item) for item in item_list]

print("In provided folder is", len(items_with_paths), "files.")

# Users input of required crf value for video conversion/compresion.
print("CRF = Constant Rate Factor - this rate control method tries to ensure" \
" that every frame gets the number of bits it deserves to achieve a certain (perceptual) " \
"quality level. Lower CRF means better quality and lower compresion rate. In table below are " \
"approximate sizes of files bassed on CRF value (H.264, CRF 0 is base 100%). \n")
print("CRF | H.264 | H.265 | MPEG-2 | AV1 \n",
    "---------------------------------- \n",
    "  0 | 100%  | 100%  | 200% | 100% \n",
    "  8 |  90%  |  85%  | 180% |  80% \n",
    " 12 |  75%  |  65%  | 170% |  60% \n",
    " 15 |  65%  |  55%  | 160% |  50% \n",
    " 18 |  55%  |  45%  | 150% |  40% \n",
    " 23 |  35%  |  35%  | 140% |  30% \n",
    " 28 |  25%  |  25%  | 130% |  25% \n",
    " 32 |  20%  |  20%  | 120% |  20% \n",
    " 40 |  15%  |  15%  | 110% |  15% \n")
crf_input = input("Please provide required 'CRF' value in range 4 - 63. CRF: ")
# Testing of crf if it is in required range 4-63.
if int(crf_input) not in range(4,64):
    print("Provided CRF is not in range 4 - 63.")
    quit()
else:
    pass
    
# Show of codecs of individual items.
for item in items_with_paths:
    print("\n" , os.path.basename(item))
    # Setup of ffprobe command to return codec type.
    command = [
        'ffprobe',
        # Show only errors if occured.
        '-v', 'error', 
        # Select video stream 0.
        '-select_streams', 'v:0', 
        # Show only codec_name.
        '-show_entries', 'stream=codec_name',
        # Show only value of codec_name without other info.
        '-of', 'default=noprint_wrappers=1:nokey=1', 
        item
    ]
    # Verification of command probeing the codec of the file.
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        print(f"Codec: {result.stdout.strip()}")
    else:
        print(f"ERROR: {result.stderr.strip()}")
    # Creation of original file name
    file_name_suffix = os.path.basename(item)
    file_name = os.path.splitext(file_name_suffix)[0]

    # Setup of ffmpeg command for conversion
    command = [
        'ffmpeg',
        '-i', item,
        '-c:v', 'libsvtav1',
        '-preset', '10',
        '-crf', crf_input,
        '-b:v', '0',
        '-c:a', 'copy',
        f'{file_name}.mkv'
    ]
    # Run of ffmpeg command for conversion
    subprocess.run(command)