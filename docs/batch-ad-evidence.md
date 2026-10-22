# Batch AD — Goryeo learning and Joseon Neo-Confucian intellectual order

## Exact editorial ownership and protected base

- **Frozen authoring baseline:** `88489f7595567c6bc09f8ef71d0402c139d519f5`. Original corpus: **423 published article files, 3,237 immutable passage objects and 427,737 history words**, protected by Git blob hashes in `tests/fixtures/batch_ad_baseline.json`. Protect all **15 canonical v1.1 source files** without any editing.
- **Chapter V.6:** Goryeo learning, poetry, books, the historical compilations *Samguk Sagi* and *Samguk Yusa*, metal-type Jikji, Tripitaka Koreana, celadon, painting, built arts, scholarship and technical practices. Do not replace Chapter V.2 government or V.9 Mongol war narratives; the latter supplies historical context only.
- **Chapter VI.3:** Early Joseon Neo-Confucian learning, Jeong Do-jeon, Gwon Geun, royal ideology, state education, exams, family rites, the Sarim, Seowon, literati purges, Toegye and Yulgok. Chapters VI.1 and VI.2 own the founding dynasty's political/military and bureaucratic history; the intellectual chapter focuses on ideas, scholarly institutions, and political interpretation, not duplicate reign-by-reign narrative.
- **Manuscript snapshot:** `f9eb6a6b9af4a9275ef03a52ebe919dd94d200cc`; eighteen first-published source articles and strict append-only expansion of `V.6.5` and `VI.3.4`. The three old passages and preexisting metadata in each must match the baseline exactly. New passages carry independent IDs. Prescreen **20,139 newly authored words, 196 new blocks, 90 contextual anchors**; Python `WORD_RE` is authoritative.

## Documentary source families

**Goryeo learning and textual culture**
- NIKH: `Gukjagam` — https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_o200200 . Basis for 992 restructuring, school access, shifting royal policy and the caution that transmitted curriculum rules may not correspond exactly to actual admissions.
- NIKH: `Twelve Private Academies` — https://contents.history.go.kr/mobile/tg/view.do?ganada=&levelId=tg_002_0670&pageUnit=10&subjectCode=tg_ty_090&tabId=02 . Choe Chung's nine halls, network of private teachers, and limitations on claims about all students.
- NIKH: `Samguk Yusa` — https://contents.history.go.kr/mobile/kc/view.do?code=kc_age_20&levelId=kc_r200345 . Preserved thirteenth-century Buddhist historical compilation, disputed layers of authorship and retrospective foundation traditions. **The age narrated by a legend must never be equated with the date of the surviving version.**
- UNESCO Memory of the World: `Printing woodblocks of the Tripitaka Koreana` — https://www.unesco.org/en/memory-world/printing-woodblocks-tripitaka-koreana-and-miscellaneous-buddhist-scriptures . Exactly 81,258 blocks commissioned in the 13th century. Textual collation and preservation, not a tally of modern mass readership.
- UNESCO Memory of the World: `Jikji` — https://www.unesco.org/en/memory-world/baegun-hwasang-chorok-buljo-jikji-simche-yojeol-volii-second-volume-anthology-great-buddhist-priests . The surviving 1377 Heungdeoksa printed witness establishes the **oldest surviving book made using movable cast metal type**, not proof that no earlier metal type experiment existed.
- UNESCO WHC: `Haeinsa Janggyeong Panjeon` — https://whc.unesco.org/en/list/737 . **15th-century extant storage buildings** contain **13th-century Goryeo blocks**; never merge their construction dates.
- Metropolitan Museum of Art: `Goryeo Celadon` — https://www.metmuseum.org/it/essays/goryeo-celadon . Southwestern kilns, twelfth-century sanggam and technical ceramics; distinguish museum masterpieces from ordinary household possessions.

**Joseon Neo-Confucian intellectual order**
- AKS: `성리학` — https://encykorea.aks.ac.kr/Article/E0029308 . Development of Zhu Xi learning, Jeong Do-jeon's political and Buddhist critiques and changing royal ideology.
- AKS: `도학` — https://encykorea.aks.ac.kr/Article/E0015909 . Jeong Do-jeon, Gwon Geun, Jeong Mong-ju, Kim Jong-jik, scholarly transmission and the dangers of a simple ideological-destiny narrative.
- NIKH: `사림` — https://contents.history.go.kr/front/tg/view.do?levelId=tg_003_1140&treeId=0100 . Historiographical distinction: `Sarim` as a distinctive political group developed especially under Seongjong; not a permanently organized party from the founding of the dynasty.
- NIKH: `Jo Gwangjo` — https://contents.history.go.kr/front/kc/printViewPopup.do?levelId=kc_i301600 . Court reform, royal support and the 1519 crisis; distinguish political speech from confirmed private motives.
- NIKH: `16th-century Neo-Confucian debate` — https://contents.history.go.kr/front/km/view.do?levelId=km_024_0040_0010_0070 . Toegye–Gi Daeseung Four–Seven correspondence and Yulgok scholarship; do not flatten li and qi into modern matter-vs-idealism labels.
- UNESCO WHC: `Seowon, Korean Neo-Confucian Academies` — https://whc.unesco.org/en/list/1498/ . Heritage landscape for academy history; visible buildings may have later repair phases and cannot prove uniform teaching practice.

**Critical boundaries:** Historical texts written centuries after the events are not contemporary transcripts. Monastic miracles, foundation legends and retrospective philosophical lineages must remain qualified. Record the difference between institutional rules and actual access, the ideal of morally restrained government and coercive politics, and normatively prescribed family rites versus household practice. Elite text and material sources cannot supply invented individual narratives for women, craftspeople, farmers or most students. School membership does not imply equal access. For the 1498, 1504, 1519 and 1545 purges, avoid a false homogeneous Hungu-versus-Sarim morality play; discuss the particular court succession and accusation evidence.

## Release gates and constraints

1. Before merge compare `main` to requested baseline. At Batch AD start `main` was **35a51ed9618e2ec95b5fa88c49ccf22d8514388a**, one commit ahead of `88489f7...`, adding `AGENTS.md`. **Do not silently treat this as unchanged main**, and do not merge until the user's exact base condition has been addressed.
2. Compare all 423 old source file Git blob identities and all 15 canonical Git blobs. Only the two named existing articles may receive append-only blocks, leaving source prefix and original metadata identical.
3. Require 441 total article source files, 3,433 total passages, original authoring snapshot, 196 newly sequenced passage IDs, 18 newly written articles with a minimum 750 words each, and >=20,000 <=30,000 original narrative words from the project's Python compiler. Detect duplicate paragraphs, short passages, malformed evidence and mismatched canonical titles.
4. Preserve all existing search aliases and guided routes. Add Korean aliases for each target ID and exactly two new ten-stop reading paths in the original exploration generator.
5. Run deterministic build twice, bounded packs and shards, public asset allowlist, Node syntax and real Chromium generated assets plus real Cloudflare branch preview at desktop 1440 and mobile 390/320 px. Discover preview URL only from the successful same-head SHA check; never infer the hostname.
6. Do not merge, deploy manually, apply migrations, touch credentials, change payment plans or write production user data. Production deploy is automatic only after a permitted squash merge; then check the deployment's exact commit SHA.

**Review status:** Original source-critical historical draft with selected institutional contextual anchors; independent specialist historical peer review **NOT_TESTED**. Automated QA is not a substitute for close citation verification.
