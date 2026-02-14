# User Stories Review

Reviewed against: `.claude/docs/requirements/user-requirements.md` (approved 2026-02-13)
and `documentation/project/overview.md` (approved 2026-02-13).

Each finding is listed with: story ID, issue type, description, and suggested fix or flag for
Developer decision where scope judgement is needed.

---

## 1. Missing or Incomplete Coverage

### Finding R-001 — UR-095 partially miscovered by US-065

**Story**: US-065
**Issue**: UR-095 states that editing and deleting vocabulary terms is out of scope for Phase 1 and
deferred to Phase 2. US-065 reflects this correctly in the phase assignment. However, the
acceptance criteria say "Phase 2 introduces the ability to edit accepted **or manually-added**
vocabulary terms" — mirroring the requirement's exact wording. The definition of done says "An
accepted term can be edited and its changes take effect immediately; a deleted term is removed from
the vocabulary." This is correct but the story does not include an acceptance criterion confirming
that manually-added terms (as distinct from candidate-accepted terms) are also editable and
deletable. A developer reading only the criteria might implement edit/delete for candidate-accepted
terms only.

**Suggested fix**: Add a criterion: "Both terms accepted from the candidate queue and terms added
manually via the UI are editable and deletable."

---

### Finding R-002 — UR-033 phase assignment on US-021 is ambiguous

**Story**: US-021
**Issue**: US-021 is assigned Phase 2+ but the third acceptance criterion reads: "Duplicate
detection behaviour for inline email attachments (such as signature images) is resolved at Phase 2
scope definition." This is a scope decision point, not an acceptance criterion for the story itself.
A developer could read this as something the implementation must deliver rather than a deferred
design decision. UR-033 is a `Could` priority deferred item — the story correctly assigns Phase 2+
but the embedded note conflates a future scope decision with a testable criterion.

