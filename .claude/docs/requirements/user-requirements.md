# User Requirements

## User Types

| User Type | Phase Introduced | Description |
| --- | --- | --- |
| Primary Archivist | 1 | Builds and maintains the archive; has all capabilities in every phase |
| Family Member | 2 | Full archival and curation access; no document deletion |
| Occasional Contributor | 3 | Submits documents and queries the archive; no curation access |
| System Administrator | 3 | Manages application-level administration and user accounts |

---

## 1. Document Intake

### 1.1 Web UI Upload

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-001 | Must | Primary Archivist | The system must accept document uploads via a web form | Phase 1 intake route; provides structured metadata entry |
| UR-002 | Must | Primary Archivist | The web form must capture date and description fields at minimum | These are the core metadata fields for Phase 1 |
| UR-003 | Must | Primary Archivist | The web form must reject a submission if the date field is empty or syntactically invalid, and prompt the user to correct it | Prevents incomplete records entering the archive |
| UR-004 | Must | Primary Archivist | Date validation must be enforced both client-side and server-side | Client-side alone is insufficient; server-side is the authoritative check |
| UR-005 | Must | Primary Archivist | If the uploaded filename follows the naming convention, the system must parse it on file selection and pre-populate the matching form fields | Reduces manual data entry for bulk-style uploads via the web form |
| UR-006 | Must | Primary Archivist | If the parsed date from a filename is not a valid calendar date, the date field must be left empty with no error shown | Avoids misleading the user with a pre-populated invalid date |
| UR-007 | Must | Primary Archivist | The form fields are the canonical metadata input; any filename is accepted regardless of whether it follows the naming convention | The naming convention is a convenience for pre-population only |

### 1.2 Bulk Ingestion

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-008 | Must | Primary Archivist | The system must accept bulk ingestion of documents from a directory via an on-demand CLI command | Phase 1 intake route for large document sets |
| UR-009 | Must | Primary Archivist | Files submitted via bulk ingestion must follow the naming convention `YYYY-MM-DD - short description`; files that do not conform must be rejected with the reason included in the summary report | Ensures metadata can be derived from filenames |
| UR-010 | Must | Primary Archivist | The filename stem must be parsed into date and description metadata fields, feeding archive reference derivation identically to a web UI submission | Both intake routes must populate the same metadata model |
| UR-011 | Must | Primary Archivist | The source directory must contain only files; the presence of sub-directories must be treated as an error and the run must not proceed | Sub-directories are ambiguous and unsupported in Phase 1 |
| UR-012 | Must | Primary Archivist | When a run is halted by sub-directory detection, a summary report must still be produced with zero counts and a clear actionable error message identifying which sub-directories were found | The user needs to know what to fix before re-submitting |
| UR-013 | Must | Primary Archivist | A bulk ingestion run must be atomic; if the run is interrupted, it must be rolled back and no files from the interrupted run must be stored | Prevents partial ingestion runs corrupting the archive state |
| UR-014 | Must | Primary Archivist | Cleanup of any incomplete prior run must occur at the start of every ingestion run, before any new work is accepted | Ensures cleanup is triggered regardless of how the process was stopped |
| UR-015 | Must | Primary Archivist | No summary report must be produced for an interrupted run | An incomplete report would be misleading |
| UR-016 | Must | Primary Archivist | Per-file validation must apply format checking before size checking; if a file fails format validation, the size check must not be reached | Format is the threshold gate; no point checking size of an invalid format |
| UR-017 | Must | Primary Archivist | A file with no extension or an unrecognised extension must be treated as a format validation failure and rejected | Unrecognised files cannot be processed |

