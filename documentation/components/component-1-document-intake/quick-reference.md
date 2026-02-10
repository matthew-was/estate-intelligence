# Component 1: Document Intake — Quick Reference

## Summary

Component 1 is a three-step document upload pipeline that accepts PDF, JPG, and PNG files from the browser, validates and stores them on the local filesystem, and records structured metadata in PostgreSQL — forming the reliable ingestion foundation for downstream text extraction and processing.

---

## Three-Step Upload Flow

### Step 1: Initiate Upload
**Frontend → Next.js API → Backend tRPC**

- **Input**: `{ filename, fileSize, contentType }`
- Next.js validates size (≤ 50MB), allowed types (PDF/JPG/PNG), sanitises filename
- Backend creates DB record with `status='uploading'`, generates UUID
- **Output**: `{ documentId }`
- **DB state**: Record exists, no file stored yet

### Step 2: Upload File
**Frontend → Next.js API (temp storage) → Backend REST**

- **Input**: Multipart form-data with file binary + `documentId`
- Next.js writes to `/tmp/documentId-filename`, cleans up temp files older than 10 minutes
- Next.js forwards to backend `POST /upload/:documentId`
- Backend (Multer memory storage) writes to `/storage/uploads/YYYY/MM/uuid.ext`
- Backend updates DB: `storage_location`, `storage_provider='local'`
- Next.js deletes temp file after successful backend upload
- **Output**: HTTP 200 confirmation
- **DB state**: Record has file reference, file exists in storage

### Step 3: Finalize Upload
**Frontend → Next.js API → Backend tRPC**

- **Input**: `{ documentId, md5Hash, metadata?: { documentDate?, documentType?, notes? } }`
- Client calculates MD5 hash (2 MB chunks, spark-md5); Next.js strips HTML from notes
- Backend checks `md5_hash` unique constraint
  - **Duplicate**: Delete uploaded file, mark record `status='failed'`, return `{ status: 'duplicate', existingDocumentId }`
  - **Unique**: Update record with hash + metadata, set `status='uploaded'`
- **Output**: `{ status: 'uploaded' }` or `{ status: 'duplicate', existingDocumentId }`
- **DB state**: Record complete with hash and metadata, or marked failed

---

## Database Schema at a Glance

| Field | Type | Purpose | Set at Step |
|---|---|---|---|
| `id` | UUID, PK | Document identifier | Step 1 |
| `original_filename` | VARCHAR 500 | Sanitised original name | Step 1 |
| `file_size_bytes` | BIGINT | File size in bytes | Step 1 |
| `content_type` | VARCHAR 100 | MIME type | Step 1 |
| `uploaded_at` | TIMESTAMP (default NOW()) | Upload timestamp | Step 1 |
| `status` | VARCHAR 20, NOT NULL | `'uploading'` / `'uploaded'` / `'failed'` | Step 1, updated at Step 3 |
| `error_message` | TEXT, nullable | Failure reason | Step 3 (on failure) |
| `storage_location` | VARCHAR 500, nullable | URI e.g. `local:/uploads/2024/01/abc.pdf` | Step 2 |
| `storage_provider` | VARCHAR 20, nullable | `'local'` or `'s3'` | Step 2 |
| `md5_hash` | VARCHAR 32, nullable, UNIQUE | Duplicate detection | Step 3 |
| `document_date` | DATE, nullable | Original document date | Step 3 |
| `document_type` | VARCHAR 50, nullable | `deed` / `letter` / `survey` / `email` / `other` / `unknown` | Step 3 |
| `notes` | TEXT, nullable | Free-text notes (HTML-stripped) | Step 3 |

**Indexes**: `status`, `uploaded_at`, `document_date`, `md5_hash` (unique)

---

## StorageService Interface

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

---

## API Endpoints

| Method | Path | Purpose | Auth Required |
|---|---|---|---|
| tRPC mutation | `initiateUpload` | Step 1 — create DB record, return documentId | Yes (API key) |
| POST | `/upload/:documentId` | Step 2 — receive file binary, write to storage | Yes (API key) |
| tRPC mutation | `finalizeUpload` | Step 3 — set MD5 hash, metadata, detect duplicates | Yes (API key) |
| POST | `/cleanup` | Piggyback cleanup — expire orphaned uploading records | Yes (API key) |

---

## File Validation Rules

