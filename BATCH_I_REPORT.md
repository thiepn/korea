# KOREA Batch I — Long-Form Historical Expansion

## Baseline and preservation

- Remote `thiepn/korea` main verified at `86ed92e103907cb2d124bbcac2949b57600fa197`, Git tree `ec71b237ed22269bb10e79c544f6f3198b032e2f`.
- Source archive reconstructed at the same exact Git tree. No canonical `v1.1` files modified.
- Every earlier article retains its ID, title, exact previous ordered blocks and source metadata; six entries are append-only.
- The build uses the existing source-first JSONL importer, hash-addressed packs, lazy full-text search and current Cloudflare Pages pipeline; no new framework or database.

## Human-authored content

- Eight new canonical Baekje articles complete Chapter `III.2` alongside its previously published `III.2.2` and `III.2.5`.
- Six append-only earlier articles deepened: `III.2.2`, `III.2.5`, `III.3.6`, `VI.4.3`, `IX.1.6`, `IX.3.3`.
- Original writing: **9,821 word tokens under the production corpus counter**, **61 new immutable passages**.
- Resulting corpus: **129 articles / 549 passages / 72,819 words**.
- New 2,000+-word treatments: `III.2.1` (2,008), `III.2.6` (2,120), `III.2.8` (2,107). Other new chapters are shorter 372–934-word treatments; do not label them as monographs.
- Edited manuscripts: `content/editorial/batch_i_baekje_collection.md`, `content/editorial/batch_i_deepening.md`; immutable import JSONL is reproduced by `scripts/prepare_batch_i.py`.

## Documentary limits

- Twelve passage-specific evidence entries identify claim, source, locator and source role (`direct` versus `context`). Sources include the primary Muryeong tomb inscription via NRICH, the National Institute of Korean History, UNESCO, the Academy of Korean Studies, and the National Museum of Korea.
- The 1971 tomb discovery, 523 king's death, 525 burial, 475 Hanseong crisis, 538 Sabi move and 660 monarchy collapse have specific institutional contextual support. The conclusions concerning class, social life, state-building, or individual intentions remain editorial interpretation, often without local direct testimony.
- Several late chronicles and older textbook accounts are retrospective; institutional hosting is not proof that a late narrative is contemporary eyewitness evidence.
- No source text or images were copied into the narrative; references link to institutional pages. This is not a comprehensive peer-reviewed or claim-by-claim verified history.

## Connected reading

- Fifth complete ten-stop Chapter pathway: `baekje-river-maritime-complete`.
- Seventeen total curated collections, 57 dated atlas landmarks, 74 explained inter-article relationships.
- New Korean aliases for Baekje archaeology, rulers, capital relocations, and 660.
- Existing local bookmarks, reading progress, bounded DOM reader window, and content-pack retrieval are unchanged.

## Checks performed

- Deterministic source-first compiler and v1.1 validator PASS: 679 publishable assets, 1,733,055 uncompressed bytes, 130 immutable packs, 537 search shards.
- Source preservation and previous-paragraph exact-prefix comparison against the verified local baseline PASS.
- Import idempotence/replay, deterministic pack hashes, no unnecessary asset rewrites PASS.
- Chromium DOM interactions with deterministic content responses PASS at 1440×900, 390×844 and 320×720, including 5-Chapter navigation, full reading route, source disclosure, Hangul search aliases and mobile overflow checks. Existing H Chapter journeys also PASS after updating the fixed collection count assumption.
- Public HTTPS-origin browser acceptance NOT_TESTED (previous local-origin Chromium restrictions); deployment success cannot substitute for this test.
- No R2/D1/paid resources, no custom-domain changes, no production writes outside automatic GitHub-linked Cloudflare Pages deployments.

## Outstanding gaps

- 871 of the 1,000 canonical Subchapters still lack published articles.
- Only a minority of articles have sustained multi-thousand-word narratives; this expansion is substantial but the total corpus remains far below one million words.
- Korean morphological / Hanja search, deeper comparative primary scholarship, broader social perspectives, and independent historical review remain incomplete.