**Suggested fix**: Move the inline email attachment note to the story description or a dedicated
notes field. Replace the criterion with one that is actually testable for Phase 2+ delivery (e.g.
"Content-based duplicate detection is implemented using a defined similarity method appropriate to
the document types in scope at that phase").

---

### Finding R-003 — UR-042 Phase 2 extension not covered

**Story**: US-028
**Requirement**: UR-042 explicitly states "Phase 2 adds handwritten documents, maps, plans,
surveys, and emails."
**Issue**: US-028 covers Phase 1 text extraction only. There is no story covering Phase 2 text
extraction expansion (handwritten documents, maps, plans, surveys, emails). The file format
expansion is covered by US-007 (DOCX and EML), but the document type expansion for extraction
(handwritten, maps, plans) has no story at all.
**Suggested fix**: Add a Phase 2+ story derived from UR-042 for text extraction expansion to Phase
2 document types. Flag for Developer decision: should this be a single story or multiple stories
per document type?

---

### Finding R-004 — UR-061 re-embedding in Phase 2 has no story

**Requirement**: UR-061 states that re-embedding on metadata correction is introduced in Phase 2.
**Issue**: US-042 correctly covers Phase 1 behaviour (metadata update only, no re-embedding). The
overview confirms Phase 2 adds "Re-embedding on metadata correction." However, no Phase 2+ story
exists covering the Phase 2 behaviour — that correcting metadata triggers re-embedding
automatically. This is a `Must` Phase 1 requirement with an explicit Phase 2 successor that is
entirely absent.
**Suggested fix**: Add a Phase 2+ story: "As a Primary Archivist or Family Member, I want
correcting document metadata to automatically trigger re-embedding so that search results reflect
the corrected metadata."

---

### Finding R-005 — UR-082/083 supplementary context story (US-056) missing a criterion for pipeline progression

**Story**: US-056
**Issue**: The story has "Attaching supplementary context allows the document to progress through
the pipeline" as a criterion, but there is no criterion specifying which pipeline steps the
document progresses through, or confirming that the document becomes searchable after attachment.
The definition of done says "become searchable" but the criteria do not include "the document
appears in search results after supplementary context is attached and processing completes."
**Suggested fix**: Add a criterion: "After supplementary context is attached and processing
completes, the document appears in search results."

---

### Finding R-006 — UR-107 user type mismatch on US-074

**Story**: US-074
**Requirement**: UR-107 lists user types as "Primary Archivist, Family Member, Occasional
Contributor" with priority `Should`.
**Issue**: US-074 is assigned Phase 2+ and lists the correct user types in the "As a..." line.
However, it is labelled Phase 2+ and the requirement says Phase 3. This is a phase assignment
error. UR-107 is under the Phase 3 section of the requirements ("Phase 3 should introduce filter
and facet search"). The story title even says "(Phase 3)" but the Phase field says "Phase 2+".

**Suggested fix**: The Phase field should clearly indicate this is Phase 3 (or at minimum note
"Phase 3" rather than the generic "Phase 2+"). The stories document uses "Phase 2+" as a catch-all
for both Phase 2 and Phase 3. This creates ambiguity when a developer is scoping Phase 2 delivery
versus Phase 3 delivery. Flag for Developer decision: should stories that are specifically Phase 3
(not Phase 2) be labelled distinctly?

---

### Finding R-007 — UR-108 Occasional Contributor query (US-075) phase label inconsistency

**Story**: US-075
**Issue**: Same problem as R-006. UR-108 is a Phase 3 requirement (priority `Must`, Occasional
Contributor). US-075 is labelled "Phase 2+" but the requirement belongs to Phase 3. The story
title says "(Phase 3)" but the Phase field says "Phase 2+". A developer scoping Phase 2 work could
mistakenly include this.
**Suggested fix**: Same as R-006 — clarify Phase 3 vs Phase 2+ labelling. This applies to all
Phase 3 requirements mapped to stories labelled "Phase 2+": US-074, US-075, US-090, US-091,
US-092, US-093. Flag for Developer decision: use distinct "Phase 3" label or add a note in each
story.

---

### Finding R-008 — US-090 combines UR-126 and UR-130 inconsistently

**Story**: US-090
**Derived from**: UR-126 (Phase 3, System Administrator, user account management) and UR-130
(Phase 3, System Administrator, System Administrator role separated from Primary Archivist).
**Issue**: The "As a System Administrator" framing is questionable: the story is about introducing
the System Administrator role itself. A System Administrator does not yet exist when this story is
being implemented — the story is about creating that role. The framing should reflect that the
Primary Archivist (or the system) is the actor introducing this capability, not the System
Administrator acting on it.
**Suggested fix**: Reframe as: "As a Primary Archivist, I want a System Administrator role
introduced in Phase 3 so that infrastructure and user account management are separated from
archival responsibilities." The acceptance criteria are otherwise correct.

---

### Finding R-009 — US-092 System Administrator framing has the same problem as US-090

**Story**: US-092
**Derived from**: UR-129 (System Administrator, Phase 3, document visibility scoping).
**Issue**: Visibility scoping is a system capability introduced in Phase 3, not something a System
Administrator actively "wants." The framing "As a System Administrator, I want document visibility
scoped by user type" implies the System Administrator is the user performing an action, but the
criterion is "Phase 3 introduces visibility scoping rules" — a system design constraint. The
definition of done and criteria describe the feature introduction, not the System Administrator
acting on it.
**Suggested fix**: The user type in the "As a..." line could reasonably remain as System
Administrator if the intended reading is "As the person responsible for access control, I want
this capability." This is a minor framing issue but could mislead a developer as to what the
System Administrator does at runtime versus what is a system design constraint. Flag for Developer
decision.

---

## 2. Incorrect Phase Assignments

### Finding R-010 — US-070 page-level citation phase assignment is contradictory

**Story**: US-070
**Derived from**: UR-103 (Could, Phase — unspecified in UR, deferred "to a later phase").
**Issue**: The story title says "(future phase)" and the acceptance criteria say "Page-level
citation is deferred to a later phase (Phase 3 or beyond)" and "Full-document citation is used in
Phase 1, Phase 2, and **Phase 3**." But UR-103 says it is deferred to a later phase with the
note "Full-document citation is sufficient for Phase 1, Phase 2, and Phase 3." These two sources
agree — page-level citation is Phase 4 or beyond. The acceptance criterion in the story saying
"Phase 3 or beyond" is therefore correct. However, the definition of done says "Page-level
citation is specified, implemented, and tested in the phase it is assigned to" — which is a valid
but untestable criterion given no phase is assigned. This definition of done is not verifiable in
Phase 2+ as written.
**Suggested fix**: The definition of done should reflect the deferred nature: "This story is a
scope placeholder only. No implementation is expected until a specific phase is assigned."
Alternatively, this could be removed from the stories document entirely and left as a note on
US-067 (the active citation story).

---

### Finding R-011 — US-021 is Phase 2+ but UR-033 priority is Could with no phase commitment

**Story**: US-021
**Issue**: US-021 is assigned Phase 2+ which implies a commitment to deliver in Phase 2. UR-033
priority is `Could` and the rationale says "the appropriate phase depends on tooling and extraction
capability." The story formalises a Phase 2+ commitment that the requirement explicitly leaves
open. A developer reading US-021 could treat Phase 2 as the delivery target for content-based
duplicate detection, which contradicts the requirement's intent.
**Suggested fix**: Change the Phase label to a note such as "Phase TBD (deferred — phase to be
confirmed at Phase 2 scope definition)." Flag for Developer decision: should this story be
retained as a placeholder or removed until the phase is confirmed?

---

## 3. User Type Mismatches

### Finding R-012 — US-056 user type includes Family Member without qualification

**Story**: US-056
**Requirement**: UR-082 lists user types as "Primary Archivist, Family Member" and priority
`Should`.
**Issue**: Family Member is introduced in Phase 2. US-056 correctly assigns Phase 2+ and lists
"Primary Archivist or Family Member." However, the acceptance criterion says "Phase 2 allows a
curator to attach supplementary context." Calling the actor "a curator" rather than specifying the
user type is acceptable — but the definition of done says "A Phase 1 document with no extractable
text can receive supplementary context **in Phase 2**." This is correct. The story is internally
consistent. This finding is informational: no change required.

---

### Finding R-013 — US-048 user type is correct but the "want" is misleading

**Story**: US-048
**Issue**: The "want" in the story is "to trigger document processing manually in Phase 1 so that
I control when processing runs." The acceptance criteria correctly note that the trigger surface
is an architectural flag. However, the definition of done says "The Primary Archivist can trigger
processing manually **via the mechanism defined at the architecture phase**." This means the
story's definition of done cannot be verified until the architecture phase resolves the mechanism.
A developer implementing this story does not know what "done" looks like until the architectural
flag is resolved.
**Suggested fix**: Note explicitly in the definition of done that this story cannot be closed until
UR-070 is resolved by the Head of Development. Or restructure: split the "processing must be
manual" constraint (which is testable) from the "mechanism for triggering" (which is
architectural). The current story conflates the two in a way that leaves the definition of done
unverifiable.

