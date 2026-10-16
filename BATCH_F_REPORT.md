# KOREA Batch F — Complete Historical Reading Collections

## Exact baseline and preservation

- Parent GitHub `main`: `c50dbc7df1772a37e4fc92bc87040f05c2d81f21`, tree `9944f92cb1de9276bda55017b27419b0b60c8178`.
- Canonical Constitution, all Part architecture files and registry v1.1 are unchanged byte-for-byte.
- All **95 previously published article source JSON files remain byte-identical** to the parent. No earlier passage was rewritten or renumbered.
- No replacements of ID roots, no newly invented canonical levels; terminal and Section slots remain reserved for later authored material.

## Actual authored historical volume

| Metric | Before | After | Change |
|---|---:|---:|---:|
| Published Subchapter articles | 95 | 107 | +12 |
| Genuine narrative words (compiler count) | 38,969 | 48,075 | **+9,106** |
| Authored passage sections | 357 | 405 | +48 |
| Complete ten-Subchapter Chapters | 0 | 2 | +2 (`VI.4`, `IX.3`) |
| Curated reading pathways | 11 | 13 | +2 |
| Timeline landmarks | 30 | 36 | +6 |
| Explained cross-article relationships | 28 | 40 | +12 |
| Search alias subjects | 28 | 40 | +12 |

All new passages are original editorial narrative and individually written; no synthetic stress strings were published. The twelve essays average approximately 759 words each. They constitute meaningful complete Chapter sequences, **not** a set of twelve multi-thousand-word scholarly monographs. Both collections should receive greater documentary and interpretive depth in later work.

## Claim-level evidence, accurately scoped

- 24 selected institutional contextual source links, with **10 specific annotated factual claims** distributed across the twelve new articles.
- Verified background from National Hangeul Museum and UNESCO regarding Hunminjeongeum; from U.S. National Archives for the text and procedures of the 1953 Armistice; from ICRC institutional documentation for humanitarian work and barriers.
- Each displayed annotation distinguishes *documented* from *contextual* anchors, states the claim, provides a source-specific locator, and explicitly declines to certify the rest of its paragraph or article.
- No wholesale academic peer review, systematic Korean-language archive triangulation or verification of every military and linguistic interpretation was performed.
- The source register is editable outside public dist; only reader-facing provenance metadata is compiled into the published packs.

## Product changes

- Complete Chapter cards on the homepage and ten-stop continuous reading paths for the writing system and the Korean War.
- All ten entries in each Chapter appear as readable. Other 980 canonical Subchapters retain their original published/planned state, with the appropriate count.
- Reader passages carry accessible inline `<details>` panels linking supported facts to named institutional sources without requiring a new engine or database.
- Six dated atlas nodes, twelve author-explained relations, twelve Korean query alias entries. Existing subject search, bookmarks, resumes, themed reading, deep/overview/endless and bounded passage rehydration preserved.
- No R2, D1, database migration, paid service, new account system or runtime dependency.

## Executed checks

- `python scripts/build_release.py` — PASS: 507 public runtime assets, 1,297,605 bytes before compression, no canonical/source build folders exposed.
- `python tests/batch_f_pipeline.py` — PASS: imported canonicals, 95 source byte identities, exact word and passage counts, replay safety, stable hashes, 24 sources, 10 claim anchors.
- `python tests/batch_f_journeys.py` — PASS: real Chromium DOM and JS at 1440×900, 390×844 and 320×720 using deterministic asset responses. Tests complete Chapters, two ten-stop pathways, source annotations, passage loads, Korean search and overflow.
- Previous B/C/D/E pipeline regression suites — PASS after updating old E exact-count assertions to minimum coverage.
- Previous B/C/D browser acceptance — PASS. A long concatenated E browser run exceeded its time limit; separate E browser acceptance previously passed but was not requalified after the F content increase in that attempt.
- Synthetic 1.1M-word stress corpus, NOT published — PASS: 8.292 seconds compilation, 54.87 MB peak traced Python memory, no unchanged asset rewrites.
- Local Python HTTP server returned 200. **Real local-origin Chromium is BLOCKED:** `net::ERR_BLOCKED_BY_ADMINISTRATOR`; public HTTPS-origin browser acceptance NOT_TESTED.

## Remaining limitations

- Only 107/1,000 canonical Subchapters have published sample narratives, with 893 remaining planned. Most published articles are still shorter than the multi-thousand-word ambition.
- Passage-level evidence currently covers only ten new factual anchors; source coverage is selective, often contextual, and the war narrative still needs extensive non-US, Korean-language, civilian and DPRK primary-source triangulation.
- English/Korean keyword aliases are curated; there is no comprehensive Korean morphological index, Hanja lexicon or translated full corpus.
- The new reading order follows the canonical chapter; a future extended-history reader could add stronger prefaces, end-of-chapter review, map-grounded routes and glossaries without replacing the history IDs.
- Browser-local progress remains local to one origin/device, and heavy cross-article reading performance has not been reprofiled on actual public HTTPS origin.
