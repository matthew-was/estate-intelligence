# Conversation Summary: Agent-Based Development Workflow

## Context
Discussed setting up a multi-agent workflow using Claude Code to manage the Family Estate Document Archive System project. The project has become scattered across multiple chats and artifacts, and needs better organization and structure before significant implementation.

## Key Decisions Made

### Agent Structure (7 Roles, One Optional)

1. **Product Owner Agent**
   - Responsibility: Convert raw requirements and use cases into formal user stories with acceptance criteria
   - Output: Requirements documentation, detailed user stories
   - Interaction: Takes project goals as input, produces structured requirements

2. **Head of Development Agent**
   - Responsibility: Evolve system architecture based on requirements; make cross-cutting architectural decisions
   - Output: Architecture decisions, component specifications, validation of design patterns
   - Interaction: Works with you to iterate on architecture; ensures alignment with "infrastructure as configuration" principle
   - Role: Senior developer-level discussion, not autonomous decision-making

3. **Integration Agent** (Critical Addition)
   - Responsibility: Own the PostgreSQL backend codebase as the single source of truth
   - Output: Database schema, backend API contracts, data access patterns
   - Specific tasks:
     - Manage schema evolution
     - Define API interfaces that components depend on
     - Validate component data access patterns
     - Ensure components don't create tight coupling through the database
     - Manage migrations and backward compatibility
     - Prevent ad-hoc queries from multiple components
   - Why needed: Prevents nightmare scenario where multiple components independently query the database and break on schema changes

4. **Senior Developer Agents** (Multiple, One Per Component)
   - Responsibility: Decompose component specifications into detailed implementation plans
   - Output: Implementation plan, data access requirements, new schema/API needs for Integration Agent to approve
   - Interaction: Proposes what they need from the database/backend → Integration Agent validates → Senior Developer proceeds
   - Note: If a component is large (3-4 months, 5+ subsystems), escalate to Team Lead structure

5. **Implementer Agent** (Optional, Used Selectively)
   - Responsibility: Write code based on Senior Developer plans for components where you're not learning
   - Output: Working code following the plan, with tests
   - Used for: Component 1 (Document Intake web UI) — you already know web development well, no learning value
   - Not used for: Components 2-5 (Text Extraction, Embedding, Query, Continuous Ingestion) — these are where you're learning new concepts (OCR, embeddings, RAG, document processing pipelines)
   - Approach: Takes detailed Senior Developer plan and produces implementation-ready code with tests. Code Reviewer validates quality before you review/merge.
   - Benefit: Frees you to focus on learning new concepts while leveraging Claude Code for routine/familiar work

6. **Code Reviewer Agent**
   - Responsibility: Quality assurance and security validation of implemented code
   - Output: Code review feedback, quality concerns, security considerations
   - Specific focus:
     - Code quality, maintainability, clarity
     - Security by design (not as a separate concern, but as fundamental architecture)
     - Consistency across components (patterns, error handling, data access)
     - Proper use of configuration abstraction layer
     - Security thinking is embedded in design, not bolted on
   - Why combined: Document pipeline handles untrusted input (user uploads, PDFs) and sensitive data (family documents). Security is architectural, not compliance-driven. Code Reviewer validates that security fundamentals are embedded in implementation.
   - Interaction: Receives code after Integration Agent has validated data access contracts. Reviews for quality and security-by-design alignment.

7. **Project Manager Agent**
   - Responsibility: Convert Senior Developer implementation plans into actionable tasks
   - Output: Task breakdown with dependencies, sequencing, blockers
   - Interaction: Takes detailed plans and operationalizes them

### Design Pattern: Human-in-the-Loop

- **Not full autonomy**: Agents analyze, synthesize, present options, validate thinking
- **You make decisions**: Each workflow step involves you as decision-maker
- **Agent as informed participant**: Agents bring domain knowledge and catch issues, but don't decide ambiguous questions
- This is more sustainable and realistic than trying to make agents fully autonomous on complex architectural decisions

### Development Workflows

**For learning components (Components 2-5: Text Extraction, Embedding, Query, Continuous Ingestion):**
Plan (Senior Dev) → You implement (hands-on learning) → Integration Agent (validates contracts) → Code Reviewer (validates quality & security) → You refine → Mark done

**For non-learning components (Component 1: Document Intake web UI):**
Plan (Senior Dev) → Implementer writes code → Integration Agent (validates contracts) → Code Reviewer (validates quality & security) → You review/merge → Mark done

