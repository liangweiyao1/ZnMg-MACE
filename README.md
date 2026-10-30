# ZnMg-MACE

Fine-tuned Zn–Mg machine learning interatomic potential accompanying:

> **Mg segregation and plasticity mechanisms at Zn twin boundaries: Molecular dynamics simulations with a fine-tuned machine learning interatomic potential**

This repository provides the **1,000,000-optimizer-step, non-EMA checkpoint**, fine-tuned from **MACE-OMAT-0 medium** using original DFT labels. It supports energy, force and stress calculations through the ASE `MACECalculator`. The model file is the unmodified native MACE/PyTorch checkpoint, not a LAMMPS-compiled model.

## Download and verify

```bash
git clone https://github.com/liangweiyao1/ZnMg-MACE.git
cd ZnMg-MACE
shasum -a 256 -c SHA256SUMS.txt
```

Alternatively, download this repository through **Code → Download ZIP**. The weight file is 6,242,212 bytes (about 6.24 MB); no Git LFS client is needed.

## Quick start

Use Python 3.12 in a virtual environment. Install a PyTorch build appropriate for your CPU or CUDA system, then:

```bash
python -m pip install -r requirements.txt
python example_ase.py --device cpu
python example_ase.py --device cuda --structure POSCAR --output prediction.json
```

With no structure argument, the example builds a two-atom hcp Zn cell at the recorded model equilibrium lattice parameters. It verifies the model checksum before loading and evaluates energy, forces and stress in float64. This small example checks inference, not MD stability. `smoke_test.json` and `environment-tested.txt` record the release-time CPU check and its environment.

The example enables legacy PyTorch loading for this checksum-verified native checkpoint. Use only trusted checkpoint files.

Minimal use in an existing compatible environment, after verifying the checksum:

```python
import os
os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"  # trusted native checkpoint only
from ase.build import bulk
from mace.calculators import MACECalculator

atoms = bulk("Zn", "hcp", a=2.6466712946968562, c=5.0547879578082515)
atoms.calc = MACECalculator(
    model_paths="ZnMg_MACE_1000000steps.model",
    device="cpu",  # use "cuda" for an NVIDIA GPU
    default_dtype="float64",
)
print(atoms.get_potential_energy())  # eV, total energy
print(atoms.get_forces())           # eV/angstrom
print(atoms.get_stress())           # eV/angstrom^3; ASE Voigt order
```

## Model and reported accuracy

| Item | Value |
|---|---|
| Intended chemical system | Zn–Mg |
| Starting model | MACE-OMAT-0 medium |
| Checkpoint | 1,000,000 optimizer updates; raw weights, not EMA |
| Training / validation / historical test frames | 1,701 / 113 / 145 |
| Evaluation precision | float64 |
| Energy / length / force units | eV / angstrom / eV per angstrom |

| Split | Energy RMSE (meV/atom) | Force RMSE (eV/angstrom) | Stress RMSE (GPa) |
|---|---:|---:|---:|
| Validation (113 frames) | 0.960157 | 0.008996 | 0.056817 |
| Historical test (145 frames) | 1.006306 | 0.009209 | 0.071266 |

These are the recorded checkpoint evaluations, not new measurements from the quick-start example. The historical test set was used during development and is not a new blind test. Many property-reference structures participated in training; those comparisons are fitting diagnostics. See [MODEL_CARD.md](MODEL_CARD.md) and the [complete original numerical report](evaluation_report.zh.md).

## Files

| File | Purpose |
|---|---|
| `ZnMg_MACE_1000000steps.model` | Native fine-tuned weights |
| `SHA256SUMS.txt`, `MODEL_INFO.json` | Checkpoint identity and machine-readable metadata |
| `example_ase.py`, `requirements.txt` | Minimal ASE inference example and direct dependencies |
| `smoke_test.json`, `environment-tested.txt` | Recorded release-time inference check |
| `MODEL_CARD.md`, `evaluation_report.zh.md` | Scope, evaluation conventions and known limitations |
| `CITATION.md` | Associated manuscript and upstream attribution |
| `NOTICE.md`, `LICENSE-ASL.md` | Model provenance and upstream license |

## Scope and data availability

This release distributes model weights and an inference example. It does not include the DFT training dataset, the complete training workflow, or all MD input decks and trajectories underlying the manuscript. It is therefore sufficient for model inference, but is not a complete reproduction archive for every paper result. LAMMPS use requires an export compatible with the selected LAMMPS/MACE interface and validation against native ASE inference.

## Citation and license

Please acknowledge the associated manuscript above and the MACE/foundation-model sources listed in [CITATION.md](CITATION.md). Author list, journal and DOI will be added when confirmed; no publication identifier is assigned by this repository.

The fine-tuned weights retain the **Academic Software License (ASL)** of MACE-OMAT-0, for academic non-commercial use. Read [NOTICE.md](NOTICE.md) and [LICENSE-ASL.md](LICENSE-ASL.md). The MIT license of the MACE software should not be confused with the license of the OMAT model weights.

Questions and reproducibility reports can be raised through the repository's Issues page. Include the checkpoint hash, software versions, input structure and exact command.
