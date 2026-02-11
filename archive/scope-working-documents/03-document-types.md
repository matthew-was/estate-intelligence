# Document Types

This document defines what kinds of documents the archive contains, their characteristics, and what the system must handle by phase. This informs processing scope and user stories.

---

## Phase 1 Document Types

These are the document types the system must handle in Phase 1. They represent the most tractable material and are used to prove the pipeline before tackling harder types.

### Typewritten and Printed Documents

Typed or printed text, scanned to image or PDF. Includes legal correspondence, solicitor letters, tenancy agreements, land registry documents, formal notices, and official forms.

- Generally high text quality when scanned at reasonable resolution
- May include signatures, stamps, or handwritten annotations alongside typed content — annotations should be flagged for human review, not silently ignored
- The primary Phase 1 document type

### Printed Modern Documents

Born-digital documents printed and scanned, or received as PDFs. Includes modern correspondence, reports, financial documents, invoices, and official forms from the last 30 years.

- High extraction quality expected
- May be multi-page
- Financial documents (invoices, accounts) have sufficient surrounding context (parties, dates, descriptions) to be processed as ordinary documents — no special tabular handling required
- Some may be email printouts (email-as-document, not raw email format — those are handled separately in Phase 2)

---

## Phase 2 Document Types

These require additional processing capability or handling beyond the Phase 1 pipeline.

### Handwritten Letters and Notes

Personal correspondence, farm diaries, informal notes, and memoranda written by hand. Spanning 1950s to present.

- Highly variable legibility — older handwriting, faded ink, deteriorated paper
- Extraction quality will often be low; quality scoring and human review flagging are critical
- Context is frequently implicit — references to people and places by nickname or informal name
- Supplementary context (Phase 2) is particularly valuable for this type

### Maps, Plans, and Surveys

Hand-drawn or printed maps of the estate, field boundary surveys, drainage plans, building plans, and infrastructure layouts.

- Minimal or no extractable text in standalone maps
- Spatial relationships and annotations are the primary content
- Treated as a single visual chunk with separate metadata
- Human supplementary context is the primary mechanism for making standalone maps searchable
- Scale, orientation, and approximate date should be captured as metadata where legible
- Maps and plans embedded within larger documents (reports, surveys) are handled as part of that document — the surrounding text provides context

### Emails (Raw Format)

Email correspondence received or exported in digital format.

- Distinct from email printouts, which are handled as printed documents
- Each message in a thread is treated as a separate document
- Headers (sender, recipient, date, subject) are structured metadata, not just body text
- Attachments that are themselves documents require separate processing

---

## Phase 3+ Document Types

These are explicitly deferred. The data model must not actively prevent them from being added later.

### Standalone Photographs

Physical photographs scanned to image, or digital photographs with no accompanying text document.

- No extractable text in most cases
- Human supplementary context would be the sole mechanism for making these searchable
- Photographs embedded within reports or surveys are not affected by this deferral — they are part of the containing document
- Deferred because processing approach and value relative to effort need more consideration

---

## Explicitly Out of Scope

- **Audio and video recordings** — no audio or video material currently exists in the archive; may be reconsidered in a future phase if relevant material emerges
- **Structured data files** (spreadsheets, databases, CSV exports) — these require a fundamentally different processing approach and are not present in the current archive
- **Social media content**
- **Web page captures or web archives**

---

## Notes on Digitisation

The system does not handle scanning. Physical documents must be digitised (scanned to PDF or image file) before submission. Digitisation is a precondition to submission, not a system responsibility.
