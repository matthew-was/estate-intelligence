"""FastAPI application entry point (ADR-042, ADR-044)."""

from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Annotated

import structlog
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from pipeline.factories.completeness_scorer_factory import create_completeness_scorer
from pipeline.factories.metadata_factory import create_metadata_extractor
from pipeline.factories.ocr_factory import create_ocr_service
from pipeline.factories.quality_scorer_factory import create_quality_scorer
from pipeline.interfaces.metadata_extractor import MetadataResult
from pipeline.orchestrator import (
    PipelineOrchestrator,
    PreviousOutputs,
    ProcessingRequest,
    ProcessingResponse,
)
from query.query_handler import QueryHandler
from query.response_synthesis import SynthesisResult
from query.router_factory import create_query_router
from shared.config import config
from shared.factories.embedding_factory import create_embedding_service
from shared.factories.http_client import create_http_client
from shared.factories.llm_factory import (
    create_llm_service,
    create_llm_service_for_query,
)
from shared.interfaces.embedding_service import EmbeddingService
from shared.interfaces.http_client import HttpClientBase
from shared.schemas import (
    ChunkSchema,
    CitationSchema,
    DocumentFlagSchema,
    EntitySchema,
    ProcessDocumentRequest,
    ProcessDocumentResponse,
    ProcessingMetadataSchema,
    QueryRequest,
    QueryResponse,
    RelationshipSchema,
    StepResultSchema,
)

_log = structlog.get_logger().bind(service="app")


@dataclass
class _AppDeps:
    """Container for application-level dependencies created at startup."""

    pipeline: PipelineOrchestrator
    query: QueryHandler
    http_client: HttpClientBase
    embedding: EmbeddingService


# ---------------------------------------------------------------------------
# Lifespan — startup and teardown
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Create all service instances once at startup and tear them down at shutdown."""
    _log.info("service_starting")

    http_client = create_http_client(
        auth_config=config.AUTH,
        service_config=config.SERVICE,
        log=_log,
    )
    ocr = create_ocr_service(config=config.PROCESSING.OCR, log=_log)
    llm = create_llm_service(config=config.PROCESSING.LLM, log=_log)
    query_llm = create_llm_service_for_query(config=config.QUERY.LLM, log=_log)
    embedding = create_embedding_service(config=config.PROCESSING.EMBEDDING, log=_log)
    quality_scorer = create_quality_scorer(config=config.PROCESSING.OCR, log=_log)
    metadata_extractor = create_metadata_extractor(
        config=config.PROCESSING.METADATA, log=_log
    )
    completeness_scorer = create_completeness_scorer(
        config=config.PROCESSING.METADATA, log=_log
    )

    pipeline = PipelineOrchestrator(
        ocr_service=ocr,
        quality_scorer=quality_scorer,
        metadata_extractor=metadata_extractor,
        completeness_scorer=completeness_scorer,
        llm_service=llm,
        embedding_service=embedding,
        http_client=http_client,
        llm_config=config.PROCESSING.LLM,
        embedding_config=config.PROCESSING.EMBEDDING,
        log=_log,
    )
    query_router = create_query_router(config=config.QUERY)
    query_handler = QueryHandler(
        query_router=query_router,
        llm_service=query_llm,
        embedding_service=embedding,
        http_client=http_client,
        vector_search_config=config.QUERY.VECTOR_SEARCH,
        context_assembly_config=config.QUERY.CONTEXT_ASSEMBLY,
        log=_log,
    )

    app.state.deps = _AppDeps(
        pipeline=pipeline,
        query=query_handler,
        http_client=http_client,
        embedding=embedding,
    )
    _log.info("service_started")

    yield

    _log.info("service_stopping")
    await http_client.aclose()
    await llm.close()
    await query_llm.close()
    await embedding.close()
    _log.info("service_stopped")


app = FastAPI(lifespan=lifespan)


# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Return HTTP 400 for request body validation failures.

    FastAPI defaults to 422 Unprocessable Entity, but the PROC-003 and QUERY-003
    contracts specify 400 Bad Request for invalid request bodies.
    """
    return JSONResponse(
        status_code=400,
        content={"detail": "Bad Request", "errors": exc.errors()},
    )


# ---------------------------------------------------------------------------
# Auth middleware
# ---------------------------------------------------------------------------


