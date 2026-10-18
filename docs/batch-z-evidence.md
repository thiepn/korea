# Batch Z — Mongol invasions, Yuan world and Imjin War: provenance and qualification

## Ownership and frozen baseline

- Exact baseline: `f94378fce1e8b6b2425072487a02b68a608acedf`; 350 existing source articles, 2,467 immutable blocks, 345,793 source words, and 15 canonical v1.1 source Git blobs. Original article JSON SHA-1s are pinned in `tests/fixtures/batch_z_baseline.json`.
- Author-window snapshot: `65eda326054f0332e6509fbfbc60c062b50fec71` fixes the 20 new `V.9.1–V.9.10` and `VI.10.1–VI.10.10` articles. Each was entirely missing before Batch Z; no legacy article is expanded, and every original article and block remains byte-identical at publication.
- The baseline validator permits later *strictly append-only* extensions of old articles while forbidding any changed old block or metadata, and permits additions after frozen Batch Z passage windows without counting them in Batch Z's authored total. Canonical sources cannot change.
- The two Chapter scopes are disjoint: V.9 covers thirteenth-century Mongol–Goryeo warfare and Yuan relations; VI.10 covers the 1592–1598 Japanese invasions of Joseon and regional coalition warfare. Reader state, application runtime and source IDs are unchanged.

## V.9 — method and source criticism

- The Academy of Korean Studies' *Goryeo* overview: https://encykorea.aks.ac.kr/Article/E0003424 — places the 1219 alliance, 1231 invasion, 1232 transfer, continued campaigns, Choe fall in 1258, 1259 settlement, 1270 mainland return, 1273 suppression and Yuan-era royal marriage into chronological context. It is a modern specialist overview rather than contemporaneous testimony.
- AKS, *Ganghwa capital transfer*: https://encykorea.aks.ac.kr/Article/E0001532 — detailed account of strategic geography and dissenting readings of Choe leadership; its retrospective judgement is not an objective survey of all households.
- AKS, *Cheoinseong battle*: https://encykorea.aks.ac.kr/Article/E0055720 — emphasizes that low-status settlement residents and Buddhist defenders participated in the 1232 engagement, not merely Kim Yun-hu.
- AKS, *Sambyeolcho resistance*: https://encykorea.aks.ac.kr/Article/E0026605 — records the conflict over 1270–1273, including military institutions and contested anti-Mongol motives.
- UNESCO, *Tripitaka Koreana*: https://www.unesco.org/en/memory-world/printing-woodblocks-tripitaka-koreana-and-miscellaneous-buddhist-scriptures — a material and curatorial reference for the surviving war-era Buddhist canon; its preservation is not proof of every monk's political motives.
- Ganghwa County historical interpretation: https://www.ganghwa.go.kr/open_content/tour/tour/tourInfoDetail.do?tour_seq=114&tourdiv=all — local commemorative context, not a substitute for independent assessment of individual battles.

The manuscripts generally survive through later dynastic collections that privilege court and military elites. Numbers of soldiers and casualties are not treated as verified demographic enumerations; the writing avoids invented contemporary quotations, treats local civilians as partly invisible in the records, and distinguishes Yuan institutions of later decades from policy at the initial invasion.

## VI.10 — method and source criticism

- Jinju National Museum, *Imjin War Hall*: https://jinju.museum.go.kr/eng/html/sub02/020101.html — institutional material and textual contexts spanning Japanese invasion, local resistance, Yi Sun-sin, Jinju, refugee diaries and aftereffects.
- AKS, *Imjin War*: https://encykorea.aks.ac.kr/Article/E0047674 — interpretive synthesis of 1592–1598 campaigns, righteous armies and the East Asian setting.
- UNESCO, *Nanjung Ilgi*: https://en.unesco.org/memoryoftheworld/registry/498 — a surviving personal naval diary from Yi Sun-sin's perspective; not a complete campaign ledger or unbiased account of other commanders.
- AKS, *Jingbirok*: https://encykorea.aks.ac.kr/Article/E0055088 — Ryu Seong-ryong's retrospective attempt to explain failure and derive lessons, as participant memoir rather than impersonal official truth.
- Jinju National Museum, *Chronicle of a Refugee*: https://jinju.museum.go.kr/eng/html/sub02/0202.html?mng_no=120&mode=V — contextual exhibition around O Hui-mun's *Swaemirok*, whose elite-household witness cannot stand for all refugees.
- AKS, *Myeongnyang*: https://encykorea.aks.ac.kr/Article/E0018250 and *Noryang*: https://encykorea.aks.ac.kr/Article/E0012716 — late-war naval chronology, numbers and commemorative viewpoints, explicitly distinguished from source certainty.

Historical actors and sources did not share identical aims: Hideyoshi's expansionist policy, Ming security interests, Joseon dynastic survival, regional local defence and household survival are kept separate. The narrative does not invent casualty totals or convert naval legends into undocumented physical facts.

## Automatic release qualification

1. Exact prior 350 article blob identities (or full prefix plus metadata for future strictly append-only versions), 15 canonical blobs and frozen authored passage snapshot.
2. All twenty exact canonical titles and IDs; 20,000–30,000 original words by the source compiler's Python `WORD_RE`, no duplicate paragraphs, minimum 750 words per new article, valid cited source indices and 40+ evidence anchors.
3. Twenty Korean alias sets and exactly two ten-stop Chapter pathways, source-complete search, bounded content packs and shards, deterministic repeat compilation and public release allowlist.
4. Exact-head push and PR workflow passes, 1440/390/320-pixel Chromium acceptance against compiled assets and a real HTTPS Cloudflare branch preview discovered from the Cloudflare check at the *same exact SHA*. No preview URL may be assumed or fabricated.
5. Merge only after all checks conclude success, the base main SHA remains unchanged, and head SHA matches; verify Cloudflare production deployment at the final merge SHA. No manual deployment, migrations, credential changes or billable services.

**Editorial limitation:** These are original source-critical synthesis articles with selected contextual citation anchors, not a fully peer-reviewed academic monograph or a sentence-by-sentence independent source audit. Independent scholarly peer review remains NOT_TESTED.
