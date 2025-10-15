<!-- <h1 align="center">PACE (Precise and Accurate Configuration Evaluation)</h1>

<h4 align="center">

</h4> -->

<p align="center">
  <img src="./logo_1.png" alt="Precise and Accurate Configuration Evaluation" width="600"/>
</p>
<br/>



![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=%23E9EAE8&color=%235C6216)
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)



The workbook contains the code and notebook to run PACE (Precise and Accurate Configuration Evaluation).


## 🚀 Environment Setup
- System requirements: This package requires a standard Linux computer with GPU (supports CUDA >= 10) and enough RAM (> 2 GB). The code has been tested on NVIDIA V100 SXM2. If you want to run the code on a GPU that does not support CUDA>=10, you need to modify the versions of PyTorch and CUDA in the [env.yml](env.yml) file.
- We'll use `conda` to install dependencies and set up the environment for a Nvidia GPU machine.
We recommend using the [Miniconda installer](https://docs.conda.io/projects/miniconda/en/latest/miniconda-other-installer-links.html).
- After installing `conda`, install [`mamba`](https://mamba.readthedocs.io/en/latest/) to the base environment. `mamba` is a faster, drop-in replacement for `conda`:
    ```bash
    conda install mamba -n base -c conda-forge
    ```
- Then create a conda environment and install the dependencies:
    ```bash
    mamba env create -f env.yml
    ```
    Activate the conda environment with `conda activate pace-env`.



## ⚙️ Installation

```sh
pip install pace
```

if PyPI installation fails or you need the latest `main` branch commits, you can install from source:

```sh
pip install git+https://github.com/dixitmudit/PACE.git
```
    
## 🧪 Getting Started

### 1. Direct Usage

```bash
  python main.py --model /path/to/your/mace/model.model --metals Fe-Ru Fe-Mo --adsorbates Li2S Li2S2 --device cuda
```

### 2. Example notebook
[![Static Badge](https://img.shields.io/badge/google_colab-open_in_colab?style=flat-square&logo=googlecolab)](https://github.com/dixitmudit/PACE/blob/main/examples/pace-results.ipynb)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://github.com/dixitmudit/PACE/blob/main/examples/pace-results.ipynb)

### 3. PACE class to screen
```bash
from pace import PACE
from 

# Setup PACE:
pace = PACE(base=base, adsorbate=adsorbate, division=5, z_levels=[1.35, 1.75])
# Handy VS Code feature: Hover over PAACE or any method/function to obtain info about arguments

# Screen conformations
results = pace.screen(calculator=mace_calc, fig_save_at='/your/path/here', mlip_optimization=3)
# if mlip_optimization > 0, it will initate mlip optimization of top `input: integer` (by_default: 20) structures.


```

## 🌈 Acknowledgements

M.D. and S.K. gratefully acknowledge the financial support provided by the CSIR, India, which facilitated the completion of this work. A.M.K.R. acknowledges the Department of Atomic Energy and UM-DAE-Centre for Excellence in Basic Sciences, 

We express our gratitude to the National Supercomputing Mission (NSM) for granting access to the computing resources of the Param Porul HPC System. This system is implemented by C-DAC and is supported by the Ministry of Electronics and Information Technology (MeitY) and the Department of Science and Technology (DST), Government of India.

This code repo is based on several existing repositories and MLIPs:
* ASE
* MACE-MP-0
* CHGNet


## 📝 Citation
If you find our work useful, please consider citing it:
 /TBU/
```bibtex


```