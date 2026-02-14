# User Stories Review

Reviewed against: `.claude/docs/requirements/user-requirements.md` (approved 2026-02-14)
and `documentation/project/overview.md` (approved 2026-02-14).

This review covers the complete document as it stands. Previous review cycles (cycles 1–3)
are archived. This is cycle 4.

---

## Summary

14 findings. All are precision or completeness issues; no findings require upstream changes
to `overview.md` or `user-requirements.md`.

---

## Findings

### R-001: Story count in document header may be incorrect

**Location**: Header, line 4
**Finding**: The header states "Covers all 137 requirements (UR-001 to UR-137)." It also
states there are 102 stories. Counting the numbered stories (US-001 to US-099 = 99) plus
the lettered additions (US-028a, US-042a) gives 101 stories, not 102. Either the count is
wrong, or there is a story that was not observed during this review.
**Resolution needed**: Verify the story count and update the header to match the actual
total. If a story is missing, identify which requirement it derives from.

---

### R-002: Architectural flag in US-009 not listed in the Architectural Flags Summary table

**Location**: US-009, acceptance criterion 5; Architectural Flags Summary table
**Finding**: US-009 contains an inline architectural flag: "The storage mechanism (file
copy, reference, or other) is an architectural decision `[ARCHITECTURAL FLAG — for Head of
Development]`." This flag does not appear in the Architectural Flags Summary table at the
end of the document. All other inline flags are represented in the table.
**Resolution needed**: Add an entry to the Architectural Flags Summary table for US-009 /
UR-012, noting the storage mechanism as the architectural implication.

---

### R-003: US-016 cross-reference to US-010 does not fully cover the "all files present but none conform" case

**Location**: US-016, acceptance criterion 3; US-010
**Finding**: US-016 criterion 3 states "The case where files are present but none conform to
the naming convention is covered by US-010." US-010 covers individual file rejection and
per-file rejection reasons. UR-026, from which US-016 derives, requires that when "the
source directory is empty or contains no conforming files, the report must still be produced
with zero counts and a note that no files were found." The "zero counts with a note" summary
behaviour for the all-rejected case is not a criterion in US-010, which focuses on per-file
rejection reasons. US-016 only covers the empty directory case in its own criteria.
**Resolution needed**: Either extend US-016 to explicitly cover the all-files-present-but-
none-conform case (zero accepted, report produced with note), or add a criterion to US-010
that addresses the summary-level behaviour when all files are rejected for naming reasons.
The cross-reference as written overstates US-010's coverage.

---

### R-004: US-036 criterion 3 introduces precision not in the requirements

**Location**: US-036, acceptance criterion 3
**Finding**: Criterion 3 states: "When the system detects no value for a non-description
metadata field, that field is stored as empty." UR-051 and UR-052 state what happens with
description detection (conditional overwrite) but do not specify the storage representation
for undetected non-description fields (empty string, null, absent field, or other). Stating
"stored as empty" adds implementation precision that is not in scope for user stories and
could conflict with an architectural or schema decision.
**Resolution needed**: Remove the precision about storage representation or qualify it as an
implementation decision. The criterion's intent (the field is not populated when nothing is
detected) can be expressed without specifying the storage form.

---

### R-005: US-030 Definition of Done references failing pages but US-030 derives from UR-044 only

**Location**: US-030, Definition of done
**Finding**: The DoD states: "After extraction, all pages have scores; a document with
multiple failing pages lists all of them in the flag reason." The second clause (listing all
failing pages in the flag reason) is from UR-050, which is the source of US-035, not
US-030. US-030 derives from UR-044 only (all pages evaluated, no fail-fast). The flag
reason content requirement belongs in US-035's DoD, not US-030's.
**Resolution needed**: Remove the second clause from the US-030 DoD, or add a cross-
reference to US-035. The DoD should only verify what UR-044 requires: that all pages have
scores after extraction, not that the flag reason is correct.

---

### R-006: US-035 acceptance criterion uses "page number and score" — this detail is not in the requirements

