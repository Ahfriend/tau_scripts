
from mp_api.client import MPRester

# Replace with your Materials Project API key
API_KEY = "XxDa3pGHBrqnY7PmCKDZYWAYhVnXBzTz"

# List of Materials Project IDs to fetch
material_ids = [
    "mp-1234",
    "mp-5678",
    # Add more IDs as needed
]

# Directory to save CIF files
output_dir = "structures"
import os
os.makedirs(output_dir, exist_ok=True)

with MPRester(API_KEY) as mpr:
    for mp_id in material_ids:
        try:
            # Fetch structure object
            structure = mpr.get_structure_by_material_id(mp_id)
            # Save as CIF
            cif_path = os.path.join(output_dir, f"{mp_id}.cif")
            structure.to(fmt="cif", filename=cif_path)
            print(f"Saved {mp_id} to {cif_path}")
        except Exception as e:
            print(f"Failed to fetch {mp_id}: {e}")
