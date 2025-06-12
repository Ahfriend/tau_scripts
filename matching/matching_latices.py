
#latice reduction algorithm
import numpy as np

def lattice_reduction(a,b):
    while True:
        # Step 1
        if np.dot(a, b) < 0:
            b = -b
        # Step 2
        #print ('step 2 - norm a > norm b:')
        if np.linalg.norm(a) > np.linalg.norm(b):           
            a, b = b, a
            continue
    
        # Step 3
        if np.linalg.norm(b) > np.linalg.norm(b + a):
            #print ('    True')
            b = b + a      
            continue
        #else:
            print ('    False')

        # Step 4
        if np.linalg.norm(b) > np.linalg.norm(b - a):
           
            b = b - a
       
            continue
        break
    return a, b


#find r1 and r2 for the ratio of the areas of the two structures
def find_ratio(a1_rdc, b1_rdc, a2_rdc, b2_rdc, Amax=400):

    # input: reduced lattice vectors of two structures
    
    # compute the area of the parallelogram
    A1 = np.linalg.norm(np.cross(a1_rdc, b1_rdc))
    A2 = np.linalg.norm(np.cross(a2_rdc, b2_rdc))

  
    # calculate the ratio
    ratio = A2 / A1
    print(f"Ratio: {ratio}")  

    # precision parameter
    precision = 0.4

    # find the nearest integer to the ratio
    nearest_int = round(ratio)

    # set r1 and r2 based on the nearest integer
    r1 = nearest_int
    r2 = 1

    # if the nearest integer is 0, set r1 to 1 and r2 to the inverse of the ratio
    if nearest_int == 0:
        r1 = 1
        r2 = round(1 / ratio)

    # adjust r1 and r2 until the difference between r1/r2 and A2/A1 is less than the precision
    r_values = []
    while r1*A1 < Amax and r2*A2 < Amax:
        if (r1/r2) < ratio:
            r1 += 1
        else:
            r2 += 1
        
        if abs((r1/r2) - ratio) < precision:
            
            #print(f"r1: {r1}, r2: {r2}, r1*A1: {r1*A1}, r2*A2: {r2*A2}, precision: {(r1/r2) - ratio}")
            r_values.append((r1, r2))

    return r_values    


def upper_HNF(n):
    HNFs = []
    for m in range(1, n+1):
        if n%m == 0:
            i = int(n / m)
            for j in range(m): # m make matricies like table 3 and i like the text
                HNF = np.array([[i, j],
                                [0, m]])# chech
                HNFs.append(HNF)
             
    return HNFs


def make_supercells(a,b,n):
    supercells = []
    A = np.array([a,b])
    HNFs = upper_HNF(n)
    for HNF in HNFs:
        a_new, b_new = np.dot(HNF,A)
        reduced_supper_cell = lattice_reduction(a_new,b_new)
        supercells.append([[a_new, b_new],HNF,reduced_supper_cell])

    return supercells


# plot the supercells on a the lattice of the unit cell.

import matplotlib.pyplot as plt
import numpy as np

# plot the lattice points
def plot_lattice(ax,i_min=-5,i_max=5,j_min=-5, j_max=5,color='gray'):
    print ('plot lattice points')
    for i in range(i_min,i_max):
        for j in range(j_min,j_max,1):
            ax.plot(i*a[0]+j*b[0], i*a[1]+j*b[1], 'o',color=color, markersize=2)

    return ax

#ploth a unit cell
def plot_cell(a,b,ax,color,d=0,l=0):
    ax.quiver(0+l, 0+d, a[0], a[1], angles='xy', scale_units='xy', scale=1, color=color,headlength=0, headaxislength=0)
    ax.quiver(0+l, 0+d, b[0], b[1], angles='xy', scale_units='xy', scale=1, color=color,headlength=0, headaxislength=0)
    ax.quiver(a[0]+l, a[1]+d, b[0], b[1], angles='xy', scale_units='xy', scale=1, color=color,headlength=0, headaxislength=0)
    ax.quiver(b[0]+l, b[1]+d, a[0], a[1], angles='xy', scale_units='xy', scale=1, color=color,headlength=0, headaxislength=0)

    return ax


