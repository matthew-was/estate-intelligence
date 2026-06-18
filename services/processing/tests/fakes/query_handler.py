"""Fake QueryHandler for Tier 2 tests (Task 20)."""

from query.response_synthesis import CitationResult, SynthesisResult


class FakeQueryHandler:
    """Fake QueryHandler that returns a deterministic SynthesisResult."""

    async def handle(self, query_text: str) -> SynthesisResult:
        return SynthesisResult(
            response_text="Documents found.",
            citations=[
                CitationResult(
                    chunk_id="chunk-1",
                    document_id="doc-1",
                    document_description="Test document",
                    document_date="1967-03-15",
                )
            ],
            no_results=False,
        )
