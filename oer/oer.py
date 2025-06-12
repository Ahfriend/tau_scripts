import os
import json
import subprocess
import pandas as pd

def Etots(E_slab, E_slab_OH , E_slab_O, E_slab_OOH,U):
    E_H2  = -.67734730E+01
    E_H2O = -.14237440E+02
    E_O2 = -.98885499E+01

    delta_E_OH =  E_slab_OH     + 0.5 * E_H2 + E_H2O - E_slab - 2*E_H2O
    delta_E_O =   E_slab_O      + 1.0 * E_H2 + E_H2O - E_slab - 2*E_H2O
    delta_E_OOH = E_slab_OOH    + 1.5 * E_H2         - E_slab - 2*E_H2O
    #delta_E_O2 =  E_slab_110 + E_O2 + 2.0 * E_H2    - E_slab_110 - 2*E_H2O

    delta_E_O2 =  2.46 * 2   # from Northkov paper   H2O -> 1/2 O2 + H2   E = 2.46 eV
    
    etots = [0,delta_E_OH, delta_E_O, delta_E_OOH, delta_E_O2]
  
    delta_G_values = [0, delta_E_OH +0.35 - U, delta_E_O + 0.05 - 2*U, delta_E_OOH +0.4 - 3*U, 4.92 - 4*U]
    

    return etots, delta_G_values


def read_energies_log(file_path):
    df = pd.read_csv(file_path, delim_whitespace=True, names=["path", "dft_opt", "mace_opt", "mace_single", "single_dft"])
    # Convert columns to numeric, forcing errors to NaN
    df["dft_opt"] = pd.to_numeric(df["dft_opt"], errors='coerce')
    df["mace_opt"] = pd.to_numeric(df["mace_opt"], errors='coerce')
    df["mace_single"] = pd.to_numeric(df["mace_single"], errors='coerce')
    df["single_dft"] = pd.to_numeric(df["single_dft"], errors='coerce')
    return df

def process_oer_energies(input_file):
    try:
        with open(input_file, 'r') as f:
            paths = json.load(f)
            print(paths)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON file: {e}")
        return None

    OH_path = str(paths["OH"])
    O_path = str(paths["O"])
    OOH_path = str(paths["OOH"])
    match_path = str(paths["match"])    

    #Call the energies.py script for each path
    #with open("all_energies.log", "w") as outfile:
    #    for path in [OH_path, O_path, OOH_path,match_path]:
    #        os.chdir(path)
    #        subprocess.run(["python", "/work/alonh/scripts/energies.py"])
    #        os.chdir('..')
    #        with open(os.path.join(path, "energies.log"), "r") as infile:
    #            outfile.write(f"--- Energies from {path} ---\n")
    #            outfile.write(infile.read())
    #            outfile.write("\n")

    # Read energies.log files into DataFrames
    OH_energies_df = read_energies_log(os.path.join(OH_path, "energies.log"))
    O_energies_df = read_energies_log(os.path.join(O_path, "energies.log"))
    OOH_energies_df = read_energies_log(os.path.join(OOH_path, "energies.log"))
    match_energies_df = read_energies_log(os.path.join(match_path, "energies.log"))

    # Find the lowest value and its path for each column in each DataFrame
    lowest_values = {}
    for key, df in {"OH": OH_energies_df, "O": O_energies_df, "OOH": OOH_energies_df, "match": match_energies_df}.items():
        lowest_values[key] = {}
        for column in ["dft_opt", "mace_opt", "mace_single", "single_dft"]:
            if df[column].notna().any():  # Check if the column has any non-NaN values
                row = df.loc[df[column].idxmin()]
                lowest_values[key][column] = (row[column], row["path"])
            else:
                lowest_values[key][column] = (None, None)  # Handle columns with only NaN values

    # Write the lowest values and their paths to a file
    with open("lowest_values.txt", "w") as file:
        for key, values in lowest_values.items():
            file.write(f"Lowest values for {key}:\n")
            for column, (value, path) in values.items():
                if value is not None:
                    file.write(f"{column}: {value} (Path: {path})\n")
                else:
                    file.write(f"{column}: No valid data\n")
            file.write("\n")

    # Create a DataFrame with the required information
    data = {
        "OH": [
            OH_energies_df["dft_opt"].min(),
            OH_energies_df["mace_opt"].min(),
            OH_energies_df["mace_single"].min(),
            OH_energies_df["single_dft"].min()
        ],
        "O": [
            O_energies_df["dft_opt"].min(),
            O_energies_df["mace_opt"].min(),
            O_energies_df["mace_single"].min(),
            O_energies_df["single_dft"].min()
        ],
        "OOH": [
            OOH_energies_df["dft_opt"].min(),
            OOH_energies_df["mace_opt"].min(),
            OOH_energies_df["mace_single"].min(),
            OOH_energies_df["single_dft"].min()
        ]
    }
    result_df = pd.DataFrame(data, index=["dft_opt", "mace_opt", "mace_single", "dft_single"])

    # Add 'slab' column with values from match_energies_df where dft_opt is min
    min_dft_opt_row = match_energies_df.loc[match_energies_df["dft_opt"].idxmin()]
    print (min_dft_opt_row)
    result_df["slab"] = min_dft_opt_row.values[1:len(result_df.index)+1]

    return result_df


