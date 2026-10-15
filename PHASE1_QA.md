# KOREA Interactive Universe — Phase 1 QA

**Date:** 2026-10-15  
**Artifact:** Local, undelivered preview application. **No production deployment or paid services.**

## Proven results

| Gate | Result | Evidence |
|---|---|---|
| Structure preservation | PASS | 10 Parts, 100 Chapters and 1,000 distinct Subchapter IDs extracted from uploaded canonical v1.1 files |
| Deeper addressing | PASS | Section and terminal addresses generated virtually at 10-by-10 per canonical Subchapter; no fabricated titles |
| Sample narrative integrity | PASS | Seven sample articles, 4,488 words, 28 independently fetchable JSON chunks with verified SHA-256 |
| HTTP static responses | PASS (CLI) | 200 for HTML, application JS, canonical navigation JSON, manifest and sample block from local Python HTTP server |
| JavaScript syntax | PASS | `node --check app.js` |
| Chromium DOM/layout | PASS (in-memory harness) | Explorer, reader, search, planned IDs, bookmarks, modes and progressive passages at 1440×900, 390×844, 320×720 and 844×390 |
| Mouse search + mobile drawer | PASS (in-memory harness) | Search input, click-through search result, mobile navigation to Part VI |
| Endless progression | PASS (in-memory harness) | 28 story chunks across 7 sample topics, 6 transitions, final bounded-sample exit |
| Contextual detour and resume | PASS (in-memory harness) | Return to former reading position; resume previous page progress after leaving and returning |
| Canonical file preservation | PASS (spot comparisons) | Original copied constitution, master registry, and sampled Part files byte-identical to uploads |
| Actual HTTP-origin Chromium acceptance | **NOT_TESTED** | Browser navigation blocked by administrator policy for loopback HTTP and local-file URLs |
| Real CDN, PWA, deployment, remote storage | **NOT_TESTED** | Intentionally out of Phase 1 scope |

## Known limitations

- Reading samples cover seven Subchapters only. The remaining nodes are clearly marked planned.
- `Overview` lists article passages and a short introduction; it is not an independently researched abstract.
- Search indexes canonical IDs and topic titles; it does not search full narrative text.
- Reader chunking is network-per-passage, but runtime data is a local manifest and JSON files, not Cloudflare R2.
- Initial browser storage is per-origin and does not provide cross-device sync.
- Article prose is prototype demonstration text, not a sourced historical reference edition.
- Fonts use system sans-serif/serif fallbacks; no remote assets or external packages are required.
- No actual production hosting, R2/D1/Workers, or service worker was configured.

**Recommended user acceptance:** Serve the extracted archive locally and exercise desktop/mobile using a real HTTP origin (e.g. `http://localhost:8000`), then refine readability before increasing the corpus size.
