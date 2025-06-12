def add_selective_dynamics_freeze_layers(poscar_path, n_freeze):
    """
    Adds or updates Selective Dynamics in a POSCAR file and freezes the n lowest layers based on z-axis values.

    Parameters:
        poscar_path (str): Path to the POSCAR file.
        n_freeze (int): Number of lowest layers to freeze.
    """
    try:
        print(f"Debug: Attempting to read POSCAR file from {poscar_path}")
        # Read the POSCAR file
        with open(poscar_path, 'r') as file:
            lines = file.readlines()

        print(f"Debug: Successfully read POSCAR file. Total lines: {len(lines)}")
        print(f"Debug: POSCAR file contents:\n{''.join(lines)}")

        # Validate POSCAR format
        if len(lines) < 8:
            raise ValueError("POSCAR file is incomplete or incorrectly formatted.")
        print("Debug: POSCAR file format validated.")

        # Check if Selective Dynamics is already present
        has_selective_dynamics = "Selective Dynamics" in lines[7]
        print(f"Debug: Selective Dynamics present: {has_selective_dynamics}")

        # Extract atomic positions (assumes Direct coordinates)
        start_index = 8 if has_selective_dynamics else 7
        atomic_positions = lines[start_index:]
        print(f"Debug: Extracted atomic positions. Total positions: {len(atomic_positions)}")

        if len(atomic_positions) == 0:
            raise ValueError("POSCAR file does not contain atomic positions.")

        # Remove atomic symbols if present
        atomic_positions = [atom.strip().split()[:3] for atom in atomic_positions]
        print(f"Debug: Atomic positions after removing symbols: {atomic_positions}")

        # Sort atoms by z-axis value
        atomic_positions = sorted(atomic_positions, key=lambda x: float(x[2]))
        print(f"Debug: Atomic positions sorted by z-axis: {atomic_positions}")

        # Add or update Selective Dynamics
        if not has_selective_dynamics:
            lines.insert(7, "Selective Dynamics\n")
            print("Debug: Added Selective Dynamics header.")
        for i, atom in enumerate(atomic_positions):
            dynamics = "F F F" if i < n_freeze else "T T T"
            atom_line = " ".join(atom[:3]) + f" {dynamics}\n"
            atomic_positions[i] = atom_line
        print(f"Debug: Updated atomic positions with Selective Dynamics: {atomic_positions}")

        # Write the modified POSCAR file
        with open(poscar_path, 'w') as file:
            file.writelines(lines[:8])  # Write header
            file.writelines(atomic_positions)  # Write updated atomic positions
        print(f"Debug: Successfully wrote updated POSCAR file to {poscar_path}")

        print(f"Selective Dynamics added or updated in {poscar_path}. Frozen {n_freeze} lowest layers.")
    except FileNotFoundError:
        print(f"POSCAR file not found: {poscar_path}")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An error occurred while modifying {poscar_path}: {e}")


if __name__ == "__main__":
    poscar_path = input("Enter the path to the POSCAR file: ").strip()
    n_freeze = int(input("Enter the number of lowest layers to freeze: "))
    add_selective_dynamics_freeze_layers(poscar_path, n_freeze)
