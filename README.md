# KOREA — Interactive History Universe

**Phase 1: functional local prototype · 15 October 2026**

An interactive, text-first Korean history explorer and continuous reader. This is a **prototype**, not a published historical encyclopedia. The supplied `MASTER v1.1` canonical Part files remain **unchanged** under `canonical/`.

## Run locally

Requires Python 3, no package installation and no accounts.

```bash
cd korea-phase1
python3 -m http.server 8000
```

Open **http://localhost:8000** in a browser. If port 8000 is occupied, substitute another port. Double-clicking `index.html` is **not** supported because the app fetches JSON chunks: it requires a local HTTP server. `npm`, databases, GitHub access, and Cloudflare access are not required.

On Windows: run `py -m http.server 8000` in the extracted folder from a terminal.

## What works

- **Explorer:** responsive homepage; ten eras; featured starting points; random-sample discovery.
- **Canonical navigator:** real ten Parts / 100 Chapters / 1,000 Subchapters extracted from the uploaded master v1.1 Part files. Each Subchapter has 10 structurally reserved Section IDs and 100 virtual terminal IDs, such as `VI.4.2.1.2`; these **are not represented as finished authored titles**.
- **Search:** keyboard-accessible archive lookup across all 1,000 canonical Subchapters (press `/`, arrows, Enter, Esc).
- **Reader:** sample content for seven actual canonical Subchapter IDs; Overview, Deep dive, Endless; lazily fetches independent passage files instead of loading the entire corpus at once.
- **Endless:** scroll-triggered progressive passages followed by a clearly labeled curated transition to the next available demonstration article. This sample trail ends after its seven articles; the complete corpus has not been generated.
- **Progress:** browser-local bookmarks, recent reads, saved reading position and resume control; no user accounts or network writes. Contextual detours can return to a prior reading position.
- **Comfort:** change font size and line width; full-width desktop navigation, responsive mobile drawer and bottom bar; keyboard focus rings, reduced-motion support.
- **Transparency:** prototype narrative and planned/unwritten entries are clearly distinguished. Sample prose is original illustrative content and has not undergone source review.

## Sample topics

| ID | Canonical topic |
|---|---|
| `I.1.1` | The Geological Formation of the Korean Peninsula |
| `II.1.2` | Dangun, Foundation Myth, and the Construction of Gojoseon Origins |
| `III.1.5` | Gwanggaeto the Great and Imperial Expansion |
| `VI.4.2` | Sejong's Linguistic Problem and the Purpose of a New Script |
| `VIII.9.2` | The March First Movement of 1919 |
| `IX.1.1` | 15 August 1945: Liberation, Political Vacuum, and the Collapse of Colonial Authority |
| `X.5.10` | Global Fandom, Cultural Policy, Intellectual Property, Cultural Controversies, and the Evolution of Hallyu |

The sample corpus has **4,488 words across 28 independently fetched passage assets**. These do not approach the proposed long-term 100,000-word milestone.

## Source layout

```text
index.html                     Static application entry point
styles.css                     Responsive editorial design
app.js                         Navigation, search, modes, progressive reading, persistence
data/architecture.json         Generated index of all 1,000 canonical Subchapters
/data/content-manifest.json    Versioned manifest, content counts, chunk digests
/data/articles/*.json          Editable complete prototype articles
/data/blocks/*.json            Individually fetched release chunks
canonical/                     Original uploaded Part files, governance, registry and v2 draft
scripts/build_architecture.py  Parse canonical files without renaming anything
scripts/build_articles.py      Build curated sample article sources
scripts/build_packs.py         Produce granular reading assets and SHA-256 manifest
scripts/validate.py            Validate hierarchy, IDs, payloads and checksums
tests/browser_smoke.py         Chromium DOM interaction tests using in-memory assets
```

## Rebuild and validate

