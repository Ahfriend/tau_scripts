import os

def add_selective_dynamics(poscar_path, selective_dynamics):
    """
    Adds Selective Dynamics to a POSCAR file.

    Parameters:
        poscar_path (str): Path to the POSCAR file.
        selective_dynamics (list): List of 'T T T' or 'F F F' strings for each atom.
    """
    try:
        # Read the POSCAR file
        with open(poscar_path, 'r') as file:
            lines = file.readlines()

        # Check if Selective Dynamics is already present
        if "Selective Dynamics" in lines[7]:
            print(f"Selective Dynamics already present in {poscar_path}. Skipping modification.")
            return

        # Add Selective Dynamics
        lines.insert(7, "Selective Dynamics\n")
        for i, dynamics in enumerate(selective_dynamics):
            lines[8 + i] = lines[8 + i].strip() + f" {dynamics}\n"

        # Write the modified POSCAR file
        with open(poscar_path, 'w') as file:
            file.writelines(lines)

        print(f"Selective Dynamics added to {poscar_path}.")
    except FileNotFoundError:
        print(f"POSCAR file not found: {poscar_path}")
    except Exception as e:
        print(f"An error occurred while modifying {poscar_path}: {e}")

def process_paths(input_file=None):
    """
    Processes paths and adds Selective Dynamics to POSCAR files.

    Parameters:
        input_file (str): Path to the file containing paths. If None, modifies local POSCAR.
    """
    selective_dynamics = []
    num_atoms = int(input("Enter the number of atoms in the POSCAR file: "))
    print("Enter 'T T T' or 'F F F' for each atom:")
    for i in range(num_atoms):
        dynamics = input(f"Atom {i + 1}: ").strip()
        selective_dynamics.append(dynamics)

    if input_file:
        # Read paths from the input file
        try:
            with open(input_file, 'r') as file:
                paths = file.read().splitlines()

            # Iterate over each path and modify POSCAR
            for path in paths:
                poscar_path = os.path.join(path, "POSCAR")
                add_selective_dynamics(poscar_path, selective_dynamics)
        except FileNotFoundError:
            print(f"Input file not found: {input_file}")
        except Exception as e:
            print(f"An error occurred while processing paths: {e}")
    else:
        # Modify local POSCAR file
        local_poscar = "POSCAR"
        add_selective_dynamics(local_poscar, selective_dynamics)

if __name__ == "__main__":
    input_file = input("Enter the path to the input file (leave blank to modify local POSCAR): ").strip()
    input_file = input_file if input_file else None
    process_paths(input_file)
