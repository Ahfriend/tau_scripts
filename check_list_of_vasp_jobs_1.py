import os
import psutil  # To check running processes
import argparse

def check_vasp_termination(directory_path):
    """
    Checks if a VASP job has terminated correctly or is still running.

    Parameters:
        directory_path (str): Path to the directory containing the OUTCAR file.

    Returns:
        str: Status of the VASP job.
    """
    outcar_path = os.path.join(directory_path, "OUTCAR")
    try:
        # Check if the OUTCAR file exists
        if not os.path.exists(outcar_path):
            return f"{directory_path}: OUTCAR file not found."

        # Check if the VASP process is still running
        for process in psutil.process_iter(['pid', 'name', 'cwd']):
            if "vasp" in process.info['name'].lower() and process.info['cwd'] == os.path.abspath(directory_path):
                return f"{directory_path}: VASP job is still running (PID: {process.info['pid']})."

        # Check for termination message in OUTCAR
        with open(outcar_path, 'r') as file:
            lines = file.readlines()
            if any("reached required accuracy - stopping structural energy minimisation" in line for line in lines):
                return f"{directory_path}: VASP job terminated correctly."
            else:
                return f"{directory_path}: VASP job did NOT terminate correctly."

    except FileNotFoundError:
        return f"{directory_path}: OUTCAR file not found."
    except Exception as e:
        return f"{directory_path}: Error occurred - {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Check if VASP jobs terminated correctly.")
    parser.add_argument('-i', '--input', required=True, help="Path to the file containing paths to the output files.")
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as file:
            paths = file.read().splitlines()
            for path in paths:
                result = check_vasp_termination(path)
                print(result)
    except FileNotFoundError:
        print(f"{args.input}: Input file not found.")
    except Exception as e:
        print(f"Error occurred while reading input file: {str(e)}")

if __name__ == "__main__":
    main()
