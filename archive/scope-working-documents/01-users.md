# User Types

This document defines who uses the Estate Intelligence system, what they need from it, and when they are introduced. These definitions inform user stories and acceptance criteria — they are not technical roles.

---

## Phase 1 Users

### Primary Archivist

**Who**: The estate owner responsible for building and maintaining the archive. The only user in Phase 1.

**What they need to do**:

- Submit documents to the archive (upload, scan, or batch import)
- Review and correct document metadata after processing
- Add context to documents the system cannot interpret automatically (handwritten notes, low-quality scans, maps with no text)
- Curate the domain vocabulary (names of fields, people, infrastructure) that the system uses to organise knowledge
- Query the archive with natural language questions
- Browse and filter documents directly (not only by querying)
- Mark documents as reviewed, verified, or needing attention
- Delete or supersede documents (e.g. replace a poor scan with a better one)
- Manage system administration: configuration, monitoring, processing errors, backups

**What they must NOT be able to do accidentally**:

- Delete documents without confirmation
- Corrupt or overwrite the original file once ingested

---

## Phase 2 Users

### Family Member

**Who**: A family member with full understanding of the estate context who wants to use the archive actively. Non-technical. Introduced in Phase 2 to provide feedback while the dataset is still being built.

**What they need to do**:

- Query the archive with natural language questions
- Browse and filter documents by date, type, or topic
- View original documents alongside extracted text and answers
- Review and verify documents (mark as reviewed, flag issues)
- Add context to documents (notes, supplementary information)
- Curate the domain vocabulary
- Submit documents to the archive

**What they must NOT be able to do**:

- Delete or supersede documents
- Access system administration (configuration, infrastructure, processing errors)
- Manage other users

---

## Phase 3+ Users

### System Administrator

**Who**: The person responsible for the infrastructure — storage, database, processing services, backups, user management. In Phase 1 and 2 this responsibility sits with the Primary Archivist. Separated out in Phase 3 when the system moves to hosted infrastructure and has real multi-user access.

**What they need to do**:

- Start, stop, and monitor the system
- Manage configuration (storage backend, providers)
- Review processing errors and resubmit failed documents
- Manage user accounts and access
- Perform backups and manage storage

**What they must NOT be able to do** (as a distinct concern from the Archivist role):

- Access document content — administration tasks should be possible without reading private family documents

---

### Occasional Contributor

**Who**: A professional with a legitimate need to interact with the archive on an infrequent basis — for example, a solicitor, accountant, or estate manager. Introduced in Phase 3 or later.

**What they need to do**:

- Submit documents to the archive
- Query the archive for information relevant to their work

**What they must NOT be able to do**:

- Modify or delete any document, including their own submissions once sent
- Access curation, domain vocabulary, or verification tools
- Access system administration

**Open question (Phase 3)**: Whether query access is scoped (only documents they submitted, or documents explicitly shared with them) or full-archive. This will be decided when multi-user access is properly designed.

---

## Out of Scope for All Phases (Explicit Exclusions)

- No public access — the archive is private
- No self-registration — user accounts are managed by the Primary Archivist
- No collaborative annotation or commenting between users
- No export of the full archive by any user
- No anonymous access
