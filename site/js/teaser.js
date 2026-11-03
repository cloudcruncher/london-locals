(function(){
  const box=document.getElementById('teaser');if(!box)return;
  const el=(t,c,x)=>{const e=document.createElement(t);if(c)e.className=c;if(x!=null)e.textContent=x;return e};
  fetch('data/offers.json').then(r=>r.json()).then(j=>{
    const seen=new Set(),pick=[];
    // one offer per venue, spread across boroughs
    ['Hackney','Lambeth','Lewisham','Hackney','Lambeth','Lewisham'].forEach(b=>{
      const o=j.offers.find(x=>x.borough===b&&!seen.has(x.name));if(o){seen.add(o.name);pick.push(o)}});
    pick.forEach(o=>{const c=el('article','dcard');
      c.appendChild(el('div','meta',o.type+' · '+o.neighbourhood+', '+o.borough));
      c.appendChild(el('h3',null,o.name));c.appendChild(el('div','ot',o.offer_title));c.appendChild(el('div',null,o.offer_detail));
      const a=el('a','src','See source');a.href=o.source_url;a.rel='noopener noreferrer';a.target='_blank';c.appendChild(a);box.appendChild(c)});
  }).catch(()=>{box.textContent=''});
})();
