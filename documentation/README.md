# Documentation

All design and process documentation for the Estate Intelligence project. Start here to find anything.

---

## Navigation Guide

### If you want to understand the project

→ [project/overview.md](project/overview.md) — Goals, use cases, principles, developer background

→ [project/architecture.md](project/architecture.md) — All 4 components, phases, tech stack, data flow

→ [project/pipeline-diagram.mermaid](project/pipeline-diagram.mermaid) — Visual pipeline diagram

### If you want to implement a component

→ [components/component-1-document-intake/specification.md](components/component-1-document-intake/specification.md) — Full Phase 1 spec

→ [components/component-1-document-intake/quick-reference.md](components/component-1-document-intake/quick-reference.md) — Upload flow, DB schema, API at a glance

→ [components/component-2-processing-and-embedding/overview.md](components/component-2-processing-and-embedding/overview.md) — High-level overview of both extraction and embedding stages

→ [components/component-2-processing-and-embedding/specification.md](components/component-2-processing-and-embedding/specification.md) — Full detailed spec

→ [components/component-2-processing-and-embedding/quick-reference.md](components/component-2-processing-and-embedding/quick-reference.md) — Tables and checklists at a glance

### If you want to understand why a decision was made

→ [components/component-2-processing-and-embedding/design-rationale.md](components/component-2-processing-and-embedding/design-rationale.md) — Component 2 design journey and reasoning

→ [decisions/architecture-decisions.md](decisions/architecture-decisions.md) — All ADRs across the project

### If you want to know what questions are still open

→ [decisions/unresolved-questions.md](decisions/unresolved-questions.md) — Blocking and non-blocking open questions

### If you are setting up Claude agents and skills

→ [SUMMARY.md](SUMMARY.md) — What was done + step-by-step guide to set up `.claude/` directory

→ [process/agent-workflow.md](process/agent-workflow.md) — 7-agent role definitions and workflows

→ [process/skills-catalogue.md](process/skills-catalogue.md) — All identified skills with creation order

### If you are designing a component not yet specified

→ [components/component-3-query-retrieval/README.md](components/component-3-query-retrieval/README.md) — Design brief with open questions

→ [components/component-4-continuous-ingestion/README.md](components/component-4-continuous-ingestion/README.md) — Design brief with open questions

### If you are working with estate terminology

→ [project/domain-context.md](project/domain-context.md) — Living document: approved terms, field names, people, candidates

---

## Document Status

| Document | Status | Notes |
| --- | --- | --- |
| project/overview.md | Current | Incorporates INITIAL_PURPOSE.md |
| project/architecture.md | Current | 4-component structure |
| project/pipeline-diagram.mermaid | Current | Updated for 4 components |
| project/domain-context.md | Living document | Populate as documents are processed |
| components/component-1-document-intake/specification.md | Current | Phase 1 ready to implement |
| components/component-1-document-intake/quick-reference.md | Current | |
| components/component-2-processing-and-embedding/overview.md | Current | Combined C2+C3 design |
| components/component-2-processing-and-embedding/specification.md | Current | Phase 1 ready to implement |
| components/component-2-processing-and-embedding/design-rationale.md | Current | |
| components/component-2-processing-and-embedding/readiness-checklist.md | Current | |
| components/component-2-processing-and-embedding/quick-reference.md | Current | |
| components/component-3-query-retrieval/README.md | Placeholder | Design pending after C1+C2 complete |
| components/component-4-continuous-ingestion/README.md | Placeholder | Design pending last |
| process/agent-workflow.md | Current | 7 agents defined |
| process/skills-catalogue.md | Current | 6 skills identified, none written yet |
| process/development-principles.md | Current | |
| decisions/architecture-decisions.md | Current | All ADRs from design phase |
| decisions/unresolved-questions.md | Current | Update as questions are resolved |
| SUMMARY.md | Current | .claude/ setup guide |

---

## Component Numbering Reference

This project uses 4 components (previously 5 in early design documents). The merge:

| Current | Was | Description |
| --- | --- | --- |
| Component 1 | Component 1 | Document Intake (unchanged) |
| Component 2 | Components 2 + 3 | Text Extraction, Processing & Embedding |
| Component 3 | Component 4 | Query & Retrieval |
| Component 4 | Component 5 | Continuous Ingestion |
