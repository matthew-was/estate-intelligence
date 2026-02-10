# Component 2 Design Conversation Summary

## How We Got Here

This specification was developed through iterative design conversation with the following progression:

### Initial Framing
Started by understanding that Components 2 & 3 are actually tightly coupled and should be designed together, not separately. This reframing clarified scope: Component 2 handles extraction and processing, Component 3 handles embedding and storage.

### Key Conversation Threads

#### 1. Understanding Embedding & Chunking (Your Research)
You identified a gap in your knowledge about embeddings and chunking, went away to research, and came back with understanding. This led to the **parent document retrieval pattern** as the solution to preserve map coherence while keeping chunks embedable.

**Outcome**: Document-type-specific chunking strategies with parent references became core design.

#### 2. Domain Context as Learning Tool
Discussed whether system should autonomously classify and extract entities vs. human-guided learning.

**Key Decision**: Human maintains authoritative domain context, system flags candidates. This prevents the system from "running away" with assumptions and ensures you control terminology understanding.

**Outcome**: Feedback loop designed with frequency tracking and threshold-based flagging for Phase 2.

#### 3. Duplicate Handling
Clarified that duplicates are removed at upload time (Component 1), so Component 2 doesn't need to worry about them.

**Outcome**: Simplified Component 2 scope; embedding similarity checking deferred to Phase 3+.

#### 4. Metadata at Upload vs. Processing
Discussed what user should provide at upload time vs. what Component 2 should extract.

**Final Approach**: User provides minimal (date + broad category). Component 2 validates category and extracts everything else.

**Outcome**: Low user friction at upload, intelligence deferred to processing.

#### 5. Quality Scoring
Discussed whether poor extractions should block processing or proceed with flags.

**Decision**: Phase 1 processes all documents regardless of quality. Quality scores provide visibility. Manual review queue comes in Phase 3+.

**Rationale**: Learning phase prioritizes data volume and visibility over purity.

**Outcome**: Quality scores stored for future gatekeeping.

#### 6. OCR as "Good Enough"
Questioned whether to over-engineer OCR quality gates upfront.

**Decision**: Assume Tesseract works well enough on typewritten documents (95%+ accuracy). Iterate if it doesn't.

**Rationale**: Real-world iteration beats speculative architecture. Your estate documents are mostly typewritten (better for OCR), not handwritten.

**Outcome**: Simple OCR pipeline, quality validation happens through real-world testing.

#### 7. Maps & Plans Treatment
Debated how to handle primarily visual documents.

**Journey**: → Single chunk (your intuition) → Question about embedding implications → Your research on embeddings → Recognition that parent document retrieval solves the problem → Final design: single visual chunk + metadata chunks.

**Outcome**: Maps/plans get special handling while remaining discoverable.

#### 8. Email Chunking Strategy
Discussed whether email chains should be single chunks or split by message.

**Decision**: Semantic chunking of individual messages (avoids huge variability), thread context preserved via parent reference.

**Rationale**: Prevents chunk size variability, preserves context for RAG.

**Outcome**: Email-specific chunking strategy for Phase 3.

---

## Design Principles That Emerged

### 1. **Incremental Intelligence**
Start simple (heuristic rules), add sophistication (ML/LLM) in later phases. This applies to:

- Category detection (Phase 1: patterns, Phase 2: LLM)
- Semantic chunking (Phase 1: heuristics, Phase 2: ML similarity)
- Entity extraction (Phase 1: regex/NLP, Phase 2: LLM)

### 2. **Human-in-the-Loop Learning**
System proposes, human decides. This prevents:

- Confident mistakes from cascading
- System making assumptions about terminology
- Loss of control over entity/relationship definitions

### 3. **Iterate on Reality, Not Speculation**
Don't over-engineer for cases you haven't seen:

- OCR quality assumed good—validate on real documents
- Chunking heuristics assumed adequate—inspect real chunk boundaries
- Category rules derived from real document patterns

### 4. **Observability First**
When uncertain about quality, measure it:

- Quality scores visible for every document
- Processing metadata recorded for audit
- Reprocessing capability built in for refinement

### 5. **Graceful Degradation**
One component failing shouldn't block the whole pipeline:

- If OCR fails, try PDF extraction + metadata-only processing
- If metadata extraction fails, record error but continue with basic data
- Failures logged with enough context for debugging

---

## Critical Design Decisions & Their Rationale

