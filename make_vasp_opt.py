import os
import shutil

def make_vasp_single():
    with open('main_job_dirs.txt', 'r') as file:
        paths = file.readlines()

    vasp_single_paths = []

    for path in paths:
        print(path)
        path = path.strip()
        vasp_single_path = os.path.join(path, 'dft_opt')

        if not os.path.exists(vasp_single_path):
            os.makedirs(vasp_single_path)

        # Check if vasp_opt_file/poscar.vasp exists
        opt_poscar_path = os.path.join('vasp_opt_files', 'poscar.vasp',f'{path}.vasp')
        print (f'opt_poscar_path: {opt_poscar_path}')
        if os.path.exists(opt_poscar_path):
            try:
                # Copy poscar.vasp to dft_opt as POSCAR
                shutil.copy(opt_poscar_path, os.path.join(vasp_single_path, 'POSCAR'))
            except Exception as e:
                print(f"Error copying poscar.vasp: {e}")
                continue

        # Copy files from ./vasp_opt_files
        single_files_dir = './vasp_opt_files'
        for filename in ['KPOINTS', 'command.txt', 'POTCAR', 'INCAR']:
            shutil.copy(os.path.join(single_files_dir, filename), vasp_single_path)

        # Copy additional POSCAR files in the form path.vasp
        try:
            poscar_files = [f for f in os.listdir(path) if f.endswith('.vasp')]
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
