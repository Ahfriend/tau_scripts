import os
import shutil

def move_files_to_dft_opt(input_file):
    with open(input_file, 'r') as file:
        paths = file.readlines()

    for path in paths:
        path = path.strip()
        dft_opt_path = os.path.join(path, 'dft_opt')

        # Ensure the target directory exists
        os.makedirs(dft_opt_path, exist_ok=True)

        # Move all files from the current path to the dft_opt directory
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):  # Only move files, not directories
                shutil.move(item_path, os.path.join(dft_opt_path, item))
                print(f"Moved {item} to {dft_opt_path}")

if __name__ == "__main__":
    input_file = 'vasp_job_paths.txt'  # Replace with the actual file path if different
    move_files_to_dft_opt(input_file)

