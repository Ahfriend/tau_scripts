import os
import json
import subprocess
from datetime import datetime

# Paths to the global and local logs
global_log_path = "/andata/alonh/vasp_jobs.log"

def load_log(log_path):
    """
    Load the JSON log file.

    Parameters:
        log_path (str): Path to the log file.

    Returns:
        dict: Parsed JSON data from the log file.
    """
    if os.path.exists(log_path):
        with open(log_path, "r") as file:
            return json.load(file)
    return {}

def save_log(log_path, log_data):
    """
    Save the JSON log file.

    Parameters:
        log_path (str): Path to the log file.
        log_data (dict): Data to save in the log file.
    """
    with open(log_path, "w") as file:
        json.dump(log_data, file, indent=4)

def check_job_status(job_id):
    """
    Check the status of a SLURM job using its job ID.

    Parameters:
        job_id (str): SLURM job ID.

    Returns:
        tuple: (status, error_message)
            - status: The status of the job (e.g., SUBMITTED, RUNNING, COMPLETED, FAILED).
            - error_message: Error message if the job failed or encountered issues.
    """
    try:
        result = subprocess.run(
            ["scontrol", "show", "job", str(job_id)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "JobState=" in line:
                    return line.split("JobState=")[1].split()[0], None
            return "UNKNOWN", "Job state not found in SLURM output."
        else:
            return "FAILED", result.stderr.strip()
    except Exception as e:
        return "FAILED", str(e)

def update_local_log(job_path, job_id, status, error=None):
    """
    Update the local log file for a specific job.

    Parameters:
        job_path (str): Path to the job directory.
        job_id (str): SLURM job ID.
        status (str): Current status of the job.
        error (str): Error message if the job failed (optional).
    """
    local_log_path = os.path.join(job_path, "vasp_job.log")
    os.makedirs(job_path, exist_ok=True)

    # Load existing local log data
    if os.path.exists(local_log_path):
        with open(local_log_path, "r") as file:
            log_data = json.load(file)
    else:
        log_data = []

    # Add a new log entry
    log_entry = {
        "job_id": job_id,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    if error:
        log_entry["error"] = error

    log_data.append(log_entry)

    # Save updated local log data
    with open(local_log_path, "w") as file:
        json.dump(log_data, file, indent=4)

def process_jobs(global_log_path):
    """
    Process jobs from the global log and update their statuses.

    Parameters:
        global_log_path (str): Path to the global log file.
    """
    # Load the global log
    global_log = load_log(global_log_path)

    for job_path, job_info in global_log.items():
        job_id = job_info.get("job_id")
        current_status = job_info.get("status")

        # Skip jobs that are already completed successfully or failed
        if current_status in ["COMPLETED", "FAILED"]:
            continue

        # Check the job status
        new_status, error_message = check_job_status(job_id)

        # Update the global log
        global_log[job_path]["status"] = new_status
        global_log[job_path]["timestamp"] = datetime.now().isoformat()
        if error_message:
            global_log[job_path]["error"] = error_message

        # Update the local log
        update_local_log(job_path, job_id, new_status, error=error_message)

        if error_message:
            print(f"Job {job_id} at {job_path} failed: {error_message}")
        else:
            print(f"Updated job {job_id} at {job_path}: {new_status}")

    # Save the updated global log
    save_log(global_log_path, global_log)

if __name__ == "__main__":
    process_jobs(global_log_path)
