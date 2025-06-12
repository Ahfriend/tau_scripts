import os
import shutil
import argparse

def process_paths_file(paths_file, job_name):
    # Read the paths from the file
    with open(paths_file, 'r') as file:
        paths = file.readlines()

    for path in paths:
        path = path.strip()  # Remove any trailing whitespace or newline characters
        dft_opt_path = os.path.join(path, "dft_opt")
        
        # Check if the dft_opt directory exists
        if not os.path.exists(dft_opt_path):
            print(f"Path does not exist: {dft_opt_path}")
            continue

        # Create the old_jobs/job_name directory
        old_jobs_path = os.path.join(dft_opt_path, "old_jobs", job_name)
        os.makedirs(old_jobs_path, exist_ok=True)

        # Copy POSCAR and CHGCAR to old_jobs/job_name
        for file_name in ["POSCAR", "CHGCAR"]:
            src_file = os.path.join(dft_opt_path, file_name)
            if os.path.exists(src_file):
                shutil.copy(src_file, old_jobs_path)
                print(f"Copied {file_name} to {old_jobs_path}")
            else:
                print(f"{file_name} does not exist in {dft_opt_path}")

        # Move all other files to old_jobs/job_name
        for file_name in os.listdir(dft_opt_path):
            src_file = os.path.join(dft_opt_path, file_name)
            dest_file = os.path.join(old_jobs_path, file_name)
            if file_name not in ["POSCAR", "CHGCAR", "old_jobs"]:
                shutil.move(src_file, dest_file)
                print(f"Moved {file_name} to {old_jobs_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize VASP job files.")
    parser.add_argument("-i", "--input", required=True, help="Path to the file containing paths.")
    parser.add_argument("-j", "--job_name", required=True, help="Name of the job for old_jobs directory.")
    args = parser.parse_args()

    process_paths_file(args.input, args.job_name)