import argparse
    
if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process and plot step graphs.")
    parser.add_argument("-u", "--uvalue", type=float, default=1.23, help="Value of u (default: 1.23)")
    args = parser.parse_args()

    # Access the u value
    U = args.uvalue
    print(f"Using u value: {U}")

    input_file = "energy_paths.json"
    result_df = process_oer_energies(input_file)
    print(result_df)

    result_df.loc["dft_single", "slab"] = result_df.loc["dft_opt", "slab"]

    print (result_df)
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use('Agg')  # Use a non-interactive backend

    # Define the steps
    steps = ['Initial', 'OH', 'O', 'OOH', 'O2']
    
    # Calculate Etots for each optimization method
    etots_dft_opt, deltaGs_dft_opt = Etots(result_df.loc["dft_opt", "slab"], result_df.loc["dft_opt", "OH"], result_df.loc["dft_opt", "O"], result_df.loc["dft_opt", "OOH"], U)
    etots_mace_opt, deltaGs_mace_opt = Etots(result_df.loc["mace_opt", "slab"], result_df.loc["mace_opt", "OH"], result_df.loc["mace_opt", "O"], result_df.loc["mace_opt", "OOH"], U)
    etots_mace_single, deltaGs_mace_single = Etots(result_df.loc["mace_single", "slab"], result_df.loc["mace_single", "OH"], result_df.loc["mace_single", "O"], result_df.loc["mace_single", "OOH"], U)
    etots_dft_single, deltaGs_dft_single = Etots(result_df.loc["dft_single", "slab"], result_df.loc["dft_single", "OH"], result_df.loc["dft_single", "O"], result_df.loc["dft_single", "OOH"], U)
    print ('single: ',etots_dft_single, deltaGs_dft_single)
    # Create the Etots table
    etots_table = pd.DataFrame({
        "Steps": steps,
        "DFT_Opt": etots_dft_opt,
        "MACE_Opt": etots_mace_opt,
        "MACE_Single": etots_mace_single,
        "DFT_Single": etots_dft_single
    })

    # Create the Etots table in transposed form
    etots_table_transposed = etots_table.set_index("Steps").transpose()
    # Create the Delta Gs table
    deltaGs_table = pd.DataFrame({
        "Steps": steps,
        "DFT_Opt": deltaGs_dft_opt,
        "MACE_Opt": deltaGs_mace_opt,
        "MACE_Single": deltaGs_mace_single,
        "DFT_Single": deltaGs_dft_single
    })

    # Create the Delta Gs table in transposed form
    deltaGs_table_transposed = deltaGs_table.set_index("Steps").transpose()
    print("\nEtots Table:")
    print(etots_table_transposed)

    print("\nDelta Gs Table:")
    print(deltaGs_table_transposed)

    # Open a file to save the tables
    with open(f"OER_steps_delta_E.txt", "w") as file:
        # Write the U value at the top
        #file.write(f"U value: {U}\n\n")

        # Write the Etots table
        file.write("Etots Table:\n")
        file.write(etots_table_transposed.to_string())
        file.write("\n\n")

        # Write the Delta Gs table
        #file.write("Delta Gs Table:\n")
    with open(f"OER_steps_delta_G_U_{U}.txt", "w") as file:
        file.write(deltaGs_table_transposed.to_string())
        #file.write("\n")

    # Plot the step graph for each optimization method
    print ('ploting graph')

    plt.step(steps, deltaGs_dft_opt, where='mid', label='DFT_Opt')
    for i, txt in enumerate(deltaGs_dft_opt):
        plt.text(steps[i], deltaGs_dft_opt[i], f'{txt:.2f}', ha='center', va='bottom')

    plt.step(steps, deltaGs_mace_opt, where='mid', label='MACE_Opt')
    for i, txt in enumerate(deltaGs_mace_opt):
        plt.text(steps[i], deltaGs_mace_opt[i], f'{txt:.2f}', ha='center', va='bottom')

    plt.step(steps, deltaGs_mace_single, where='mid', label='MACE_Single')
    for i, txt in enumerate(deltaGs_mace_single):
        plt.text(steps[i], deltaGs_mace_single[i], f'{txt:.2f}', ha='center', va='bottom')

    plt.step(steps, deltaGs_dft_single, where='mid', label='DFT Single')
    for i, txt in enumerate(deltaGs_dft_single):
        plt.text(steps[i], deltaGs_dft_single[i], f'{txt:.2f}', ha='center', va='bottom')
    print ('line were ploted')
    plt.text(0.5, max(deltaGs_dft_opt) + 0.5, f'U = {U} V', ha='center', va='bottom', fontsize=12, color='blue')

    plt.xlabel('Reaction Steps')
    plt.ylabel('Delta G (eV)')
    plt.title('Free Energy Diagram')
    plt.legend()
 
    #plt.show()
    print ('before save')
    plt.savefig(f'oer_graph_{U}V.png')
    print ('after save')

