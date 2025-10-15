import numpy as np
import pandas as pd
import argparse
import torch
from ase.io import read
from mace.calculators import MACECalculator

# Note: Assuming mdgroup and its contents (PACE, utilfuncs) are available in your environment.
from mdgroup.pace import PACE
from mdgroup.utilfuncs import create_directory_if_not_exists


def parse_args():
    """Parses command line arguments for the PACE screening script."""
    parser = argparse.ArgumentParser(
        description="Run Potential Adsorption Conformation Explorer (PACE) screening using MACE."
    )

    # Required: MACE model path
    parser.add_argument(
        '--model',
        type=str,
        required=True,
        help='Path to the MACE pre-trained model file (e.g., 2024-01-07-mace-128-L2_epoch-199.model).'
    )

    # Optional: List of metals (e.g., --metals Ru Mo Pt)
    parser.add_argument(
        '--metals',
        nargs='+',  # Expects one or more arguments
        default=['Ru', 'Mo', 'Pt'],
        help='Space-separated list of metals for the base slabs (e.g., --metals Ru Mo Pt). Default: Ru Mo Pt'
    )

    # Optional: List of adsorbates (e.g., --adsorbates Li2S Li2S2)
    parser.add_argument(
        '--adsorbates',
        nargs='+',
        default=['Li2S', 'Li2S2', 'Li2S4', 'Li2S6', 'Li2S8', 'S8'],
        help='Space-separated list of adsorbate molecules (e.g., --adsorbates Li2S Li2S2). Default: Li2S Li2S2 Li2S4 Li2S6 Li2S8 S8'
    )

    # Optional: Device to run on
    parser.add_argument(
        '--device',
        type=str,
        default='auto',
        choices=['cpu', 'cuda', 'auto'],
        help='Specify device for MACE calculation (cpu, cuda, or auto). Auto detects CUDA if available.'
    )

    return parser.parse_args()


def main():
    """Main function to run the PACE screening."""
    args = parse_args()

    # --- 1. Device Setup ---
    # Determine the device based on command-line argument
    if args.device == 'auto':
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    else:
        device = args.device

    print('Running on device:', device)

    # --- 2. Calculator Initialization ---
    try:
        # Use the model path from the command line argument
        mace_calc = MACECalculator(args.model, device=device)
    except FileNotFoundError:
        print(f"Fatal Error: MACE model file not found at {args.model}. Exiting.")
        return
    except Exception as e:
        print(f"Fatal Error initializing MACE calculator: {e}. Exiting.")
        return

    # --- 3. Parameter Assignment ---
    metals = args.metals
    all_adsorbates = args.adsorbates
    
    # Setup calculator list for iteration
    calculators = [mace_calc]
    calculator_names = ["mace"]

    # --- 4. Main Screening Loop ---
    # Append to the error log file instead of overwriting it each time
    with open('errors_log.txt', 'a') as log_file:
        log_file.write("\n--- Starting New Screening Run ---\n")

    for calculator, model in zip(calculators, calculator_names):
        
        for metal in metals:
            slab_filename = f'slabs/{metal}.vasp'
            
            # Read base slab
            try:
                base = read(slab_filename)
            except Exception as e:
                error_msg = f"Warning: Could not read base slab file {slab_filename}. Skipping metal {metal}. Error: {e}"
                print(error_msg)
                with open('errors_log.txt', 'a') as log_file:
                    log_file.write(error_msg + "\n")
                continue

            arch = f'{model}/Fe-{metal}'
            
            for substrate in all_adsorbates:
                try:
                    print(f"Currently processing: {metal} with {substrate}")
                    
                    adsorbate_filename = f"substrate/{substrate}"
                    adsorbate = read(adsorbate_filename, format='vasp')
                    
                    # Create output directory for the current substrate
                    create_directory_if_not_exists(substrate)
                    
                    # Setup PACE
                    pace = PACE(
                        arch=arch+"/"+substrate, 
                        base=base, 
                        adsorbate=adsorbate, 
                        division=10, 
                        z_levels=[2.5]
                    )

                    # Screen conformations
                    # The original code passed mace_calc here, which is fine since it's the only calculator.
                    results = pace.screen(
                        calculator=mace_calc, 
                        fig_save_at='figs', 
                        mlip_optimization=40, 
                        make_countours=1
                    )
                    
                except Exception as e:
                    # Log the error and continue to the next adsorbate
                    error_msg = f"Error occurred for {metal} and adsorbate {substrate}: {e}"
                    print(error_msg)
                    with open('errors_log.txt', 'a') as log_file:
                        log_file.write(error_msg + "\n")
                    continue
            
    print("\n--- Screening Complete. Check 'errors_log.txt' for any warnings/errors. ---")


if __name__ == '__main__':
    main()