---

## 4. Untestable, Vague, or Incomplete Acceptance Criteria

### Finding R-014 — US-013 has no testable acceptance criteria

**Story**: US-013
**Issue**: This story documents a known limitation (concurrent bulk ingestion is undefined). The
acceptance criteria are:

- "The system does not define or guarantee any behaviour when two ingestion runs are started
  simultaneously in Phase 1"
- "This limitation is documented"

The first criterion is not testable — it describes an absence of behaviour, not a verifiable
outcome. The second criterion ("This limitation is documented") is testable but only if a
documentation location is specified. Neither criterion can be checked by a developer completing
the story.
**Suggested fix**: The first criterion could be made testable: "No locking mechanism, error, or
concurrent-session detection is implemented for simultaneous ingestion runs." The second should
specify where documentation lives (e.g. "documented in the CLI help output or README"). Flag for
Developer decision: should this be a story at all, or a note in US-009?

---

### Finding R-015 — US-039 is not a story — it is an architectural deferral notice

**Story**: US-039
**Issue**: This story's "want" is: "I want to understand that the specific metadata fields assessed
and the completeness scoring method are determined at the architecture phase." This describes a
scope constraint that the user wants to understand, not a system capability the user wants the
system to provide. Neither acceptance criterion is testable by a developer — both state that
something is defined during the architecture phase. The definition of done says "The Head of
Development has defined the metadata fields and scoring method" — this is an architectural
deliverable, not a story deliverable.

A story exists to specify what the system does. US-039 specifies what the system does not yet
define. It belongs in the architectural flags, not in the stories.
**Suggested fix**: Remove US-039 as a story. The UR-056 architectural flag is already captured in
the Architectural Flags Summary table. If retained, it should be labelled a "scope note" or
"constraint note" rather than a user story. Flag for Developer decision.

---

### Finding R-016 — US-051 definition of done is unverifiable

**Story**: US-051
**Issue**: The definition of done is: "The Head of Development has defined the pipeline state
tracking mechanism; the implementation supports re-entry at any step." The first clause — "The
Head of Development has defined..." — is not something a developer implementing the story can
verify or control. It describes a precondition, not a done state.
**Suggested fix**: The definition of done should focus on what the implementation must demonstrate:
"A document that has completed extraction but not embedding can be re-processed starting from the
embedding step, without re-running extraction; pipeline state is persisted across processing runs."
The architectural resolution is a precondition, not the done criterion.

