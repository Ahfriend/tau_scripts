import os
import shutil

def copy_mace_opt_to_dft_single(input_file):
    """
    Iterates over paths in main_job_dirs.txt and copies mace_opt/out_structure to dft_single/POSCAR.

    Parameters:
        input_file (str): Path to the input file containing job directories.
    """
    try:
        # Read paths from the input file
        with open(input_file, 'r') as file:
            paths = file.read().splitlines()

        # Iterate over each path
        for path in paths:
            if not os.path.exists(path):
                print(f"Path not found: {path}")
                continue

            # Define source and destination paths
            source_file = os.path.join(path, "mace_opt", "out_structure")
            destination_dir = os.path.join(path, "dft_single")
            destination_file = os.path.join(destination_dir, "POSCAR")

            # Check if source file exists
            if not os.path.exists(source_file):
                print(f"Source file not found: {source_file}")
                continue

            # Create destination directory if it doesn't exist
            os.makedirs(destination_dir, exist_ok=True)

            # Copy the file
            shutil.copy(source_file, destination_file)
            print(f"Copied {source_file} to {destination_file}")

    except FileNotFoundError:
        print(f"Input file not found: {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "main_job_dirs.txt"  # Replace with the path to your input file
    copy_mace_opt_to_dft_single(input_file)
