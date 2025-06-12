import os
import shutil

def process_failed_dft_single(input_file):
    """
    Processes paths from failed_dft_single.txt, moves VASP files in dft_single to a failed_<n> directory.

    Parameters:
        input_file (str): Path to the failed_dft_single.txt file containing paths.
    """
    try:
        # Read paths from the input file
        with open(input_file, 'r') as file:
            paths = file.read().splitlines()

        # Iterate over each path
        for path in paths:
            dft_single_dir = os.path.join(path, "dft_single")
            
            # Check if dft_single directory exists
            if not os.path.exists(dft_single_dir):
                print(f"dft_single directory not found: {dft_single_dir}")
                continue

            # Check if there are vasprun.xml files in dft_single
            vasprun_files = [f for f in os.listdir(dft_single_dir) if f == "vasprun.xml"]
            if not vasprun_files:
                print(f"No vasprun.xml files found in: {dft_single_dir}")
                continue

            # Determine the failed_<n> directory name
            failed_dir_number = 1
            while os.path.exists(os.path.join(dft_single_dir, f"failed_{failed_dir_number}")):
                failed_dir_number += 1
            failed_dir = os.path.join(dft_single_dir, f"failed_{failed_dir_number}")

            # Create the failed_<n> directory
            os.makedirs(failed_dir, exist_ok=True)

            # Move only files (not directories) in dft_single to the failed_<n> directory
            for file_name in os.listdir(dft_single_dir):
                file_path = os.path.join(dft_single_dir, file_name)
                if os.path.isfile(file_path):  # Ensure it's a file, not a directory
                    shutil.move(file_path, os.path.join(failed_dir, file_name))

            print(f"Moved files from {dft_single_dir} to {failed_dir}")

    except FileNotFoundError:
        print(f"Input file not found: {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input_file = "failed_dft_single.txt"  # Replace with the path to your failed_dft_single.txt file
    process_failed_dft_single(input_file)
