# Code provenance and reproducibility limitations

This repository contains a retained unified Kaggle notebook for the three open-weight automated judges, plus reviewer-safe analysis scripts that recompute the numerical results from the frozen analysis-ready tables.

Important distinction: the current manuscript explicitly states that a **complete judge-specific decoding configuration is not fully documented** in the peer-review materials. Inclusion of the retained notebook does not override that limitation. Values visible in the notebook should not be interpreted as independently proven historical settings for every judge unless they are also supported by the preserved run metadata.

What is strongly supported by retained provenance:

- exact judge repositories and pinned revisions;
- common frozen input identity / hashes;
- common judge instructions/rubric/item schema;
- judge-specific randomized evaluation orders;
- raw and parsed output provenance;
- Qwen3 raw-output parser recovery;
- corrected metadata audit without score editing;
- analysis-ready 144-item and 432-rating tables used by the scripts here.

The public repository intentionally excludes the private unblinding key and raw high-risk dialogue text.

## Tie-sensitive Model × Prompt interaction

The manuscript's composite interaction diagnostic (χ²≈3.08, p≈0.214) is checked against the frozen primary blocked-factor analysis table. The public item-consensus CSV stores rounded consensus values; recomputing a Friedman interaction directly from those rounded values can alter tie correction slightly. The repository therefore does not present a numerically different rounded-table recalculation as if it were the original statistic.
