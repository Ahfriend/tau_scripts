import os
import argparse
import subprocess
import json
from datetime import datetime

# Centralized log file path
central_log_file = "/work/alonh/vasp.log/vasp_jobs.log"


def update_central_log(log_file, job_path, job_id, status, tags=None):
    """
    Update the centralized log file with job_path, job_id, status, timestamp, and tags.

    Parameters:
        log_file (str): Path to the centralized log file.
        job_path (str): Path to the job directory.
        job_id (str): SLURM job ID.
        status (str): Current status of the job.
        tags (list): List of user-defined tags for the job (optional).
    """
    # Ensure the directory for the log file exists
    log_dir = os.path.dirname(log_file)


    # Load existing log data
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            log_data = json.load(file)
    else:
        log_data = {}

    # Update or add the job entry
    log_data[job_path] = {
        "job_id": job_id,
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "tags": tags or []  # Add the user-defined tags (default to an empty list)
    }

    # Write updated log data back to the file
    with open(log_file, "w") as file:
        json.dump(log_data, file, indent=4)




# Function to update the centralized log

def update_job_log(job_path, job_id, status, tags=None):
    """
    Update the per-job log file with job_id, status, timestamp, and tags.

    Parameters:
        job_path (str): Path to the job directory.
        job_id (str): SLURM job ID.
        status (str): Current status of the job.
        tags (list): List of user-defined tags for the job (optional).
    """
    # Convert job_path to absolute path
    job_log_file = os.path.join(job_path, "vasp_job.log")

    # Debugging statements
    print(f"Attempting to write to: {job_log_file}")
    print(f"Directory exists: {os.path.exists(job_path)}")
    print(f"Directory writable: {os.access(job_path, os.W_OK)}")

    # Ensure the directory exists
    #os.makedirs(job_path, exist_ok=True)

    # Load existing log data
    if os.path.exists(job_log_file):
        with open(job_log_file, "r") as file:
            log_data = json.load(file)
    else:
        log_data = []

    # Add a new log entry
    log_data.append({
        "job_id": job_id,
        "status": status,
        "timestamp": datetime.now().isoformat(),
        "tags": tags or []  # Add the user-defined tags (default to an empty list)
    })

    # Write updated log data back to the file
    with open(job_log_file, "w") as file:
        json.dump(log_data, file, indent=4)



# Parse command line arguments
parser = argparse.ArgumentParser(description='Process VASP job paths.')
parser.add_argument('-i', '--input', default='vasp_job_paths.txt', help='Input file with VASP job paths')   
parser.add_argument('-c', '--cpus', default='40', help='Number of CPUs to use')
parser.add_argument('-m', '--memory', default='150gb', help='Amount of memory to use')
parser.add_argument('-p', '--partition', default='engineering', help='Partition to use')
parser.add_argument('-t', '--tag', default=None, help='Tag to associate with the job')  # Add tag argument
args = parser.parse_args()

job_paths_file = args.input

with open(job_paths_file, 'r') as f:
    job_paths = f.read().splitlines()

# Save the starting directory
start_dir = os.getcwd()

# Process each job path
for job_path in job_paths:
    job_path = os.path.join(start_dir,job_path)
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
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # Extract job ID from the SLURM output (if available)
    job_id = None
    if result.returncode == 0:
        job_id = result.stdout.strip().split()[-1]  # Assuming job ID is the last part of the output
        status = "SUBMITTED"
    else:
        status = "FAILED"

    # Update centralized log
    update_central_log(central_log_file, job_path, job_id, status, tags=args.tag)

    # Update per-job log
    update_job_log(job_path, job_id, status, tags=args.tag)

    # Create vasp.lock file
    with open('vasp.lock', 'w') as lock:
        lock.write('')

    print(f"Executed script for {job_path} and created vasp.lock")

    # Change back to the starting directory
    os.chdir(start_dir)
