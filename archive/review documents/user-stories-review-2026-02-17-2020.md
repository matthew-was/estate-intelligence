# User Stories Review

Reviewed against:

- `documentation/project/overview.md` (approved 2026-02-14)
- `.claude/docs/requirements/user-requirements.md` (approved 2026-02-14)
- `.claude/docs/requirements/phase-1-user-stories.md` (unapproved — under review)

Review cycle: 5 (post-cycle-4 approval review)

---

## Coverage Check

All 137 requirements (UR-001 to UR-137) are covered by at least one story. All 101 stories (US-001 to US-101) carry a phase assignment and a definition of done. No coverage gaps found.

---

## Findings

### R-001: US-002 criterion 3 introduces a requirement not backed by any UR

**Story**: US-002 (Provide date and description at intake)
**Criterion**: "Submission is not possible unless the date field contains a valid date (per US-003) and the description field contains a non-empty string"
**Severity**: Substantive

US-002 criterion 3 requires that the description field must contain a non-empty string before submission proceeds. No requirement in `user-requirements.md` specifies this behaviour. UR-002 says the form must "capture date and description fields at minimum" — it does not say description must be non-empty. UR-003 establishes date validation as a blocking error but covers date only.

The non-empty description rule was a decision made in a cycle 2 review, but it was not reflected in `user-requirements.md` as a requirement. It is therefore a story-level addition without requirement backing.

Additionally, US-003 establishes the behaviour for invalid date: "rejected and the user is prompted to correct it... enforced client-side and server-side". No equivalent story or criterion establishes what happens when the description field is empty: whether the submission is rejected, how the user is informed, whether enforcement is client-side, server-side, or both, and what the error message says. The non-empty description rule is stated as a gate in US-002 criterion 3 but the validation behaviour (error message, enforcement level) is left undefined.

**Decision required**: Confirm whether empty description must block submission (and add a UR if so), or relax criterion 3 to reflect what UR-002 actually requires.

---

### R-002: US-065 does not state the explicit outcome when a candidate matches the rejected-terms list

**Story**: US-065 (Deduplicate vocabulary candidates by normalised comparison)
**Criterion**: Criterion 1 — "Candidate deduplication is performed against both the accepted vocabulary and the rejected-terms list before a candidate is raised"
**Severity**: Minor precision

UR-092 requires deduplication against both the accepted vocabulary and the persisted rejected-terms list. UR-093 specifies the outcome when a candidate matches an accepted term: suppressed from queue, and normalised variant appended to aliases if not already present.

US-065 covers the accepted-term match case in criteria 3–5. However, no criterion states the outcome when a candidate matches the rejected-terms list specifically — the outcome is different (suppressed from queue, no alias appending). Criterion 1 says deduplication runs against both lists "before a candidate is raised", which implies suppression, but an implementer comparing rejected-list matching against accepted-term matching could wrongly attempt alias appending in both cases.

**Decision required**: Confirm that a candidate matching the rejected-terms list is suppressed without alias appending and add a criterion to that effect, or confirm that criterion 1 is sufficient as written.

---

### R-003: Two architectural flags appear in the stories summary table but not in user-requirements.md

**Stories**: US-009 (UR-012), US-022 (UR-035)
**Location**: Architectural Flags Summary table (end of stories document) vs. Architectural Flags section of `user-requirements.md`
**Severity**: Substantive

The Architectural Flags Summary in the stories document lists 16 entries. The Architectural Flags section of `user-requirements.md` lists 14 entries. Two entries in the stories table — US-009/UR-012 (storage mechanism for accepted files) and US-022/UR-035 (CLI mechanism for expressing a virtual document group) — do not appear in `user-requirements.md`.

Both flags were added to the stories during earlier review cycles. Neither was added back to `user-requirements.md`. The requirements document is the authoritative source for architectural implications passed to the Head of Development. If these flags are not in the requirements document, they may be overlooked.

**Decision required**: Either add UR-012 and UR-035 to the Architectural Flags section of `user-requirements.md` (which would require a requirements document update and re-approval), or confirm the current split is acceptable and that the stories architectural flags table is treated as a supplementary source alongside the requirements table.

