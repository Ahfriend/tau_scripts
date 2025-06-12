import os
import argparse
import subprocess

# Parse command line arguments
parser = argparse.ArgumentParser(description='Process VASP job paths.')
parser.add_argument('-i', '--input', default='vasp_job_paths.txt', help='Input file with VASP job paths')
parser.add_argument('-c', '--cpus', default='40', help='Number of CPUs to use')
parser.add_argument('-m', '--memory', default='150gb', help='Amount of memory to use')
parser.add_argument('-p', '--partition', default='engineering', help='Partition to use')
args = parser.parse_args()

job_paths_file = args.input

with open(job_paths_file, 'r') as f:
    job_paths = f.read().splitlines()

# Save the starting directory
start_dir = os.getcwd()

# Process each job path
for job_path in job_paths:
    if not os.path.exists(job_path):
        print(f"Directory not found: {job_path}")
        continue

    # Check if vasp.lock exists
    lock_file = os.path.join(job_path, 'vasp.lock')
    if os.path.exists(lock_file):
        print(f"Skipping {job_path} (vasp.lock exists)")
        continue

    # Change the current working directory to the job path
    os.chdir(job_path)

    # Extract the path name (last part of the path)
    path_name = os.path.basename(job_path)

    # Construct the command to call the script
    command = f"/work/scripts/srun_pl.sh {path_name} {args.cpus} {args.memory} {args.partition}"
    # Call the script
    subprocess.run(command, shell=True)

    # Create vasp.lock file
    with open('vasp.lock', 'w') as lock:
        lock.write('')

    print(f"Executed script for {job_path} and created vasp.lock")

    # Change back to the starting directory
    os.chdir(start_dir)
