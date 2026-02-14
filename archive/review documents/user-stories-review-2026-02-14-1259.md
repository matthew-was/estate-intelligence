# User Stories Quality Review

Reviewed: `.claude/docs/requirements/phase-1-user-stories.md`
Against: `.claude/docs/requirements/user-requirements.md` (approved 2026-02-14)
Date: 2026-02-14

This is a fresh quality and consistency review. The file has already completed one review cycle (34 findings, all resolved). These findings represent issues remaining after that cycle.

---

## Summary

32 findings are grouped into four categories:

- **Coverage gaps** — requirements that are not fully represented in the stories
- **Untestable criteria** — acceptance criteria or definitions of done that cannot be objectively verified
- **Internal inconsistencies** — stories that contradict each other or contain conflicting statements
- **Precision issues** — criteria that are ambiguous or underspecified in ways that would cause a developer to make assumptions

---

## Coverage Gaps

### CG-001: UR-056 has no story and is absent from the Architectural Flags Summary

UR-056 states that the specific metadata fields assessed for completeness and the scoring method are deferred to the architecture phase (`[ARCHITECTURAL FLAG — for Head of Development]`). This flag appears explicitly in the requirements document but has no corresponding story and does not appear in the Architectural Flags Summary table at the end of the stories document. US-037 covers UR-053 and UR-055 but does not reference UR-056 or carry the architectural flag. A developer working from stories alone would have no record of this architectural dependency.

The story numbering jumps from US-038 to US-040 with no US-039. This gap is likely where UR-056 was intended to be covered.

**Affected requirements**: UR-056
**Suggested action**: Add US-039 covering UR-056 (the architectural deferral of metadata scoring fields and method), and add the corresponding row to the Architectural Flags Summary table.

---

### CG-002: US-016 DoD covers only the empty directory case, not the all-rejected case

US-016 has two acceptance criteria: one for an empty source directory and one for a directory containing files where none conform to the naming convention. The DoD covers only the empty directory case: "Running ingestion against an empty directory produces a report with zero counts and a note." The second case (files present but none conforming) is tested by the acceptance criteria but is absent from the DoD. A developer would pass the DoD without implementing the second case.

**Affected requirements**: UR-026
**Suggested action**: Extend the DoD to cover both cases.

---

### CG-003: US-028 omits image-format documents (TIFF, JPEG, PNG)

The acceptance criterion for US-028 states "Text is extracted from Phase 1 document types (typewritten and printed documents; modern digital PDFs)." Phase 1 accepts TIFF, JPEG, and PNG files (UR-009), which are image formats requiring OCR rather than text layer extraction. The criterion does not address these formats. A developer implementing this story could deliver text extraction only for PDFs with text layers and not implement OCR for image-format files.

**Affected requirements**: UR-042, UR-009
**Suggested action**: Add a criterion explicitly covering text extraction from image-format documents (TIFF, JPEG, PNG) submitted in Phase 1.

---

### CG-004: US-022 has no architectural flag for the CLI group expression mechanism

US-022 establishes that virtual document grouping is CLI-only in Phase 1, but there is no acceptance criterion or architectural flag addressing how the CLI expresses a group (flag, manifest file, directory structure, or other mechanism). Without a flag, a developer implementing this story has no architectural resolution path for this design decision. The Architectural Flags Summary table does not include this story.

**Affected requirements**: UR-035
**Suggested action**: Add an acceptance criterion noting that the CLI mechanism for expressing a group is an architectural decision, and add a corresponding row to the Architectural Flags Summary table.

---

## Untestable Criteria

### UC-001: US-002 — "both fields are presented to the user before submission" is not testable

The second acceptance criterion — "Both fields are presented to the user before submission" — describes a UI structural property rather than a testable condition. "Presented" has no verifiable threshold: is a hidden field "presented"? The criterion should describe observable behaviour, for example: "The date field and description field are visible and interactive before the submit action is available."

**Affected story**: US-002
**Suggested action**: Replace with a criterion stating that both fields are visible and accessible before submission can be attempted.

---

### UC-002: US-002 — "Submission is not possible without engaging both fields" — "engaging" is undefined

