# Component 2 & 3 Combined: Text Extraction, Document Processing, & Embedding (UPDATED)

## Purpose

Transform raw uploaded documents into semantic chunks with embedded vectors, ready for retrieval and RAG queries.

## Scope

**Component 2** (Text Extraction & Document Processing):

- Detects PDF type (born-digital vs scanned) and extracts text appropriately
- Applies OCR to scanned documents and images
- Generates quality scores (0-100) based on extraction confidence
- Extracts and enriches metadata (refined category, dates, entities)
- Creates semantically coherent chunks with parent document references
- Tracks domain context candidates for human review and learning

**Component 3** (Embedding & Storage):

- Receives chunks from Component 2
- Generates vector embeddings via configured service (OpenAI/Anthropic/local)
- Stores embeddings + metadata + parent references in PostgreSQL with pgvector
- Enables vector similarity search and parent document retrieval for RAG

## Data Flow

```
Documents (uploaded, deduplicated)
         ↓
    Component 2: Text Extraction & Document Processing
         ↓
    - Extract text (PDF or OCR)
    - Assess quality
    - Enrich metadata
    - Chunk semantically
    - Track domain context
         ↓
    Chunks with quality scores, metadata, parent refs
         ↓
    Component 3: Embedding & Storage
         ↓
    - Generate embeddings
    - Store in pgvector
    - Enable retrieval with full context
         ↓
    Query & Retrieval (Component 4)
```

## Key Design Decisions

### Text Extraction

- **PDF Detection**: Distinguish born-digital (use PDF extraction) from scanned (use OCR)
- **OCR Engine**: Docling (structure-preserving, accepts slower processing for better quality)
- **Quality Assumption**: Docling produces acceptable text and structural information for embedding on your estate documents
- **Strategy**: Iterate on quality through real-world testing; all documents proceed (Phase 1)
- **Rationale for Docling**: Better preserves document structure (important for deeds, letters, maps); handles complex layouts better than Tesseract alone. Tradeoff: slower processing, but acceptable for learning phase.

### Quality Assessment

- **Score 0-100** based on: OCR confidence, text coherence, structural integrity, category-specific signals
- **Phase 1**: Score and proceed (no quality gates)
- **Phase 3+**: Quality gates and manual review queue enabled

### Metadata & Categorization

- **Input**: User provides creation date and broad category (letter, deed, map, plan, invoice, operational log, email, survey)
- **Processing**: Component 2 validates category, suggests alternatives, extracts key dates and entities
- **Phase 1**: Pattern-based detection (rules per category)
- **Phase 2+**: LLM-assisted validation and entity extraction

### Domain Context Learning

- **Model**: You maintain authoritative domain context document; Component 2 flags candidates
- **Mechanism**: Frequency tracking—when a term/entity appears N times (configurable), flag for your review
- **Feedback Loop**: You approve additions → Component 2 reprocesses documents with updated context
- **Prevents**: System making confident assumptions; maintains human control over terminology

### Document Chunking (Type-Specific)

- **Text Documents** (letters, deeds, invoices, operational logs):
  - Semantic chunking on logical boundaries (paragraphs, sections)
  - Target size: 500-1000 tokens
  - Preserve sentence boundaries
  
- **Maps & Plans** (primarily visual):
  - Single chunk for visual preservation
  - Separate metadata chunks for discoverable text (title, date, scale, labels)
  - Maintains coherence for image embeddings/retrieval
  
- **Email Chains** (Phase 3):
  - Individual message chunking (semantic within each message)
  - Threading metadata preserved
  - Avoids chunk size variability

### Parent Document Management

- **Reference Model**: All chunks maintain link to parent document (original file)
- **Purpose**: Enable full-document context retrieval during RAG
- **Metadata Stored**: Parent ID, chunk position, boundaries (character offset or page number)
- **Component 3 Usage**: When chunk is retrieved, parent can be fetched for extended context

## Build Phases

### Phase 1: Core Pipeline (MVP)
**Component 2:**

- PDF type detection (born-digital vs scanned)
- Text extraction (PDF extraction for born-digital, Tesseract for scanned/images)
- Quality scoring (OCR confidence + text coherence)
- Basic metadata extraction (dates, entity patterns)
- Category validation (compare extracted content to user category)
- Semantic chunking (heuristic-based: paragraphs, sections)
- Parent document reference tracking
- Domain context candidate collection (no flagging yet)

