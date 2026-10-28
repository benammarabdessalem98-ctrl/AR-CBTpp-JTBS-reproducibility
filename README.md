# AR-CBT++ — JTBS Reviewer Reproducibility Snapshot

Companion code and reviewer-safe numerical artifacts for the manuscript:

**Safety, CBT Fidelity, and Cultural Adaptation of Large Language Models in Arabic CBT-Style Mental Health Dialogue: The AR-CBT++ Benchmark**

Authors: Abdessalem Ben Ammar, Ridha Zaghdoud, Tarek M. Hamdani, Habib Chabchoub, Adel M. Alimi.

## Scope

This repository is synchronized with the current 18-page JTBS revision. It is designed to let reviewers verify the main numerical claims and regenerate the manuscript figures without publishing the private unblinding key or raw high-risk dialogue text.

### Included

- reviewer-safe 144-item consensus and 432-rating analysis tables;
- exact open-weight candidate/judge revision identifiers;
- retained unified Kaggle three-judge notebook;
- numerical reproduction script for the current manuscript;
- programmatic figure-generation script for Figs. 1–6;
- publication-aligned Tables 7, 9, 12, and 13;
- post-correction audit/provenance records;
- documented candidate prompts and open-weight generation settings.

### Intentionally excluded

- private unblinding key;
- raw candidate-response text and detailed high-risk dialogue text;
- authentication tokens/API keys;
- the separate planned human-validation forms, because the current manuscript explicitly reports that no clinician or dialect-native human validation was conducted in this pilot.

## Reproduce the current manuscript results

```bash
pip install -r requirements.txt
python scripts/reproduce_jtbs_results.py
```

The numerical check is written to:

`verification/JTBS_main_results_check.csv`

## Regenerate manuscript figures

```bash
python scripts/generate_jtbs_figures.py
```

The script generates `figures/Fig1_workflow.png` through `figures/Fig6_variety_core_profiles.png` and writes the corresponding source tables to `figure_sources/`.

## Important reproducibility limitation

The manuscript reports a documentation gap for the complete judge-specific decoding configuration. The retained notebook is provided for transparency and inspection, but its presence should not be interpreted as proving every historical judge runtime parameter unless independently supported by run metadata. See `docs/CODE_PROVENANCE_AND_LIMITATIONS.md`.

## GPT-5.6 limitation

GPT-5.6 is the ChatGPT product-interface label observed during data collection. No immutable backend revision or decoding controls were exposed, and fresh-chat isolation is unverified. Those 48 outputs are treated as observed artifacts rather than bit-for-bit reproducible generations.

## Public-release boundary

This snapshot intentionally favors reviewer verification while minimizing unnecessary publication of high-risk text. Reviewer-safe numeric/categorical tables are public; sensitive raw text and the private key remain outside the repository.

See `MANUSCRIPT_ALIGNMENT.md` for a direct manuscript-to-file map.
