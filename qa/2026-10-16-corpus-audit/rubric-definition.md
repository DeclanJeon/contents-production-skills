# Rubric definition, 0-5 per skill (fixed before scoring)

Anchors are observable: each score names what must be present in the skill's own files. Scoring is done per *independent* installed skill (24), not per reference file.

| Score | Name | Required observable |
|---|---|---|
| 0 | absent | No owner exists for the request; no file states the behaviour. |
| 1 | named-only | Trigger/description exists but no procedure, no boundary, no output contract. |
| 2 | partial | Procedure present for the main path; boundary or output contract missing; no acceptance check. |
| 3 | usable | Procedure + explicit boundary (what it excludes) + named output; acceptance check missing or vague. |
| 4 | gated | Above, plus an explicit acceptance/QA criterion a reviewer can fail the work against, and named blockers instead of silent substitution. |
| 5 | gated + evidence-bound | Above, plus each craft claim traceable to a cited source (book/module) with read-scope stated, and an exercised verification record. |

## Mandatory modifiers (report beside the score, never folded in)

- `unverified`, the skill's craft content rests on books this audit did not read. Score may not exceed **3** while any load-bearing source is unread.
- `[INFERENCE]`, a gap asserted from an unread source.
- `dup:<other skill>`, the same principle is stated by two owners; the pair is scored once for the principle and flagged.
- `token:<bytes>`, instruction bytes a consumer must read to apply the skill.

## Evidence addressing (new, the reading set is 136 works behind 213 paths)

A score-5 citation MUST name an addressable location, not just a book title:

- `E:\Book\06_Book\<relpath>#L<line>`, line 1-based; books carry no Markdown headings, so join to the nearest `P a g e | N` marker when a line is inside a page.
- If several renditions of the same work exist, cite the **one rendition that was read** and record its byte size, so a reader can find the exact copy. Renditions differ in whitespace and sometimes in content, a citation to `originals/…` is **not** satisfied by the top-level copy.
- A citation with no read state (`READ-FULL|READ-PARTIAL`) is not evidence; the read state attaches at the citation, not at the file level.

## What is NOT evidence for a score

- A file existing, a link resolving, a heading being present, a test passing.
- A skill describing correct behaviour it does not require.
- A book being on disk. Only read book content with a stated read state counts.
- A previously recorded QA number reused without rerunning the scenario.
