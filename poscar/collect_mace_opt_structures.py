import os
import shutil
import zipfile

def process_paths(input_file, output_zip):
    """
    Iterates over paths in the input file, copies and renames out_structure files, and zips them.

    Parameters:
        input_file (str): Path to the input file containing paths.
        output_zip (str): Path to the output zip file.
    """
    # Create a temporary directory to store renamed files
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Read paths from the input file
        with open(input_file, 'r') as file:
            paths = file.read().splitlines()

        # Iterate over each path
        for path in paths:
            # Construct the source file path
            source_file = os.path.join(path, "mace_opt", "out_structure")
            
            # Check if the source file exists
            if not os.path.exists(source_file):
                print(f"File not found: {source_file}")
                continue

            # Construct the destination file name
            destination_file = os.path.join(temp_dir, f"{os.path.basename(path)}_mace_opt.vasp")

            # Copy and rename the file
            shutil.copy(source_file, destination_file)
            print(f"Copied and renamed: {source_file} -> {destination_file}")

        # Create a zip file containing all renamed files
        with zipfile.ZipFile(output_zip, 'w') as zipf:
            for file_name in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file_name)
                zipf.write(file_path, arcname=file_name)
                print(f"Added to zip: {file_path}")

    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        print("Temporary files cleaned up.")

# Example usage
if __name__ == "__main__":
    input_file = "main_job_dirs.txt"  # Replace with the path to your input file
    output_zip = "mace_opt_structures.zip"  # Replace with the desired output zip file name
    process_paths(input_file, output_zip)
