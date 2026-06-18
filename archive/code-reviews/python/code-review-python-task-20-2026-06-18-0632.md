# Code Review — Python Service — Task 20: FastAPI route wiring and dependency injection (`app.py`)

**Date**: 2026-06-18 06:32
**Task status at review**: in_review
**Files reviewed**:

- `services/processing/shared/schemas.py` (new)
- `services/processing/app.py` (rewritten)
- `services/processing/tests/test_app.py` (rewritten)
- `services/processing/shared/adapters/ollama_llm.py` (minor update)
- `services/processing/shared/factories/llm_factory.py` (new `create_llm_service_for_query`)

---

## Acceptance condition

**Condition type**: automated

**Condition**: Unit tests in `tests/test_app.py` confirm using fully mocked orchestrator and
query handler: (1) `POST /process` with a valid body and correct auth header returns HTTP 200
with a JSON body matching the `ProcessingResponse` shape; (2) `POST /process` with an invalid
body returns HTTP 400; (3) `POST /query` with a valid body and correct auth header returns
HTTP 200 with `responseText`, `citations`, and `noResults` fields in the response JSON;
(4) `POST /query` with an empty `queryText` returns HTTP 400;
(5) all previously passing auth middleware tests from Task 4 still pass.

**Result**: Met (with one qualification noted under Suggestions)

- AC-1: `test_process_valid_body_and_auth_returns_200` — sends a valid body with correct auth,
  asserts HTTP 200, asserts `documentId`, `stepResults`, and `flags` are present and
  correctly typed. Falsifiable: removing the route handler returns 404; removing auth
  overrides causes 401.
- AC-2: `test_process_invalid_body_returns_400` — sends `{"notAField": "value"}` missing all
  required fields; the `RequestValidationError` exception handler converts FastAPI's 422 to
  400; asserts HTTP 400. Falsifiable: removing the custom exception handler returns 422.
- AC-3: `test_query_valid_body_and_auth_returns_200_with_correct_fields` — sends
  `{"queryText": "..."}` with correct auth; asserts HTTP 200 and asserts `responseText` (str),
  `citations` (list), and `noResults` (bool) are all present. Falsifiable: stubbing the route
  to return wrong keys fails the `in data` assertions.
- AC-4: `test_query_empty_query_text_returns_400` and
  `test_query_whitespace_only_query_text_returns_400` — both assert HTTP 400. Falsifiable:
  removing the `.strip() == ""` guard in the route returns 200.
- AC-5: The four auth middleware tests from Task 4 (`test_health_route_no_auth`,
  `test_api_process_fail_with_wrong_auth`, `test_api_process_fail_with_no_auth`,
  `test_api_query_fail_with_no_auth`) are all present and pass. The original Task 4 test
  `test_api_success_with_auth` (which asserted 501 for a valid-key request) is absent —
  this is expected because the route now returns 200. A replacement test
  `test_process_with_valid_auth_reaches_handler` covers the same auth concern (valid key
  → handler reached → 200). The intent of AC-5 is met; see Suggestions below.

---

## Findings

### Blocking

None.

---

### Suggestions

**S-001** — `tests/test_app.py` lines 27–75: `_FakePipeline` and `_FakeQueryHandler`
defined inline

The fakes placement rule (development-principles-python.md) states: "Test helper fakes for
service ABCs defined inline in a test file — put them in `tests/fakes/<service_name>.py`."
The strict text of the rule mentions "service ABCs." `PipelineOrchestrator` and `QueryHandler`
are concrete orchestrator classes without ABCs, so the rule does not apply literally.

However, the spirit of the rule is reuse across test files. If Task 21 or future integration
tests need to stub the orchestrator or query handler at the app level, these fakes would need
to be duplicated or moved at that point. Consider moving them to `tests/fakes/pipeline.py`
and `tests/fakes/query_handler.py` now to be consistent with the project's established
pattern. Not blocking — the fakes are only used in one file and `PipelineOrchestrator` has
no ABC.

**S-002** — `app.py` lines 22–23: concrete step classes imported at the composition root

