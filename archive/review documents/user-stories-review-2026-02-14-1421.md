# User Stories Review

Review of: `.claude/docs/requirements/phase-1-user-stories.md`
Against: `.claude/docs/requirements/user-requirements.md` (approved 2026-02-14)
Against: `documentation/project/overview.md` (approved 2026-02-14)
Date: 2026-02-14

---

## Summary

All 137 requirements (UR-001 to UR-137) are covered by at least one story. No requirements are missing. The review identifies 12 findings across five categories: user type mismatches, untestable or process-oriented acceptance criteria, architectural assumptions embedded in story criteria, misleading story framing, and one missing architectural flag entry.

---

## Finding Index

| ID | Category | Story | Severity |
| --- | --- | --- | --- |
| R-001 | User type mismatch | US-090 | Medium |
| R-002 | User type mismatch | US-087, US-094, US-095, US-096, US-097, US-098, US-099 | Low |
| R-003 | Untestable criteria | US-039 | Medium |
| R-004 | Untestable DoD | US-044 | Low |
| R-005 | Architectural assumption in story | US-056 | Medium |
| R-006 | Misleading framing | US-069, US-081, US-085, US-013 | Low |
| R-007 | Unverifiable criterion at phase close | US-069 | Low |
| R-008 | Misleading criterion | US-042 | Low |
| R-009 | Missing architectural flag in summary table | US-039 | Low |
| R-010 | Ambiguous queue scope | US-078 | Low |
| R-011 | Phase Future label on a Could requirement | US-021 | Low |
| R-012 | Incomplete coverage note in DoD | US-068 | Low |

---

## Findings

### R-001 — User type mismatch: US-090

**Story**: US-090 (Derived from: UR-126, UR-130)
**Category**: User type mismatch
**Severity**: Medium

US-090 is written as "As a Primary Archivist, I want a System Administrator role introduced in Phase 3..."
Both UR-126 and UR-130 assign user type "System Administrator", not "Primary Archivist".

The System Administrator is the user who performs user account management and manages infrastructure. The Primary Archivist benefits from the separation of concerns but is not the actor performing these tasks. The story's protagonist should be the System Administrator (the user who gains and exercises the capability), not the Primary Archivist.

As written, the story implies the Primary Archivist is the user who manages accounts and infrastructure, which is the opposite of the requirement's intent.

**Suggested action**: Change the story protagonist to System Administrator. The "benefit" clause (so that...) can reference the separation from Archivist responsibilities.

---

### R-002 — User type mismatch: system-wide requirements attributed to Primary Archivist

**Stories**: US-087, US-094, US-095, US-096, US-097, US-098, US-099
**Category**: User type mismatch
**Severity**: Low

The following requirements carry user type `—` (system-wide, not tied to any user):

| Story | Requirement | Requirement user type |
| --- | --- | --- |
| US-087 | UR-122 | `—` |
| US-094 | UR-132 | `—` |
| US-095 | UR-133 | `—` |
| US-096 | UR-134 | `—` |
| US-097 | UR-135 | `—` |
| US-098 | UR-136 | `—` |
| US-099 | UR-137 | `—` |

All seven stories use "As a Primary Archivist" as the protagonist. For system-wide constraints (no public access, provider abstraction, configuration file, actionable errors, backups, minimal schema, non-destructive migrations) this is pragmatic but imprecise. The constraints apply regardless of user type and are not privileges or capabilities of the Primary Archivist specifically.

This is low severity because user stories for non-functional requirements commonly adopt a representative user type. However, it means the stories could be interpreted as constraining these properties to the Primary Archivist's experience only.

**Suggested action**: Acknowledge as a known simplification, or adopt a consistent convention such as "As a system operator" or "As any user" for non-functional requirements, or leave as-is with a note in the document header.

---

### R-003 — Untestable acceptance criteria: US-039

**Story**: US-039 (Derived from: UR-056)
**Category**: Untestable acceptance criteria
**Severity**: Medium

US-039 acceptance criteria read:

> The metadata fields used in the completeness assessment are determined during implementation, informed by corpus analysis
> The scoring method is determined during implementation, informed by the extraction tooling selected

These are process obligations (things the implementer will decide during implementation) rather than system behaviours that can be verified against a built system. Acceptance criteria for user stories should describe observable system behaviour that a tester can verify.

The DoD partially addresses this by saying "the implementer has defined which fields contribute to the completeness score and how the score is calculated, and has documented this decision before US-037 is closed" — but this is a documentation check, not a system behaviour test.

UR-056 is an architectural flag, and the decision is genuinely deferred. The issue is that the acceptance criteria describe the decision-making process, not the resulting system behaviour.

**Suggested action**: Reframe acceptance criteria as observable outcomes: e.g. "The completeness assessment evaluates a defined set of metadata fields (documented by the implementer before US-037 closes)"; "The scoring method produces a numeric score in a documented range for each assessed document". The DoD is already correct in requiring documentation.

---

### R-004 — Subjective verification in DoD: US-044