```bash
python3 scripts/build_architecture.py
python3 scripts/build_articles.py
python3 scripts/build_packs.py
python3 scripts/validate.py
node --check app.js
```

**Important:** `scripts/build_articles.py` regenerates curated source samples; if you edit `data/articles/*.json` directly, run `build_packs.py` only. In a production content engine, replace the hand-curated source generator with governed batch ingestion.

### Browser checks

The `tests/browser_smoke.py` test requires Python Playwright and a Chromium installation available at `/usr/bin/chromium` (adjust for other operating systems). It executes the real UI source and simulates JSON asset responses in an about:blank page. This validates DOM interactions and responsive layout, but **does not** establish actual HTTP-origin acceptance, service-worker behavior, deployability, or external hosting.

In the execution environment used to make this archive, genuine Chromium navigation to both `http://127.0.0.1` and `file://` was blocked by administrator policy. The static server was reachable using command-line HTTP tools. Browser acceptance under a real served origin remains **NOT_TESTED**.

## Routing and persistence

The prototype uses hash-based routes such as `#/history/VI.4.2` to avoid requiring server rewrites on Python's basic HTTP server. Published deployment may later use real `/history/VI.4.2` routes. Browser-local state is stored using `localStorage` keys prefixed `korea-v1-`; it remains on the same browser origin and has no cloud sync.

## Known limitations and next stage

This phase is **not production-ready**. Full-text content search is not implemented (metadata-title search only). The section titles and terminal subsections are not written. The content pipeline is a small local proof of concept; there is no R2/D1/Workers integration, server-side indexing, account sync, translated corpus, image-license system, or actual million-word content store. There is no claim of archival accuracy for the sample prose.

Next: validate a true local Chromium HTTP run on the owner's machine, iterate reader feel, add substantive editorial sample volume, then develop content-pack ingestion, pagination, indexes, and an optional R2 storage adapter before generating millions of blocks.

## Policy / licensing

All prose in `data/articles` is an original illustrative draft created for this prototype. The supplied canonical architecture materials are copied from this project's files without alteration. The application intentionally has no external runtime packages or external image dependencies. No services were provisioned or deployed.

## Deployment preparation (15 October 2026)

This repository is intended for `thiepn/korea`. The publication-only build is generated with:

```bash
python3 scripts/build_release.py
```

For Cloudflare Pages, configure a Git-integrated project named `korea` on the Junsosmart account, `main` branch, with `python3 scripts/build_release.py` as build command and `dist` as output directory. The future `korea.thiepn.dev` domain is intentionally not configured. See `DEPLOYMENT.md`.

Unlike the editable full source, `dist/` includes only the page's 33 runtime files. The original canonical files are preserved separately in `canonical/`.

## Batch A — functional exploration feature branch (October 2026)

This branch expands Phase 1 without changing the canonical v1.1 archive. Dedicated Chapter routes, six themed collections, full-text sample search, and a richer Endless Reader are implemented. It now provides 17 original demo articles in 68 passages (8,672 words), not a million-word production corpus. All bookmarks and reading history remain private to the current browser.

**New routes:** `#/explore`, `#/collection/everyday-worlds`, `#/chapter/VI.4`, and existing `#/history/VI.4.2` and `#/part/VI`. All work using the static-host-friendly hash router.

**Rebuild after editing authoring sources:**

```bash
python3 scripts/build_packs.py
python3 scripts/build_exploration.py
python3 scripts/validate.py
python3 scripts/build_release.py
python3 tests/browser_smoke.py
python3 tests/batch_a_journeys.py
```

The `build_packs.py` manifest keeps words/checksums from `data/content-manifest.json`, so after adding a new article you must register its metadata there before compiling. `build_exploration.py` derives the searchable paragraphs and themed trail metadata. See `BATCH_A_REPORT.md` for detailed functionality and test limitations. Do not run `scripts/build_articles.py` to refresh the Batch A corpus; that original Phase 1 sample generator is intentionally preserved and would replace the manifest with its seven original demonstrations. Production `main` is unchanged; this work is an unmerged development branch.


