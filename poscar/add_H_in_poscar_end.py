import argparse
import os

def update_poscar_with_hydrogen():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Update POSCAR files with hydrogen.")
    parser.add_argument("-s", "--source", required=True, help="Path to the source directory")
    parser.add_argument("-i", "--index", type=int, help="Index of the atom to use as the base for the new hydrogen atom (1-based)")
    parser.add_argument("-f", "--file", default="main_job_dirs.txt", help="Path to the input file (default: main_job_dirs.txt)")
    args = parser.parse_args()
    source = args.source
    atom_index = args.index
    input_file = args.file

    with open(input_file, 'r') as file:
        paths = file.readlines()

    for path in paths:
        print(path)
        path = path.strip()
        dft_opt_path = os.path.join(path, 'dft_opt')
        print(dft_opt_path)
        source_poscar = os.path.join(source, path, 'dft_opt', 'POSCAR')
        print(source_poscar)
        target_poscar = os.path.join(dft_opt_path, 'POSCAR')
        print(target_poscar)

        # Check if CONTCAR exists at the target path
        contcar_path = os.path.join(dft_opt_path, 'CONTCAR')
        if os.path.exists(contcar_path):
            print('there is a job here')
            continue

        # Ensure the target directory exists
        os.makedirs(dft_opt_path, exist_ok=True)

        # Read the source POSCAR file
        with open(source_poscar, 'r') as poscar_file:
            lines = poscar_file.readlines()

        # Extract the atom coordinates and filter out zero-only lines
        atom_coordinates_start = 9  # Assuming coordinates start at line 8
        # Determine the number of atoms from the atom counts line
        atom_counts = list(map(int, lines[6].split()))
        total_atoms = sum(atom_counts)

        # Extract the atom coordinates based on the total number of atoms
        atom_coordinates = lines[atom_coordinates_start:atom_coordinates_start + total_atoms]

        print(len(atom_coordinates))

        # Determine the base coordinates for the new atom
        if atom_index is not None:
            if atom_index < 1 or atom_index > total_atoms:
                raise ValueError(f"Atom index {atom_index} is out of range (1-{total_atoms}).")
            base_atom = atom_coordinates[atom_index - 1].split()
        else:
            base_atom = atom_coordinates[-1].split()  # Default to the last atom

        x, y, z = map(float, base_atom[:3])

        # Add the new H atom
        new_atom_line = f"{x:.6f} {y:.6f} {z + 0.032:.6f} T   T   T\n"
        if not atom_coordinates[-1].endswith("\n"):
            atom_coordinates[-1] = atom_coordinates[-1] + "\n"
        atom_coordinates.append(new_atom_line)

        # Update the atom count
        atom_counts = list(map(int, lines[6].split()))
        atom_counts.append(1)  # Assuming H is the last atom type
        lines[6] = " ".join(map(str, atom_counts)) + "\n"

        # Update the elements line to include H if not already present
        elements = lines[5].split()
        if "H" not in elements:
            elements.append("H")
        lines[5] = " ".join(elements) + "\n"

        # Write the updated POSCAR
        with open(target_poscar, 'w') as poscar_file:
            poscar_file.writelines(lines[:atom_coordinates_start] + atom_coordinates)


if __name__ == "__main__":
    update_poscar_with_hydrogen()
