# KOREA — Interactive History Universe
## Product Vision and Technical Architecture (Draft v2.0)
**Date:** 2026-10-15  
**Status:** Proposal only. Does not replace or amend the locked Project Constitution v1.0 or Master Architecture v1.1.  
**Goal:** Build an exceptionally large, entertaining, navigable online history of Korea, expandable from 100,000 terminal topics to millions of narrative segments and hundreds of millions of words.

## 1. Product priorities
1. Content abundance, including long-form historical explanation and exploratory narrative.
2. Low-friction, interactive discovery and continuous reading.
3. A stable, familiar historical structure with unlimited append-only expansion.
4. Affordable hosting and scalable content packaging.
5. Automatic preparation, ingestion, publication, and quality checks.
6. Honest labeling of imaginative reconstruction; no requirement for article-by-article academic citations.

## 2. Preserve the original architectural investment
- Preserve the original ten Parts, 100 Chapters, 1,000 Subchapters, 10,000 Sections, and 100,000 terminal Subsections as the **baseline navigation taxonomy**.
- Keep historical canonical IDs (e.g., `VI.4.3.6.8`) stable.
- A terminal Subsection can contain unlimited `content_blocks`, `continuations`, `side_stories`, and `related_paths`. These are **publication objects**, not a renumbering of locked canonical structural levels.
- Millions of content blocks do not require millions of public HTML files, Markdown files, or build outputs.
- Any future change to the locked hierarchy requires an explicit constitution version and migration record; publication-layer expansion may proceed without redefining existing history IDs.

## 3. User experience
### A. Explorer landing page
- Visual clickable era strip; interactive ten-Part overview; quick entry points.
- Start at the beginning, continue a bookmark, browse a random interesting topic, explore a featured historical thread.
- Show breadth through counts and subject discovery, but never land new readers on an enormous 100,000-item list.

### B. Endless Reader
- Core distraction-free reader with Overview, Deep Dive, and Endless modes.
- Lazy-load content chunks (target 800–2,500 words per chunk, tunable; the underlying source file can be much bigger).
- Readers can continue to next local narrative block, follow a contextual detour, or progress to the next canonical subsection.
- Collapsible mini-outline, progress markers, font/width controls, bookmarks and resume-on-return.
- Pause and return to a linked detour without losing the original place.
- Accessibility: semantic headings, keyboard navigation, focus states, responsive mobile layout, reduced motion, optional disable-infinite-scroll.

### C. Knowledge Navigator
- Expandable Part → Chapter → Subchapter → Section → Subsection tree.
- Breadcrumbs, forward/back links, timeline, people/place/topic connections.
- Search and filtering by period, dynasty, theme, place, people, and content size.
- Contextual cards: 'What happened before?', 'What happened next?', 'Explore the everyday life', 'Related event'.

### D. Engagement without gamified distortion
- Reading path/history, topic rabbit holes, surprise discoveries, optional progress milestones.
- No forced sign-in, streak pressure, or live AI-generated claims during reading.
- Images/maps can be added later; initial UI must work beautifully as text-only.

## 4. Logical model vs. physical storage
### Logical object model
- `node`: canonical navigation unit `{id,parent_id,type,title,era,start_date,end_date,order}`.
- `article`: coherent editorial subject attached to node, can contain unlimited blocks.
- `block`: `{block_id,node_id,article_id,sequence,kind,title,body,word_count,source_pack,version,content_label}`.
- `link`: typed cross-reference between nodes or blocks (precedes, follows, same-person, same-place, alternative-angle).
- `reading_path`: ordered views through multiple canonical nodes and narrative blocks.
- `release_manifest`: snapshot IDs, checksums, active pack versions, index version, generation provenance.
- `status`: `planned`, `drafted`, `checked`, `published`, `revised` (for administrative progress only; no fake published material).

### Source files vs deployed assets
- Human/AI authoring: normalized JSONL/Markdown batches, possibly one source file per Section or Chapter.
- Build-time packaging: split very long source material into independently fetchable blocks or block bundles.
- Deploy packages by era/chapter/section using manifest references; revisions rewrite only affected packs.
- Visitors retrieve a few kilobytes of navigation metadata and the current reading chunk(s), not a 100,000-word file.
- Navigation IDs and article IDs are independent of physical file paths.

### Illustrative authoring path
`corpus/part-vi/chapter-04/section-03-06.jsonl` (not prescribed: physical grouping can change).  
`packs/VI/4/3/6/pack-000012.json.gz` (derived distribution asset).  
Canonical browser path: `/history/VI.4.3.6.8` (resolver maps ID to selected blocks).

## 5. Proposed infrastructure
### Phase A (functional prototype)
- **UI**: Astro website, with interactive React or framework-native islands only where needed.
- **Host**: Cloudflare Pages (static shell, landing pages, limited pre-rendered content).
- **Source of truth**: canonical architecture, application, schemas and tools in GitHub; preserve prior files unchanged.
- **Content**: local JSONL/Markdown batches; deploy small compressed content packs as assets.
- **Navigation/search**: manifest and metadata index (small initial scale), basic search.

