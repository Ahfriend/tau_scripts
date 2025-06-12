import os
import shutil
import argparse

def restore_empty_poscar(input_file):
    with open(input_file, 'r') as file:
        paths = file.readlines()

    for path in paths:
        path = path.strip()
        poscar_path = os.path.join(path, 'POSCAR')
        poscar_init_path = os.path.join(path, 'POSCAR_init')

        # Check if POSCAR exists and is empty
        if os.path.exists(poscar_path) and os.path.getsize(poscar_path) == 0:
            if os.path.exists(poscar_init_path):
                shutil.copy(poscar_init_path, poscar_path)
                print(f"Restored POSCAR from POSCAR_init in: {path}")
            else:
                print(f"POSCAR_init not found in: {path}")
        elif not os.path.exists(poscar_path):
            print(f"POSCAR not found in: {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Restore empty POSCAR files from POSCAR_init.")
    parser.add_argument('-i', '--input', required=True, help="Path to the input file containing paths.")
    args = parser.parse_args()

    restore_empty_poscar(args.input)

