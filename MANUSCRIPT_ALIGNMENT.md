# Alignment with the current JTBS manuscript

Manuscript title:

**Safety, CBT Fidelity, and Cultural Adaptation of Large Language Models in Arabic CBT-Style Mental Health Dialogue: The AR-CBT++ Benchmark**

This reviewer snapshot is synchronized with the 18-page revision supplied by the authors. Key mappings:

| Manuscript element | Repository artifact |
|---|---|
| 144 candidate responses / 432 judge-item ratings | `data/` reviewer-safe analysis tables |
| Exact open-weight model revisions | `MODEL_REVISIONS.md` |
| Table 7 explicit-risk scenario breakdown | `tables/JTBS_Table7_Explicit_Risk_Scenario_Failures.csv` |
| Table 9 critical-flag error categories | `tables/JTBS_Table9_Critical_Failure_Error_Categories.csv` |
| Table 12 composite-definition sensitivity | `tables/JTBS_Table12_Composite_Definition_Sensitivity.csv` |
| Table 13 high-disagreement examples | `tables/JTBS_Table13_High_Disagreement_Examples.csv` |
| Main numerical checks | `scripts/reproduce_jtbs_results.py` |
| Figures 1–6 | `scripts/generate_jtbs_figures.py` + `figure_sources/` |
| Pipeline correction/integrity checks | `audit/` |
| Candidate prompt/settings documentation | `docs/CANDIDATE_GENERATION_SETTINGS.md` |
| Judge-code provenance limitation | `docs/CODE_PROVENANCE_AND_LIMITATIONS.md` |

The private unblinding key is not included.