**Story**: US-044 (Derived from: UR-063)
**Category**: Untestable DoD
**Severity**: Low

US-044 DoD reads:

> Chunk boundaries are reviewed against at least two Phase 1 document types (e.g. a typewritten document and a digital PDF) from the estate corpus and confirmed by the Primary Archivist to align with logical document units; no chunk boundary splits a meaningful unit arbitrarily.

The final clause — "no chunk boundary splits a meaningful unit arbitrarily" — relies entirely on the Primary Archivist's subjective judgment as the verification mechanism. There is no repeatable, objective test defined. "Confirmed by the Primary Archivist" is a valid human acceptance test but "no chunk boundary splits a meaningful unit arbitrarily" cannot be verified objectively by a third party or in an automated test.

This is low severity because human review is an acceptable DoD mechanism for AI-determined outputs, and the story correctly flags the chunking mechanism as an architectural decision.

**Suggested action**: Consider reframing as: "Chunk boundaries are reviewed against at least two document types and the Primary Archivist confirms no boundary splits a logically indivisible unit (e.g. a clause, a named transaction, or a named party's entry). The review outcome is recorded before the story is closed." This makes the deliverable explicit without claiming automated verifiability.

---

### R-005 — Architectural assumption embedded in acceptance criteria: US-056

**Story**: US-056 (Derived from: UR-082, UR-083)
**Category**: Architectural assumption in story
**Severity**: Medium

US-056 acceptance criterion reads:

> Supplementary context text is combined with any extracted text and used as the input to the embedding step; it does not re-run text extraction; the document progresses from the embedding step onward

The clause "it does not re-run text extraction" asserts a specific pipeline behaviour: that text extraction is a discrete step that can be skipped. This is an architectural assumption about pipeline design, not a requirement stated in UR-082 or UR-083. UR-082 says only that supplementary context "should be embedded and searchable and should allow the document to progress through the pipeline."

How the pipeline handles supplementary context (whether it skips text extraction, whether it branches, whether it uses a separate embedding path) is an architectural decision that depends on UR-070 and UR-074, both of which are unresolved architectural flags.

**Suggested action**: Remove the implementation-specific clause "it does not re-run text extraction; the document progresses from the embedding step onward" and replace with requirement-level language: e.g. "Supplementary context text is combined with available extracted text (if any) and the document becomes embeddable and searchable." The specific pipeline mechanics are an architectural decision.

---

### R-006 — Misleading "I want to understand that" framing

**Stories**: US-013, US-069, US-081, US-085
**Category**: Misleading framing
**Severity**: Low

Four stories use the framing "I want to understand that..." which is informational rather than action-oriented. User stories should describe something a user wants to do or a behaviour the system provides.

| Story | Framing |
| --- | --- |
| US-013 | Story body abandons the standard format entirely ("The system does not implement...") |
| US-069 | "I want to understand that structured filtering... is a Phase 3 feature" |
| US-081 | "I want to understand that there is no in-application mechanism to remove..." |
| US-085 | "I want to understand that Phase 1 is designed for a single browser session..." |

"I want to understand that" encodes a scope constraint as a user learning need, which is not the standard purpose of a user story. These stories describe system constraints (things the system does not do) rather than user capabilities.

This pattern was retained from prior review cycles as an accepted simplification for constraint stories. However, it creates a risk that implementers treat these as informational notes rather than testable constraints.

**Suggested action**: Rephrase to describe the system constraint directly. For example: "I want the system to have no concurrent session support in Phase 1 so that..." or convert to a system constraint story format with a clear "so that" clause that names the design intent. US-013's complete departure from the story format is the most severe instance.

---

### R-007 — Acceptance criterion references Phase 2 behaviour in a Phase 1 story

**Story**: US-069 (Derived from: UR-102)
**Category**: Unverifiable criterion at phase close
**Severity**: Low

US-069 is labelled Phase 1. One acceptance criterion reads:

> No structured filtering options are provided in Phase 1 or Phase 2

This criterion cannot be verified at Phase 1 story close because Phase 2 has not yet been delivered. The story cannot be fully closed until Phase 2 is deployed and confirmed to have no structured filtering.

This is a low-severity issue because the constraint is reasonable and the Phase 2 conformance check is straightforward. But it means US-069 has a partially deferred acceptance criterion that can only be verified at Phase 2 delivery.

**Suggested action**: Split the criterion into two: one that is verifiable at Phase 1 close ("No structured filtering options are provided in Phase 1") and one that is a Phase 2 constraint note ("Structured filtering is not introduced in Phase 2 — this is verified at Phase 2 delivery").

---

### R-008 — Misleading acceptance criterion: US-042

**Story**: US-042 (Derived from: UR-061)
**Category**: Misleading criterion
**Severity**: Low

US-042 acceptance criteria include:

> The document remains in the search index with its existing embeddings unchanged; corrected metadata fields are reflected in the document record and citations on next display

This criterion assumes the document is already in the search index. Metadata correction via the curation UI can be applied to any document in the curation queue, including documents that have not yet completed the pipeline and have no embeddings — for example, a document flagged at the text extraction step. For such a document, it is not in the search index and has no existing embeddings to remain unchanged.

