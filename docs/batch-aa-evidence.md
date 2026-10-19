# Batch AA — Goguryeo formation and northern kingdom: evidence and release qualification

## Scope and ownership

- Main baseline: `dc4fa7f738c32c06eda3870563b85b5f2430723d`, comprising **370 published articles**, **15 canonical files**, **366,110 historical prose words** and **2,663 passage blocks**.
- Target chapters: **II.5 — The Formation of Goguryeo** (formation, settlement, frontier contacts to c. 300 CE) and **III.1 — Goguryeo: The Northern Kingdom** (internal royal and territorial changes from the early fourth century through Yeon Gaesomun).
- Exactly **20 target article IDs**; **17 originally absent articles created** and **three preexisting articles enlarged strictly by appending passages** (`II.5.2`, `III.1.4`, `III.1.5`). Frozen authored narrative snapshot `2dbb2a5b3a2a7461400e0151bc0f6d161dc4f8f1`. This is an immutable content snapshot, not a production release claim.
- **20,394 candidate newly authored words** in the JavaScript manuscript prescreen and **182 new immutable passages**; the Python `WORD_RE` gate in the exact-head CI is authoritative and requires 20,000–30,000.
- Each target article has at least three searchable Korean aliases. Two ten-stop chapter pathways connect exact II.5 and III.1 canonical IDs without rearranging existing routes.
- **Non-ownership**: II.5 cannot narrate the mature fourth-century kingdom as its primary history, and III.1 cannot preempt III.10's detailed interstate and final-war chronology. Founding narratives are categorized as traditions, not proof of a modern ethnic origin.

## Source families and interpretive cautions

- **Academy of Korean Studies, *Goguryeo* (고구려)** — https://encykorea.aks.ac.kr/Article/E0003323. Broad reference for early royal succession, frontier policy, changing regional power, institutional chronology, and contested reconstruction. A specialist synthesis is not a contemporary royal administrative ledger.
- **Academy of Korean Studies, *Dongmyeongseongwang* (동명성왕)** — https://encykorea.aks.ac.kr/Article/E0016431. Context for Jumong/Chumo foundation traditions, names and retrospectively transmitted genealogy. Not proof of a literally witnessed miraculous origin.
- **Academy of Korean Studies, *Yeon Gaesomun* (연개소문)** — https://encykorea.aks.ac.kr/Article/E0036672. Describes the 642 seizure of power and its later narrative transmission, including the influence of Chinese writing on surviving biographical details.
- **Academy of Korean Studies, *King Bojang* (보장왕)** — https://encykorea.aks.ac.kr/Article/E0023525. Reference for royal enthronement after 642, constrained monarchy and divergent later assessments.
- **National Institute of Korean History, *Goguryeo and Former Yan: conflict and crisis*** — https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_013_0120. Differentiates mid-fourth-century political pressure, later chronicles and the state-building response.
- **National Institute of Korean History, *Sosurim's reconstruction*** — https://contents.history.go.kr/front/hm/view.do?levelId=hm_009_0030. The transmitted *Samguk Sagi* entries for 372 reception of Buddhism and Taehak, and 373 promulgation of statutes. These notices do not preserve a complete law code, school syllabus or evidence of universal Buddhist conversion.
- **National Institute of Korean History, *Pyongyang relocation and southward advance*** — https://contents.history.go.kr/mobile/hm/view.do?levelId=hm_009_0050. Annotated later textual evidence for 427 capital relocation and the 475 Hanseong campaign. Reported troop totals in chronicles are not uncorroborated census-grade quantities.
- **National Institute of Korean History, *Samguk Sagi geography and capital chronology*** — https://db.history.go.kr/ancient/level.do?levelId=sg_037r_0020_0030. Later compilation of capital names and dates, including 586. Complex sites in greater Pyongyang require archaeology to distinguish building phases.
- **Korean Citation Index, Park Jong-seo, 2023**, *King Jangsu's entry into the Han River basin and operation of southward routes*, https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002932690. Scholarly alternative to a simplistic one-route/one-border reading of southern occupation.
- **Korean Citation Index, 2024**, *Goguryeo's loss of the Han River basin in the mid-sixth century*, https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART003123574. Source for reconsidering 551–553 frontier shifts; neither scholarship nor chronicles allow a permanently static territorial map.
- **UNESCO World Heritage Centre, *Capital Cities and Tombs of the Ancient Koguryo Kingdom*** — https://whc.unesco.org/en/list/1135. Archaeological and heritage context for Huanren, Ji'an, royal capitals, burials and monuments. Individual excavated features are not all attributable to specific dated raids.
- **UNESCO World Heritage Centre, *Complex of Koguryo Tombs*** — https://whc.unesco.org/en/list/1091/. Visual and funerary context; tomb paintings primarily document elite commemorative representation, not direct evidence of every household's beliefs or a complete political census.

## Principal research risks

1. **Foundation traditions**: mythic and traditional episodes about Jumong, Buyeo kinship and Jolbon must never be identified automatically with dated excavation layers or modern ethnicity.
2. **Third-/fourth-century transition**: II.5.10 is the transition to a mature kingdom; III.1 owns actual post-300 restructuring. III.1.2 treats the commandery aftermath, not a retelling of II.3 commandery institutions.
3. **Gogukwon**: 342 Former Yan invasion and 371 Baekje confrontation are broadly evidenced in later compilations, but capture narratives, victim totals, royal motive and site-level military detail remain source-sensitive.
4. **Gwanggaeto stele**: royal epigraphy commissioned under Jangsu in 414; readings of Wa-related passages and modern Korean/Japanese political claims are not the same as inscriptional fact.
5. **Administration and society**: fortress networks, tribute and royal titles cannot be used to fabricate a uniform cadastral bureaucracy or presumed testimony from ordinary households.
6. **590–668**: Sui/Tang diplomacy and the 642 coup are political background here; detailed military campaign chronology and the state's fall belong to Chapter III.10.
7. **Evidence anchors**: contextual links attached to new passage blocks document a recoverable reference family, not sentence-by-sentence primary-source verification. Earlier articles' unchanged metadata and passages remain explicitly unreviewed where originally unsourced.

## Release gates and remaining limits

- Verify all **370 prior source Git blobs** against the pinned baseline, permitting only strictly append-only future extension with byte-identical historical block prefixes and metadata. Verify all **15 canonical blobs** unchanged.
- Verify the exact frozen Batch AA passage window on every target, including the three prior passages' source identity and original `release` value, all twenty canonical titles, 17 new article files, 182 new passages, and at least 80 contextual evidence anchors.
- Validate the source compiler's 20,000–30,000-word gate, passage naming/order, duplicated prose, valid evidence locators, all 20 Korean aliases, exact two ten-stop routes, old route preservation, deterministic sharded build and allowlisted release.
- Run 1440/390/320-pixel Chromium acceptance on generated assets and the **real HTTPS Cloudflare Pages preview URL extracted from a successful exact-SHA Cloudflare check**. Never invent a preview URL.
- Only squash merge after exact-head push/PR Actions, Cloudflare preview and unchanged main pass; then verify the resulting production commit/deployment. No manual deployment, migrations, credentials or paid external services.

**Editorial state:** original interpretive publication draft, **not specialist peer-reviewed**. Where claims depend on inscriptions, later chronicles, excavations or disputed territorial reconstructions, the account preserves that evidentiary distinction.
