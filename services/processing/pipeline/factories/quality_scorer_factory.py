"""TextQualityScorer factory — selects implementation from config (ADR-011)."""

import structlog

from pipeline.interfaces.text_quality_scorer import TextQualityScorer
from pipeline.steps.text_quality_scoring import WeightedTextQualityScorer
from shared.config import OCRConfig


def create_quality_scorer(
    config: OCRConfig, log: structlog.BoundLogger
) -> TextQualityScorer:
    """Return the Phase 1 weighted quality scorer.

    A second implementation would be selected here via config in a future phase.
    The ``log`` parameter is accepted for interface consistency with other factories
    even though the current implementation does not use it directly.
    """
    _ = log  # reserved for future use
    return WeightedTextQualityScorer(config=config)