### 1.3 Bulk Ingestion Summary Report

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-018 | Must | Primary Archivist | The system must produce a summary report after each bulk ingestion run: a header showing totals (submitted, accepted, rejected) followed by a per-file record of filename, outcome, and rejection reason where applicable | Gives the user a complete record of what happened |
| UR-019 | Must | Primary Archivist | The report must be printed to stdout and written to a timestamped file in a configurable output directory | Supports both immediate review and later audit |
| UR-020 | Must | Primary Archivist | If the output directory does not exist at run time, it must be created automatically | Reduces configuration friction |
| UR-021 | Must | Primary Archivist | If the source directory is empty or contains no conforming files, the report must still be produced showing zero counts with a note that no files were found | Confirms to the user that the command ran; silence would be ambiguous |

### 1.4 File Validation

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-022 | Must | Primary Archivist | The system must reject files that cannot be opened or parsed at intake, including empty or zero-byte files | Unparseable files cannot be processed |
| UR-023 | Must | Primary Archivist | The system must detect and reject exact duplicate files by file hash; hash-based duplicate detection applies to individual files regardless of intake route or group membership | Prevents duplicate records in the archive |
| UR-024 | Must | Primary Archivist | Content-based duplicate detection (rescanned copies of the same document) is out of scope for Phase 1 | Deferred; requires more sophisticated comparison |
| UR-025 | Must | Primary Archivist | The system must enforce a configurable maximum file size per file; the limit applies to each individual file including files within a virtual document group | Prevents excessively large files from entering the pipeline |
| UR-026 | Must | Primary Archivist | Zero and negative values for the file size limit must be rejected at startup with an actionable error message | Invalid configuration must be caught before any work begins |
| UR-027 | Must | Primary Archivist | Rejected files must not be stored; a re-submission in a later run must be treated as a fresh submission with no memory of the previous rejection | The system is stateless with respect to rejected files |

### 1.5 Virtual Document Groups

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-028 | Must | Primary Archivist | The system must support grouping multiple files into a single virtual document at submission time | Multi-part scanned documents must be treated as one logical unit |
| UR-029 | Must | Primary Archivist | A virtual document group must be processed and referenced as a single logical unit in query results | Users query documents, not individual files |
| UR-030 | Must | Primary Archivist | If any file in a group fails intake validation (including duplicate detection), the entire group must be rejected; no partial groups must be stored | Partial groups would create incomplete documents in the archive |
| UR-031 | Must | Primary Archivist | Phase 1 must use fail-fast validation for groups: processing must stop on the first failure; remaining files must be reported as not attempted; only failing files must be reported with their reasons | Consistent with Phase 1 simplicity; try-all deferred to Phase 2 |
| UR-032 | Should | Primary Archivist | Phase 2 must introduce a per-request CLI flag to switch to try-all validation, validating every file and reporting all failures in a single pass | Improves usability when submitting large groups |
| UR-033 | Must | Primary Archivist | A group containing a single file must be valid and processed identically to a standalone submission | Avoids special-casing single-file groups |
| UR-034 | Must | Primary Archivist | A zero-file group must be a validation error and rejected at intake | A group with no files is meaningless |
| UR-035 | Must | Primary Archivist | If two files in the same group share a filename, the group must be rejected at intake | Duplicate filenames within a group are ambiguous |

### 1.6 Accepted Formats

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-036 | Must | Primary Archivist | Phase 1 must accept PDF, TIFF, JPEG, and PNG files | Covers scanned and digital documents for Phase 1 |
| UR-037 | Should | Primary Archivist, Family Member | Phase 2 must additionally accept DOCX and EML files | Covers digital correspondence and email formats |

---

