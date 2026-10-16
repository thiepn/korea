# Batch R evidence and source audit

## Published scope

- Base: `e9841f1686f364fb2c4c87b1b3480a436c3a8591`; new material restricted to **IV.5** and **VIII.3**.
- The 17 new article files carry contextual evidence anchors and source metadata. The three existing articles **IV.5.2, VIII.3.1, VIII.3.5** are **append-only**; their published metadata and old block prefixes are identical to the base. New paragraphs refer to sources in their prose, but new top-level source metadata was deliberately *not* retrofitted.
- This is original editorial synthesis, **not independent peer review, exhaustive scholarly collation, or a claim that every sentence has a direct primary source**.

## Balhae — verified institutional references

1. [National Institute of Korean History, Balhae foundation](https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_i100800): Yingzhou crisis, founding sequence and dating of 698.
2. [National Institute of Korean History, capital movements](https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_i101000): Dae dynasty capitals, post-793 succession; distinguish reconstructed motives from dated events.
3. [National Institute of Korean History, collapse of Balhae](https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_i100900): Seon's recovery, the late Khitan offensive, surrender in 926 and aftermath.
4. [Academy of Korean Studies, Balhae](https://encykorea.aks.ac.kr/Article/E0021626): complex Goguryeo/Mohe inheritance and disputed dates for mature local administration.
5. [Academy of Korean Studies, local administration](https://encykorea.aks.ac.kr/Article/E0054208): five capitals, fifteen prefectures, reported sixty-two `ju`. The transmitted `New Book of Tang` geographical record lists only sixty named `ju`; do not imply an exact modern boundary map.
6. [National Museum of Korea, Balhae gallery](https://www.museum.go.kr/ENG/contents/E0201031000.do?showHallId=760&showroomCode=DM0010): capital remains, craft and regional links as archaeological context.

**Qualifiers:** Chinese dynastic texts employ political categories and investiture conventions; they are not direct censuses of ethnicity or evidence that the emperor administered Balhae's territory. Balhae's five-capital scheme and prefectural locations are reconstructions. Volcanic or internal-rebellion explanations for its swift fall are hypotheses, not independently verified causes.

## Donghak and the Gabo order — verified institutional and contemporary evidence

1. [Academy of Korean Studies, Donghak Movement](https://encykorea.aks.ac.kr/Article/E0016865): the religion's role, Jeon Bong-jun, social mobilization and the successive uprisings.
2. [Academy of Korean Studies, peasant movements](https://encykorea.aks.ac.kr/Article/E0013107): Gobu, Jeonju, local organization, the later anti-Japanese campaign and Ugeumchi.
3. [Academy of Korean Studies, `jipgangso`](https://encykorea.aks.ac.kr/Article/E0055029): local administrative experiments in Jeolla following the Jeonju negotiations; local scope and formal terms require care.
4. [Academy of Korean Studies, Gabo Reform](https://encykorea.aks.ac.kr/Article/E0000925): Gunguk Gimucheo and cabinet chronology; legislative ambition must be separated from implementation.
5. [Academy of Korean Studies, Eulmi Reform](https://encykorea.aks.ac.kr/Article/E0042947): changes after the assassination, the topknot controversy and political collapse in 1896.
6. [National Institute of Korean History, Gabo Reform](https://contents.history.go.kr/mobile/kc/view.do?levelId=kc_i400600): Korean reform efforts and their serious deficit of independent political authority amid Japanese military pressure.
7. [Office of the Historian, `FRUS` 1894 Appendix I](https://history.state.gov/historicaldocuments/frus1894app1/index): contemporaneous diplomatic record. [Korean Council proposals](https://history.state.gov/historicaldocuments/frus1894app1/d53) and [Korean diplomatic protest of foreign forces](https://history.state.gov/historicaldocuments/frus1894app1/d16) provide specific primary-source constraints.

**Qualifiers:** `FRUS` documents are translated correspondence and sometimes contain interpretive notes or unverified wartime reports, not neutral full descriptions of Korean opinion. A Gabo decree is evidence of a measure proposed or adopted, not evidence that it was enforced everywhere. Donghak leadership, religious aims, regional participation, and subsequent political interpretations must not be collapsed into one fixed platform. The 1895 palace assassination involved Japanese agents; specific eyewitness accounts may differ on circumstances.

## Release and source-boundary controls

- The Chapter reader retains immutable pre-Batch-R passages and all current local-state ownership. Changes to `scripts/build_exploration.py` and Korean aliases alter navigation/indexing, not old article IDs.
- The Batch R QA workflow triggers for its own two Chapter inventories and own tests only; later additive batches require their own baseline.
- QA covers content compilation, source locator structure, Git blob SHA preservation, full Chapter navigation, desktop/mobile browser routes and real-origin branch preview. It does not constitute independent confirmation of every interpretive sentence or a physical-device usability study.
