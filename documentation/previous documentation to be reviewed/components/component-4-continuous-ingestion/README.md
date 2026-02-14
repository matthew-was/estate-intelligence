# Component 4: Continuous Ingestion

**Status**: Design pending. This is the last component in the pipeline. Complete all other components before designing this one. Use this document as the starting brief for the Component 4 design conversation.

---

## Responsibility

Component 4 monitors for new documents and automatically triggers the full processing pipeline (Components 1–3) without manual intervention. It handles the operational side of keeping the archive up to date as new documents arrive.

**What it owns**:

- New document detection (watch folder and/or API endpoint)
- Processing queue management
- Pipeline trigger (Component 1 intake → Component 2 processing → Component 3 embedding)
- Change tracking in the database
- Failure handling and retry strategy for batch jobs

---

## Known Requirements

### Phase 1 (Manual Pipeline)

Phase 1 has no automated ingestion — documents are uploaded manually through the Component 1 web interface. Component 4 is a Phase 2+ concern.

### Phase 2: Basic Automation

- Watch folder on local filesystem: new files dropped into a folder trigger the pipeline
- Processing queue: queued documents processed in order, one at a time (Phase 2 simplicity)
- Basic failure handling: log failures, don't block queue on single document failure
- Change tracking: record what was processed and when in PostgreSQL

### Phase 3: Robust Ingestion

- API endpoint for programmatic document submission
- Concurrent processing (configurable workers)
- Retry logic with backoff for transient failures
- Processing status visibility (which documents are queued/processing/done/failed)
- Email import integration (for Phase 3 email parsing capability)

---

## Open Design Questions

These must be answered before Component 4 design begins:

1. **Watch folder vs API endpoint vs both**: What is the primary ingestion mechanism? (Watch folder is simplest for Phase 2; API endpoint enables programmatic use)
2. **Queue technology**: In-process queue (simplest), Redis, AWS SQS? Depends on deployment target and reliability requirements
3. **Concurrency model**: Process one document at a time, or parallel processing? OCR is CPU-intensive; parallel processing may strain the development machine
4. **Change tracking schema**: What fields are needed? (document ID, queue time, processing start, processing end, status, error message)
5. **Failure/retry strategy for batch jobs**: How many retries? What failures are retryable (transient network errors) vs permanent (corrupted file)?
6. **Integration with Component 1**: Does Component 4 call Component 1's API directly, or write directly to storage and database?

---

## Known Configuration Points

- Watch folder path (local filesystem)
- Processing queue size (max concurrent documents)
- Retry count and backoff strategy
- Supported file types (subset of what Component 1 accepts)
- API endpoint enable/disable

---

## When Ready to Design

1. Ensure Components 1, 2, and 3 are complete and stable
2. Review [project/architecture.md](../../project/architecture.md) for full system context
3. Review [components/component-1-document-intake/specification.md](../component-1-document-intake/specification.md) — Component 4 will trigger Component 1's intake flow
4. Answer the open design questions above
5. Decide on queue technology (aligns with ADR-001 infrastructure-as-configuration principle)
6. Start Component 4 design conversation with this README as the brief
