import os
import shutil

def make_vasp_single():
    with open('main_job_dirs.txt', 'r') as file:
        paths = file.readlines()

    vasp_single_paths = []

    for path in paths:
        path = path.strip()
        vasp_single_path = os.path.join(path, 'dft_single')
        
        if not os.path.exists(vasp_single_path):
            os.makedirs(vasp_single_path)
        
        # Copy files from ./vasp_single_files
        single_files_dir = './vasp_single_files'
        for filename in ['KPOINTS', 'command.txt', 'POTCAR', 'INCAR']:
            shutil.copy(os.path.join(single_files_dir, filename), vasp_single_path)
        
        # Copy out_structure to POSCAR
        mace_opt_path = os.path.join(path, 'mace_opt', 'mac_opt_structure')
        try:  
           shutil.copy(mace_opt_path, os.path.join(vasp_single_path, 'POSCAR'))
        except: continue

        # Add vasp_single_path to the list
        vasp_single_paths.append(vasp_single_path)

    # Write all vasp_single paths to vasp_single_paths.txt
    with open('vasp_single_paths.txt', 'w') as file:
        for vasp_path in vasp_single_paths:
            file.write(vasp_path + '\n')

if __name__ == "__main__":
    make_vasp_single()

