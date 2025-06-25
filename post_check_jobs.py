import json
import os
import argparse

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

def filter_jobs(log_data, status=None, tags=None):
    """
    Filter jobs based on status and/or tags.

    Parameters:
        log_data (dict): The JSON data from the log file.
        status (str): The status to filter by (optional).
        tags (list): The tags to filter by (optional).

    Returns:
        dict: Filtered jobs sorted by their status.
    """
    filtered_jobs = {}

    for job_path, job_info in log_data.items():
        job_status = job_info.get("status")
        job_tags = job_info.get("tags", [])

        # Filter by status if provided
        if status and job_status != status:
            continue

        # Filter by tags if provided
        if tags and not any(tag in job_tags for tag in tags):
            continue

        # Add job to filtered list
        if job_status not in filtered_jobs:
            filtered_jobs[job_status] = []
        filtered_jobs[job_status].append({"job_path": job_path, **job_info})

    return filtered_jobs

def display_jobs(filtered_jobs):
    """
    Display jobs sorted by their status.

    Parameters:
        filtered_jobs (dict): Filtered jobs sorted by their status.
    """
    for status, jobs in filtered_jobs.items():
        print(f"\nJobs with status '{status}':")
        for job in jobs:
            print(f"  Job Path: {job['job_path']}")
            print(f"  Job ID: {job['job_id']}")
            print(f"  Tags: {job.get('tags', [])}")
            print(f"  Timestamp: {job['timestamp']}")
            if "error" in job:
                print(f"  Error: {job['error']}")
            print()

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Filter and display VASP jobs based on their status and/or tags.")
    parser.add_argument(
        "-s", "--status",
        help="Filter jobs by status (e.g., FAILED, RUNNING, COMPLETED). Default: Show all statuses.",
        default=None
    )
    parser.add_argument(
        "-t", "--tags",
        help="Filter jobs by tags (comma-separated, e.g., tag1,tag2). Default: Show all tags.",
        default=None
    )
    args = parser.parse_args()

    # Path to the global log file
    log_path = "/work/alonh/vasp.log/vasp_jobs.log"

    # Load the log file
    log_data = load_log(log_path)

    # Parse tags argument
    tags_to_filter = args.tags.split(",") if args.tags else None
    if tags_to_filter:
        tags_to_filter = [tag.strip() for tag in tags_to_filter]

    # Filter jobs based on user input
    filtered_jobs = filter_jobs(log_data, status=args.status, tags=tags_to_filter)

    # Display the filtered jobs
    display_jobs(filtered_jobs)
