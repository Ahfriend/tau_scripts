import os
import argparse
import json
from datetime import datetime

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

def find_latest_job_id(job_path):
    """
    Find the latest job ID from files named dft_opt-<job_id>.err.

    Parameters:
        job_path (str): Path to the job directory.

    Returns:
        str: The latest job ID if found, otherwise None.
    """
    try:
        # List all files in the job path
        files = os.listdir(job_path)
        # Filter files matching the pattern dft_opt-<job_id>.err
        job_files = [f for f in files if f.startswith("dft_opt-") and f.endswith(".err")]
        if not job_files:
            return None

        # Extract job IDs and find the latest one
        job_ids = [int(f.split("-")[1].split(".")[0]) for f in job_files]
        latest_job_id = max(job_ids)
        return str(latest_job_id)
    except Exception as e:
        print(f"Error finding job ID in {job_path}: {e}")
        return None

def add_jobs_to_log(paths_file, tags, log_path):
    """
    Add jobs to the general log file.

    Parameters:
        paths_file (str): Path to the file containing job paths.
        tags (list): List of tags to associate with the jobs.
        log_path (str): Path to the general log file.
    """
    # Load existing log data
    log_data = load_log(log_path)

    # Read paths from the input file
    with open(paths_file, "r") as file:
        paths = file.read().splitlines()

    for job_path in paths:
        if not os.path.exists(job_path):
            print(f"Job path does not exist: {job_path}")
            continue

        # Check if the path is already in the log
        if job_path in log_data:
            print(f"Job path already exists in the log: {job_path}. Skipping...")
            continue

        # Find the latest job ID
        job_id = find_latest_job_id(job_path)

        # If no job ID is found, use "UNKNOWN" as a placeholder
        if not job_id:
            print(f"No job ID found for {job_path}. Adding placeholder...")
            job_id = "UNKNOWN"

        # Add job to the log
        log_data[job_path] = {
            "job_id": job_id,
            "status": "SUBMITTED",
            "timestamp": datetime.now().isoformat(),
            "tags": tags
        }

        print(f"Added job {job_id} for path {job_path} to the log.")

    # Save updated log data
    save_log(log_path, log_data)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Add jobs to the general log file.")
    parser.add_argument("-i", "--input", required=True, help="Path to the file containing job paths.")
    parser.add_argument("-t", "--tags", required=False, default="", help="Comma-separated list of tags to associate with the jobs.")
    parser.add_argument("-l", "--log", required=False, default="/work/alonh/vasp.log/vasp_jobs.log", help="Path to the general log file.")
    args = parser.parse_args()

    # Parse tags
    tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]

    # Add jobs to the log
    add_jobs_to_log(args.input, tags, args.log)