## Batch B — scalable content platform (October 2026)

**Source of truth:** `data/articles/*.json` contains the editable original history texts; `canonical/` preserves v1.1 architecture byte-for-byte.
The original 10/100/1,000 historical IDs (and planned 10,000/100,000 descendant addresses) are untouched.

The site now downloads a compact **v2 article catalog + shard map** at startup rather than the original entire text index.
Full-text search retrieves only relevant `data/search/shards/*.json` files as needed, with a bounded in-memory cache.
Reading fetches compact content-addressed `data/packs/*.json` and reuses prefetched/loaded packs instead of fetching one network request per paragraph or downloading a huge whole-article file. These assets are deterministic: unchanged text produces unchanged URLs.

### Build

```bash
python3 scripts/build_release.py
python3 tests/batch_b_pipeline.py
python3 tests/batch_b_browser.py  # requires Playwright / Chromium
```

The release builder regenerates the v2 corpus, shard indexes and themed paths from original editable sources, runs full validation, and writes only allowlisted public files to `dist/`.
Cloudflare Pages continues to use `python3 scripts/build_release.py` and `dist`.

### Batch ingest

An import file contains one JSON object per line, e.g.

```json
{"id":"VI.4.2","mode":"append","blocks":[{"title":"A new extended passage","paragraphs":["A full paragraph of newly written history with enough explanatory detail to justify publication."]}]}
```

```bash
python3 scripts/ingest.py content/imports/example.jsonl --dry-run
python3 scripts/ingest.py content/imports/example.jsonl
python3 scripts/build_release.py
```

The importer verifies that IDs exist in the canonical source, prevents edits to published history under `replace`, detects ambiguous overlapping passage content, assigns monotonically increasing stable passage IDs and accepts exact replay without double-adding content. **It does not itself publish to GitHub or Cloudflare**, and a batch with several changed articles uses per-file atomic writes rather than a multi-file database transaction.

The starting Batch B import file lives in `content/imports/batch_b_editorial.jsonl`; its ten published new texts are also preserved under `data/articles`. All texts are original *illustrative editorial narratives*, not source-verified academic accounts.

**Scale boundary:** The compiler currently produces static files for Cloudflare Pages. When the pack/shard count approaches the Pages Free file cap, transition the same content-addressed artifacts to R2 without changing canonical IDs. Do not commit generated `dist`, pack or shard files as source; they are recreated by the Cloudflare build.

## Batch C — expanded original corpus and scalable reader

Batch C adds 50 human-authored editorial history samples (77 total entries, 258 passages, 24,137 original narrative words) without modifying the locked v1.1 canonical archive. New material has a homepage shelf and the seventh cross-era trail. These are explicitly labeled unverified editorial demonstrations, **not** completed historical research.

- Edit the source Markdown in `content/editorial/batch_c_volume_01.md`; run `python3 scripts/prepare_editorial.py <markdown> <import.jsonl>` **before** first import of an unpublished ID. The import tool deliberately refuses to overwrite published entries.
- Review the resulting `content/imports/batch_c_editorial.jsonl`, then `python3 scripts/ingest.py <import.jsonl> --dry-run` followed by the deliberate import.
- `python3 scripts/build_release.py` rebuilds deterministic pack and adaptive search assets in `dist/`. Do not commit `dist/` or generated `data/packs/` and `data/search/`.
- `python3 scripts/stress_corpus.py` tests one million-plus **synthetic** words in an isolated temporary directory without publishing them; synthetic numbers must never be counted as historical content.
- `python3 tests/batch_c_pipeline.py` and `python3 tests/batch_c_journeys.py` verify source identities and actual Chromium DOM behavior with in-memory assets.

See `BATCH_C_REPORT.md` for measured metrics and caveats.