| Decision | Rationale | Risk | Mitigation |
|----------|-----------|------|-----------|
| OCR is "good enough" without hard gates | Real-world iteration beats speculation; typewritten docs better for OCR | Quality too poor for embedding | Quality scoring provides visibility; reprocess if needed |
| All documents process regardless of quality | Learning phase needs data volume; prevent false negatives | Garbage in, garbage out | Quality scores enable future filtering; Phase 3+ adds gates |
| User maintains domain context, system flags candidates | Prevents system from making assumptions; you control terminology | Slow feedback loop | Frequency tracking enables batched review; Phase 2 automates flagging |
| Semantic chunking via heuristics in Phase 1 | Simple to implement, observable, refinable | Heuristics might miss topic boundaries | Quality inspection during Phase 1 reveals issues; Phase 2 upgrades to ML |
| Parent document references for all chunks | Enables RAG context retrieval; solves map coherence problem | Added complexity in storage/retrieval | Straightforward to implement; essential for quality RAG |
| Maps as single chunk + metadata chunks | Preserves visual integrity while remaining searchable | User finds map when searching for metadata but not content | Acceptable—metadata is usually what matters for discovery |

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

### If Parent Document Model Doesn't Work at Component 3

- This is unlikely (pattern is proven in production systems)
- If performance is issue, optimize retrieval (caching, indexing)
- If context is insufficient, supplement with chunk metadata

### If Domain Context Learning is Too Slow

- Lower flagging threshold (flag after 2 occurrences instead of 5)
- Add manual interface to suggest domain context entries
- Move to Phase 2 LLM-assisted extraction sooner

---

## Assumptions for Implementation Team

### About Your Documents

- Mostly typewritten (not handwritten) → OCR will work reasonably well
- Date ranges known or approximable → user can provide creation date
- Categories are broad and consistent → user can provide initial category
- Naming conventions exist but need learning → domain context tracking will help

### About Your Use Cases

- Land ownership, infrastructure, decisions are key queries → metadata/entity detection matters
- Historical context matters → parent document and threading context important
- You have time to review and refine → human-in-the-loop approach works
- Learning is goal as much as functionality → willing to iterate and understand

### About the Architecture

- PostgreSQL with pgvector available → storage solution settled
- AWS/local filesystem abstraction will work → configuration approach sound
- Python/TypeScript split is acceptable → OCR/processing in Python, orchestration flexible
- Docker containerization enables pipeline → deployment strategy proven

**If any of these change significantly, revisit design.**

---

## For the Development Team

### What You Can Start Building Immediately

1. **Input handling**: Accept documents from S3/filesystem, read file metadata
2. **Text extraction**: PDF type detection (try pdfplumber, pytesseract)
3. **Quality scoring**: Implement scoring based on OCR confidence + text coherence
4. **Basic metadata**: Extract dates, validate categories
5. **Output serialization**: Produce the output contract JSON structure

### What Requires Decisions First

1. **Semantic chunking heuristics**: Define exact rules for your document types
2. **Category patterns**: Enumerate characteristics of each category (emails have from/to, etc.)
3. **Domain context storage format**: JSON file? Database table? Start with JSON for simplicity
4. **Configuration approach**: Environment variables? Config file? Use Pydantic BaseSettings

### What Can Wait for Phase 2

- LLM-based classification
- ML-based semantic chunking
- Domain context flagging and reprocessing workflow
- Enhanced entity extraction

---

## Communication Template for Next Phases

### Transitioning to Implementation
**Share with dev team**:

1. Component 2 specification (main artifact)
2. This conversation summary (context and rationale)
3. Readiness checklist (what's locked vs. what's open)
4. Technology recommendations (specific libraries)

**Decisions they should make**:

1. Exact chunking heuristics for Phase 1
2. Category detection patterns
3. Domain context storage approach
4. Error handling specifics

### Transitioning to Component 3
**Share with Component 3 designers**:

1. Output contract (what Component 2 produces)
2. Design questions for Component 3 (parent retrieval strategy, quality handling)
3. Phase 1 limitations (simple classification, basic entities)
4. Phase 2+ enhancements (LLM-assisted extraction, entity relationships)

---

## Unresolved Questions (For Future Conversations)

1. **Semantic chunking specifics**: What exact heuristics work best for your documents? (Resolve in Phase 1 implementation)
2. **Domain context threshold**: How many times should a term appear before flagging? (Decide during Phase 1, refine in Phase 2)
3. **Category patterns**: What patterns reliably distinguish your document types? (Emerge from first batch processing)
4. **Performance requirements**: What's acceptable latency for processing a document? (Establish during Phase 1, optimize in Phase 4)
5. **Batch vs. streaming**: Should Component 2 process documents in batches or as they arrive? (Architectural choice for Phase 2+)

---

## Success Looks Like

**Phase 1 Complete**:

- You can upload 20 documents (mix of letters, deeds, maps, invoices)
- All text is extracted and readable
- Quality scores reflect real extraction quality
- Categories are mostly correct or sensibly suggested
- Chunks are coherent and stay together
- Parent references work and enable context retrieval

**Phase 2 Complete**:

- Domain context flagging works (shows you candidates, you update context)
- Reprocessing refines earlier documents
- LLM-assisted classification improves accuracy
- Semantic chunking better at topic boundaries

**Phase 3+ Complete**:

- Email parsing works
- Entity relationships detected
- You can query "who owns the north field across time" and get connected documents
- System learns your terminology and documents interconnections
