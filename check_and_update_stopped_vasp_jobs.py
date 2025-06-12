import os
import argparse
import shutil

def check_vasp_finished(outcar_path):
    """Check if VASP DFT job finished successfully by looking for 'Voluntary context switches' in OUTCAR."""
    if not os.path.exists(outcar_path):
        return False
    with open(outcar_path, 'r') as file:
        for line in file:
            if "Voluntary context switches" in line:
                return True
    return False

def update_incar(incar_path):
    """Update ISTART and ICHARG in the INCAR file."""
    if not os.path.exists(incar_path):
        print(f"INCAR not found: {incar_path}")
        return
    with open(incar_path, 'r') as file:
        lines = file.readlines()
    with open(incar_path, 'w') as file:
        for line in lines:
            if line.startswith("ISTART"):
                file.write("ISTART=1; ICHARG=1\n")
            else:
                file.write(line)

def process_vasp_jobs(input_file):
    try:
        with open(input_file, 'r') as file:
           paths = file.readlines()
    except:
        paths = [os.getcwd()]

    for path in paths:
        path = path.strip()
        outcar_path = os.path.join(path, 'OUTCAR')
        incar_path = os.path.join(path, 'INCAR')
        poscar_path = os.path.join(path, 'POSCAR')
        contcar_path = os.path.join(path, 'CONTCAR')
        poscar_init_path = os.path.join(path, 'POSCAR_init')
        lock_file = os.path.join(path, 'vasp.lock')

        if not check_vasp_finished(outcar_path):
            print(f"VASP job not finished successfully in: {path}")
            
            # Update INCAR
            update_incar(incar_path)
            
            # Copy POSCAR to POSCAR_init
            if os.path.exists(poscar_path):
                shutil.copy(poscar_path, poscar_init_path)
            
            # Copy CONTCAR to POSCAR
            if os.path.exists(contcar_path):
                shutil.copy(contcar_path, poscar_path)
            
            # Delete vasp.lock
            if os.path.exists(lock_file):
                os.remove(lock_file)
                print(f"Deleted lock file: {lock_file}")
        else:
            print(f"VASP job finished successfully in: {path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check and update VASP DFT jobs.")
    parser.add_argument(
        '-i', '--input',
        default=os.getcwd(),  # Use the current working directory as the default
        help="Path to the input file containing directory paths. Defaults to the current directory."
    )
    args = parser.parse_args()

    print(f"Input path: {args.input}")

    process_vasp_jobs(args.input)
