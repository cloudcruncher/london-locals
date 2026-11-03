(async function(){
  const M=window.LocalsModel, $=id=>document.getElementById(id);
  const meta=await fetch('data/boroughs.json').then(r=>r.json());
  const asOf=new Date(meta.as_of).toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'});document.querySelectorAll('.asof').forEach(e=>e.textContent=asOf);
  const B=meta.boroughs.slice().sort((a,b)=>b.venues-a.venues);
  const gbp=n=>(n<0?'-':'')+'£'+Math.round(Math.abs(n)).toLocaleString('en-GB');
  const k=n=>Math.abs(n)>=1e6?(n<0?'-':'')+'£'+(Math.abs(n)/1e6).toFixed(2)+'m':Math.abs(n)>=1e3?(n<0?'-':'')+'£'+Math.round(Math.abs(n)/1e3)+'k':gbp(n);
  let scen='base', chosen=new Set(window.LOCALS.LAUNCH_BOROUGHS), P=Object.assign({},M.SCENARIOS.base), prevTotals={};
  const sliders=[['listedPct','Share of venues listed',0,.3,.005,v=>(v*100).toFixed(1)+'%'],['paidPct','Listed venues on paid tier',0,.6,.01,v=>(v*100).toFixed(0)+'%'],['price','Paid tier £ per month',0,99,1,v=>'£'+v],['pen','Residents who join',0,.08,.0025,v=>(v*100).toFixed(2)+'%'],['active','Members active each month',.1,.8,.01,v=>(v*100).toFixed(0)+'%'],['red','Redemptions per active member / month',.5,4,.1,v=>v.toFixed(1)],['spend','Spend per redemption',10,80,1,v=>'£'+v],['newShare','Redemptions from new or off-peak customers',.1,.9,.01,v=>(v*100).toFixed(0)+'%'],['fee','Performance fee on tracked spend',0,.06,.0025,v=>(v*100).toFixed(2)+'%'],['spon','Sponsor income per borough / yr',0,100000,1000,v=>k(v)],['cont','Council or BID contract per borough / yr',0,100000,1000,v=>k(v)],['margin','Contribution margin on extra sales',.3,.8,.01,v=>(v*100).toFixed(0)+'%']];
  const ctl=$('sliders');
  sliders.forEach(([id,lab,mn,mx,st,fmt])=>{
    const l=document.createElement('label');l.innerHTML=`${lab}<output id="o_${id}"></output><input type="range" id="s_${id}" min="${mn}" max="${mx}" step="${st}">`;ctl.appendChild(l);
    l.querySelector('input').addEventListener('input',e=>{P[id]=+e.target.value;update()});
  });
  function syncSliders(){sliders.forEach(([id,,,,,fmt])=>{$('s_'+id).value=P[id]})}
  // borough chips
  const chips=$('chips');
  B.forEach(b=>{const c=document.createElement('button');c.className='chip';c.type='button';c.textContent=b.name;c.setAttribute('aria-pressed',chosen.has(b.name));
    c.onclick=()=>{chosen.has(b.name)?chosen.delete(b.name):chosen.add(b.name);if(!chosen.size)chosen.add(b.name);c.setAttribute('aria-pressed',chosen.has(b.name));
      chips.querySelectorAll('.chip').forEach(x=>x.setAttribute('aria-pressed',chosen.has(x.textContent)));update()};chips.appendChild(c)});
  $('allLondon').onclick=()=>{B.forEach(b=>chosen.add(b.name));chips.querySelectorAll('.chip').forEach(x=>x.setAttribute('aria-pressed','true'));update()};
  $('launch3').onclick=()=>{chosen=new Set(window.LOCALS.LAUNCH_BOROUGHS);chips.querySelectorAll('.chip').forEach(x=>x.setAttribute('aria-pressed',chosen.has(x.textContent)));update()};
  document.querySelectorAll('.seg button').forEach(b=>b.onclick=()=>{scen=b.dataset.s;P=Object.assign({},M.SCENARIOS[scen]);document.querySelectorAll('.seg button').forEach(x=>x.setAttribute('aria-pressed',x===b));syncSliders();update()});
  // animated number
  function setNum(el,v,fmt){const key=el.id,from=prevTotals[key]??0;prevTotals[key]=v;
    if(matchMedia('(prefers-reduced-motion: reduce)').matches){el.textContent=fmt(v);return}
    const t0=performance.now();(function f(t){const p=Math.min(1,(t-t0)/700),e=1-Math.pow(1-p,3);el.textContent=fmt(from+(v-from)*e);if(p<1)requestAnimationFrame(f)})(t0)}
  function update(){
    sliders.forEach(([id,,,,,fmt])=>$('o_'+id).textContent=fmt(P[id]));
    const sel=B.filter(b=>chosen.has(b.name)), R=M.run(sel,P), T=R.tot;
    setNum($('y1'),R.yr[0],k);setNum($('y2'),R.yr[1],k);setNum($('y3'),R.yr[2],k);setNum($('peak'),R.peakFunding,k);
    $('be').textContent=R.breakeven?'month '+R.breakeven:'not within 3 years';
    $('peakNote').textContent=R.peakMonth>=36?'Still falling at month 36, so the real need is higher.':'Lowest cumulative cash, reached around month '+R.peakMonth+'.';
    $('be').className=R.breakeven?'pos':'neg';
    $('payback').textContent=R.payback?'month '+R.payback:'beyond 3 years';
    setNum($('rev'),T.revenue,k);setNum($('cost'),T.cost,k);
    $('nb').textContent=sel.length;
    // revenue streams
    const streams=[['Business subscriptions',T.sub,'#1c7a62'],['Performance fees',T.perf,'#f2b84b'],['Sponsors',T.spon,'#8f6fe0'],['Councils and BIDs',T.cont,'#c4442a']];
    const tot=streams.reduce((a,s)=>a+s[1],0)||1;
    $('streams').innerHTML=`<div style="display:flex;height:34px;border-radius:99px;overflow:hidden;margin:.6rem 0 .9rem">${streams.map(s=>`<div title="${s[0]}" style="width:${s[1]/tot*100}%;background:${s[2]};transition:width .8s"></div>`).join('')}</div>`+
      streams.map(s=>`<div class="bar"><span style="width:auto;flex:1"><i style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${s[2]};margin-right:.4rem;width:10px"></i>${s[0]}</span><b>${k(s[1])}</b><small>${Math.round(s[1]/tot*100)}%</small></div>`).join('');
    const bizOnly=(T.sub+T.perf)/tot;
    $('mix').innerHTML=`Only <b>${Math.round(bizOnly*100)}%</b> of this revenue is paid by businesses; the rest depends on sponsors and councils, which take months to close.`;
    // who wins
    setNum($('w_res'),T.savings,k);setNum($('w_biz'),T.bizGain,k);setNum($('w_us'),T.revenue,k);setNum($('w_track'),T.tracked,k);
    $('w_biz').className=T.bizGain>=0?'pos':'neg';
    $('bizNote').textContent=T.bizGain>=0?`After paying discounts (${k(T.savings)}) and fees (${k(T.sub+T.perf)}), participating venues keep ${k(T.bizGain)} of extra margin in total.`:`At these settings venues lose money on the scheme. Raise the share of new or off-peak customers or cut the discount, or businesses will leave.`;
    // cash chart
    drawChart(R);
    // table
    $('tbody').innerHTML=R.per.map(s=>`<tr><td>${s.name}</td><td>${s.venues.toLocaleString('en-GB')}</td><td>${Math.round(s.listed)}</td><td>${Math.round(s.members).toLocaleString('en-GB')}${s.assumedPop?'*':''}</td><td>${k(s.tracked)}</td><td>${k(s.sub+s.perf+s.spon+s.cont)}</td></tr>`).join('');
  }
  function drawChart(R){
    const W=760,H=300,pl=58,pr=14,pt=14,pb=34, m=R.months;
    const vals=m.map(x=>x.cum), lo=Math.min(0,...vals), hi=Math.max(1,...vals,...m.map(x=>x.rev*12),...m.map(x=>x.cost*12));
    const x=t=>pl+(t-1)/35*(W-pl-pr), y=v=>pt+(1-(v-lo)/(hi-lo))*(H-pt-pb);
    const path=a=>a.map((v,i)=>(i?'L':'M')+x(i+1).toFixed(1)+' '+y(v).toFixed(1)).join(' ');
    const ticks=[lo,0,hi].filter((v,i,a)=>a.indexOf(v)===i);
    let svg=`<svg viewBox="0 0 ${W} ${H}" width="100%" role="img" aria-label="Cumulative cash over 36 months">`;
    ticks.forEach(v=>svg+=`<line x1="${pl}" x2="${W-pr}" y1="${y(v)}" y2="${y(v)}" stroke="currentColor" opacity=".15"/><text x="${pl-8}" y="${y(v)+4}" text-anchor="end" font-size="11" fill="currentColor" opacity=".7">${k(v)}</text>`);
    [1,12,24,36].forEach(t=>svg+=`<text x="${x(t)}" y="${H-10}" text-anchor="middle" font-size="11" fill="currentColor" opacity=".7">M${t}</text>`);
    svg+=`<path class="draw" d="${path(vals)}" fill="none" stroke="#1c7a62" stroke-width="3.5" stroke-linecap="round" pathLength="1"/>`;
    svg+=`<path d="${path(m.map(q=>q.rev*12))}" fill="none" stroke="#f2b84b" stroke-width="2" stroke-dasharray="5 5"/>`;
    svg+=`<path d="${path(m.map(q=>q.cost*12))}" fill="none" stroke="#ff6b4a" stroke-width="2" stroke-dasharray="2 5"/>`;
    const lowIdx=vals.indexOf(Math.min(...vals));
    if(R.peakFunding>0)svg+=`<circle cx="${x(lowIdx+1)}" cy="${y(vals[lowIdx])}" r="6" fill="#ff6b4a"/><text x="${x(lowIdx+1)+10}" y="${y(vals[lowIdx])-12}" font-size="12" font-weight="700" fill="#ff6b4a">cash low ${k(-R.peakFunding)}</text>`;
    svg+=`</svg>`;
    $('chart').innerHTML=svg;
  }
  syncSliders();update();
})();
