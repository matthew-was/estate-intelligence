# Claude Code — Project Instructions

## Permission Requests

When a task requires a Bash command that is not in the current allow list, always present the permission request with an explicit option to add it to the `.claude/settings.json` allow list. The user prefers to grow the allow list incrementally rather than approving one-off commands.

Current allow list (`.claude/settings.json`):
- `Bash(mkdir:*)`
- `Bash(rm:*)`
- `Bash(ls:*)`
- `Bash(tail:*)`
- `Edit(./*)`
- `Read(./*)`
- `Write(./*)`

When requesting a new permission, say clearly: "This requires `Bash(command:*)` — would you like to add it to the allow list in `.claude/settings.json`?"

---

## Project Overview

This is the **Estate Intelligence** project — a family document archiving system (1950s–present) with an AI/ML learning component. See [documentation/README.md](documentation/README.md) for full navigation.

### Component Architecture (4 components)

| Component | Name | Status |
| --- | --- | --- |
| C1 | Document Intake | Spec complete, not started |
| C2 | Text Extraction, Processing & Embedding | Spec complete, not started |
| C3 | Query & Retrieval | Design brief only |
| C4 | Continuous Ingestion | Placeholder (Phase 2+) |

### Core Principle

**Infrastructure as Configuration**: every external service (storage, database, OCR, embedding, LLM) is abstracted via an interface. Concrete implementation is selected at runtime via config. No hardcoded providers.

---

## Documentation Structure

```
documentation/
├── README.md                     ← Navigation index
├── SUMMARY.md                    ← What was done + .claude/ setup guide
├── project/                      ← Overview, architecture, pipeline diagram, domain context
├── components/                   ← Per-component specs, quick refs, design rationale
├── process/                      ← Agent workflow, skills catalogue, dev principles
└── decisions/                    ← ADRs and unresolved questions
```

---

## Agent and Skills Setup

The `.claude/` directory structure and all agents and skills still need to be created. See [documentation/SUMMARY.md](documentation/SUMMARY.md) for the complete setup guide, including:

- 7 agents to create (Product Owner, Head of Development, Integration Lead, Senior Developer × 2, Implementer, Code Reviewer, Project Manager)
- 6 skills to create (in dependency order)
- 5 unresolved questions to answer before coding begins
- 22-step recommended implementation sequence
