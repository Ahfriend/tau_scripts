#!/bin/bash

# Default SLURM job parameters
job_name="python_job"
output_file="python_job_output.txt"
error_file="python_job_error.txt"
time_limit="01:00:00"
partition="amir-cpu80"
ntasks=1
cpus=40
mem="100G"

# Parse command line arguments for memory, cores, and input_file
while getopts m:c:i:o: flag
do
    case "${flag}" in
        m) mem=${OPTARG:-100GB};;
        c) cpus=${OPTARG:-40};;
        i) input_file=${OPTARG};; 
        o) output_file=${OPTARG:-out_structure};;
    esac
done

# Create a temporary SLURM script with the updated parameters
temp_slurm_script=$(mktemp /tmp/slurm_script.XXXXXX)
cat <<EO > ${temp_slurm_script}
#!/bin/bash
#SBATCH --job-name=${job_name}
#SBATCH --output=${output_file}
#SBATCH --error=${error_file}
#SBATCH --time=${time_limit}
#SBATCH --partition=${partition}
#SBATCH --ntasks=${ntasks}
#SBATCH --cpus-per-task=${cpus}
#SBATCH --mem=${mem}

# Load necessary modules or activate environment
source activate /andata/amir/pydirs/conda/envs/mace-env

# Run the Python script
python /andata/amir/mace_tests/test_2_contcars/energy_relax_mace.py --filename ${input_file} --outfile ${output_file}
EO

# Submit the temporary SLURM script
sbatch ${temp_slurm_script}

# Clean up the temporary SLURM script
rm ${temp_slurm_script}

