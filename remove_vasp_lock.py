import os
import argparse

def remove_vasp_locks(input_file):
    with open(input_file, 'r') as file:
        paths = file.readlines()

    for path in paths:
        path = path.strip()
        lock_file = os.path.join(path, 'vasp.lock')
        if os.path.exists(lock_file):
            os.remove(lock_file)
            print(f"Removed: {lock_file}")
        else:
            print(f"No lock file found in: {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove vasp.lock files from specified directories.")
    parser.add_argument('-i', '--input', required=True, help="Path to the input file containing directory paths.")
    args = parser.parse_args()

    remove_vasp_locks(args.input)

