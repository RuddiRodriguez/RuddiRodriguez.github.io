# Ruddi Garcia — Portfolio

GitHub Pages portfolio with six linked blog articles about different parts of Tabular Classifier Flow.

- `index.html`: portfolio homepage and article links.
- `data-preparation.html`: data loading, splitting, preprocessing, and synthetic campaign histories.
- `workflow.html`: model comparison, refinement, Optuna tuning, persistence, and dashboard reporting.
- `validation.html`: scoring, cutoffs, top-ranked selections, reporting, and saved charts.
- `methodology.html`: complete procedure based on README, METHODOLOGY_AND_OPTIONS.md, and PREPROCESSING_TECHNIQUES.md; includes default versus alternate preprocessing, run order, settings, artifacts, and code excerpts from the alternate training path.
- `banking-project.html`: anonymous account of the original banking campaign-response problem, model development, and batch production scoring setup.
- `sql-feature-engineering.html`: renamed SQL/Python illustrations preserving joins, history windows, date-relative features, labels, and handoff boundaries.
- `style.css`: shared responsive layout and readable code examples.

Each article explains the problem, implemented approach, selected source functions, design limits, and demonstrated work. Code excerpts are selected functions rather than standalone scripts. The complete source repository remains private. No raw customer records, credentials, or serialized models are included.

Edit the HTML files to update articles. GitHub Pages publishes the root of `main`. Bump the stylesheet query version when changing CSS so returning visitors load the new styles.

## Evidence

Articles were checked against the source files in `tabular_classifier_flow/` in `RuddiRodriguez/Response_model_t`. Excerpts include source filenames, function names, and line ranges from the reviewed snapshot.

Three original aggregate charts were copied from `Model/validation_plots/` at source commit `069779c5e317ca24ac64e9219df5d56214346196`:

- `test_confusion_matrix.png`: TN 56,798; FP 66; FN 11; TP 87.
- `test_precision_recall_curve.png`: displayed average precision 0.74 (rounded).
- `test_roc_curve.png`: displayed AUC 0.98 (rounded).

Recall is calculated as 87 / 98; precision as 87 / 153. The original run's dataset and cutoff were not independently reproduced. Current configuration refers to credit-card fraud data; it does not prove the saved plots' dataset provenance. The source validator can select a cutoff from supplied evaluation labels, so saved label-based metrics are not presented as an independent final benchmark.

## Verification

Local checks covered section anchors, file links, source-derived code excerpts, and article layouts at narrow and desktop widths. The portfolio describes implemented code; no model training or dashboard deployment was performed for these articles.

## Banking context and anonymity

The user identified the original work as a real banking project and its deployment folder as production code. The articles describe the archived batch implementation, not a fresh live-system verification. Bank-specific names, internal infrastructure, source-table names, private categories and identifiers are omitted or replaced with generic names. The SQL examples are abbreviated explanatory adaptations, not executable production extracts. Historical window placement, joining keys, feature timing and limitations are described explicitly. Previously published bank-derived identifiers in examples have also been anonymised. Later saved classifier charts are not described as banking campaign results.
