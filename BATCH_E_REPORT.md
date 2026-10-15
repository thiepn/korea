# KOREA Batch E — Long-form Historical Reading and Source Context

## Original source preservation

- Parent remote `main` commit: `116be5a2fc8af3254d977eecf88be21a55c2d146`, exact Git tree `62b4d7bcae29e8b2cb131b7714fa3e231ef3cb6b`; reconstructed Batch D source matches it.
- Original 10 Parts, 100 Chapters, 1,000 named Subchapters, and 10,000/100,000 deeper virtual IDs unchanged.
- No previously published article source or block changed. Three new canonical article IDs added: `V.5.6`, `VI.4.3`, `IX.3.3`.
- All authoring material, canonical sources and research registry remain outside release output.

## Genuine historical narrative

| New canonical article | Original words | Passages | Contextual institutional references |
| --- | ---: | ---: | ---: |
| V.5.6 — Goryeo Tripitaka | 2,614 | 8 | UNESCO Memory of the World; UNESCO World Heritage Centre |
| VI.4.3 — Creation of Hunminjeongeum | 2,670 | 9 | UNESCO Memory of the World; National Hangeul Museum |
| IX.3.3 — Busan Perimeter | 2,012 | 7 | U.S. Army Center of Military History; United Nations Command |
| **Total** | **7,296** | **24** | **6** |

**Total corpus: 95 articles, 357 passages, 38,969 genuinely authored words.** These are original editorial essays; institutional references substantiate background and chronological anchors but no line-by-line independent academic verification was performed. The Busan material draws partly from military institutional sources; multi-perspective Korean historical sources and civilian scholarship remain important next research steps. No copied or synthetic stress text is published. Reading sources are displayed as links with labels explaining their role and limits.

## Implemented product changes

- Replay-safe, deterministic Markdown-to-JSONL preparation for new multi-thousand-word essays; minimum length, passage depth, canonical IDs, duplicate titles, and institutional provenance validated.
- Source metadata flows through existing importer, content-addressed compiler and small publication manifest; provenance visible in expandable, keyboard-accessible reader notes. Backward compatible with all existing articles.
- Featured long-form shelf on Discover and an eleventh cross-era themed pathway for extended reading.
- 3 linked chronological landmarks, 4 new explained connections, and contextual timeline backlinks from these reader pages.
- Additional Korean-script aliases for the three articles, without introducing an independent search engine or metadata silo.
- No R2, D1, paid services, credentials or production schema changes.

## Executed verification

- `python scripts/build_release.py`: PASS, 425 public assets, approximately 1.12 MB uncompressed.
- `python tests/batch_e_pipeline.py`: PASS, original prose totals, 6 references, replay safety, canonical preservation, bounded packs/shards, deterministic rebuild.
- `python tests/batch_e_journeys.py`: PASS, Chromium desktop 1440x900 and mobile 390x844 / 320x720: 3 featured essays, 11 routes, notes, timeline return, Korean search, no overflow.
- `python tests/batch_d_pipeline.py`, `tests/batch_c_pipeline.py`, `tests/batch_b_pipeline.py`: PASS (older Batch D fixed corpus-count assertions updated to growth-tolerant compatibility floors).
- `python tests/batch_d_journeys.py` and `tests/batch_c_journeys.py`: PASS older reader modes, detour restoration, 90/140-passage bounded DOM and cache restoration.
- `python scripts/stress_corpus.py --articles 1000 --blocks 10 --words-per-block 110`: PASS, **synthetic only**, 1.1M words, 7.858 seconds, 54.79 MB peak traced Python memory, repeat rewrites 0.
- Public HTTPS-origin browser acceptance: NOT_TESTED in this environment; should not be conflated with simulated asset-fetch Chromium checks.

## Limits and follow-ups

- The corpus remains 38,969 words across just 95 of 1,000 canonical named subchapters, far short of the long-term multi-million-word archive.
- Reference links are contextual sources, not embedded scholarly annotations for individual factual sentences. Peer review, primary-source apparatus, divergent scholarship, translations and source verification remain important.
- Cross-era routes and timeline have 11 collections, 30 landmarks, and 28 explained connections, but are editorially selective rather than comprehensive.
- Korean alias search is curated rather than comprehensive morphological indexing; Hanja and translated prose are not present.
- Huge cross-article Endless sessions need ongoing profiling; user state is browser-local, not synced.
- No paid infrastructure has been added.
