import argparse
from ase.io import read, write
from pathlib import Path

def generate_xyz_from_ionic_steps(dft_output_path, output_xyz_file):
    """
    Reads all ionic steps from a DFT output (vasprun.xml) and writes them to an XYZ file.

    Parameters:
        dft_output_path (str): Path to the directory containing vasprun.xml.
        output_xyz_file (str): Path to the output XYZ file.
    """
    try:
        vasprun_file = Path(dft_output_path) / "vasprun.xml"
        # Read all ionic steps from vasprun.xml
        structures = read(vasprun_file, index=":")  # ":" reads all steps
        print(f"Loaded {len(structures)} ionic steps from {vasprun_file}")

        # Add energy and forces as metadata for each structure
        for structure in structures:
            structure.info['energy'] = structure.get_potential_energy()
            structure.arrays['forces'] = structure.get_forces()
            structure.info['comment'] = f"Energy: {structure.info['energy']}"

        # Write all structures to an XYZ file
        write(output_xyz_file, structures, format='extxyz')
        print(f"XYZ file written to {output_xyz_file}")

    except FileNotFoundError:
        print(f"File not found: {vasprun_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_dft_jobs(input_file, output_xyz_file):
    """
    Processes multiple DFT job paths from an input file and generates a combined XYZ file.

    Parameters:
        input_file (str): Path to the input file containing DFT job paths.
        output_xyz_file (str): Path to the output XYZ file.
    """
    try:
        # Read all paths from the input file
        with open(input_file, "r") as file:
            dft_paths = [line.strip() for line in file if line.strip()]

        all_structures = []

        # Iterate over each DFT job path
        for dft_path in dft_paths:
            vasprun_file = Path(dft_path) / "vasprun.xml"
            try:
                # Read all ionic steps from vasprun.xml
                structures = read(vasprun_file, index=":")  # ":" reads all steps
                print(f"Loaded {len(structures)} ionic steps from {vasprun_file}")

                # Add energy and forces as metadata for each structure
                for structure in structures:
                    structure.info['energy'] = structure.get_potential_energy()
                    structure.arrays['forces'] = structure.get_forces()
                    structure.info['comment'] = f"Energy: {structure.info['energy']}"

                # Append structures to the combined list
                all_structures.extend(structures)

            except FileNotFoundError:
                print(f"File not found: {vasprun_file}")
            except Exception as e:
                print(f"An error occurred while processing {vasprun_file}: {e}")

        # Write all combined structures to an XYZ file
        write(output_xyz_file, all_structures, format='extxyz')
        print(f"Combined XYZ file written to {output_xyz_file}")

    except FileNotFoundError:
        print(f"Input file not found: {input_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate XYZ files from DFT job paths.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input file containing DFT job paths.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output XYZ file.")
    args = parser.parse_args()

    process_dft_jobs(args.input, args.output)
