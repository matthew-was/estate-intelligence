"""Tests for app.py — auth middleware and route wiring (Task 4, Task 20)."""

from collections.abc import AsyncGenerator

import httpx
import pytest

from app import _get_pipeline, _get_query_handler, app
from pipeline.interfaces.pipeline_models import DocumentFlag
from pipeline.orchestrator import (
    ProcessingResponse,
    StepResult,
)
from shared.config import config
from tests.fakes.pipeline import FakePipeline
from tests.fakes.query_handler import FakeQueryHandler

VALID_KEY = config.AUTH.INBOUND_KEY
INVALID_KEY = "invalid_key"

# ---------------------------------------------------------------------------
# Dependency override wrappers
# ---------------------------------------------------------------------------


def _override_pipeline() -> FakePipeline:
    return FakePipeline()


def _override_query_handler() -> FakeQueryHandler:
    return FakeQueryHandler()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
async def client() -> AsyncGenerator[httpx.AsyncClient]:
    """Unauthenticated client — middleware tests use this to test 401 paths."""
    app.dependency_overrides[_get_pipeline] = _override_pipeline
    app.dependency_overrides[_get_query_handler] = _override_query_handler
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers() -> dict[str, str]:
    return {"x-internal-key": VALID_KEY}


# ---------------------------------------------------------------------------
# Task 4 — Auth middleware tests (AC-5: all must still pass)
# ---------------------------------------------------------------------------


@pytest.mark.ci_integration
async def test_health_route_no_auth(client: httpx.AsyncClient) -> None:
    r = await client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"


@pytest.mark.ci_integration
async def test_api_process_fail_with_wrong_auth(client: httpx.AsyncClient) -> None:
    r = await client.post("/process", headers={"x-internal-key": INVALID_KEY})
    assert r.status_code == 401


@pytest.mark.ci_integration
async def test_api_process_fail_with_no_auth(client: httpx.AsyncClient) -> None:
    r = await client.post("/process")
    assert r.status_code == 401


@pytest.mark.ci_integration
async def test_api_query_fail_with_no_auth(client: httpx.AsyncClient) -> None:
    r = await client.post("/query")
    assert r.status_code == 401


# ---------------------------------------------------------------------------
# Task 20 — AC-1: POST /process with valid body and auth returns 200
# ---------------------------------------------------------------------------


