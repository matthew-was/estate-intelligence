# Component 2: Design Rationale

## How We Got Here

This specification was developed through iterative design conversation. The key framing that shaped everything: **Components 2 and 3 (in the original 5-component design) are tightly coupled and should be designed together**. This led to the current 4-component architecture where text extraction, processing, and embedding are a single Component 2 with two internal stages.

---

## Key Design Conversation Threads

### 1. Understanding Embedding & Chunking

The developer identified a gap in knowledge about embeddings and chunking, researched it, and returned with understanding. This led to the **parent document retrieval pattern** as the solution to preserve document coherence while keeping chunks embeddable.

**Outcome**: Document-type-specific chunking strategies with parent references became core design.

---

### 2. Domain Context as Learning Tool

Question: Should the system autonomously classify and extract entities, or should it be human-guided?

**Decision**: Human maintains authoritative domain context, system flags candidates. This prevents the system from running away with assumptions and ensures the developer controls terminology understanding.

**Outcome**: Feedback loop designed with frequency tracking and threshold-based flagging for Phase 2.

---

### 3. Duplicate Handling

Clarified that duplicates are removed at upload time (Component 1), so Component 2 doesn't need to worry about exact duplicates.

**Outcome**: Simplified Component 2 scope; embedding similarity checking deferred to Phase 3+.

---

### 4. Metadata at Upload vs. Processing

Question: What should the user provide at upload time vs. what should Component 2 extract?

**Final approach**: User provides minimal (date + broad category). Component 2 validates category and extracts everything else.

**Outcome**: Low user friction at upload; intelligence deferred to processing.

---

### 5. Quality Scoring

Question: Should poor extractions block processing or proceed with flags?

**Decision**: Phase 1 processes all documents regardless of quality. Quality scores provide visibility. Manual review queue comes in Phase 3+.

**Rationale**: Learning phase prioritises data volume and visibility over purity.

**Outcome**: Quality scores stored for future gatekeeping.

---

### 6. OCR as "Good Enough"

Question: Should we over-engineer OCR quality gates upfront?

**Decision**: Assume Docling produces acceptable results on typewritten documents. Iterate on real documents rather than speculate.

**Rationale**: Real-world iteration beats speculative architecture. Estate documents are mostly typewritten (better for OCR), not handwritten.

**Outcome**: Simple OCR pipeline; quality validated through real-world testing.

---

### 7. Maps & Plans Treatment

Question: How to handle primarily visual documents in a text-based embedding system?

**Journey**: Single chunk (intuition) → Question about embedding implications → Research on embeddings → Recognition that parent document retrieval solves the problem → Final design: single visual chunk + metadata chunks.

**Outcome**: Maps and plans get special handling while remaining discoverable via text search.

---

### 8. Email Chunking Strategy

Question: Should email chains be treated as single chunks or split by message?

**Decision**: Semantic chunking of individual messages (avoids huge variability). Thread context preserved via parent reference.

**Rationale**: Prevents chunk size variability; preserves context for RAG.

**Outcome**: Email-specific chunking strategy for Phase 3.

---

## Design Principles That Emerged

### 1. Incremental Intelligence

Start simple (heuristic rules), add sophistication (ML/LLM) in later phases:

- Category detection: Phase 1 patterns → Phase 2 LLM
- Semantic chunking: Phase 1 heuristics → Phase 2 ML similarity
- Entity extraction: Phase 1 regex/NLP → Phase 2 LLM

### 2. Human-in-the-Loop Learning

System proposes, human decides. Prevents:

- Confident mistakes from cascading
- System making assumptions about terminology
- Loss of control over entity/relationship definitions

### 3. Iterate on Reality, Not Speculation

Don't over-engineer for cases not yet seen:

- OCR quality assumed good — validate on real documents
- Chunking heuristics assumed adequate — inspect real chunk boundaries
- Category rules derived from real document patterns

### 4. Observability First

When uncertain about quality, measure it:

- Quality scores visible for every document
- Processing metadata recorded for audit
- Reprocessing capability built in for refinement