def plot_supercells(a, b, n,d=0,l=0,i_min=5,i_max=5,j_min=5,j_max=5):
    fig, ax = plt.subplots()
    ax = plot_lattice(ax,i_min,i_max,j_min,j_max)

    supercells = make_supercells(a,b,n)
   

    index = 1 
    for i,supercell in enumerate(supercells):
        
        cell_vectors,HNF,reduced_cell = supercell
   
        d_from_zero = index*d
        l = l
    
        ax = plot_cell(cell_vectors[0], cell_vectors[1], ax, 'b', d=d_from_zero, l=0)
        ax = plot_cell(reduced_cell[0], reduced_cell[1], ax, 'm', d=d_from_zero, l=l)
        ax.annotate(f"{HNF}", (0, d_from_zero), color='r')

        # reduce cell a normal,b normal, cos angle, angle
        a = reduced_cell[0]
        b = reduced_cell[1]
        norm_a = round(np.linalg.norm(a),2)
        norm_b = round(np.linalg.norm(b),2)
        cos_angle = round(np.dot(a, b)/(norm_a*norm_b),2)
        angle = np.arccos(cos_angle)
        angle = round(np.degrees(angle),2)
        print (f"norm_a:{norm_a}, norm_b: {norm_b}, cos_angle:{cos_angle}, angle: {angle} /n")

        index = index + 1


    ax.axis('equal')       
    return ax


import pandas as pd
import time
def find_matching_cells(a1,b1,a2,b2,Amax,cat_S,cat_a,cat_b,cat_angle):
        start_time = time.time()
        a1_rdc,b1_rdc = lattice_reduction(a1,b1)
        a2_rdc,b2_rdc = lattice_reduction(a2,b2)
     
        # find the possible ratios that satisfy r1*A2 = r2*A1 
        r_values = find_ratio(a1_rdc, b1_rdc, a2_rdc, b2_rdc, Amax)

        # create supercells for the possible ratios

        columns = ['r1','r2','s1','s2','delta_s','a1_norm','b1_norm','angle1','a2_norm','b2_norm','angle2','delta_a','delta_b','delta_angle']

        vectors = {}

        df = pd.DataFrame(columns=columns)
        for r1, r2 in r_values:
                    
                # create supercells for the possible ratios
                supercells1 = make_supercells(a1_rdc, b1_rdc, r1)
                
                # keep only unique reduced supercells
                supercells1 = list(set([tuple(map(tuple, supercell[2])) for supercell in supercells1]))
           
                supercells2 = make_supercells(a2_rdc, b2_rdc, r2)
               
                # keep only unique reduced supercells
                supercells2 = list(set([tuple(map(tuple, supercell[2])) for supercell in supercells2]))
              
                supercells1_parm = []
                for i, supercell in enumerate(supercells1):
                        #calculate the area of the parallelogram
                        #print (f"a_new:{a_new}, b_new:{b_new}")
                        a_new = supercell[0]
                        b_new = supercell[1]

                        s = np.linalg.norm(np.cross(a_new, b_new))
                          
                        #calcualte the new lattice vectors norm
                        a_new_norm = np.linalg.norm(a_new)
                        b_new_norm = np.linalg.norm(b_new)

                        #calculate the angle between the new lattice vectors
                        angle = np.arccos(np.dot(a_new,b_new)/(a_new_norm*b_new_norm))
                        angle = np.degrees(angle)
                        supercells1_parm.append([s,a_new,b_new, a_new_norm, b_new_norm, angle])
                     
                supercells2_parm = []    
                for i, supercell in enumerate(supercells2):
                        #calculate the area of the parallelogram
                        a_new = supercell[0]
                        b_new = supercell[1]
                        s = np.linalg.norm(np.cross(a_new, b_new))

                        #calcualte the new lattice vectors norm
                        a_new_norm = np.linalg.norm(a_new)
                        b_new_norm = np.linalg.norm(b_new)

                        #calculate the angle between the new lattice vectors
                        angle = np.arccos(np.dot(a_new,b_new)/(a_new_norm*b_new_norm))
                        angle = np.degrees(angle)
                
                        supercells2_parm.append([s, a_new, b_new, a_new_norm, b_new_norm, angle])
  
                # insert all data into the DataFrame and add errors 
                for i, (s1, a1, b1, a1_norm, b1_norm, angle1) in enumerate(supercells1_parm):
                        for j, (s2, a2, b2, a2_norm, b2_norm, angle2) in enumerate(supercells2_parm):
                                delta_s = (s2 - s1)/s2 * 100 
                                delta_a = (a2_norm - a1_norm)/a2_norm * 100
                                delta_b = (b2_norm - b1_norm)/b2_norm * 100
                                delta_angle = (angle2 - angle1)/angle2 * 100


        # Append each row of data to the DataFrame
                                new_row = pd.DataFrame({
                                        'r1': [r1], 
                                        'r2': [r2],
                                        's1': [s1],
                                        's2': [s2],
                                        'delta_s': [delta_s], 
                                        'a1_norm': [a1_norm], 
                                        'b1_norm': [b1_norm],
                                        'angle1': [angle1],
                                        'a2_norm': [a2_norm],
                                        'b2_norm': [b2_norm], 
                                        'angle2': [angle2],
                                        'delta_a': [delta_a],
                                        'delta_b': [delta_b],
                                        'delta_angle': [delta_angle]
                                }, columns=columns)
                                df = pd.concat([df, new_row], ignore_index=True)
                                
                                # make a dictioanry for the vectors
                                last_index = df.index[-1]
                                  
                                vectors[last_index] = {'cell1':np.array([a1,b1]), 'cell2': np.array([a2,b2])}

        df = df.drop_duplicates()

        # filter the DataFrame based on the error categorie      
        filtered_df = df[ (df['delta_s'] < cat_S)\
                & (df['delta_a'] < cat_a)\
                & (df['delta_b'] < cat_b)\
                & (df['delta_angle'] < cat_angle)]
        
        # keep only unique lines of filtered_df 

        # Assuming 'filtered_df' is your DataFrame
        # Use .loc to ensure you're working on the original DataFrame
        filtered_df.loc[:, filtered_df.columns[2:]] = filtered_df.iloc[:, 2:].round(2)

    
        filtered_df = filtered_df.drop_duplicates()
       
        
        print(filtered_df.to_string())

      
        # Select columns by their position (3rd column onwards) and round them
        
      
    
        return filtered_df, vectors
    

