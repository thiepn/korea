# Batch V — Goryeo society and Korean Empire source audit

## Canonical scope and release preservation

- Immutable published baseline: `33290b07049f4b584dc27f64aec5c653da663b2d`. **284 prior published articles**, **1,792 passages**, **263,443 narrative words**; **15 canonical v1.1 blobs** pinned by Git SHA. All IDs are architecture-native.
- New histories: **V.3 — Aristocracy, Status, Family, and Society** and **VIII.4 — The Korean Empire and the Search for Modernity**. Both are completed ten-article Chapters.
- Only `V.3.1`, `V.3.5`, and `VIII.4.6` existed in these Chapters before Batch V. Their prior narrative blocks, immutable passage IDs and article-level metadata are retained exactly, with Batch V blocks appended. The other 17 IDs are new. No reader storage keys, migrations, API endpoints, or application code were changed.
- The intended newly authored prose is 20,000–30,000 words, subject to the actual Python `WORD_RE` CI count rather than a manually estimated total. Source anchors are **selective contextual locators**, not direct peer-reviewed verification of every sentence.

## Goryeo social evidence and source limits

- [National Institute of Korean History, New Korean History volume 15, status and family](https://contents.history.go.kr/front/nh/view.do?levelId=nh_015_0030_0020_0020_0020) and [PDF, Goryeo family systems](https://contents.history.go.kr/data/pdf/nh/nh_015_0020.pdf): survey of status categories, kinship and property inheritance, including both paternal and maternal relationships. These are **academic syntheses** of earlier records and are not contemporaneous household censuses.
- [Academy of Korean Studies, Munbeol](https://encykorea.aks.ac.kr/Article/E0072775): civil-official elite lineages, marriage and inheritance of reputation, with social and political change across the dynasty.
- [Academy of Korean Studies, Hyangni](https://encykorea.aks.ac.kr/Article/E0062905) and [Hyangyeok](https://encykorea.aks.ac.kr/Article/E0062965): local clerks, hojang, tax/tribute collection, registration, recruitment and the administrative relation between Gaegyeong and provinces.
- [Academy of Korean Studies, Nobi](https://encykorea.aks.ac.kr/Article/E0012757) and [Nobi restoration](https://encykorea.aks.ac.kr/Article/E0012770): the **956** inspection policy under Gwangjong, subsequent restoration rules, the persistence of coercive property relationships and changing legal claims.

**Primary-source cautions:** `Goryeosa` and other transmitted dynastic compilations are mediated through later Joseon authorship and compilation. Elite marriages and inheritance records overrepresent wealthy property-holding families. Maternal inheritance and residence variation do **not** establish uniform gender equality. Social categories—free commoner, local clerk, specialized settlement resident, unfree nobi—must not be conflated. Accounts of laws and relief facilities document policy, not uniform implementation. Material culture from a grave cannot directly identify its subject's private motives or precise legal rank.

## Korean Empire and Gwangmu primary/source audit

- [National Institute of Korean History, Gojong and the Korean Empire](https://contents.history.go.kr/front/ht/view.do?levelId=ht_003_0010): detailed chronological study of the **1896 Russian-legation refuge**, **1897 imperial proclamation**, **1898 Independence Club struggle**, **1899 constitutional and reform institutions**, and diplomatic limits before **1904**.
- [National Institute of Korean History, Korean Empire and Gwangmu reforms](https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_i401000): distinction between the era name used to **1907** and the principal reform period concentrated **1897–1903**; government investments in surveys, the Wonsubu, industry and capital reform.
- [Academy of Korean Studies, Gwangmu Reform](https://encykorea.aks.ac.kr/Article/E0005118): land survey activity and constraints, imperial centralization, military and economic programmes.
- [Academy of Korean Studies, Jigye](https://encykorea.aks.ac.kr/Article/E0081002): distinction between cadastral registration, taxation and recognized property, with survey/certificate activity **1898–1903**.
- [NIKH, imperial palace ministry and officials](https://contents.history.go.kr/front/ht/view.do?levelId=ht_003_0030_0020_0040): overlap of court ministry and reform powers, ministers, new loyal administrators and their changing institutional position.

**Historical cautions:** A treaty, ordinance, military roster, title certificate or newspaper article describes a particular institutional source—not automatic public consent, universal practical enforcement or completed national modernization. The **1899 Daehanguk Gukje** asserted external sovereignty while preserving extensive autocratic imperial power. The Independence Club's constitutional ideals should not be equated with universal-suffrage institutions or with all popular views. Modern railways and mines could have Korean uses and simultaneously involve strategically asymmetric foreign concessions. The **1904 Russo-Japanese War** constrained independent reforms through external military force; later protectorate and colonial outcomes must not be treated as inevitable from 1897. Source interpretations must distinguish enacted plans, funded projects and operational outcomes.

## Release and outstanding limitations

Batch V's pinned regression verifies the exact bytes of all 15 canonical blobs and the 281 prior non-target article blobs, checks three append-only metadata/block prefixes and new source references, compares actual new prose with the 20–30k gate, tests Korean search aliases and both ten-stop routes, and checks compiler determinism and release allowlist. Generated-asset Chromium and **real confirmed** Cloudflare HTTPS branch-preview testing at desktop 1440px and mobile 390/320px are separate acceptance gates. Automated workflow triggers are scoped to the Batch V article paths, fixture and tests; they do not intentionally run unchanged historical batch-count assertions during future additive publications.

Selective academic source locators and source criticism **are not** independent scholarly peer review or exhaustive archive consultation. Actual historical interpretation would benefit from specialist review before claiming definitive academic reliability.
