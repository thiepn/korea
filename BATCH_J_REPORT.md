# KOREA Batch J — Silla Society: A Complete Sixth Chapter

## Source and preservation

- Source baseline: GitHub `main` commit `cd5bb8db15bbdd8f3f0dfb7f1cd5e0dc73913df9`, verified exact Git tree `2d4799d56dfa2935e5415d863b614e29edca6d01`.
- The preserved source snapshot was unpacked and validated by rebuilding that exact Git tree. Canonical v1.1 ID titles, architecture, ownership, and all original governance files remain byte-for-byte unchanged.
- `tests/fixtures/batch_j_verified_baseline.json` contains SHA-256 fingerprints for every prior canonical source and the existing ordered passages and identities of all 129 earlier articles. The test is independent of shallow checkout history.
- All three already-published Chapter IV.3 articles receive **append-only passages**. All prior passages and source references remain exactly intact.

## New authored text

- Sixth fully readable Chapter: `IV.3`, Silla Society, Economy, and Everyday Life, with all ten canonical Subchapters and a ten-stop themed reading path.
- Seven newly written source-first articles: `IV.3.2`, `.5`, `.6`, `.7`, `.8`, `.9`, `.10`; three prior articles deepened: `IV.3.1`, `.3`, `.4`.
- Genuine Batch J manuscript text: **9,450 counted words across 56 newly authored passages**. This is not synthetic benchmark material.
- Deep treatments: `IV.3.2` (2,115 new words), `IV.3.5` (2,154 new words), `IV.3.7` (2,049 new words). Other newly authored entries are shorter (about 560–625 words), and are not described as full monographs.
- Corpus after release build: **136 published articles, 605 passages, 82,269 narrative words**. No earlier article replaced.

## Provenance and interpretive boundaries

- Ten specific reference annotations link claims to source locators and differentiate **direct** documentary support from **contextual** institutional explanation; editorial passages are not certified as independently peer-reviewed.
- The Silla Village Register (`신라촌락문서`) is a rare state fiscal source surviving as reused paper; it covers four communities near Seowongyeong, *not* a full population survey. Its date remains contested. Relevant primary-text transcription: [National Institute of Korean History](https://contents.history.go.kr/front/hm/print.do?levelId=hm_033_0050&tabId=03&treeId=010302&whereStr=).
- Commercial and maritime anchors include [Cheonghaejin, 828](https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_10&levelId=kc_r101460) and [Jang Bogo / Jeongnyeon source transmission](https://contents.history.go.kr/front/hm/view.do?levelId=hm_034_0040). The biography is transmitted through later compilers, not an unfiltered eyewitness statement.
- A [Samguk sagi source passage](https://contents.history.go.kr/front/hm/view.do?levelId=hm_020_0110) supports the retrospective Gabae/weaving tradition, not a contemporaneous observation of every Silla settlement.
- [Donggung and Wolji](https://contents.history.go.kr/mobile/eh/view.do?code=ganada&levelId=eh_r0090_0010) materials document an elite archaeological context, not representative everyday housing. All imagined individual dialogue is omitted.

## Connected discovery and architecture

- A new `silla-everyday-life-complete` ten-stop reader path is compiled by the existing pathway builder; total curated collections: **18**.
- Six *labeled* atlas points were added, with disputed or thematic chronology marked honestly; total atlas landmarks: **63**. In particular, the village register is NOT assigned an invented exact composition date.
- Fourteen explained contextual connections now tie social class, villages, agricultural production, trade, urban archaeology, wellbeing and festival culture to earlier Chapters; total connections: **88**.
- Korean search aliases added or extended for all ten `IV.3` subjects. One-character aliases were removed because the current search compiler explicitly requires tokens of length ≥2.
- No changes to account boundaries, personal bookmarks, reader-window engine, dynamic runtime APIs or paid services.

## Local qualification

- v1.1 validator: **PASS** (10 Parts, 100 Chapters, 1,000 registered Subchapters; virtual reserved IDs maintained).
- Source-first deterministic builder: **PASS**, 137 content-addressed packs, 596 bounded search shards and 745 public allowlisted assets, approx. 1.90 MB uncompressed.
- Immutable baseline fingerprints for all 129 original articles and 15 canonical source files: **PASS**.
- Replay-safe importer, no unchanged asset rewrites, bounded pack size, new manuscript minimum-depth and paragraph uniqueness: **PASS**.
- Chromium desktop 1440px and mobile 390px/320px: **PASS** for complete Chapter, 10-stop route, evidence expansion, Korean search, timeline and no overflow under tested journey, through deterministic local content responses.
- Existing Batch B/C/D/E pipeline regressions: B, C, D, E **PASS** after repairing one exact-five-passage assumption in the D regression.
- Original old F/G/H/I pipeline tests need earlier historical Git commits not provided in the source archive; those checks are **NOT_TESTED** in this source-only workspace. Equivalent preserved-content and current workflow checks run through the Batch J fixture. Legacy browser scripts contain historical exact article-word and collection-count assumptions; don't count them as live product failures without reproducing the UI defect.
- Public HTTP(S)-origin Chromium acceptance: **NOT_TESTED** pending an authorized browser/preview environment. Deterministic DOM tests do not establish deployment success.

## Remaining gaps

- 864 of 1,000 canonical Subchapters have no published article; most of the 136 readable entries are brief compared with the desired long-form historical library.
- Historical documentation is selective. Corroboration from Korean primary sources, alternative scholarly interpretations and independent review remain incomplete.
- Full Korean morphological, Hanja, synonym and cross-language search are not implemented.
- The compiler's static asset count and source generation workflow will need capacity planning at genuinely massive scale. No new storage infrastructure added.