## 2. Text Extraction and Processing

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-038 | Must | Primary Archivist | The system must extract text from typed and printed documents | Core capability; enables search and query |
| UR-039 | Must | Primary Archivist | The system must produce a quality score per page and for the document as a whole, representing confidence that extracted text is a faithful and complete representation of the document content; scores must be in the range 0–100 | Enables flagging of poor extractions for review |
| UR-040 | Must | Primary Archivist | All pages in a document must always be evaluated; there must be no fail-fast within a document | The user needs a complete picture of which pages have issues |
| UR-041 | Must | Primary Archivist | A document must fail the quality threshold if any page fails it | Partial extractions must not be silently accepted |
| UR-042 | Must | Primary Archivist | Text quality and metadata completeness must be assessed with separate checks, each with an independent configurable threshold | The two checks are independent concerns |
| UR-043 | Must | Primary Archivist | When both thresholds fail simultaneously, both failures must be recorded as a single flag with multiple reasons; the flag reason must include the full list of failing pages | The user needs complete information in a single review action |
| UR-044 | Must | Primary Archivist | The system must detect document type, dates, people, and land references automatically | Supports metadata completeness assessment and query relevance |
| UR-045 | Must | Primary Archivist | Partial detection (some fields found, others not) must not itself trigger a flag; the configurable threshold determines whether the completeness score triggers a flag | Avoids excessive flagging for documents with partial metadata |
| UR-046 | Must | Primary Archivist | The specific metadata fields assessed and the completeness scoring method are deferred to the architecture phase | `[ARCHITECTURAL FLAG — for Head of Development]` |
| UR-047 | Must | Primary Archivist | The system must generate embeddings for each document chunk | Enables semantic search and query |
| UR-048 | Must | Primary Archivist | Chunk boundaries must be determined by an AI agent that reads the document content and identifies semantically meaningful units, rather than by fixed-size splitting | Ensures related content is kept together in a single embedding |
| UR-049 | Must | Primary Archivist | Each pipeline step must record its own completion status independently of quality outcome; a step that ran successfully must be marked complete even if its output failed a quality threshold | Enables precise pipeline resumption from the correct step |
| UR-050 | Must | Primary Archivist | A step that fails due to a technical error must be recorded as incomplete and retried on the next processing run | Transient failures must not permanently block documents |
| UR-051 | Must | Primary Archivist | A configurable retry limit must prevent infinite retry loops; when the limit is exceeded, the document must be flagged with the error reason and surfaced in the curation queue | The user must be able to act on persistently failing documents |
| UR-052 | Must | Primary Archivist | The processing trigger is manual in Phase 1 | `[ARCHITECTURAL FLAG — for Head of Development]` — automated triggers deferred to later phases |
| UR-053 | Must | Primary Archivist | If a stored file is missing or unreadable when reprocessing is attempted, the document must be flagged with the error reason and surfaced in the curation queue; processing must continue for other documents | A missing file is a recoverable document-level error, not a system failure |

---

## 3. Flagging and Curation Queue

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-054 | Must | Primary Archivist | Documents failing the text quality or metadata threshold, producing no extractable text, yielding partial extraction, or containing zero pages must be stored and flagged for manual review rather than rejected | They may be valid documents requiring manual data entry |
| UR-055 | Must | Primary Archivist | For documents with mixed extractable and non-extractable pages, the whole document must be held pending review; no partial embeddings must be generated | Partial embeddings would produce incomplete and misleading query results |
| UR-056 | Must | Primary Archivist | Flagged documents must be absent from the search index until the flag is cleared and the embedding step completes successfully | No transient visibility window is acceptable |
| UR-057 | Must | Primary Archivist | A document with no extractable text must have no in-application resolution path in Phase 1; it remains flagged until Phase 2 supplementary context is available | Phase 1 is a single-user local system; this is an accepted limitation |
| UR-058 | Must | Primary Archivist | Clearing a flag must advance processing to the next incomplete step and must not re-run completed steps | Avoids redundant reprocessing |
| UR-059 | Must | Primary Archivist | Flag-clearing and processing resumption must be separate manual actions in Phase 1; clearing a flag must not automatically trigger processing | Processing trigger is a separate architectural concern |
| UR-060 | Must | Primary Archivist | Clearing a flag must clear the flag reason field; if processing fails again after a flag is cleared, the document must be re-flagged with the reason field written fresh — no accumulation of prior reasons | Accumulated reasons would be confusing and misleading |
| UR-061 | Must | Primary Archivist | The flag mechanism must be the single reporting location for all document-level failures | Consistency; avoids multiple places to check for problems |

