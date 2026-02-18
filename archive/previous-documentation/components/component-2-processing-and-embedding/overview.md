# Component 2: Text Extraction, Processing & Embedding — Overview

## Purpose

Transform raw uploaded documents into semantic chunks with embedded vectors, ready for retrieval and RAG queries.

## Scope

This component has two internal stages designed together as a unified pipeline:

**Stage A — Text Extraction & Document Processing**:

- Detects PDF type (born-digital vs scanned) and extracts text appropriately
- Applies OCR (Docling primary, Tesseract fallback) to scanned documents and images
- Generates quality scores (0–100) based on extraction confidence
- Extracts and enriches metadata (refined category, dates, entities)
- Creates semantically coherent chunks with parent document references
- Tracks domain context candidates for human review and learning

**Stage B — Embedding & Storage**:

- Receives chunks from Stage A
- Generates vector embeddings via configured service (OpenAI/Anthropic/local)
- Stores embeddings + metadata + parent references in PostgreSQL with pgvector
- Enables vector similarity search and parent document retrieval for RAG

## Data Flow

```text
Documents (uploaded, deduplicated by Component 1)
         ↓
    Stage A: Text Extraction & Document Processing
         ↓
    - Extract text (PDF extraction or OCR)
    - Assess quality (0-100 score)
    - Enrich metadata (category, dates, entities)
    - Chunk semantically (type-specific strategies)
    - Track domain context candidates
         ↓
    Chunks with quality scores, metadata, parent refs
         ↓
    Stage B: Embedding & Storage
         ↓
    - Generate embeddings (configurable provider)
    - Store in PostgreSQL + pgvector
    - Enable retrieval with full parent context
         ↓
    Component 3: Query & Retrieval
```

## Key Design Decisions

### Text Extraction

- **PDF Detection**: Distinguish born-digital (use PDF extraction) from scanned (use OCR)
- **OCR Engine**: Docling (structure-preserving, accepts slower processing for better quality)
- **Quality Assumption**: Docling produces acceptable text and structural information for embedding on estate documents
- **Strategy**: Iterate on quality through real-world testing; all documents proceed in Phase 1
- **Rationale for Docling**: Better preserves document structure (important for deeds, letters, maps); handles complex layouts better than Tesseract alone. Tradeoff: slower processing, acceptable for learning phase

### Quality Assessment

- Score 0–100 based on: OCR confidence, text coherence, structural integrity, category-specific signals
- **Phase 1**: Score and proceed (no quality gates). Quality scores recorded for future use
- **Phase 3+**: Quality gates and manual review queue enabled

### Metadata & Categorisation

- **Input**: User provides creation date and broad category (letter, deed, map, plan, invoice, operational log, email, survey)
- **Processing**: Stage A validates category, suggests alternatives, extracts key dates and entities
- **Phase 1**: Pattern-based detection (rules per category)
- **Phase 2+**: LLM-assisted validation and entity extraction

### Domain Context Learning

- **Model**: Developer maintains authoritative domain context document; Component 2 flags candidates
- **Mechanism**: Frequency tracking — when a term/entity appears N times (configurable), flag for developer review
- **Feedback Loop**: Developer approves additions → Stage A reprocesses documents with updated context
- **Prevents**: System making confident assumptions; maintains human control over terminology

### Document Chunking (Type-Specific)

- **Text documents** (letters, deeds, invoices, operational logs):
  - Semantic chunking on logical boundaries (paragraphs, sections)
  - Target size: 500–1000 tokens
  - Preserve sentence boundaries

- **Maps & Plans** (primarily visual):
  - Single chunk for visual preservation
  - Separate metadata chunks for discoverable text (title, date, scale, labels)
  - Maintains coherence for image embeddings/retrieval

- **Email chains** (Phase 3):
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

**Stage A**:

- PDF type detection (born-digital vs scanned)
- Text extraction (PDF extraction for born-digital, Docling/Tesseract for scanned/images)
- Quality scoring (OCR confidence + text coherence)
- Basic metadata extraction (dates, entity patterns)
- Category validation (compare extracted content to user category)
- Semantic chunking (heuristic-based: paragraphs, sections)
- Parent document reference tracking
- Domain context candidate collection (no flagging yet)

