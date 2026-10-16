# KOREA Batch H — Deep Historical Narrative Expansion

## Verified baseline

- Remote `thiepn/korea` main: `e8bb9aa6ca05523da743f207583c38850f2444c1`, tree `38b142a3a1da3d42632e046fd0f8e01d037557ff`.
- Local Batch G baseline tree equals the remote Git tree; canonical v1.1 documents and spreadsheet were not edited.

## Historical content

- New complete Chapter: **IX.1 Liberation, Occupation, and the Division of Korea**, seven newly published articles (`IX.1.4`–`IX.1.10`) plus three earlier published subjects.
- Newly original narrative writing: **8,400 corpus-counted words** in 43 newly added passages, seven new articles, four append-only prior article deepening events. Earlier paragraphs remain exact ordered prefixes.
- Total source-first published corpus: **121 articles, 488 passages, 62,998 words**.
- Four individual essays exceed 2,000 words: IX.1.1 (2,174), IX.1.6 (2,127), VI.4.3 (3,072), IX.3.3 (2,387). Other collection entries are shorter, varied essays; they are not mislabeled as monographs.
- New human-authored manuscripts: `content/editorial/batch_h_liberation_collection.md` and `batch_h_deepening.md`; immutable ingest events: `content/imports/batch_h_collections.jsonl`.
- Nine source items were researched, drawn from the Academy of Korean Studies, National Library of Korea, National Institute of Korean History digitized primary materials, United Nations Yearbook and established museums/archives. Eight claims carry passage-specific anchors; the rest is original editorial synthesis, not peer-reviewed or independently checked line-by-line.

## Reader and discovery

- Existing automatic complete-Chapter shelf now recognizes four complete collections without adding another parallel engine.
- 16 thematic routes (two new) include a ten-stop liberation-to-partition Chapter sequence.
- Historical atlas: **50 curated landmarks and 62 explained connections**, seven landmarks and eleven connections newly added.
- Seven new Korean keyword alias groups; original reader bookmarks, history, routes, related-subject detours, and local state remain unchanged.

## Verification and caveats

- All v1.1 IDs, original paragraphs and canonical bytes checked against exact Batch G baseline Git tree.
- Replay-safe importer check PASS with no edits on reimport; first and second compiler runs produce no changed assets after publication.
- B/C/D/E/F/G pipeline regression scripts PASS. Existing E/F/G tests had stale fixed corpus sizes or fixed passage counts; assertions were revised for append-only growth while retaining original source and reference checks.
- Batch H browser interaction checks PASS at 1440×900, 390×844 and 320×720 with deterministic local asset requests and actual Chromium JS/DOM execution.
- Cloudflare-compatible release build PASS with **616 public assets**, 1,562,051 uncompressed bytes. No `canonical/`, raw `content/`, `data/articles/`, tests or scripts enter `dist/`.
- Real public-origin HTTPS browser acceptance is NOT_TESTED in this environment; local HTTP navigation remains restricted by the administrator in prior batches. A Cloudflare deployment status does not substitute for this check.
- Source metadata is selective, not claim-by-claim academic quality assurance. Korean morphological/Hanja search remains limited. The projected million-word library remains far ahead of current volume. No R2, D1 or paid resources.
