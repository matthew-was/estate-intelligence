# Component 1: Document Intake — Phase 1 Specification

## Project Overview

**Purpose**: Build a document intake system for preserving family estate documents (1950s-present) while learning AI fundamentals and document processing pipelines.

**Phase 1 Goal**: Create a complete, working end-to-end upload pipeline with the simplest viable implementation. Focus on reliability and foundation over features.

**Developer Profile**: 9 years full-stack experience with TypeScript/Node.js, PostgreSQL, Docker, AWS.

---

## Architecture Principles

### Three-Layer Security Model

- **Layer 1 (Browser)**: Public-facing Next.js application
- **Layer 2 (Next.js API Routes)**: Security gateway - validates, sanitizes, enforces policies
- **Layer 3 (Express Backend)**: Internal only, never exposed to internet - handles business logic

**Critical Rule**: Backend is never internet-accessible. All external requests flow through Next.js validation layer.

### Monorepo Structure

```
estate-archive/
├── packages/
│   ├── shared/          # @estate-archive/shared - Types & validation
│   ├── frontend/        # @estate-archive/frontend - Next.js App Router
│   └── backend/         # @estate-archive/backend - Express + tRPC
├── config/              # Runtime configs (gitignored, Docker-mounted)
├── storage/             # Local file storage (gitignored)
├── docs/                # Documentation
└── docker-compose.yml
```

**Package Management**: pnpm workspaces with explicit package listing, unified versioning (all packages share version), workspace protocol for local dependencies.

---

## Technology Stack

### Frontend

- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript (strict mode)
- **API Communication**: tRPC client
- **File Handling**: Temporary disk storage in `/tmp/`, spark-md5 for browser-side hashing

### Backend

- **Framework**: Express 5
- **Language**: TypeScript (strict mode)
- **API Layer**: tRPC for procedures + REST endpoints for file uploads (Multer)
- **Database**: Knex.js with PostgreSQL 16
- **Storage**: Abstracted interface (local filesystem → S3 migration path)

### Shared

- **Validation**: Zod schemas
- **Configuration**: nconf + Zod validation
- **Logging**: Pino (structured JSON logs)
- **Testing**: Vitest (all packages)

### Infrastructure

- **Containers**: Docker Compose
- **Node.js**: v22 LTS (enforced via engines + .nvmrc)
- **Database**: PostgreSQL 16 + pgvector extension (for future phases)

---

## Document Upload Flow (Three Steps)

### Step 1: Initiate Upload (Metadata Only)
**Frontend → Next.js API → Backend tRPC**

- Client sends: `{ filename, fileSize, contentType }`
- Next.js validates: file size ≤ 50MB, allowed types (PDF/JPG/PNG), sanitizes filename
- Backend creates database record with `status='uploading'`, generates UUID
- Returns: `documentId`

**Database State**: Record exists, no file stored yet

### Step 2: Upload File (Binary Transfer)
**Frontend → Next.js API (temp storage) → Backend REST**

- Client sends file as multipart/form-data with `documentId`
- Next.js writes to `/tmp/documentId-filename` (avoid memory pressure)
- Next.js cleans up old temp files (>10 minutes) before processing
- Next.js forwards to backend `POST /upload/:documentId`
- Backend (Multer memory storage) writes to local storage: `/storage/uploads/YYYY/MM/uuid.ext`
- Backend updates database: `storage_location`, `storage_provider='local'`
- Next.js deletes temp file after successful backend upload

**Database State**: Record has file reference, file exists in storage

### Step 3: Finalize Upload (Hash & Metadata)
**Frontend → Next.js API → Backend tRPC**

- Client calculates MD5 hash (2MB chunks, spark-md5)
- Client sends: `{ documentId, md5Hash, metadata?: { documentDate?, documentType?, notes? } }`
- Next.js validates and sanitizes (strip HTML from notes)
- Backend checks for duplicates via `md5_hash` unique constraint
  - **If duplicate**: Delete uploaded file, mark record `status='failed'`, return `{ status: 'duplicate', existingDocumentId }`
  - **If unique**: Update record with hash + metadata, set `status='uploaded'`

**Database State**: Record complete with hash and metadata, or marked as failed duplicate

### Error Handling Philosophy
**Aggressive Immediate Cleanup**: Any failure at any step triggers deletion of uploaded file (if exists), marking/deletion of database record, and cleanup of temp files. No orphaned state accumulates.

