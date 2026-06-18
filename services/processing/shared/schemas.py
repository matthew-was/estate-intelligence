"""Python-side OpenAPI request/response schemas (ADR-048, PROC-003, QUERY-003)."""

from pydantic import BaseModel

# ---------------------------------------------------------------------------
# PROC-003 — POST /process (Express → Python)
# ---------------------------------------------------------------------------


class PreviousMetadataSchema(BaseModel):
    """Metadata from a previously completed pipeline run (PROC-003)."""

    documentType: str | None = None
    dates: list[str] = []
    people: list[str] = []
    organisations: list[str] = []
    landReferences: list[str] = []
    description: str | None = None


class PreviousOutputsSchema(BaseModel):
    """Outputs from previously completed pipeline steps (PROC-003, ADR-027)."""

    extractedText: str | None = None
    textPerPage: list[str] = []
    confidencePerPage: list[float] = []
    metadata: PreviousMetadataSchema | None = None


class ProcessDocumentRequest(BaseModel):
    """Request body for POST /process (PROC-003).

    Sent by Express when triggering C2 pipeline processing for one document.
    The file is accessed via a shared Docker Compose volume mount — no binary
    content is transferred over HTTP.
    """

    documentId: str
    fileReference: str
    incompleteSteps: list[str]
    previousOutputs: PreviousOutputsSchema | None = None


# ---------------------------------------------------------------------------
# PROC-002 — response shape returned from POST /process
# ---------------------------------------------------------------------------


class StepResultSchema(BaseModel):
    """Per-step processing outcome returned in the POST /process response."""

    status: str
    errorMessage: str | None = None


class DocumentFlagSchema(BaseModel):
    """A document flag raised by a pipeline step."""

    type: str
    reason: str


class ProcessingMetadataSchema(BaseModel):
    """Detected document metadata returned in the POST /process response."""

    documentType: str | None = None
    dates: list[str] = []
    people: list[str] = []
    organisations: list[str] = []
    landReferences: list[str] = []
    description: str | None = None


class ChunkSchema(BaseModel):
    """A single document chunk with its embedding."""

    chunkIndex: int
    text: str
    tokenCount: int
    embedding: list[float]


class EntitySchema(BaseModel):
    """An entity extracted by the LLM combined pass."""

    name: str
    type: str
    confidence: float
    normalisedName: str


class RelationshipSchema(BaseModel):
    """A relationship extracted by the LLM combined pass."""

    sourceEntityName: str
    targetEntityName: str
    relationshipType: str
    confidence: float


class ProcessDocumentResponse(BaseModel):
    """Response body for POST /process (PROC-003 / PROC-002 shape).

    This mirrors the ProcessingResultsRequest schema that Express expects.
    Serialised with camelCase field names for Express compatibility.
    """

    documentId: str
    stepResults: dict[str, StepResultSchema]
    flags: list[DocumentFlagSchema]
    metadata: ProcessingMetadataSchema | None = None
    chunks: list[ChunkSchema] | None = None
    entities: list[EntitySchema] | None = None
    relationships: list[RelationshipSchema] | None = None


# ---------------------------------------------------------------------------
# QUERY-003 — POST /query (CLI / Next.js → Python)
# ---------------------------------------------------------------------------


class QueryRequest(BaseModel):
    """Request body for POST /query (QUERY-003)."""

    queryText: str


class CitationSchema(BaseModel):
    """A single citation in the query response (QUERY-003)."""

    chunkId: str
    documentId: str
    documentDescription: str
    documentDate: str


class QueryResponse(BaseModel):
    """Response body for POST /query (QUERY-003).

    Serialised with camelCase field names to comply with the QUERY-003 contract.
    """

    responseText: str
    citations: list[CitationSchema]
    noResults: bool