def find_epitaxial_direction(super_cell_vectors, basis_cell_vectores):
    U = np.array(super_cell_vectors)
    A = np.array(basis_cell_vectores)
    M = np.dot(U, np.linalg.inv(A))
    return M


def find_epitaxial_directions(filtered_df, super_cell_vectors, basis_cell_vectors1, basis_cell_vectors2):
    for i,line in enumerate(filtered_df.iterrows()):
            print (f"\nsupercell:{line[0]}")
            super_cell_vectors_1 = super_cell_vectors[line[0]]['cell1']
            super_cell_vectors_2 = super_cell_vectors[line[0]]['cell2']
            
            M1 = find_epitaxial_direction(super_cell_vectors_1, basis_cell_vectors1)
            M2 = find_epitaxial_direction(super_cell_vectors_2, basis_cell_vectors2)

            print(f"Matrix M1:\n {M1}")
            print(f"Matrix M2:\n {M2}")

def modify_poscar(file_path, layers_fixed):
    print ("modifying POSCAR file: ")
    # Read the POSCAR file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Check if Selective dynamics is already there
    if 'Selective dynamics' not in lines[7]:
        # Add 'Selective dynamics' after the line specifying direct/Cartesian coordinates
        lines.insert(7, 'Selective dynamics\n')
    
    # Extract z-coordinates and identify unique layers
    z_coords = [float(line.split()[2]) for line in lines[9:]]  # Assuming positions start at line 10

    unique_layers = sorted(set(z_coords), reverse=True)  # Sort layers from top to bottom

    # Determine the cutoff layer for 'F F F' based on user input
    cutoff_layer_z = unique_layers[-layers_fixed-1] if layers_fixed <= len(unique_layers) else unique_layers[0]

    # Modify atom positions with selective dynamics flags
    for i, line in enumerate(lines[9:], start=9):
        parts = line.split()
        z_coord = float(parts[2])
     
        flag = 'T T T' if z_coord >= cutoff_layer_z else 'F F F'
        
        # Reconstruct the line without the atomic species
        new_line = f"{parts[0]} {parts[1]} {parts[2]} {flag}\n"
        lines[i] = new_line
        
    # Write the modified POSCAR back to a new file
    file_name = file_path.split('/')[-1]
    print (file_name)
    path = '/'.join(file_path.split('/')[:-1]) + '/'
    base_name = file_name.split('.')[0]
    print (f"Writing modified POSCAR to {path}{base_name}_modified.vasp")
    with open(f"{path}{base_name}_modified.vasp", 'w') as file:
        file.writelines(lines)

    return     


