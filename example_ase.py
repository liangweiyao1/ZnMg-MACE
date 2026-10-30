"""Evaluate the bundled Zn-Mg checkpoint with ASE; default: two-atom hcp Zn."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path

import numpy as np
from ase.build import bulk
from ase.io import read


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    parser.add_argument("--structure", type=Path, help="ASE-readable input, e.g. POSCAR")
    parser.add_argument("--output", type=Path, help="Optional JSON result file")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    info = json.loads((root / "MODEL_INFO.json").read_text())
    model = root / info["model"]
    digest = hashlib.sha256(model.read_bytes()).hexdigest()
    if digest != info["sha256"]:
        raise RuntimeError("Model checksum does not match MODEL_INFO.json")
    # Native MACE checkpoints contain Python objects. Load only this verified file.
    # e3nn 0.4.4 also requires legacy loading on newer PyTorch releases.
    os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"
    from mace.calculators import MACECalculator
    atoms = read(args.structure) if args.structure else bulk(
        "Zn", "hcp", a=2.6466712946968562, c=5.0547879578082515
    )
    if not set(atoms.get_chemical_symbols()).issubset({"Zn", "Mg"}):
        raise ValueError("This release is intended for Zn and Mg only")
    atoms.calc = MACECalculator(
        model_paths=str(model), device=args.device, default_dtype="float64"
    )
    energy = float(atoms.get_potential_energy())
    forces = atoms.get_forces()
    stress = atoms.get_stress()
    if not all(np.isfinite(x).all() for x in [energy, forces, stress]):
        raise RuntimeError("Non-finite model output")
    result = {
        "model_sha256": digest,
        "device": args.device,
        "dtype": "float64",
        "structure": args.structure.name if args.structure else "hcp_Zn_model_equilibrium",
        "symbols": atoms.get_chemical_symbols(),
        "positions_angstrom": atoms.positions.tolist(),
        "cell_angstrom": atoms.cell.array.tolist(),
        "pbc": atoms.pbc.tolist(),
        "energy_eV": energy,
        "energy_eV_per_atom": energy / len(atoms),
        "forces_eV_per_angstrom": forces.tolist(),
        "stress_eV_per_angstrom3_voigt_xx_yy_zz_yz_xz_xy": stress.tolist(),
        "versions": {k: importlib.metadata.version(k) for k in
                     ["mace-torch", "torch", "ase", "e3nn", "numpy"]},
    }
    encoded = json.dumps(result, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(encoded)
    print(encoded)


if __name__ == "__main__":
    main()