`app.py` imports `WeightedTextQualityScorer` and `WeightedFieldPresenceScorer` directly from
`pipeline/steps/`, which are concrete implementations. The dependency composition pattern
(development-principles-python.md) shows `create_quality_scorer` and `create_completeness_scorer`
factory functions as the preferred abstraction boundary. In Phase 1 there is only one
implementation, so this is not a functional problem. If a Phase 2 scorer is added, `app.py`
would need to be updated alongside the factory. Consider wrapping these in thin factory
functions (e.g. `create_quality_scorer(config: OCRConfig, log: Logger) -> TextQualityScorer`)
in `pipeline/factories/` so `app.py` only calls factories and never imports from
`pipeline/steps/` directly.

**S-003** — `tests/test_app.py` lines 281–289: `test_query_response_citation_has_correct_fields`
uses field-presence assertions only

The citation test asserts that `chunkId`, `documentId`, `documentDescription`, and
`documentDate` keys are present in the citation dict but does not assert their values. This
is weaker than the AC-3 test already present (which asserts types). The `_FakeQueryHandler`
returns a deterministic `CitationResult` with known values. Consider strengthening to
`assert citation["chunkId"] == "chunk-1"` etc. (per CR-015). Not blocking — AC-3 is
independently falsifiable and the test is not vacuous (it would fail if the key names were
misspelled in the schema), but a value assertion would be more robust.

**S-004** — `tests/test_app.py`: the original Task 4 `test_api_success_with_auth` test is absent

Task 20 AC-5 says "all previously passing auth middleware tests from Task 4 still pass." The
original test asserted HTTP 501 (the stub response), which can no longer pass because the
route now returns 200. The replacement `test_process_with_valid_auth_reaches_handler` covers
the same concern (valid auth → handler reached) with 200. The intent of AC-5 is met. Consider
adding a comment in the test file noting that this test supersedes `test_api_success_with_auth`
to make the substitution explicit for future readers.

---

## Summary

**Outcome**: Pass

No blocking findings. The implementation correctly wires both C2 and C3 pipeline routes,
implements camelCase serialisation via Pydantic models with camelCase field names, handles
auth middleware (Task 4 tests all pass), converts FastAPI's 422 to 400 for contract
compliance, and tears down async resources on shutdown. All five acceptance conditions are
met by falsifiable tests. The composition root pattern in `app.py` is clean — all services
are instantiated once in the lifespan context and injected via `Depends()`. The
`shared/schemas.py` separation of Python-side OpenAPI schemas from generated Express models
is correct and maintainable.

Four suggestions are noted but none are blocking. Task status set to `review_passed`.

The review is ready for the user to check.

---

## Post-review actions

**2026-06-18** — All four suggestions applied by implementer:

- **S-001**: `_FakePipeline` and `_FakeQueryHandler` moved to `tests/fakes/pipeline.py`
  and `tests/fakes/query_handler.py` respectively. `test_app.py` updated to import
  `FakePipeline` and `FakeQueryHandler` from those modules.
- **S-002**: `create_quality_scorer()` added to
  `pipeline/factories/quality_scorer_factory.py`; `create_completeness_scorer()` added to
  `pipeline/factories/completeness_scorer_factory.py`. `app.py` updated to call these
  factories instead of importing `WeightedTextQualityScorer` and
  `WeightedFieldPresenceScorer` directly from `pipeline/steps/`.
- **S-003**: `test_query_response_citation_has_correct_fields` strengthened to assert
  exact field values (`chunk-1`, `doc-1`, `Test document`, `1967-03-15`) against the
  deterministic `FakeQueryHandler` return values.
- **S-004**: Explanatory comment added to `test_process_with_valid_auth_reaches_handler`
  noting that it supersedes the Task 4 `test_api_success_with_auth` test (which asserted
  501 for stub routes; 501 can no longer pass now that the route returns 200).

All checks passed after applying suggestions: `ruff check`, `ruff format --check`, `mypy`,
and `pytest -m "not integration" tests/` (107 tests, 0 failures).
