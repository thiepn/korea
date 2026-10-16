# KOREA Batch K — Complete Gojoseon Chapter and Evidence-Aware Historical Reading

## Ground truth and scope

- Remote baseline: `thiepn/korea` `main` commit `322dac0225dc022464f64215bd0632efee241e95`, Git tree `b6e53c0ab1ddd76964dddda1b1e0493d52ec1689`.
- The original architecture, all 15 `canonical/` files, and the ordered text of all **136 previously published articles** are unchanged. `tests/fixtures/batch_k_verified_baseline.json` contains SHA-256 fingerprints of those sources independent of Git history.
- Seventh complete Chapter: `II.1 — Gojoseon: Tradition, Archaeology, and the Earliest Korean State`.
- Seven new articles: `II.1.1`, `.3`, `.5`, `.6`, `.8`, `.9`, `.10`; three older articles deepened only by appended material: `II.1.2`, `.4`, `.7`.
- **9,331 actually written words, 55 new passages, 11 separately sourced passage annotations**. The three extended essays are `II.1.1` (2,209), `II.1.6` (2,218), `II.1.10` (2,137) counted by the site's compiler tokenizer; the other four new articles contain 558–594 words each and are not represented as monographs.
- Corpus: **143 articles, 660 passages, 91,600 narrative words**. Previous release: 136 articles, 605 passages, 82,269 words.

## Historical approach and source trust

This Chapter has high source uncertainty. The publication explicitly separates:

1. **Transmitted ancient claims** (e.g. Joseon/Yan diplomatic episodes in a *Weilüe* excerpt surviving via later *Sanguozhi* compilation; named officers in the *Shiji* accounts of late Gojoseon). Citing that passage directly establishes what the transmitted text says, not automatic proof of every reported event or its date.
2. **Excavated material and modern scholarly interpretation** (e.g. Liaoning daggers, burial types, disputed political assignments). These establish material and archaeological context, not the ownership of an entire kingdom simply from object shape.
3. **Medieval and Joseon-era memory** (Dangun in *Samguk yusa*; ritual treatment of Gija). These are excellent sources for historical memory and later state practice, not Bronze Age eyewitnesses.

Institutional research references:

- National Institute of Korean History, `고조선의 성장과 변화`, transmitted *Weilüe* excerpt: https://contents.history.go.kr/front/hm/view.do?levelId=hm_001_0020
- National Institute of Korean History, `고조선의 정치구조`, *Shiji* and transmitted *Weilüe* texts: https://contents.history.go.kr/front/hm/view.do?levelId=hm_001_0040
- National Institute of Korean History, `고조선의 위치와 강역`, competing geography: https://contents.history.go.kr/front/nh/view.do?levelId=nh_004_0030_0010_0050
- National Institute of Korean History, `단군`, medieval source chronology: https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_10&levelId=kc_n100800
- National Institute of Korean History, early Joseon historiography and ancestor rites: https://contents.history.go.kr/mobile/nh/view.do?levelId=nh_026_0020_0030_0010_0010_0010
- Academy of Korean Studies, Gojoseon and Liaoning bronze material: https://encykorea.aks.ac.kr/Article/E0003937 and https://encykorea.aks.ac.kr/Article/E0039316
- Academy of Korean Studies, `기자조선`: https://encykorea.aks.ac.kr/Article/E0008396

The eleven reader annotations offer direct/contextual source links at passage level. All unannotated prose is original explanatory synthesis, **not** independently peer-reviewed scholarship. Ancient capital, territorial, ethnic and founding-year disputes are explicitly qualified.

## Website integration

- Adds the fully published ten-stop `gojoseon-evidence-and-memory-complete` thematic route, for **19** curated paths.
- Adds **7** dated/thematic timeline landmarks, total **70**; period-only labels and the medieval compilation date are distinguished from exact Bronze Age foundation claims.
- Adds **12** explained contextual relationships, total **100**, linking neighbouring canonical topics and other published historical eras. No related-story links point to unpublished subjects.
- Adds Korean search aliases for all ten `II.1.*` IDs.
- Uses the unchanged Endless Reader, browser-local reading/bookmarks, original searchable pack/shard compiler, and original Cloudflare Pages deployment command.
- No new databases, storage services, credentials, paid infrastructure, or duplicate content engines.

## Executed qualification

- Original v1.1 validator: **PASS**, 10/100/1000 canonical architecture and virtual deeper descendants unchanged.
- Baseline source fingerprint validation for all 136 existing articles and all 15 canonical files: **PASS**.
- JSONL original importer replay dry-run: **PASS**, zero prospective rewrites after original import.
- Three 2,000+-word article checks, nonduplicated new paragraphs, source metadata, evidence-source indices: **PASS**.
- Deterministic build and zero unchanged asset rewrites: **PASS**.
- Chromium user-journey tests at 1440×900, 390×844, 320×720 with deterministic local assets: **PASS** for Chapter, route, passage evidence, Korean keyword search, timeline, return to prior Chapter, horizontal overflow.
- `node --check` on unchanged JS runtime modules; Python syntax checks: **PASS**.
- Release build: **807 public assets**, **2,066,285 bytes uncompressed**. Local measured build time **3.47 seconds**, peak process memory reported by `/usr/bin/time` **110,600 KiB** (not equivalent to Python traced allocations).
- Public HTTPS-origin browser acceptance: **NOT_TESTED** in this environment. Chromium DOM tests do not constitute an independent production-origin test.

## Remaining limitations

- **857 of 1,000** canonical Subchapters still have no published article, and much of the narrative corpus is shorter than the intended deeply immersive scope.
- The Gojoseon articles contain selective anchored sources, but are not reviewed claim by claim by independent Korean-history scholars. Some institutional articles themselves present contested positions.
- Korean morphological/Hanja search remains less complete than original English indexing; new aliases do not solve this structural limitation.
- No new account system, offline archive, or paid storage; R2/D1 not needed at present.
- Future extremely large content batches may require greater asset-count capacity planning and testing of real-world public HTTP performance.
