# Ruddi Garcia — Portfolio

Personal portfolio hosted on GitHub Pages. The first project describes the response-model validation workflow without publishing private code, customer data, or unverified results.

Edit `index.html` to update content and `style.css` to adjust appearance. GitHub Pages publishes the root of the `main` branch.

## Saved report evidence

Three aggregate charts were copied from `Model/validation_plots/` in the private source project at commit `069779c5e317ca24ac64e9219df5d56214346196`:

- `test_confusion_matrix.png`: TN 56,798; FP 66; FN 11; TP 87.
- `test_precision_recall_curve.png`: displayed average precision 0.74 (rounded).
- `test_roc_curve.png`: displayed AUC 0.98 (rounded).

Recall is calculated as 87 / 98; precision as 87 / 153. The original run's dataset and cutoff were not independently reproduced. Current source configuration refers to credit-card fraud data; this does not prove the saved plots' dataset provenance. No raw records or serialized models are included.

The source validator can select a cutoff using evaluation labels when no cutoff is supplied. The portfolio therefore presents these as saved report examples, not an independently reproduced final benchmark.

## Tabular Classifier Flow portfolio entry

The second project entry summarizes `tabular_classifier_flow/README.md`: reusable configuration, CSV train/test preparation, model comparison, candidate refinement, Optuna tuning, saved pipelines, validation outputs, optional permutation importance, and the Streamlit dashboard. It does not claim a newly run model or a live dashboard. The original validation entry remains available at `#projects`.
