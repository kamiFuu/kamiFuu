# Hi, I'm Thanh — Tin

I build research software and data workflows, with a focus on making results easier to inspect, explain and reproduce.

## FPL — classroom research

I am responsible for the software development of FPL, a collaborative research project on attention in foreign-language classrooms. I have used ChatGPT and Claude to support programming since 2024.

FPL brings together self-report alert clicks, researcher-defined lecture segments, observations and surveys. My current development focus is data quality, clear metric definitions and reproducible examples.

I am a co-author of [The impact of well-being on university students’ attention in foreign language classrooms in Japan](https://doi.org/10.1016/j.socimp.2026.100195), published in Societal Impacts in 2026.

### Inspect a concrete example

[**FPL alert and survey linkage example**](fpl-demo/README.md) — synthetic data, Python and SQLite, no external services.

- Separate alert counts, clicker counts and mapped student counts.
- Preserve missing survey links and report unmapped devices.
- Check timestamp boundaries and lecture-scoped identities.
- Run nine automated checks and inspect the [sample output](fpl-demo/example_output.json).

Read the [case study](fpl-demo/CASE_STUDY.md) and [development journey](fpl-demo/JOURNEY.md). This is a new AI-assisted portfolio extension; it does not reproduce the published study. Reviewing and explaining the extension is my next step.

## Related project areas

- **CorEmoLex:** emotion and corpus pipelines for NLP research.
- **CODA:** tools for AI workflow orchestration and project memory.
- **LINE translation app:** an Android prototype for translation and reply workflows.
- **Tent:** personal experiments with financial data workflows.

## Current direction

I am interested in research software, data quality and data analysis work where careful validation and clear explanations matter.
