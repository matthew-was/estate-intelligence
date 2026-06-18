"""Fake PipelineOrchestrator for Tier 2 tests (Task 20)."""

from pipeline.interfaces.metadata_extractor import MetadataResult
from pipeline.interfaces.pipeline_models import DocumentFlag
from pipeline.orchestrator import ProcessingRequest, ProcessingResponse, StepResult


class FakePipeline:
    """Fake PipelineOrchestrator that returns a minimal ProcessingResponse."""

    def __init__(self, flags: list[DocumentFlag] | None = None) -> None:
        self._flags = flags or []

    async def process(self, request: ProcessingRequest) -> ProcessingResponse:
        return ProcessingResponse(
            document_id=request.document_id,
            step_results={
                "text_extraction": StepResult(status="completed", error_message=None)
            },
            flags=self._flags,
            metadata=MetadataResult(
                document_type=None,
                dates=[],
                people=[],
                organisations=[],
                land_references=[],
                description=None,
                detection_confidence={},
            ),
            chunks=None,
            entities=None,
            relationships=None,
        )
