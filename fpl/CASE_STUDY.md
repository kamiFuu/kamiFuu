# FPL — research software, data engineering and interpretable ML

## Research and publication

FPL (FocusPoint Learning) supports collaborative research into attention in foreign-language classrooms. Thanh (Cầm Duy Thành, Tin) develops the project software and data pipeline and is a co-author of [The impact of well-being on university students’ attention in foreign language classrooms in Japan](https://doi.org/10.1016/j.socimp.2026.100195), Societal Impacts, 2026.

The published study collected data from four French classes in Japan (107 students), using real-time self-report clickers, synchronized classroom observations, end-of-class surveys and follow-up interviews. Quantitative analysis combined XGBoost, SHAP and Pearson correlations.

## What the software handles

A click is a self-report signal of an attentional lapse. Researchers define lecture structures to represent teaching segments. Survey and observation records supply context for interpreting the patterns.

The local implementation includes the following workflow:

1. Collect and manage classroom records through the application and SQLite-backed data model.
2. Align clicker records with lecture structures and combine student/lecture survey and observation data.
3. Aggregate student-level information into structure-level features and prepare structured/text representations.
4. Produce attention-class labels using a Nearest Centroid component and train/evaluate XGBoost classifiers.
5. Analyze features with interpretability and correlation tools and generate evaluation/research reports and dashboards.

## Technical scope

| Area | Methods and tools used in the project |
|---|---|
| Data engineering | Python, SQL/SQLite, pandas, multi-source integration, time alignment, aggregation, feature engineering |
| AI/NLP | Structured feature extraction, text processing, sentence embeddings |
| Machine learning | scikit-learn, Nearest Centroid, XGBoost, train/validation/test handling, class weighting, model evaluation and persistence |
| Interpretability/statistics | SHAP code paths, Pearson/correlation analysis, feature importance, classification metrics and confusion matrices |
| Research software | Django, Flask, Docker, reporting and dashboard components |

## Published findings

Physical condition had the strongest association with inattention among the examined variables (r = +0.7054); device multiplicity showed a small association (r = +0.0312). These results are attributed to the collaborative publication. Correlations and model explanations are not proof of causality.

## Existing project evidence

The inspected checkout contains training/orchestration source, a saved evaluation-metrics artifact, feature-impact reports and a documented train/test-before-labeling workflow. The local feature-impact JSON records physical-condition and equipment-diversity correlations that round to the values reported in the paper.

One stored feature-impact report explicitly records **Correlation Analysis (Fallback from SHAP)**. Its correlation values must not be described as SHAP values. Saved classifier accuracy is not presented here as independently verified generalization performance: its run configuration, label provenance and evaluation split still need tracing.

The exact historical code/snapshot used for every published result has not been fully mapped to this checkout. This case study describes the real implementation and existing evidence; it does not substitute an invented demo for the project.
