# KOREA Batch L — Opening Korea and the Treaty-Port World

## Baseline and source preservation

- GitHub `main` at the start: `4113b91000fdb9c0f854146f16c85a80e9f25c26` with Git tree `67716a6c4880d67fc317be99be53ef6ff6351737`.
- All fifteen source files in `canonical/` remain byte-identical to the baseline.
- All 143 previously published articles have their original paragraphs in the same order. Three (`VIII.1.1`, `.2`, `.5`) have **one new appended passage**, while all other 140 previous article files are byte-identical. The original titles, source metadata, and passage identities of the three append targets are unchanged.
- `tests/fixtures/batch_l_prior_bytes.json` is a source snapshot fingerprint independent of local Git history.
- No architecture changes, no new numbered canonical IDs, no browser-local state migration, no paid storage or database resources.

## New authored historical material

Seventh earlier complete Chapters retained. **Eighth complete Chapter:** `VIII.1 — Opening Korea and the Treaty-Port World`.

- 7 entirely new articles: `VIII.1.3`, `.4`, `.6`, `.7`, `.8`, `.9`, `.10`.
- 3 append-only expansions: `VIII.1.1`, `.2`, `.5`.
- 66 new passages, **9,055 newly written words** using the existing `build_corpus.WORD_RE` standard.
- Deep independent essays: Japanese merchants and jurisdiction (`VIII.1.3`, 2,021 words); intellectual reform debate (`VIII.1.7`, 2,022 words); U.S. treaty of 1882 (`VIII.1.9`, 2,057 words). All three exceed 2,000 authored words **without** counting previous text.
- Other entries address tariff/trade systems, Qing military technical learning, Qing–Japan–Russia strategic discussion, and differentiated social consequences of opening. These four are ~620–650 words, not mischaracterized as long-form monographs.
- Corpus: **150 published articles, 726 independently loadable passages, 100,655 narrative words** versus 143 / 660 / 91,600 in Batch K.

## Evidence and interpretation

Nineteen specific passage annotations link factual assertions to Korean institutional source pages and a primary-text transcription. Examples:

- National Institute of Korean History: `조미 수호 통상 조약`, primary Chinese treaty transcription including May 22, 1882, named parties, and first two clauses: https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_115_0060
- National Institute of Korean History: pre-opening regional trade routes, grain exports and the 1876 shortage: https://contents.history.go.kr/mobile/km/view.do?levelId=km_026_0060_0010_0010_0010 and https://contents.history.go.kr/mobile/km/view.do?levelId=km_026_0060_0010_0010_0020
- Academy of Korean Studies: `영선사` mission and technical training: https://encykorea.aks.ac.kr/Article/E0037460
- Academy of Korean Studies: `조선책략` and its strategic debate: https://encykorea.aks.ac.kr/Article/E0052228
- Academy of Korean Studies: `통리기무아문 관제`: https://encykorea.aks.ac.kr/Article/E0005000
- Academy of Korean Studies: `천진담초`, historical description of contemporary Kim Yun-sik diplomatic records: https://encykorea.aks.ac.kr/Article/E0056056

**Source limits:** Institutional encyclopedia entries are secondary scholarship; transcribed treaty clauses witness what negotiators wrote, not the actual future performance of state obligations. A source describing a primary manuscript is not identical to our own independent inspection of its every folio. Where accounts disagree on Yeongseonsa participant totals, this edition avoids inventing a single uncontested number. No historical claim of guaranteed U.S. military assistance is inferred from the friendly-offices language. Much interpretive prose is original editorial synthesis, **not claim-by-claim peer reviewed**. Full Korean/Hanja search remains incomplete.

## Website integration

- Complete ten-stop reading route `opening-korea-treaty-ports-complete`, while retaining all earlier routes (20 now).
- 8 dated historical landmarks (78 total), source-authored to avoid falsely precise historical timing.
- 16 explained, published-to-published connections (116 total), including comparisons to earlier markets, knowledge systems and later diplomatic history.
- Korean search aliases for all ten Chapter VIII.1 entries (no new search engine or database).
- Existing source-first compiler, immutable bounded content packs, lazy index, Endless Reader, reader-window restoration, bookmarks and saved reading positions unchanged.

## Executed verification

- Exact baseline source tree, immutable canonical files and existing article paragraph prefixes: **PASS**.
- Replay-safe JSONL import, new document uniqueness, canonical IDs, evidence index integrity: **PASS**.
- Python syntax, JavaScript syntax, original v1.1 validator, deterministic pack/shard compiler, full release build: **PASS**.
- Chromium at 1440×900, 390×844 and 320×720 with real DOM interactions and deterministic local built assets: **PASS** (Chapter route, evidence links, Korean search, chronology, navigation back to older Chapter, no horizontal overflow).
- Release build: **881 public runtime assets, 2,245,352 bytes before compression**; editable sources / canonical files excluded.
- Public HTTPS-origin browser acceptance: **NOT_TESTED** in local Chromium because navigation outside the deterministic asset harness is not available.

This report records implementation and qualification; use GitHub and Cloudflare APIs for the separate PR merge/deployment verification. Do not infer production success from these local tests.
