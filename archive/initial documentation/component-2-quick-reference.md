# Component 2: Quick Reference Guide

## What Component 2 Does (In One Sentence)
Takes uploaded documents and produces extracted text, enriched metadata, and semantically chunked content ready for embedding.

## Input

- PDF or image files from S3/local storage
- User-provided: creation date, broad category

## Output

- Extracted text with quality score
- Enriched metadata (refined category, dates, entities)
- Chunks with parent document references
- Domain context candidates for human review

---

## Document Type Handling at a Glance

| Type | Extraction | Chunking | Special Handling |
|------|-----------|----------|------------------|
| Born-digital PDF | PDF text extraction | Semantic (paragraphs) | Straightforward |
| Scanned PDF / Image | Tesseract OCR | Semantic (paragraphs) | Quality score critical |
| Map / Plan | Tesseract OCR | Single chunk + metadata chunks | Preserves visual integrity |
| Email | Parse headers + body | Semantic within message | Per-message chunks (Phase 3) |
| Letter / Deed | OCR or PDF extraction | Semantic (sections) | Look for signatures, legal phrases |
| Invoice | OCR or PDF extraction | Semantic (items/sections) | Extract amounts, vendor info |

---

## Quality Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 80-100 | High confidence extraction | Proceed normally, prioritize in search |
| 60-79 | Good confidence | Proceed, tag as medium confidence |
| 40-59 | Uncertain | Proceed, flag for potential review |
| 0-39 | Poor quality | Proceed, but expect issues; flag for review |

**Phase 1 Decision**: All scores proceed to embedding. Quality gate comes in Phase 3+.

---

## Processing Pipeline (Linear Sequence)

```
1. Detect file type (PDF type detection, image format)
   ↓
2. Extract text (PDF extraction or OCR)
   ↓
3. Assess quality (score 0-100)
   ↓
4. Extract metadata (dates, entities, category validation)
   ↓
5. Create chunks (document-type-specific strategy)
   ↓
6. Assign parent references (link chunks to source)
   ↓
7. Track domain context (count candidates, prepare feedback)
   ↓
8. Output contract (serialize and pass to Component 3)
```

---

## Configuration You Need to Make (Phase 1)

| Setting | Options | Default | Impact |
|---------|---------|---------|--------|
| OCR engine | Tesseract | Tesseract | Text quality for scanned docs |
| Chunk size target | 500-1500 tokens | 1000 | Embedding coherence |
| Quality threshold | 0-100 | None (all pass) | Which documents process |
| Domain context storage | JSON file / DB | JSON file | Simplicity vs. richness |
| Chunking heuristics | Rules per doc type | Define these | Chunk boundary accuracy |

---

## Decisions the Dev Team Needs to Make

### Before Starting (Blocking)

1. **Category detection rules**: What makes a document a "deed" vs "letter"? List 3-5 distinguishing patterns per category.
2. **Semantic chunking heuristics**: "Split on blank lines" vs "split on paragraph markers" vs "split on topic shift"? Choose for Phase 1.
3. **Domain context storage**: File-based JSON or PostgreSQL table? Start simple (JSON).

### Before Phase 1 Testing (Non-blocking)

1. **Fallback strategies**: If OCR fails, what happens? (Try PDF extract? Use metadata only? Fail document?)
2. **Reprocessing logic**: When user updates domain context, how does reprocessing happen? (On-demand? Batch?)
3. **Logging detail**: What goes in logs? (Errors only? All processing? Performance metrics?)

### During Phase 1 (Learning)

1. **Fine-tune chunking heuristics** based on real document results
2. **Adjust quality score weights** based on actual extraction quality
3. **Gather domain context candidates** to inform Phase 2 flagging logic

---

## Phase 1 Success Criteria (How to Know It's Working)

- [ ] PDF type detection works (born-digital vs scanned)
- [ ] Tesseract OCR successfully extracts readable text from scanned documents
- [ ] Quality scores vary (not all 100, not all 0) and roughly match manual assessment
- [ ] Categories are correct or sensibly suggested (>70% accuracy acceptable for Phase 1)
- [ ] Chunks are coherent (paragraphs stay together, section breaks respected)
- [ ] Parent document references are valid and retrievable
- [ ] Domain context candidates collected (can review what system found)
- [ ] Output contract matches spec (Component 3 can deserialize and use)

---

## When to Escalate / Ask Questions

### If OCR Quality is Unacceptable
→ Stop and investigate before proceeding. Options: better preprocessing, different OCR engine, human review gates

