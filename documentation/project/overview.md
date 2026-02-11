# Project Overview

## Why This Project Exists

This project has two equally important goals:

1. **Preserve family history**: Archive and make searchable the historic documents from a family farming estate — spanning from the 1950s to the present. These documents record land ownership, infrastructure decisions, farming operations, and family history. Without a systematic archive, this knowledge is at risk of being lost.

2. **Learn AI engineering**: Use this real project as a hands-on vehicle for learning AI/ML workflows, document processing pipelines, and modern AI tooling. The developer has strong existing skills in web development but wants to build practical expertise in AI as a professional skill.

Both goals are first-class. Design decisions deliberately choose approaches that maximise learning and understanding over black-box convenience.

---

## Document Scope

**Time range**: 1950s to present

**Initial scale**: Hundreds of documents (learning phase)

**Target scale**: Tens of thousands of documents

**Document types**:

- Handwritten letters (scanned to image)
- Typewritten documents (scanned to image or PDF)
- Modern emails and digital PDFs
- Physical documents requiring scanning before digitisation

---

## Key Use Cases

The system is designed to answer questions about the estate's history. Primary query types:

- **Land ownership**: "What is known about ownership of the north field?"
- **Infrastructure history**: "Where were pipes laid through the east meadow, and when?"
- **Decision summaries**: "What decisions were made about the purchase or sale of certain plots?"
- **People and relationships**: "Who was involved in the sale of the mill pasture?"

These use cases drive metadata and retrieval design — dates, land references, people, and document relationships are first-class metadata requirements.

---

## Architectural Principles

### Infrastructure as Configuration

The single most important architectural principle in this project. Every external service must be accessed through an abstraction interface. The concrete implementation is selected at runtime via configuration, not hardcoded in application logic.

**What this means in practice**:

```text
Application code: storageService.store(file)   ← never changes
Configuration:    STORAGE_BACKEND=local         ← changes per environment
Runtime:          LocalFilesystemAdapter loads  ← determined by config
```

**Key abstraction points**:

| Service | Phase 1 Default | Phase 2+ Option |
| ------- | --------------- | --------------- |
| Document storage | Local filesystem | AWS S3 |
| Database | Local PostgreSQL (Docker) | AWS RDS |
| OCR engine | Docling (+ Tesseract fallback) | Alternative OCR services |
| LLM provider | Claude API | GPT, local models |
| Embedding service | OpenAI/Anthropic | Local embedding models |
| Vector DB | pgvector (PostgreSQL) | Dedicated vector DB |
| Compute | Docker local | AWS EC2/ECS |

**Implementation approach**: TypeScript interfaces + factory/DI patterns (backend); Python abstract base classes + factory functions (processing pipeline). See [process/development-principles.md](../process/development-principles.md) and the `configuration-patterns.md` skill for implementation guidance.

---

## Design Principles

1. **Start small and complete**: Build a complete end-to-end pipeline with the simplest cases first. A working system with limited scope beats a partial system with broad scope.

2. **Infrastructure as code from day one**: All infrastructure choices configurable from day one, not retrofitted later.

3. **Incremental expansion**: Add complexity component by component, phase by phase.

4. **Real-world testing**: Use actual family documents during development, not toy datasets. Assumptions only get validated on real data.

5. **Maintainability**: Design for ongoing document addition and for infrastructure changes over time.

6. **Learning-focused**: Understand each step deeply. Components 2–4 are learning components — the developer implements them personally rather than using an Implementer agent.

7. **Migration-ready**: Apply patterns from day one that will work on AWS without code rewrites.

8. **Type safety end-to-end**: TypeScript strict mode in all TypeScript packages. Zod validation at all external boundaries.

9. **Test early**: Tests written alongside code, not deferred. Real PostgreSQL for integration tests, not mocks.

10. **Document during build**: Documentation written as decisions are made, not after.

---

## Developer Background

**Strong existing skills**:

- 9+ years full-stack JavaScript/TypeScript
- Docker and Linux environments
- PostgreSQL (extensive experience)
- AWS: EC2, ECS, S3, some OpenSearch

**Skills being developed through this project**:

- Python (OCR and AI/ML components)
- Document processing pipelines
- Vector embeddings and pgvector
- RAG (Retrieval Augmented Generation)
- AI/ML workflow tooling

---

## Development Environments

**Local development (Phase 1–2)**:

- Docker Compose orchestrates all local services (PostgreSQL + pgvector, application containers)
- Configuration points to local services by default
- No cloud dependencies required for development

**Production (Phase 3+)**:

- Same application code and Docker containers
- Configuration points to AWS RDS, S3, and API endpoints
- Docker runs on EC2 or migrates to ECS
- No code rewrites required — only configuration changes

This seamless transition is guaranteed by the Infrastructure as Configuration principle.

---

## Navigation

| If you want to... | Go to... |
| --- | --- |
| Understand the full system architecture | [project/architecture.md](architecture.md) |
| See the pipeline visually | [project/pipeline-diagram.mermaid](pipeline-diagram.mermaid) |
| Understand a specific component | [components/](../components/) |
| Understand why decisions were made | [decisions/architecture-decisions.md](../decisions/architecture-decisions.md) |
| See what questions are still open | [decisions/unresolved-questions.md](../decisions/unresolved-questions.md) |
| Set up agents and skills | [documentation/SUMMARY.md](../SUMMARY.md) |