---

## 4. Search and Retrieval

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-062 | Must | Primary Archivist | The system must answer natural language questions with synthesised responses and source citations via CLI | Core query capability for Phase 1 |
| UR-063 | Must | Primary Archivist | Each citation must include the document title, date, and a human-readable archive reference | Users need enough information to locate and verify the source |
| UR-064 | Must | Primary Archivist | Documents must be stored internally under a system-generated unique identifier; this identifier must never be exposed to the user | The internal key must be stable and independent of user-facing metadata |
| UR-065 | Must | Primary Archivist | The human-readable archive reference must be derived from the document's curated metadata at the time of display; it is mutable and will change if the underlying metadata is corrected | Archive references reflect current metadata, not a fixed snapshot |
| UR-066 | Must | Primary Archivist | Two documents may share the same human-readable reference if their metadata is identical; they remain distinct by their internal identifier | Uniqueness is the responsibility of the internal identifier |
| UR-067 | Must | Primary Archivist | If no relevant documents exist for a query, the system must say so | Avoids misleading the user with silence or a fabricated answer |
| UR-068 | Must | Primary Archivist | All structured filtering of results (by date range, document type, or similar) is out of scope for Phase 1 and Phase 2; queries use natural language only | Deferred to Phase 3 |
| UR-069 | Should | Primary Archivist, Family Member | Phase 2 must return original documents alongside query answers | Users want to verify against the source document |
| UR-070 | Should | Primary Archivist, Family Member | Phase 2 must support browsing documents directly | Supports curation and exploration workflows |
| UR-071 | Could | Primary Archivist | Page-level citation is deferred to a later phase | Lower priority enhancement; full-document citation is sufficient for Phase 1 |
| UR-072 | Should | Primary Archivist, Family Member, Occasional Contributor | Phase 3 must support filter and facet search | Improves precision for users with large archives |

---

## 5. Metadata

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-073 | Must | Primary Archivist | The system must maintain a domain vocabulary of estate-specific terms (field names, people, organisations, legal phrases, and similar); the vocabulary must be stored entirely in the database | Supports accurate extraction and query across estate-specific language |
| UR-074 | Must | Primary Archivist | The database must be initialised from a seed script on first use and in development environments; the seed script must provide an initial vocabulary, not an empty one | An empty vocabulary would produce poor extraction quality on first use |
| UR-075 | Must | Primary Archivist | The vocabulary schema and seed script content are deferred to the architecture phase | `[ARCHITECTURAL FLAG — for Head of Development]` |
| UR-076 | Must | Primary Archivist | On restart, the system must reconnect to the existing database; no vocabulary rebuild must be required | Vocabulary is persistent state; rebuild would be destructive and slow |
| UR-077 | Must | Primary Archivist | Each vocabulary term must be a structured record with at minimum: term, category, description, aliases (a list — zero or more), and relationships; category must be a first-class attribute that drives which fields are relevant to the record | Supports consistent storage and display of heterogeneous term types |
| UR-078 | Must | Primary Archivist | The vocabulary must be extendable manually via CLI at any time | The curator must be able to add terms outside of the automated pipeline |
| UR-079 | Must | Primary Archivist | During document processing, candidate terms must be proposed automatically and surfaced in a separate vocabulary review queue immediately as each document completes processing, ordered by step-completion timestamp; tie-break is natural database ordering | Keeps vocabulary current without requiring manual trawling of documents |
| UR-080 | Must | Primary Archivist | Candidates must be deduplicated against both the accepted vocabulary and a persisted rejected-terms list before being raised; deduplication must be normalised (case-insensitive, punctuation stripped) | Avoids presenting the curator with near-identical candidates repeatedly |
| UR-081 | Must | Primary Archivist | When a candidate matches an accepted term after normalisation, it must be suppressed from the review queue and the normalised variant must be appended to the aliases list of the existing term | Enriches the vocabulary automatically without curator intervention |
| UR-082 | Must | Primary Archivist | The curator must be able to accept (add to vocabulary) or reject (add to rejected list) each candidate in the vocabulary review queue | Gives the curator control over vocabulary quality |
| UR-083 | Must | Primary Archivist | Submitter identity must be recorded on every document from Phase 1; in Phase 1 this field is always the Primary Archivist, but the field must exist in the data model to support multi-user phases without schema changes | `[ARCHITECTURAL FLAG — for Head of Development]` — schema must include this field from Phase 1 |
| UR-084 | Must | Primary Archivist | Submitter identity must be visible in the curation queue only; it must not be shown in query results or document views | Operational information, not archival information |
| UR-085 | Must | Primary Archivist | The Phase 1 data model must be minimal; fields introduced in later phases must be added at the phase boundary; submitter identity is the one explicitly required exception | Avoids schema pollution with unused future fields |