The third acceptance criterion uses "engaging," which is not a standard form interaction term. It is unclear whether this means: the field must have a value, the field must have been focused, or the field must have been modified. The date field is validated per US-003 (required, must be valid), but the description field has no explicit required-content validation in UR-002. If description is not required to have content, this criterion is misleading.

**Affected story**: US-002
**Suggested action**: Replace "engaging" with a precise term. If description is required, state it explicitly. If it is optional, remove this criterion or restate it to reflect that only the date field is validated for content.

---

### UC-003: US-003 — example invalid date `32/13/1962` uses DD/MM/YYYY format

The example uses day/month/year notation (`32/13/1962`). The system's naming convention and metadata model use `YYYY-MM-DD` throughout. A developer implementing date validation could interpret this example as specifying that the validated format is `DD/MM/YYYY` rather than `YYYY-MM-DD`, resulting in the wrong validation format being implemented.

**Affected story**: US-003
**Suggested action**: Replace the example with one using `YYYY-MM-DD` format, e.g. `1962-13-32`.

---

### UC-004: US-011 — DoD says "names each sub-directory found" but acceptance criteria do not state this

The DoD for US-011 states "the summary report names each sub-directory found." The third acceptance criterion also says "The error message names each sub-directory found, not just a count." However, the DoD appears to restate only the naming requirement without confirming zero counts. Neither criterion nor DoD explicitly verifies that files are not processed — only that the run does not proceed. The DoD should be checked against both criteria.

**Affected story**: US-011
**Suggested action**: Minor — confirm the DoD covers all criteria including the "no files are processed" criterion.

---

### UC-005: US-025 — "processed by the same code path" is an implementation assertion, not a testable observable

The criterion "It is processed by the same code path as a standalone submission" cannot be verified by testing the system's behaviour. It describes an implementation decision. The intent — that a single-file group produces the same result as a standalone submission — should be expressed in terms of observable outcomes.

**Affected story**: US-025
**Suggested action**: Replace with "A group of one file is accepted, processed, and produces the same pipeline outcome as a standalone submission with the same file."

---

### UC-006: US-044 DoD requires review against "at least two sample documents" without specifying document types

The DoD for US-044 states "Chunk boundaries are reviewed against at least two sample documents of different types from the estate corpus and confirmed by the Primary Archivist." In Phase 1 the accepted document types are typewritten, printed, and modern digital PDFs (plus image formats). The DoD does not specify that the reviewed documents must be Phase 1 types, potentially implying Phase 2 types (handwritten, maps, emails) are needed to close the story.

**Affected story**: US-044
**Suggested action**: Specify "at least two Phase 1 document types (e.g. a typewritten document and a digital PDF)" to scope the review to what is available in Phase 1.

---

### UC-007: US-067 — "no legal advice" criterion has no testable operationalisation in the DoD

The acceptance criterion "The system does not give legal advice or legal interpretation" and the corresponding DoD statement "responses contain no legal advice" provide no test method. This is a constraint that can only be verified by testing against representative queries. The DoD should reference a test approach.

**Affected story**: US-067
**Suggested action**: Add to the DoD: "A representative set of queries that could elicit legal interpretation (e.g. 'do we have a right of way?') produces responses that describe document content only without legal conclusions."

---

### UC-008: US-071 — "same results" in DoD is ambiguous

"A query submitted via the Phase 2 web UI returns the same results as the same query submitted via the CLI." Results could differ in rendering, ordering, or citation format while the underlying documents and synthesis are identical. It is unclear whether the DoD requires bitwise identical output or equivalent retrieved content. If the intent is that both interfaces use the same retrieval and synthesis logic, this should be stated explicitly.

**Affected story**: US-071
**Suggested action**: Clarify the DoD to specify whether "same results" means identical underlying documents and synthesis, or identical rendered output.

---

### UC-009: US-082 — acceptance criteria are not testable

US-082 (enhanced UI, Phase 2) has two criteria: "Phase 2 enhances the intake form with additional fields and improved usability" and "Phase 2 enhances curation and vocabulary management UI." "Improved usability" has no objective measure. The DoD ("views are improved compared with Phase 1") is equally untestable. This story is effectively a placeholder for Phase 2 scope definition.

