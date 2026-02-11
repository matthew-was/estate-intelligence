# Query Scope

This document defines the types of questions the system must be able to answer, and what it explicitly does not need to answer. This drives embedding strategy, metadata requirements, and retrieval design.

---

## What a Query Looks Like

A query is a natural language question asked by an authorised user. The system returns a synthesised answer in plain language, with citations identifying the source documents used to construct it.

The system does not return a list of search results for the user to read through. It reads the relevant documents and answers the question directly, like asking a knowledgeable colleague who has read everything.

---

## Phase 1 Query Types

These are the question types the system must answer in Phase 1, using the initial set of typewritten and printed documents. The retrieval system is capable of all question types from Phase 1 — what changes across phases is the breadth and quality of available documents, not the retrieval capability itself.

### Land and Ownership

Questions about who owns or has owned specific parcels of land, and the history of transactions.

Examples:

- "What is known about ownership of the north field?"
- "Who owned the mill pasture before the family acquired it?"
- "Has the east meadow ever been sold or transferred?"
- "What parcels of land were purchased in the 1970s?"

### Infrastructure and Works

Questions about physical works carried out on the estate — drainage, fencing, buildings, roads, utilities, and rights of way.

Examples:

- "Where were pipes laid through the east meadow, and when?"
- "When was the barn on the home farm built or extended?"
- "What drainage work has been done on the lower fields?"
- "Are there any records of work done to the boundary with the neighbouring farm?"
- "Where does the right of way cross the estate, and when was it established?"

### People and Relationships

Questions about individuals mentioned in the documents — family members, tenants, solicitors, contractors, neighbours.

Examples:

- "Who was involved in the sale of the mill pasture?"
- "Which solicitors acted for the family in land transactions?"
- "Who were the tenants of the home farm and when did their tenancies run?"
- "What is known about the Smith family's connection to the estate?"

### Decisions and Agreements

Questions about decisions made, agreements reached, or intentions recorded — including legal and contractual matters.

Examples:

- "What decisions were made about the purchase or sale of certain plots?"
- "Were there any recorded disputes about the eastern boundary?"
- "What were the terms of the tenancy agreement with the Joneses?"
- "Is there any record of a right of way agreement with the neighbouring landowner?"

### Document and Date Lookup

Questions that locate a specific document or find what was recorded in a time period.

Examples:

- "What documents relate to the sale of the north field?"
- "What was happening with the estate in the 1960s?"
- "Is there a record of the 1978 drainage survey?"
- "Show me everything recorded about the mill pasture"

---

## Phase 2 Query Types

These become meaningfully answerable once handwritten documents, maps, and emails are in the archive. The retrieval system can handle them from Phase 1, but useful answers depend on having the relevant source material.

### Spatial and Physical Queries

Questions about the physical layout of the estate that draw on map or survey documents.

Examples:

- "What is the boundary between the home farm and the neighbouring property?"
- "Where does the field drain run through the lower meadow?"

### Relationship and Communication Queries

Questions that draw on correspondence and email threads.

Examples:

- "What did the solicitor say about the boundary dispute?"
- "What was agreed in correspondence with the estate agent in 2005?"

---

## Phase 3+ Query Types

These require a sufficiently large and well-indexed archive to produce useful answers.

### Aggregated and Analytical Queries

Questions that require synthesising across many documents to produce a summary or timeline.

Examples:

- "Give me a complete history of land transactions on the estate"
- "Summarise everything known about drainage works since 1950"
- "What changes were made to the field boundaries between 1960 and 1990?"

---

## What the System Does Not Answer

These are explicitly out of scope:

- Questions about land or property outside the estate
- Legal advice or interpretation — the system surfaces what a document says, not what it means legally
- Predictive or forward-looking questions
- Questions requiring real-time or current data (current land registry, current ownership)
- Arithmetic or financial calculations across documents

---

## Query Quality and Uncertainty

The system must be honest about the limits of its answers:

- If no relevant documents exist, the system must say so clearly rather than fabricating an answer
- If the answer is based on partial or low-quality source material, this must be indicated
- Source citations must always be provided so the user can verify the answer against the original documents

The practical quality of answers is directly proportional to the breadth and quality of documents in the archive. Building the dataset is as important as building the retrieval system.