### 5. Graceful Degradation

One component failing shouldn't block the whole pipeline:

- If OCR fails, try PDF extraction + metadata-only processing
- If metadata extraction fails, record error but continue with basic data
- Failures logged with enough context for debugging

---

## Critical Design Decisions & Their Rationale

| Decision | Rationale | Risk | Mitigation |
| --- | --- | --- | --- |
| OCR is "good enough" without hard gates | Real-world iteration beats speculation; typewritten docs better for OCR | Quality too poor for embedding | Quality scoring provides visibility; reprocess if needed |
| All documents process regardless of quality | Learning phase needs data volume; prevent false negatives | Garbage in, garbage out | Quality scores enable future filtering; Phase 3+ adds gates |
| Human maintains domain context, system flags candidates | Prevents system from making assumptions; developer controls terminology | Slow feedback loop | Frequency tracking enables batched review; Phase 2 automates flagging |
| Semantic chunking via heuristics in Phase 1 | Simple to implement, observable, refinable | Heuristics might miss topic boundaries | Quality inspection during Phase 1 reveals issues; Phase 2 upgrades to ML |
| Parent document references for all chunks | Enables RAG context retrieval; solves map coherence problem | Added complexity in storage/retrieval | Straightforward to implement; essential for quality RAG |
| Maps as single chunk + metadata chunks | Preserves visual integrity while remaining searchable | User finds map when searching for metadata but not content | Acceptable — metadata is usually what matters for discovery |

---

## What Would Change This Design

### If OCR Quality Proves Poor

- Implement quality gates before embedding
- Add manual review queue for low-confidence extractions
- Investigate OCR preprocessing (deskew, contrast enhancement)
- Evaluate alternative OCR engines

### If Semantic Chunking Heuristics Fail

- Inspect chunk boundaries on real documents early
- Move to ML-based similarity scoring (Phase 2 sooner)
- Adjust heuristic rules based on document type patterns

### If Parent Document Model Doesn't Work

- This is unlikely (pattern is proven in production systems)
- If performance is issue, optimise retrieval (caching, indexing)
- If context is insufficient, supplement with chunk metadata

### If Domain Context Learning Is Too Slow

- Lower flagging threshold (flag after 2 occurrences instead of 5)
- Add manual interface to suggest domain context entries
- Move to Phase 2 LLM-assisted extraction sooner

---

## Assumptions for Implementation Team

### About the Documents

- Mostly typewritten (not handwritten) → OCR will work reasonably well
- Date ranges known or approximable → user can provide creation date
- Categories are broad and consistent → user can provide initial category
- Naming conventions exist but need learning → domain context tracking will help

### About the Use Cases

- Land ownership, infrastructure, decisions are key queries → metadata/entity detection matters
- Historical context matters → parent document and threading context important
- Developer has time to review and refine → human-in-the-loop approach works
- Learning is goal as much as functionality → willing to iterate and understand

### About the Architecture

- PostgreSQL with pgvector available → storage solution settled
- AWS/local filesystem abstraction will work → configuration approach sound
- Python/TypeScript split is acceptable → OCR/processing in Python, orchestration flexible
- Docker containerisation enables pipeline → deployment strategy proven

**If any of these change significantly, revisit the design.**

---

## Success Looks Like

**Phase 1 Complete**:

- Upload 20 documents (mix of letters, deeds, maps, invoices)
- All text extracted and readable
- Quality scores reflect real extraction quality
- Categories mostly correct or sensibly suggested
- Chunks coherent and standalone-readable
- Parent references work and enable context retrieval

**Phase 2 Complete**:

- Domain context flagging works (shows candidates, developer updates context)
- Reprocessing refines earlier documents
- LLM-assisted classification improves accuracy
- Semantic chunking better at topic boundaries

**Phase 3+ Complete**:

- Email parsing works
- Entity relationships detected
- Queryable: "who owns the north field across time" returns connected documents
- System learns estate terminology and document interconnections
