import os
import shutil

def make_vasp_single():
    with open('main_job_dirs.txt', 'r') as file:
        paths = file.readlines()

    vasp_single_paths = []

    for path in paths:
        print (path)
        path = path.strip()
        vasp_single_path = os.path.join(path, 'dft_opt')
        
        if not os.path.exists(vasp_single_path):
            os.makedirs(vasp_single_path)

        # Check if CONTCAR exists at the target path
        #contcar_path = os.path.join(vasp_single_path, 'CONTCAR')
        #if os.path.exists(contcar_path):
        #    print('there is a job here')
        #    continue
        
        # Copy files from ./vasp_single_files
        single_files_dir = './vasp_opt_files'
        for filename in ['KPOINTS', 'command.txt', 'POTCAR', 'INCAR']:
            shutil.copy(os.path.join(single_files_dir, filename), vasp_single_path)
        
        # Copy out_structure to POSCAR

        try:
            poscar_files = [f for f in os.listdir(path) if f.startswith('POSCAR_combined_da') and f.endswith('_modified.vasp')]
            for poscar_file in poscar_files:
               shutil.copy(os.path.join(path, poscar_file), os.path.join(vasp_single_path, 'POSCAR'))
               break
        except Exception as e:
            print(f"Error copying POSCAR file: {e}")
            continue


        # Add vasp_single_path to the list
        vasp_single_paths.append(vasp_single_path)

    # Write all vasp_single paths to vasp_single_paths.txt
    with open('vasp_paths.txt', 'w') as file:
        for vasp_path in vasp_single_paths:
            file.write(vasp_path + '\n')

if __name__ == "__main__":
    make_vasp_single()

