import os
from ase.io import read, write
from ase.visualize.plot import plot_atoms
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def vasprun_to_xyz_and_gif(vasprun_path, output_xyz, output_gif):
    """
    Reads a vasprun.xml file, extracts all ionic steps, saves them as an .xyz file,
    and creates an animated .gif of the optimization process.

    Parameters:
        vasprun_path (str): Path to the vasprun.xml file.
        output_xyz (str): Path to save the .xyz file.
        output_gif (str): Path to save the .gif file.
    """
    try:
        # Read all ionic steps from vasprun.xml
        structures = read(vasprun_path, index=":")  # ":" reads all steps
        print(f"Loaded {len(structures)} ionic steps from {vasprun_path}")

        # Save all structures to an .xyz file
        write(output_xyz, structures, format="extxyz")
        print(f"XYZ file saved to {output_xyz}")

        # Create a GIF animation
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.axis("off")  # Turn off axes

        def update(frame):
            ax.clear()
            ax.axis("off")
            plot_atoms(structures[frame], ax=ax, radii=0.5, rotation=("90x,0y,0z"))

        ani = FuncAnimation(fig, update, frames=len(structures), interval=200)  # 200ms per frame
        ani.save(output_gif, writer="pillow")
        print(f"GIF animation saved to {output_gif}")

    except FileNotFoundError:
        print(f"File not found: {vasprun_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    vasprun_path = "vasprun.xml"  # Replace with the path to your vasprun.xml
    output_xyz = "ionic_steps.xyz"  # Replace with the desired .xyz file name
    output_gif = "optimization.gif"  # Replace with the desired .gif file name

    vasprun_to_xyz_and_gif(vasprun_path, output_xyz, output_gif)