@pytest.mark.ci_integration
async def test_process_valid_body_and_auth_returns_200(
    client: httpx.AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    body = {
        "documentId": "doc-abc-123",
        "fileReference": "/data/docs/test.pdf",
        "incompleteSteps": ["text_extraction"],
        "previousOutputs": None,
    }
    r = await client.post("/process", json=body, headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    # Verify the response shape matches ProcessDocumentResponse
    assert "documentId" in data
    assert data["documentId"] == "doc-abc-123"
    assert "stepResults" in data
    assert "flags" in data
    assert isinstance(data["flags"], list)


# ---------------------------------------------------------------------------
# Task 20 — AC-2: POST /process with invalid body returns 400
# ---------------------------------------------------------------------------


@pytest.mark.ci_integration
async def test_process_invalid_body_returns_400(
    client: httpx.AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    # Missing required fields — custom exception handler converts 422 → 400
    r = await client.post("/process", json={"notAField": "value"}, headers=auth_headers)
    assert r.status_code == 400


# ---------------------------------------------------------------------------
# Task 20 — AC-3: POST /query with valid body and auth returns 200 with correct fields
# ---------------------------------------------------------------------------


@pytest.mark.ci_integration
async def test_query_valid_body_and_auth_returns_200_with_correct_fields(
    client: httpx.AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    body = {"queryText": "Who owned East Meadow?"}
    r = await client.post("/query", json=body, headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert "responseText" in data
    assert "citations" in data
    assert "noResults" in data
    # Verify types are correct
    assert isinstance(data["responseText"], str)
    assert isinstance(data["citations"], list)
    assert isinstance(data["noResults"], bool)


# ---------------------------------------------------------------------------
# Task 20 — AC-4: POST /query with empty queryText returns 400
# ---------------------------------------------------------------------------


@pytest.mark.ci_integration
async def test_query_empty_query_text_returns_400(
    client: httpx.AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    body = {"queryText": ""}
    r = await client.post("/query", json=body, headers=auth_headers)
    assert r.status_code == 400


@pytest.mark.ci_integration
async def test_query_whitespace_only_query_text_returns_400(
    client: httpx.AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    body = {"queryText": "   "}
    r = await client.post("/query", json=body, headers=auth_headers)
    assert r.status_code == 400


# ---------------------------------------------------------------------------
# Additional: verify auth middleware still active after route wiring
# ---------------------------------------------------------------------------


@pytest.mark.ci_integration
async def test_process_with_valid_auth_reaches_handler(
    client: httpx.AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    """Regression: middleware passes valid key through to the real route (not 401).

    This test supersedes the Task 4 ``test_api_success_with_auth`` test, which
    asserted HTTP 501 when routes were stubs. The route now returns 200 with a real
    handler, so 501 can no longer pass. The auth concern (valid key is not rejected)
    is covered here by asserting 200 rather than 401 or 501.
    """
    body: dict[str, object] = {
        "documentId": "doc-xyz",
        "fileReference": "/data/docs/doc.pdf",
        "incompleteSteps": [],
        "previousOutputs": None,
    }
    r = await client.post("/process", json=body, headers=auth_headers)
    # 200 proves the middleware passed the request through (not 401)
    assert r.status_code == 200


# ---------------------------------------------------------------------------
# Additional: verify flags and metadata shape in process response
# ---------------------------------------------------------------------------


@pytest.mark.ci_integration
async def test_process_response_includes_step_results(
    client: httpx.AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    body = {
        "documentId": "doc-step-check",
        "fileReference": "/data/docs/file.pdf",
        "incompleteSteps": ["text_extraction"],
        "previousOutputs": None,
    }
    r = await client.post("/process", json=body, headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    step_results = data["stepResults"]
    assert isinstance(step_results, dict)
    assert "text_extraction" in step_results
    step = step_results["text_extraction"]
    assert step["status"] == "completed"


# ---------------------------------------------------------------------------
# Additional: verify query response contains citation fields
# ---------------------------------------------------------------------------


@pytest.mark.ci_integration
async def test_query_response_citation_has_correct_fields(
    client: httpx.AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    # FakeQueryHandler returns a deterministic CitationResult — assert exact values
    # (per CR-015: presence-only assertions are weaker than value assertions)
    body = {"queryText": "Tell me about East Meadow"}
    r = await client.post("/query", json=body, headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert len(data["citations"]) == 1
    citation = data["citations"][0]
    assert citation["chunkId"] == "chunk-1"
    assert citation["documentId"] == "doc-1"
    assert citation["documentDescription"] == "Test document"
    assert citation["documentDate"] == "1967-03-15"


# ---------------------------------------------------------------------------
# Process route — DocumentFlag in response
# ---------------------------------------------------------------------------


@pytest.mark.ci_integration
async def test_process_response_flags_field_is_list(
    client: httpx.AsyncClient,
    auth_headers: dict[str, str],
) -> None:
    body = {
        "documentId": "doc-flags",
        "fileReference": "/data/docs/flagged.pdf",
        "incompleteSteps": ["text_extraction"],
        "previousOutputs": None,
    }
    r = await client.post("/process", json=body, headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    flags = data["flags"]
    assert isinstance(flags, list)


# ---------------------------------------------------------------------------
# Process route — with DocumentFlag in response from fake
# ---------------------------------------------------------------------------


@pytest.mark.ci_integration
async def test_process_response_with_flags_maps_to_schema() -> None:
    """Verify _map_processing_response correctly maps flags to DocumentFlagSchema."""
    from app import _map_processing_response

    response = ProcessingResponse(
        document_id="doc-with-flag",
        step_results={
            "text_extraction": StepResult(status="completed", error_message=None)
        },
        flags=[DocumentFlag(type="extraction_failure", reason="No pages")],
        metadata=None,
        chunks=None,
        entities=None,
        relationships=None,
    )
    result = _map_processing_response(response)
    assert result.documentId == "doc-with-flag"
    assert len(result.flags) == 1
    assert result.flags[0].type == "extraction_failure"
    assert result.flags[0].reason == "No pages"
