# Overview Review

_Review date: 2026-02-13_
_Basis: `documentation/project/overview.md` only — no other sources consulted._

## Contradictions

- None identified.

## Missing information

1. **Metadata correction scope — which fields are correctable in Phase 1.**
   The curation section states that metadata correction covers "type, date, people, land references,
   description". The automatic detection section states the system detects "document type, dates,
   people, and land references". Description is included in the correctable fields but is not listed
   as an automatically detected field. It is unclear whether description is a user-supplied field
   only (set at intake), a system-detected field, or both. This affects what the curation queue
   displays and what the correction form must support. Clarification is needed before requirements
   for the correction UI can be written completely.

2. **Vocabulary candidate tie-break ordering stated twice, inconsistently.**
   The vocabulary section states candidates are ordered "by the timestamp of the step completion
   that raised the candidate". The curation section repeats this wording. Both uses are consistent.
   No issue. _(Self-resolved during review — included for completeness, no action needed.)_

3. **Bulk ingestion: atomic rollback mechanism unspecified for the "cleanup at run start" case.**
   The document states cleanup of any incomplete prior run occurs at the start of every ingestion
   run. It does not state what "incomplete prior run" means in terms of detectable state — i.e.
   how the system knows a prior run was interrupted vs. completed cleanly. This is likely an
   architectural detail, but if no state marker is written, cleanup cannot be triggered correctly.
   This may be appropriate to defer to architecture, but requirements should state that the system
   must be able to distinguish interrupted from completed runs — if that is the intent.

## Undocumented edge cases

1. **Vocabulary candidate raised from a document that is subsequently deleted out-of-band.**
   The overview states that accepted vocabulary terms are independent of source documents and are
   unaffected by out-of-band document removal. It also states that candidates remain in the review
   queue regardless of the source document's subsequent flag state. However, it does not address
   what happens to a _pending_ (unreviewed) candidate when its source document is removed out-of-band
   in Phase 1. The candidate may reference a document the system no longer holds. Does the candidate
   remain in the queue? Is the source document reference simply broken? This is a Phase 1 edge
   case because out-of-band deletion is the only deletion mechanism available in Phase 1 and Phase 2.

2. **What happens when the bulk ingestion output directory cannot be created.**
   The overview states the output directory is created automatically if it does not exist. It does
   not address the case where directory creation fails (e.g. insufficient permissions). Requirements
   should specify the failure behaviour — error and abort, or continue without writing the file.

3. **Concurrent ingestion runs.**
   Phase 1 is described as single-browser-session only for the web UI. No equivalent constraint
   is stated for the CLI. It is not stated whether two simultaneous bulk ingestion runs are possible
   and, if so, how conflicts (e.g. duplicate detection race conditions, atomic rollback) are handled.
   If concurrent runs are not supported, this should be stated explicitly so requirements do not
   inadvertently rely on it.

4. **Web UI behaviour when the server is unavailable mid-session.**
   Phase 1 is single-browser-session only. No guidance is given on what happens if the server
   becomes unavailable during a submission (e.g. part-way through an upload). This may be
   acceptable to leave to implementation, but if the requirement is that "no partial submissions
   are stored", the atomicity guarantee for web UI uploads should be stated.

## Ambiguities

1. **"The web UI is the intended primary interface and will be enhanced in Phase 2" (Phase 1 section).**
   The same paragraph describes query as CLI-only in Phase 1. This creates a possible reading that
   "primary interface" refers only to intake and curation, not to query. The statement is
   technically accurate but could be read as implying the web UI will eventually replace the CLI
   for all functions including query. Given that the CLI is described as a "developer-facing tool"
   throughout, it may be worth clarifying whether the CLI remains permanently available for query
   in Phase 2 and beyond, or whether it is deprecated in favour of the web UI for query by Phase 2.
   This affects Phase 2 scope requirements.

2. **Archive reference derivation — "derived from the document's curated metadata at the time of display".**
   The overview states the archive reference is derived from curated metadata at display time and
   is mutable. It does not specify which metadata fields contribute to the reference or the
   derivation format. This is described as deferred to architecture, which is appropriate —
   but requirements should explicitly flag that the derivation rule is an architectural output,
   so the requirements document does not inadvertently imply a fixed format.
