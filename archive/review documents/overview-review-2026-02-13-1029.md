# Overview Review

Reviewed against `documentation/project/overview.md` (post four prior review cycles).

## Contradictions

None found. Phase assignments, intake routes, and pipeline behaviour are internally consistent.

## Missing information

1. **Alias cardinality** — The vocabulary term structure shows "Aliases" as a column in the example table,
   but the text describes auto-adding "an alias" (singular). The schema is deferred to architecture, but it
   is not stated whether aliases is a list or a single value. This matters for requirements describing
   alias auto-addition behaviour.

2. **Curation queue tie-break** — The curation queue is ordered by "timestamp of the last successfully
   completed pipeline step that raised the flag", but there is no stated rule for what order applies when
   two documents share an identical timestamp.

3. **Vocabulary review queue tie-break** — Same gap as above: ordering by step completion timestamp, with
   no tie-break rule when two candidates share the same timestamp.

4. **Missing output directory** — The bulk ingestion summary report is written to a configurable output
   directory, but there is no statement about what happens if that directory does not exist at run time
   (created automatically, or error and run aborted?).

5. **File size limit configuration** — The configurable maximum file size has no stated minimum or maximum
   permissible configuration value, and no statement on whether zero is a valid value. Requirements cannot
   be written for boundary behaviour without this.

6. **Invalid parsed date in web UI filename** — The web form pre-populates from the filename if it follows
   the naming convention, but there is no statement about what happens if the parsed date is syntactically
   invalid (e.g. `1962-13-45 - description`). Bulk ingestion rejects non-conforming filenames outright;
   the web UI accepts any filename. An invalid date in a conforming-looking filename is not addressed.

7. **Search index visibility during pipeline resumption** — The overview states flagged documents are absent
   from the search index until the flag is cleared and embeddings are complete, but it does not state
   whether a document that has been cleared and is mid-pipeline (processing resumed, not yet re-flagged) is
   transiently visible in the search index.

## Undocumented edge cases

1. **Re-flag overwrites or appends** — The overview states "no history of previous flag/clear cycles is
   retained" in the curation queue. It is not stated whether the flag reason field is overwritten on
   re-flag or appended. A document that has been flagged, cleared, and re-flagged may have accumulated
   distinct failure reasons, and the curator's view will differ depending on which model is used.

2. **Startup rollback trigger in a long-running service** — Rollback of a crashed ingestion run is
   described as completing "on next startup before any new work is accepted". If the system runs as a
   persistent service (not restarted between runs), the trigger for detecting and completing an unfinished
   rollback is not defined.

3. **Web form with empty or invalid date** — The Phase 1 web form captures date and description. It is not
   stated whether submitting the form with an empty or syntactically invalid date value is a validation
   error at submission time, or whether the document is accepted and subsequently flagged for metadata
   incompleteness.

4. **Technical failures vs quality failures mid-pipeline** — "Each pipeline step records its own completion
   status independently of quality outcome" applies to quality outcomes, but it is not stated how a step
   that fails due to a technical error (service unavailable, exception) is recorded — as incomplete, or as
   a distinct error state separate from both a successful completion and a quality-threshold failure. The
   flag mechanism covers quality failures; technical failures are not distinguished.

## Ambiguities

1. **Metadata correction and re-embedding** — "Correct document metadata (type, date, people, land
   references, title)" is listed as a curation action. It is not stated whether correcting metadata on an
   already-embedded document triggers re-embedding. The overview explicitly defers enrichment
   reprocessing, but metadata correction is a distinct action and its downstream effect is not addressed.

2. **Submitter identity visibility scope** — "Curators can see who submitted a document when reviewing the
   queue" is the only statement about submitter identity display. It is not stated whether submitter
   identity is also visible in query results or document views outside the curation queue.

3. **Future metadata fields in Phase 1 model** — The overview states "both intake routes populate the same
   metadata model" and notes the submitter identity field must exist from Phase 1. It is not stated whether
   other fields that are introduced in later phases (e.g. document visibility scope) must also be present
   but unused in the Phase 1 schema, or whether the model is extended at the phase boundary.
