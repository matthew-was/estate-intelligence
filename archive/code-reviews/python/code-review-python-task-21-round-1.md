# Code Review — Python Service — Task 21: C2 and C3 pipeline unit test suite completion

**Date**: 2026-06-18 08:56
**Task status at review**: in_review
**Files reviewed**:

- `services/processing/shared/config.py`
- `services/processing/app.py`
- `services/processing/tests/test_app.py`
- `services/processing/tests/shared/test_config.py`

---

## Acceptance condition

**Stated condition**: Running `pytest -m "not integration" services/processing/tests/` reports
all test files present and all tests passing with zero failures, zero errors, and zero warnings.
The output shows at least one test function per test file listed in the task description.

**Condition type**: automated

**Result**: The files under review relate to the config lazy-loading proxy change that unblocks
the test suite from any working directory. The caller reports 107 tests passing with 96%
coverage. This condition is accepted as met for the test execution aspect.

However, the proxy implementation introduces a mypy type regression — see blocking finding
B-001 below. The implementation completion checklist (`development-principles-python.md`)
requires `mypy .` to pass. If mypy fails, the acceptance condition is not fully met because
the checklist is a prerequisite to marking a task `code_written`.

---

## Findings

### Blocking

**B-001 — `_ConfigProxy.__getattr__` return type breaks mypy across the codebase**

File: `services/processing/shared/config.py`, lines 154–157

```python
def __getattr__(self, name: str) -> object:
    if self._singleton is None:
        self._singleton = _load_config()
    return getattr(self._singleton, name)
```

Before this change, `config = _load_config()` returned `AppConfig`, so `config.AUTH` was
correctly typed as `AuthConfig` and `config.AUTH.INBOUND_KEY` as `str`. After this change,
`config = _ConfigProxy()` means `config` is typed as `_ConfigProxy`. When mypy sees
`config.AUTH`, it invokes `__getattr__` and sees the return type as `object`. Any subsequent
attribute access on that result (e.g. `config.AUTH.INBOUND_KEY`, `config.PROCESSING.OCR`)
will fail mypy because `object` has no those attributes.

This affects at minimum:

- `services/processing/app.py` — `config.AUTH`, `config.PROCESSING.*`, `config.QUERY.*`,
  `config.SERVICE` (all call sites introduced in Task 20)
- `services/processing/tests/test_app.py` — `config.AUTH.INBOUND_KEY` in the `valid_key`
  fixture
- `services/processing/tests/shared/test_config.py` — `shared.config.config.AUTH.INBOUND_KEY`
  and `shared.config.config.PROCESSING.OCR.QUALITY_SCORING.CONFIDENCE_WEIGHT`

The implementation completion checklist (`development-principles-python.md`) requires
`mypy .` to pass before a task is marked `code_written`. If it does not pass, this is a
blocking finding.

**What must change**: The `__getattr__` return type must be fixed so mypy understands that
attribute access on the proxy returns the same types as the underlying `AppConfig`. Acceptable
approaches include:

- Returning `Any` (with an inline comment explaining why, per the `Any` prohibition rule):
  `def __getattr__(self, name: str) -> Any: ...`  — this silences mypy for all accesses on
  the proxy but satisfies the prohibition rule if justified
- Using a `TYPE_CHECKING` guard to declare `config: AppConfig` for static analysis while
  the runtime uses the proxy — this gives full type coverage without runtime cost
- Explicitly typing `__getattr__` with an `@overload` per attribute — this is precise but
  verbose for a config object with many fields

The fix is the developer's choice; the requirement is that `mypy .` passes with zero errors.

---

**B-002 — `test_process_response_with_flags_maps_to_schema` takes an unused `valid_key` fixture parameter**

File: `services/processing/tests/test_app.py`, line 289

```python
async def test_process_response_with_flags_maps_to_schema(valid_key: str) -> None:
```

The `valid_key: str` parameter is never used in the test body. The test only calls
`_map_processing_response`, a pure mapping function that requires no auth key. The `valid_key`
fixture was added (presumably) to ensure the config singleton is initialized before the test,
but this is not a correct use of a fixture — the config proxy will initialise itself on first
access regardless, and the fixture does not provide any isolation guarantee.

This is a blocking finding because:

1. The `ANN` ruff ruleset enforces that all function parameters are used; an unused parameter
   may trigger a ruff lint violation depending on how the rule is configured
2. More fundamentally, `valid_key` in a test function signature that never references it
   misleads the reader into thinking auth is relevant to this test, and it may cause `ruff`
   to report `ARG001` (unused function argument) — which would break the `ruff check .`
   completeness-checklist step

**What must change**: Remove the `valid_key: str` parameter from
`test_process_response_with_flags_maps_to_schema`. The test body does not need it.

---

### Suggestions

**S-001 — `_singleton` reset in `test_config_env_var_override` is not cleanup-safe**

File: `services/processing/tests/shared/test_config.py`, lines 17–22

The test manually sets `shared.config.config._singleton = None` at both the start and the
end of the function body. If the assertion at line 21 (`assert shared.config.config.AUTH.INBOUND_KEY == "overridden-key"`) fails, the final `_singleton = None` at line 22 is never reached. At that point `monkeypatch` will still clean up the env var, but `_singleton` will hold the overridden config (loaded with the test env var), not the original. The next test that accesses `config` will get the correct value (because `monkeypatch` removes the env var before test teardown runs and `_singleton` holds the overridden value — which means the first access after teardown will return the wrong value until some test re-triggers a reload).

The safer pattern is to use a `try/finally` block or to call `_singleton = None` in a
`monkeypatch` finalizer. Alternatively, adding a `monkeypatch.setattr` to reset the singleton
in the teardown phase is idiomatic pytest:

```python
def test_config_env_var_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(shared.config.config, "_singleton", None)
    monkeypatch.setenv("IK_AUTH__INBOUND_KEY", "overridden-key")
    assert shared.config.config.AUTH.INBOUND_KEY == "overridden-key"
```

Using `monkeypatch.setattr` to reset `_singleton` means pytest's own teardown restores it
(to the pre-test value) after the test, regardless of pass or fail.

**S-002 — `_ConfigProxy` class-level `_singleton` is shared across all instances**

File: `services/processing/shared/config.py`, line 152

`_singleton: AppConfig | None = None` is a class-level variable. Every instance of
`_ConfigProxy` shares the same `_singleton`. Since there is only one `config = _ConfigProxy()`
in the module, this works correctly in practice. However, if a test or future code creates
a second `_ConfigProxy()`, it would share the same singleton as the module-level `config`.
Making `_singleton` an instance variable is more correct:

```python
def __init__(self) -> None:
    self._singleton: AppConfig | None = None
```

This is a suggestion, not blocking — the current pattern is safe given single-instance usage.

**S-003 — `import os` inside `_load_config` body**

File: `services/processing/shared/config.py`, line 129

`import os` is placed inside the function body (inside the `if settings_files is None` block).
Convention in this codebase (and Python generally) is to place all imports at the top of the
module. `os` is a stdlib module with zero cost to import at module load time.

---

## Summary

**Outcome**: Fail

Two blocking findings:

- **B-001**: `_ConfigProxy.__getattr__` returns `object`, breaking mypy type checking across
  all call sites that access `config.*` attributes. The `mypy .` step in the implementation
  completion checklist will fail. The return type must be corrected before the task can pass.
- **B-002**: `test_process_response_with_flags_maps_to_schema` accepts an unused `valid_key`
  fixture parameter, which is likely to trigger a ruff lint violation and misleads the reader.

Three suggestions (S-001, S-002, S-003) are optional improvements.

The review is ready for the user to check.
