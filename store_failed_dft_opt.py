import os
import shutil

def process_failed_dft_opt(input_file):
    """
    Processes paths from failed_dft_opt.txt, moves VASP files in dft_opt to a failed_<n> directory.

    Parameters:
        input_file (str): Path to the failed_dft_opt.txt file containing paths.
    """
    try:
        # Read paths from the input file
        with open(input_file, 'r') as file:
            paths = file.read().splitlines()

        # Iterate over each path
        for path in paths:
            dft_opt_dir = os.path.join(path, "dft_opt")
            
            # Check if dft_opt directory exists
            if not os.path.exists(dft_opt_dir):
                print(f"dft_opt directory not found: {dft_opt_dir}")
                continue

            # Check if there are vasprun.xml files in dft_opt
            vasprun_files = [f for f in os.listdir(dft_opt_dir) if f == "vasprun.xml"]
            if not vasprun_files:
                print(f"No vasprun.xml files found in: {dft_opt_dir}")
                continue

            # Determine the failed_<n> directory name
            failed_dir_number = 1
            while os.path.exists(os.path.join(dft_opt_dir, f"failed_{failed_dir_number}")):
                failed_dir_number += 1
            failed_dir = os.path.join(dft_opt_dir, f"failed_{failed_dir_number}")

            # Create the failed_<n> directory
            os.makedirs(failed_dir, exist_ok=True)

            # Move only files (not directories) in dft_opt to the failed_<n> directory
            for file_name in os.listdir(dft_opt_dir):
                file_path = os.path.join(dft_opt_dir, file_name)
                if os.path.isfile(file_path):  # Ensure it's a file, not a directory
                    shutil.move(file_path, os.path.join(failed_dir, file_name))

            print(f"Moved files from {dft_opt_dir} to {failed_dir}")

    except FileNotFoundError:
        print(f"Input file not found: {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a failed DFT optimization file.")
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the failed_dft_opt.txt file"
    )
    args = parser.parse_args()

    process_failed_dft_opt(args.input_file)
