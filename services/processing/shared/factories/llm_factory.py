"""Factory for creating the LLMService adapter (ADR-038, ADR-042)."""

import structlog

from shared.adapters.ollama_llm import OllamaLLMAdapter
from shared.config import LLMBaseConfig, LLMConfig  # LLMConfig extends LLMBaseConfig
from shared.interfaces.llm_service import LLMService


def create_llm_service(config: LLMConfig, log: structlog.BoundLogger) -> LLMService:
    # NOTE: create_llm_service expects LLMConfig (with chunking constraints) which is
    # correct for the pipeline (C2). For query (C3), use create_llm_service_for_query
    # which accepts LLMBaseConfig (no chunking fields). The two factories are separate
    # so the pipeline and query LLM configs can be independently optimised.
    if config.PROVIDER == "ollama":
        return OllamaLLMAdapter(config=config, log=log)

    raise ValueError(f"{config.PROVIDER} is not a supported LLM Service Provider")


def create_llm_service_for_query(
    config: LLMBaseConfig, log: structlog.BoundLogger
) -> LLMService:
    """Create an LLMService adapter for the C3 query pipeline.

    Accepts ``LLMBaseConfig`` (provider, base URL, model only — no chunking
    fields) because query understanding and synthesis do not chunk documents.
    This is intentionally separate from ``create_llm_service`` so the query
    and pipeline LLM providers can be configured independently.
    """
    if config.PROVIDER == "ollama":
        return OllamaLLMAdapter(config=config, log=log)

    raise ValueError(f"{config.PROVIDER} is not a supported LLM Service Provider")
