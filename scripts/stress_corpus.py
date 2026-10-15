#!/usr/bin/env python3
"""Synthetic, isolated capacity benchmark. NEVER publishes synthetic history.
Builds 1,000 canonical-ID fixture articles in a disposable directory to test
compiler speed, shard sizes, immutable pack boundaries, and output limits.
The generated text is meaningless vocabulary and is not counted as content.
"""
import argparse,contextlib,io,json,tempfile,time,tracemalloc
from pathlib import Path
import build_corpus as bc

def benchmark(article_count=1000,blocks=10,words_per_block=110):
    titles=bc.canonical()
    keys=sorted(titles,key=lambda v:(['I','II','III','IV','V','VI','VII','VIII','IX','X'].index(v.split('.')[0]),*(int(n) for n in v.split('.')[1:])))
    if not 1<=article_count<=1000:raise ValueError('Use 1–1000 original canonical IDs')
    prior=bc.DATA
    with tempfile.TemporaryDirectory(prefix='korea-scale-test-') as folder:
        root=Path(folder);(root/'articles').mkdir();(root/'architecture.json').write_bytes((prior/'architecture.json').read_bytes())
        lexicon=['trade','mountain','river','palace','market','family','season','archive','stone','farming','learning','ritual','administration','journey','region','migration','record','dynasty','labor','community','craft','settlement','writing','reform','language','harvest','navigation','network','heritage','ceramic','politics','climate','economic','memory','boundary','innovation','assembly','chronology','chronicle','institution','fishing','maritime','scholar','monastery','transport','textile','fortress','agriculture','cultural','riverbank']
        # Common & unique terms are deliberate adversarial test data.
        for k,key in enumerate(keys[:article_count]):
            bs=[]
            for i in range(blocks):
                phrase=[lexicon[(k*7+i*9+j)%len(lexicon)] for j in range(words_per_block)]
                phrase[0]=f're{k:04d}{i:03d}'
                bs.append({'id':f'{key}:b{i+1:02d}','sequence':i+1,'title':f'Synthetic stress passage {i+1}', 'paragraphs':[' '.join(phrase)+'.']})
            article={'id':key,'title':titles[key],'description':'Synthetic capacity test — not historical narrative', 'blocks':bs}
            (root/'articles'/f'{key}.json').write_text(json.dumps(article),encoding='utf-8')
        bc.DATA=root
        tracemalloc.start()
        try:
            t0=time.perf_counter();metrics=bc.compile_corpus();secs=round(time.perf_counter()-t0,3)
            _,peak=tracemalloc.get_traced_memory()
            again=bc.compile_corpus();assert again['assets_changed']==0
            catalog=json.loads((root/'search/catalog.json').read_text())
            shard_map=json.loads((root/'search/shard-map.json').read_text())
            assert len(catalog['articles'])==article_count
            assert metrics['packs']<=article_count*blocks
            assert metrics['largest_pack']<bc.MAX_PACK_BYTES+12000
            assert metrics['search_shards']<20_000
            if article_count>=1000 and blocks>=10:
                assert any(len(prefix)>2 for prefix in shard_map['shards']), 'adaptive prefix split not exercised'
                term='re0000000'
                assert any(term.startswith(prefix) and term in json.loads((root/meta['path'].removeprefix('./data/')).read_text())['terms'] for prefix,meta in shard_map['shards'].items() if term.startswith(prefix)), 'synthetic token not searchable'
            result={'synthetic_only':True,'articles':article_count,'passages':article_count*blocks,'synthetic_words':metrics['words'],'build_seconds':secs,'peak_python_tracemalloc_mb':round(peak/1048576,2),'packs':metrics['packs'],'shards':metrics['search_shards'],'largest_pack_bytes':metrics['largest_pack'],'largest_shard_bytes':metrics['largest_shard'],'term_count':metrics['terms'],'repeat_rewrites':again['assets_changed'],'published_files':len(list((root/'packs').glob('*.json')))+len(list((root/'search/shards').glob('*.json')))+3}
            return result
        finally:tracemalloc.stop();bc.DATA=prior

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--articles',type=int,default=1000);p.add_argument('--blocks',type=int,default=10);p.add_argument('--words-per-block',type=int,default=110);o=p.parse_args()
    print(json.dumps(benchmark(o.articles,o.blocks,o.words_per_block),indent=2))
