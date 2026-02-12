# Overview Review

## Contradictions

- **Phase 4 document type vs phase table**: The document type table lists "Standalone photographs" as Phase 4+, but the phase table in "What the System Must Do" only covers Phases 1–3 with Phase 4 described as "deferred without a committed phase". The notation "4+" in the document type table implies a defined Phase 4, which does not exist elsewhere in the document.

- **Primary Archivist description vs Phase 1 scope**: The user table describes the Primary Archivist as having "full access including system administration". The Phase 1 scope explicitly defers user authentication and states administration is out of scope for Phase 1. It is unclear whether the Primary Archivist role is defined at Phase 1 or only becomes meaningful at Phase 3 when a System Administrator is introduced.

## Missing Information

- **What constitutes a "document chunk"**: The overview references "AI-agent-defined embeddings for each document chunk" but does not define what a chunk is or what scope "AI-agent-defined" means in practice. This is significant for writing requirements around the processing pipeline.

- **Definition of "exact duplicate"**: The system must detect and reject exact duplicates, but the overview does not define how a duplicate is identified — by file hash, content, filename, or a combination. Without this, the rejection requirement cannot be fully specified.

- **Poor-quality extraction threshold**: The overview states the system must "flag poor-quality extractions for human review" but does not define what constitutes poor quality, how quality is measured, or what the flagging workflow looks like.

- **Source citation format**: The overview states "answers always include citations so users can verify against the originals" but does not define what a citation must contain — document title, page, date, identifier, or a link to the original file.

- **Processing queue definition**: The Phase 1 CLI curation requirement includes "view and resubmit processing queue" but the overview does not describe the lifecycle of the processing queue — what states a document can be in, what triggers resubmission, or what resubmission does.

- **Bulk ingestion scope for Phase 1**: The overview states "bulk ingestion from a directory via CLI" as a Phase 1 must-have but does not define whether this is a one-time import, an ongoing watched directory, or an on-demand command. This affects requirements significantly.

- **Supplementary context definition (Phase 2)**: "Attach human notes to documents the system cannot interpret automatically" does not define whether these notes are searchable, whether they affect query answers, or how they relate to the document's embeddings.

- **Document visibility scoping (Phase 3)**: The overview mentions "document visibility scoping by user type" but gives no rules for how visibility is assigned, who assigns it, or what the default visibility of a document is at upload time.

- **No definition of "reprocess" (Phase 2)**: "Reprocess documents after human correction" does not define what triggers reprocessing, what parts of the pipeline are re-run, or whether old embeddings are replaced or versioned.

## Undocumented Edge Cases

- **Document fails text extraction entirely**: The overview describes flagging poor-quality extractions but does not address what happens when a document produces no extractable text at all — whether it is stored, rejected, or held pending manual input.

- **Duplicate submission during bulk ingestion**: It is unspecified whether duplicate detection during bulk CLI ingestion behaves the same as via web UI upload, and whether the user is notified per-document or with a summary report.

- **Document submitted with no detectable metadata**: Automatic detection of type, dates, people, and land references is required. It is unspecified what happens when none of these can be detected — whether the document is accepted, flagged, or requires manual metadata entry before acceptance.

- **Large or multi-part documents**: The overview does not address whether there is a maximum file size, or how multi-part scanned documents (e.g. a 50-page land deed scanned as separate image files) are handled — as separate documents or as one.

- **Partially digitised documents**: A physical document scanned with mixed readable and unreadable pages is not addressed. It is unclear whether partial extraction is acceptable or whether the document must be fully re-scanned.

- **Corrupted or unreadable file formats**: The overview does not describe what happens when a submitted file cannot be opened or parsed — whether it is rejected at intake, quarantined, or stored without processing.

- **Domain vocabulary conflicts**: The overview requires maintaining a domain vocabulary and flagging new candidates from documents. It does not address what happens when a flagged term conflicts with or duplicates an existing term, or who resolves the conflict.

## Ambiguities

