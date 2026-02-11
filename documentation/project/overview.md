# Project Overview

## Why This Project Exists

The Estate Intelligence system exists to preserve and make accessible the recorded history of a family farming estate spanning from the 1950s to the present. Decades of land transactions, infrastructure works, tenancy agreements, legal correspondence, and family history exist only as physical and digital documents — scattered, unsearchable, and at risk of being lost as knowledge passes between generations.

The system creates a searchable archive of these documents. A user asks a question in plain language — "what is known about the drainage works in the east meadow?" or "who owned the mill pasture before the family acquired it?" — and the system reads the relevant documents and answers directly, citing its sources.

This project also serves as a deliberate learning vehicle. The developer is using a real, meaningful problem to build practical expertise in AI and document processing. Design decisions throughout favour understanding over convenience.

---

## Who the System Is For

| User | Phase | Description |
| --- | --- | --- |
| Primary Archivist | 1 | Builds and maintains the archive; full access including system administration |
| Family Member | 2 | Full archival and curation access; no system administration or document deletion |
| Occasional Contributor | 3 | Submits documents and queries the archive; no post-submission control |
| System Administrator | 3 | Manages infrastructure and user accounts; separated from the Archivist role |

The system is private at all phases. There is no public access and no self-registration.

---

## What Documents the System Handles

| Document Type | Phase |
| --- | --- |
| Typewritten and printed documents (scanned) | 1 |
| Modern digital PDFs, correspondence, financial documents | 1 |
| Handwritten letters and notes | 2 |
| Maps, plans, and surveys | 2 |
| Emails (raw format) | 2 |
| Standalone photographs | 4+ |

Audio, video, structured data files, and web content are out of scope. Physical documents must be digitised before submission — scanning is not a system responsibility.

---

## What the System Must Do

### Phase 1 — Prove the Pipeline

A complete end-to-end pipeline running locally, used by one person. Document upload via minimal web UI; query and curation via command line.

**Must have**:

- Accept document uploads via web UI; bulk ingestion from a directory via CLI
- Detect and reject exact duplicates
- Extract text from typed and printed documents with quality scoring
- Flag poor-quality extractions for human review
- Detect document type, dates, people, and land references automatically
- Generate AI-agent-defined embeddings for each document chunk
- Maintain a domain vocabulary of estate-specific terms; flag new candidates from documents
- Answer natural language questions with synthesised responses and source citations (CLI)
- Basic curation via CLI: mark reviewed, flag issues, correct metadata, view and resubmit processing queue
- Provider-agnostic configuration throughout

**Out of scope for Phase 1**: web UI for query, curation, or administration; user authentication; supplementary context; browsing documents; viewing originals in results; replace or delete documents; multi-user access.

### Phase 2 — Expand and Share

Harder document types, full web interface, first external user.

**Adds**:

- Web UI for all functions (upload, query, curation)
- User authentication
- Supplementary context — attach human notes to documents the system cannot interpret automatically
- Reprocess documents after human correction
- Return original documents alongside query answers
- Browse documents directly
- Family Member access

### Phase 3 — Open to Others

Hosted infrastructure, external user access, access controls.

**Adds**:

- User account management
- Replace or delete documents
- Occasional Contributor access (submit and query)
- Document visibility scoping by user type
- Filter and facet search
- System Administrator role (separated from Primary Archivist)

### Phase 4 and Beyond

Deferred without a committed phase: standalone photographs, near-duplicate detection, knowledge graph, cross-document contradiction detection.

---

## What Questions the System Answers

The system is designed to answer questions about the estate's recorded history:

- **Land and ownership**: "What is known about ownership of the north field?"
- **Infrastructure and works**: "Where were pipes laid through the east meadow, and when?"
- **Rights and agreements**: "Is there any record of a right of way agreement with the neighbouring landowner?"
- **People and relationships**: "Who was involved in the sale of the mill pasture?"
- **Decisions**: "What decisions were made about the purchase or sale of certain plots?"
- **Time period**: "What was happening with the estate in the 1960s?"

The system surfaces what documents say. It does not give legal advice or interpretation. Answers always include citations so users can verify against the originals. If no relevant documents exist, the system says so.

The practical quality of answers is directly proportional to the breadth and quality of documents in the archive.

---

## What the System Does Not Do

- Provide public or anonymous access
- Allow self-registration
- Give legal advice or interpret legal documents
- Answer questions about land or property outside the estate
- Process audio, video, structured data files, or web content
- Handle document scanning — digitisation is a precondition to submission

---

## Navigation

| If you want to... | Go to... |
| --- | --- |
| Understand the system architecture and technology choices | [project/architecture.md](architecture.md) |
| Understand the developer background and environment setup | [project/developer-context.md](developer-context.md) |
| See the pipeline visually | [project/pipeline-diagram.mermaid](pipeline-diagram.mermaid) |
| Understand a specific component | [components/](../components/) |
| Understand why decisions were made | [decisions/architecture-decisions.md](../decisions/architecture-decisions.md) |
| See what questions are still open | [decisions/unresolved-questions.md](../decisions/unresolved-questions.md) |
| Set up agents and skills | [SUMMARY.md](../SUMMARY.md) |