**Location**: US-035, acceptance criterion 1
**Finding**: The criterion states: "The flag reason for a text quality failure includes the
page number and score for each failing page." UR-050 states: "The flag reason for a text
quality failure must include the full list of failing pages." The requirement specifies that
failing pages are listed; it does not specify that the score is also included in the flag
reason. Including the score in the flag reason is a reasonable design choice but is
implementation precision beyond the requirement.
**Resolution needed**: Either align the criterion to "page number" only (per UR-050) or
explicitly note that including the score is an implementer decision not mandated by the
requirement.

---

### R-007: US-047 and US-046 share an identical note about manual trigger verification

**Location**: US-046 acceptance criterion 5; US-047 acceptance criterion 5
**Finding**: Both stories include the identical criterion: "Processing runs are triggered
manually in Phase 1 (see US-048); there is no automatic retry between runs; this criterion
cannot be fully verified until UR-070 is resolved by the Head of Development." The criterion
is appropriate in US-047 (retry depends on trigger mechanism) but its presence in US-046
(which is about step completion recording, not retry) is less clear. US-046's fifth
criterion conflates step-completion recording with the trigger mechanism, which is a
separate concern.
**Resolution needed**: In US-046, remove or narrow the fifth criterion to only the part
relevant to step completion (i.e. that processing does not automatically start). The
cross-reference to US-048 is sufficient; the manual trigger note in full does not belong
in a story about pipeline state recording.

---

### R-008: US-051 Definition of Done states "must be resolved before this story can be closed" but the story is Phase 1

**Location**: US-051, Definition of done
**Finding**: The DoD states: "The pipeline state tracking mechanism is defined by UR-074
`[ARCHITECTURAL FLAG — for Head of Development]` and must be resolved before this story can
be closed." This is correct, but because US-051 is Phase 1, there is a dependency ordering
risk: if UR-074 is not resolved before Phase 1 implementation begins, US-051 cannot be
closed. This dependency is not called out in a way that distinguishes it from stories where
the architectural flag is informational only.
**Resolution needed**: Add a note to US-051 making explicit that this is a hard blocking
dependency — US-051 cannot be implemented until UR-074 is resolved by the Head of
Development. This distinguishes it from architectural flags that are informational context
only (e.g. US-040, where the flag describes a format choice but does not block story closure).

---

### R-009: US-048 Definition of Done mixes negative and positive constraint verification inconsistently

**Location**: US-048, Definition of done
**Finding**: The DoD states: "Processing does not start automatically in Phase 1; manual
triggering is the only mechanism. The negative constraint (processing does not start
automatically) is testable in Phase 1. The positive constraint (manual trigger invokes
processing) cannot be fully verified until UR-070 is resolved by the Head of Development.
The story cannot be fully closed until UR-070 is resolved and the trigger surface is
implemented and tested." This is accurate and thorough, but inconsistent with US-051's DoD
(finding R-008 above), which uses a less prominent phrasing. Both stories have the same
blocking architectural dependency but communicate it differently.
**Resolution needed**: Align the phrasing between US-048 and US-051 so that blocking
dependencies on architectural flags are stated consistently. One of the two formulations
should be standardised and applied to both.

---

### R-010: US-064 cross-reference to UR-094 omits the rejected-terms persistence criterion source

**Location**: US-064, acceptance criterion 4
**Finding**: Criterion 4 states: "The rejected-terms list is stored in the database and
persists across system restarts; it is not an in-memory structure that resets on restart."
This is consistent with UR-092 (deduplication against a persisted rejected-terms list) but
the criterion is in US-064, which derives from UR-094 only. The persistence requirement
originates from UR-092, the source of US-063. Adding a persistence criterion to US-064
without a cross-reference to US-063 or UR-092 creates an implicit dependency that is not
traceable.
**Resolution needed**: Either move the persistence criterion to US-063 (UR-092 source),
add a cross-reference from US-064 to US-063 for this criterion, or add UR-092 to the
"Derived from" field of US-064.

---

### R-011: US-067 Definition of Done includes a test-framing clause that implies automated testing for a non-automated concern