---

### Finding R-017 — US-055 ordering direction not specified

**Story**: US-055
**Issue**: The acceptance criterion says "Documents are ordered by the timestamp of the last
successfully completed pipeline step that raised the flag (**ascending or descending as defined by
the architecture**)." The ordering direction is left open in the story. A developer implementing
the queue could reasonably choose either direction. UR-080 does not specify direction either —
but the story should not leave this open at story level if the direction matters to the
curator's workflow.
**Suggested fix**: Flag for Developer decision: should the ordering direction be specified here or
left to the architecture phase? If it matters to the curator (oldest-flagged first to work through
the backlog, or most-recently-flagged first), this is a product decision that should be made
before implementation.

---

### Finding R-018 — US-085 definition of done uses passive voice that is unverifiable

**Story**: US-085
**Issue**: The definition of done is: "The Phase 1 application is delivered without concurrent
session handling; **this limitation is documented**." As with US-013, "this limitation is
documented" is only verifiable if a documentation location is specified.
**Suggested fix**: Specify where the limitation is documented (e.g. in the application README, the
CLI help, or a known limitations section of the web app).

---

### Finding R-019 — US-044 definition of done has an unverifiable clause

**Story**: US-044
**Issue**: The definition of done says "each document's chunks align with semantically meaningful
units (clauses, paragraphs, named transactions); no chunk boundary splits a meaningful unit
arbitrarily." The phrase "semantically meaningful" and "no chunk boundary splits a meaningful unit
arbitrarily" cannot be objectively tested — they rely on human judgement about what is meaningful.
**Suggested fix**: Add a verifiable proxy criterion, for example: "Chunk boundaries are reviewed
against at least two sample documents of different types from the estate corpus and confirmed by
the Primary Archivist to align with logical document units." This acknowledges that "semantically
meaningful" requires human review, not automated test.

---

### Finding R-020 — US-036 description field overwrite not fully covered in acceptance criteria

**Story**: US-036
**Derived from**: UR-051, UR-052.
**Issue**: The acceptance criteria include "The system-generated description overwrites the
description provided at intake." However, they do not specify what happens if the system fails to
detect a description — does the intake description remain, or is it replaced with an empty/null
value? UR-052 says "The system-generated description must overwrite the description provided at
intake" with no exception for detection failure. The story should either match this (overwrite
unconditionally, even with null) or surface the ambiguity.
**Suggested fix**: Add a criterion: "If the system does not detect a description, the intake
description is overwritten with a null/empty value (per UR-052); the curator may then correct it."
Or flag for Developer decision if the intended behaviour is that the intake description is
preserved on detection failure.

---

### Finding R-021 — US-078 does not specify what "sufficient information to identify the document" means

**Story**: US-078
**Issue**: The criterion "Each entry shows sufficient information to identify the document and
understand the flag reason" is vague. A developer does not know which fields constitute
"sufficient information." The curation queue in the overview mentions date, description, and
archive reference but the story does not specify these.
**Suggested fix**: Replace with specific fields: "Each entry shows at minimum the document
description, date, flag reason, and submitter identity." This makes the criterion testable.

---

## 5. Acceptance Criteria Embedding Architectural Assumptions

### Finding R-022 — US-005 hardcodes accepted formats in acceptance criteria

**Story**: US-005
**Issue**: The acceptance criteria state "The file picker is restricted to PDF, TIFF, JPEG, and
PNG." This is correct for Phase 1 per UR-009 and overview.md. This is not an architectural
assumption — the formats are explicitly defined in scope. This finding is informational: no change
required.

---

### Finding R-023 — US-019 criterion says "read from a configuration file" — correct but confirm scope

**Story**: US-019
**Issue**: The criterion "The limit is read from a configuration file external to the codebase at
runtime" is consistent with UR-133 and is not an architectural assumption. This is a stated scope
requirement. Informational: no change required.

---

### Finding R-024 — US-043 embeds a specific list of external services in acceptance criteria

**Story**: US-043
**Issue**: The acceptance criterion says "The embedding provider is abstracted via an interface and
selected at runtime via configuration." This is consistent with UR-062 and UR-132. The criterion
correctly carries the architectural flag. No issue.

---

### Finding R-025 — US-059 acceptance criterion uses "at minimum" language inconsistent with UR-087

