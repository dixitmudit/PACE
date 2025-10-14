# %%
import numpy as np
import pandas as pd
from ase import Atoms
from ase.io import read, write
import matplotlib.pyplot as plt
import torch
from mace.calculators import MACECalculator
# from matlantis_features.ase_ext.optimize import FIRELBFGS

from mdgroup.pace import PACE
from mdgroup.utilfuncs import create_directory_if_not_exists

# MACE
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('Running on: ', device)
mace_calc = MACECalculator('/scratch/muditdixit_csir/Adithya/2024-01-07-mace-128-L2_epoch-199.model', device=device)


# Read base and define adsorbate
#changes 
metals = ["Ru", "Mo", "Pt"]
# arch = "mace/Fe-Co"

#metals = ['Ni']

all_adsorbates = ['Li2S', 'Li2S2', 'Li2S4', 'Li2S6', 'Li2S8', 'S8']
#all_adsorbates = ['Li2S2']

# Calculators
calculators = [mace_calc]
calculator_names = ["mace"]

for calculator, model in zip(calculators, calculator_names):
        
    for metal in metals:
        base = read(f'slabs/Fe-{metal}.vasp')
        arch = f'{model}/Fe-{metal}'
        for substrate in all_adsorbates:
            try:            
                print(f"Currently: ", substrate)
                adsorbate = read(f"substrate/{substrate}", format='vasp')
                create_directory_if_not_exists(substrate)
                # dir = metal + '/' + substrate
                # Setup PACE:
                pace = PACE(arch=arch+"/"+substrate, base=base, adsorbate=adsorbate, division=10, z_levels=[2.5])

                # Screen conformations
                results = pace.screen(calculator=mace_calc, fig_save_at='figs', mlip_optimization=40, make_countours=1)
            
            except Exception as e:
                with open('errors_log.txt', 'w') as file:
                    file.write(f"Error occurred for adsorbate: {substrate}: {e}")
                
                continue