**Acceptable for Phase 1**: Single user, small files, fast network. Phase 2 will improve handling for slower uploads and larger files.

---

## Database Schema

### `intake_documents` Table

**Step 1 Fields**:

- `id` (UUID, PK)
- `original_filename` (VARCHAR 500)
- `file_size_bytes` (BIGINT)
- `content_type` (VARCHAR 100)
- `uploaded_at` (TIMESTAMP, default NOW())

**Step 2 Fields**:

- `storage_location` (VARCHAR 500, nullable) - e.g., `"local:/uploads/2024/01/abc-123.pdf"`
- `storage_provider` (VARCHAR 20, nullable) - `"local"` or `"s3"`

**Step 3 Fields**:

- `md5_hash` (VARCHAR 32, nullable, UNIQUE) - duplicate detection
- `document_date` (DATE, nullable) - original document date
- `document_type` (VARCHAR 50, nullable) - `'deed'`, `'letter'`, `'survey'`, `'email'`, `'other'`, `'unknown'`
- `notes` (TEXT, nullable)

**Status Tracking**:

- `status` (VARCHAR 20, NOT NULL, default `'uploading'`) - `'uploading'`, `'uploaded'`, `'failed'`
- `error_message` (TEXT, nullable)

**Indexes**: `status`, `uploaded_at`, `document_date`, `md5_hash` (unique)

### Migration Strategy

- Knex.js migrations in `packages/backend/src/db/migrations/`
- Auto-run on backend startup (`await db.migrate.latest()`)
- Fail-fast: exit if migrations fail
- Separate test database (`estate_archive_test`)

---

## Configuration System

### Hierarchy (Highest → Lowest Priority)

1. Command-line arguments
2. Environment variables (use `__` separator: `DATABASE__CONNECTION__HOST`)
3. Docker-mounted runtime configs (`/config/*.runtime.json`)
4. Local runtime configs (`packages/*/config.runtime.json`, gitignored)
5. Package default configs (`packages/*/config.json`, committed)

### Technology

- **nconf**: Hierarchical loading
- **Zod**: Runtime validation + type inference
- **Fail-fast**: Invalid config → immediate exit

### Backend Configuration Sections

- **server**: `{ port: 4000, host: '0.0.0.0' }`
- **database**: PostgreSQL connection, pool settings, migrations
- **storage**: Discriminated union on `provider` field
  - `provider: 'local'` → `{ local: { basePath } }`
  - `provider: 's3'` → `{ s3: { bucket, region, accessKeyId?, secretAccessKey? } }`
- **upload**: `{ maxFileSize: 52428800, allowedTypes: ['application/pdf', 'image/jpeg', 'image/png'] }`
- **logging**: `{ level: 'info' | 'debug' | 'warn' | 'error' }`
- **apiKeys**: Array of valid API key strings

### Frontend Configuration

- **backend**: `{ apiUrl: 'http://backend:4000' }`
- **server**: `{ port: 3000 }`
- **backendApiKey**: Single API key for authenticating with backend

---

## Storage Architecture

### Phase 1: Local Filesystem
**Directory Structure**: `/storage/uploads/YYYY/MM/uuid.ext`

- `YYYY`: Four-digit year
- `MM`: Two-digit month (zero-padded)
- `uuid`: Document ID (UUID v4)
- `ext`: Original file extension

**Database Reference**: URI format `"local:/uploads/2024/01/abc-123.pdf"`

### Storage Service Interface

```typescript
interface StorageService {
  store(buffer: Buffer, metadata: object): Promise<StorageReference>
  retrieve(ref: StorageReference): Promise<Buffer>
  delete(ref: StorageReference): Promise<void>
  exists(ref: StorageReference): Promise<boolean>
}

type StorageReference = {
  location: string  // URI: 'local:/...' or 's3://...'
  provider: 'local' | 's3'
}
```

### Future S3 Migration
**No code changes required** - only:

1. Implement `S3StorageService` class (same interface)
2. Migrate data: Export files → Upload to S3 → Update database URIs
3. Update configuration: `storage.provider = 's3'`

---

## Security & API Design

### API Key Authentication

- Backend validates all requests using API keys
- Support multiple clients (frontend, MCP server, future services)
- Each client has unique key → individual revocation possible
- Keys identify clients in logs

