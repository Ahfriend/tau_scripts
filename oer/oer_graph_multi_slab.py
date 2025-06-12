import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def process_and_collect(slab_name, slab_path, all_data):
    """
    Reads the OER_steps_delta_G_U_1.23.txt file, processes the data, and collects step graph data.

    Parameters:
        slab_name (str): Name of the slab.
        slab_path (str): Path to the directory containing OER_steps_delta_G_U_1.23.txt.
        all_data (dict): Dictionary to collect data for all slabs.
    """
    file_path = slab_path

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    try:
        # Read the table into a DataFrame
        df = pd.read_csv(file_path, sep='\s+')

        print(f"Data for {slab_name} loaded successfully.")

        # Extract the lowest values between 'DFT Opt' and 'DFT Single' for each column
        columns = ["Initial", "OH", "O", "OOH", "O2"]
        if not all(col in df.columns for col in columns):
            print(f"Skipping {slab_name} due to missing required columns.")
            return

        lowest_values = df.loc[df["Steps"] == "DFT_Opt", columns].squeeze().combine(
            df.loc[df["Steps"] == "DFT_Single", columns].squeeze(),
            min
        )

        # Collect data for the slab
        all_data[slab_name] = lowest_values

    except Exception as e:
        print(f"Error processing {file_path}: {e}")


reaction_steps = ['Initial', 'OH', 'O', 'OOH', 'O2']

def plot_all_step_graphs(all_data, slab_colors, output_name):
    """
    Plots all step graphs on a single plot, using the same style as the previous cell.
    For each series, finds the highest delta between the right step and the left step
    and writes it on the diagonal line between the relevant steps.

    Parameters:
        all_data (dict): Dictionary containing step graph data for all slabs.
        slab_colors (dict): Dictionary mapping slab names to colors.
        output_name (str): Name of the output file to save the plot.
    """
    plt.figure(figsize=(8, 5))
    step_positions = range(len(reaction_steps))
    step_width = 0.5
    shrink = 0.6

    handles = []
    for idx, (slab_name, lowest_values) in enumerate(all_data.items()):
        y = np.array(lowest_values, dtype=float)
        x = np.array(step_positions, dtype=float)
        x_left = x - shrink / 2
        x_right = x + shrink / 2
        color = slab_colors.get(slab_name, plt.cm.tab10(idx))  # Default to tab10 if no color is specified

        # Find the highest positive delta and annotate it
        max_delta = 0
        max_delta_index = -1
        for i in range(len(x) - 1):
            delta = y[i + 1] - y[i]
            if delta > max_delta:
                max_delta = delta
                max_delta_index = i

            # Plot horizontal and diagonal lines
            plt.plot([x_left[i], x_right[i]], [y[i], y[i]], color=color, linewidth=2)
            plt.plot([x_right[i], x_left[i + 1]], [y[i], y[i + 1]], color=color, linestyle='--', linewidth=1)
        plt.plot([x_left[-1], x_right[-1]], [y[-1], y[-1]], color=color, linewidth=2)

        # Annotate all horizontal lines (step values) without a frame
        for i in range(len(x)):
            mid_x_h = (x_left[i] + x_right[i]) / 2
            plt.text(
            mid_x_h, y[i], f"{y[i]:.2f}", color=color, fontsize=10, ha='center', va='bottom'
            )

        # Annotate the highest positive delta on the diagonal line with background
        if max_delta_index != -1 and max_delta > 0:
            mid_x = (x_right[max_delta_index] + x_left[max_delta_index + 1]) / 2
            mid_y = (y[max_delta_index] + y[max_delta_index + 1]) / 2
            plt.text(
            mid_x, mid_y, f"{max_delta:.2f}", color='black', fontsize=10, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor=color, boxstyle='round,pad=0.2', alpha=0.8)
            )

        handles.append(plt.Line2D([0], [0], color=color, lw=2, label=slab_name))

    plt.xticks(step_positions, reaction_steps)
    plt.xlabel('Reaction Step')
    plt.ylabel('delta_G [eV]')
    plt.title('Step Graphs for All Slabs')
    plt.legend(handles=handles)
    plt.xlim(-step_width, len(reaction_steps) - 1 + step_width)
    plt.tight_layout()
    plt.savefig(f"{output_name}.png", dpi=300)
    plt.show()





import argparse
import json
import matplotlib.pyplot as plt

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process slab data and plot step graphs.")
    parser.add_argument("-i", "--input", required=True, help="Path to the JSON file containing slab paths.")
    parser.add_argument("-o", "--output", required=True, help="Name of the output file to save the plot.")
    args = parser.parse_args()

    # Load the JSON file containing slab paths
    slabs_json = args.input
    output_name = args.output

    all_data = {}

    try:
        with open(slabs_json, "r") as file:
            slabs_data = json.load(file)

        # Create a dictionary mapping slab_name to color
        slab_colors = {slab_name: slab_info.get("color", plt.cm.tab10(idx))
                       for idx, (slab_name, slab_info) in enumerate(slabs_data["slabs"].items())}

        # Iterate over each slab and collect its data
        for slab_name, slab_info in slabs_data["slabs"].items():
            slab_path = slab_info["path"]  # Extract the path from the JSON
            print(f"Processing {slab_name} at {slab_path}...")
            # Replace 'process_and_collect' with the actual function to process and collect data
            process_and_collect(slab_name, slab_path, all_data)

        # Plot all step graphs on a single plot
        plot_all_step_graphs(all_data, slab_colors, output_name)

    except FileNotFoundError:
        print(f"JSON file not found: {slabs_json}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file: {slabs_json}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
