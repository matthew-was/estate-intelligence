# Documentation

All design and process documentation for the Estate Intelligence project. Start here to find anything.

---

## Navigation Guide

### If you want to understand the project

→ [project/overview.md](project/overview.md) — Scope document: users, document types, capabilities by phase, query scope

→ [project/developer-context.md](project/developer-context.md) — Developer background and environment setup

→ [project/architecture.md](project/architecture.md) — All 4 components, phases, tech stack, data flow

→ [project/pipeline-diagram.mermaid](project/pipeline-diagram.mermaid) — Visual pipeline diagram

### If you want to understand why a decision was made

→ [decisions/architecture-decisions.md](decisions/architecture-decisions.md) — All ADRs across the project (populated by Head of Development agent)

### If you want to know what questions are still open

→ [decisions/unresolved-questions.md](decisions/unresolved-questions.md) — Blocking and non-blocking open questions

### If you want to read the requirements and user stories

→ [requirements/user-requirements.md](requirements/user-requirements.md) — Authoritative scope: 138 requirements across all phases

→ [requirements/phase-1-user-stories.md](requirements/phase-1-user-stories.md) — 101 user stories covering Phase 1 requirements

→ [approvals.md](approvals.md) — Approval status of all scope documents

### If you are setting up Claude agents and skills

→ [SUMMARY.md](SUMMARY.md) — What was done + step-by-step guide to set up `.claude/` directory

→ [process/agent-workflow.md](process/agent-workflow.md) — 8-agent role definitions and workflows

→ [process/skills-catalogue.md](process/skills-catalogue.md) — All identified skills with creation order

### If you are working with estate terminology

→ [project/domain-context.md](project/domain-context.md) — Living document: approved terms, field names, people, candidates

---

## Document Status

| Document | Status | Notes |
| --- | --- | --- |
| project/overview.md | Current | Rewritten as scope document; approved 2026-02-17 |
| project/developer-context.md | Current | Developer background and environment |
| project/architecture.md | Pending | Written by Head of Development agent |
| project/pipeline-diagram.mermaid | Current | Updated for 4 components |
| project/domain-context.md | Living document | Populate as documents are processed |
| decisions/architecture-decisions.md | Pending | Populated by Head of Development agent |
| decisions/unresolved-questions.md | Reference copy | Historical context; primary input is user-requirements.md Architectural Flags |
| requirements/user-requirements.md | Current | 138 requirements (UR-001 to UR-138); approved 2026-02-17 |
| requirements/phase-1-user-stories.md | Current | 101 stories covering all requirements; approved 2026-02-17 |
| approvals.md | Current | Approval tracking for all scope documents |
| process/agent-workflow.md | Current | 8 agents defined |
| process/skills-catalogue.md | Current | Skills identified; 3 needed before Senior Developers |
| process/development-principles.md | Current | |
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
