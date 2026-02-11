# Phases and Priorities

This document summarises what is in scope for each phase of the project. It is a consolidation of decisions made across the other scope documents, not a source of new decisions.

---

## Phase 1 — Prove the Pipeline

**Goal**: A working end-to-end system that can ingest documents, extract and embed their content, and answer natural language questions with citations. Used by one person, running locally. Document upload is via a minimal web UI; query and curation are via command line.

**Users**: Primary Archivist only.

**Document types**: Typewritten documents, printed modern documents (PDFs, correspondence, financial documents).

**Scale**: ~20 documents initially, enough to validate the pipeline on real material.

**Capabilities**:

- Upload a single document via web UI
- Bulk ingestion from a directory, driven by an external agent or tool via CLI
- Exact duplicate detection and rejection
- Text extraction with quality scoring
- Automatic detection of document type, dates, people, and land references
- Flagging of poor-quality extractions for human review
- AI-agent-defined embeddings for each document chunk
- Domain vocabulary maintenance (add, edit, approve terms) via CLI
- Flagging of new domain vocabulary candidates from documents
- Natural language query with synthesised answer and source citations via CLI
- Mark documents as reviewed or needing attention via CLI
- Correct document metadata via CLI
- View processing queue and status via CLI
- Resubmit failed documents via CLI
- Provider-agnostic configuration (storage, OCR, LLM, embeddings)

**Out of scope for Phase 1**: web UI for query, curation, or administration; user authentication; browsing and filtering documents; supplementary context; viewing original documents alongside query results; replace/delete documents; multi-user access.

---

## Phase 2 — Expand and Share

**Goal**: Extend the archive to harder document types, introduce a full web interface for all functions, and bring in the first external user (Family Member) for feedback and collaborative curation.

**Users**: Primary Archivist, Family Member.

**New document types**: Handwritten letters and notes, maps and plans, raw emails.

**New capabilities**:

- Web UI for all archival, curation, and query functions
- User authentication
- Supplementary context — attach human notes to documents the system cannot interpret fully (particularly valuable for handwritten documents and maps)
- Reprocess a document after human correction or supplementary context is added
- Return original document alongside query answers
- Browse documents directly (not only via query)
- Bulk import via web UI
- System health monitoring

**Still out of scope**: replace/delete documents, filter and facet search, user account management, document scoping by user type, external contributors.

---

## Phase 3 — Open to Others

**Goal**: Make the system safely accessible to people outside the immediate family, with appropriate controls. Move from local infrastructure to hosted environment.

**Users**: Primary Archivist, Family Member, Occasional Contributor (solicitors, accountants, estate managers), System Administrator (separated from Primary Archivist role).

**New capabilities**:

- User account management
- Replace an existing document with a better version
- Delete a document with confirmation
- Restrict which documents are visible to which user types
- Filter and facet search results
- Occasional Contributor access: submit documents and query the archive
- Scoped query access (which users can see which documents) — approach to be defined at this phase

**Infrastructure**: move from local Docker to hosted environment; System Administrator role becomes distinct from Primary Archivist.

---

## Phase 4 and Beyond

Capabilities explicitly deferred without a committed phase:

- Standalone photograph handling
- Near-duplicate document detection (same content, different scans)
- Aggregated and analytical queries across the full archive (possible earlier but only useful at scale)
- Knowledge graph of entities and relationships
- Cross-document contradiction detection
- Audio and video recordings — out of scope indefinitely unless relevant material emerges

---

## What Never Changes

These constraints apply across all phases:

- The system is private — no public access at any phase
- No self-registration — users are managed by the Primary Archivist
- The system surfaces what documents say; it does not give legal advice or interpretation
- Answers always include source citations
- The design must not prevent document-level access scoping from being added in Phase 3 without significant rework
