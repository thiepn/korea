/* Bounded pack loader + lazily fetched inverted search shards. Static-host friendly. */
import {rankSearch} from './exploration.js';
export function createPackLoader(fetchAsset=fetch,{maxCached=16}={}) {
  const cache=new Map(),inflight=new Map();
  async function pack(path) {
    if(cache.has(path)){const value=cache.get(path);cache.delete(path);cache.set(path,value);return value}
    if(inflight.has(path))return inflight.get(path);
    const task=(async()=>{const response=await fetchAsset(path);if(!response.ok)throw new Error(`Content HTTP ${response.status}`);const value=await response.json();if(!value||!Array.isArray(value.blocks))throw new Error('Invalid content pack');cache.set(path,value);while(cache.size>maxCached)cache.delete(cache.keys().next().value);return value})();
    inflight.set(path,task);try{return await task}finally{inflight.delete(path)}
  }
  async function load(chunk){
    if(!chunk.pack){const r=await fetchAsset(chunk.path);if(!r.ok)throw new Error(`Passage HTTP ${r.status}`);return r.json()}
    const p=await pack(chunk.pack),b=p.blocks[chunk.offset];
    if(p.version!==2||b?.id!==chunk.id)throw new Error('Passage identity mismatch in pack');
    return b;
  }
  return {load,prefetch:(chunk)=>chunk?.pack?pack(chunk.pack).catch(()=>null):Promise.resolve(null),cacheSize:()=>cache.size};
}
const normalizeQuery=t=>String(t||'').normalize('NFKD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
const STOP=new Set('the and for but was were are that this with from have has had into between its their there which what when where been being about also through these those they them then than would could should because while before after under over more some each other only such many much very even often across among most just will can not you your our how why who all his her she him one two three both onto itself within without together during around'.split(' '));
export function createShardedSearch(fetchAsset=fetch,{maxCached=20}={}){
 const shards=new Map(),pending=new Map();let map=null,catalog=[];
 function init(shardMap,catalogRows){map=shardMap.shards;catalog=catalogRows.articles||[]}
 async function get(prefix){const meta=map?.[prefix];if(!meta)return null;if(shards.has(prefix)){const val=shards.get(prefix);shards.delete(prefix);shards.set(prefix,val);return val}
  if(pending.has(prefix))return pending.get(prefix);
  const task=(async()=>{const r=await fetchAsset(meta.path);if(!r.ok)throw new Error(`Search index HTTP ${r.status}`);const data=await r.json();if(data.prefix!==prefix||data.version!==2)throw new Error(`Invalid search shard ${prefix}`);shards.set(prefix,data.terms);while(shards.size>maxCached)shards.delete(shards.keys().next().value);return data.terms})();pending.set(prefix,task);try{return await task}finally{pending.delete(prefix)}
 }
 async function search(query,canonical,readableIds,filter='all'){
   const titleHits=rankSearch(query,canonical,[],readableIds,filter);
   const terms=[...new Set((normalizeQuery(query).match(/[a-z0-9]{3,}/g)||[]).filter(w=>!STOP.has(w)))].slice(0,6);
   if(!terms.length||!map)return titleHits;
   const lists=await Promise.all(terms.map(async term=>{let prefix=term.slice(0,2);while(!map[prefix]&&prefix.length<term.length)prefix=term.slice(0,prefix.length+1);const shard=await get(prefix);return shard?.[term]||[]}));
   const scores=new Map(),hits=new Map();
   for(const list of lists)for(const [doc,block] of list){scores.set(doc,(scores.get(doc)||0)+1);if(!hits.has(doc))hits.set(doc,block)}
   const corpus=Array.from(scores.entries()).filter(([,score])=>score===terms.length).map(([doc])=>{
     const a=catalog[doc],snippet=a?.previews?.[hits.get(doc)];if(!a||filter==='planned')return null;
     return {id:a.id,title:a.title,readable:true,score:55+terms.length*18,summary:snippet?.text||a.description,where:snippet?.title||'Article'};
   }).filter(Boolean);
   const merged=new Map();for(const item of titleHits)merged.set(item.id,item);for(const item of corpus){const other=merged.get(item.id);merged.set(item.id,other&&other.score>item.score?other:item)}
   return [...merged.values()].sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id,undefined,{numeric:true})).slice(0,60);
 }
 return {init,search,cacheSize:()=>shards.size};
}