**Affected story**: US-082
**Suggested action**: Either mark this story explicitly as a Phase 2 scope placeholder requiring further decomposition before implementation, or replace the criteria with specific enhancements that can be verified. The current criteria cannot be used to confirm the story is done.

---

### UC-010: US-024 — no criterion verifying that fail-fast remains the default

US-024 states "The default (without the flag) remains fail-fast" as an acceptance criterion. This is correct but is not verifiable from this story alone — it requires a test that confirms US-023 (fail-fast) still works as expected after the try-all flag is introduced. The DoD only addresses the try-all path. The regression check against Phase 1 fail-fast behaviour should be explicit.

**Affected story**: US-024
**Suggested action**: Add to the DoD: "Fail-fast behaviour (US-023) is verified unchanged after the try-all flag is introduced."

---

## Internal Inconsistencies

### IC-001: US-006 contains a re-submission criterion that belongs in US-020

US-006 (web UI submission atomicity) includes the criterion: "A subsequent submission of the same document is treated as a fresh first submission." This describes stateless re-submission behaviour following a rejection, which is the subject of US-020 (detect and reject exact duplicate files) and is derived from UR-034. The criterion is misplaced in a story about upload atomicity (UR-008). A developer could implement this criterion at the wrong layer (atomicity mechanism rather than duplicate detection), or implement it twice.

**Affected story**: US-006
**Suggested action**: Remove this criterion from US-006. It is already covered by US-020.

---

### IC-002: Architectural Flags Summary maps UR-017 to two different architectural implications in two different stories

The Architectural Flags Summary table contains two entries for UR-017:

- US-009: "Storage mechanism for accepted files (file copy, reference, or other)"
- US-012: "Bulk ingestion run atomicity and rollback"

UR-017 is the atomicity and rollback requirement. The storage mechanism concern noted in US-009 is not stated in UR-017 — it is an implicit concern that was added to the Architectural Flags Summary without a corresponding requirement. This creates confusion: a developer following the table would flag UR-017 for two separate architectural concerns from two different stories, with no clear way to reconcile them.

**Affected stories**: US-009, US-012
**Suggested action**: Either add a new requirement to cover the storage mechanism concern in US-009 (if it is a genuine distinct concern), or remove the US-009 entry from the Architectural Flags Summary and consolidate the storage mechanism note within US-012 (where atomicity is already flagged).

---

### IC-003: US-030 and US-035 have overlapping criteria on the same behaviour

US-030 (evaluate all pages — no fail-fast within a document) includes the criterion "The flag reason lists all failing pages, not only the first." US-035 (include all failing pages in the flag reason) exists as a separate story with more specific criteria ("the page number and score for each failing page"). The criterion in US-030 partially pre-implements US-035. A developer completing US-030 may believe US-035 is already done, or may implement a less specific version (page list without scores) believing it satisfies both.

**Affected stories**: US-030, US-035
**Suggested action**: Remove the "flag reason lists all failing pages" criterion from US-030 and add a cross-reference to US-035 instead (e.g. "see US-035 for flag reason content requirements").

---

### IC-004: US-046 and US-047 both carry an identical criterion that depends on an unresolved architectural flag

Both US-046 and US-047 contain the criterion: "Processing runs are triggered manually in Phase 1 (see US-048); there is no automatic retry between runs." US-048 has an unresolved architectural flag (UR-070 — trigger surface undefined). The cross-reference in US-046 and US-047 implies these stories can be closed once US-048 is done, but the architectural flag in US-048 blocks that closure. Neither US-046 nor US-047 notes this architectural dependency. A developer could close US-046 and US-047 without the trigger surface being resolved, leaving the cross-referenced criterion unverifiable.

**Affected stories**: US-046, US-047
**Suggested action**: Add a note to the affected criterion in both stories: "This criterion cannot be verified until UR-070 is resolved by the Head of Development (see US-048)."

---

### IC-005: US-051 contains a criterion that belongs in US-053

