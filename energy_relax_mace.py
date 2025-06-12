#!/usr/bin/env python
import argparse
import os
from ase.io import read, write
from ase.optimize import BFGS
from ase.constraints import ExpCellFilter
from mace.calculators import mace_mp  # Using the correct MACE interface as provided

def main():
    # Set up command-line arguments
    parser = argparse.ArgumentParser(
        description="Relax a structure (atomic positions and cell) using MACE and BFGS."
    )
    parser.add_argument("--filename", type=str,
                        help="Path to the input structure file (e.g., CONTCAR)")

    args = parser.parse_args()

    # Check that the input file exists
    if not os.path.exists(args.filename):
        raise FileNotFoundError(f"Input file not found: {args.filename}")

    # Read the input structure using ASE
    atoms = read(args.filename, format='vasp')
    
    # Create the MACE calculator instance using the mace_mp interface
    calculator = mace_mp()
    atoms.set_calculator(calculator)
    
    # Calculate and print the initial potential energy
    initial_energy = atoms.get_potential_energy()
    print("Initial potential energy: {:.4f} eV".format(initial_energy))

    # Set up the relaxation to optimize both atomic positions and the cell shape/size
    ecf = ExpCellFilter(atoms)
    optimizer = BFGS(ecf, logfile="relaxation.log")
    print("Starting relaxation...")
    optimizer.run(fmax=0.01)

    # Calculate and print the final potential energy
    final_energy = atoms.get_potential_energy()
    print("Final potential energy: {:.4f} eV".format(final_energy))
    
    # Write the final relaxed structure to the output file in VASP CONTCAR format
    write("out_structure", atoms, format="vasp")
    print("Final relaxed structure written to:", "out_structure")

if __name__ == "__main__":
    main()