**Key principle**: Security is fundamental architecture, not a separate compliance concern. Code Reviewer validates that security thinking is embedded in design and implementation from the start.

### Key Insight: Skills vs Agents

Skills are **reusable workflow definitions and domain knowledge** that multiple agents reference. They're patterns that get used across components.

For your project, skills should include patterns like:

- OCR & Text Extraction Workflow (used by multiple text extraction components)
- Embedding & Chunking Strategy (referenced by integration agent and extraction developers)
- Configuration Pattern (your "infrastructure as configuration" principle, used by every developer)
- RAG Implementation (shared between query and LLM integration)
- Testing Strategy for Pipelines (each pipeline component needs this)

Skills are identified by asking: "Will multiple agents or components need to reference this pattern?" If yes, it's a skill. If specific to one component, it belongs in that component's detailed plan.

## Critical Unknowns to Resolve Before Code

Before implementation, you need to document:

1. **Component Boundaries**
   - Current doc lists five components but boundaries aren't precise
   - Example: Does "Text Extraction & Processing" own deduplication or "Document Intake"?

2. **Data Flow Between Components**
   - What data gets passed where?
   - Which components write to database? Which read-only? Both?
   - What are transaction/consistency requirements?

3. **Configuration Abstraction Points**
   - Map every service needing abstraction: OCR engines, LLM providers, embedding services, storage backends, database connections, vector DB
   - Define how each gets swapped at runtime

4. **Error Handling & Retry Strategy**
   - What happens when OCR fails?
   - When embedding service is down?
   - When duplicate detection finds a match?
   - Each component needs to know the contract

5. **Metadata Evolution Strategy**
   - Current doc lists important metadata but needs formal schema
   - How can components extend metadata without breaking others?

6. **Testing Strategy Per Component Type**
   - Pipeline components (text extraction) test differently than query components
   - Need reusable patterns for each type

7. **Integration Points with PostgreSQL**
   - Read vs write semantics for each component
   - Consistency guarantees
   - Transaction boundaries

## Repository Structure Recommendation

```text
.claude/
├── agents/
│   ├── product-owner.md              # Requirements & user stories
│   ├── head-of-development.md        # Architecture evolution
│   ├── integration-lead.md           # Database schema & backend API
│   ├── senior-developer-template.md  # Template for component leads
│   └── project-manager.md            # Task breakdown
├── skills/
│   ├── ocr-extraction-workflow.md
│   ├── embedding-chunking-strategy.md
│   ├── configuration-patterns.md
│   ├── rag-implementation.md
│   ├── metadata-schema.md
│   └── pipeline-testing-strategy.md
├── rules/
│   └── system-principles.md          # "Infrastructure as configuration" principle
├── docs/
│   ├── requirements/                 # Output from Product Owner
│   ├── architecture/                 # Output from Head of Development
│   ├── component-plans/              # Output from Senior Developers
│   ├── integration-spec/             # Output from Integration Agent
│   └── tasks/                        # Output from Project Manager
└── contexts/                         # Project state and decisions
```

## Next Steps (Recommended Order)

1. **Formalize Requirements** — Take existing use cases and turn into detailed user stories with acceptance criteria
2. **Map Component Boundaries & Data Flow** — Create precise definitions of what each component owns, what data moves where
3. **Document Configuration Abstraction Layer** — List every service/backend that needs to be pluggable and how

Once these three are clear, the rest becomes straightforward for Senior Developers to implement in isolation.

## Reference Materials

- **everything-claude-code repo**: https://github.com/affaan-m/everything-claude-code
  - Battle-tested agent patterns from Anthropic hackathon winner
  - Shows how to structure agents as markdown files with role definitions, scope, tools, input/output formats
  - Examples: planner, architect, code-reviewer, security-reviewer, etc.
  - Note: For this project, code-reviewer and security-reviewer are merged into a single Code Reviewer agent because security is fundamental to the document pipeline architecture, not a separate compliance concern

## Key Philosophy

This approach prioritizes **clarity and documentation over quick implementation** because:

- Project will be paused and resumed multiple times
- Clear boundaries and contracts prevent rework when picking it back up
- Each agent/developer can work independently with full context
- Reduces surprises and integration issues later
- Makes the entire system understandable to future maintainers (including future you)
