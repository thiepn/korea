/** Search and discovery logic; pure, independent from DOM and browser persistence. */
const normalize = value => String(value ?? '').toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');
export function excerptAround(content, words, length=175) {
  const text = String(content || '').replace(/\s+/g,' ').trim();
  const hit = words.map(w=>normalize(text).indexOf(w)).filter(n=>n>=0).sort((a,b)=>a-b)[0];
  const from = hit == null ? 0 : Math.max(0,hit-58);
  const end = Math.min(text.length,from+length);
  return `${from?'…':''}${text.slice(from,end).trim()}${end<text.length?'…':''}`;
}
export function rankSearch(query, canonical, articles, readableIds, filter='all') {
  const terms = normalize(query).trim().split(/\s+/).filter(Boolean).slice(0,8);
  const source = new Map((articles || []).map(a=>[a.id,a]));
  const results = [];
  for (const node of canonical) {
    const item=source.get(node.id),readable=readableIds.has(node.id);
    if(filter==='readable'&&!readable || filter==='planned'&&readable)continue;
    let score=readable?4:0,summary='',where='title';
    if(terms.length){
      const title=normalize(node.title),id=normalize(node.id),desc=normalize(item?.description||'');
      const matchedBlock=item?.blocks?.find(b=>terms.every(t=>normalize(b.title+' '+b.text).includes(t)));
      const haystack=normalize(item?.blocks?.map(b=>b.title+' '+b.text).join(' ')||'');
      if(!terms.every(t=>id.includes(t)||title.includes(t)||desc.includes(t)||haystack.includes(t)))continue;
      for(const t of terms){
        if(id===t)score+=70;else if(id.startsWith(t))score+=20;
        if(title.startsWith(t))score+=25;else if(title.includes(t))score+=15;
        if(desc.includes(t))score+=8;
        if(haystack.includes(t))score+=3;
      }
      if(matchedBlock){summary=excerptAround(matchedBlock.text,terms);where=matchedBlock.title;}
      else if(desc){summary=item.description;where='Article introduction';}
    }else if(!readable)continue;
    results.push({...node,readable,score,summary,where});
  }
  return results.sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id,undefined,{numeric:true})).slice(0,60);
}
export function collectionFor(collections,id) {
  return (collections||[]).filter(c=>c.ids.includes(id));
}