- **"Provider-agnostic configuration throughout"**: This is listed as a Phase 1 must-have but is not defined as a user-facing requirement — it reads as an architectural constraint. It is ambiguous whether this belongs in user requirements or in a system design constraint. Leaving it in the must-have list risks embedding an architectural assumption. `[ARCHITECTURAL FLAG — for Head of Development]`

- **"Agentic embeddings"**: The phrasing "AI-agent-defined embeddings" appears in the must-have list without definition. It is ambiguous whether this refers to a specific architectural pattern, a product behaviour, or a design constraint. If it is a design constraint rather than a user-facing requirement, it should be separated accordingly. `[ARCHITECTURAL FLAG — for Head of Development]`

- **CLI scope for Phase 1**: The overview states "query and curation via command line" but it is ambiguous whether the CLI is an internal developer tool (not user-facing) or the primary interface for the Primary Archivist in Phase 1. This changes who the user of the CLI is and how it should be specified.

- **"Minimal web UI" for Phase 1 upload**: It is not defined what "minimal" means — whether it is a file picker with no metadata entry, or a form with required fields. This affects what the upload interface must do.

- **Family Member access in Phase 2**: The user table says Family Member has "full archival and curation access; no system administration or document deletion". The Phase 2 additions list does not specify which curation actions Family Members can perform relative to the Primary Archivist, or whether they can edit metadata on documents they did not submit.

- **"Answer questions about land or property outside the estate"**: Listed under "What the System Does Not Do". It is ambiguous whether this means the system must refuse such questions, or that it simply will not have source documents to draw on. These have different implications — one is a system behaviour requirement, the other is a data scope statement.

---

## Decisions Made

All scope-level items were resolved in conversation with the developer and applied to `documentation/project/overview.md`. Items flagged for the Head of Development remain open in `decisions/unresolved-questions.md`.

### Resolved in overview.md

| Item | Decision |
| --- | --- |
| Phase 4 notation ("4+") | Changed to "Deferred / future phase" |
| Primary Archivist "full access" vs Phase 1 scope | Added clarifying note: role capabilities are progressively enabled; full access only realised at Phase 3 |
| CLI scope | Developer-facing tool with basic usability; not a polished user interface; web UI is the intended primary interface |
| "Minimal web UI" | Minimal means unpolished, not stripped of function; simple upload form allowing supplementary input |
| Family Member curation permissions | Can curate any document in the archive (not only own submissions); same as Primary Archivist except no deletion |
| "Answer questions outside the estate" | Reframed as data coverage statement; system responds based on available sources only; outside-party references may appear where mentioned in estate documents |
| Definition of "exact duplicate" | Phase 1: file hash only; content-based detection deferred to future phase |
| Bulk ingestion scope | On-demand CLI command; watched directory is out of scope at all phases |
| Document fails text extraction entirely | Store and flag for manual review; not rejected |
| No metadata auto-detected | Store and flag for review |
| Large/multi-part documents | Configurable maximum file size; multi-part files can be grouped into a single virtual document at submission |
| Duplicate detection during bulk ingestion | Reject and continue; summary report produced at end of run listing all rejections with reasons |
| Partially digitised documents | Store with partial extraction and flag for review |
| Corrupted or unreadable file formats | Reject at intake, not stored; reason included in summary report |
| Domain vocabulary conflicts | System deduplicates before flagging; only genuinely new candidates raised; resolution handled through normal curation workflow |

### Deferred to Head of Development

| Item | Reason |
| --- | --- |
| "Provider-agnostic configuration throughout" | Architectural constraint, not a user-facing requirement |
| "AI-agent-defined embeddings" | Architectural pattern vs product behaviour — needs classification |
| What constitutes a "document chunk" | Implementation detail |
| Poor-quality extraction threshold | Implementation detail |
| Source citation format | Implementation detail |
| Processing queue lifecycle | Implementation detail |
| Supplementary context searchability (Phase 2) | Implementation detail |
| Definition of "reprocess" (Phase 2) | Implementation detail |
| Document visibility rules (Phase 3) | Implementation detail |