---

## 6. Curation

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-086 | Must | Primary Archivist | The system must provide a CLI command to view the document curation queue: documents awaiting review or flagged with issues, ordered by timestamp of the last successfully completed pipeline step that raised the flag; no history of previous flag/clear cycles is retained; tie-break is natural database ordering | Gives the curator a prioritised list of documents requiring attention |
| UR-087 | Must | Primary Archivist | The system must provide a CLI command to view the vocabulary review queue: candidate terms awaiting accept or reject decisions, ordered by step-completion timestamp; tie-break is natural database ordering | Keeps vocabulary review distinct from document curation |
| UR-088 | Must | Primary Archivist | The system must provide a CLI command to clear a flag on a document to resume pipeline processing from the next incomplete step | Primary action for resolving flagged documents |
| UR-089 | Must | Primary Archivist | The system must provide a CLI command to correct document metadata (type, date, people, land references, title); in Phase 1, correcting metadata must update the metadata fields only and must not trigger re-embedding | Phase 1 scope; re-embedding on correction deferred to Phase 2 or 3 |
| UR-090 | Must | Primary Archivist | The system must provide a CLI command to flag a document manually with a typed status and a free-text reason | Allows the curator to mark documents that need attention for reasons the system cannot detect automatically |
| UR-091 | Should | Primary Archivist, Family Member | Phase 2 must provide a web UI for all curation functions | Replaces CLI curation for Phase 2+ users |
| UR-092 | Should | Primary Archivist, Family Member | Phase 2 must allow supplementary context to be attached to documents the system cannot interpret automatically; supplementary context must be embedded and searchable; when a query answer draws on supplementary context, the citation must identify it as supplementary context added by the curator rather than text extracted from the document | Provides a resolution path for documents with no extractable text |
| UR-093 | Should | Primary Archivist, Family Member | Phase 2 must allow metadata correction to trigger re-embedding | Corrected metadata should be reflected in search results |
| UR-094 | Should | Primary Archivist, Family Member | Phase 2 must support automated reprocessing after human correction or supplementary context is added; this is an automated trigger for the same processing pipeline, not a new reprocessing capability | Reduces manual steps for the curator in Phase 2 |
| UR-095 | Must | Primary Archivist | In Phase 1 and Phase 2, there must be no in-application mechanism to remove erroneously submitted documents; the Primary Archivist has direct out-of-band access to the underlying system | Document deletion as a managed application feature is deferred to Phase 3 |
| UR-096 | Should | Primary Archivist, Family Member | Family Member access must be introduced in Phase 2; a Family Member has the same curation access as the Primary Archivist except no document deletion; a Family Member can curate any document regardless of who submitted it | Shares the curation workload |

---

