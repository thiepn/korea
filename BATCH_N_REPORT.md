# KOREA Batch N — Early Goryeo historical consolidation

## Scope and exact starting point

- GitHub repository: `thiepn/korea`; verified base `main` SHA `330d73f18920ef097e918a992e5edeba26ac8e47` and tree `4dc625cacd234c58e992e83f378b1af5a13dedbe`.
- Canonical v1.1 files: all 15 preserved byte-identically. Previous articles: all 158 preserved byte-identically except original metadata-preserving, passage-only append in V.1.2 and V.1.5.
- Eighth new articles under V.1: V.1.1, V.1.3, V.1.4, V.1.6, V.1.7, V.1.8, V.1.9 and V.1.10. V.1.2 and V.1.5 remain published with two extra original passages each.
- Full tenth Chapter: `V.1 — Goryeo after 936`; all 10 IDs are readable.

## Genuine authored prose

- Baseline: 158 articles, 784 immutable passages, 109,655 narrative words.
- Batch N: +8 genuinely authored new articles, +52 original passages, +9,071 original words.
- Result: **166 articles; 836 passages; 118,726 genuine authored words**.
- Independently long new essays (same regex/counter as existing compiler): V.1.1 = 2,137; V.1.4 = 2,217; V.1.7 = 2,027 words. Five remaining new articles contain 426–477 words, and two prior ones get append-only additions. This is a meaningful published chapter but not a scholarly book-length treatment of all ten subjects.
- Paragraph uniqueness tested; no synthetic benchmark content included in narrative counts.

## Sources and reliability

- New evidence anchors: **14** specific claims within passages, linked to Korean historical institutions.
- Documents and institutional scholarship: *Goryeosa* text excerpts on 956 slave-status investigation, Seongjong's provincial twelve *mok* decree (983), the 993 *sangpyeongchang* decree, Choe Seung-ro's incomplete memorial submitted in 982, and AKS scholarship on the *jeonsigwa* land allotment introduced in 976.
- Sources are selected **claim-level direct or contextual references**, not sentence-by-sentence peer review. The source chain between tenth-century events and fifteenth-century compilation of the *Goryeosa* is explicitly discussed in the narrative. Unnamed farmers and enslaved people are not represented by invented first-person quotes or manufactured case files.

## Exploration and integration

- New `goryeo-foundation-complete` route: all 10 ordered V.1 IDs; total curated routes: 22.
- Historical timeline: 93 grounded events, up from 86 (eight new candidate events, one duplicate 936 event reconciled).
- Curated explained relationships: 143 (11 new links) connecting state formation, land, education, regional geography, and public responsibility across canonical Chapters.
- Korean aliases: all ten V.1 topics now have searchable Korean terms.
- Existing Endless Reader, state/bookmarks, search shards, canonical registry, and immutable hash-based content pack engine remain unchanged.

## Tests

- `python scripts/prepare_batch_n.py`: deterministic JSONL with counted original words and verified source indexes — PASS.
- `python scripts/ingest.py content/imports/batch_n_goryeo.jsonl --dry-run`: 0 changes after first import — PASS.
- `python scripts/build_release.py`: production allowlist build — PASS, **980 assets**, **2,566,248 bytes** uncompressed.
- `python tests/batch_n_pipeline.py`: original 158 articles and 15 canonical file hashes, block append invariants, canonical IDs, source evidence, replay, 48KiB shard and 24KiB pack bounds, repeat-zero rewrites, clean dist — PASS.
- `python tests/batch_n_journeys.py`: actual Chromium execution with deterministic generated local assets at 1440×900, 390×844 and 320×720 — PASS. Tests Chapter, 10-stop route, source notes and their HTTPS links, Korean search `최승로`, timeline, legacy Chapter, viewport overflow and no pageerrors.
- **Public HTTPS-origin Chromium test is NOT_TESTED.** A build or Cloudflare status alone does not establish runtime acceptance on the public domain.

## Outstanding

- 834 of 1,000 canonical Subchapters remain without published narrative. Nine earlier complete Chapters plus V.1 now provide ten complete reading Chapters.
- Most published articles are shorter than 2,000 words. The research apparatus offers limited anchors; systematic academic vetting, Korean/Hanja morphological search and public-origin browser acceptance remain outstanding.
- No new paid services, database migrations, R2 or D1 resources.
