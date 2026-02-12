# Project Overview

## Why This Project Exists

The Estate Intelligence system exists to preserve and make accessible the recorded history of a family farming estate spanning from the 1950s to the present. Decades of land transactions, infrastructure works, tenancy agreements, legal correspondence, and family history exist only as physical and digital documents — scattered, unsearchable, and at risk of being lost as knowledge passes between generations.

The system creates a searchable archive of these documents. A user asks a question in plain language — "what is known about the drainage works in the east meadow?" or "who owned the mill pasture before the family acquired it?" — and the system reads the relevant documents and answers directly, citing its sources.

This project also serves as a deliberate learning vehicle. The developer is using a real, meaningful problem to build practical expertise in AI and document processing. Design decisions throughout favour understanding over convenience.

---

## Who the System Is For

| User | Phase | Description |
| --- | --- | --- |
| Primary Archivist | 1 | Builds and maintains the archive; has all capabilities available in each phase |
| Family Member | 2 | Full archival and curation access; no document deletion |
| Occasional Contributor | 3 | Queries the archive; may submit documents; no curation access |
| System Administrator | 3 | Manages infrastructure and user accounts; separated from the Archivist role |

The system is private at all phases. There is no public access and no self-registration.

In Phase 1 there is a single user and no authentication — the Primary Archivist is the system. The System Administrator role is introduced in Phase 3, when infrastructure and user account management are separated from the Archivist's responsibilities.

---

## What Documents the System Handles

| Document Type | Phase |
| --- | --- |
| Typewritten and printed documents (scanned) | 1 |
| Modern digital PDFs, correspondence, financial documents | 1 |
| Handwritten letters and notes | 2 |
| Maps, plans, and surveys | 2 |
| Emails (raw format) | 2 |
| Standalone photographs | Deferred / future phase |

Accepted file formats by phase:

| Format | Phase |
| --- | --- |
| PDF | 1 |
| TIFF | 1 |
| JPEG | 1 |
| PNG | 1 |
| DOCX | 2 |
| EML | 2 |

Audio, video, structured data files, and web content are out of scope. Physical documents must be digitised before submission — scanning is not a system responsibility.

---

## What the System Must Do

### Phase 1 — Prove the Pipeline

A complete end-to-end pipeline running locally, used by one person. Document upload via a simple web form; query and curation via command line. The web form is unpolished but functional. The CLI is a developer-facing tool: functional and minimally documented, but not required to be a polished user interface. The web UI is the intended primary interface in later phases.

Files submitted via the web UI or bulk ingestion must follow a structured naming convention: `YYYY-MM-DD - short description` (for example, `1962-08-20 - letter from estate manager about updates`). For web UI uploads, the filename is parsed on selection and matching fields are auto-populated in the upload form; the convention is optional and any filename is accepted. For bulk ingestion, the convention is required — files that do not conform are rejected and the reason is included in the summary report.

**Must have**:

- Accept document uploads via web UI; bulk ingestion from a directory via on-demand CLI command (watched directory is out of scope at all phases); bulk ingestion and document processing are separate steps — ingestion stores files, processing runs independently
- Produce a bulk ingestion summary report after each run: a summary header (total submitted, accepted, rejected) followed by a per-file record of filename, outcome, and rejection reason where applicable; printed to stdout and written to a timestamped file in a configurable output directory
- Detect and reject exact duplicate files by file hash; hash-based duplicate detection applies to individual files regardless of whether they are submitted standalone or as part of a virtual document group; content-based duplicate detection (rescanned copies of the same document) is deferred to a future phase (duplicate detection behaviour for inline email attachments such as signature images is an open question deferred to Phase 2 scope)
- Enforce a configurable maximum file size per file; the limit applies to each individual file in a submission, including files within a virtual document group
- Support grouping multiple files into a single virtual document at submission time; multi-part scanned documents (e.g. a multi-page deed scanned as separate image files) are submitted and processed as one logical unit and referenced as such in query results; if any file in a group fails intake validation, the entire group is rejected — no partial groups are stored; the rejection report identifies which file failed and the reason
- Extract text from typed and printed documents; produce a quality score per page and for the document as a whole, representing confidence that the extracted text is a faithful and complete representation of the document content; scores are in the range 0–100
- Flag poor-quality extractions for human review; documents scoring below a configurable threshold on any page or overall, documents that produce no extractable text, or documents where only some pages yield text (partial extraction) are stored and flagged for manual review rather than rejected (they may be plans, maps, or images requiring manual data entry)
- Reject files that cannot be opened or parsed at intake (including empty or zero-byte files), or that do not conform to the required filename convention (bulk ingestion only); rejected files are not stored
- Detect document type, dates, people, and land references automatically; metadata completeness contributes to the overall quality score — a document with extractable text but no detectable metadata will score lower and may fall below the review threshold; partial detection (some fields found, others not) is not itself a flag trigger
- Generate embeddings for each document chunk; chunk boundaries are determined by an AI agent that reads the document content and identifies semantically meaningful units, rather than by fixed-size splitting — ensuring that related content (a clause, a paragraph, a named transaction) is kept together in a single embedding
- Maintain a domain vocabulary of estate-specific terms (field names, people, organisations, recurring legal phrases, and similar estate-specific language); the vocabulary is seeded by the archivist before first use and can be extended manually via CLI at any time; during document processing, candidate terms are proposed automatically and surfaced in the curation queue; candidates are deduplicated against both the accepted vocabulary and a persisted rejected-terms list before being raised, so nothing is proposed more than once; the curator accepts (adds to vocabulary) or rejects (adds to rejected list) each candidate
- Answer natural language questions with synthesised responses and source citations (CLI); each citation includes the document title, date, and a human-readable archive reference; page-level citation is deferred to a later phase
- Basic curation via CLI: view the processing queue (documents awaiting review or flagged with issues); clear flags to resume pipeline processing from the next incomplete step; correct document metadata (type, date, people, land references, title); flag documents with a typed status and a free-text reason

**Out of scope for Phase 1**: web UI for query, curation, or administration; user authentication; supplementary context; browsing documents; viewing originals in results; replace or delete documents; multi-user access; curation by anyone other than the Primary Archivist.

There is no in-application mechanism to remove erroneously submitted documents in Phase 1 or Phase 2. The Primary Archivist has direct access to the underlying system and can remove documents out-of-band. Document deletion as a managed application feature is deferred to Phase 3.

**Design constraints**:

- Provider-agnostic configuration throughout: every external service (storage, database, OCR, embedding, LLM) is abstracted via an interface; concrete implementations are selected at runtime via configuration with no hardcoded providers
- Submitter identity is recorded on every document from Phase 1; in Phase 1 this field is always the Primary Archivist, but the field must exist in the data model to support multi-user phases without schema changes; curators can see who submitted a document when reviewing the queue

### Phase 2 — Expand and Share

Harder document types, full web interface, first external user.

**Adds**:

- Web UI for all functions (upload, query, curation)
- User authentication
- Supplementary context — attach human-provided text to documents the system cannot interpret automatically (e.g. no extractable text); this allows flagged documents to progress through the pipeline
- Reprocess documents after human correction or supplementary context is added
- Return original documents alongside query answers
- Browse documents directly
- Family Member access — can curate any document in the archive (not only their own submissions), to share the load of reviewing system-flagged documents; same curation access as the Primary Archivist except no document deletion

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
- Answer questions about topics with no relevant estate documents — responses are based on available sources only. References to adjacent landowners or outside parties may appear in answers where they are mentioned in estate documents
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
