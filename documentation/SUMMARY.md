# Estate Intelligence: Documentation Summary & Next Steps

## What Was Done

### What Was Found

The `initial documentation/` directory contained high-quality, well-considered design work across 10 files — two complete component specs, an agent workflow design, a combined overview, and pipeline diagrams. The content was strong but scattered with inconsistent naming, no navigational structure, and no clear indication of which document superseded which.

Key findings:
- Components 1 and 2 are fully specified and ready for Phase 1 implementation
- The agent workflow design (in `working-with-claude.md`) was complete but had no `.claude/` directory to make it operational
- A combined C2+C3 overview document signalled that the original 5-component design had evolved to 4 components
- Critical unresolved questions were mixed into a workflow document rather than tracked as blockers

### Component Renumbering

During this reorganisation, the decision was made to merge the original Components 2 and 3 into a single Component 2. See [decisions/architecture-decisions.md](decisions/architecture-decisions.md) ADR-005.

| Was | Now |
| --- | --- |
| Component 1 (Document Intake) | Component 1 (unchanged) |
| Component 2 (Text Extraction) + Component 3 (Embedding) | Component 2 (Text Extraction, Processing & Embedding) |
| Component 4 (Query & Retrieval) | Component 3 |
| Component 5 (Continuous Ingestion) | Component 4 |

### Source-to-Destination Map

| Source File | Destination | Treatment |
| --- | --- | --- |
| `family-estate-ducment-archive-system-project-context.md` | `project/overview.md` + `project/architecture.md` | Split: goals/principles → overview; components/phases/stack → architecture |
| `estate-archive-document-intake-system-component-1-specification.md` | `components/component-1-document-intake/specification.md` | Moved; H1 title added |
| `high-level-project-document-component-2-update.md` | `components/component-2-processing-and-embedding/overview.md` | Moved; component numbers updated |
| `component-2-text-extraction-and-document-processing-design-spec.md` | `components/component-2-processing-and-embedding/specification.md` | Moved; "Handoff Notes to Component 3" → "Internal Stage: Embedding & Storage" |
| `component-2-design-conversation-summary.md` | `components/component-2-processing-and-embedding/design-rationale.md` | Moved, renamed |
| `component-2-design-readiness-and-handoff-checklist.md` | `components/component-2-processing-and-embedding/readiness-checklist.md` | Moved, renamed |
| `component-2-quick-reference.md` | `components/component-2-processing-and-embedding/quick-reference.md` | Moved; embedding stage added |
| `working-with-claude.md` | `process/agent-workflow.md` + `process/skills-catalogue.md` | Split by concern |
| `document_pipeline.mermaid` | `project/pipeline-diagram.mermaid` | Updated for 4-component structure |
| `INITIAL_PURPOSE.md` | Incorporated into `project/overview.md` | Merged |

New files synthesised:
- `documentation/README.md` — navigation index
- `project/domain-context.md` — living estate terminology document
- `components/component-1-document-intake/quick-reference.md` — synthesised from C1 spec
- `components/component-3-query-retrieval/README.md` — design brief with open questions
- `components/component-4-continuous-ingestion/README.md` — design brief with open questions
- `process/development-principles.md` — synthesised from all design documents
- `decisions/architecture-decisions.md` — all ADRs consolidated
- `decisions/unresolved-questions.md` — all open questions consolidated

### Current Implementation Status

| Component | Design | Implementation |
| --- | --- | --- |
| Component 1: Document Intake | Phase 1 complete | Not started |
| Component 2: Processing & Embedding | Phase 1 complete | Not started |
| Component 3: Query & Retrieval | Design brief ready | Not started |
| Component 4: Continuous Ingestion | Placeholder (Phase 2+) | Not started |

---

## Next Steps: Setting Up the `.claude/` Directory

The `process/agent-workflow.md` document defines a complete 7-agent workflow. None of the agent or skill files exist yet. This section provides the concrete steps to make it operational.

### Target `.claude/` Structure

```text
.claude/
├── settings.json             ← Already created (permissions)
├── agents/
│   ├── product-owner.md
│   ├── head-of-development.md
│   ├── integration-lead.md
│   ├── senior-developer-template.md
│   ├── senior-developer-component-1.md
│   ├── senior-developer-component-2.md
│   ├── implementer.md
│   ├── code-reviewer.md
│   └── project-manager.md
└── skills/
    ├── configuration-patterns.md
    ├── metadata-schema.md
    ├── pipeline-testing-strategy.md
    ├── ocr-extraction-workflow.md
    ├── embedding-chunking-strategy.md
    └── rag-implementation.md
```

---

## Agents to Create

