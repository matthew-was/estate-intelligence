# User Stories Review — Phase 1

Review date: 2026-02-17
Document reviewed: `.claude/docs/requirements/phase-1-user-stories.md`
Upstream documents:

- `documentation/project/overview.md` (approved 2026-02-17)
- `.claude/docs/requirements/user-requirements.md` (approved 2026-02-17)

Reviewer: Product Owner agent

---

## Review scope

This is a final pre-approval review following two corrections applied immediately before this session:

1. US-007 `Derived from: UR-010` corrected to `Derived from: UR-011`
2. Document header date updated from `2026-02-14` to `2026-02-17`

The review checks:

- All "Derived from" UR references against the approved user-requirements.md
- All story content against the approved requirements and overview
- Coverage completeness (all 138 requirements represented)
- Any other issues found during inspection

---

## Coverage check

All 138 requirements (UR-001 to UR-138) are represented in the document. No requirement is unrepresented.

UR-043 is split across two stories (US-028 for Phase 1 document types, US-029 for Phase 2 document types) — this split is intentional and correct.

UR-062 is split across two stories (US-043 for Phase 1 metadata-only correction, US-044 for Phase 2 re-embedding trigger) — this split is intentional and correct.

UR-093 appears in both US-065 (deduplication check) and US-066 (accept/reject action with rejected-terms persistence) — the dual citation is legitimate because UR-093 contains both the deduplication logic and the rejected-terms persistence requirement.

---

## Derived-from reference check

All "Derived from" references have been checked against the approved user-requirements.md. The two corrections noted in the review scope (US-007 from UR-010 → UR-011) are correctly applied in the current document.

One discrepancy was found and is raised as a finding below.

---

## Findings

### F-001: US-066 — UR-092 missing from "Derived from" field

**Severity**: Minor — does not affect story content or acceptance criteria

**Location**: US-066 "Accept or reject a vocabulary candidate", line ~1308

**Observation**: The cycle 4 review resolution (documented in project memory) states: "US-066 criterion 4: UR-092 added to derived-from; cross-reference to US-065 added." The cross-reference to US-065 is present in criterion 4 ("see also US-065"). However, UR-092 is not in the "Derived from" field, which currently reads "Derived from: UR-093, UR-095".

**Analysis**: On content grounds, UR-092 ("Accepted vocabulary terms must be independent of the documents that surfaced them and must not be affected by out-of-band document removal") is squarely US-064's territory, not US-066's. US-066 covers the accept/reject action and rejected-terms persistence. There is no acceptance criterion in US-066 that derives from UR-092. Adding UR-092 to US-066's "Derived from" field would be misleading — it would suggest US-066 covers source-document independence, which it does not.

**Conclusion**: The project memory's cycle 4 note may be inaccurate, or the UR-092 addition may have been deliberately deferred and not recorded as deferred. The current document state (without UR-092 in US-066) appears correct on content grounds. However, since the memory explicitly records this as a resolved finding, the Developer should confirm whether UR-092 belongs in US-066's "Derived from" field or whether the cycle 4 note was an error.

**Action required**: Developer to confirm whether UR-092 should be added to US-066's "Derived from" field. If not, no change is needed. If yes, the field should be updated to "Derived from: UR-092, UR-093, UR-095".

---

## Content review findings

No content issues were found. The following checks passed:

**Consistency with overview.md**

- Web UI as primary intake for Phase 1, CLI for query and bulk ingestion — correctly reflected throughout
- Phase 1 single-user, no authentication — US-088 correct
- Document types by phase (PDF, TIFF, JPEG, PNG in Phase 1; DOCX, EML in Phase 2) — US-005 and US-007 correct
- Bulk ingestion atomicity and rollback — US-012 correct
- Virtual document groups — CLI-only in Phase 1 per US-022 and US-023; note present in US-023
- Fail-fast vs try-all — Phase 1 fail-fast (US-023), Phase 2 try-all option (US-024), consistent
- Naming convention enforcement — US-010 correct, cross-reference to US-010 present in US-009
- Agentic semantic chunking — US-046 correct with hard blocking note
- Vocabulary as a structured record — US-061 correct
- Curation via minimal web UI in Phase 1 — US-078 correct, not CLI
- CLI query at all phases, not deprecated — US-070 correct
- No in-app document removal in Phase 1 or Phase 2 — US-083 correct, Phase 2 regression check present
- Single web application for upload, curation, vocabulary management — US-086 correct
- Submitter identity: present from Phase 1, visible in curation queue only — US-091 correct

