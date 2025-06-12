import os
import argparse

def update_incar_magmom(poscar_path, incar_path, magmom_values):
    """
    Updates the MAGMOM value in the INCAR file based on the atom order in the POSCAR file.

    Parameters:
        poscar_path (str): Path to the POSCAR file.
        incar_path (str): Path to the INCAR file.
        magmom_values (dict): Dictionary of atom types and their MAGMOM values.
    """
    try:
        # Read the POSCAR file to get the atom order and counts
        with open(poscar_path, 'r') as poscar_file:
            lines = poscar_file.readlines()

        # Extract atom types and their counts
        atom_types = lines[5].split()
        atom_counts = list(map(int, lines[6].split()))

        # Generate the MAGMOM string
        magmom_list = []
        for atom, count in zip(atom_types, atom_counts):
            mag_value = magmom_values.get(atom, 0)  # Default to 0 if not specified
            magmom_list.append(f"{count}*{mag_value}")

        magmom_string = " ".join(magmom_list)

        # Read the INCAR file
        with open(incar_path, 'r') as incar_file:
            incar_lines = incar_file.readlines()

        # Update or add the MAGMOM line
        magmom_updated = False
        for i, line in enumerate(incar_lines):
            if line.strip().startswith("MAGMOM"):
                incar_lines[i] = f"MAGMOM = {magmom_string}\n"
                magmom_updated = True
                break

        if not magmom_updated:
            incar_lines.append(f"MAGMOM = {magmom_string}\n")

        # Write the updated INCAR file
        with open(incar_path, 'w') as incar_file:
            incar_file.writelines(incar_lines)

        print(f"Updated MAGMOM in {incar_path} based on {poscar_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Update MAGMOM in INCAR files based on POSCAR atom order.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input file containing paths to job directories.")
    parser.add_argument("-m", "--magmom", nargs="+", help="MAGMOM values for specific atoms in the format 'Atom=Value'. Default is 0 for unspecified atoms.")

    args = parser.parse_args()

    # Parse MAGMOM values
    magmom_values = {}
    if args.magmom:
        for magmom in args.magmom:
            atom, value = magmom.split("=")
            magmom_values[atom] = float(value)

    # Read the input file
    try:
        with open(args.input, 'r') as input_file:
            paths = input_file.read().splitlines()

        # Iterate over each path and update the INCAR file
        for path in paths:
            poscar_path = os.path.join(path, "POSCAR")
            incar_path = os.path.join(path, "INCAR")

            if os.path.exists(poscar_path) and os.path.exists(incar_path):
                update_incar_magmom(poscar_path, incar_path, magmom_values)
            else:
                print(f"POSCAR or INCAR not found in {path}. Skipping...")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
