# Component 2: Text Extraction & Document Processing

## Purpose

Transform uploaded documents (with basic user-provided metadata) into extracted text, enriched metadata, and semantically chunked content ready for embedding and vector storage.

## Inputs

From document upload/storage (Component 1):

- Document file (PDF or image) stored in configured backend (S3 or local filesystem)
- User-provided metadata:
  - Creation date (can be approximate: month/year acceptable)
  - Broad category (letter, deed, map, plan, invoice, operational log, email, etc.)
  - Filename and upload timestamp
- File type indication (PDF or image format)

## Outputs

To Embedding & Storage (Component 3):

- Extracted and cleaned text
- Enriched metadata including:
  - Refined/validated category
  - Extracted key dates
  - Detected entities and patterns
  - Quality score (0-100 based on extraction confidence)
  - Processing metadata (extraction method, model/engine used, extraction timestamp)
- Chunked content with:
  - Individual chunks (semantically meaningful pieces)
  - Parent document references (to retrieve full document context)
  - Chunk metadata (type, position in original, quality indicators)
  - Treatment guidance (e.g., "reference material", "metadata chunk")
- Domain context feedback:
  - Candidates for domain terminology/entity tracking
  - Confidence level of each suggestion
  - Frequency tracking for flagging threshold

## Core Processes

### 1. Text Extraction

**Detection Phase:**

- Determine if PDF is born-digital (searchable text) or scanned (image-based)
- For image files, proceed directly to OCR
- For born-digital PDFs, use standard PDF text extraction

**Extraction:**

- Born-digital PDFs: extract text preserving structure where possible
- Scanned documents/images: apply OCR (Tesseract, with abstraction for alternatives)
- Preserve text formatting and layout hints when available

**Output:** Raw extracted text with minimal cleanup

### 2. Quality Assessment

Generate a quality score (0-100) based on:

- OCR confidence scores (per-word or per-page aggregation for scanned documents)
- Text coherence (character distribution, word frequency, sentence structure validation)
- Structural integrity (clean page breaks, proper alignment, minimal skewing detected)
- Category-specific signals:
  - Letters: date/signature patterns present
  - Invoices: numeric patterns and currency symbols detected
  - Maps/plans: visual content detected alongside text
  
**Note:** Low-quality documents proceed through Component 2 but are flagged. Component 3 will store the quality score for later manual review in a future build phase.

### 3. Metadata Extraction & Classification

**Refine category:**

- Validate user-provided broad category
- Suggest alternative categories if content suggests different type
- Flag category changes for domain context learning

**Extract key information:**

- Dates beyond the creation date (when document mentions other dates)
- Document-specific metadata (e.g., plot names, recipient names, financial amounts)
- Structural markers (page count, sections, list items, etc.)

**Special document types:**

- Maps/plans: mark as "visual reference" in metadata
- Emails: extract sender, recipients, timestamp if not already in filename (Phase 3)

### 4. Domain Context Tracking & Feedback

**Internal tracking document:**

- Maintain a working record of entities/terms detected but not in user's domain context
- Track frequency of each candidate
- Track first occurrence and all subsequent occurrences

**Flagging mechanism:**

- When a candidate appears N times (configurable threshold, e.g., 3-5), flag it for user review
- Include confidence score and context (where it appeared)
- Present as: "Consider adding to domain context: 'The North Plot' (appears in documents dated 1975-1982, detected 5 times)"

**User feedback loop:**

- You maintain official domain context document
- You review suggestions and update context
- Component 2 reprocesses flagged documents with updated context (Phase 2 of Component 2)

**Second pass processing:**

- Once domain context is updated, reprocess documents to refine entity detection and classification
- Store both original and context-refined metadata for audit trail

### 5. Document Chunking

Apply document-type-specific strategies:

#### Text Documents (letters, deeds, operational logs, invoices)