**Consistency with user-requirements.md**

- UR-010 (description validation): covered by US-003b, correctly derived, correctly absent from US-007's derivation
- UR-053 (conditional description overwrite): US-037 criteria correctly reflect "overwrites if detected, preserves intake description if not detected"
- UR-055 (dual-failure single flag): US-039 correctly specifies a single flag with both reasons, not two flags
- UR-062 (Phase 1 metadata-only, Phase 2 re-embedding): US-043 and US-044 correctly split on phase boundary
- UR-078/079 (flag clearing): US-055 correctly specifies that clearing does not trigger processing and clears the reason field
- UR-081 (queue ordering): US-057 correctly specifies ascending (oldest-flagged first)
- UR-090 (queue ordering): US-063 correctly specifies ascending (oldest-raised first)
- UR-094 (alias-append deduplication): US-065 correctly specifies silent ignore for duplicate aliases
- UR-095 (accept/reject): US-066 correctly specifies both actions, with rejected-terms persistence from UR-093 noted
- UR-115 (no in-app removal, user type "—"): US-083 uses Primary Archivist protagonist with Note block explaining the scope constraint framing; consistent with the convention note in the document header
- UR-123 (no public access, user type "—"): US-089 uses Primary Archivist protagonist with appropriate scope constraint framing; consistent
- UR-132 (replace/delete, user type "—"): US-095 uses "As a user with appropriate permissions" which correctly reflects the open question about which user type(s) gain this in Phase 3

**Phase assignments**

All phase assignments have been checked against the priority and phase language in user-requirements.md:

- `Must` Phase 1 requirements → Phase 1 stories: all correct
- `Should` Phase 2 requirements → Phase 2 stories: all correct
- `Should` Phase 3 requirements → Phase 3 stories: all correct
- `Could` requirements (UR-034, UR-104) → Phase Future stories: all correct

**Architectural Flags Summary table**

The table contains 16 entries. All 15 requirements flagged as `[ARCHITECTURAL FLAG]` in user-requirements.md are represented. The additional entry (US-009/UR-013 — storage mechanism) was correctly added as a story-level flag for an architectural decision not explicitly flagged at the UR level.

**Hard blocking dependency notes**

All six hard blocking dependency notes required by the cycle 4 resolution are present:

- US-009 (storage mechanism — UR-013)
- US-012 (rollback mechanism — UR-018)
- US-022 (CLI group expression — UR-036)
- US-042 (archive reference derivation — UR-061)
- US-046 (AI chunking agent — UR-064)
- US-060 (vocabulary schema and seed — UR-086)

**Cycle 4 changes verified**

The following cycle 4 resolutions are confirmed correctly applied:

- US-016 criterion 3: "report format is the same as for a normal run" makes all-rejected summary behaviour explicit, not delegated to US-010 ✓
- US-037 criterion 4: uses "not populated" (not "stored as empty") ✓
- US-031 DoD: no stray "flag reason lists all failing pages" clause ✓
- US-048 criterion 5: concise cross-reference to US-050 ✓
- US-050 and US-053: hard blocking dependency notes present ✓
- US-066 criterion 4: "see also US-065" cross-reference present ✓ (UR-092 in Derived from: see F-001)
- US-069 DoD: human review made explicit; review outcome recording required ✓
- US-084 acceptance criteria: collapsed to single placeholder criterion ✓
- US-009: cross-reference to US-010 present in criterion 3 ✓
- US-023: note added confirming group validation is CLI bulk ingestion only in Phase 1 ✓
- Architectural Flags Summary table: US-009/UR-013 entry present ✓
- Full renumber (US-028a → US-029, US-042a → US-044): applied; all IDs post-US-028 are consistent ✓

---

## Summary

One finding (F-001): a potential discrepancy between the project memory's cycle 4 resolution record and the current document regarding whether UR-092 should appear in US-066's "Derived from" field. On content grounds the current document appears correct — UR-092 is US-064's territory, not US-066's. Developer confirmation is needed.

No coverage gaps. No content inconsistencies with either approved upstream document. All cycle 4 changes verified as applied. The document is otherwise clean and ready for Developer approval once F-001 is confirmed.

**DO NOT APPROVE** — approval is the Developer's action only.
