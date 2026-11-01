# ZnMg-MACE

Model and DFT dataset for **Mg segregation and plasticity mechanisms at Zn twin boundaries: Molecular dynamics simulations with a fine-tuned machine learning interatomic potential**.

The Zn–Mg potential was fine-tuned from MACE-OMAT-0 medium using DFT energies, forces and stresses. `ZnMg_MACE.model` contains the raw weights after 1,000,000 optimizer updates, without EMA averaging. The native MACE model can be used through ASE; a separate export is needed for LAMMPS.

## Files

- `ZnMg_MACE.model`: fine-tuned potential.
- `data/train.extxyz`, `data/validation.extxyz`, `data/test.extxyz`: the dataset splits used for this model.
- `example_ase.py`: energy, force and stress calculation with ASE.
- `requirements.txt`: Python dependencies.
- `LICENSE-ASL.md`: upstream model license.

## Installation and use

Use Python 3.12 and install a PyTorch build suitable for your CPU or CUDA system.

```bash
git clone https://github.com/liangweiyao1/ZnMg-MACE.git
cd ZnMg-MACE
python -m pip install -r requirements.txt
python example_ase.py --device cpu
```

The example uses a two-atom hcp Zn cell with a = 2.6466713 Å and c = 5.0547880 Å. To evaluate another structure:

```bash
python example_ase.py --device cuda --structure POSCAR --output prediction.json
```

Calculations use float64. Energy is reported in eV, forces in eV/Å, and ASE stress in eV/Å³ with Voigt order xx, yy, zz, yz, xz, xy. Energy follows the DFT TOTEN reference; it is not a cohesive energy relative to isolated atoms.

The example checks the model hash before loading. Native MACE checkpoints require legacy PyTorch object loading, which the script enables for this file. Only load checkpoints from a trusted source.

The CPU example was checked with Python 3.12.13, MACE 0.3.16, PyTorch 2.14.1, e3nn 0.4.4 and ASE 3.29.0. The hcp Zn energy was −1.10712235 eV/atom.

## Fine-tuning dataset

The dataset contains 1,959 configurations with original DFT labels, divided into 1,701 training, 113 validation and 145 test configurations. It includes bulk structures, compounds, solid solutions, defects, stacking faults, twin boundaries, surfaces, AIMD snapshots and loading/thermal configurations. The split files retain their original frame identifiers and training weights.

| Field | Meaning | Unit |
|---|---|---|
| `REF_energy` | DFT total energy of the configuration | eV |
| `REF_forces` | Cartesian force on each atom | eV/Å |
| `REF_stress` | 3 × 3 stress tensor | eV/Å³ |
| `frame_id` | Configuration identifier | — |
| `config_type` | Configuration category | — |

Read the files with ASE:

```python
from ase.io import read

frames = read("data/train.extxyz", index=":")
atoms = frames[0]
energy = atoms.info["REF_energy"]
forces = atoms.arrays["REF_forces"]
stress = atoms.info["REF_stress"]
```

For MACE training, use `energy_key=REF_energy`, `forces_key=REF_forces` and `stress_key=REF_stress`. The files preserve the existing split; they should not be randomly repartitioned when comparing with the results below. The historical test data influenced the exclusion rules during development, so the retained test set is a development benchmark rather than an untouched blind test.

## Accuracy and scope

| Split | Configurations | Energy RMSE (meV/atom) | Force RMSE (eV/Å) | Stress RMSE (GPa) |
|---|---:|---:|---:|---:|
| Validation | 113 | 0.960157 | 0.008996 | 0.056817 |
| Test | 145 | 1.006306 | 0.009209 | 0.071266 |

The intended application is Zn–Mg segregation and deformation at Zn twin boundaries. Many property-reference structures were included in training. Known deviations include the T2 stacking-fault energy (94.81 versus 86.78 mJ/m² in DFT), Mg segregation at the prismatic (10-10) surface (0.07059 eV error), and structural relaxation of the S-type interstitial. Some Mg-decorated twin and stacking-fault references were not fully force-converged. These comparisons concern the specified reference geometries; they do not establish accuracy for all defects or loading conditions.

The repository provides the model and fine-tuning data. Production MD trajectories and the complete training workflow are not included.

## File verification

SHA256 checksums:

```text
aeec2e2b1eadd28997d89621ece1f10bdd3d38f14c3fe9194a60438ee8aa2d7a  ZnMg_MACE.model
a763bc6c5f8d48bfe24e9ef854b5837ce6fb262ffff128fee7be58eb41b0cf70  data/train.extxyz
6b4e9b4ee22af9572755098dbeb1276de6db50c8c7ac6aeb8cb7f04e6710123b  data/validation.extxyz
bbec471a1428fc8e061032895c9ca0f597fad11c00e4840906ed4b9121a7c755  data/test.extxyz
```

## Citation and license

Please cite the associated manuscript named above and the relevant [MACE](https://github.com/ACEsuit/mace) and [foundation-model](https://github.com/ACEsuit/mace-foundations) publications when using this potential.

The model is a fine-tuned derivative of [MACE-OMAT-0 medium](https://github.com/ACEsuit/mace-foundations/releases/tag/mace_omat_0) and retains its Academic Software License (ASL), for academic non-commercial use. The full upstream terms are included in [LICENSE-ASL.md](LICENSE-ASL.md). The MIT license of the MACE software does not replace the license of the OMAT weights. The ASL statement here applies to the model; no separate license is assigned to the original DFT dataset.

The foundation weights were modified by Zn–Mg fine-tuning; this checkpoint was frozen on 25 October 2026. Renaming the file does not change its weights. The model architecture and inference source are available in the MACE repository linked above.
