import os

# Read the paths from permutation_paths.txt
with open('main_job_dirs.txt', 'r') as file:
    paths = [path.strip() for path in file.readlines() if path.strip()]

# Number of paths per job
paths_per_job = 20
total_jobs = (len(paths) + paths_per_job - 1) // paths_per_job

# Generate SLURM job scripts
for job_num in range(total_jobs):
    job_paths = paths[job_num * paths_per_job:(job_num + 1) * paths_per_job]
    job_name = f"mace_single_batch_{job_num + 1}"
    
    script_content = f"""#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --partition=engineering
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --mem=60G
#SBATCH --output={job_name}.out
#SBATCH --error={job_name}.err

source activate /andata/amir/pydirs/conda/envs/mace-env

"""
    for path in job_paths:
        mace_opt_dir = os.path.join(path, 'mace_single')
        script_content += f"cd {mace_opt_dir}\n"
        #script_content += f"python /andata/amir/mace_tests/scripts/selective_energy_relax_mace_novol.py  --filename ../dft_opt/POSCAR --outfile out_structure\n"
        script_content += f"python /work/alonh/scripts/single_point_energy.py  --filename ../dft_opt/CONTCAR\n"
        script_content += "cd -\n"

    script_path = f"./{job_name}.sh"
    with open(script_path, 'w') as script_file:
        script_file.write(script_content)

