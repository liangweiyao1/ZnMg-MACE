# Model card: ZnMg-MACE, 1,000,000 steps

## Identity and provenance

The checkpoint is `ZnMg_MACE_1000000steps.model`, SHA256 `aeec2e2b1eadd28997d89621ece1f10bdd3d38f14c3fe9194a60438ee8aa2d7a`. It contains raw weights after 1,000,000 optimizer updates, not EMA weights. An optimizer step is not an epoch. The original local checkpoint was frozen on 2026-10-25 and copied without changes for this repository on 2026-10-30.

The starting checkpoint was official MACE-OMAT-0 medium. The recorded preparation converted the official checkpoint to float32 without optimization; its tensors were checked against the official weights after casting. Fine-tuning then used original DFT energy, force and stress labels. No teacher-generated labels were reported in the release metadata. See MODEL_INFO.json for foundation and final-model hashes.

## Intended use

Research on Zn and Mg-containing Zn structures, including Mg segregation at Zn twin boundaries and related plasticity simulations. The intended system is Zn–Mg; inherited support for other elements is not evidence of validation for them. Validate the configurations, temperatures, strain rates, concentrations and deployment precision relevant to a new application.

## Units and reference conventions

Energies are in eV and follow the original DFT TOTEN convention. They are not cohesive energies referenced to isolated atoms. Forces are eV/angstrom. ASE returns stress in eV/angstrom^3 and Voigt order xx, yy, zz, yz, xz, xy; the evaluation table reports stress errors in GPa. Model equilibrium lattice parameters and calculations at fixed DFT geometries are distinct protocols.

The Zn model equilibrium lattice is a = 2.6466713 angstrom and c = 5.0547880 angstrom. The Mg model equilibrium lattice is a = 3.1898898 angstrom and c = 5.1831358 angstrom. Elastic comparisons in the original report use matched DFT strained geometries with fixed internal positions; separately listed relaxed-ion model constants have no matching DFT reference in that report.

## Evaluation interpretation

The dataset contains 1,701 training, 113 validation and 145 historical test frames. Historical test RMSEs are 1.006306 meV/atom for energy, 0.009209 eV/angstrom for force and 0.071266 GPa for stress. These are checkpoint-recorded values. The test set was used during development; it is not a newly held-out blind benchmark. Many property structures were included in training.

## Known limitations in the checkpoint report

- The S-type interstitial initial structure has a formation energy of 1.54774 eV at the DFT geometry and 1.28062 eV after model relaxation. The final defect topology needs checking; agreement at the initial geometry does not establish defect stability.
- The T2 stacking-fault energy is 94.80776 mJ/m^2 versus the DFT reference 86.78465 mJ/m^2.
- Mg segregation at the prismatic (10-10) surface site differs from its DFT reference by 0.07059 eV. That surface was excluded from training. Basal subsurface segregation differs by -0.02772 eV.
- Some Mg-decorated twin and stacking-fault DFT references were not force-converged. Their segregation comparisons describe energy differences between those specific geometries.
- The original checkpoint report did not establish isolated-atom cohesive energies, vacancy migration barriers or melting temperature. Later application calculations are not reproduced in this release.

A successful small-cell inference check does not establish large-system long-time MD stability or physical accuracy for every defect. The numerical property table and its original Chinese protocol notes are preserved in evaluation_report.zh.md.

## Reproducibility boundary

This is a native model release with an ASE inference example. Training data, full optimization history and production trajectories are not bundled. A deployment to LAMMPS or another accelerated backend should be compared against native energy, forces and stress before running production trajectories.