## 7. User Management and Access Control

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-097 | Must | Primary Archivist | Phase 1 must have a single user with no authentication; the Primary Archivist is the system | Phase 1 is a local, single-user tool |
| UR-098 | Should | Primary Archivist, Family Member | Phase 2 must introduce user authentication | Required before a second user is added |
| UR-099 | Should | System Administrator | Phase 3 must introduce user account management | Required before external users are admitted |
| UR-100 | Should | Occasional Contributor | Phase 3 must introduce Occasional Contributor access: submit documents and query the archive; no curation access | Widens the archive to trusted external contributors |
| UR-101 | Should | System Administrator | Phase 3 must introduce document visibility scoping by user type | Controls what different user types can see |
| UR-102 | Should | System Administrator | Phase 3 must introduce the System Administrator role, separated from the Primary Archivist; System Administrator manages application-level administration and user accounts | Separates operational responsibilities as the system scales |
| UR-103 | Must | — | There must be no public or anonymous access at any phase; there must be no self-registration | The system is private at all phases |

---

## 8. Non-Functional Requirements

### 8.1 Configuration

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-104 | Must | Primary Archivist | Every external service (storage, database, OCR, embedding, LLM) must be abstracted via an interface; concrete implementations must be selected at runtime via configuration with no hardcoded providers | `[ARCHITECTURAL FLAG — for Head of Development]` — core design constraint; drives interface design throughout |
| UR-105 | Must | Primary Archivist | All configurable operational values (quality score thresholds, file size limit, retry limit, and similar parameters) must be read from a configuration file external to the codebase at runtime; they must not be hardcoded or set only via environment variables | Supports tuning without code changes or redeployment |

### 8.2 Error Messages

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-106 | Must | Primary Archivist | All error messages delivered during human interaction (CLI output, curation queue, summary reports) must be actionable — they must state what went wrong and what the user can do to resolve it | Poor error messages produce support burden; this is a design constraint throughout |

### 8.3 Data Integrity

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-107 | Must | Primary Archivist | Stored files must be immutable once accepted | Prevents accidental or unauthorised modification of archive records |
| UR-108 | Must | Primary Archivist | Regular database backups are assumed to protect vocabulary and metadata; backup implementation is outside the system's direct responsibility | `[ARCHITECTURAL FLAG — for Head of Development]` — hosting and ops concern |

### 8.4 Scale and Performance

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-109 | Could | Primary Archivist | Phase 1 performance requirements are not formally specified; the system must be usable by a single user on local hardware | Phase 1 is a proof-of-pipeline; formal performance targets are deferred |
| UR-110 | Should | Primary Archivist, Family Member, Occasional Contributor | Phase 3 hosted infrastructure requirements are deferred to the architecture phase when hosting targets are known | `[ARCHITECTURAL FLAG — for Head of Development]` |

### 8.5 Maintainability

| ID | Priority | User Type | Requirement | Rationale |
| --- | --- | --- | --- | --- |
| UR-111 | Must | Primary Archivist | The processing pipeline must be re-entrant by design: documents must be resumable from any incomplete step without re-running completed steps | Required for flag-clearing, retry logic, and future enrichment reprocessing |
| UR-112 | Must | Primary Archivist | The data model must be designed to allow fields to be added at phase boundaries without requiring destructive schema migrations | Supports incremental delivery across phases |

---

## Architectural Flags

The following requirements have architectural implications. They are surfaced here for resolution by the Head of Development before implementation begins.

| Requirement ID | Note |
| --- | --- |
| UR-046 | Metadata fields assessed for completeness and the scoring method are deferred to architecture — they depend on what the extraction pipeline can reliably produce |
| UR-052 | Processing trigger is manual in Phase 1; the mechanism for automated triggering in later phases is an architectural decision |
| UR-075 | Vocabulary schema and seed script content depend on domain modelling decisions and extraction pipeline design |
| UR-083 | Submitter identity field must be present in the Phase 1 schema; the data model design must accommodate this from the start |
| UR-104 | Provider-agnostic configuration is a core design constraint; every external service must be behind an interface — this drives the entire system architecture |
| UR-105 | External configuration file format and loading mechanism are architectural decisions |
| UR-108 | Database backup strategy is an operational/hosting concern outside the application boundary |
| UR-110 | Phase 3 hosted infrastructure and performance requirements depend on hosting target decisions |
