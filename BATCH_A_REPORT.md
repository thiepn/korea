# KOREA — Batch A Exploration Experience (feature-branch candidate)

**Baseline:** `main` at `4b226b5e2868afbc36d0a244e49fd648e48e6fee`, tree `dd8ecac4e1b57d229292f414dd8899f2420ae7ad`.

## Implemented

- Functional **Discover** page with 10 eras, reading samples, themed-entry cards, and personal Continue Reading action.
- Dedicated **Chapter** routes `#/chapter/VI.4`, breadcrumbs, counts, and each Chapter's 10 canonical Subchapters. Era rows now permit both navigating to a Chapter and previewing its Subchapter list.
- Functional **Explore** gallery and six curated cross-era pathways; collection pages distinguish readable from planned destinations. A selected trail guides the Endless Reader through its available stops.
- Search across **all 1,000 canonical Subchapter IDs/titles** and article paragraphs within published demo texts. Search supports All, Read now, Planned filtering and contextual excerpts. The full-text index is limited to sample prose, and not claimed to cover the planned archive.
- Reader Overview incorporates a real introductory excerpt; Deep dive loads all passage assets on demand; Endless loads new passages and seamlessly transitions to the next article. On-page contextual detours can return to loaded positions; planned detours expose a Return action. Global Continue Reading, bookmarks, passage progress, settings and saved place remain **browser-local**.
- Stronger responsive exploration, higher-contrast secondary text, mobile bottom navigation, and dense Chapter/trail indexes.
- Ten newly written original illustrative articles spread across all ten canonical Parts, preserving all original seven files and 28 original blocks.
- Separate `exploration.js` search module and reproducible `scripts/build_exploration.py` compiler. Deployment build now allowlists `exploration.js`, `data/explore.json`, and `data/search-index.json` alongside the original runtime files.

## Corpus counts

- **17** published *demonstration* articles (was 7)
- **68** independently fetchable passages (was 28)
- **8,672** words (was 4,488)
- **6** themed pathways
- **10 / 100 / 1,000** fixed original Part / Chapter / Subchapter IDs preserved, with the **10,000 / 100,000** structurally reserved descendant address space unchanged.

Illustrative prose is not claimed to be independently source-verified history. Planned canonical addresses are not mislabeled as completed titles.

## Executed checks

- `python3 scripts/validate.py` — PASS: canonical structure, content digest integrity, search-index text consistency, themed path IDs.
- `node --check app.js && node --check exploration.js` — PASS.
- `python3 scripts/build_release.py` — PASS: exactly 76 public assets, no canonical documents, article-source files, tests, or scripts.
- `python3 tests/browser_smoke.py` — PASS desktop 1440×900, mobile 390×844 and 320×720, short landscape 844×390.
- `python3 tests/batch_a_journeys.py` — PASS 1440×900 and 390×844: thematic trail start, sample text search, planned and readable detours, recovery, new-story endless transition, bookmark and local library.
- Attempted local HTTP Chromium navigation — **BLOCKED** by `net::ERR_BLOCKED_BY_ADMINISTRATOR`; therefore browser checks use real DOM/CSS/JS in Chromium with same-page, in-memory assets and are **not HTTP-origin acceptance**.

## Remaining functional gaps

The website is still an expanding demo, not a massive published archive. Only 17 Subchapters have substantive samples. Universal full-text search needs a sharded index before scaling to a large corpus. Story connections are curated rather than inferred dynamically. Section and terminal *titles* are still not authored and remain planned. Browser-local state is not account-synced; detour stacks are session-local. Reading progress is anchored to the currently opened article, not tracked independently for every article inside one Endless chain. No media/maps, server API, R2, D1, full-text indexing of unpublished content, or paid services were added.

## Cloudflare preview safety

The feature branch `feat/batch-a-exploration-experience` is excluded from Cloudflare Pages preview deployment triggers. Production deployments from `main` remain enabled. This branch must **not** be merged or deployed without user approval.
