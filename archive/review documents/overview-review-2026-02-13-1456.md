# Overview Review

## Contradictions

None found.

## Missing information

None found.

## Undocumented edge cases

None found.

## Ambiguities

- **Format validation scope (web UI vs bulk ingestion):** The format validation rules — accepted file formats (PDF, TIFF, JPEG, PNG in Phase 1) and the handling of files with no extension or an unrecognised extension — are stated within the bulk ingestion must-have bullet. The document does not explicitly state whether the same format validation applies to web UI uploads. If a user submits an invalid file type via the web form, should the system reject it? On what basis and at what point (client-side, server-side, or both)? This needs to be stated to write unambiguous requirements for the web UI intake path.
