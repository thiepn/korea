"""B compiler regressions: idempotence, no public governance leakage, input safety."""
from pathlib import Path
import sys,json,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_corpus import ROOT,DATA,compile_corpus,digest
from ingest import run
source=ROOT/'content/imports/batch_b_editorial.jsonl'
before={p.name:digest(p.read_bytes()) for p in (DATA/'articles').glob('*.json')}
result=run(source,dry_run=True)
assert result['articles_updated']==0, result
result=run(source,dry_run=False)
assert result['articles_updated']==0, 're-import wrote anything'
assert before=={p.name:digest(p.read_bytes()) for p in (DATA/'articles').glob('*.json')}
compiled=compile_corpus()
assert compiled['assets_changed']==0, compiled
assert compiled['largest_pack']<=24_000
assert compiled['articles']>=27
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/'bad.jsonl'
 p.write_text(json.dumps({'id':'VI.4.2.9.3','mode':'replace','blocks':[{'title':'invalid','paragraphs':['A deliberately long enough but invalid fictional text goes here.']}]})+'\n')
 try:run(p)
 except ValueError as exc:assert 'unknown canonical' in str(exc)
 else:raise AssertionError('invalid canonical ID was accepted')
 p.write_text(json.dumps({'id':'VI.4.2','mode':'replace','blocks':[{'title':'invalid','paragraphs':['A deliberately long enough but invalid fictional text goes here.']}]})+'\n')
 try:run(p)
 except ValueError as exc:assert 'cannot replace published' in str(exc)
 else:raise AssertionError('published overwrite was accepted')
assert not any((ROOT/'dist'/folder).exists() for folder in ('canonical','scripts','tests','data/articles','data/blocks','content'))
files=[p for p in (ROOT/'dist').rglob('*') if p.is_file()]
assert len(files)<20_000
print(f'PASS Batch B pipeline: replay safe, corrupt input rejected, stable pack hashes, {len(files)} allowlisted release assets')
