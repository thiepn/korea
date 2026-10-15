/** Bounded DOM and bounded HTML snapshots for prolonged Endless reading.
 * Old canonical blocks are recovered from their immutable content packs when
 * revisited; placeholders retain their measured layout height while loading.
 * Generic injected test passages are kept in memory when no pack exists.
 */
export function createReaderWindow({maxRendered=22,marginScreens=2,maxSnapshots=48,rehydrate=null}={}) {
 const pages=new Map();let observer=null,scheduled=false;
 function reset(){observer?.disconnect();observer=null;pages.clear();scheduled=false}
 function root(){return document.getElementById('readerBody')}
 function observerFor(){if(observer||!('IntersectionObserver' in window))return;observer=new IntersectionObserver(entries=>{
  for(const entry of entries)if(entry.isIntersecting&&entry.target.classList.contains('passage-placeholder'))restore(entry.target);
  schedule();
 },{rootMargin:'850px 0px 850px 0px'})}
 function publish(el,item,html){if(!el.isConnected||!el.classList.contains('passage-placeholder'))return;
  observer?.unobserve(el);el.insertAdjacentHTML('beforebegin',html);el.remove();item.html=html;item.pending=false;item.rendered=true;limitSnapshots();
 }
 function restore(el){if(!el?.classList?.contains('passage-placeholder'))return Promise.resolve();const item=pages.get(el.id);if(!item)return Promise.resolve();
  if(item.html){publish(el,item,item.html);return Promise.resolve()}
  if(item.pending)return item.task||Promise.resolve();if(!rehydrate)return Promise.resolve();item.pending=true;
  item.task=Promise.resolve().then(()=>rehydrate(el.id)).then(html=>{if(!html||!html.includes('body-section'))throw Error('Empty restored passage');publish(el,item,html)}).catch(()=>{
   item.pending=false;el.setAttribute('aria-label','Passage could not load. Scroll away and back to retry.');
  });return item.task;
 }
 function limitSnapshots(){let count=0;for(const v of pages.values())if(v.html&&!v.rendered&&v.recoverable)count++;
  if(count<=maxSnapshots)return;
  for(const item of pages.values()){
   if(count<=maxSnapshots)break;
   if(item.html&&!item.rendered&&item.recoverable){item.html=null;count--}
  }
 }
 function prune(){scheduled=false;const container=root();if(!container)return;observerFor();
  const live=[...container.querySelectorAll('.body-section:not(.passage-placeholder)')];if(live.length<=maxRendered)return;
  const border=innerHeight*marginScreens;const candidates=live.map(el=>{const r=el.getBoundingClientRect();return {el,r,dist:Math.min(Math.abs(r.bottom),Math.abs(r.top-innerHeight))}})
   .filter(x=>x.r.bottom< -border || x.r.top>innerHeight+border).sort((a,b)=>b.dist-a.dist);
  let count=live.length;
  for(const {el} of candidates){if(count<=maxRendered)break;const height=Math.ceil(el.getBoundingClientRect().height);if(height<1)continue;
   const id=el.id;const html=el.outerHTML;const recoverable=/^[IVX]+\.\d+\.\d+:b\d+$/.test(id)&&!!rehydrate;
   const item={html,height,rendered:false,recoverable,pending:false};pages.set(id,item);
   const placeholder=document.createElement('div');placeholder.id=id;placeholder.className='passage-placeholder';placeholder.dataset.blockid=id;placeholder.style.height=height+'px';placeholder.setAttribute('aria-label','Earlier passage. Scroll here to restore its text.');
   el.replaceWith(placeholder);observer?.observe(placeholder);count--;
  }
  limitSnapshots();
 }
 function schedule(){if(scheduled)return;scheduled=true;requestAnimationFrame(prune)}
 function reveal(id){return restore(document.getElementById(id))}
 return {reset,schedule,reveal,liveCount:()=>root()?.querySelectorAll('.body-section').length||0,placeholderCount:()=>[...pages.values()].filter(x=>!x.rendered).length,snapshotCount:()=>[...pages.values()].filter(x=>!!x.html&&!x.rendered).length,snapshotState:(id)=>!pages.has(id)?'untracked':pages.get(id).rendered?'restored':pages.get(id).html?'cached':'evicted'};
}
