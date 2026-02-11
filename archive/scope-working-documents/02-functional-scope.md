# Functional Scope

This document defines what the system must do, grouped by capability area. Each item is tagged by phase and priority:

- **Must have** — required for the phase to be considered complete
- **Nice to have** — valuable but not blocking; added when capacity allows
- **Later** — explicitly deferred

---

## Document Submission

The system must accept documents and record them in the archive.

| Capability | Priority | Phase |
| --- | --- | --- |
| Upload a single document (PDF, image) | Must have | 1 |
| Detect and reject exact duplicate submissions | Must have | 1 |
| Capture basic metadata at submission (filename, date submitted) | Must have | 1 |
| Support bulk ingestion from a directory, driven by an external agent or tool, without requiring manual upload of each document | Must have | 1 |
| Allow submitter to provide a brief note about the document at upload time | Nice to have | 2 |
| Replace an existing document with a better version (supersede) | Must have | 3 |
| Delete a document with confirmation | Must have | 3 |

---

## Document Processing

Once submitted, the system must extract usable text and assess quality.

| Capability | Priority | Phase |
| --- | --- | --- |
| Extract text from typed and printed documents | Must have | 1 |
| Extract text from handwritten documents (best effort) | Must have | 1 |
| Assign a quality score to each extracted document | Must have | 1 |
| Flag documents where extraction quality is poor, for human review | Must have | 1 |
| Handle documents where text extraction fails entirely | Must have | 1 |
| Detect document type automatically (letter, legal doc, map, etc.) | Must have | 1 |
| Detect and extract dates mentioned in the document | Must have | 1 |
| Detect and extract names of people, places, and land references | Must have | 1 |
| Reprocess a document after a human has corrected or supplemented it | Must have | 2 |

---

## Knowledge Organisation

The system must build a searchable knowledge base from processed documents.

Embeddings are produced using an AI agent that analyses document context to determine the most meaningful representation — this is slower than mechanical chunking but produces richer, more accurate retrieval results.

| Capability | Priority | Phase |
| --- | --- | --- |
| Split documents into semantically coherent chunks | Must have | 1 |
| Generate and store AI-agent-defined embeddings for each chunk | Must have | 1 |
| Maintain a domain vocabulary of estate-specific terms (field names, people, infrastructure) | Must have | 1 |
| Flag new terms encountered in documents as candidates for the domain vocabulary | Must have | 1 |
| Allow authorised users to add, edit, and approve domain vocabulary entries | Must have | 1 |
| Automatically apply domain vocabulary to improve retrieval | Nice to have | 2 |
| Detect near-duplicate documents (same content, different scans) | Later | 3 |

---

## Search and Retrieval

The system must answer natural language questions about the archive.

| Capability | Priority | Phase |
| --- | --- | --- |
| Accept a natural language question and return an answer | Must have | 1 |
| Cite the source documents used to construct an answer | Must have | 1 |
| Return the relevant original document alongside an answer | Must have | 2 |
| Browse documents directly (not via query) | Must have | 2 |
| Filter results by date range, document type, or land reference | Nice to have | 3 |
| Surface related documents alongside a query result | Nice to have | 3 |

---

## Curation and Maintenance

The system must support ongoing quality improvement of the archive.

| Capability | Priority | Phase |
| --- | --- | --- |
| Mark a document as reviewed and verified | Must have | 1 |
| Flag a document as needing attention | Must have | 1 |
| Correct metadata on a document after processing | Must have | 1 |
| View a queue of documents that need review or have processing issues | Must have | 1 |
| Add supplementary context to a document (notes, clarifications for things the system could not extract) | Must have | 2 |

---

## Administration

The system must be manageable by whoever is responsible for running it.

| Capability | Priority | Phase |
| --- | --- | --- |
| View processing status of submitted documents | Must have | 1 |
| Resubmit a document that failed processing | Must have | 1 |
| Change the storage or processing provider via configuration | Must have | 1 |
| Monitor system health | Nice to have | 2 |
| Bulk import of a large document set via the UI | Nice to have | 2 |
| Manage user accounts | Must have | 3 |
| Restrict which documents are visible to which user types | Must have | 3 |

---

## Design Constraints

The following are not capabilities but requirements that constrain how capabilities must be designed:

- The system must not prevent document-level access scoping from being added in Phase 3 without significant rework. This means document ownership and visibility fields should be included in the data model from Phase 1, even if unused.
- Bulk ingestion must be possible without a web UI — an agent or script must be able to drive it programmatically.