The criterion is correct for documents that have already been embedded, but misleading when read as applying to any document a curator might correct metadata on.

**Suggested action**: Qualify the criterion: e.g. "If the document is already in the search index, it remains there with its existing embeddings unchanged. Documents not yet in the search index are unaffected by metadata correction and will be indexed when pipeline processing completes."

---

### R-009 — UR-056 missing from Architectural Flags Summary table

**Story**: US-039 (Derived from: UR-056)
**Category**: Missing architectural flag
**Severity**: Low

UR-056 is marked `[ARCHITECTURAL FLAG — for Head of Development]` in `user-requirements.md`. US-039 does not carry the architectural flag inline in its acceptance criteria, and UR-056 / US-039 is absent from the Architectural Flags Summary table at the end of the document.

The Architectural Flags Summary table currently has 14 entries. UR-056 should be entry 15.

**Suggested action**: Add the following row to the Architectural Flags Summary table:

| US-039 | UR-056 | Metadata fields assessed for completeness and the scoring method depend on what the extraction pipeline can reliably produce |

Additionally, consider adding a note in US-039's acceptance criteria consistent with the architectural flag pattern used in other stories.

---

### R-010 — Ambiguous scope of curation queue in US-078

**Story**: US-078 (Derived from: UR-111)
**Category**: Internal inconsistency / ambiguity
**Severity**: Low

US-078 acceptance criteria say:

> The curation queue displays all flagged documents

UR-111 and overview.md both describe the queue as containing "documents awaiting review or flagged with issues". The phrase "awaiting review" could imply a state distinct from "flagged" — for example, a document that has completed processing and is waiting for the curator to review it without having raised a flag. However, reading the full requirements, all documents that enter the curation queue do so via the flag mechanism (UR-073, UR-075). There is no state described in the requirements where a document is "awaiting review" but not flagged.

The discrepancy between "awaiting review or flagged" (overview and UR-111 language) and "all flagged documents" (US-078) is likely harmless but could cause confusion if an implementer interprets "awaiting review" as a distinct queue state.

**Suggested action**: Align the acceptance criterion with the upstream language: "The curation queue displays all documents in the flagged or awaiting-review state" — and confirm whether these are the same state or distinct. If they are the same state, document that in US-078 to prevent a future implementer introducing a separate non-flagged queue state.

---

### R-011 — Phase Future label on a Could requirement without phase assignment

**Story**: US-021 (Derived from: UR-033)
**Category**: Phase assignment consistency
**Severity**: Low

US-021 is labelled "Phase Future" and the document header states "Phase Future = no phase assigned yet; no implementation expected until a specific phase is assigned." UR-033 is priority `Could` with no assigned phase.

This is consistent. However, the acceptance criteria include:

> Content-based duplicate detection (beyond hash matching) is implemented in a future phase
> The appropriate phase is determined when tooling and extraction capability are confirmed
> Content-based duplicate detection is implemented using a defined similarity method appropriate to the document types in scope at that phase

The third criterion ("implemented using a defined similarity method...") is a forward-looking implementation requirement that can only be evaluated when the phase is assigned and the story is decomposed. As written, this criterion could create an expectation that the similarity method must be resolved now as part of this story.

**Suggested action**: Align with the scope placeholder pattern used in US-082: make clear that all acceptance criteria for US-021 will be decomposed into specific testable criteria when the phase is assigned, and remove the third criterion (similarity method) as premature specification.

---

### R-012 — DoD contains unresolvable dependency note in duplicate location

**Story**: US-068 (Derived from: UR-101)
**Category**: Incomplete coverage note in DoD
**Severity**: Low

US-068 DoD reads:

> The CLI query command is functional and unchanged after Phase 2 deploys web UI query.

This DoD requires Phase 2 to have been deployed before it can be fully verified — similar to the issue in R-007 (US-069). The Phase 1 story cannot be fully closed until Phase 2 delivery confirms the CLI is still present and unchanged.

This is lower severity than R-007 because the DoD describes a Phase 2 regression check, which is a normal practice, rather than an acceptance criterion that conflates two phases.

**Suggested action**: Note in the DoD that this story requires a regression check at Phase 2 delivery: "The CLI query command is functional and unchanged after Phase 2 deploys web UI query. A regression check is performed at Phase 2 delivery to confirm the CLI is still functional."

---

## Coverage Summary

| Total requirements | Requirements covered | Requirements missing |
| --- | --- | --- |
| 137 | 137 | 0 |

All 137 requirements (UR-001 to UR-137) are covered by at least one story.

---

## Findings by Category

| Category | Findings |
| --- | --- |
| User type mismatch | R-001, R-002 |
| Untestable / process-oriented criteria | R-003, R-004 |
| Architectural assumption in story | R-005 |
| Misleading framing | R-006, R-007, R-008 |
| Missing architectural flag | R-009 |
| Ambiguity / inconsistency | R-010, R-011, R-012 |
