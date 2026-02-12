# Overview Review

## Contradictions

No contradictions found. The document is internally consistent.

## Missing information

- **Metadata threshold definition**: The overview states that metadata completeness is assessed with a
  configurable threshold and that partial detection is not itself a flag trigger. It does not define what
  "metadata completeness" means quantitatively — which fields are required, which are optional, and how
  completeness is scored. This is needed to write a testable requirement.
- **Archive reference format**: The overview states that the archive reference is derived from extracted
  metadata and the supplied filename but does not specify the format or structure of the reference. The
  requirements will need to describe what a valid archive reference looks like.
- **Bulk ingestion rollback scope**: The overview states a bulk ingestion run is atomic and rolled back on
  interruption. It does not specify whether files accepted and stored before the interruption point are also
  removed, or whether rollback applies only to the in-progress file. (Reading the text as written, the full
  run is rolled back — this should be confirmed.)
- **Vocabulary YAML schema**: The overview mentions a YAML seed file but does not describe its expected
  structure. This is a requirement detail that must be defined somewhere, though it may be appropriate to
  defer to architecture.
- **Curation queue content**: The overview lists what the CLI curation queue shows (documents awaiting
  review or flagged with issues) and what actions are available. It does not specify whether vocabulary
  candidates appear in the same queue or a separate one, nor the order in which items are presented.

## Undocumented edge cases

- **File submitted with no extension**: The overview defines accepted formats but does not state what
  happens if a file is submitted with no extension or an unrecognised extension (e.g. `.xyz`). Should be
  treated as a format validation failure — but this is not stated explicitly.
- **Virtual group with a single file**: The overview defines multi-file virtual document groups but does
  not state whether a group of one file is valid or should be rejected as a misconfiguration.
- **Vocabulary seed file missing at startup**: The overview states the YAML seed file is read at first
  startup. It does not state what happens if the file does not exist or cannot be read (error and halt, or
  start with an empty vocabulary).
- **Duplicate archive reference**: The overview says the archive reference is generated during processing
  and is stable once assigned. It does not state what happens if the generated reference collides with one
  already in the system.
- **Flag cleared but original file no longer accessible**: The overview describes re-processing after a
  flag is cleared. It does not state what happens if the stored file is missing or corrupted at that point.
- **Bulk ingestion source directory contains sub-directories**: The overview specifies a source directory
  but does not state whether sub-directories are traversed, ignored, or treated as an error.

## Ambiguities

- **"First startup" for vocabulary seeding**: The overview states the YAML seed file is read "at first
  startup." It is ambiguous whether this means the very first time the system runs (once only), or every
  time the system starts (re-importing on each restart). This affects whether manual vocabulary additions
  made after first startup could be overwritten.
- **"Entire group is rejected" vs individual file rejection**: The overview states that if any file in a
  virtual group fails validation the whole group is rejected, and "the rejection report identifies which
  file failed and the reason." It is not stated whether all files in the group are listed in the report
  (with one marked as the failure cause) or only the failing file.
- **Processing queue vs curation queue**: The overview uses both "processing queue" and "curation queue"
  in different sections. It is not clear whether these are the same queue (documents awaiting any action)
  or two distinct queues with different contents.
- **Vocabulary candidate proposal timing**: The overview states candidates are "proposed automatically and
  surfaced in the curation queue" during processing. It is not stated whether candidates are surfaced
  immediately as each document is processed or batched until a processing run completes.
- **Supplementary context searchability (Phase 2)**: The overview states supplementary context "is
  embedded and searchable." It does not state whether supplementary context is included in query responses
  in the same way as extracted text, or whether it is identified separately as a source type in citations.
