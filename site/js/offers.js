(function(){
  const grid=document.getElementById('grid'),count=document.getElementById('count'),q=document.getElementById('q');
  const st={b:'All',t:'All',q:''};let data=[];
  const el=(tag,cls,txt)=>{const e=document.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e};
  function chips(id,key,vals){
    const box=document.getElementById(id);box.textContent='';
    ['All',...vals].forEach(v=>{const b=el('button','chip',v);b.type='button';b.setAttribute('aria-pressed',st[key]===v);
      b.onclick=()=>{st[key]=v;chips(id,key,vals);draw()};box.appendChild(b)});
  }
  function draw(){
    const t=st.q.toLowerCase();
    const r=data.filter(o=>(st.b==='All'||o.borough===st.b)&&(st.t==='All'||o.type===st.t)&&(!t||[o.name,o.neighbourhood,o.offer_title,o.offer_detail].join(' ').toLowerCase().includes(t)));
    grid.textContent='';grid.className='dir';
    r.forEach(o=>{const c=el('article','dcard');
      c.appendChild(el('div','meta',o.type+' · '+o.neighbourhood+', '+o.borough));
      c.appendChild(el('h3',null,o.name));
      c.appendChild(el('div','ot',o.offer_title));
      c.appendChild(el('div',null,o.offer_detail));
      if(o.conditions)c.appendChild(el('div','meta','When: '+o.conditions));
      const a=el('a','src','See source');a.href=o.source_url;a.rel='noopener noreferrer';a.target='_blank';
      c.appendChild(a);c.appendChild(el('div','meta','Checked '+o.checked_on));grid.appendChild(c)});
    count.textContent=r.length+' offer'+(r.length===1?'':'s')+' shown';
  }
  q.addEventListener('input',()=>{st.q=q.value;draw()});
  fetch('data/offers.json').then(r=>r.json()).then(j=>{
    data=j.offers;
    chips('bchips','b',[...new Set(data.map(o=>o.borough))].sort());
    chips('tchips','t',[...new Set(data.map(o=>o.type))].sort());
    document.getElementById('asof').textContent='Offers last checked '+j.checked_on+'. Source: each venue’s own public page.';
    draw();
  }).catch(()=>{count.textContent='Could not load offers. Please refresh.'});
})();
