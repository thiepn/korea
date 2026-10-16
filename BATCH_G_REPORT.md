# KOREA Batch G — Three Complete Historical Collections

## Version authority

- Confirmed origin: GitHub `thiepn/korea` `main` SHA `c747bdd5fd2c7ec55e6f2891dd58540d704c7ae1`, Git tree `bd35c3bd78b1d92894a1b7cb82c0f607aadbeb04`.
- All files under `canonical/`, including the original v1.1 registry, are byte-identical to the starting tree.
- Every originally published passage among the 107 baseline articles is an unchanged ordered prefix of its present article. New material is append-only for 12 existing articles; the other 95 prior article files are unchanged.

## User-facing functionality

- Chapter `III.3` now offers all ten Silla subjects in canonical order, rather than only three.
- The complete-Chapter home shelf derives its three entries from actual published availability and supports future complete Chapters without manually adding more HTML; the Chapter CTA resolves the matching ten-stop curated trail.
- Curated timeline: 43 landmarks (7 new). Curated explanatory relationships: 51 (11 new). Thematically curated pathways: 14 (1 new ten-stop `silla-rise-complete`).
- Seven new search alias groups support Korean terms for Naemul, Silla, Gwanggaeto, Jinheung, bone rank, Queen Seondeok and Kim Chunchu / Kim Yushin.
- Twelve original Hangul and Korean War articles gain a new substantial passage exploring historical evidence, social and technological questions, and interpretive limits. All past material, browser-local bookmarks, route hashes and saved progress remain compatible.

## Actual authored corpus

- Baseline: 107 articles, 405 passages, 48,075 corpus words.
- Batch G: 7 new Silla articles, 28 new Silla passages, 12 append-only evidence-question passages, 6,523 new corpus words.
- Total: **114 articles, 445 passages, 54,598 words** counted by the source-first compiler. No stress-test or boilerplate text is counted as published words.
- Individual Silla articles are sustained original narrative syntheses; they are not yet multi-thousand-word historical monographs.

## Evidence reliability

- Institutional references from the Academy of Korean Studies and UNESCO were checked for selected facts. Seven passage-level anchors are embedded in the new Silla articles. The broad historical narrative, causal interpretations and descriptions of possible lived experiences are original editorial synthesis, **not verified claim by claim**.
- Where written narratives and monuments differ or have ambiguous readings (particularly the Gwanggaeto Stele), the text expressly preserves uncertainty; no invented first-person testimonies or purported archival quotations are introduced.
- No images or media were reproduced from external source sites, and no paid resource or database was created.

## Measured local checks

- `python3 scripts/build_release.py`: PASS. **559 public assets**, 1,418,033 bytes. No `canonical/`, `content/`, internal Python/test files or raw editable articles published.
- `python3 tests/batch_g_pipeline.py`: PASS. Every previous block preserved exactly, seven new validated canonical articles, twelve append-only records, exact source counts, replay-safe idempotence, stable content addresses.
- `python3 tests/batch_g_journeys.py`: PASS. Real Chromium execution with local deterministic asset responses at **1440×900, 390×844 and 320×720**; all three complete Chapters, Korean full-text search, passage-level evidence and mobile horizontal-overflow gates pass.
- Earlier Batch B/C/D/E source-pipeline tests: PASS at the larger corpus size.
- Local HTTP server: HTTP 200 for index; direct Chromium navigation to `127.0.0.1` is **BLOCKED by administrator** (`ERR_BLOCKED_BY_ADMINISTRATOR`). External public HTTPS browser acceptance **NOT_TESTED**, not mislabeled as pass.

## Remaining meaningful gaps

- 886 of the 1,000 Subchapters still lack published narrative. Most entries remain short relative to the intended enormous multi-million-word corpus. The new Silla articles average hundreds of words, not multi-thousand-word academic treatments.
- More Korean-language primary source transcriptions, scholarly disagreements, archaeological chronology and comprehensive passage-level claim checking are needed.
- Curated aliases cannot replace full Korean morphological or Hanja search. Local reading preferences are not synchronized between devices.
- The historical atlas is a curated guide, not a complete independently verified chronology. Public-origin runtime performance has not been measured.

## Post-merge regression hardening

- A subsequent qualification pass exposed that the original Batch G preservation test assumed the previous corpus was always Git `HEAD`, invalid after merging. It now locates the exact preserved F baseline (`c747bdd5...` on remote, local mirror fallback) and accepts future additive corpus growth.
- The source importer now recognizes complete matching earlier passage sequences anywhere in a published article, not only the final suffix. That lets older import batches be replayed safely after another batch appends more passages. Partial or conflicting overlaps still fail closed.
- The importer change is accompanied by explicit tests for in-sequence replay, and the original B/C pipeline tests were rerun successfully.
