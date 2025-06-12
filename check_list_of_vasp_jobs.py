import argparse
import os

def check_vasp_termination(directory_path):
    outcar_path = os.path.join(directory_path, "OUTCAR")
    try:
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