US-051 (pipeline is re-entrant by design) includes the criterion: "The UI mechanism for clearing a flag is covered by US-079." This criterion does not relate to pipeline re-entrancy. It appears to be a leftover from a previous editing pass. US-053 (clear a flag to mark a document ready to resume) already references US-079. The criterion in US-051 adds noise and could mislead a developer implementing pipeline state tracking.

**Affected story**: US-051
**Suggested action**: Remove the third acceptance criterion from US-051. It is redundant with the cross-reference already present in US-053.

---

### IC-006: US-087 Phase 1 DoD contradicts Phase 1 reality

US-087 (no public or anonymous access at any phase) has the DoD: "The system has no public-facing access; all user access is controlled; self-registration is absent." In Phase 1, there is no authentication and no access control — US-086 explicitly states the system has a single user with no authentication. In Phase 1, "all user access is controlled" is not true in any meaningful sense. The story is labelled Phase 1 but its DoD cannot be satisfied until Phase 2 introduces authentication. This is a contradiction between US-086 and US-087 in Phase 1.

**Affected stories**: US-087, US-086
**Suggested action**: Adjust the DoD to acknowledge Phase 1 reality: in Phase 1 the system is local and single-user (no access control needed); from Phase 2, access is controlled. Alternatively, label this story Phase 2 (where authentication is introduced) and note that the Phase 1 constraint is that no public-facing deployment is intended.

---

## Precision Issues

### PR-001: US-013 and US-069 use "I want to understand that..." framing for constraints

US-013 ("Concurrent bulk ingestion runs are undefined") and US-069 ("Natural language query only in Phase 1 and Phase 2") use the framing "As a..., I want to understand that..." This framing describes informational intent rather than a system capability or constraint. While both stories have testable acceptance criteria, the framing could confuse a developer about whether anything needs to be built (US-013) or just documented. US-069 is less problematic as it has clear criteria.

**Affected stories**: US-013, US-069
**Suggested action**: For US-013, consider reframing as a system constraint rather than a user-facing story: "The system does not implement concurrent run detection in Phase 1; the limitation is documented." For US-069, the framing is acceptable given the testable criteria.

---

### PR-002: US-036 does not address what happens to non-description metadata fields when no detection occurs

US-036 correctly handles the conditional description overwrite (UR-052). However, there is no criterion describing what is stored for non-description metadata fields (document type, dates, people, land references) when the system detects nothing. A developer implementing this story needs to know: are these fields left empty, set to null, or set to a default value? The requirement UR-051 says the system detects these fields automatically, but does not specify what is stored when detection fails. US-037 covers the threshold/flagging aspect, but the storage behaviour for empty detection results is not addressed.

**Affected story**: US-036
**Suggested action**: Add a criterion: "When the system detects no value for a non-description metadata field, that field is stored as empty/null; the intake description is preserved per UR-052."

---

### PR-003: US-038 does not have a criterion for the single-threshold-failure case

US-038 (record both failures as a single flag when both thresholds fail simultaneously) specifies the dual-failure case. There is no criterion confirming that a single-threshold failure also raises exactly one flag. Without this, a developer could implement a combined-failure flag that fires whenever either threshold fails, producing unexpected behaviour in the single-failure case.

**Affected story**: US-038
**Suggested action**: Add a criterion: "When only one threshold fails, a single flag is raised with one reason (not two flags, not a combined-failure flag)."

---

### PR-004: US-042 third criterion could be misread as implying search results use pre-correction metadata

US-042 states "The document remains in the search index with its existing embeddings after a metadata correction." This is accurate but could be misread as implying search results will continue to show the old metadata. The intent is that the document remains findable (not removed from the index), while metadata fields in the display reflect the corrected values. The criterion should distinguish between the embedding content (unchanged) and the metadata fields (updated).

**Affected story**: US-042
**Suggested action**: Restate as: "The document remains in the search index with its existing embeddings unchanged; corrected metadata fields are reflected in the document record and citations on next display."

---

### PR-005: US-048 DoD claims the constraint is "testable independently of the trigger surface" — this is only partially true

The DoD for US-048 states "This constraint is testable independently of the trigger surface." The negative — that processing does not start automatically — can be verified. The positive — that manual triggering works — cannot be verified until the trigger surface is defined (UR-070, unresolved). The DoD overstates the testability of this story in its current state.