### If Chunking Produces Poor Boundaries  
→ Pause, inspect real chunks, adjust heuristics. This affects embedding quality downstream.

### If Quality Scoring Doesn't Match Reality
→ Adjust weighting factors in Phase 1. Quality score is trust indicator—must be reliable.

### If Document Types Don't Fit Categories
→ Add categories as needed. Your domain expertise beats our assumptions.

### If Domain Context Candidates Are Noisy
→ Document what the noise is. Phase 2 will add filtering/confirmation logic.

---

## Interfaces to Other Components

### Depends On (Component 1)

- Documents already in S3/local storage
- File metadata in database (format, upload timestamp)
- Deduplication already done (no exact duplicates)

### Required By (Component 3)

- Chunks with parent references
- Quality scores per chunk/document
- Metadata (category, dates, entities)
- Treatment tags (reference-only, metadata-only, etc.)

### Feedback To (Component 1 - Future)

- Quality scores → enables quality review queue
- Processing metadata → enables audit trail

---

## Common Workflows

### Processing a New Batch of Documents

1. Upload documents (Component 1)
2. Component 2 processes automatically or on-demand
3. Review quality scores and domain context feedback
4. Update domain context if needed
5. Proceed to Component 3 for embedding

### Updating Domain Context (Phase 2+)

1. Review Component 2's flagged candidates
2. Approve/reject additions to domain context
3. Component 2 reprocesses flagged documents
4. Review refined metadata, proceed if improved

### Debugging a Low-Quality Document

1. Check quality score and extraction method
2. Check OCR confidence values (if applicable)
3. Check extracted metadata (dates, entities detected correctly?)
4. For Phase 3+: add to manual review queue
5. For Phase 1: document the issue, move on (this is learning data)

---

## Technology Stack Summary

**Primary Language**: Python

**Key Libraries**:

- `pdfplumber` or `PyPDF2` - PDF text extraction
- `docling` - OCR and document structure preservation (primary choice over Tesseract)
- `spacy` - NLP, entity recognition, sentence splitting
- `nltk` - Text utilities, tokenization
- `sentence-transformers` - Semantic similarity (Phase 2+)
- `psycopg2` or `asyncpg` - PostgreSQL connection

**External Services**:

- Docling (structure-preserving OCR, can run locally or via API)
- PostgreSQL (for tracking, Phase 2+)
- S3 or local filesystem (document storage)

**Environment Config**: Python dotenv, Pydantic BaseSettings

---

## Phase 1 vs Phase 2 Comparison

| Feature | Phase 1 | Phase 2 |
|---------|---------|---------|
| Category detection | Pattern rules | LLM-validated |
| Semantic chunking | Heuristics | ML similarity-based |
| Entity extraction | Regex + basic NLP | LLM-assisted |
| Domain context flagging | Manual review | Automated threshold |
| Email parsing | Basic structure | Individual message extraction |
| Reprocessing | Manual/on-demand | Automated batch |

---

## Failure Modes & Mitigations

| Failure | Detection | Mitigation |
|---------|-----------|-----------|
| OCR produces gibberish | Quality score ~0, incoherent text | Log + flag + proceed (learn what went wrong) |
| Wrong category detected | User reviews suggestion, disagrees | Update domain context, reprocess |
| Chunks break mid-sentence | Inspect real chunk boundaries | Adjust heuristics, test with more docs |
| Quality score unreliable | Manual spot checks don't match score | Adjust scoring weights |
| Domain context feedback too noisy | Too many candidates suggested | Raise flagging threshold in Phase 2 |
| Parent references broken | Component 3 can't retrieve context | Validate references in tests |

---

## Handoff Checklist

**Before handing off to dev team:**

- [ ] Show them this spec
- [ ] Show them conversation summary (WHY we made each decision)
- [ ] Show them readiness checklist (what's locked, what's open)
- [ ] Have them make decisions on: chunking heuristics, category rules, storage approach
- [ ] Have them propose fallback strategies for errors
- [ ] Have them estimate Phase 1 timeline

**Before handing off to Component 3 design:**

- [ ] Phase 1 implementation complete
- [ ] Output contract validated (sample Component 2 outputs reviewed)
- [ ] Quality scores validated (real docs assessed manually, compared)
- [ ] Domain context candidates collected (reveal terminology patterns)
- [ ] Phase 1 learnings documented (what worked, what needs adjustment)
- [ ] Open questions for Component 3 answered (parent retrieval strategy, quality handling, metadata weighting)