import numpy as np
import pymatgen as mg
from pymatgen.io.vasp import Poscar

def combine_structures(path,POSCAR_host, POSCAR_guest, da=0,db=0,dc=2):
    # Read the host POSCAR files
    host_poscar = Poscar.from_file(POSCAR_host)
    host_structure = host_poscar.structure
    host_cell = host_structure.lattice.matrix
    print (f"host cell: {host_cell}")   

    # Read the guest POSCAR files
    guest_poscar = Poscar.from_file(POSCAR_guest)
    print (f"guest cell: {guest_poscar}")
    guest_structure = guest_poscar.structure

    # Find the highest z-value in the host structure
    max_z_host_cart = -float('inf')  # Start with negative infinity to ensure any z-value is higher
    for site in host_structure:
        if site.z > max_z_host_cart:
            max_z_host_cart = site.z

    print("Highest z-value in the host structure:", max_z_host_cart)


    # Calculate the total distance to add in Cartesian coordinates
    total_distance_to_add = max_z_host_cart + dc
    print("Total distance to add:", total_distance_to_add)

    # normalize host's a and b vectors
    a = host_structure.lattice.matrix[0]
    b = host_structure.lattice.matrix[1]
    a_norm = np.linalg.norm(a)
    b_norm = np.linalg.norm(b)
    a_normalized = a / a_norm
    b_normalized = b / b_norm
    
    print (f"a_normalized: {a_normalized}, b_normalized: {b_normalized}")

    delta_a = da*a_normalized
    delta_b = db*b_normalized

    print (f"delta_a: {delta_a}, delta_b: {delta_b}")

    #franslate d1 and d2 to fractional coordinates
    #d_frac = host_structure.lattice.get_fractional_coords([d1, d2, 0])

    # Add atoms from the guest structure to the host structure with adjusted z-values in Cartesian coordinates
    for site in guest_structure:
        # Convert site's fractional coordinates to Cartesian
        site_cart_coords = site.coords
        print(f"\nsit_cart_coords: {site_cart_coords}")

        # Shift the guest atom in the z-direction by the total distance to add
        shifted_z = site_cart_coords[2] + total_distance_to_add
        print(f"shifted_z: {shifted_z}")

        # adjust shifted guest cartezian z-coordinate to fractional coordinates of the host
        site_z_frac = host_structure.lattice.get_fractional_coords([site_cart_coords[0], site_cart_coords[1], shifted_z ])[2] 
        print(f"site_z_frac: {site_z_frac}")

        # Convert the site's Cartesian coordinates to fractional of the guest coordinates for x and y
        site_frac_coords = guest_structure.lattice.get_fractional_coords(site.coords)
        print(f"site_frac_coords: {site_frac_coords}")
       
        # Adjust the z-coordinate
        adjusted_frac_coords = np.array([site_frac_coords[0]+da,site_frac_coords[1]+db, site_z_frac ])
       
        print(f"adjusted_frac_coords: {adjusted_frac_coords}")
        
        # change coordinates from fractional to cartesian
        adjusted_cart_coords = host_structure.lattice.get_cartesian_coords(adjusted_frac_coords)

        # add to the adjusted_cart_coords the delta_a and delta_b
        adjusted_cart_coords = adjusted_cart_coords + delta_a + delta_b
        print(f"adjusted_cart_coords: {adjusted_cart_coords}")
        
        # Append the atom with the adjusted coordinates to the host structure
        host_structure.append(site.species_string, adjusted_frac_coords, coords_are_cartesian=False)

    # Write the combined structure back to a new POSCAR file
    da_text = str(da).split('.')[-1]
    db_text = str(db).split('.')[-1]

    out_file = path+f'POSCAR_combined_da{da_text}_db{db_text}_dz{dc}.vasp'
    Poscar(host_structure).write_file(out_file)
    modify_poscar(out_file, layers_fixed=2)    

    return host_structure

