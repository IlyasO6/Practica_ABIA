import shutil
import os

source_file = "experimentos/experimento_1.py"
destination_folder = "experimentos"

num_copias = 6

os.makedirs(destination_folder, exist_ok=True)

for i in range(2, num_copias + 2):
    new_filename = f"experimento_{i}.py"
    new_file_path = os.path.join(destination_folder, new_filename)
    
    # Copy the file
    shutil.copy(source_file, new_file_path)
    print(f"Created: {new_file_path}")

print("--> All copies created!")
