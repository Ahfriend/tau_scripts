import argparse
import os
import psutil  # To check running processes

def check_vasp_termination(directory_path):
    """
    Checks if a VASP job has terminated correctly or is still running.

    Parameters:
        directory_path (str): Path to the directory containing the OUTCAR file.

    Returns:
        str: Status of the VASP job.
        bool: True if the job terminated correctly, False otherwise.
    """
    outcar_path = os.path.join(directory_path, "OUTCAR")
    try:
        # Check if the OUTCAR file exists
        if not os.path.exists(outcar_path):
            return f"{directory_path}: OUTCAR file not found.", False

        # Check for termination message in OUTCAR
        with open(outcar_path, 'r') as file:
            lines = file.readlines()
            if any("reached required accuracy - stopping structural energy minimisation" in line for line in lines):
                return f"{directory_path}: VASP job terminated correctly.", True
            else:
                return f"{directory_path}: VASP job did NOT terminate correctly.", False

    except FileNotFoundError:
        return f"{directory_path}: OUTCAR file not found.", False
    except Exception as e:
        return f"{directory_path}: Error occurred - {str(e)}", False

def main():
    parser = argparse.ArgumentParser(description="Check if VASP jobs terminated correctly.")
    parser.add_argument('-i', '--input', required=True, help="Path to the file containing paths to the output files.")
    parser.add_argument('-o', '--output', required=True, help="Path to the output file for paths of jobs that did not terminate correctly.")
    args = parser.parse_args()

    try:
        with open(args.input, 'r') as file:
            paths = file.read().splitlines()

        failed_paths = []

        for path in paths:
            result, terminated_correctly = check_vasp_termination(path)
            print(result)
            if not terminated_correctly:
                failed_paths.append(path)

        # Write paths of jobs that did not terminate correctly to the output file
        with open(args.output, 'w') as outfile:
            outfile.write("\n".join(failed_paths))

        print(f"Paths of jobs that did not terminate correctly have been written to {args.output}.")

    except FileNotFoundError:
        print(f"{args.input}: Input file not found.")
    except Exception as e:
        print(f"Error occurred while reading input file: {str(e)}")

if __name__ == "__main__":
    main()
