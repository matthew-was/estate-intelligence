"""MetadataCompletenessScorer factory — selects implementation from config (ADR-012)."""

import structlog

from pipeline.interfaces.completeness_scorer import MetadataCompletenessScorer
from pipeline.steps.completeness_scoring import WeightedFieldPresenceScorer
from shared.config import MetadataConfig


def create_completeness_scorer(
    config: MetadataConfig, log: structlog.BoundLogger
) -> MetadataCompletenessScorer:
    """Return the Phase 1 weighted field-presence scorer.

    A second implementation would be selected here via config in a future phase.
    The ``log`` parameter is accepted for interface consistency with other factories
    even though the current implementation does not use it directly.
    """
    _ = log  # reserved for future use
    return WeightedFieldPresenceScorer(config=config)
