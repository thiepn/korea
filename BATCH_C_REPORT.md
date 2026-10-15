# KOREA Batch C — Corpus Expansion, Search Scale & Long-Session Reader

## Provenance and protected baseline

- Exact predecessor `main`: `e82cca36384b309ce677036c8c90f56219a84c89`.
- The predecessor Git tree SHA `abe4094309fc9ed8540af178e1411c9924793f58` was reconstructed from the Phase 1/Batch A archive and Batch B source delta, then locally verified to equal GitHub.
- Original canonical Constitution and Part I–X architecture files are **unchanged**. Existing 27 article JSONs and their original passages remain intact.

## Original writing published in this batch

- 50 newly authored prose entries spread across all ten Parts, each with 3 individually loadable passages (150 additional passages).
- Articles increased **27 → 77**, passages **108 → 258**, actual narrative words **13,904 → 24,137** (+10,233; +73.6%).
- New editable editorial source `content/editorial/batch_c_volume_01.md`, replayable import `content/imports/batch_c_editorial.jsonl`, source reader `scripts/prepare_editorial.py`; imported article JSON remains the delivery source.
- Added release metadata (`release: C`), a homepage shelf for newly published entries, and a seventh cross-era trail. Previous six trails are retained.
- Editorial texts are original **unverified demonstration narratives**. They are not citations, externally checked scholarship, or Section/subsection content already completed. Content volume is genuine authored prose; synthetic stress text is explicitly excluded.

## Core implementation

1. **Adaptive full-text sharding** — the existing two-letter token index still works, but crowded prefixes split into additional prefix levels (48 KB target per shard). Browser search resolves the longest existing prefix lazily and preserves the previous LRU behavior.
2. **Bounded long-session DOM** — `reader-window.js` replaces far-away `.body-section` elements with height-preserving placeholders. IntersectionObserver restores HTML as users scroll back; reader tokens, original canonical URLs, pack caching, and local-only bookmarks remain intact. A 140-passage test caps live passages at 22 in three browser widths.
3. **Extended progress continuity** — saved positions and detours now include the Endless reading chain. Reloading a saved reading route replays previously visited chunks and restores scroll position while applying DOM pruning. Cross-article loading remains controlled by the original reader engine.
4. **Source-first publication** — original build command stays `python3 scripts/build_release.py`; new reader module is allowlisted; canonical files and editorial inputs remain excluded from `dist/`. Single oversized passages are rejected by the compiler.
5. **Authoring tooling** — Markdown-to-JSONL preparation validates canonical IDs and passage prose, and the existing importer rejects unknown canonical IDs, accidental published replacement, and ambiguous append overlaps.

## Measured checks

| Check | Result |
|---|---|
| v1.1 architecture, original article identity, pack hashes, search shards | PASS |
| Batch C editorial import replay and no source mutation | PASS |
| JavaScript syntax, public-file allowlist, Cloudflare Pages static build | PASS |
| Batch B compatibility in-memory Chromium at 1440, 390, 320 px | PASS |
| Batch C newly published article, full-text search, bookmarks, Endless, bounded 140-passage DOM, scroll-back restoration | PASS at 1440, 390, 320 px |
| 1,000-article / 10,000-passage / 1,100,000-word **synthetic, nonpublished** compiler stress | PASS, 6.426 s, 54.11 MB peak `tracemalloc`, 1,000 packs, 51 shards, max 23,743-byte shard, 1,054 outputs |
| Stable rerun of synthetic pack compiler | PASS (0 rewritten assets) |
| Actual Cloudflare public HTTPS browser origin | NOT_TESTED; local Chromium permits in-memory tests but not local HTTP navigation in this environment |

## Remaining limitations

- Only 77/1,000 canonical Subchapters have prose; 24,137 words are still a tiny fraction of the intended history universe. Avoid presenting the archive as complete or fully researched.
- Reader long-session restoration may need optimization to skip directly to distant virtualized pages when hundreds/thousands of articles exist. Its current replay is correct for modest sessions but linear in previously loaded passages.
- Search is English tokenization, exact-token intersection, and limited-title discovery. Korean-specific language search, stemming, semantic ranking, and advanced search UI remain future work.
- Browser session HTML snapshots retain prior content in JS memory even though live DOM is bounded; production-million-word session memory and scroll-anchor behavior need further dedicated profiling.
- Cloudflare Pages free-plan 20,000-file capacity requires R2 or larger pack strategies eventually, but neither was introduced here. All new content is intentionally free-tier static.
- Browser-local reading history does not sync between devices; full historical image rights, citations, and expert research verification are out of scope.
