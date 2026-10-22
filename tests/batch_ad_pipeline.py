"""Batch AD: frozen authorship, immutable earlier archive, canonical identity and deterministic publication."""
from __future__ import annotations
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_corpus import canonical, compile_corpus, WORD_RE

fixture = json.loads((ROOT / "tests/fixtures/batch_ad_baseline.json").read_text(encoding="utf-8"))
BASE = "88489f7595567c6bc09f8ef71d0402c139d519f5"
SNAP = fixture["authored_snapshot"]
assert fixture["baseline_main"] == BASE
assert SNAP == "f9eb6a6b9af4a9275ef03a52ebe919dd94d200cc"

def git_show(ref: str, path: str) -> bytes:
    return subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT,
                          capture_output=True, check=True).stdout

def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

titles = canonical()
baseline = fixture["article_blobs"]
assert len(baseline) == fixture["prior_article_count"] == 423
assert len(fixture["canonical_blobs"]) == 15
for path, expected in fixture["canonical_blobs"].items():
    assert git_blob(ROOT / path) == expected, ("changed canonical master source", path)

old_articles = {}
for path, expected in baseline.items():
    current = ROOT / path
    assert current.exists(), ("missing published source", path)
    if git_blob(current) == expected:
        continue
    original = json.loads(git_show(BASE, path).decode("utf-8"))
    newer = json.loads(current.read_text(encoding="utf-8"))
    assert newer["blocks"][:len(original["blocks"])] == original["blocks"], ("rewritten historic passage", path)
    assert {k:v for k,v in newer.items() if k != "blocks"} == {k:v for k,v in original.items() if k != "blocks"}, ("rewritten published metadata", path)
    old_articles[path] = len(original["blocks"])

targets = {f"{chapter}.{n}" for chapter in fixture["target_chapters"] for n in range(1,11)}
assert len(targets) == 20
appended = fixture["prior_appended"]
assert set(appended) == {"V.6.5", "VI.3.4"}
assert all(f"data/articles/{id}.json" in baseline for id in appended)
new_ids = targets - set(appended)
assert len(new_ids) == 18
for id in new_ids:
    assert f"data/articles/{id}.json" not in baseline, ("supposed new article already existed", id)

all_articles = {p.stem for p in (ROOT / "data/articles").glob("*.json")}
assert len(all_articles) >= 441 and targets <= all_articles
words = 0
passages = 0
anchors = 0
normalized_paragraphs = []
per_article = {}
for id in sorted(targets):
    path = f"data/articles/{id}.json"
    a = json.loads((ROOT / path).read_text(encoding="utf-8"))
    frozen = json.loads(git_show(SNAP, path).decode("utf-8"))
    assert a["id"] == id and a["title"] == titles[id], ("canonical identity or title", id)
    if id in appended:
        original = json.loads(git_show(BASE, path).decode("utf-8"))
        assert len(original["blocks"]) == appended[id], ("changed prior passage window", id)
        assert a["blocks"][:appended[id]] == original["blocks"], ("rewritten early historical block", id)
        assert {k:v for k,v in a.items() if k != "blocks"} == {k:v for k,v in original.items() if k != "blocks"}, ("rewritten prior article metadata", id)
    else:
        assert a.get("release") == "AD" and len(a.get("sources", [])) >= 3, id
        assert len(a["blocks"]) >= 10, ("new article too short", id)
        assert all(s["url"].startswith("https://") for s in a["sources"]), id
    end = len(frozen["blocks"])
    assert a["blocks"][:end] == frozen["blocks"], ("frozen authored manuscript changed", id)
    begin = appended.get(id, 0)
    assert end > begin, ("missing new manuscript", id)
    fresh = a["blocks"][begin:end]
    passages += len(fresh)
    article_words = 0
    for n,b in enumerate(a["blocks"][:end],1):
        assert b["id"] == f"{id}:b{n:02d}" and b.get("sequence",n) == n, ("passage identity",id,n)
    for b in fresh:
        assert b.get("title") and b.get("paragraphs"), id
        for paragraph in b["paragraphs"]:
            assert isinstance(paragraph,str) and len(paragraph) >= 150, ("short paragraph",id)
            article_words += len(WORD_RE.findall(paragraph))
            normalized_paragraphs.append(" ".join(re.findall(r"\w+",paragraph.casefold())))
        for e in b.get("evidence", []):
            assert e.get("type") in ("context","direct"), id
            assert len(e.get("locator", "")) >= 12 and len(e.get("claim", "")) >= 24, id
            assert 0 <= e["sourceIndex"] < len(a.get("sources", [])), id
            anchors += 1
    assert article_words >= (750 if id not in appended else 300), ("thin authored section",id,article_words)
    words += article_words
    per_article[id] = article_words

assert len(normalized_paragraphs) == len(set(normalized_paragraphs)), "duplicated Batch AD prose"
assert 20_000 <= words <= 30_000, ("fresh narrative word gate",words)
# Expected snapshot count is independently cross-checked; allow a narrow tokenization
# difference from the JavaScript manuscript prescreen, while Python governs the release.
assert abs(words - fixture["expected_new_words"]) <= 20, ("unexpected rewritten or missing words",words)
assert passages == fixture["expected_new_passages"] == 196
assert anchors >= 90 and anchors == fixture["expected_source_anchors"]

aliases = json.loads((ROOT / "content/atlas/search-aliases.json").read_text(encoding="utf-8"))
old_aliases = json.loads(git_show(BASE,"content/atlas/search-aliases.json").decode("utf-8"))
for id, previous in old_aliases.items():
    assert set(previous) <= set(aliases.get(id, [])), ("removed legacy search terms",id)
assert all(len(aliases.get(id,[])) >= 3 for id in targets), "incomplete Korean terms"

explore = json.loads((ROOT / "data/explore.json").read_text(encoding="utf-8"))["collections"]
original_routes = json.loads(git_show(BASE,"data/explore.json").decode("utf-8"))["collections"]
old_slugs = {route["slug"] for route in original_routes}
assert len(old_slugs) == len(original_routes), "prior routes contain duplicate slugs"
assert [route for route in explore if route["slug"] in old_slugs] == original_routes, "historic routes removed, altered, duplicated or reordered"
for slug,ch in [
    ("goryeo-learning-art-science-complete","V.6"),
    ("joseon-neo-confucian-intellectual-order-complete","VI.3"),
]:
    routes = [r for r in explore if r["slug"] == slug]
    assert len(routes) == 1 and routes[0]["ids"] == [f"{ch}.{n}" for n in range(1,11)], slug

manifest = json.loads((ROOT/"data/content-manifest.json").read_text(encoding="utf-8"))
assert manifest["count"] >= 441
assert manifest["sampleWordCount"] >= fixture["prior_word_count"] + words
assert sum(a["blocks"] for a in manifest["articles"]) >= fixture["prior_passages"] + passages
first = compile_corpus()
second = compile_corpus()
assert second["assets_changed"] == 0, "non-deterministic corpus rebuild"
assert first["largest_pack"] <= 24_000 and first["largest_shard"] <= 48_000
assets = [p.relative_to(ROOT/"dist").as_posix() for p in (ROOT/"dist").rglob("*") if p.is_file()]
assert assets and all(not x.startswith(("canonical/","content/","scripts/","tests/","data/articles/","data/blocks/")) for x in assets)
print(f"PASS Batch AD: +{words:,} original words, {passages} passages, {anchors} contextual source anchors; 18 new + 2 append-only articles; 423 old and 15 canonical preserved; two complete Chapter routes and deterministic release.")