- Semantic chunking: split on logical boundaries (paragraphs, sections, topic shifts)
- Target chunk size: 500-1000 tokens (adjustable based on learning)
- Preserve sentence boundaries (don't split mid-sentence)
- Maintain context: if chunk references "above" or "below", consider preceding/following content
- Each chunk tagged with: position in original, semantic topic, quality score

#### Maps & Plans

- Single visual chunk: keep entire document as one unit to preserve coherence
- Metadata chunk: extract any descriptive/text content separately:
  - Title, date, scale information, legend text, labels
  - This chunk is discoverable and searchable
  - Treatment tag: "metadata chunk" and "reference chunk"
- Parent document reference: full map image/visual for context retrieval

#### Email Chains (Phase 3)

- Individual message chunking: each email treated as semantic unit
- Semantic chunking within message: split long emails on topic boundaries
- Threading metadata: preserve thread ID, message sequence, quoted/forwarded indicators
- Parent document reference: full email thread for conversation context

### 6. Parent Document Management

For all document types:

- Assign unique parent document identifier (reference to original in storage)
- For each chunk, store:
  - Parent document ID
  - Position/sequence in parent (e.g., "chunk 2 of 5" for text docs, page numbers for maps)
  - Chunk boundaries (character offsets or page references)
- Metadata enables Component 3 to retrieve full parent context when needed for RAG

## Data Structures & Contracts

**Input Contract (from Component 1):**

```
{
  documentId: string,
  fileLocation: string (path in configured storage),
  fileName: string,
  uploadedAt: timestamp,
  userProvidedCreationDate: date or date-range,
  userProvidedCategory: string,
  fileType: "pdf" | "image",
  mimeType: string
}
```

**Output Contract (to Component 3):**

```
{
  documentId: string,
  parentDocumentReference: {
    documentId: string,
    fileLocation: string,
    documentType: string,
    creationDate: date or date-range
  },
  extractedText: string,
  extractionMethod: "pdf-extraction" | "ocr-tesseract" | [other],
  qualityScore: number (0-100),
  metadata: {
    refinedCategory: string,
    extractedDates: date[],
    detectedEntities: string[],
    documentStructure: object (page count, sections, etc.),
    processingMetadata: {
      extractionTimestamp: timestamp,
      extractionModel: string,
      ocrConfidence: number (if applicable)
    }
  },
  chunks: [{
    chunkId: string,
    content: string,
    parentPosition: string (position within parent),
    chunkType: "content" | "metadata" | "reference",
    treatmentTags: string[] (e.g., ["reference-only"], ["visual-primary"]),
    qualityScore: number,
    semanticTopic: string (brief summary of chunk topic)
  }],
  domainContextFeedback: {
    flaggedCandidates: [{
      term: string,
      frequency: number,
      confidence: number (0-100),
      contexts: string[],
      firstDetected: timestamp,
      requiresUserReview: boolean
    }]
  }
}
```

## Build Phases

### Phase 1 (Current)

- PDF and image file detection
- Basic OCR for scanned documents (Tesseract)
- Quality scoring based on OCR confidence and text coherence
- User-provided category validation (with suggested alternatives)
- Simple metadata extraction (dates, basic entities)
- Fixed-size or simple semantic chunking for text documents
- Single-chunk handling for maps/plans with metadata chunks
- Parent document reference tracking
- Domain context candidate tracking (collect and monitor frequency, but don't flag yet)
- **Key simplifications for Phase 1:**
  - Category suggestions use rule-based heuristics (not LLM-based)
  - Semantic chunking uses simple heuristics (paragraph breaks, section headers) not ML-based topic detection
  - Entity detection limited to basic patterns (dates, numbers, proper nouns via NLP libraries, not LLM extraction)
  - Domain context tracking: log candidates to working document, human reviews periodically (no automated flagging)

### Phase 2

- Domain context flagging and reprocessing workflow (automated threshold-based flagging)
- Semantic chunking refinement (improve topic boundary detection)
- LLM-assisted category validation and entity detection
- Relationship detection (document A references document B)
- Email parsing and threading (preparation for Phase 3)
- Quality score refinement based on real-world results
- Integration with domain context during reprocessing

### Phase 3+

- Email chain parsing and individual message extraction
- Advanced deduplication (embedding similarity) integration
- Knowledge graph building (entity relationships)
- Automatic linking of related documents
- Multi-pass processing with feedback loops

## Configuration Points

- OCR engine selection (Docling primary, Tesseract fallback, alternatives pluggable)
- Text extraction library for PDFs
- Chunking algorithm and target chunk size
- Quality score thresholds and weighting
- Domain context flagging threshold (how many occurrences before flagging)
- LLM/embedding service for context-aware extraction (Phase 2+)
- Storage backend for document references (S3, local filesystem)
- Document type categories (letter, deed, map, plan, invoice, operational log, email, survey, etc.)—configurable additions
- Quality score minimum threshold for proceeding (Phase 1: all documents proceed; Phase 3+: may implement hard gates)
- Docling processing timeout (if needed—structure preservation may be slower)

## Success Criteria

- Extracted text is 95%+ readable for typewritten/printed documents
- Quality scores correlate with manual assessment of extraction quality
- Chunking preserves semantic coherence (topics stay together)
- Maps/plans maintain visual integrity as single units
- Parent document references enable full-document retrieval
- Domain context suggestions are high-confidence (user approves >80% of suggestions)
- Processing latency acceptable for learning phase (can iterate on production speed later)

## Design Decisions & Rationale

### OCR as "Good Enough"
**Decision:** Use Docling for OCR on scanned documents and images. Assume it produces acceptable text and structure for embedding. If quality proves insufficient, we'll iterate.

**Rationale:** Docling better preserves document structure (important for deeds, formal letters, maps) than Tesseract alone. Learning-focused approach: real-world iteration on your documents beats speculative architecture. Structure preservation helps semantic chunking. Quality scoring provides visibility if this assumption breaks down.

**Tradeoff:** Docling is slower than Tesseract, but acceptable for learning phase. Can optimize or swap engines later if speed becomes critical.

**Note:** Your estate documents are mostly typewritten (good for OCR) and structure matters (good for Docling).

### Single Chunks for Maps/Plans
**Decision:** Keep maps and plans as single chunks to preserve visual coherence, with separate metadata chunks for discoverable text.

**Rationale:** Maps lose meaning if fragmented. Parent document retrieval pattern allows full visual context retrieval while keeping metadata searchable. Metadata chunks ensure maps surface in searches ("map of north field, 1975") even if OCR text extraction is poor.

### Domain Context as Human-Maintained
**Decision:** You maintain authoritative domain context document. Component 2 flags candidates, you approve additions.

**Rationale:** Prevents system from confidently making assumptions about terminology. High-confidence user approval threshold (>80%) means system learns gradually and safely.

### Semantic Chunking for Emails
**Decision:** Chunk individual email messages semantically rather than keeping entire threads as single units.

**Rationale:** Prevents variability in chunk size (some emails are one sentence, some are multi-page). Semantic chunking within messages keeps related content together. Parent document reference preserves thread context for RAG.

### Quality Scoring Without Hard Gates
**Decision:** Phase 1 processes all documents regardless of quality score. Phase 3+ may implement quality gates and manual review.

**Rationale:** Learning phase prioritizes data volume and visibility. Low-quality documents still provide value (metadata, relationships, patterns) even if text is imperfect. Quality scores flag which documents need attention without blocking pipeline.

## Handoff Notes to Component 3: Embedding & Storage

### Critical Inputs Component 3 Receives

- **Chunks with parent references**: Component 3 must store the relationship between chunks and original documents
- **Quality scores**: Use these to weight chunk importance in retrieval (higher quality = more confident match)
- **Chunk metadata** (semantic topic, position): Available for filtering/ranking but not required for Phase 1
- **Treatment tags** (e.g., "metadata chunk", "reference-only"): Component 3 should respect these in ranking (metadata chunks discoverable but lower weight than content chunks)
- **Domain context feedback list**: Available for Component 3 to use in entity extraction/disambiguation (Phase 2+)

### Design Questions for Component 3

1. **Parent document retrieval**: When a user query returns a chunk, should the system automatically retrieve the full parent document for RAG context, or just the chunk? (Recommendation: always retrieve parent for RAG—chunk alone may lack context)
2. **Quality score usage**: Should low-quality chunks be excluded from search entirely, weighted lower, or included with confidence warnings? (Current assumption: include with lower weight)
3. **Metadata chunk handling**: Should metadata chunks from maps be searchable but with explicit "this is a reference" signals in results?
4. **Duplicate detection at Component 3**: Embedding similarity for near-duplicates (Phase 3) will require additional logic—should Component 3 implement this or should it stay in Component 2?

### Processing Assumptions Component 3 Can Make

- All documents in input have been through deduplication (no exact file duplicates)
- Text extraction is complete and quality-assessed
- Metadata is enriched and reliable
- Chunking is semantically coherent
- Parent document references are valid and retrievable from storage backend
- Domain context has been applied (Phase 2+)

### Potential Integration Points for Future Enhancement

- Component 3 can provide feedback to Component 2 on quality scores (e.g., "embeddings for this chunk are incoherent, quality score might be too high")
- Component 3 can identify when chunks don't embed well (embedding variance indicators) and flag for review
- Component 3 could notify Component 2 when domain context updates would help (e.g., "multiple chunks reference unknown entity 'The Mill'")

## Future Integration: Component 1

**Quality Score Review Queue (Future Build Phase)**

- Component 3 needs ability to surface low-quality documents (below configurable threshold)
- Allow human review/correction of extracted text before embedding
- Update quality scores post-correction
- Re-embed if corrections change content significantly

## Technical Considerations for Implementation

## Implementation Notes for Claude Code / Development

### Technology Stack Guidance

- **Languages**: Python (primary for OCR and text processing), TypeScript/Node.js optional for orchestration
- **Key Libraries**:
  - **Text Extraction**: pdfplumber (born-digital PDFs), PyPDF2 (alternative)
  - **OCR**: Tesseract via pytesseract (with abstraction layer for alternatives)
  - **Metadata/Entity Extraction**: spaCy (NER for basic entities), regex for dates/patterns
  - **Semantic Chunking**: sentence-transformers for semantic similarity, nltk/spacy for sentence boundaries
  - **Database**: psycopg2 or asyncpg for PostgreSQL interactions
  - **Configuration**: python-dotenv for environment variables, Pydantic for config objects
  - **Logging**: Python logging or structlog for structured logs
  - **Testing**: pytest, pytest-fixtures for test data

### Architecture Pattern Recommendation
Component 2 should follow a **pipeline pattern** with pluggable stages:

1. **Input validation** (document exists, file accessible)
2. **Text extraction** (PDF type detection → extraction/OCR)
3. **Quality assessment** (scorer produces 0-100 score)
4. **Metadata extraction** (category, dates, entities)
5. **Chunking** (document-type-specific strategies)
6. **Parent tracking** (assign references, maintain audit trail)
7. **Domain context tracking** (frequency counting, candidate collection)
8. **Output serialization** (produce output contract JSON/objects)

Each stage should:

- Have well-defined input/output contracts
- Be independently testable
- Be able to fail gracefully with logging (don't stop entire pipeline for single stage failure)
- Support skipping (e.g., if text extraction fails, continue with metadata from filename)

### State & Persistence for Component 2

- **Domain context candidates**: Store in file (JSON) or database table:
  - Candidate term, frequency count, first detected date, all contexts where seen, current status
  - Retrieve/update on each processing run
  - Allows human review and status tracking ("approved", "rejected", "pending")

- **Processing records**: Store for audit trail:
  - Document ID, processing timestamp, extraction method used, quality score, any errors
  - Enables reprocessing and change tracking

- **Reprocessing flag**: Track which documents have been reprocessed with updated domain context
  - Enables comparison/audit of how domain context changes document output

### Dependencies & External Services

- **Tesseract OCR**: Must be installed and available (docker base image should include it)
- **Embedding service** (Phase 2+): Abstraction layer for OpenAI/Anthropic/local models (configured at runtime)
- **PostgreSQL**: For storing domain context candidates and processing records (optional for Phase 1, required by Phase 2)
- **Storage backend**: S3 or local filesystem (configured, abstraction layer used)

### Edge Cases & Error Scenarios Component 2 Must Handle

**Text Extraction Failures:**

- Corrupted PDF file: log error, attempt image extraction if embedded images present, mark quality score low
- OCR timeout: set timeout limit, fail gracefully, record partial text if available
- Unsupported encoding: detect and convert if possible, flag in quality score
- Unreadable image: document unreadable, mark quality score 0, still create document record

**Metadata Extraction Issues:**

- No detectable date in document: use user-provided creation date, flag as approximate
- Category mismatch: suggest best-guess category, mark confidence level, flag for review
- Entity extraction ambiguity: extract what's confident, leave unknowns unextracted

**Chunking Edge Cases:**

- Very short document (< 1 chunk worth): entire document is one chunk (acceptable)
- Very long document (100+ pages): multiple chunks created, may have thousands
- Document with no clear paragraphs/sections (e.g., image-based letter): fall back to size-based chunks
- Document with ambiguous boundaries (e.g., email forward chains): create chunks for each logical section

**Domain Context Challenges:**

- Unknown entity appears once: add to candidates, doesn't flag yet
- Entity appears with variations ("North Field" vs "north field" vs "north pasture"): frequency tracking handles this (similar strings counted)
- Homonym problem ("The Mill" could be building or watermill): quality issue, domain context needs human judgment

**Configuration & Setup Issues:**

- Tesseract not installed: clear error message, document what to install
- No write access to domain context tracking file: graceful failure with logging
- PostgreSQL connection unavailable: log error, can operate read-only if needed (Phase 1)
- Storage backend unavailable (S3 or local filesystem): fail with clear diagnostic

**Partial Failures (Graceful Degradation Recommended):**

- OCR fails, but PDF text extraction works: use PDF extraction, mark extraction method in metadata
- Entity extraction fails, but text extraction succeeds: proceed without entity metadata, document quality score reflects this
- Chunking fails, but text is complete: use fixed-size chunks as fallback, log issue
- Quality scoring fails: assign default score (50?), flag for investigation

### Key Implementation Decisions to Make

1. **Semantic chunking approach**:
   - Use simple heuristics (Phase 1): split on paragraph breaks, respect sentence boundaries
   - Use ML-based similarity (Phase 2): sentence-transformers to identify topic shifts
   - Recommendation for Phase 1: start with heuristics, don't block on ML approach

2. **Category suggestion mechanism**:
   - Phase 1: Pattern matching (emails have "from/to", invoices have currency symbols, deeds have legal phrases)
   - Phase 2: LLM-based validation
   - Have clear rules for Phase 1 so you can understand why suggestions are made

3. **Domain context storage**:
   - Phase 1: JSON file in project (simple, human-readable)
   - Phase 2: Database table (enables rich queries, relationships)
   - Start with JSON for simplicity

4. **Error handling strategy**:
   - Decide: should one extraction failure (e.g., OCR hangs) block entire document, or should it gracefully degrade (skip OCR, use metadata extraction only)?
   - Recommendation: graceful degradation with detailed logging

### Phase 1 Implementation Priorities

1. **Core extraction pipeline working** (PDF detection, OCR, text output)
2. **Quality scoring** (visible, can validate against manual assessment)
3. **Basic metadata extraction** (dates, categories)
4. **Chunking working** (sentences/paragraphs together, maps as single units)
5. **Output contract satisfied** (Component 3 receives what it expects)
6. **Domain context tracking** (collecting candidates, no flagging logic yet)

Everything else is enhancement/refinement for Phase 2+.
