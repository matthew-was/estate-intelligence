# Component 2: Quick Reference

## What Component 2 Does (One Sentence)

Takes uploaded documents and produces extracted text, enriched metadata, semantically chunked content, and vector embeddings stored in PostgreSQL — ready for retrieval and RAG queries.

## Input

- PDF or image files from S3/local storage (stored by Component 1)
- User-provided: creation date, broad category
- File metadata from Component 1 database record

## Output

- Extracted text with quality score (0–100)
- Enriched metadata (refined category, dates, entities)
- Chunks with parent document references
- Domain context candidates for developer review
- Vector embeddings stored in PostgreSQL + pgvector

---

## Document Type Handling at a Glance

| Type | Extraction | Chunking | Special Handling |
| --- | --- | --- | --- |
| Born-digital PDF | PDF text extraction | Semantic (paragraphs) | Straightforward |
| Scanned PDF / Image | Docling OCR (Tesseract fallback) | Semantic (paragraphs) | Quality score critical |
| Map / Plan | Docling OCR | Single chunk + metadata chunks | Preserves visual integrity |
| Email | Parse headers + body | Semantic within message | Per-message chunks (Phase 3) |
| Letter / Deed | OCR or PDF extraction | Semantic (sections) | Look for signatures, legal phrases |
| Invoice | OCR or PDF extraction | Semantic (items/sections) | Extract amounts, vendor info |

---

## Quality Score Interpretation

| Score | Meaning | Action (Phase 1) |
| --- | --- | --- |
| 80–100 | High confidence extraction | Proceed normally |
| 60–79 | Good confidence | Proceed; tag medium confidence |
| 40–59 | Uncertain | Proceed; flag for potential review |
| 0–39 | Poor quality | Proceed; expect issues; flag for review |

**Phase 1**: All scores proceed to embedding. Quality gates come in Phase 3+.

---

## Processing Pipeline (Linear Sequence)

```text
1. Detect file type (PDF type detection, image format)
   ↓
2. Extract text (PDF extraction or OCR via Docling/Tesseract)
   ↓
3. Assess quality (score 0-100)
   ↓
4. Extract metadata (dates, entities, category validation)
   ↓
5. Create chunks (document-type-specific strategy)
   ↓
6. Assign parent references (link chunks to source document)
   ↓
7. Track domain context (count candidates, prepare feedback)
   ↓
8. Generate embeddings (configurable provider)
   ↓
9. Store in PostgreSQL + pgvector (vectors + metadata + parent refs)
```

---

## Configuration (Phase 1)

| Setting | Options | Default | Impact |
| --- | --- | --- | --- |
| OCR engine | Docling, Tesseract | Docling (Tesseract fallback) | Text quality for scanned docs |
| Chunk size target | 500–1500 tokens | 1000 | Embedding coherence |
| Quality threshold | 0–100 | None (all pass) | Which documents proceed |
| Domain context storage | JSON file / DB table | JSON file | Simplicity vs richness |
| Chunking heuristics | Rules per doc type | Define these during implementation | Chunk boundary accuracy |
| Embedding provider | OpenAI, Anthropic, local | Configurable | Vector quality and cost |

---

## Decisions the Dev Team Needs to Make

### Before Starting (Blocking)

1. **Category detection rules**: What distinguishes a "deed" from a "letter"? List 3–5 patterns per category
2. **Semantic chunking heuristics**: Split on blank lines? Paragraph markers? Topic shifts? Choose for Phase 1
3. **Domain context storage**: JSON file or PostgreSQL table? Start simple (JSON)

### Before Phase 1 Testing (Non-blocking)

1. **Fallback strategies**: If OCR fails, what happens? Try PDF extract? Use metadata only? Fail the document?
2. **Reprocessing logic**: When domain context is updated, how does reprocessing happen? On-demand? Batch?
3. **Logging detail**: Errors only? All processing steps? Performance metrics?

### During Phase 1 (Learning)

1. Fine-tune chunking heuristics based on real document results
2. Adjust quality score weights based on actual extraction quality
3. Gather domain context candidates to inform Phase 2 flagging logic

---

## Phase 1 Success Criteria

- [ ] PDF type detection works (born-digital vs scanned)
- [ ] Docling/Tesseract OCR extracts readable text from scanned documents
- [ ] Quality scores vary and roughly match manual assessment
- [ ] Categories are correct or sensibly suggested (>70% accuracy acceptable for Phase 1)
- [ ] Chunks are coherent (paragraphs stay together, section breaks respected)
- [ ] Parent document references are valid and retrievable
- [ ] Domain context candidates collected and reviewable
- [ ] Embeddings generated and stored in pgvector
- [ ] Output contract satisfied (Component 3 can query and retrieve)

---

## When to Escalate

**If OCR quality is unacceptable**: Stop and investigate before proceeding. Options: better preprocessing, different OCR engine, manual review gates

**If chunking produces poor boundaries**: Pause, inspect real chunks, adjust heuristics — this affects embedding quality downstream

**If quality scoring doesn't match reality**: Adjust weighting factors. Quality score is a trust indicator — it must be reliable

**If document types don't fit categories**: Add categories as needed. Domain expertise beats assumptions

**If domain context candidates are noisy**: Document the noise. Phase 2 will add filtering/confirmation logic

---

## Interfaces to Other Components

| Direction | Component | What Is Exchanged |
| --- | --- | --- |
| Input ← | Component 1 (Intake) | Documents in storage, file metadata in DB, deduplication already applied |
| Output → | Component 3 (Query) | Embeddings in pgvector, chunks with parent refs, quality scores, metadata, treatment tags |
| Feedback → | Developer | Domain context candidates for review and approval |

---

## Technology Stack

**Primary Language**: Python (Stage A — extraction/processing)

**Key Libraries**:

- `pdfplumber` — PDF text extraction
- `docling` — Structure-preserving OCR (primary)
- `pytesseract` — Tesseract OCR (fallback)
- `spacy` — NLP, entity recognition, sentence splitting
- `nltk` — Text utilities, tokenisation
- `sentence-transformers` — Semantic similarity (Phase 2+)
- `psycopg2` / `asyncpg` — PostgreSQL connection
- `pydantic` — Configuration and data validation

**External Services**: Docling, PostgreSQL + pgvector, S3/local filesystem, embedding provider API

---

## Phase 1 vs Phase 2 Comparison

| Feature | Phase 1 | Phase 2 |
| --- | --- | --- |
| Category detection | Pattern rules | LLM-validated |
| Semantic chunking | Heuristics | ML similarity-based |
| Entity extraction | Regex + basic NLP | LLM-assisted |
| Domain context flagging | Manual review | Automated threshold |
| Email parsing | Basic structure | Individual message extraction |
| Reprocessing | Manual/on-demand | Automated batch |

---

## Failure Modes & Mitigations

| Failure | Detection | Mitigation |
| --- | --- | --- |
| OCR produces gibberish | Quality score ~0, incoherent text | Log + flag + proceed (learning data) |
| Wrong category detected | Developer reviews suggestion, disagrees | Update domain context, reprocess |
| Chunks break mid-sentence | Inspect real chunk boundaries | Adjust heuristics, test with more docs |
| Quality score unreliable | Manual spot checks don't match score | Adjust scoring weights |
| Domain context feedback too noisy | Too many candidates suggested | Raise flagging threshold in Phase 2 |
| Parent references broken | Component 3 can't retrieve context | Validate references in tests |
