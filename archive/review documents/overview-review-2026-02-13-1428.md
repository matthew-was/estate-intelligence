# Overview Review

Reviewed against `documentation/project/overview.md` (post five prior review cycles; scope change
applied 2026-02-13).

## Contradictions

1. **Flag-clearing and processing advancement** — Two statements about flag-clearing appear to
   conflict. Line 70 states "clearing a flag advances processing to the next incomplete step." A
   later sentence in the same paragraph states "clearing a flag does not automatically trigger
   processing." These can be reconciled if the first statement describes *where* processing will
   resume (from the next incomplete step, not from the beginning) and the second describes *when*
   (only when manually triggered). However, this reading is not explicit in the text, and the two
   sentences read as contradictory without clarification. A requirement writer would need to know:
   does clearing a flag change the document's processing state, independently of whether the trigger
   fires?

## Missing information

1. **Document title at intake** — Citations in query results include "document title" (line 83), and
   curators can correct "title" as a metadata field (line 84). However, title does not appear in
   either intake route. The Phase 1 web form captures date and description (line 60). Bulk
   ingestion parses a filename stem into date and description (line 60). Title is neither captured
   at intake nor described as derived or auto-detected. It is not stated whether title is the same
   as description, a separately entered field, or something the extraction pipeline produces. This
   gap makes it impossible to write requirements for citation format or the intake form without
   assuming an answer.

2. **Manual flag — queue ordering** — The document curation queue is ordered by "the timestamp of
   the last successfully completed pipeline step that raised the flag" (line 84). A curator can
   manually flag a document (line 84: "flag documents with a typed status and a free-text reason").
   A manually raised flag is not associated with a pipeline step. It is not stated what timestamp
   value governs queue position for a manually flagged document, or whether manually flagged
   documents occupy a distinct position or section in the queue.

3. **User-initiated flag — typed status values** — Curators can "flag documents with a typed status
   and a free-text reason" (line 84). The valid status values are not listed and are not described
   as open-ended text. If status is a constrained list, the list is missing. If it is free-text,
   the word "typed" is misleading. This is needed to write requirements for the flag action.

## Undocumented edge cases

1. **Missing/unreadable stored file — no in-app resolution path in Phase 1** — When a stored file
   is missing or unreadable, the document is flagged and surfaced in the curation queue (line 70).
   However, document replacement is out of scope for Phase 1 and Phase 2 (lines 86 and 88). There
   is no in-app action the curator can take to resolve this flag. The document will remain flagged
   and unresolvable until Phase 3. The overview does not address what the curator is expected to do
   when they encounter this flag, or whether the flag should carry a message distinguishing it from
   flags that have an in-app resolution path.

2. **User-initiated flag vs system-generated flag — same mechanism or separate?** — The overview
   describes a system-generated flag mechanism throughout the pipeline section. It also describes a
   curator-initiated "flag documents" action in the curation list (line 84). It is not stated
   whether these use the same flag field and queue entry, or whether they are distinct. If the
   same: does clearing a system flag also clear a curator note, and vice versa? If separate: does
   the curation queue show both, and are they interleaved or separated?

## Ambiguities

1. **"Typed status" in manual flagging** — See Missing information item 3 above. The word "typed"
   could mean: (a) the user types free text as a status label, (b) the status is selected from a
   predefined type list, or (c) "typed" is used informally to mean "categorised". Each
   interpretation produces different requirements for the flag action UI and data model.

2. **Metadata completeness threshold and partial detection** — Line 72 states "partial detection
   (some fields found, others not) is not itself a flag trigger." Line 69 states "a document must
   satisfy both [text quality and metadata completeness thresholds] to proceed without a flag."
   These are consistent if the completeness score is a numeric value across all fields and partial
   detection may still achieve a passing score. However, the relationship between "partial
   detection" and the completeness score is not explicit. A requirement writer could reasonably
   interpret this as: any partial detection always passes the completeness threshold (making the
   threshold only relevant for zero-metadata cases), or as: partial detection may or may not pass
   depending on the score. The intended semantics need to be stated.