### Request Flow Security

**Next.js Validation Layer**:

- File size ≤ 50MB
- File type: PDF/JPG/PNG only
- Zod schema validation
- Filename sanitization (remove `../`, special chars)
- Notes sanitization (strip HTML tags)

**Backend Trust Model**:

- Validates API key on all endpoints
- Trusts Next.js has validated inputs (internal network)
- Performs business logic
- Returns standardized errors

### File Validation

- **Size**: 50MB max (configurable)
- **Type**: MIME type check against allowlist
- **Duplicates**: MD5 hash vs database unique constraint
- **Filename**: Path traversal prevention, special char handling, length limit

### Error Response Format
Standard HTTP status + JSON body:

- `400`: Validation errors
- `409`: Conflicts (duplicate files)
- `500`: Server errors

Example: `{ error: 'File already exists', existingDocumentId: 'uuid' }`

### Security Notes

- **CORS**: Not needed (backend is internal)
- **HTTPS**: Phase 2+ (Let's Encrypt or AWS ACM)
- **Security Headers**: Phase 2+

---

## Testing Strategy

### Framework & Structure

- **Vitest** (all packages)
- **Backend tests**: Separate `__tests__/` directory mirroring `src/`
- **Frontend tests**: Colocated with source files

### Test Scope (Phase 1)
**Integration tests within package boundaries only**. No E2E across frontend/backend.

**Backend Coverage**:

- Configuration parsing (nconf + Zod, including invalid configs)
- Database operations (CRUD, migrations)
- Storage service methods (save/retrieve/delete)
- tRPC procedures (initiate, finalize)
- API key validation middleware

**Frontend Coverage**:

- API client functions (mocked responses)
- Form validation and state management
- Next.js API route handlers (mocked backend)
- Configuration loading

**Explicitly Not Included**:

- Browser-based E2E tests (Playwright/Cypress)
- Tests crossing frontend/backend boundary
- Performance/load tests
- UI snapshot testing

### Test Database

- Separate database: `estate_archive_test`
- Real PostgreSQL in Docker (not in-memory)
- Cleanup: Truncate tables + reset sequences after each test

### Test Fixtures
Small test files in `__tests__/fixtures/`:

- Sample PDFs (~50KB)
- Sample JPG/PNG (~40-60KB)
- Invalid file types (for error testing)
- Total: ~200KB (acceptable for git)

### Coverage Philosophy
**No percentage targets**. Focus on:

- Critical paths where bugs cause most damage
- Integration points between components
- Comprehensive but pragmatic coverage
- Quality over metrics

---

## Logging & Observability

### Logging Library: Pino

- Structured JSON logs
- Levels: `debug`, `info`, `warn`, `error`
- Output: stdout only (Docker captures automatically)
- Production: Add CloudWatch or similar

### Request Tracking

- Unique request ID (UUID v4) generated in Next.js
- Passed to backend via HTTP header
- Included in all logs via Pino child loggers: `logger.child({ requestId })`

### What to Log

- **Error logs**: Stack traces, context (documentId, requestId), structured fields
- **Never log**: API keys, passwords, document content
- **Optional**: Operation durations for performance analysis

### Standard Log Fields

- `timestamp` (auto-added by Pino)
- `level`
- `requestId`
- `message`
- Additional context as needed

---

## Development Workflow

### Initial Setup

```bash
git clone <repo>
./setup.sh              # Creates config files from .example
pnpm install
docker-compose up -d    # Migrations auto-run
# Access: http://localhost:3000
```

### Commands

**Root Level**:

- `pnpm install` - Install all dependencies
- `pnpm run dev` - Start all services in parallel
- `pnpm run validate` - Type-check + lint + format-check
- `pnpm run db:migrate` - Run migrations
- `pnpm run db:rollback` - Rollback last migration batch

**Backend**:

- `pnpm run dev` - Nodemon + ts-node (hot reload)
- `pnpm run build` - Compile TypeScript → `dist/`
- `pnpm run start` - Run compiled production build
- `pnpm run test` - Run Vitest tests

**Frontend**:

- `pnpm run dev` - Next.js dev server (hot reload)
- `pnpm run build` - Production build
- `pnpm run start` - Run production build

### TypeScript Configuration

- Root base config with shared settings
- Package configs extend base with overrides
- **Strict mode enabled from start**
- Path aliases: `@/` → each package's `src/` directory
- Modern settings: ESNext modules, ES2020+ target

### Linting & Formatting

- Shared ESLint + Prettier config at root
- Recommended rules as baseline (TypeScript, React, Node.js)
- `eslint-config-prettier` to avoid conflicts
- Prettier defaults (can modify during development)

### Validation Script
`pnpm run validate` runs:

1. `tsc --noEmit` (type-check)
2. `eslint .` (lint)
3. `prettier --check .` (format-check)

Complementary: `pnpm run format` auto-fixes formatting

### Git Workflow

- Simple pre-push hook runs `pnpm run validate`
- Plain git hooks (no Husky)
- No pre-commit hooks
- `.gitignore`: `node_modules/`, `storage/`, runtime configs, build outputs, IDE settings

### Docker Development

- **Hot reload**: Volume mounts for source code
- **Backend startup**: Wait for PostgreSQL health → run migrations → start Express
- **Graceful shutdown**: Handle SIGTERM/SIGINT, close DB connections, complete in-flight requests
- **Temp cleanup**: Next.js deletes `/tmp/` files >10 minutes old on each upload

---

## Docker Compose Structure

### Services

**Frontend**:

- Next.js on port 3000 (exposed to host)
- Volume mounts: source code, node_modules, `.next` cache, runtime config
- Depends on: backend

**Backend**:

- Express on port 4000 (internal only, not exposed)
- Volume mounts: source code, node_modules, storage, runtime config
- Depends on: db (service_healthy)

**Database**:

- PostgreSQL 16-alpine
- Healthcheck: `pg_isready` (every 5s, timeout 5s, 5 retries)
- Named volume: `postgres_data` (persists across restarts)
- Port 5432: Internal only (expose during development for debugging if needed)

### Network Isolation

- `frontend-network`: Frontend ↔ Backend
- `backend-network`: Backend ↔ Database
- Database not directly accessible from frontend

### Volumes

- `postgres_data`: Named volume for database persistence
- `./storage`: Host mount for uploaded files (easy backup/inspection)

---

## Deployment Architecture

### Phase 1-3: Development

- Local Docker Compose on developer machine
- Local filesystem storage (`./storage/`)
- PostgreSQL in Docker (named volume)
- Backups: Original documents kept separately (this system is the archive copy)

### Production (Phase 2+)
**Target Platform**: AWS EC2 (primary), ECS (where compatible)

**Database Options**:

- PostgreSQL on EC2 + EBS (snapshots for backup)
- AWS RDS (automated backups/maintenance)

**Storage**: AWS S3 (redundancy, versioning)

**Networking**:

- Frontend: Public subnet
- Backend: Private subnet with security groups
- HTTPS: Let's Encrypt or AWS ACM

**Secrets**: AWS Secrets Manager or Parameter Store

### Migration Paths (No Code Changes Required)

**Local → EC2**: Deploy same Docker Compose, configure EBS, set up security groups

**Local DB → RDS**: `pg_dump` → import to RDS → update backend config

**Local Storage → S3**: Sync files to S3 → update database URIs → update storage config

---

## Phase 1 Scope

### Features Included

- Three-step upload flow (initiate → upload → finalize)
- PDF, JPG, PNG support
- Local filesystem storage (date-based folders)
- MD5 duplicate detection (database unique constraint)
- Basic metadata (document date, type, notes)
- Aggressive error cleanup (no partial state)
- Comprehensive Vitest tests
- Docker Compose development environment

### Features Explicitly NOT Included
Authentication/authorization, multi-user support, document listing/browsing UI, search interface, document preview, **batch upload of multiple files simultaneously** (see Multi-File Upload Strategy below), progress bars, drag-and-drop, resume uploads, advanced retry logic, rate limiting, versioning, audit logs, email notifications, webhooks, GraphQL, mobile app, public API, analytics, sharing/permissions, comments/annotations, workflows, external integrations.

### Multi-File Upload Strategy

**Phase 1 Approach**: The upload flow handles one file at a time through the three-step process. For users needing to upload multiple documents, the frontend can:

- **Sequential upload**: Loop through files calling the same three-step flow for each (simplest, works with zero backend changes)
- **Frontend-only parallelism** (optional Phase 1.5 enhancement): Send multiple files in parallel with concurrency limiting (e.g., 3 at a time) - each file still uses independent three-step flow, no backend changes required

**Why This Works**:

- Phase 1 single-user scenario means upload concurrency is controlled client-side
- Each upload is independent (no atomic batch semantics needed yet)
- Database md5_hash unique constraint prevents duplicates regardless of upload order
- Temp file cleanup handles concurrent uploads (files are request-scoped)

**Phase 2 Considerations**:

- True batch upload endpoints with atomic all-or-nothing semantics
- Progress tracking across multiple files in a batch
- Sophisticated error handling for partial batch failures
- Transaction management for batch metadata

**Design Rationale**: Defer complex batch semantics until actual usage patterns are understood. Sequential upload is acceptable for Phase 1 learning goals (uploading 10-50 documents to test the pipeline). If bulk import becomes painful during development, frontend-only parallelism provides 3x speedup without architectural changes.

### Exit Criteria
Phase 1 complete when:

- Upload flow works reliably end-to-end
- Tests pass with comprehensive critical coverage
- Real family documents successfully uploaded and retrievable
- Database queries work, data integrity maintained
- Code is clean with proper TypeScript types
- Linting passes, formatting consistent
- Documentation exists (setup, architecture, API, config)
- Dev environment can be torn down and rebuilt cleanly
- **You're satisfied it's a solid Phase 2 foundation**

**No hard requirements**: No specific document counts, coverage percentages, or formal checklists. Quality and learning are the measures of success.

---

## Key Design Principles

1. **Start Small and Complete**: Full simple system > partial complex system
2. **Incremental Complexity**: Add features component-by-component in later phases
3. **Real-World Testing**: Actual family documents from day one
4. **Maintainability**: Designed for ongoing addition over years
5. **Learning-Focused**: Understand deeply, not just use black boxes
6. **Migration-Ready**: Abstractions support future changes without rewrites
7. **Type Safety**: End-to-end TypeScript + runtime Zod validation
8. **Test Early**: Tests from Phase 1, not deferred
9. **Aggressive Cleanup**: No partial state accumulation
10. **Document as You Build**: Documentation during development, not after

---

## Implementation Discretion

**Decide during implementation** (not upfront):

- Specific TypeScript compiler options beyond strict mode + path aliases
- Exact ESLint rules beyond recommended
- Prettier settings beyond defaults
- API key header name (Authorization vs X-API-Key vs custom)
- Request ID header name (likely X-Request-ID)
- Database field types (ENUM vs VARCHAR with constraints)
- Timestamp types (TIMESTAMP vs TIMESTAMPTZ)
- Logger instance pattern (global vs per-module)
- Test environment setup
- Edge case handling (zero-byte files, malformed requests)
- File type validation depth (magic bytes vs MIME only)
- Database field naming (snake_case vs camelCase)
- All other implementation details that don't affect architecture

**Philosophy**: Architecture provides guardrails, not step-by-step instructions. Make good judgments within established constraints.

---

## Error Handling Patterns

### Next.js API Routes → Backend Communication

**Timeout Handling**:

- Next.js API routes should set reasonable timeout for backend calls (implementation decision: 30-60 seconds)
- On timeout: Log error, cleanup temp files, return 504 Gateway Timeout to client

**Network Errors**:

- Backend unreachable: Log error, cleanup temp files, return 503 Service Unavailable to client
- No automatic retries in Phase 1 (fail-fast approach)
- Phase 2+ may add retry logic for idempotent operations

**Error Response Translation**:

- Next.js passes through backend error responses with minimal transformation
- Backend returns structured errors: `{ error: string, code?: string, details?: object }`
- Next.js may add `requestId` to error response for client-side debugging
- HTTP status codes preserved from backend to client

**Logging**:

- Next.js logs all backend calls with: requestId, endpoint, duration, status
- Errors logged with full context before returning to client
- No sensitive data (API keys, file contents) in logs

### Backend Error Handling

**Database Errors**:

- Connection failures: Log and return 500 Internal Server Error
- Constraint violations (duplicate md5_hash): Return 409 Conflict with details
- Query timeouts: Log and return 500 (investigate if frequent)

**Storage Errors**:

- Write failures: Log, cleanup database record, return 500
- Delete failures during cleanup: Log but don't fail request (orphaned files acceptable for Phase 1)
- Read failures: Log and return 500

**Validation Errors**:

- Invalid API key: Return 401 Unauthorized immediately
- Invalid input after Next.js validation: Log warning (shouldn't happen), return 400 Bad Request

---

## API Key Management

### Key Format

- Simple random strings (implementation decision: UUID v4 or 32+ character random hex)
- Stored in plain text in backend configuration (acceptable for Phase 1 internal network)
- Future enhancement: Hash keys like passwords for defense-in-depth

### Key Storage

- **Never in committed code**: Keys live in runtime config files only (gitignored)
- **Backend config**: `apiKeys` array contains all valid keys
- **Frontend config**: `backendApiKey` contains single key this instance uses
- **Example**:

  ```json
  // backend.runtime.json
  {
    "apiKeys": ["frontend-key-abc123", "mcp-key-def456"]
  }

  // frontend.runtime.json
  {
    "backendApiKey": "frontend-key-abc123"
  }
  ```

### Client Identification

- Backend logs which API key was used for each request
- Naming convention helps identify clients: `frontend-*`, `mcp-*`, `service-*`
- Keys are functionally identical (no permission differences in Phase 1)
- Future enhancement: Associate permissions/roles with keys

### Key Rotation
**Simple approach for Phase 1**:

1. Add new key to backend `apiKeys` array
2. Update client config to use new key
3. Restart client service
4. Remove old key from backend `apiKeys` array
5. Restart backend (or reload config if hot-reload implemented)

**No downtime required** if backend supports multiple valid keys during transition.

### Header Name
Implementation decision during development (options: `Authorization`, `X-API-Key`, `X-Estate-Archive-Key`). Backend validates presence and matches against configured keys.

---

## Database Cleanup Strategy

### Orphaned Upload Records

**Definition**: Records with `status='uploading'` that exceed age threshold (e.g., 10 minutes).

**Phase 1 Approach - Piggyback Cleanup**:

- Next.js temp file cleanup (runs on each upload) also triggers backend cleanup endpoint
- Backend queries: `SELECT id FROM intake_documents WHERE status='uploading' AND uploaded_at < NOW() - INTERVAL '10 minutes'`
- For each orphaned record: Delete associated file from storage, update status to 'failed' with error_message='Upload timeout'

**Limitations**:

- Cleanup only happens when someone uploads
- If no uploads for days, orphans persist (acceptable for Phase 1 single user)

**Phase 2+ Enhancement**:

- Dedicated cron job or scheduled task for cleanup
- Configurable timeout threshold
- More sophisticated retry/resume logic for legitimate slow uploads

### Temporary File Cleanup

**Next.js `/tmp/` Directory**:

- Before processing new upload: Delete files older than 10 minutes
- Pattern: `documentId-*` files in `/tmp/`
- Cleanup is best-effort (log failures but don't block upload)

**Considerations**:

- 10-minute threshold allows for slow networks while preventing buildup
- Phase 2 may need longer threshold for larger files or slower connections
- Multi-user Phase 2+ will need process-safe cleanup (file locking or temp directory per upload)

---

## Next Phase Preview

**Phase 2: Essential Intelligence** (to be planned separately)

- Text extraction from PDFs
- OCR for scanned documents
- Better handling for slower/larger uploads
- Smarter chunking (semantic boundaries)
- Enhanced metadata extraction (AI-assisted)
- Simple web UI for querying
- **MCP wrapper implementation**

### MCP Integration Approach (Phase 2)

**Architecture**: MCP server is a thin client wrapping the same backend APIs used by the frontend HTTP client.

**Authentication**: Uses the same API key mechanism as frontend. Backend config includes MCP's key in the `apiKeys` array.

**Implementation Pattern**:

- MCP server explicitly registers tools that map to backend API endpoints
- Example: `upload_document` tool calls the same three-step flow (initiate → upload → finalize)
- MCP handles file reading from local filesystem, backend handles storage
- No special MCP-specific backend endpoints needed

**Why Phase 2**:

- Get core upload pipeline solid first
- Understand real usage patterns before adding automation
- MCP integration is straightforward once backend APIs are stable

**Phase 3: Production Features**
**Phase 4: Scale & Polish**

Each phase builds on the reliable foundation of previous phases.
