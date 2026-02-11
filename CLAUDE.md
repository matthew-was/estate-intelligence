# Claude Code — Project Instructions

## Permission Requests

When a task requires a Bash command that is not in the current allow list, always present the permission request with an explicit option to add it to the `.claude/settings.json` allow list. The user prefers to grow the allow list incrementally rather than approving one-off commands.

Current allow list (`.claude/settings.json`):

- `Bash(mkdir:*)`
- `Bash(rm:*)`
- `Bash(mv:*)`
- `Bash(ls:*)`
- `Bash(tail:*)`
- `Bash(git:*)`
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

```text
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

> **Immediate next step**: Write `.claude/skills/agent-file-conventions.md` — this is the prerequisite for all agent file creation and must exist before any `.claude/agents/*.md` files are written.

The `.claude/` directory structure and all agents and skills still need to be created. See [documentation/SUMMARY.md](documentation/SUMMARY.md) for the complete setup guide, including:

- 8 agents to create (Product Owner, Head of Development, Integration Lead, Senior Developer × 2, Implementer, Pair Programmer, Code Reviewer, Project Manager)
- 7 skills to create (in dependency order — `agent-file-conventions.md` first)
- 6 unresolved questions to answer before coding begins (UQ-001 through UQ-006)
- 24-step recommended implementation sequence

### Key Output Locations

As agents complete their phases, outputs are written here:

```text
.claude/docs/
├── requirements/
│   ├── user-requirements.md       ← Product Owner (Step 1) — authoritative scope baseline
│   └── phase-1-user-stories.md    ← Product Owner (Step 2)
└── tasks/
    ├── component-1-tasks.md       ← Project Manager (Step 10)
    └── component-2-tasks.md       ← Project Manager (Step 18)
```

These documents are the handoff mechanism between agents. Each subsequent agent reads from the relevant output documents of prior phases. When starting a new agent session, pass the appropriate documents as context — see [documentation/process/agent-workflow.md](documentation/process/agent-workflow.md) for the per-agent context table.