---

### R-004: Inconsistent regression check language across multi-phase constraint stories

**Stories**: US-070, US-071 (explicit regression checks) vs. US-083 criterion 1, US-089 DoD (Phase 2 assertions without regression check language)
**Severity**: Minor precision

US-070 DoD says: "A regression check is performed at Phase 2 delivery to confirm the CLI remains functional and unchanged after Phase 2 deploys web UI query."

US-071 criterion 2 says: "No structured filtering options are introduced in Phase 2 — this criterion is verified at Phase 2 delivery as a regression check."

These two stories explicitly name the Phase 2 regression check and state when verification occurs. Two other stories contain Phase 2 assertions without this explicit framing:

- US-083 criterion 1: "No remove, replace, or delete document option is available in the web UI in Phase 1 or Phase 2" — no statement that this is verified at Phase 2 delivery.
- US-089 DoD: "From Phase 2, all user access is controlled via authentication and self-registration is absent" — this is an assertion, not a regression check instruction.

The inconsistency means it is unclear whether US-083 criterion 1 and US-089 DoD are intended to be checked at Phase 2 delivery or are informational only.

**Decision required**: Confirm whether US-083 criterion 1 and US-089 DoD should be updated to use the explicit regression check language established in US-070 and US-071, or confirm the current wording is intentional and sufficient.

---

### R-005: US-016 title overstates the cases the story covers

**Story**: US-016 (Produce a report for an empty or all-rejected source directory)
**Severity**: Minor precision

The title "Produce a report for an empty or all-rejected source directory" implies the story covers all cases where all files are rejected (e.g. all files fail format validation, all files fail size validation). The criteria cover two specific cases only:

- Criterion 1: source directory is empty
- Criterion 2: files are present but none conform to the naming convention

A directory where all files pass the naming convention but all fail format or size validation is a different case. That case produces a report with non-zero submitted and rejected counts via the normal report mechanism (US-014), not via this story's zero-count mechanism. The current title could lead an implementer to treat US-016 as the handler for all all-rejected scenarios.

**Decision required**: Retitle to something like "Produce a report when the source directory is empty or contains no conforming files" to match the criteria, or confirm the current title is acceptable.

---

### R-006: US-039 criterion 2 imprecise about the full list of failing pages

**Story**: US-039 (Record both failures as a single flag when both thresholds fail)
**Criterion**: Criterion 2 — "The flag reason includes the text quality failure (with failing pages) and the metadata completeness failure"
**Severity**: Minor precision

US-036 requires "the flag reason for a text quality failure includes the page number for each failing page; no failing page is omitted from the flag reason." This establishes the full-list requirement for standalone text quality flags.

US-039 criterion 2 uses "with failing pages" rather than "with the full list of failing pages" or a cross-reference to US-036. An implementer reading US-039 in isolation could reasonably include some failing pages rather than all, satisfying "with failing pages" without satisfying the full-list requirement in US-036.

**Decision required**: Add a cross-reference to US-036 in criterion 2 (e.g. "the flag reason includes the text quality failure with the full list of failing pages per US-036") or confirm the current wording is sufficient.

---

## Summary

| ID | Story | Severity | Type |
| --- | --- | --- | --- |
| R-001 | US-002 criterion 3 — description non-empty rule not backed by a UR, validation behaviour undefined | Substantive | Missing requirement coverage |
| R-002 | US-065 — rejected-terms list match outcome not explicitly stated | Minor precision | Incomplete criteria |
| R-003 | US-009/UR-012 and US-022/UR-035 in stories arch flags table but not in requirements arch flags table | Substantive | Cross-document inconsistency |
| R-004 | US-083, US-089 — Phase 2 assertions without explicit regression check language | Minor precision | Inconsistent pattern |
| R-005 | US-016 — title broader than criteria | Minor precision | Misleading title |
| R-006 | US-039 criterion 2 — "with failing pages" imprecise; no cross-reference to US-036 | Minor precision | Imprecise criterion |

Two findings (R-001 and R-003) are substantive and require a decision before approval. Four findings (R-002, R-004, R-005, R-006) are minor precision issues.
