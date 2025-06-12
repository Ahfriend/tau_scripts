import os

with open('main_job_dirs.txt', 'r') as file:
    vasp_paths = file.readlines()

for path in vasp_paths:
    path = path.strip()
    mace_opt_dir = os.path.join(path, 'mace_opt')
    mace_single_dir = os.path.join(path, 'mace_single')
    dft_opt_dir = os.path.join(path, 'dft_opt')
    dft_single_dir = os.path.join(path, 'dft_single')
    

    os.makedirs(mace_opt_dir, exist_ok=True)
    os.makedirs(mace_single_dir, exist_ok=True)
    os.makedirs(dft_opt_dir, exist_ok=True)
    os.makedirs(dft_single_dir, exist_ok=True)
