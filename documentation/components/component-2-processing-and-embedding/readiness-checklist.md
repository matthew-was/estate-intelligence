# Component 2: Design Readiness & Handoff Checklist

**Status**: Ready for Phase 1 implementation

---

## What Is Locked Down

### ✅ Scope & Purpose

- Clear inputs (uploaded documents with basic metadata from Component 1)
- Clear outputs (embedded vectors + enriched metadata + chunks in PostgreSQL)
- Two internal stages: extraction/processing + embedding/storage

### ✅ Document Handling Strategy

- **PDF detection**: Identify born-digital vs scanned PDFs
- **Text extraction**: PDF extraction for born-digital, Docling/Tesseract OCR for scanned
- **Image files**: Direct OCR processing
- **Maps/plans**: Single visual chunk + metadata chunks for searchable text
- **Email chains**: Individual message semantic chunking (Phase 3)

### ✅ Quality Assurance

- Quality scoring (0–100) based on OCR confidence, text coherence, structure integrity
- All documents process regardless of quality (Phase 1)
- Quality scores enable future filtering/review (Phase 3+)

### ✅ Metadata & Categorisation

- User provides: creation date (approximate acceptable), broad category
- Stage A refines: validates category, suggests alternatives, extracts key dates
- Pattern-based detection for Phase 1 (rules for different document types)
- LLM-based validation for Phase 2+

### ✅ Domain Context Management

- Human-maintained domain context document (developer updates it)
- Stage A tracks candidate terms/entities found during processing
- Frequency counting to identify recurring unknowns
- Phase 2 adds automated flagging when candidates reach threshold
- Reprocessing workflow to apply updated context

### ✅ Chunking Strategy

- **Text documents** (letters, deeds, invoices): Semantic chunking on paragraph/section boundaries
- **Maps/plans**: Single chunk for visual preservation, separate metadata chunks
- **Emails** (Phase 3): Semantic chunking within individual messages, thread metadata
- All chunks maintain parent document references

### ✅ Internal Stage Handoff (Stage A → Stage B)

- Well-defined data structure for passing from extraction to embedding
- Includes: extracted text, metadata, chunks, quality scores, parent references, domain context feedback
- Enables Stage B to implement required functionality

### ✅ Build Phase Strategy

- **Phase 1**: Core extraction, basic chunking, quality scoring, candidate tracking
- **Phase 2**: Enhanced metadata extraction, domain context flagging/reprocessing, semantic chunking refinement
- **Phase 3+**: Email parsing, advanced deduplication, relationship detection

---

## What Still Needs Exploration (Doesn't Block Phase 1)

### ⚠️ Semantic Chunking Implementation

**Status**: Architecture decided, specific algorithm not yet chosen

**Decision**: Use simple heuristics for Phase 1 (paragraph breaks, sentence boundaries), upgrade to ML-based approach in Phase 2

**What Phase 1 implementation needs**:
- Define exact rules: what constitutes a paragraph boundary, how to respect sentence breaks
- Maximum chunk size guidance (500–1000 tokens estimated; refine through real-world testing)
- Fallback strategy if heuristics produce poor results

**Who decides**: Development team during Phase 1 implementation

---

### ⚠️ Category Detection Rules

**Status**: Approach decided (pattern-based), specific patterns not enumerated

**Decision**: Phase 1 uses rule-based heuristics (emails have from/to headers, invoices have currency symbols, deeds have legal phrases)

**What Phase 1 implementation needs**:
- Document-specific pattern list for each category
- Confidence thresholds for suggestions vs certainty
- Fallback behaviour when patterns don't match clearly

**Who decides**: Development team, informed by first real-world documents processed

---

### ⚠️ Domain Context Flagging Threshold

**Status**: Concept locked (flagging when candidate appears N times), specific threshold not set

**Decision**: Phase 2 will determine threshold (3, 5, 10 occurrences?) through observation

**What Phase 1 implementation needs**:
- Configurable parameter for threshold (default: 5?)
- Counter mechanism for tracking occurrences
- Ability to adjust without code changes

**Who decides**: Developer during Phase 1, based on what feels right for feedback volume

---

## Gaps & Assumptions to Validate

### 🔍 Assumption: OCR Quality Is "Good Enough"

**Assumption**: Docling OCR on typewritten documents produces text suitable for embedding (~95% accuracy)

**Validation Method**:
- Process sample documents from estate collection
- Compare extracted text to manual reading
- If quality is poor, iterate on: preprocessing (deskew, contrast), OCR alternatives, quality gatekeeping

**Risk Level**: Medium (mitigated by quality scoring + willingness to iterate)

---

### 🔍 Assumption: Semantic Chunking Heuristics Work

**Assumption**: Simple paragraph/section break detection preserves semantic coherence adequately

**Validation Method**:
- Process real documents, inspect chunk boundaries
- Check if chunks make sense standalone
- If chunks are too small or fragmented, refine heuristics

**Risk Level**: Low (easy to adjust, observable immediately)

---

### 🔍 Assumption: Parent Document Model Is Sufficient

**Assumption**: Parent-child references enable adequate context retrieval in RAG

**Validation Method**:
- Component 3 implementation will confirm retrieval strategy
- Query time performance will show if parent retrieval is a bottleneck

**Risk Level**: Low (architecture is sound, may need optimisation)

---

### 🔍 Missing Detail: Document Type Category List

**What we know**: Broad categories (letter, deed, map, plan, invoice, operational log, email, survey, etc.)

**What's open**: Is this list exhaustive? Will real documents fit cleanly? Should categories be hierarchical?

**Decision point**: Review actual documents early in Phase 1, refine if needed

---

## Handoff Checklist

- [x] Purpose and scope clear
- [x] Inputs and outputs defined
- [x] Major design decisions documented with rationale
- [x] Build phase strategy aligned (Phase 1 simplifications clear)
- [x] Data contracts defined
- [x] Configuration points identified
- [x] Error handling approach outlined
- [x] Testing strategy hints provided
- [x] Internal stage interface expectations clear
- [x] Implementation technology stack recommended
- [x] Known gaps and assumptions listed
- [x] Phase 1 priorities sequenced

---

## Next Steps

### Before Implementation Starts

1. Review specification with development team
2. Identify any additional technology constraints or preferences
3. Validate assumptions — especially OCR quality on real estate documents
4. Confirm semantic chunking heuristics approach works with sample documents

### During Phase 1 Implementation

1. Establish domain context tracking (basic JSON file collection)
2. Validate quality scoring against manual assessment
3. Test with 20–30 real documents across different categories
4. Document any adjustments to heuristics based on real-world results
5. Prepare for Phase 2 transition (flagging logic, LLM integration)

### After Phase 1 Complete

1. Hand off to Component 3 design with confidence in output contract
2. Gather metrics on extraction quality, chunking coherence
3. Plan Phase 2 enhancements based on learnings
4. Document any domain-specific patterns discovered