**Story**: US-059
**Issue**: UR-087 says "Each vocabulary term must be a structured record with **at minimum**: term,
category, description, aliases, and relationships." US-059's criterion says "Each vocabulary term
record contains: term, category, description, aliases (a list, may be empty), and relationships"
— without the "at minimum" qualifier. A developer could implement exactly these five fields and
consider the story done, even if the architecture phase determines additional fields are needed.
**Suggested fix**: Add "at minimum" to the criterion to match the requirement's intent and leave
room for additional fields determined at architecture phase.

---

## 6. Internal Inconsistencies Between Stories

### Finding R-026 — US-032 and US-033 overlap with US-045 without cross-reference

**Stories**: US-032, US-033, US-045
**Issue**: US-032 states "The document is absent from the search index." US-033 states "The
document is absent from the search index until the flag is cleared and processing completes."
US-045 also states "A document does not appear in search results until the embedding step has
completed successfully." These three stories express the same constraint from different angles
without cross-referencing each other. A developer could implement these stories independently and
produce conflicting outcomes (e.g. US-032 says absent from search, but US-045 could be read as
only about pipeline-resumption documents). The stories are consistent in substance but a developer
without full context might treat them as independent features.
**Suggested fix**: Add cross-references in the derived-from lines or in the story descriptions:
"See also US-032, US-033 for related zero-text and partial-extraction cases" (in US-045) and
"See also US-045 for the general rule on search exclusion" (in US-032 and US-033).

---

### Finding R-027 — US-053 and US-079 duplicate flag-clearing behaviour without explicit cross-reference

**Stories**: US-053, US-079
**Issue**: US-053 defines the flag-clearing behaviour (state semantics). US-079 defines the
flag-clearing UI action. Both describe clearing a flag. US-079 references US-053 in its criteria
("Clearing the flag marks the document ready to resume from the next incomplete step (per
US-053)") which is good. However, US-053 does not reference US-079. This means a developer could
implement the flag-clearing state logic from US-053 without implementing the UI mechanism covered
by US-079 — and vice versa.
**Suggested fix**: Add to US-053: "The UI mechanism for clearing a flag is covered by US-079."

---

### Finding R-028 — US-046 and US-047 use "processing run" without defining what triggers a run

**Stories**: US-046, US-047
**Issue**: Both stories reference "the next processing run" as the trigger for resumption and
retry. US-048 is the story covering the manual processing trigger. However, US-046 and US-047 do
not cross-reference US-048. A developer implementing retry logic needs to know that "next
processing run" means "next manually triggered processing run" in Phase 1. Without the
cross-reference, the developer might implement an automatic retry loop.
**Suggested fix**: Add to the relevant criteria in US-046 and US-047: "Processing runs are
triggered manually in Phase 1 (see US-048); there is no automatic retry between runs."

---

## 7. Stories That Would Be Ambiguous or Misleading for a Developer

### Finding R-029 — US-009 does not specify what "stored in the archive" means for bulk ingestion

**Story**: US-009
**Issue**: The criterion "The command stores accepted files in the archive" and the definition of
done "stores accepted files in the archive" give no indication of the storage mechanism or what
"stored" means (file copy, reference, database record). This is an architectural concern per
UR-017 and UR-132, but the story does not flag it. A developer could implement "stored" as a
database record only without copying the actual file, or vice versa.
**Suggested fix**: Add an architectural flag: "The storage mechanism (file copy, reference, or
other) is an architectural decision `[ARCHITECTURAL FLAG — for Head of Development]`." This
parallels the flag already present in US-012 for atomicity.

---

### Finding R-030 — US-022 does not specify how virtual document groups are expressed at the web UI

**Story**: US-022
**Derived from**: UR-035.
**Issue**: The criterion "The submission mechanism (web UI or CLI) allows multiple files to be
associated as a single virtual document" leaves the mechanism entirely open. For the CLI this is
reasonable (architectural), but for the web UI in Phase 1, the mechanism needs to be understood
by the implementer. The story does not distinguish between how grouping works at the web UI versus
the CLI. A developer implementing the Phase 1 web UI cannot determine from this story what the
grouping UI looks like.
**Suggested fix**: Either specify that the grouping mechanism for both surfaces is an architectural
decision (and add the flag), or note that Phase 1 group submission is CLI-only and the web UI
grouping mechanism is Phase 2+. Flag for Developer decision: is virtual document grouping
available via the web UI in Phase 1?

---

### Finding R-031 — US-063 and US-064 do not confirm the rejected-terms list persists across restarts

