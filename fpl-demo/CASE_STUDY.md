# FPL — research software and a reproducible data example

## Research context

FPL supports research into attention in foreign-language classrooms. Its workflow combines self-report alert clicks, researcher-defined lecture segments, classroom observations and surveys. The published study also describes follow-up interviews and interpretable machine learning analysis.

Thanh (Cầm Duy Thành, Tin) is a co-author of [The impact of well-being on university students’ attention in foreign language classrooms in Japan](https://doi.org/10.1016/j.socimp.2026.100195), Societal Impacts, 2026. He reports responsibility for FPL software development, using ChatGPT and Claude for programming support since 2024. The paper is a collaborative research output.

## The concrete problem

An alert count, a student count and the amount of survey context answer different questions. Merging them without clear units can make a report appear more complete than its inputs support.

This new example makes those distinctions inspectable. It uses synthetic records and a small SQLite database created in memory. It is separate from the private research system and its historical datasets.

## Design decisions

- Sum `click_count` as alerts and count mapped students separately.
- Link clicker identity within a lecture, rather than assuming a device always belongs to one person.
- Preserve missing survey links and distinguish them from observed negative survey answers.
- Assign a shared timestamp boundary to one segment using an explicit example policy; reject overlapping segments.
- Report unmapped devices and alerts outside all segments.
- Expose a clearly named linkage fraction and leave research confidence unestimated.

## Evidence

The example produces the table in [README](README.md). Nine automated checks exercise the decisions above. A fresh run needs only Python's standard library and does not access research data or services.

## Development history and ownership

On 6 October 2026, Tin clarified the meaning of an alert and challenged a draft exercise that treated it as a correct or incorrect answer. That clarification changed the example's domain model.

The example implementation, tests and initial documentation were prepared with AI assistance during that session. Tin's independent explanation and modification of the example are the next review step; they are not recorded as completed.

## Scope and next steps

The code version and dataset used for the published paper have not yet been mapped to this local checkout. The example does not recreate the paper's analysis or validate its confidence rules. The next steps are to review those definitions with Tin, add a versioned research data contract, and trace one permitted result from source to output.
