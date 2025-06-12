#!/usr/bin/env python
import argparse
import os
from ase.io import read
from mace.calculators import mace_mp

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Calculate energy using MACE from a CONTCAR file.")
    parser.add_argument("--filename", type=str, help="Path to the CONTCAR file (or any ASE-readable file)")
    args = parser.parse_args()
    
    # Check if the input file exists
    if not os.path.exists(args.filename):
        raise FileNotFoundError(f"Input file not found: {args.filename}")
    
    # Read the atomic structure from the specified file
    atoms = read(args.filename, format='vasp')
    
    # Create the MACE calculator instance using the provided model
    calculator = mace_mp()
    
    # Attach the calculator to the atomic configuration
    atoms.set_calculator(calculator)
    
    # Calculate the potential energy
    energy = atoms.get_potential_energy()
    print("Calculated energy:", energy, "eV")

    #write into file
    with open ('point_energy.txt','w') as f:
        f.write(str(energy))
      

if __name__ == "__main__":
    main()

