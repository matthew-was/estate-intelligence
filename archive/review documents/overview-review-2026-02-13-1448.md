# Overview Review

## Contradictions

- **Curation interface: CLI vs web UI.** The existing `user-requirements.md` (UR-086, UR-087, UR-088, UR-089, UR-090) specifies CLI commands for viewing the curation queue, viewing the vocabulary review queue, clearing flags, correcting metadata, and manually flagging documents. The updated `overview.md` states that basic curation is via a minimal web UI in Phase 1 — not the CLI. This is a direct contradiction between the two documents. The `user-requirements.md` must be revised to reflect the updated scope.

- **Vocabulary management interface: CLI vs web UI.** UR-078 states the vocabulary must be extendable manually via CLI at any time. The updated `overview.md` states the vocabulary can be extended via the curation web UI. These are in direct conflict and `user-requirements.md` must be updated.

- **Curator-initiated manual flag.** UR-090 includes a requirement for a CLI command to flag a document manually with a typed status and free-text reason. The updated `overview.md` states: "Curator-initiated flag removed from scope — flags are system-generated only." This requirement must be removed from `user-requirements.md`.

## Missing information

- **Web UI scope for Phase 1 curation.** The overview describes a "minimal web UI" for curation and vocabulary management, but does not define what "minimal" means in terms of the specific screens or workflows it must cover. It is not clear whether the curation web UI is a separate application from the intake web UI, or whether they are the same application with different sections. This affects the scope of Phase 1 UI implementation.

- **Vocabulary review queue in the curation web UI.** The overview states candidates are surfaced in a "separate vocabulary review queue (distinct from the document curation queue)". It is not stated whether these are two separate pages or views within the same web UI, or two separate interfaces entirely.

- **Trigger for manual processing in Phase 1.** The overview confirms the processing trigger is manual in Phase 1, and that flag-clearing and processing resumption are separate manual actions. It does not describe how or where the processing trigger is invoked in Phase 1 — whether via CLI, a button in the web UI, or another mechanism. This is noted as an architectural concern but the trigger surface (CLI vs web UI) has direct scope implications.

## Undocumented edge cases

- **Web UI session behaviour.** Phase 1 has no authentication. The overview does not address how the web UI handles concurrent browser sessions (e.g. two browser windows open simultaneously), since Phase 1 is single-user. This is low risk in Phase 1 but the lack of a stated constraint could introduce scope questions during implementation.

- **Vocabulary review queue interaction in Phase 1 web UI.** The overview describes accepting or rejecting vocabulary candidates via the curation web UI but does not specify what happens if a candidate is accepted and then later found to be incorrect. No correction path for accepted vocabulary terms is described.

## Ambiguities

- **"Minimal web UI" definition.** The term "minimal" is used to describe both the intake web UI and the curation web UI. In the intake context it is clarified: "The web UI is unpolished but functional — it is not required to be a polished or fully-featured interface." No equivalent clarification is given for the curation web UI. This could be interpreted as (a) any functional UI suffices, or (b) specific design quality constraints apply that differ from the intake UI.

- **Single web application vs multiple.** The overview describes a web UI for document upload and a (separate?) minimal web UI for curation, without stating whether these are the same application. If they are separate applications, each has separate startup, configuration, and deployment scope. If they are a single application, the Phase 1 scope is correspondingly larger.
