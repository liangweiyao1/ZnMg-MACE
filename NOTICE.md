# Provenance and license notice

The ZnMg-MACE checkpoint is a fine-tuned derivative of **MACE-OMAT-0 medium** from the MACE foundation-model authors. The official release identifies its license as the Academic Software License (ASL):

https://github.com/ACEsuit/mace-foundations/releases/tag/mace_omat_0

The fine-tuned weights are distributed under those ASL terms. The full upstream license is preserved verbatim in LICENSE-ASL.md, sourced from https://github.com/gabor1/ASL/blob/main/ASL.md on 2026-10-30. Its appendix contains upstream template placeholders and is retained as part of the original text, not as a claim about this repository's authorship.

Modification notice: the foundation weights were fine-tuned on the Zn–Mg DFT dataset; the 1,000,000-optimizer-step raw checkpoint was frozen on 2026-10-25. The checkpoint bytes were not altered during packaging on 2026-10-30. The native editable weight format is provided. Model architecture and inference implementation are supplied by the separately distributed MACE package: https://github.com/ACEsuit/mace.

ASL limits use to academic non-commercial purposes and includes redistribution obligations and a disclaimer of warranty. Commercial use requires contacting the original licensor. The MIT license of MACE software does not replace the ASL license of the OMAT weights. This notice does not assign a new permissive license to the accompanying original research documents or example script.
