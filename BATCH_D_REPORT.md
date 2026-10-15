# KOREA Batch D — Deep History and Connected Timeline

## Provenance and integrity

- Reverified predecessor GitHub `main` commit `e6c32c006af87be7878f9b00a2fd1f2acdb1ace1`; its Git tree `fd22017e24528f0821ca11dccbca2c86002ae5a8` exactly equals the locally reconstructed Batch C working tree.
- All original canonical Part I–X and governance source files unchanged; ten Parts, 100 Chapters, 1,000 Subchapters, 10,000 reserved Sections and 100,000 virtual terminal addresses remain as before.
- All earlier published article files preserved byte-for-byte. Batch D inserts 15 new distinct canonical article IDs and does not replace previous passages.

## Real published editorial material

| Measurement | Before | After | Change |
| --- | ---: | ---: | ---: |
| Published narrative articles | 77 | 92 | +15 |
| Independently loadable passages | 258 | 333 | +75 |
| Actual authored words | 24,137 | 31,673 | +7,536 |
| Curated thematic pathways | 6 | 10 | +4 |
| Chronological landmarks | 0 | 27 | +27 |
| Explained cross-topic connections | 0 | 24 | +24 |

- Editorial manuscript `content/editorial/batch_d_deep_volume.md` contains five distinct substantive passages per subject, discussing material evidence, households, government, education, legal reforms, the Korean War and contemporary labor.
- Its replay-safe import is `content/imports/batch_d_deep.jsonl`; `scripts/prepare_editorial.py --release D` can prepare future unpublished source batches. The manuscript and import are not served publicly.
- Writing is **original, unverified editorial interpretation**, not sourced scholarly research; this is made clear in the reader. Dates in the authored timeline are curated interpretations with approximate periods explicitly marked. Synthetic performance test text is never published or counted as actual prose.

## Implemented reading and discovery

1. New chronological Atlas page `#/timeline`, plus stable era deep links `#/timeline/VI`, showing 27 human-authored landmarks. Each card retains an original canonical destination and its actual readable/planned state.
2. Connected reading: 24 bidirectional explanatory links prioritized over merely adjacent topics. Clicking a connected story from the reader opens a detour and permits restoration to the original passage and reading chain.
3. New mobile accessible contextual link section where the previous desktop-only rail was hidden.
4. Korean keyword/alias search for 25 genuinely published subjects. Unicode word indexing plus two-syllable substring matching, while preserving original English search and lazy sharding. This is targeted bilingual discovery, **not** complete Korean translation or morphological search.
5. Bounded reader HTML memory: at most 48 distant passage HTML snapshots plus at most 22 live passages. Evicted canonical prose is recoverable from published immutable content packs; already-pending restorations return the same task instead of racing duplicate requests.
6. Reworked source-first deterministic build includes Atlas compiler with canonical-ID, chronology-order, and explained-link validation; public artifact allowlist protects all authoring and governance files. Cloudflare Pages remains the only hosting service.

## Executed checks

- `python scripts/build_release.py` — PASS: 402 public assets, 1,014,352 raw bytes; all original canonical ID counts and pack/search integrity pass.
- `python tests/batch_d_pipeline.py` — PASS: 15 new five-passage texts, exact word totals, safe importer replay, source hashes, bounded packs and shards, deterministic rebuild.
- `python tests/batch_d_journeys.py` — PASS: Chromium 1440×900 and 390×844 with timeline, 10 pathways, newly published article, contextual detour and return, Korean and English search; 90-passage synthetic DOM and snapshot pruning, real pack rehydration. 320×720 layout/timeline/no-overflow PASS.
- `python scripts/stress_corpus.py --articles 1000 --blocks 10 --words-per-block 110` — PASS synthetic, non-published 1.1M words / 10,000 passages, compile 9.156 seconds, traced Python peak 54.36 MB, 155 search shards, max shard 23,743 bytes, zero rewritten assets on repeat.
- Local static HTTP requests `/` and `/data/atlas.json` returned HTTP 200. Chromium HTTP-origin navigation BLOCKED by environment administrator (`ERR_BLOCKED_BY_ADMINISTRATOR`); HTTP-origin browser acceptance NOT_TESTED. In-memory Chromium does execute original app JS and render actual CSS/content pack assets.

## Still outstanding

- 92 of 1,000 canonical Subchapters have demonstration text. 31,673 words remain tiny compared with the intended multi-million-word universe; most subjects remain planned. Later work should produce fuller book-length narratives instead of mechanically repeated fragments.
- The current timeline is an interpretive, selective 27-landmark lens rather than an exhaustive dated event database; some dates are only approximate. Scholarly verification and sourced annotations are not yet in place.
- Korean alias search is limited to selected topics; stemming, Hanja, Korean-language full prose, and cross-language semantic ranking are future work.
- Reader memory retains metadata about all pruned passages and relies on pack network access for evicted HTML; extremely long hundreds-of-thousands-of-passages session recovery and offline failure UX require further profiling.
- Cross-device reading sync, authoritative media licensing, full-text citations, R2, D1 and real public browser qualification remain future work. No paid services were introduced.