@app.middleware("http")
async def internal_key_auth_middleware(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    if request.url.path == "/health":
        return await call_next(request)
    elif (
        "x-internal-key" not in request.headers
        or request.headers["x-internal-key"] != config.AUTH.INBOUND_KEY
    ):
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    else:
        return await call_next(request)


# ---------------------------------------------------------------------------
# Dependency providers
# ---------------------------------------------------------------------------


def _get_pipeline(request: Request) -> PipelineOrchestrator:
    deps: _AppDeps = request.app.state.deps
    return deps.pipeline


def _get_query_handler(request: Request) -> QueryHandler:
    deps: _AppDeps = request.app.state.deps
    return deps.query


# ---------------------------------------------------------------------------
# Helpers — map internal dataclasses to response schemas
# ---------------------------------------------------------------------------


def _map_processing_response(internal: ProcessingResponse) -> ProcessDocumentResponse:
    """Map an internal ProcessingResponse dataclass to the Pydantic response schema."""

    step_results_schema: dict[str, StepResultSchema] = {
        step: StepResultSchema(
            status=result.status,
            errorMessage=result.error_message,
        )
        for step, result in internal.step_results.items()
    }

    flags_schema = [
        DocumentFlagSchema(type=f.type, reason=f.reason) for f in internal.flags
    ]

    meta = internal.metadata
    metadata_schema: ProcessingMetadataSchema | None = None
    if meta is not None:
        metadata_schema = ProcessingMetadataSchema(
            documentType=meta.document_type,
            dates=meta.dates,
            people=meta.people,
            organisations=meta.organisations,
            landReferences=meta.land_references,
            description=meta.description,
        )

    chunks_schema: list[ChunkSchema] | None = None
    if internal.chunks is not None:
        chunks_schema = [
            ChunkSchema(
                chunkIndex=chunk.chunk_index,
                text=chunk.text,
                tokenCount=chunk.token_count,
                embedding=chunk.embedding,
            )
            for chunk in internal.chunks
        ]

    entities_schema: list[EntitySchema] | None = None
    if internal.entities is not None:
        entities_schema = [
            EntitySchema(
                name=ent.name,
                type=ent.type,
                confidence=ent.confidence,
                normalisedName=ent.normalised_name,
            )
            for ent in internal.entities
        ]

    relationships_schema: list[RelationshipSchema] | None = None
    if internal.relationships is not None:
        relationships_schema = [
            RelationshipSchema(
                sourceEntityName=rel.source_entity_name,
                targetEntityName=rel.target_entity_name,
                relationshipType=rel.relationship_type,
                confidence=rel.confidence,
            )
            for rel in internal.relationships
        ]

    return ProcessDocumentResponse(
        documentId=internal.document_id,
        stepResults=step_results_schema,
        flags=flags_schema,
        metadata=metadata_schema,
        chunks=chunks_schema,
        entities=entities_schema,
        relationships=relationships_schema,
    )


def _map_synthesis_result(result: SynthesisResult) -> QueryResponse:
    """Map an internal SynthesisResult dataclass to the Pydantic response schema."""
    citations_schema = [
        CitationSchema(
            chunkId=c.chunk_id,
            documentId=c.document_id,
            documentDescription=c.document_description,
            documentDate=c.document_date,
        )
        for c in result.citations
    ]
    return QueryResponse(
        responseText=result.response_text,
        citations=citations_schema,
        noResults=result.no_results,
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/process", response_model=ProcessDocumentResponse)
async def process_document(
    body: ProcessDocumentRequest,
    pipeline: Annotated[PipelineOrchestrator, Depends(_get_pipeline)],
) -> ProcessDocumentResponse:
    """Process a single document through the C2 pipeline (PROC-003)."""
    prev = body.previousOutputs
    previous_outputs: PreviousOutputs | None = None
    if prev is not None:
        prev_meta = prev.metadata
        metadata: MetadataResult | None = None
        if prev_meta is not None:
            metadata = MetadataResult(
                document_type=prev_meta.documentType,
                dates=prev_meta.dates,
                people=prev_meta.people,
                organisations=prev_meta.organisations,
                land_references=prev_meta.landReferences,
                description=prev_meta.description,
                detection_confidence={},
            )
        previous_outputs = PreviousOutputs(
            extracted_text=prev.extractedText,
            text_per_page=prev.textPerPage,
            confidence_per_page=prev.confidencePerPage,
            metadata=metadata,
        )

    request = ProcessingRequest(
        document_id=body.documentId,
        file_reference=body.fileReference,
        incomplete_steps=body.incompleteSteps,
        previous_outputs=previous_outputs,
    )

    _log.info("pipeline_request_received", document_id=body.documentId)
    internal_response = await pipeline.process(request)
    return _map_processing_response(internal_response)


@app.post("/query", response_model=QueryResponse)
async def query_documents(
    body: QueryRequest,
    query_handler: Annotated[QueryHandler, Depends(_get_query_handler)],
) -> QueryResponse:
    """Run the C3 query pipeline for the given query text (QUERY-003)."""
    if body.queryText.strip() == "":
        raise HTTPException(status_code=400, detail="queryText must not be empty")

    _log.info("query_request_received")
    result = await query_handler.handle(body.queryText)
    return _map_synthesis_result(result)