- **Size limit**: 50 MB maximum (configurable via `upload.maxFileSize`)
- **Type allowlist**: `application/pdf`, `image/jpeg`, `image/png` — checked by MIME type against configured allowlist
- **Filename sanitisation**: Path traversal characters (`../`) and special characters removed; length limit enforced; applied in Next.js validation layer before reaching backend
- **MD5 uniqueness**: Client computes MD5 hash (spark-md5, 2 MB chunks) after upload; backend enforces uniqueness via PostgreSQL `UNIQUE` constraint on `md5_hash`; duplicate files are rejected with `409 Conflict` and the existing document ID is returned

---

## Configuration Sections

| Section | Key Settings |
|---|---|
| `server` | `port: 4000`, `host: '0.0.0.0'` (backend); `port: 3000` (frontend) |
| `database` | PostgreSQL connection string, pool settings, migration auto-run on startup |
| `storage` | Discriminated union on `provider`: `'local'` → `{ basePath }` / `'s3'` → `{ bucket, region, accessKeyId?, secretAccessKey? }` |
| `upload` | `maxFileSize: 52428800` (50 MB), `allowedTypes: ['application/pdf', 'image/jpeg', 'image/png']` |
| `logging` | `level: 'info' \| 'debug' \| 'warn' \| 'error'` |
| `apiKeys` | Array of valid API key strings (backend); single `backendApiKey` string (frontend) |
| `backend` | `{ apiUrl: 'http://backend:4000' }` (frontend only) |

Configuration is loaded via nconf in priority order: CLI args → environment variables (`__` separator) → Docker-mounted runtime JSON → local runtime JSON → committed default JSON. Invalid config causes immediate process exit.

---

## Error Response Format

```json
{
  "error": "Human-readable error message",
  "code": "OPTIONAL_ERROR_CODE",
  "details": {}
}
```

Standard HTTP status codes:

- `400` — Validation errors (bad input, unsupported file type, oversized file)
- `401` — Invalid or missing API key
- `409` — Conflict (duplicate file detected via MD5)
- `500` — Internal server error (storage failure, database error)
- `503` — Backend unreachable (reported by Next.js layer)
- `504` — Backend timeout (reported by Next.js layer)

The `requestId` (UUID v4, generated per request in Next.js) may be appended to error responses for client-side debugging. HTTP status codes are preserved end-to-end from backend through Next.js to browser.

---

## Docker Services

| Service | Port | Exposure |
|---|---|---|
| `frontend` (Next.js) | 3000 | Exposed to host |
| `backend` (Express) | 4000 | Internal only — not exposed to host |
| `db` (PostgreSQL 16-alpine) | 5432 | Internal only (may expose during development for debugging) |

**Networks**: `frontend-network` (frontend ↔ backend), `backend-network` (backend ↔ database). Database is not reachable directly from frontend.

**Volumes**: `postgres_data` (named volume, persists DB across restarts), `./storage` (host mount for uploaded files).

---

## Exit Criteria

Phase 1 is complete when:

- [ ] Upload flow works reliably end-to-end (all three steps)
- [ ] Tests pass with comprehensive critical coverage
- [ ] Real family documents successfully uploaded and retrievable
- [ ] Database queries work; data integrity maintained
- [ ] Code is clean with proper TypeScript types
- [ ] Linting passes; formatting is consistent
- [ ] Documentation exists (setup, architecture, API, config)
- [ ] Dev environment can be torn down and rebuilt cleanly
- [ ] Codebase is a solid foundation for Phase 2

No hard requirements on document counts or coverage percentages — quality and learning are the measures of success.

---

## Key Development Commands

**Setup**:

```bash
./setup.sh          # Create runtime config files from .example templates
pnpm install        # Install all workspace dependencies
docker-compose up -d  # Start all services; migrations run automatically
```

**Root-level**:

```bash
pnpm run dev        # Start all services in parallel (hot reload)
pnpm run validate   # Type-check + lint + format-check (runs before push)
pnpm run format     # Auto-fix formatting with Prettier
pnpm run db:migrate # Run pending Knex migrations
pnpm run db:rollback  # Rollback last migration batch
```

**Backend** (`packages/backend`):

```bash
pnpm run dev        # Nodemon + ts-node hot reload
pnpm run build      # Compile TypeScript → dist/
pnpm run start      # Run compiled production build
pnpm run test       # Run Vitest test suite
```

**Frontend** (`packages/frontend`):

```bash
pnpm run dev        # Next.js dev server with hot reload
pnpm run build      # Production build
pnpm run start      # Run production build
```
