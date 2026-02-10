# Family Estate Document Archive System - Project Context

## Project Goals

This is a dual-purpose project:

1. **Preserve family history**: Backup and archive historic documents from a family farming estate
2. **Learn AI fundamentals**: Understand document processing pipelines and how to build an AI-powered knowledge base from a large corpus of information

## Document Scope

- **Time range**: 1950s to present
- **Initial scale**: Hundreds of documents for learning phase
- **Target scale**: Tens of thousands of documents
- **Document types**:
  - Handwritten letters (scanned)
  - Typewritten documents (scanned)
  - Modern emails and PDFs
  - Physical documents requiring digitization via scanning

## Key Use Cases

The system needs to answer questions such as:

- Land ownership inquiries ("What is known about ownership of the north field?")
- Infrastructure history ("Where were pipes laid through fields if a leak is found?")
- Decision summaries ("What decisions were made about purchase or sale of certain plots?")

## Technical Background

**Developer Experience**:

- 9 years full-stack web development (JavaScript/TypeScript)
- Docker and Linux environments
- PostgreSQL (extensive), MongoDB (limited, needs refresh)
- AWS: EC2, ECS, S3, some OpenSearch experience
- Python, Java, .NET (limited, willing to expand Python knowledge)

**Preferred Tech Stack**:

- TypeScript/Node.js for orchestration
- Python for OCR and AI/ML components
- PostgreSQL with pgvector extension (vector search)
- Docker containers for pipeline components
- AWS S3 for document storage
- AWS ecosystem overall

## Architectural Principles

### Infrastructure as Configuration

All infrastructure choices must be pluggable and configurable. The application code should not branch based on deployment environment or service choice. This allows seamless movement from local development to production AWS infrastructure.

**Key abstraction points**:

- **Compute**: All processing runs in Docker containers. Whether containers run locally, on EC2, or ECS is determined by environment configuration, not code.
- **Document storage**: Abstract S3/local filesystem operations behind a common interface. Code uses the abstraction; configuration determines backend.
- **Database connections**: PostgreSQL connection string and pool configuration via environment. Same code path for local Docker Postgres, RDS, or other managed services.
- **Vector database**: Same abstraction principle for pgvector queries.
- **LLM/embedding services**: All calls to Claude, GPT, local models, or other LLMs route through abstraction layer. Configuration determines provider and model.
- **OCR engines**: Tesseract and future OCR alternatives accessed via common interface.

**Implementation approach**: Each major service should expose a well-defined interface/contract. Concrete implementations (e.g., S3Adapter, LocalFilesystemAdapter) are swappable. Factory patterns or dependency injection determine which implementation loads at runtime based on configuration.

## System Architecture

### Pipeline Components

**1. Document Intake**

- Physical document scanning → digital files
- Digital file upload interface
- Original file storage (configured backend: S3 or local filesystem)

**2. Text Extraction & Document Processing**

- OCR engine (Tesseract, with abstraction for alternatives)
- PDF text extraction
- Email parsing and message extraction
- Quality assessment
- Metadata extraction (dates, document types, entities)
- Deduplication detection (hash-based and embedding similarity)
- Document chunking (semantic boundaries)
- Special handling for email chains to extract individual messages
- *Phase 2/3 enhancement: Entity relationship extraction and knowledge graph building (Graph-RAG foundations)*

**3. Embedding & Storage**

- Vector embedding generation (configurable: OpenAI/Anthropic APIs or local models)
- Storage in PostgreSQL with pgvector
- Metadata storage
- References to original documents (via configured storage backend)
- *Phase 2/3 enhancement: Knowledge graph storage alongside vectors*

**4. Query & Retrieval**

- Search interface (initially CLI, later web UI)
- Vector similarity search
- RAG (Retrieval Augmented Generation) implementation
- Response generation via configured LLM provider
- *Phase 2/3 enhancement: Graph-aware retrieval that traverses relationships alongside vector search*

**5. Continuous Ingestion**

- Monitoring for new documents
- Automated processing pipeline triggers
- Version control and change tracking

### Important Metadata Requirements

Documents should track:

- Date/date ranges
- Document type (deed, letter, email, survey, operational log, etc.)
- Entities mentioned (people, plot references, infrastructure)
- Relationships between documents
- Threading information for emails
- Processing metadata (OCR confidence, extraction date, embedding model used)

### Deduplication Strategy

- File hashing for exact duplicates
- Embedding similarity for near-duplicates
- Email-specific: parse individual messages from threads, extract by headers/separators
- Store each email message separately with threading metadata
- Content hashing to identify quoted/forwarded portions
- Create embeddings only for new content, not quoted replies

## Phased Build Approach

### Phase 1 - Minimum Viable Pipeline (Starting Point)

- Manual file upload (simple web form)
- Basic text extraction (PDF-only initially)
- Minimal metadata (filename, date added, document type)
- No deduplication (flag for later)
- Simple chunking (fixed size or page-based)
- Basic embedding + pgvector storage
- Command-line query tool
- **Configuration-first**: All infrastructure abstractions in place but with sensible defaults for local development

**Goal**: Small, complete system to establish baseline. All components designed with configuration surface exposed—what can be swapped, what loads from environment.

### Phase 2 - Essential Intelligence

- Add OCR for scanned documents
- Smarter chunking (semantic boundaries)
- Basic deduplication (file hashing)
- Enhanced metadata extraction
- Simple web UI for queries
- Begin entity extraction in text processing pipeline

### Phase 3 - Production Features

- Email parsing and thread handling
- Advanced deduplication (embedding similarity)
- Entity relationship extraction
- Knowledge graph building (Graph-RAG foundations)
- Graph-aware retrieval alongside vector search
- Better search filtering
- Document relationships

### Phase 4 - Scale & Polish

- Batch processing improvements
- Performance optimization
- Advanced retrieval strategies
- Monitoring and quality metrics

## Design Principles

- **Start small**: Build complete end-to-end pipeline with simplest cases first
- **Infrastructure as code**: All infrastructure choices configurable from day one
- **Incremental expansion**: Add complexity component by component
- **Real-world testing**: Use actual family documents, not toy datasets
- **Maintainability**: Design for ongoing document addition and infrastructure flexibility
- **Learning-focused**: Understand each step deeply, not just use black-box solutions
- **Production-ready patterns**: Apply patterns from day one that will scale to AWS, not patterns that require rewriting later

## Development Infrastructure

**Local Development**:

- Docker Compose orchestrates local services (PostgreSQL, optional local LLM, application containers)
- Refurbished server or local machine runs full pipeline for iteration
- Configuration points to local services by default

**Transition to AWS**:

- Same application code and containers
- Configuration points to RDS, S3, Bedrock/API endpoints instead
- Docker runs on EC2 or migrates to ECS
- No code rewrites required

## Data Flow

1. Documents → Configured storage backend (S3 or local filesystem, originals preserved)
2. Text extraction & document processing → Raw text, entities, relationships (Phase 3+), chunks + metadata
3. Embedding → Vectors (via configured embedding service)
4. Storage → PostgreSQL (vectors + metadata + graph relationships, with references to storage backend)
5. Query → Vector/graph search → RAG (via configured LLM) → Answer

## Next Steps

Each pipeline component can be explored in detail in separate conversations:

- Component-specific technology choices and abstraction patterns
- Data schemas and API contracts
- Configuration and dependency injection strategies
- Success criteria and testing approaches

---

*Use this document as context when starting new chats about specific components of this system.*
