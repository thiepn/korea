# Batch Y — Han commanderies and Goryeo government: provenance and QA

## Boundaries

Frozen starting main: `74adc154bd38f1541d6ea8d42e1a8e8d243bab05`: **334 article IDs, 2,286 passages, 325,272 narrative words**, and 15 immutable canonical v1.1 sources. Article-authorship snapshot: `62ff00e6b6a7505e803e3522432bec7fda22a6e9`. Batch Y completes Chapters `II.3` and `V.2` with 16 new original historical articles and four strictly append-only extensions (`II.3.2`, `II.3.4`, `V.2.3`, `V.2.5`). No existing article title, metadata, original block, passage ID or other already-published article is rewritten. Reader local storage and application code remain unchanged. The fixture freezes previous Git blobs and author-window ends, allowing later valid append-only additions without altering this batch's original-word count. Authoritative totals must be computed in Python CI.

## II.3 — Source evidence and chronology

The Han conquest of Wiman Joseon ended in **108 BCE** and was followed by Lelang, Xuantu, Zhenfan and Lintun commanderies, whose trajectories diverged. Zhenfan and Lintun were absorbed in **82 BCE**; Xuantu moved amid frontier conflict, while Lelang survived until its political end around **313 CE**. The later Daifang commandery was established in the context of Gongsun regional power in the early third century. Transmitted administrative district lists do not establish precisely controlled borders, and labels such as Han, Ye, Wa or foreign subject reflect literate political viewpoints, not the unmediated identities of all inhabitants.

Selected sources:
- National Institute of Korean History, *A History of Korea*, ancient society and Lelang: https://contents.history.go.kr/resources/common/pdf/A%20History%20of%20Korea_The%20Understanding%20Korea%20Series.pdf — institutional synthesis.
- Academy of Korean Studies, *Lelang Commandery*: https://encykorea.aks.ac.kr/Article/E0011576 — administrative, contact and historiographical questions.
- National Museum of Korea, *Lelang inscribed roof-end tile*: https://vcm.museum.go.kr/ENG/contents/E0402000000.do?relicId=1874&schM=view&searchId=search — direct material proof of an inscription and associated building tradition, not a territorial survey.
- AKS, *Zhenfan*: https://encykorea.aks.ac.kr/Article/E0054690 — incorporation and disputed location.
- AKS, *Lintun*: https://encykorea.aks.ac.kr/Article/E0047426 — early merger and relocation history.
- AKS, *Xuantu*: https://encykorea.aks.ac.kr/Article/E0063309 — geographical controversy and relocation.
- AKS, *Daifang*: https://encykorea.aks.ac.kr/Article/E0014398 — later reorganization and regional power.
- AKS, *Eunyul Gwansan-ri tombs*: https://encykorea.aks.ac.kr/Article/E0042852 — mortuary archaeological comparison.

Material sources, tombs and inscriptions are not straightforward ethnic labels or direct proof of all imperial geographic claims. Colonial-period excavation provenance and unequal access to North Korean archaeological records warrant explicit caution. The four legacy articles' previous metadata are immutable: their later additions are supported by this bibliography, not falsely labelled as newly source-indexed material.

## V.2 — Institutional change and limits of official histories

Goryeo (918–1392) governed through monarchy, household alliances, learned service, inherited opportunity, military resources and regionally varying administration. Civil service examinations were introduced in **958** under Gwangjong, without making preparation universally accessible. Seongjong-era reforms adapted broader East Asian models, while Goryeo-specific bodies included the Dobyeongmasa and Sikmok Dogam. The five circuits and two frontier regions developed over time, not from one uniformly applied original blueprint.

Selected sources:
- National Institute of Korean History, *Political Structure of Early Goryeo*: https://db.history.go.kr/diachronic/level.do?levelId=nh_013_0010 — complex institutional adaptation.
- Academy of Korean Studies, *Central Secretariat-Chancellery*: https://encykorea.aks.ac.kr/Article/E0053786 — formal titles, debated configurations, late changes.
- AKS, *Six Ministries*: https://encykorea.aks.ac.kr/Article/E0042104 — functions and administrative evolution.
- AKS, *Sikmok Dogam*: https://encykorea.aks.ac.kr/Article/E0032553 — Goryeo legal council and changing competencies.
- AKS, *Five Circuits*: https://encykorea.aks.ac.kr/Article/E0038163 — non-simultaneous geographic organization.
- AKS, *Goryeo*: https://encykorea.aks.ac.kr/Article/E0003424 — contested aristocracy-versus-bureaucracy research.
- AKS, *Official evaluation*: https://encykorea.aks.ac.kr/Article/E0003313 — personnel assessment.
- Ministry of Personnel Management, *History of Recruitment*: https://www.mpm.go.kr/historyofexam/ — the 958 exam initiative.

The *Goryeosa* and related histories were compiled under Joseon and privilege elite male actions and evaluative frames. Law, fiscal assessment and appointment norms cannot be read as proof of universal practical enforcement. Source anchors in new articles are contextual, not independent sentence-by-sentence scholarly review. No invented verbatim ancient quotations or fabricated archival locators.

## Release criteria

The fixture must preserve all 334 baseline article blobs or their original metadata and passage prefixes, all 15 canonical source Git blobs, all four legacy article originals, and the 20 immutable authored passage windows. Test 20,000–30,000 new Python `WORD_RE` words, complete ten-article canonical Chapters, distinct paragraphs, valid citations, Korean search aliases, exactly two ten-stop curated reading trails, deterministic compilation and public asset allowlist. Run exact-head push/PR GitHub Actions, Chromium 1440px/390px/320px generated assets, and verified exact-head Cloudflare HTTPS branch preview. Squash merge only against unchanged main after all check conclusions succeed. No manual deployment, credentials, migrations, or costs. Independent specialist peer review remains NOT_TESTED.
