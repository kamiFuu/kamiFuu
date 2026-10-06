# FPL: alert and survey linkage example

A small, reproducible example of data quality checks for classroom research. Every record is synthetic. It is a new portfolio extension, prepared with AI assistance on 6 October 2026, inspired by the FPL research workflow.

An alert is a student's self-report signal of an attentional lapse. It is not a quiz answer. A lecture structure represents a researcher-defined segment of teaching. A survey provides further context for interpreting the alerts.

## Run

Python 3.10+; standard library only. No GPU, API key, database file or external service.

```bash
python3 demo.py
python3 -m unittest discover -s . -p 'test_demo.py' -v
```

## What the example demonstrates

| Segment | Alerts | Mapped students | Students without linked survey | Unmapped records |
|---|---:|---:|---:|---:|
| LS01 | 3 | 2 | 1 | 0 |
| LS02 | 2 | 1 | 0 | 1 |
| LS03 | 0 | 0 | 0 | 0 |

Two alerts from one student remain two alerts but one student. A missing survey remains missing; a survey answer of false is still an observed answer. A clicker with no student assignment remains visible in the quality report.

The example scopes clicker assignments and survey links by lecture. Its interval policy is `[start, end)`: an event on a shared boundary belongs to the following segment. Overlapping segments are rejected. These are explicit example policies; the legacy FPL pipeline's interval policy still needs separate review.

`linked_alert_fraction` counts alerts linked to a survey divided by all alerts in that segment. It describes linkage, not statistical confidence or a causal attribution of a reason to each alert. For a segment without alerts it is `null`. `confidence` remains `null`: the research definition and calibration are not implemented here.

## Tests and limitations

Nine tests cover repeated alerts, boundaries, missing versus false survey answers, an empty segment, unmapped clickers, aggregated click counts, lecture-scoped assignments, overlap rejection and events outside all segments.

This checks deterministic linkage and reporting on synthetic inputs. It does not measure student attention accurately, validate a machine learning model, establish causality, or reproduce the published study. All timestamps in the example use a single normalized format and timezone; a production adapter must validate those conditions.

Read [the case study](CASE_STUDY.md) and [development notes](JOURNEY.md) for the problem, decisions, evidence and next steps.