**Stories**: US-063, US-064
**Issue**: US-063 mentions "the persisted rejected-terms list" in the criteria. US-064 says a
rejected candidate is "added to the persisted rejected list." The word "persisted" is used in
both, which is correct per UR-092. However, neither story specifies that the rejected-terms list
survives system restarts (which is implied by "persisted" but not stated). A developer could
implement the rejected-terms list as an in-memory set that resets on restart.
**Suggested fix**: Add to US-064: "The rejected-terms list persists across system restarts; it is
not an in-memory structure that resets on restart."

---

### Finding R-032 — US-011 summary report criterion does not require named sub-directories

**Story**: US-011
**Issue**: The acceptance criterion says "A summary report is produced with zero counts and an
actionable error message identifying the sub-directories found." UR-016 says the report has "zero
counts" which the story captures. However, UR-016 says "identifying **which** sub-directories were
found" and the criterion says only "identifying the sub-directories found." This is minor wording
but could lead a developer to implement a count ("2 sub-directories found") rather than a named
list ("sub-directories found: /path/subdir1, /path/subdir2"). The overview explicitly says "a
clear actionable error message identifying which sub-directories were found" implying named
identification.
**Suggested fix**: Strengthen the criterion: "The error message names each sub-directory found
(not just a count)."

---

### Finding R-033 — US-081 does not cross-reference its Phase 3 counterpart

**Story**: US-081
**Issue**: UR-114 explicitly covers Phase 1 and Phase 2. US-081's definition of done says "Phase 1
and Phase 2 web UI contains no document removal capability" — correct. However, the acceptance
criterion says only "No remove, replace, or delete document option is available in the web UI in
Phase 1 or Phase 2." It does not mention Phase 3 at all, which is where UR-131 (US-093) covers
the introduction of these features. A developer might wonder whether the Phase 1 story should
forward-reference Phase 3 or stand alone. No issue but cross-referencing US-093 as the Phase 3
counterpart would help.
**Suggested fix**: Add a note: "Phase 3 introduces replace and delete as managed features (see
US-093)."

---

### Finding R-034 — US-089 does not specify how the Phase 1 submitter identity value is set

**Story**: US-089
**Issue**: The criterion "In Phase 1, this field is always set to the Primary Archivist" leaves
open whether this is a hardcoded value, a configuration value, or a default. UR-124 says the
field "must exist in the data model to support multi-user phases without schema changes." The
mechanism for assigning "Primary Archivist" in Phase 1 (where there is no authentication) should
be clarified.
**Suggested fix**: Add a criterion: "In Phase 1, the submitter identity value is set to a fixed
constant (e.g. 'Primary Archivist') at intake with no runtime selection; in Phase 2 this is
replaced by the authenticated user identity." Flag for Developer decision: should the Phase 1
constant value be configurable or hardcoded?

---

## 8. Summary of High-Priority Findings

The following findings are the most likely to cause implementation errors and should be resolved
before development begins.

| Finding | Story | Type | Action Needed |
| --- | --- | --- | --- |
| R-003 | US-028 | Missing coverage | Add Phase 2+ story for expanded text extraction |
| R-004 | US-042 | Missing coverage | Add Phase 2+ story for re-embedding on metadata correction |
| R-006 | US-074 | Phase assignment | Clarify Phase 3 vs Phase 2+ labelling |
| R-007 | US-075, US-090, US-091, US-092, US-093 | Phase assignment | Clarify Phase 3 vs Phase 2+ labelling |
| R-013 | US-048 | Untestable DoD | Split constraint from mechanism; note precondition on UR-070 |
| R-014 | US-013 | Untestable criteria | Make criteria testable; specify documentation location |
| R-015 | US-039 | Not a story | Developer decision: remove or relabel as scope note |
| R-016 | US-051 | Untestable DoD | Rewrite DoD to focus on implementation evidence |
| R-017 | US-055 | Vague criterion | Developer decision: specify ordering direction |
| R-020 | US-036 | Missing criterion | Specify overwrite behaviour when detection fails |
| R-021 | US-078 | Vague criterion | Specify which fields are shown in the curation queue |
| R-028 | US-046, US-047 | Misleading | Cross-reference US-048 for "next processing run" meaning |
| R-030 | US-022 | Misleading | Clarify whether web UI grouping is Phase 1 or Phase 2+ |
| R-031 | US-063, US-064 | Ambiguous | Specify rejected-terms list persists across restarts |
| R-034 | US-089 | Ambiguous | Clarify mechanism for setting Phase 1 submitter identity |
