# Overview Review

## Contradictions

- **Phase 1 supplementary information vs. out of scope**: The Phase 1 description states the web form "allows supplementary information to be provided at upload time". The out-of-scope list for Phase 1 explicitly includes "supplementary context". These two statements conflict. If supplementary information can be entered at upload time in Phase 1, it must be defined as in scope; if it cannot, the web form description is misleading.

- **Primary Archivist full access vs. progressive enablement**: The user table states the Primary Archivist has "full access including system administration" from Phase 1. The explanatory paragraph then states that "full access (including administration) is only fully realised at Phase 3". This is contradictory — a reader writing Phase 1 requirements cannot tell whether system administration is in scope for Phase 1 or not.

## Missing information

- **What "curation" means in practice**: The Phase 1 must-have list includes "basic curation via CLI: mark reviewed, flag issues, correct metadata, view and resubmit processing queue". The scope of each of these operations is not defined. For example: which metadata fields can be corrected? What does "flag issues" produce — a status change, a notification, an entry in a log? What does "resubmit processing queue" mean — re-run extraction, re-run embedding, or the full pipeline?

- **Quality scoring definition**: The document requires "quality scoring" for text extraction but does not define what quality means, what the scale is, or what threshold triggers a flag for human review. This is needed to write acceptance criteria.

- **Domain vocabulary scope**: The document requires maintaining a domain vocabulary of estate-specific terms. It does not state who seeds the initial vocabulary, what a "term" is (a word, a phrase, a named entity), how terms are proposed (automatically during processing, manually), or how a curator approves or rejects a proposed term.

- **Bulk ingestion summary report**: The report format and delivery mechanism are not defined. Is it written to a file, printed to stdout, or both? What fields does it contain beyond "rejection reason"? Does it report successful ingestions as well as rejections?

- **"Virtual document" behaviour**: Multi-file grouping into a virtual document is required, but the document does not state how the virtual document is referenced in query results (as one unit or by constituent file), how it is stored, or what happens if one file in the group fails intake.

- **File format scope**: The document types table describes content categories (typewritten, handwritten, emails) but does not specify accepted file formats (PDF, JPEG, TIFF, EML, etc.). This is needed at intake to define validation rules.

- **Query result format**: The document states answers include "source citations" but does not define what a citation contains — document title, date, page number, a file reference, or something else. This affects both Phase 1 CLI and Phase 2 UI requirements.

## Undocumented edge cases

- **Partial group failure at bulk ingestion**: If a multi-file virtual document is submitted via bulk ingestion and one file is unparseable, the document does not state whether the whole group is rejected, the parseable files are stored individually, or the group is stored with a flag.

- **Reprocessing after manual data entry**: Documents flagged for manual review (no extractable text) can presumably have data entered later. The document does not state how manual data is submitted or what triggers re-embedding after manual entry. Phase 2 mentions "reprocess documents after human correction" but the Phase 1 flag-for-review requirement implies some form of queue management is already needed in Phase 1.

- **Duplicate detection across virtual documents**: If a file submitted as part of a virtual document was previously submitted as a standalone file (or vice versa), the hash-based duplicate check may or may not catch it depending on implementation. The scope does not address this.

- **Maximum file size for grouped submissions**: The configurable file size limit is described per submission. It is unclear whether this applies per individual file or per group total when multiple files are grouped into a virtual document.

- **Empty or zero-byte files**: Not addressed. These would be parseable by a file reader but contain no content — distinct from a file that cannot be opened.

- **Metadata detection confidence**: The document states documents with no detectable metadata are stored and flagged. It does not address partial detection (e.g. date detected but no people or land references) — whether partial detection is treated as success or triggers a flag.

## Ambiguities

- **"Supplementary information" vs. "supplementary context"**: Two different terms appear to refer to the same concept (human-provided notes about a document). The Phase 1 web form description uses "supplementary information"; the Phase 2 adds list uses "supplementary context". If these are the same thing, one is in scope for Phase 1 (contradicting the out-of-scope list) or neither is. If they are different things, the distinction is not explained.

- **"AI-agent-defined embeddings"**: The document requires embeddings to be "AI-agent-defined" rather than mechanical chunking. It is not stated what this means in terms of system behaviour — whether an AI agent decides chunk boundaries, selects which content to embed, or something else. This phrase will need clarification before the Head of Development can make architectural decisions.

- **"Provider-agnostic configuration throughout"**: This is listed as a Phase 1 must-have but is not defined in behavioural terms. It implies an architectural pattern but does not state what the system must do to satisfy it. This is an architectural concern rather than a functional requirement and may be better placed in a design constraints section.

- **Family Member curation scope (Phase 2)**: The document states Family Members can "curate any document in the archive (not only their own submissions)". This implies Occasional Contributors (Phase 3) can only curate their own submissions. But the Occasional Contributor description says "no post-submission control". It is unclear whether this means no curation at all, or only self-curation — and whether curation access for each role is intentionally asymmetric.

- **"Replace or delete documents" deferred to Phase 3**: The Phase 1 out-of-scope list includes "replace or delete documents". Phase 3 adds this capability. However, the document does not state what happens in Phase 1 or Phase 2 if a document is submitted in error — whether it persists permanently until Phase 3, or whether the Primary Archivist has some out-of-band removal mechanism.