Each agent is a markdown file in `.claude/agents/`. Use [everything-claude-code](https://github.com/affaan-m/everything-claude-code) as a reference for file format.

For each agent, the file should contain: role definition, inputs, output format, scope constraints, escalation rules, and context files to read.

---

### `product-owner.md`

**Role**: User story writer. Converts use cases and requirements into formal user stories with acceptance criteria.

**Input**: Project goals, use cases, feature requests, phase requirements

**Output format**: User stories (`As a [role], I want [action] so that [benefit]`) with acceptance criteria, definition of done, phase assignment

**Scope**: Does NOT make architectural decisions. Flags architectural implications to Head of Development.

**Key context to include**: [project/overview.md](project/overview.md) (use cases section)

**Output location**: `.claude/docs/requirements/`

---

### `head-of-development.md`

**Role**: Architectural decision-maker for cross-cutting concerns. Ensures Infrastructure as Configuration principle is upheld.

**Input**: Requirements from Product Owner, proposals from Senior Developers, cross-cutting questions

**Output format**: Architecture decisions (recorded in decisions/architecture-decisions.md), updated architecture docs, validation or rejection of component choices

**Scope**: Cross-cutting decisions ONLY. Discussion partner, not autonomous decision-maker — presents options with tradeoffs.

**Hard constraint**: Every decision must honour the Infrastructure as Configuration principle.

**Key context to include**: [project/architecture.md](project/architecture.md), [process/development-principles.md](process/development-principles.md), [decisions/architecture-decisions.md](decisions/architecture-decisions.md)

---

### `integration-lead.md`

**Role**: Owns the PostgreSQL backend as the single source of truth.

**Input**: Data access requirement proposals from Senior Developers

**Output format**: Approved schema changes + migration files, API contracts (TypeScript interfaces), rejections with recommended alternatives

**Specific responsibilities**:
- Manage schema evolution and migrations
- Define API interfaces that all components depend on
- Validate component data access patterns (no ad-hoc queries)
- Prevent components from coupling through the database
- Manage backward compatibility

**Hard rules**:
- No component gets database access without Integration Lead approval
- No direct SQL queries outside defined access patterns

**Key context to include**: [project/architecture.md](project/architecture.md), all component specifications, [decisions/unresolved-questions.md](decisions/unresolved-questions.md) (UQ-001, UQ-003, UQ-005)

**First task when set up**: Review Component 1 and Component 2 specifications for compliance with these rules. Answer UQ-001 and UQ-005.

---

### `senior-developer-template.md`

**Role**: Implementation planner for a single component (instanced per component).

**Input**: Component specification, architecture, Integration Lead contracts, relevant skills

**Output format**: Implementation plan with ordered tasks, data access requirements (for Integration Lead), new schema/API needs, complexity estimates

**Workflow**: Propose data access needs → Integration Lead validates → proceed with plan

**Escalation**: If component has 5+ subsystems or 3–4 months of work, escalate to Team Lead structure

Component-specific instances:
- `senior-developer-component-1.md` — context: [components/component-1-document-intake/specification.md](components/component-1-document-intake/specification.md)
- `senior-developer-component-2.md` — context: all files in [components/component-2-processing-and-embedding/](components/component-2-processing-and-embedding/)

---

### `implementer.md`

**Role**: Code writer. Used for Component 1 ONLY (established domain, no learning value for developer).

**Input**: Detailed Senior Developer implementation plan

**Output**: Working TypeScript/Node.js code + Vitest tests

**Hard constraints**:
- Implements exactly what the plan specifies
- Does NOT make architectural decisions
- Does NOT skip tests
- Does NOT choose different libraries than specified

**Code standards**: TypeScript strict mode, Pino logging, Zod validation, pnpm workspace patterns.

**Key context to include**: [components/component-1-document-intake/specification.md](components/component-1-document-intake/specification.md), `configuration-patterns.md` skill, `pipeline-testing-strategy.md` skill

---

### `code-reviewer.md`

**Role**: Quality and security reviewer. Security is treated as architectural, not as compliance.

**Input**: Code (PR or file set) + original implementation plan

**Output**: Review comments with severity (blocking/suggestion), security findings, pattern observations

**Review focus**:
- Code quality, maintainability, TypeScript strictness
- Security at system boundaries (file upload validation, input sanitisation, path traversal, MIME types)
- Proper use of configuration abstraction layer (no hardcoded providers)
- Error handling consistency (correct HTTP codes, cleanup on failure)
- No secrets/credentials/document content in logs

**When invoked**: After Integration Lead validates data access contracts; after code is written.

**Key context to include**: [process/development-principles.md](process/development-principles.md), [decisions/architecture-decisions.md](decisions/architecture-decisions.md)

---

### `project-manager.md`

**Role**: Task breakdown and sequencing from Senior Developer plans.

**Input**: Senior Developer implementation plan

**Output format**: Ordered task list — each task has: description, dependency (if any), complexity (S/M/L), acceptance condition

**Scope**: Does not make design decisions. If a task is ambiguous, flags it for the Senior Developer.

**Output location**: `.claude/docs/tasks/component-N-tasks.md`

---

## Skills to Create

Skills live in `.claude/skills/`. Write them in this order — each is a dependency for work that follows.

Full descriptions in [process/skills-catalogue.md](process/skills-catalogue.md).

### Creation Order

**1. `configuration-patterns.md`** — Write first (blocks all Senior Developer agents)

- The "Infrastructure as Configuration" principle in implementation terms
- TypeScript interfaces + factory/DI patterns
- Python abstract base classes + factory functions
- All abstraction points enumerated with runtime selection mechanism
- Component 1's `StorageService` as first concrete reference

**2. `metadata-schema.md`** — Write second (Integration Lead needs this)

- Canonical field list for document, chunk, and processing metadata
- Required vs optional per document type
- Schema evolution strategy

**3. `pipeline-testing-strategy.md`** — Write third (must exist before code)

- Vitest (TypeScript) and pytest (Python) setup patterns
- Pipeline stage isolation testing
- Fixture document strategy
- Test database management (`estate_archive_test`)

**4. `ocr-extraction-workflow.md`** — Write before Component 2 implementation

- File type detection algorithm
- Docling/Tesseract decision tree
- Confidence scoring
- Graceful degradation ladder

**5. `embedding-chunking-strategy.md`** — Write after Component 2 Phase 1

- Heuristic chunking algorithm
- Parent document reference pattern
- pgvector storage patterns
- Embedding provider abstraction

**6. `rag-implementation.md`** — Write before Component 3 design

- Similarity search patterns
- Context assembly
- LLM provider abstraction
- Response format with citations

---

## Unresolved Questions to Answer Before Coding

Full details in [decisions/unresolved-questions.md](decisions/unresolved-questions.md).

**Must answer before any component coding begins**:

1. **UQ-001 Data flow & read/write ownership** — Which components write vs read the database? Transaction boundaries?
2. **UQ-002 Configuration abstraction map** — Complete list of every service needing abstraction + runtime selection mechanism
3. **UQ-003 Formal metadata schema** — Canonical fields, required/optional per type, extension strategy
4. **UQ-004 Testing strategy** — Python pipeline testing patterns + fixture strategy
5. **UQ-005 PostgreSQL integration points** — Read/write semantics per component

**Must answer before Component 2 implementation**:

6. **UQ-C2-001 Semantic chunking heuristics** — Exact rules per document type
7. **UQ-C2-002 Category detection patterns** — Pattern list per category

---

## Recommended Implementation Sequence

This sequence minimises rework by resolving dependencies before they block work.

### Foundation (Before Any Code)

**Step 1**: Use Head of Development agent to work through UQ-001, UQ-002, UQ-003, UQ-005

**Step 2**: Write `configuration-patterns.md` skill (using Component 1 StorageService as first example)

**Step 3**: Write `metadata-schema.md` skill (informed by Step 1 answers)

**Step 4**: Write `pipeline-testing-strategy.md` skill

**Step 5**: Set up Integration Lead agent. Its first task: review C1 + C2 specs for data access compliance; answer UQ-001 and UQ-005 formally.

### Component 1 Implementation

**Step 6**: Product Owner agent — formalise Phase 1 user stories from [project/overview.md](project/overview.md) use cases → `.claude/docs/requirements/phase-1-user-stories.md`

**Step 7**: Senior Developer (Component 1) agent — create implementation plan

**Step 8**: Integration Lead validates Component 1 data access patterns

**Step 9**: Project Manager — create task breakdown → `.claude/docs/tasks/component-1-tasks.md`

**Step 10**: Implementer agent — writes Component 1 code + tests

**Step 11**: Code Reviewer validates

**Step 12**: Developer reviews and merges

### Component 2 Implementation

**Step 13**: Answer UQ-C2-001 and UQ-C2-002 (requires looking at actual estate documents)

**Step 14**: Write `ocr-extraction-workflow.md` skill

**Step 15**: Senior Developer (Component 2) agent — create implementation plan. Uses all files in [components/component-2-processing-and-embedding/](components/component-2-processing-and-embedding/).

**Step 16**: Integration Lead validates Component 2 data access patterns

**Step 17**: Project Manager — create task breakdown

**Step 18**: Developer implements Component 2 (learning component — no Implementer agent)

**Step 19**: Code Reviewer validates

### Component 3 Design

**Step 20**: Write `embedding-chunking-strategy.md` skill (now informed by real implementation)

**Step 21**: Design Component 3 using [components/component-3-query-retrieval/README.md](components/component-3-query-retrieval/README.md) as the brief

**Step 22**: Write `rag-implementation.md` skill

**Then**: Continue with Component 3 implementation (developer implements — learning component), then Component 4 design and implementation.

---

## Reference

- [process/agent-workflow.md](process/agent-workflow.md) — Full agent role definitions
- [process/skills-catalogue.md](process/skills-catalogue.md) — Full skills list with purpose and dependencies
- [decisions/unresolved-questions.md](decisions/unresolved-questions.md) — Open questions
- [decisions/architecture-decisions.md](decisions/architecture-decisions.md) — All ADRs
- [everything-claude-code repo](https://github.com/affaan-m/everything-claude-code) — Agent file format reference
