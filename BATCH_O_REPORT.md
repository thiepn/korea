# KOREA Batch O — Two complete Chapters / substantial original historical writing

**Baseline GitHub main:** `7baf2f930498ec8ec595d58a50d43c1ab815fb6a`  
**Preserved exact source tree:** `c7e29d31a05ca365a8935b379575186ef4797c4c`  
**Canonical v1.1:** unchanged; no renumbering, no replacements of published blocks.

## Scope

- Completed `V.5`, *Buddhism, Confucianism, and Religious Life*: eight new canonical subjects, two existing articles deepened append-only.
- Completed `VIII.9`, *Independence, Nationalism, Socialism, and Resistance*: nine new subjects and the March First article deepened append-only.
- Deepened six further earlier articles spanning Hangul, family and women's property, Silla queenship, treaty-port commerce, liberation, and wartime civilians.
- Three separately written articles exceed 2,000 Batch O words: `V.5.3` 2,282; `VIII.9.3` 2,033; `VIII.9.8` 2,070. Original editorial material distributed across five inherited authoring manuscripts and new full-length essay continuations.
- Exactly **22,930 words** (compiler `WORD_RE`, editorial paragraphs only) added in **101 passages**, **17 newly published articles**, **nine existing articles deepened append-only**. Total: **183 articles, 937 passages, 141,656 narrative words**.
- Added **20 selective passage-evidence annotations** linking claim / source index / locator / direct-context type. They do not imply every proposition or interpretation is individually verified. Source roles acknowledge the retrospective nature of *Goryeosa*, temple commemorative inscriptions, colonial surveillance accounts, historical memoirs and legacy textbook syntheses.

## Source discipline

References include NIHK's parallel historical source excerpts on Goryeo lantern and Palgwan rituals, Uicheon, 1919 independence declarations, the Republic's provisional charters, the 1923 National Representatives' Conference, the 1920 Bongodong engagements, June Tenth student demonstrations, and AKS historical studies of Gyojang and Singanhoe. Particular contentious casualty figures, uniform statements about political loyalties, and retrospective certainty about movements' future outcomes are deliberately avoided. The essays are original interpretation, not independently peer-reviewed.

## User-facing integration

- 24 complete thematic pathways, including new complete-Chapter routes `goryeo-religion-complete` and `independence-movements-complete`.
- 108 dated/thematic atlas landmarks, 163 annotated connections, Korean-language and mixed script aliases for all 20 subjects across the two Chapters.
- Existing source-first JSONL importer, immutable content packs, search shards, bookmarks, positions, and Endless Reader retained. Fix only necessary UI change: narrow-screen long chronology titles at <=350px wrap correctly rather than creating horizontal overflow.

## Focused evidence

- `python scripts/prepare_batch_o.py` / `scripts/ingest.py`: 26 canonical article records; replay-safe import after publication.
- `python scripts/build_release.py`: PASS; 1,109 allowed public assets, 2,937,171 bytes uncompressed; packs <=24kB, shards <=48kB.
- `python tests/batch_o_pipeline.py`: PASS, SHA-256 preservation against 166 original articles and 15 canonical files, nine append-only prior block prefixes and metadata identities unchanged, 22,930 authored words, 20 annotations, no duplicated new paragraphs, replay no-op, deterministic compiler on second pass.
- `python tests/batch_o_journeys.py`: PASS local Chromium 1440x900, 390x844, 320x720; both complete Chapter routes, source panels, Korean search, chronology and no horizontal overflow. Browser fetches deterministic local build assets; public HTTPS browser acceptance NOT_TESTED.

## Release disposition

Remote GitHub commit, PR, merge and Cloudflare deployment must be verified independently. Local test success alone is not release evidence.
