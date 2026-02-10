# Component 3: Query & Retrieval

**Status**: Design pending. Complete Components 1 and 2 before designing this component. Use this document as the starting brief for the Component 3 design conversation.

---

## Responsibility

Component 3 is the interface between the processed document archive and the developer (or future users). It accepts natural language queries, searches the vector store, assembles context, and generates answers via a configured LLM.

**What it owns**:
- Query embedding (same abstraction layer as document embedding)
- Vector similarity search against pgvector
- Parent document retrieval for extended RAG context
- Context assembly and prompt construction
- LLM response generation (configurable provider)
- Response formatting (answer + source citations)

---

## What Component 2 Delivers to Component 3

Component 2 (Embedding stage) stores into PostgreSQL + pgvector:

- **Chunks**: content, chunkId, parentDocumentId, chunkPosition, chunkType, treatmentTags (metadata-chunk, reference-only, etc.), semanticTopic
- **Quality scores**: per chunk (0–100), extraction method, OCR confidence
- **Enriched metadata**: refinedCategory, extractedDates, detectedEntities, structuralMarkers
- **Parent document references**: link back to original file in storage
- **Treatment guidance**: metadata chunks should rank differently to content chunks; reference-only tags indicate map/plan chunks

---

## Open Design Questions (From Component 2)

These questions were identified during Component 2 design and must be answered during Component 3 design:

1. **Parent document retrieval strategy**: Always retrieve full parent document for RAG context, or retrieve on request only? What triggers parent retrieval?
2. **Low-quality chunk handling**: Exclude chunks below a quality threshold from search? Weight them lower in ranking? Include with a warning in the response? (Quality gates come in Phase 3+ per ADR-C2-002)
3. **Metadata chunk ranking strategy**: Metadata chunks (from maps/plans) should be discoverable but rank differently to content chunks. How?
4. **Duplicate-similar detection**: If two chunks from different documents are near-identical (embedding similarity), how should search results handle this?

---

## Known Requirements by Phase

### Phase 1: CLI Query Tool

- Accept natural language query via command line
- Embed query using configured embedding service (same abstraction as document embedding)
- Search pgvector for top-N similar chunks
- Assemble retrieved chunks as context
- Feed context + query to configured LLM (Claude/GPT/local)
- Return answer to terminal
- Show source citations (document name, date, chunk reference)

### Phase 2: Web UI

- Simple web interface for queries
- Same backend logic as Phase 1 CLI
- Query history (nice to have)

### Phase 3: Advanced Retrieval

- Graph-aware retrieval when entity relationships are built (Component 2 Phase 3)
- Better search filtering (by date range, document type, entity)
- Query understanding (date extraction from query, entity recognition)
- Confidence/uncertainty signalling ("I found 3 documents that suggest X, but they contradict Y")

---

## Known Configuration Points

Following the infrastructure-as-configuration principle:
- Embedding service (same provider used for document embedding; must match)
- LLM provider (Claude, GPT, local model) — abstraction enables switching
- Number of chunks to retrieve (top-N, configurable)
- Quality score threshold for inclusion (Phase 3+)
- Response format (answer-only, answer + citations, structured JSON)

---

## Known Assumptions

- PostgreSQL + pgvector available (set up by Component 2)
- Embedding dimensions match between query embedding and stored document embeddings
- LLM provider abstraction is available (shared skill with Component 2 embedding stage)
- Parent document storage references are valid (Component 2 guarantee)

---

## When Ready to Design

1. Ensure Component 2 (Phase 1) is complete and the output contract is validated
2. Review [project/architecture.md](../../project/architecture.md) for full system context
3. Review [components/component-2-processing-and-embedding/specification.md](../component-2-processing-and-embedding/specification.md) — the "Internal Stage: Embedding & Storage" section defines exactly what Component 3 reads
4. Review [decisions/unresolved-questions.md](../../decisions/unresolved-questions.md) — UQ-POST-005 (query latency) should be answered first
5. Answer the 4 open design questions above
6. Start Component 3 design conversation with this README as the brief
