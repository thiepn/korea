# KOREA — Batch B Implementation and Qualification

## Source baseline

GitHub main `4f48671edafec3a29b3cb3015fc737b5133fc93e` (merged Batch A). Original v1.1 canonical source files and 17 existing history articles retained unchanged.

## Real changes

- Ten new original history essays under existing canonical IDs across all ten Parts. Source import JSONL under `content/imports/batch_b_editorial.jsonl`, replay-safe `scripts/ingest.py` with dry-run, append and unpublished-only replace.
- Deterministic v2 compiler `scripts/build_corpus.py` derives manifest, content-addressed small packs and sharded inverted full-text search, with SHA-256 metadata, stale asset deletion and unchanged-output preservation.
- Browser `content-platform.js` loads packs on demand with bounded LRU + prefetch, and search shards only when queried, with bounded LRU, token intersections, loading race suppression and title-search fallback.
- Existing Explorer, 10 eras, 100 chapters, 1,000 Subchapters, virtual Section/terminal addresses, three reader modes, browser-local bookmarks, detours and thematic trails remain in original app.js.
- Existing Cloudflare Pages `main` build remains `python3 scripts/build_release.py`, targeting allowlisted `dist/`; now compiles and validates before output. No R2, D1 or service costs.

## Corpus

27 authored illustrative articles, 108 independent passages, 13,904 words (formerly 17 articles, 68 passages, 8,672 words). 27 content-addressed reading packs; 182 sharded search payloads, 2,876 index terms; 219 total static assets, 560,394 uncompressed bytes.

## Measured gates

- PASS canonical architecture unchanged at 10/100/1,000 with 10,000/100,000 reserved IDs.
- PASS manifest article/block identities, packed block SHA digests, search shard hashes, and content-addressed release output.
- PASS importer idempotent replay, invalid ID rejection, and published-content replacement prevention.
- PASS unchanged rebuild wrote zero assets.
- PASS JavaScript syntax, compilation, asset allowlist, under 20k Pages file cap.
- PASS Chromium in-memory DOM at 1440x900, 390x844, 320x720 for reading packs, lazy search, modes, bookmarks and canonical navigation.
- NOT_TESTED external Cloudflare HTTP-origin browser user acceptance; local HTTP Chromium is restricted by runtime networking.

## Remaining product gaps

The public archive remains a relatively small corpus, not millions of words. Content generation orchestration, editorial expansion, R2 migration and large-index stress testing at 100k+ articles are still future work. Search is English-token-based with two-character sharding, rather than multilingual or an advanced search server. The reader still retains all DOM passages during an extremely long Endless session; viewport virtualization is a later improvement. Full content provenance/citations and image rights are not in scope for this volume-first project. Browser-local bookmarks do not sync across devices.
