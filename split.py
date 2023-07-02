import os
import sys
import re

DEFAULT_CHUNK_SIZE = 1440 * 1024  # 1.44MB
KB_SIZE = 1024
MB_SIZE = 1024 * 1024

if len(sys.argv) < 2:
    print("Please provide the input file name as a command line argument.")
    sys.exit(1)

input_file = sys.argv[1]

chunk_size = DEFAULT_CHUNK_SIZE
if len(sys.argv) >= 3:
    chunk_size_arg = sys.argv[2].lower()

    # Check for different input formats: "1.44mb", "1.44Mb", "720kb", or "720Kb"
    match = re.match(r"^(\d+\.?\d*)([km]b)$", chunk_size_arg)
    if match:
        size = float(match.group(1))
        unit = match.group(2)

        if unit == "kb":
            chunk_size = int(size * KB_SIZE)
        elif unit == "mb":
            chunk_size = int(size * MB_SIZE)
    else:
        print("Invalid chunk size format. Using the default size.")

output_prefix = os.path.splitext(input_file)[0] + '_'
file_number = 1

with open(input_file, 'rb') as f:
    chunk = f.read(chunk_size)
    while chunk:
        padding = b'\x00' * (chunk_size - len(chunk))  # Padding with null bytes
        chunk += padding
        output_file = f'{output_prefix}{file_number}.img'
        with open(output_file, 'wb') as chunk_file:
            chunk_file.write(chunk)
        file_number += 1
        chunk = f.read(chunk_size)

# Check if there is any remaining padding file and delete it
padding_file_number = file_number
padding_file_path = f'{output_prefix}{padding_file_number}.img'
while os.path.exists(padding_file_path):
    os.remove(padding_file_path)
    padding_file_number += 1
    padding_file_path = f'{output_prefix}{padding_file_number}.img'
