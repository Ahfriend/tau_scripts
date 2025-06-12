import os
import shutil
import argparse

def copy_vasp_to_poscar(input_file):
    """
    Reads paths from an input file, and for each path, copies the .vasp file to POSCAR in the same directory.

    Parameters:
        input_file (str): Path to the file containing directories with .vasp files.
    """
    try:
        # Read the paths from the input file
        with open(input_file, 'r') as file:
            paths = file.read().splitlines()

        for path in paths:
            if not os.path.exists(path):
                print(f"Path does not exist: {path}")
                continue

            # Find the .vasp file in the directory
            vasp_file = None
            for file_name in os.listdir(path):
                if file_name.endswith(".vasp"):
                    vasp_file = os.path.join(path, file_name)
                    break

            if vasp_file:
                # Define the destination POSCAR file
                poscar_file = os.path.join(path, "POSCAR")

                # Copy the .vasp file to POSCAR
                shutil.copy(vasp_file, poscar_file)
                print(f"Copied {vasp_file} to {poscar_file}")
            else:
                print(f"No .vasp file found in {path}")

    except FileNotFoundError:
        print(f"Input file not found: {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate desodiation energy from input data.")
    parser.add_argument('-i', '--input', required=True, help="Path to the input file containing energy and sodium count data.")
    args = parser.parse_args() 

    input_file = "paths.txt"  # Replace with the path to your input file
    copy_vasp_to_poscar(args.input)