**Affected story**: US-048
**Suggested action**: Qualify the DoD: "The negative constraint (processing does not start automatically) is testable in Phase 1. The positive constraint (manual trigger invokes processing) cannot be fully verified until UR-070 is resolved by the Head of Development."

---

### PR-006: US-056 does not specify how supplementary context interacts with the pipeline steps

US-056 (supplementary context, Phase 2) states "Attaching supplementary context allows the document to progress through the pipeline." This does not specify which pipeline steps are skipped and which run using the supplementary context text. A developer implementing this story needs to know: does supplementary context replace extracted text (so embedding runs on supplementary context), or does it supplement the existing (empty) extraction? Without this, two developers could implement incompatible behaviour.

**Affected story**: US-056
**Suggested action**: Add a criterion specifying the pipeline interaction: "Supplementary context text is used as the input to the embedding step; it does not re-run text extraction; the document progresses from the embedding step onward."

---

### PR-007: US-060 criterion "immediately active in the vocabulary" is ambiguous

The criterion "The added term is immediately active in the vocabulary" does not define "active." The DoD clarifies "available to the extraction pipeline on the next processing run" — but the criterion itself says "immediately." These two statements are inconsistent: "immediately" suggests real-time availability, while "on the next processing run" means availability is deferred until the next run. The criterion and DoD should use consistent language.

**Affected story**: US-060
**Suggested action**: Align the criterion with the DoD: "The added term is stored in the vocabulary immediately; it is available to the extraction pipeline from the next processing run."

---

### PR-008: US-064 has no criterion for accepting a candidate that has since become a duplicate

US-064 covers the accept/reject flow for candidates. Deduplication is applied at the point a candidate is raised (US-063), not at the point a curator acts on it. If a curator adds a term manually (US-060) while a matching candidate is pending review, the candidate in the queue is now a duplicate of an accepted term. There is no criterion for how the system handles this race condition at accept time.

**Affected story**: US-064
**Suggested action**: Add a criterion: "If a candidate is accepted that matches a term already in the vocabulary (added after the candidate was raised), the system handles this gracefully — either treating it as a duplicate silently or informing the curator."

---

### PR-009: US-078 criterion "documents awaiting review" is undefined — DoD uses narrower "all flagged documents"

The first acceptance criterion states "The curation queue displays all documents awaiting review or flagged with issues." The DoD says "The curation queue lists all flagged documents." "Awaiting review" and "flagged" may refer to the same set of documents, but this is not stated explicitly. If they differ (e.g. a document could be "awaiting review" without a flag), a developer could implement a broader queue than intended, or the DoD and criteria could diverge.

**Affected story**: US-078
**Suggested action**: Clarify whether "awaiting review" and "flagged" are synonymous in this context. If they are the same set, use consistent terminology in both the criterion and DoD.

---

### PR-010: US-089 specifies "hardcoded to a fixed constant" which is an implementation detail

The criterion "in Phase 1, the submitter identity value is hardcoded to a fixed constant (e.g. 'Primary Archivist') at intake with no runtime selection" specifies an implementation approach (hardcoding) rather than an observable requirement. UR-124 requires the field to exist and be set correctly; it does not prescribe how the value is determined. Specifying "hardcoded" constrains the implementation unnecessarily — the value could equally be read from configuration.

**Affected story**: US-089
**Suggested action**: Replace "hardcoded to a fixed constant" with "set to a fixed value representing the Primary Archivist in Phase 1."

---

### PR-011: US-097 is labelled Phase 1 but its DoD depends entirely on the Head of Development acting

US-097 (database backups) has the DoD: "The Head of Development has defined and documented the backup strategy; the application itself does not implement backups." This story cannot be closed by an implementer — it requires the Head of Development to produce documentation. Labelling it Phase 1 is correct (the strategy must exist before Phase 1 ships), but the story should clarify that it is a Head of Development deliverable, not an implementer deliverable.

**Affected story**: US-097
**Suggested action**: Add a note to the story: "This story is a Head of Development deliverable. The implementer's responsibility is to confirm the strategy exists and is documented; no application code is required."

---