**Location**: US-067, Definition of done
**Finding**: The DoD includes: "a representative set of queries that could elicit legal
interpretation (e.g. 'do we have a right of way?') produces responses that describe
document content only without legal conclusions." This is a reasonable verification
approach but the phrasing "a representative set of queries" leaves the verification method
ambiguous — it could be read as a test suite or as a human review exercise. The story
involves LLM behaviour, which is probabilistic and not reliably covered by a fixed test
set.
**Resolution needed**: Clarify whether this verification is human review (manually run a
set of queries and review the responses) or an automated test. If human review, use
language consistent with US-044's DoD ("reviewed against at least two... confirms no...
records the review outcome"). If this is considered untestable in an automated sense, note
that.

---

### R-012: US-082 (Phase 2 scope placeholder) does not note that the story is also the derivation point for UR-115

**Location**: US-082, story body
**Finding**: US-082 derives from UR-115 and is a Phase 2 scope placeholder. The note says
"The specific enhancements are to be defined during Phase 2 scope definition." This is
consistent with the treatment of US-021. However, unlike US-021, US-082 has two concrete
acceptance criteria rather than a single placeholder criterion. The two AC items ("Phase 2
enhances the intake form with additional fields and improved usability" and "Phase 2
enhances curation and vocabulary management UI") are not testable as stated — they describe
outcomes that require Phase 2 scope definition before they can be verified.
**Resolution needed**: Either (a) reframe the two ACs as non-testable scope indicators
with a note that they will be decomposed, or (b) apply the same placeholder AC treatment
used in US-021 ("Content-based duplicate detection is implemented in the phase assigned to
this story"). The current formulation is inconsistent with how other Phase 2 placeholders
are structured.

---

### R-013: US-009 derives from UR-012 and UR-021 but not UR-013 or UR-014 — naming convention requirement is split across stories

**Location**: US-009, "Derived from" field; US-010, "Derived from" field
**Finding**: US-009 derives from UR-012 and UR-021. UR-013 (naming convention enforcement)
and UR-014 (filename parsed into metadata) are the source of US-010. This split is correct
as a structural matter, but US-009's DoD ("Running the CLI command with a valid source
directory stores accepted files in the archive") does not clarify that "valid source
directory" means the files must conform to the naming convention to be accepted. A reader
of US-009 alone might not understand that the naming convention is a precondition to
acceptance. The cross-reference between US-009 and US-010 is missing.
**Resolution needed**: Add a cross-reference in US-009 noting that naming convention
enforcement (the gate for "valid" files) is covered by US-010.

---

### R-014: US-023 does not specify how a "not attempted" outcome is reported for a rejected group in the web UI context

**Location**: US-023, acceptance criteria
**Finding**: US-023 criterion 3 states "Phase 1 uses fail-fast validation: processing stops
on the first failure" and criterion 4 states "Files not reached due to fail-fast are
reported with outcome 'not attempted'." The story context is bulk ingestion (UR-036 and
UR-037 both reference bulk ingestion). However UR-035 now restricts virtual document
grouping to CLI only in Phase 1 (web UI grouping deferred to Phase 2). US-023 makes no
mention of this restriction; a reader might not know that group validation with "not
attempted" reporting is a bulk ingestion CLI concern only in Phase 1.
**Resolution needed**: Add a note to US-023 clarifying that virtual document grouping is
CLI-only in Phase 1 (per US-022 and UR-035), so the "not attempted" outcome applies only
to bulk ingestion in Phase 1.

---

## Non-Findings (items examined and found acceptable)

- **US-021 (Phase Future placeholder)**: Structure is consistent with how Phase Future
  stories are handled; no implementation expected.
- **US-024 default behaviour deferral**: "default validation behaviour determined during
  Phase 2 implementation" — consistent with the decisions in cycle 2 notes.
- **US-039 architectural flag ACs**: Reframed as observable outcomes with architectural
  flags; consistent with cycle 3 decisions.
- **US-090 Primary Archivist protagonist**: Intentional; documented in the Note block
  per cycle 3 decisions.
- **US-097 Head of Development deliverable note**: Consistent with cycle 2 decisions.
- **All "Phase 1" / "Phase 2" / "Phase 3" / "Phase Future" phase labels**: All checked;
  each aligns with the corresponding requirement priority and phase assignment.
- **All derived-from fields**: Spot-checked against the requirements document; mappings
  are accurate throughout.
