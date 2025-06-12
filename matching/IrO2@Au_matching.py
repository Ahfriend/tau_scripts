import numpy as np
import pandas as pd
from matching_latices import find_matching_cells
from matching_latices import find_epitaxial_directions



#IrO2 001 on Ir 111
a_IrO2_on_Ir_111 = np.array([-4.0713444969018804, -2.3505918412500000, 0.0000000000000000])
b_IrO2_on_Ir_111 = np.array([-4.0713444969018804, 7.0517755237500097, 0.0000000000000000])
c_IrO2_on_Ir_111 = np.array([0.0000000000000000, 0.0000000000000000, -31.0262293739934485])

# Au slab 111 - made from Ir primitive cell
a_Au_111 = np.array([2.8847131274475171, -0.0000000000000003,   -0.0000000000000002])
b_Au_111 = np.array([1.4423565637237588,  2.4982348510000061,   -0.0000000000000002])
c_Au_111 = np.array([0.0000000000000050,  0.0000000000000006,   56.5286017324374157])

#
a_IrO2_001 = np.array([4.49900000000000,   0.00000000000000,   0.00000000000000])
b_IrO2_001 = np.array([0.00000000000000,   4.49900000000000,   0.00000000000000])
c_IrO2_001 = np.array([0.00000000000000,   0.00000000000000,  23.59500000000000])

# Ir slab 111 - made from Ir primitive cell
a_Ir_111 = np.array([2.7142296646012540, 0.0000000000000000, -0.0000000000000000])
b_Ir_111 = np.array([1.3571148323006268, 2.3505918412500026, -0.0000000000000000])
c_Ir_111 = np.array([ 0.0000000000000029, 0.0000000000000004, 33.2423886149929899])




cell_1 = "Au(111) slab z-direction"
a1 = a_Au_111
b1 = b_Au_111   

cell_2 = "IrO2(001) on Ir(111)"
a2 = a_IrO2_001
b2 = b_IrO2_001

cat_S = 20
cat_a =10
cat_b = 10
cat_angle = 10
Amax = 200
filtered_df,vectors_Au_111_Au2O3_111 = find_matching_cells(a1,b1,a2,b2,Amax,cat_S,cat_a,cat_b,cat_angle)

basis_cell_vectors1 = np.array([a_Au_111, b_Au_111, c_Au_111])
basis_cell_vectors2 = np.array([a_IrO2_on_Ir_111, b_IrO2_on_Ir_111, c_IrO2_on_Ir_111])
vectors = vectors_Au_111_Au2O3_111
find_epitaxial_directions(filtered_df, vectors, basis_cell_vectors1, basis_cell_vectors2) 