**Stage B**:

- Vector embedding generation (configurable service)
- pgvector storage of embeddings + metadata + parent references
- Basic similarity search

**Outcome**: Complete extraction → embedding → storage pipeline with real documents

### Phase 2: Enhanced Intelligence

**Stage A**:

- Domain context flagging and reprocessing workflow
- Semantic chunking refinement (ML-based topic detection)
- LLM-assisted category validation and entity extraction
- Relationship detection (document A references document B)
- Email parsing and threading preparation

**Stage B**:

- Enhanced retrieval with chunk metadata
- Quality-score-aware ranking

### Phase 3: Production Features

**Stage A**:

- Email chain parsing and individual message extraction
- Advanced deduplication (embedding similarity)
- Entity relationship extraction
- Knowledge graph building

**Stage B**:

- Graph-aware retrieval
- Knowledge graph storage and traversal

### Phase 4: Scale & Polish

- Batch processing optimisation
- Performance tuning
- Advanced retrieval strategies
- Monitoring and quality metrics

## Configuration Points

**Stage A**:

- OCR engine (Docling default, Tesseract fallback)
- Chunking strategy per document type
- Quality score weighting
- Domain context flagging threshold
- Text extraction library
- Entity extraction patterns

**Stage B**:

- Embedding service (OpenAI/Anthropic/local)
- Vector dimension handling
- Storage backend (PostgreSQL with pgvector)
- Search ranking strategy

## Success Criteria

**Phase 1 Complete**:

- Text extracted and readable for 95%+ of documents
- Quality scores reflect real extraction quality (validated against manual assessment)
- Chunks are semantically coherent (related content stays together)
- Parent references valid and retrievable
- Output contract satisfied (Stage B can deserialise and process)
- Domain context candidates collected and reviewable

**Phase 2 Complete**:

- Domain context flagging working (developer approves >80% of suggestions)
- Reprocessing improves document metadata and categorisation
- LLM-assisted classification measurably more accurate

**Phase 3+ Complete**:

- Email parsing functional
- Entity relationships detected
- Knowledge graph queryable
- Users can trace document relationships across time

## Risks & Mitigations

| Risk | Likelihood | Mitigation |
| --- | --- | --- |
| OCR quality insufficient | Medium | Quality scoring provides visibility; real-world iteration on real docs |
| Semantic chunking breaks coherence | Low | Observable in Phase 1; adjust heuristics or upgrade to ML-based |
| Domain context learning too slow | Low | Frequency tracking enables batching; Phase 2 adds automation |
| Parent reference model adds overhead | Low | Standard pattern in production systems; optimise if needed |
| Developer overwhelmed by domain context feedback | Medium | Configurable threshold; Phase 2 adds filtering |

## Dependencies & Assumptions

**About Documents**:

- Mostly typewritten (not handwritten) — OCR viable
- Date/date-range discoverable — user can provide
- Broad categories apply — user can classify initially
- Naming conventions exist — domain context learning will help

**About Infrastructure**:

- PostgreSQL available with pgvector extension
- S3 or local filesystem for storage
- Python environment for Stage A
- Embedding service available (OpenAI/Anthropic/local model)

## Integration Points

**Component 2 ← Component 1 (Intake)**:

- Documents stored in S3/filesystem
- File metadata in database
- Deduplication already applied

**Stage A → Stage B (Internal)**:

- Chunks with parent references
- Quality scores per chunk
- Enriched metadata
- Treatment tags (reference vs content, etc.)

**Component 2 → Component 3 (Query & Retrieval)**:

- Vector similarity search queries
- Parent document retrieval requests
- Quality score filters (Phase 3+)

**Component 2 ← Developer (Domain Context)**:

- Domain context document maintained by developer
- Feedback on suggested candidates (Phase 2+)
- Category updates when suggestions missed

## Notes for Implementation

- Stage A is Python-primary (OCR, NLP, text processing)
- Stage B can be any language with pgvector support
- Quality scoring is critical — must reflect real extraction quality for trust in downstream components
- Domain context model enables safe, incremental learning without system running away with assumptions
- Parent document references enable high-quality RAG by preserving context
