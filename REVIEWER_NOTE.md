# Note for peer reviewers

This versioned repository corresponds to the manuscript:

**Safety, CBT Fidelity, and Cultural Adaptation of Large Language Models in Arabic CBT-Style Mental Health Dialogue: The AR-CBT++ Benchmark**

For the fastest verification:

```bash
python scripts/reproduce_jtbs_results.py
python scripts/generate_jtbs_figures.py
```

The repository intentionally excludes the private unblinding key and raw high-risk dialogue text. The numerical/categorical tables are sufficient to reproduce the principal reported analyses, including the explicit-risk scenario breakdown, critical-failure error-category counts, same-family sensitivity, and composite-definition sensitivity.

Please see `docs/CODE_PROVENANCE_AND_LIMITATIONS.md` for the documented limitation concerning complete judge-specific decoding settings.
