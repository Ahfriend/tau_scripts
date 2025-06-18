import argparse
import os

def add_atoms_to_poscar(source_poscar, target_poscar, atom_index=None):
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

    # Determine the base coordinates for the new atoms
    if atom_index is not None:
        if atom_index < 1 or atom_index > total_atoms:
            raise ValueError(f"Atom index {atom_index} is out of range (1-{total_atoms}).")
        base_atom = atom_coordinates[atom_index - 1].split()
    else:
        base_atom = atom_coordinates[-1].split()  # Default to the last atom

    x, y, z = map(float, base_atom[:3])

    # Ensure the last atom line ends with a newline character
    if not atom_coordinates[-1].endswith("\n"):
        atom_coordinates[-1] += "\n"

    # Extract the elements line
    elements = lines[5].split()

    # Find the index where O atoms end
    o_atom_count = atom_counts[elements.index("O")] if "O" in elements else 0
    o_atom_start_index = sum(atom_counts[:elements.index("O")]) 
    print (f"o_atom_start_index: {o_atom_start_index}")
    print (elements.index("O"))
    print (f"o_atom_count: {o_atom_count}")
    o_atom_end_index = o_atom_start_index + o_atom_count
    print (f"o_atom_end_index: {o_atom_end_index}")

    # Insert the new O atom at the end of the O atoms
    new_oxygen_line = f"{x:.6f} {y:.6f} {z + 0.038:.6f} T   T   T\n"
    atom_coordinates.insert(o_atom_end_index, new_oxygen_line)

    # Add the new H atom
    new_hydrogen_line = f"{x:.6f} {y:.6f} {z + 0.07:.6f} T   T   T\n"
    atom_coordinates.append(new_hydrogen_line)

    # Update the atom count
    atom_counts = list(map(int, lines[6].split()))
    atom_counts[elements.index("O")] += 1  # Add O atom count
    atom_counts.append(1)  #  Assuming H is the last atom type
    lines[6] = " ".join(map(str, atom_counts)) + "\n"

    # Update the elements line to include O and H if not already present
    elements = lines[5].split()
    if "O" not in elements:
        elements.append("O")
    if "H" not in elements:
        elements.append("H")
    lines[5] = " ".join(elements) + "\n"

    # Write the updated POSCAR
    with open(target_poscar, 'w') as poscar_file:
        poscar_file.writelines(lines[:atom_coordinates_start] + atom_coordinates)


def update_poscar_with_oxygen_and_hydrogen():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Update POSCAR files with oxygen and hydrogen.")
    parser.add_argument("-s", "--source", required=True, help="Path to the source directory")
    parser.add_argument("-i", "--index", type=int, help="Index of the atom to use as the base for the new atoms (1-based)")
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
        source_poscar = os.path.join(source, path, 'dft_opt', 'POSCAR')
        target_poscar = os.path.join(dft_opt_path, 'POSCAR')

        # Check if CONTCAR exists at the target path
        contcar_path = os.path.join(dft_opt_path, 'CONTCAR')
        if os.path.exists(contcar_path):
            print('there is a job here')
            continue

        # Ensure the target directory exists
        os.makedirs(dft_opt_path, exist_ok=True)

        # Call the function to add atoms to the POSCAR
        add_atoms_to_poscar(source_poscar, target_poscar, atom_index)


if __name__ == "__main__":
    update_poscar_with_oxygen_and_hydrogen()
