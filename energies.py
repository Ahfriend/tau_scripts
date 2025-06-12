import os

def extract_total_energy_from_oszicar(dft_path):
    oszicar_path = os.path.join(dft_path, 'OSZICAR')
    outcar_path = os.path.join(dft_path, 'OUTCAR')
    
    # Check if the DFT job terminated properly by looking for "Voluntary context switches" in OUTCAR
    if os.path.exists(outcar_path):
        with open(outcar_path, 'r') as outcar_file:
            if not any("Voluntary context switches" in line for line in outcar_file):
                return None  # Job did not terminate properly
    
    # Extract energy from OSZICAR
    if os.path.exists(oszicar_path):
        with open(oszicar_path, 'r') as file:
            lines = file.readlines()
            for line in reversed(lines):
                if 'F=' in line:
                    return float(line.split()[4])  # Taking E0
    return None

def extract_last_energy_from_relaxation_log(relaxation_log_path):
    with open(relaxation_log_path, 'r') as file:
        lines = file.readlines()
        if len(lines) > 1:
            last_line = lines[-1].strip().split()
            if float(last_line[-1]) <= 0.01:  # Check if last fmax value is <= 0.01 
                return round(float(last_line[-2]),5)  # Return the last energy value
    return None

def extract_energy_from_point_energy(point_energy_path):
    with open(point_energy_path, 'r') as file:
        return round(float(file.readline().strip()),5)
    return None


with open('main_job_dirs.txt', 'r') as file:
    paths = file.readlines()

with open('energies.log', 'w') as log_file:
    log_file.write(f'{"path":<30} {"dft_opt":<15} {"mace_opt":<15} {"mace_single":<15} {"single_dft":<15}\n')
    for path in paths:
        path = path.strip()
        dft_opt_energy = None
        mace_opt_energy = None
        mace_single_energy = None
        single_dft_energy = None

        dft_opt = os.path.join(path, 'dft_opt')
        if os.path.exists(dft_opt):
             dft_opt_energy = extract_total_energy_from_oszicar(dft_opt)

        relaxation_log_path = os.path.join(path, 'mace_opt', 'relaxation.log')
        if os.path.exists(relaxation_log_path):
            mace_opt_energy = extract_last_energy_from_relaxation_log(relaxation_log_path)

        point_energy_path = os.path.join(path, 'mace_single', 'point_energy.txt')
        if os.path.exists(point_energy_path):
            mace_single_energy = extract_energy_from_point_energy(point_energy_path)

        single_dft_path = os.path.join(path, 'dft_single')
        if os.path.exists(single_dft_path):
            single_dft_energy = extract_total_energy_from_oszicar(single_dft_path)

        log_file.write(f'{path:<30} {dft_opt_energy if dft_opt_energy is not None else "N/A":<15} {mace_opt_energy if mace_opt_energy is not None else "N/A":<15} {mace_single_energy if mace_single_energy is not None else "N/A":<15} {single_dft_energy if single_dft_energy is not None else "N/A":<15}\n')
