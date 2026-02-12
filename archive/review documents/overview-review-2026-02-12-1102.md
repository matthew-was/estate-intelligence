# Overview Review

## Contradictions

- **Phase 1 upload interface vs. CLI-only query**: The overview states the web form is "unpolished but
  functional" and is "the intended primary interface in later phases", while also stating that Phase 1
  query and curation are CLI-only. This is consistent, but Phase 2 says "Web UI for all functions
  (upload, query, curation)" — implying Phase 1 already has a web UI for upload but not for query or
  curation. This is not a contradiction, but the asymmetry (web UI for intake, CLI for everything
  else in Phase 1) should be confirmed as intentional.

- **No deletion in Phase 1 and Phase 2, then deletion in Phase 3**: The overview states "There is no
  in-application mechanism to remove erroneously submitted documents in Phase 1 or Phase 2." Phase 3
  adds "Replace or delete documents." The out-of-scope list for Phase 1 includes "replace or delete
  documents", but Phase 2 does not explicitly include deletion in its out-of-scope list, nor does it
  explicitly re-state that deletion remains out of scope in Phase 2. The body text handles this, but
  it could be read ambiguously when comparing the Phase 2 "Adds" list against the Phase 3 list.

## Missing information

- **What "searchable" means for flagged documents**: A document flagged for review is stored but not
  described as searchable or unsearchable. It is unclear whether flagged documents appear in query
  results while awaiting review, or whether they are excluded until a curator clears the flag. This
  affects requirements for both the query pipeline and the curation queue.

- **Behaviour after a curator clears a flag**: The overview says curators can "clear flags to resume
  pipeline processing from the next incomplete step", but does not say what the next incomplete step
  is in practice, or what happens if processing subsequently fails again (e.g. re-extracted text
  still scores below threshold).

- **Domain vocabulary seeding mechanism**: The vocabulary "is seeded by the archivist before first
  use" — but no mechanism is described. It is unclear whether seeding is done via CLI, a config
  file, a data import, or another method. This is needed to write a complete intake requirement for
  vocabulary setup.

- **What a "citation" contains for CLI query responses**: The overview states each citation includes
  "the document title, date, and a human-readable archive reference". It does not define what format
  a human-readable archive reference takes (e.g. a sequential ID, a filename, a slug), or who
  assigns it.

- **Bulk ingestion error recovery**: If a bulk ingestion run is interrupted partway through, the
  overview does not describe whether partially ingested files are rolled back, retained, or flagged.
  This is an edge case but has requirements implications.

- **Configurable thresholds — where and how configured**: Quality score thresholds and maximum file
  size are described as configurable, but the overview does not say where this configuration lives
  (config file, environment variable, CLI argument, admin UI) or who can change it. This affects
  non-functional requirements for maintainability and administration.

## Undocumented edge cases

- **Zero files submitted in a bulk ingestion run**: The overview defines the summary report format
  for runs that include rejected files, but does not address what happens if the source directory is
  empty or contains no conforming files at all.

- **Virtual document group with a file that exceeds the size limit**: The overview states the size
  limit applies to each individual file in a group, and that if any file in a group fails validation
  the entire group is rejected. It does not address whether the size check is applied before or after
  format validation, which affects the rejection reason reported.

- **Duplicate file that is also part of a virtual document group**: If a file submitted as part of a
  group is detected as a duplicate of an already-stored file, the whole group is rejected (per the
  group-rejection rule). It is unclear whether this is the intended behaviour, since the duplicate
  may be incidental (e.g. a cover page used across multiple submissions).

- **Files with mixed extractable and non-extractable pages**: The overview covers documents that
  produce no text and documents where only some pages yield text (partial extraction), both of which
  are flagged. It does not address whether any pages with good extraction are processed and embedded
  before the flag is raised, or whether the entire document is held pending review.

- **Vocabulary candidate that exactly matches an existing vocabulary term but with different
  casing or punctuation**: The deduplication rule covers candidates already in the accepted list or
  rejected list, but does not address near-identical matches (e.g. "Mill Pasture" vs "mill pasture").
  This is relevant to the deduplication logic for the vocabulary curation queue.

- **Resubmission of a previously rejected file (bulk ingestion)**: If a file was rejected in a prior
  run (e.g. for a filename convention violation), corrected, and resubmitted, the hash-based
  duplicate check should not fire (the filename changed). The overview does not explicitly address
  this scenario, but there is no apparent gap — noting it for completeness.

## Ambiguities

- **"Metadata completeness contributes to the overall quality score"**: The overview states that a
  document with extractable text but no detectable metadata will score lower and may fall below the
  review threshold. It is not stated whether metadata completeness is a fixed component of the score
  formula or whether the threshold comparison is applied separately for text quality and metadata
  quality. This could produce two different requirement interpretations.

- **"Candidate terms are deduplicated against both the accepted vocabulary and a persisted
  rejected-terms list before being raised"**: It is ambiguous whether this deduplication is exact
  string matching only, or whether it also covers normalised forms (e.g. case-insensitive, stripped
  punctuation). The behaviour in the edge case of near-duplicate terms is not defined.

- **Phase 2 curation: "can curate any document in the archive (not only their own submissions)"**:
  This implies the Primary Archivist's curation scope is limited to their own submissions in Phase 1.
  But Phase 1 describes a single-user system with no authentication, so the distinction between
  "own submissions" and "all documents" is meaningless in Phase 1. The phrasing may be intended to
  describe Phase 2 behaviour only, but it reads as a contrast that implies a Phase 1 limitation that
  does not exist in practice.

- **"Supplementary context" in Phase 2**: The overview defines this as "human-provided text attached
  to documents the system cannot interpret automatically". It is not stated whether supplementary
  context is searchable and embeddable like extracted document text, or whether it serves only as an
  aide-memoire for the curator. This affects Phase 2 requirements for the processing pipeline.

- **"Filter and facet search" deferred to Phase 3**: It is ambiguous whether basic date or type
  filtering on query results is also deferred to Phase 3, or whether some filtering capability is
  implied by Phase 1 or Phase 2 query requirements that are not yet described in detail.
