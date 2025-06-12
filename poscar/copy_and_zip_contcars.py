import os
import shutil
import zipfile

def copy_and_zip_poscars():
    poscars_dir = "./CONTCARS"
    os.makedirs(poscars_dir, exist_ok=True)

    with open('main_job_dirs.txt', 'r') as file:
        paths = file.readlines()

    for path in paths:
        path = path.strip()
        source_poscar = os.path.join(path, 'dft_opt', 'CONTCAR')
        target_poscar = os.path.join(poscars_dir, f"{os.path.basename(path)}.vasp")

        if os.path.exists(source_poscar):
            shutil.copy(source_poscar, target_poscar)

    # Zip the POSCARs directory
    zip_filename = "CONTCARs.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(poscars_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, poscars_dir)
                zipf.write(file_path, arcname)

if __name__ == "__main__":
    copy_and_zip_poscars()

