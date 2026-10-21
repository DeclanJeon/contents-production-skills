# Frozen QA prompts (baseline; not to be edited after first run)

Scenario S1 targets the two audit findings: (a) can a consumer tell whether a craft claim in a module is book-derived or self-authored, and (b) does an emotion/retention-heavy request get a craft answer whose basis is stated. Baseline and post-change runs MUST use the byte-identical prompt text below.

## S1a, provenance-awareness probe (single-turn, read-only)

```text
Read video-production-assets/references/16-concept-emotion-retention.md and video-production-assets/references/12-qa.md.

For each file, answer exactly:
1. Which claims in it are derived from supplied source books, and which are the package's own design? Quote the sentence in the file that tells you.
2. If you cannot tell from the files alone, say so explicitly and name what is missing.

Do not read any other file. Do not edit anything. Return a table: file | derived-from-books | own-design | which-sentence-told-you | unknown.
```

## S1b, emotion/retention craft probe (single-turn, read-only)

```text
A client wants a 60-second vertical brand video. The brief: a local bakery owner shows the moment she decides to keep her grandmother's recipe instead of selling it. The client asks only for the emotional design and the retention architecture, no script, no images, no generation.

Using only this package, produce:
1. The intended emotion journey as an ordered sequence, each step tied to something an audience can observe.
2. A retention architecture for 60 seconds with per-segment open question.
3. For every craft claim you make, name the exact package file and section it came from, and say whether that file states the claim's source basis. If it does not, mark the claim [BASIS-UNSTATED].

Do not generate media. Do not write files.
```

## Scoring

- S1a: PASS only if the answer names the actual sentence for each file and correctly separates `설계 확장` / ID-listed content from unbased content. A generic "some claims may be unsourced" without quoting the file's own sentence = FAIL.
- S1b: PASS only if every craft claim carries a file+section locator, and claims from modules with no provenance heading are marked `[BASIS-UNSTATED]`. Missing locators, or unmarked unbased claims = FAIL.
- Both prompts must be run **before** any edit (baseline) and re-run **after** (post). Same prompt bytes, fresh single-turn session each time. No statistical claim is made from one sample per arm.
