/** Bounded live-passage DOM for long KOREA reading sessions.
 * Replaces far-away rendered paragraphs with height-preserving placeholders.
 * The saved HTML is kept in memory for upward scrolling and accessibility.
 * No text is discarded from the publication or reading position.
 */
export function createReaderWindow({maxRendered=22, marginScreens=2}={}) {
  const pages=new Map();
  let observer=null, scheduled=false;
  function reset() {observer?.disconnect();observer=null;pages.clear();scheduled=false}
  function findRoot(){return document.getElementById('readerBody')}
  function ensureObserver(){if(observer||!('IntersectionObserver' in window))return;observer=new IntersectionObserver(entries=>{
    for(const e of entries)if(e.isIntersecting&&e.target.classList.contains('passage-placeholder'))restore(e.target);
    schedule();
  },{rootMargin:'850px 0px 850px 0px'})}
  function restore(el){
    if(!el?.classList?.contains('passage-placeholder'))return;
    const item=pages.get(el.id);if(!item)return;
    observer?.unobserve(el);
    el.insertAdjacentHTML('beforebegin',item.html);
    el.remove();
    item.rendered=true;
  }
  function prune(){
    scheduled=false;
    const root=findRoot();if(!root)return;
    ensureObserver();
    const live=[...root.querySelectorAll('.body-section:not(.passage-placeholder)')];
    if(live.length<=maxRendered)return;
    const keepDist=innerHeight*marginScreens;
    const candidates=live.map(el=>{
      const r=el.getBoundingClientRect();return {el,r,dist:Math.min(Math.abs(r.bottom),Math.abs(r.top-innerHeight))};
    }).filter(x=>x.r.bottom< -keepDist || x.r.top>innerHeight+keepDist).sort((a,b)=>b.dist-a.dist);
    let remaining=live.length;
    for(const {el} of candidates){
      if(remaining<=maxRendered)break;
      const h=Math.ceil(el.getBoundingClientRect().height);
      if(h<1)continue;
      const id=el.id;pages.set(id,{html:el.outerHTML,height:h,rendered:false});
      const spacer=document.createElement('div');spacer.id=id;spacer.className='passage-placeholder';spacer.dataset.blockid=id;
      spacer.style.height=h+'px';spacer.setAttribute('aria-label','Earlier passage. Scroll here to restore its text.');
      el.replaceWith(spacer);observer?.observe(spacer);remaining--;
    }
  }
  function schedule(){if(scheduled)return;scheduled=true;requestAnimationFrame(prune)}
  function reveal(id){const el=document.getElementById(id);if(el?.classList.contains('passage-placeholder'))restore(el)}
  return {reset,schedule,reveal,liveCount:()=>findRoot()?.querySelectorAll('.body-section').length||0,placeholderCount:()=>pages.size};
}