**Component 3:**

- Vector embedding generation (configurable service)
- pgvector storage of embeddings + metadata + parent references
- Basic similarity search

**Outcome**: Complete extraction → embedding → storage pipeline with real documents

### Phase 2: Enhanced Intelligence
**Component 2:**

- Domain context flagging and reprocessing workflow
- Semantic chunking refinement (ML-based topic detection)
- LLM-assisted category validation and entity extraction
- Relationship detection (document A references document B)
- Email parsing and threading preparation

**Component 3:**

- Enhanced retrieval with chunk metadata
- Quality-score-aware ranking

### Phase 3: Production Features
**Component 2:**

- Email chain parsing and individual message extraction
- Advanced deduplication (embedding similarity)
- Entity relationship extraction
- Knowledge graph building

**Component 3:**

- Graph-aware retrieval
- Knowledge graph storage and traversal

### Phase 4: Scale & Polish

- Batch processing optimization
- Performance tuning
- Advanced retrieval strategies
- Monitoring and quality metrics

## Configuration Points

**Component 2:**

- OCR engine (Tesseract default)
- Chunking strategy per document type
- Quality score weighting
- Domain context flagging threshold
- Text extraction library
- Entity extraction patterns

**Component 3:**

- Embedding service (OpenAI/Anthropic/local)
- Vector dimension handling
- Storage backend (PostgreSQL with pgvector)
- Search ranking strategy

## Success Criteria

**Phase 1 Complete:**

- Text extracted and readable for 95%+ of documents
- Quality scores reflect real extraction quality (validated against manual assessment)
- Chunks are semantically coherent (related content stays together)
- Parent references valid and retrievable
- Output contract satisfied (Component 3 can deserialize and process)
- Domain context candidates collected and reviewable

**Phase 2 Complete:**

- Domain context flagging working (user approves >80% of suggestions)
- Reprocessing improves document metadata and categorization
- LLM-assisted classification measurably more accurate

**Phase 3+ Complete:**

- Email parsing functional
- Entity relationships detected
- Knowledge graph queryable
- Users can trace document relationships across time

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
|------|------------|-----------|
| OCR quality insufficient | Medium | Quality scoring provides visibility; real-world iteration on real docs |
| Semantic chunking breaks coherence | Low | Observable in Phase 1; adjust heuristics or upgrade to ML-based |
| Domain context learning too slow | Low | Frequency tracking enables batching; Phase 2 adds automation |
| Parent reference model adds overhead | Low | Standard pattern in production systems; optimize if needed |
| User overwhelmed by domain context feedback | Medium | Configurable threshold; Phase 2 adds filtering |

## Dependencies & Assumptions

### About Documents

- Mostly typewritten (not handwritten) → OCR viable
- Date/date-range discoverable → user can provide
- Broad categories apply → user can classify initially
- Naming conventions exist → domain context learning will help

### About Infrastructure

- PostgreSQL available with pgvector extension
- S3 or local filesystem for storage
- Python environment for Component 2
- Embedding service available (OpenAI/Anthropic/local model)

### About Users

- Have time to review domain context suggestions
- Can update domain context periodically
- Willing to iterate on classification if needed
- Want to learn system deeply (not just use black-box)

## Integration Points

**Component 2 ← Component 1 (Intake)**

- Documents stored in S3/filesystem
- File metadata in database
- Deduplication already applied

**Component 2 → Component 3 (Embedding)**

- Chunks with parent references
- Quality scores per chunk
- Enriched metadata
- Treatment tags (reference vs. content, etc.)

**Component 3 ← Component 4 (Query & Retrieval)**

- Vector search queries
- Parent document retrieval requests
- Quality score filters (Phase 3+)

**Component 2 ← User Input (Domain Context)**

- Domain context document maintained by user
- Feedback on suggested candidates (Phase 2+)
- Category updates when suggestions missed

## Notes for Implementation

- Component 2 and 3 are logically separate but designed together
- Component 2 is Python-primary; Component 3 can be any language with pgvector support
- Quality scoring is critical—must reflect real extraction quality for trust in downstream components
- Domain context model enables safe, incremental learning without system "running away" with assumptions
- Parent document references enable high-quality RAG by preserving context
