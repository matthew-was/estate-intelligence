# Notion Lab Entry

This skill creates a new entry in the Programming Lab Notebook in Notion at the end of a
programming session. Entries are concise — bullet points only — and include links to all
commits made during the session.

---

## When to use

Use this skill when the developer asks to create a lab notebook entry, log a session, or
record what was done in Notion.

---

## Workflow

### Step 1 — Gather commit information

Ask the developer: "What commit or time should I use as the start boundary for this session?"

Then run:

```bash
git log --oneline --since="<boundary>" --reverse
```

or

```bash
git log --oneline <boundary-commit>..HEAD --reverse
```

Use the result to build a list of commits with their short hashes and messages.

To construct GitHub-style commit links, check the remote URL:

```bash
git remote get-url origin
```

Format each commit as a markdown link:
`[abc1234](https://github.com/<owner>/<repo>/commit/abc1234) — commit message`

---

### Step 2 — Infer entry properties from context

Infer **Type** and **Outcome** from the session content without asking:

- **Type**: use the most appropriate option — Debugging, Feature, Refactor, Research, Note,
  Documentation
- **Outcome**: infer from whether the goal was achieved — Success, Partial, or Failed

Ask only for **Start time**: "What time did this session start?" (date is always today)

---

### Step 3 — Fetch the Notion Markdown spec

Before creating the page, fetch the MCP resource at `notion://docs/enhanced-markdown-spec`.
Do not guess or hallucinate Notion Markdown syntax.

---

### Step 4 — Create the entry

Create the page in the Lab Entries data source (`collection://30a66aac-d77c-4da6-b243-0bbb9aecdf7c`).

**Properties:**

| Property | Value |
| --- | --- |
| `Name` | Session title (provided by developer or inferred from the work done) |
| `Type` | Inferred from context |
| `Outcome` | Inferred from context |
| `date:Date:start` | Today's date (YYYY-MM-DD) |
| `date:Date:is_datetime` | 0 |
| `date:Start:start` | Today's date + start time (ISO-8601 with time) |
| `date:Start:is_datetime` | 1 |

**Content structure (bullet points only):**

```markdown
## What was done

- <bullet per meaningful thing accomplished>

## Commits

- [<short-hash>](<commit-url>) — <commit message>
- [<short-hash>](<commit-url>) — <commit message>

## Next steps

- <bullet per next step, drawn from session context>
```

Keep each bullet to one line. No paragraphs. No sub-bullets unless essential. Omit any
section that has nothing to say (e.g. no commits, no next steps).

---

## Notes

- The Lab Entries database is at `https://www.notion.so/c92903bec2524c48934b510d2e8e776c`
- The data source ID is `30a66aac-d77c-4da6-b243-0bbb9aecdf7c`
- The Programming Lab Notebook page is at `https://www.notion.so/d1e7e18f044a4d7bba5ddb1e0da968ca`
- Always fetch the Markdown spec before creating the page — do not rely on memory of the spec
- If the git remote is not GitHub, omit commit links and include only short hashes and messages
