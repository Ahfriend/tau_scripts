import argparse
from ase.io import read, write
import random

def split_xyz(input_xyz, train_ratio, val_ratio, test_ratio, seed=42):
    """
    Splits an .xyz file into training, validation, and test sets.

    Parameters:
        input_xyz (str): Path to the input .xyz file.
        train_ratio (float): Proportion of data for training.
        val_ratio (float): Proportion of data for validation.
        test_ratio (float): Proportion of data for testing.
        seed (int): Random seed for reproducibility.

    Outputs:
        Writes train.xyz, val.xyz, and test.xyz files.
    """
    # Check that the ratios sum to 1
    if not abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6:
        raise ValueError("Train, validation, and test ratios must sum to 1.")

    # Read all structures from the input .xyz file
    structures = read(input_xyz, index=":")
    print(f"Loaded {len(structures)} structures from {input_xyz}")

    # Shuffle the structures
    random.seed(seed)
    random.shuffle(structures)

    # Split the data
    n_total = len(structures)
    n_train = int(train_ratio * n_total)
    n_val = int(val_ratio * n_total)

    train_set = structures[:n_train]
    val_set = structures[n_train:n_train + n_val]
    test_set = structures[n_train + n_val:]

    # Write the splits to separate .xyz files
    write("train.xyz", train_set, format="extxyz")
    write("val.xyz", val_set, format="extxyz")
    write("test.xyz", test_set, format="extxyz")

    print(f"Training set: {len(train_set)} structures written to train.xyz")
    print(f"Validation set: {len(val_set)} structures written to val.xyz")
    print(f"Test set: {len(test_set)} structures written to test.xyz")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Split an .xyz file into training, validation, and test sets.")
    parser.add_argument("-i","--input_xyz", type=str, help="Path to the input .xyz file")
    parser.add_argument("--train_ratio", type=float, default=0.8, help="Proportion of data for training (default: 0.8)")
    parser.add_argument("--val_ratio", type=float, default=0.1, help="Proportion of data for validation (default: 0.1)")
    parser.add_argument("--test_ratio", type=float, default=0.1, help="Proportion of data for testing (default: 0.1)")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducibility (default: 42)")

    # Parse arguments
    args = parser.parse_args()

    # Call the split function
    split_xyz(args.input_xyz, args.train_ratio, args.val_ratio, args.test_ratio, args.seed)
