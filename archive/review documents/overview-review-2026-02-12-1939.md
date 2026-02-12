# Overview Review

## Contradictions

- **Curation access and out-of-scope statement**: The Phase 1 "Must have" list includes "correct document metadata (type, date, people, land references, title)" via CLI curation, but the Phase 1 "Out of scope" list states "curation by anyone other than the Primary Archivist." These are not contradictory with each other, but the out-of-scope entry implies curation itself is in scope — the statement reads as a user-restriction caveat, not a feature exclusion. No actual contradiction, but the phrasing may cause confusion when writing requirements.

- **Bulk ingestion filename convention vs. archive reference**: The overview states that "for bulk ingestion, the filename stem is the initial basis for the reference." It also states that the form fields are canonical for web UI uploads. This implies the archive reference derivation mechanism differs by intake route. The phrase "initial basis" is vague — it is unclear whether the filename stem is used as-is, normalised, or only partially used. This creates a potential contradiction with the statement that the archive reference is "derived from the document's curated metadata — enriched from extraction where possible," which applies to both routes. If the archive reference is always derived from curated metadata, why does the intake route matter?

## Missing information

- **What "cleared" means for a flagged document**: The overview states that clearing a flag resumes processing "from the next incomplete step." It does not define what steps exist in the pipeline, what order they run in, or what "next incomplete step" means in practice. Without this, it is not possible to write requirements for the flag-clearing behaviour.

- **Definition of "accepted" vocabulary**: The overview describes accepting a candidate term as "adds to vocabulary" and rejecting as "adds to rejected list," but does not describe what an accepted vocabulary term contains beyond the term string itself. Are there associated fields (definition, category, aliases)? This affects the requirements for the vocabulary review queue and manual vocabulary extension.

- **Reprocess trigger in Phase 1**: The overview states that once a flag is cleared, processing resumes. It does not describe whether this is triggered automatically (on flag clear) or requires a separate manual step. Phase 2 explicitly introduces "reprocess documents after human correction," but the Phase 1 flag-clearing behaviour implies reprocessing also happens in Phase 1. The mechanism is not defined.

- **Summary report output format**: The overview describes report content (header counts, per-file records) but does not specify the file format of the written report (plain text, JSON, CSV, structured log). This is likely an architectural decision, but requirements writers need to know whether to specify a format or leave it open.

- **Quality score definition per document vs. per page**: The overview states scores are produced "per page and for the document as a whole" and that flags are triggered by failing "on any page or overall." It does not describe how the per-document score is derived from per-page scores (e.g. minimum, average, weighted). This may be an architectural concern, but the behaviour — specifically what "failing on any page" means relative to the document-level threshold — needs to be clear for requirements.

- **Vocabulary seed script content**: The overview defers "the schema and initial content of the seed script to the architecture phase." This is appropriate, but it is also not clear whether the seed vocabulary is expected to contain any terms at all in Phase 1, or whether the vocabulary starts empty and is built entirely from candidate proposals and manual additions. This affects what the system "must do" at first use.

- **Hard system error behaviour**: The overview states that a missing or unreadable stored file during re-processing "is treated as a hard system error rather than a curation issue." It does not describe what happens next: does the system halt, log and continue, alert the user, quarantine the document record? This is needed to write requirements for error handling.

## Undocumented edge cases

- **Duplicate virtual group file names within a single submission**: If two files in the same virtual group have the same filename (but are distinct files), the behaviour is not described. Hash-based duplicate detection would not catch this if the content differs.

- **Empty virtual document group**: The overview states a single-file group is valid. It does not state whether a zero-file group is a valid submission or an error condition.

- **Vocabulary candidate that matches an accepted term after normalisation but not before**: The overview describes normalised deduplication (case-insensitive, punctuation stripped). It does not describe whether the already-accepted form takes precedence over the proposed form, or whether the user is informed of the existing form when a near-duplicate is suppressed.

- **Flag cleared but supplementary context also present (Phase 2 interaction)**: The Phase 2 section introduces supplementary context as a mechanism for flagged documents to progress. The Phase 1 flag-clearing behaviour does not account for this — the two mechanisms are described independently. The interaction between them (e.g. can Phase 2 supplementary context substitute for re-processing in Phase 1 mode?) is not addressed.

- **Multiple quality thresholds failing simultaneously**: The overview describes text quality and metadata completeness as independent checks with independent thresholds. It does not describe how the flag reason is recorded when both thresholds fail at once — is it one flag with both reasons, or two separate flags?

- **Document with zero pages after parsing**: The overview covers empty/zero-byte files (rejected at intake) and documents with no extractable text (flagged). A document that opens successfully but contains zero pages is not addressed.

- **Bulk ingestion run with a mix of valid files and a sub-directory**: The overview states the presence of a sub-directory is an error and the run does not proceed. It does not describe what the summary report contains in this case, or whether any part of the report (e.g. the sub-directory detection error) is included.

- **Re-submission of a previously rejected file**: If a file was rejected (e.g. failed format validation) and is submitted again later in a separate run, the hash-based duplicate detection would not block it (it was not stored). No behaviour is described for this case — expected, but worth confirming.

## Ambiguities

- **"Bulk ingestion and document processing are separate steps"**: The overview states ingestion stores files and processing runs independently. It does not describe how processing is triggered — is it scheduled, manually initiated, event-driven, or continuous? This has significant requirements implications (and architectural ones), but the trigger mechanism is not mentioned anywhere in the overview.

- **"Oldest-first" ordering for both queues**: The document curation queue and vocabulary review queue are both described as ordered oldest-first. It is not stated whether "oldest" means oldest submission date, oldest flag date, or oldest creation timestamp. These could differ for re-flagged documents.

- **"Structured form" for web UI uploads**: The overview states the web UI uses a structured form with date and description fields. It does not define what other fields the form contains, or whether the form fields map one-to-one to metadata fields. The canonical status of form fields vs. extracted metadata for archive reference derivation depends on knowing what the form captures.

- **"Human-readable archive reference" derivation**: The overview states the reference is "derived from the document's curated metadata — enriched from extraction where possible." It then says for bulk ingestion "the filename stem is the initial basis." It is not clear whether the filename stem populates a metadata field (which then becomes the reference) or directly generates the reference bypassing the metadata model. The distinction matters for whether the reference is mutable (via metadata correction) or fixed at intake.

- **"Configurable" validation mode for virtual groups**: The overview describes fail-fast vs. try-all as configurable. It does not state where this is configured (runtime config file, per-run CLI flag, per-submission option). This may be an architectural decision, but the scope of "configurable" needs to be clear for requirements.

- **Phase 2 "reprocess documents"**: Phase 2 adds the ability to reprocess documents after human correction. Phase 1 already implies reprocessing via flag-clearing. The distinction between these two mechanisms — or whether they are the same mechanism exposed via different interfaces — is ambiguous.