### Phase B (large corpus)
- **Large content storage**: Cloudflare R2 Standard object storage, with custom-domain caching for public immutable content packs.
- **Dynamic routes and metadata query**: Cloudflare Worker; Cloudflare D1 for compact navigation/search metadata (not full text if it overflows practical database constraints).
- **Search**: title/description/tags first; scale to indexed block-level full-text search, potentially sharded or a dedicated service after measurements.
- **Delivery**: cache aggressively, content-address or version every pack, paginate metadata, lazy-load reading chunks.
- **Backups**: independent locally downloadable corpus snapshots, manifests, checksums; do not depend solely on R2 or Git history.

### Operational limitations to monitor
- Cloudflare Pages Free deployment static asset limit: 20,000 files per site; do **not** attempt one pre-rendered file per article.
- Worker Free: 100,000 requests per day across scripts, and CPU limits. Static/cached R2 content can reduce Worker load.
- R2 Standard Free: 10 GB-month storage, 1 million Class A operations and 10 million Class B operations monthly; beyond-free usage billed.
- D1 Free: 500 MB per database, 5 GB total across databases, 5 million rows read/day, 100,000 rows written/day; FTS5 support but indexing scale must be validated.
- Keep public HTML/routes indexable if search-engine discoverability matters; an exclusively client-rendered shell may limit crawling. Dynamic SSR or targeted pre-rendering can address this.

Official docs checked 2026-10-15:
- https://developers.cloudflare.com/pages/platform/limits/
- https://developers.cloudflare.com/workers/platform/limits/
- https://developers.cloudflare.com/r2/pricing/
- https://developers.cloudflare.com/r2/buckets/public-buckets/
- https://developers.cloudflare.com/d1/platform/limits/
- https://developers.cloudflare.com/d1/sql-api/sql-statements/
- https://developers.cloudflare.com/workers/framework-guides/web-apps/astro/

## 6. Scale estimates (illustrative, not storage guarantees)
Assume English raw text averages approximately 6 bytes per word including spaces, before indexing or assets.
| Text volume | Approximate raw text storage |
|---|---:|
| 10 million words | 60 MB |
| 50 million words | 300 MB |
| 100 million words | 600 MB |
| 1 billion words | 6 GB |
These estimates exclude markup, metadata, indexes, version history, backup copies, images, and serving overhead. Unicode language mix changes byte density.

**Primary challenge is content throughput and navigational coherence, not plain-text storage volume.**

## 7. Mass content generation system
1. Load canonical scope + immediate neighbors and active continuation records.
2. Select a content category (overview, narrative history, institutional detail, social life, region, biographies, contextual digression, comparison, interpretation, optional labeled imaginative reconstruction).
3. Build a small generator task (e.g., 1–5 narrative blocks) with stable destination IDs and prior continuation state.
4. Produce content and structured metadata; stage in drafts, not directly on the public website.
5. Automatically validate JSONL, IDs, chronological framing, duplicate titles, paragraph corruption, repetition, unsupported cross-references, and bizarre off-topic drift.
6. Label synthetic reconstruction and uncertain accounts. Do not invent quotations or documentary citations.
7. Approve at batch level; package and publish new/revised blocks with manifests and atomically switch active version.
8. Record throughput, content volume, duplication rate, cost, and broken link rate.

Quality philosophy: **quantity first, coherence second, rigorous historiography optional**. Avoid automated plagiarism, substantial repeated passages, nonsensical loops, and invented historical facts because they degrade reader experience even when academic accuracy is not the objective.

## 8. Milestone gates
**M0:** Preserve original canonical v1.1 files, recover available Part I work, snapshot.
**M1:** Build an authentic 10-Part explorer + navigation tree with all 100,000 baseline IDs represented as PLANNED (not falsely claimed as written).
**M2:** Ship a polished reader with modes, lazy loading, progress, bookmarks, history, related links; demonstrate 100,000+ words with realistic content.
**M3:** Build source ingest and content pack compiler, automatic validation, versioned release manifests, recoverable backups.
**M4:** Confirm a 1-million-word load and navigate/search performance, then move corpus delivery to R2 as appropriate.
**M5:** Progressively reach 10M, 50M, 100M+ published words only if costs, generation rate and UX remain acceptable.

## 9. Decision summary
- Do **not** shrink the original 100,000-subsection baseline.
- Do **not** generate a million static HTML pages or a million physical source files.
- Do **not** use a typical static documentation website as the only long-term experience.
- Do **not** make academic footnotes or source reviews the bottleneck.
- **Do** build the reader and explorer first, then an automated data engine that feeds them.
- **Do** use stable IDs, independent content blocks, versioned packed storage, and clear planned/published states.
- **Do** deliberately support long, enjoyable content paths with progressive loading and contextual navigation.

**Next implementation phase:** a local interactive Explorer + Reader proof-of-concept using real v1.1 architecture records and a small number of populated narratives; no Cloudflare or GitHub writes until reviewed.
