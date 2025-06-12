#!/bin/bash
#BATCH --job-name=mace_training       # Job name
#SBATCH --output=mace_training.out     # Output file
#SBATCH --error=mace_training.err      # Error file
#SBATCH --partition=engineering                
#SBATCH --cpus-per-task=4              # Number of CPU cores per task
#SBATCH --mem=50G                      # Memory allocation
#SBATCH --time=24:00:00                # Maximum runtime (24 hours)

# Load necessary modules (if required)
module load python/pathon-3.9.18 : Load Python module

# Activate your virtual environment (if applicable)
source /andata/alonh/python_lib/mace/mace_env/bin/activate 

# Run MACE training
mace_run_train --config config.yaml
