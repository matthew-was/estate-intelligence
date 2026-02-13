# Product Owner Review — overview.md

**Review number**: 10
**Date**: 2026-02-13
**Reviewer**: Product Owner agent
**Document reviewed**: `documentation/project/overview.md`
**Approval status at review start**: Unapproved (unapproved 2026/02/13 13:58 — scope change in progress)

---

## Summary

The document is comprehensive and internally coherent across most of its scope. Nine prior review cycles
have resolved a large volume of detail. This review identifies six issues that should be resolved before
the document is approved and user requirements are written. None are structural problems; all are specific
gaps or ambiguities in defined behaviour.

---

## Issues

### 1. Duplicate detection scope — across runs or within a run only?

**Category**: Missing information

**Location**: Phase 1 Must have, duplicate detection bullet (approximately line 66)

**Current text**: "Detect and reject exact duplicate files by file hash; hash-based duplicate detection
applies to individual files regardless of whether they are submitted standalone or as part of a virtual
document group."

**Issue**: The document does not state whether duplicate detection is checked against:

- Only the files submitted in the current run (within-run deduplication), or
- The full history of previously accepted files in the system (cross-run deduplication), or
- Both.

This materially affects the behaviour. If a file submitted in Run 1 is submitted again in Run 2, should
Run 2 reject it as a duplicate? The document is silent. This needs to be stated explicitly — it is a
scope decision, not an architectural one.

**Question for resolution**: Does file hash duplicate detection operate against the full archive of
previously accepted files, within a single run only, or both?

---

### 2. Summary report content for un-attempted files in a rejected group

**Category**: Ambiguity / contradiction

**Location**: Phase 1 Must have — summary report bullet and virtual document group bullet

**Current text (summary report)**: "a summary header (total submitted, accepted, rejected) followed by
a per-file record of filename, outcome, and rejection reason where applicable"

**Current text (group validation)**: "Phase 1 uses fail-fast validation: processing stops on the first
failure and remaining files are reported as not attempted; only failing files are reported with their
reasons — passing files are not listed individually"

**Issue**: These two statements are in tension. The summary report specifies "a per-file record" for
the run. The group validation rule says "only failing files are reported" — which implies un-attempted
files (those not reached because fail-fast stopped at an earlier failure) are not listed. But the
summary report format implies all files submitted appear in the per-file section.

For a group of three files where file 2 fails and file 3 is never evaluated:

- Does file 3 appear in the summary report with outcome "not attempted"?
- Or is file 3 omitted entirely from the per-file section?

The answer affects how the summary report is written and what the user sees. This needs to be
disambiguated.

**Question for resolution**: For files in a rejected group that were never evaluated (fail-fast),
do they appear in the summary report with outcome "not attempted", or are they omitted from the
per-file section entirely?

---

### 3. Vocabulary candidates raised by subsequently flagged documents

**Category**: Missing information / edge case

**Location**: Phase 1 Must have — vocabulary bullet (approximately line 81)

**Current text**: "during document processing, candidate terms are proposed automatically and surfaced
in a separate vocabulary review queue immediately as each document completes processing"

**Issue**: The document states candidates are surfaced immediately on step completion. But if a later
step fails and the document is flagged, vocabulary candidates raised by earlier steps remain in the
review queue. The document does not address this scenario.

Two questions:

(a) If a document raises vocabulary candidates and is then flagged (for a quality or technical reason),
do the candidates remain in the vocabulary review queue, or are they withdrawn pending resolution?

(b) If a curator accepts vocabulary candidates from a document that is later removed out-of-band (direct
storage deletion), the vocabulary retains those terms. Is this acceptable, or should vocabulary
candidates be tied to document state?

These are scope decisions. Withdrawing candidates when a document is flagged would be a coupling
between the document pipeline and the vocabulary queue — leaving them in place would be simpler but
could introduce noise. The document needs to state the intended behaviour.

**Question for resolution**: Do vocabulary candidates raised during processing remain in the review
queue if the source document is subsequently flagged or removed? Or are they withdrawn?

---

### 4. Phase 2 metadata correction — does it trigger re-embedding?

**Category**: Ambiguity

**Location**: Phase 1 Must have — curation bullet (approximately line 84); Phase 2 Adds section

**Current text (Phase 1)**: "correcting metadata updates the metadata fields only and does not trigger
re-embedding; metadata correction triggering re-embedding is deferred to Phase 2 or 3"

**Current text (Phase 2)**: "Reprocess documents after human correction or supplementary context is
added — Phase 2 introduces an automated trigger for the same processing pipeline"

**Issue**: The Phase 1 note says re-embedding on metadata correction is deferred to "Phase 2 or 3."
The Phase 2 description says reprocessing is triggered "after human correction or supplementary
context is added" — "human correction" plausibly means metadata correction.

These two statements are consistent if Phase 2 triggers re-embedding on metadata correction. But "Phase
2 or 3" in the Phase 1 note creates genuine uncertainty about whether Phase 2 includes this, or whether
it only includes reprocessing triggered by supplementary context.

This ambiguity would cause the Phase 2 requirements to be written without a clear answer to a core
question. The "or 3" hedge should be resolved.

**Question for resolution**: Does Phase 2 trigger re-embedding when metadata is corrected, or only
when supplementary context is added? Is metadata-correction re-embedding a Phase 2 or Phase 3 feature?

---

### 5. Accepted vocabulary terms — no edit or delete path stated

**Category**: Missing information

**Location**: Phase 1 Must have — vocabulary bullet; curation section

**Current text**: "The vocabulary can be extended manually via the curation web UI at any time" and
"the curator accepts (adds to vocabulary) or rejects (adds to rejected list) each remaining candidate"

**Issue**: The document describes how terms enter the vocabulary (manually added or accepted from
candidates) and how candidates are rejected (added to rejected list). But it does not state whether
accepted or manually-added vocabulary terms can be edited or deleted in Phase 1.

If the curator accepts a term with an error in the description, or adds a term manually with a typo,
what is the resolution path? This is a scope question — if editing and deleting accepted terms is out
of scope for Phase 1, this should be stated explicitly so that requirements do not inadvertently include
it.

**Question for resolution**: Can accepted or manually-added vocabulary terms be edited or deleted via
the curation web UI in Phase 1? If not, this should be stated as explicitly out of scope.

---

### 6. Alias deduplication — handling of already-present aliases

**Category**: Edge case / missing information

**Location**: Phase 1 Must have — vocabulary bullet (approximately line 81)

**Current text**: "when a candidate matches an accepted term after normalisation, it is suppressed from
the review queue and the normalised variant is appended to the aliases list on the existing term"

**Issue**: If the normalised variant is already present in the aliases list, would it be appended again,
creating a duplicate alias? The document does not state whether the alias-append step itself performs
deduplication.

This is a minor edge case but affects the data integrity requirement for vocabulary records.

**Question for resolution**: When appending a normalised alias to an existing term, is a check
performed to avoid duplicating an alias that is already present?

---

## Assessment

The document cannot be approved in its current state due to issues 1–5. Issue 6 is minor and could
be resolved with a brief clarifying sentence.

Issue 1 (duplicate detection scope) is the highest priority — it defines a core data integrity
behaviour. Issue 4 (Phase 2 metadata re-embedding) is the second priority — it affects how Phase 2
requirements are framed.

Issues 2, 3, 5, and 6 are resolvable with brief clarifying additions to existing bullet points.

No structural problems were found. The document's overall scope, phase structure, user table,
format table, design constraints, and query section are all clear and consistent.
