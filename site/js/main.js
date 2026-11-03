(function(){
  const rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.add('js');
  const ad=window.LOCALS&&window.LOCALS.ANALYTICS_DOMAIN;
  if(ad){const sc=document.createElement('script');sc.defer=true;sc.dataset.domain=ad;sc.src='https://plausible.io/js/script.js';document.head.appendChild(sc)}
  // scroll reveal
  const io = new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.15});
  document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
  // counters
  const cio = new IntersectionObserver(es=>es.forEach(e=>{
    if(!e.isIntersecting)return; cio.unobserve(e.target);
    const el=e.target, to=+el.dataset.count, pre=el.dataset.pre||'', suf=el.dataset.suf||'';
    if(rm){el.textContent=pre+to.toLocaleString('en-GB')+suf;return}
    const t0=performance.now(), d=1600;
    (function tick(t){const p=Math.min(1,(t-t0)/d), v=Math.round(to*(1-Math.pow(1-p,3)));
      el.textContent=pre+v.toLocaleString('en-GB')+suf; if(p<1)requestAnimationFrame(tick)})(t0);
  }),{threshold:.4});
  document.querySelectorAll('[data-count]').forEach(el=>cio.observe(el));
  // animated bars
  const bio = new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.querySelectorAll('i[data-w]').forEach(i=>i.style.width=i.dataset.w+'%');bio.unobserve(e.target)}}),{threshold:.3});
  document.querySelectorAll('.dash').forEach(el=>bio.observe(el));
  // forms
  document.querySelectorAll('form[data-signup]').forEach(f=>{
    f.addEventListener('submit',async ev=>{
      ev.preventDefault();
      const data=Object.fromEntries(new FormData(f)); data.kind=f.dataset.signup; data.at=new Date().toISOString();
      if(data.website) return; // honeypot
      delete data.website;
      const box=f.querySelector('.msg');const sb=f.querySelector('button[type=submit]'); const ep=window.LOCALS.FORM_ENDPOINT;
      if(!f.checkValidity()){f.reportValidity();return}
      if(sb)sb.disabled=true;
      try{
        if(ep){const r=await fetch(ep,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(data)});if(!r.ok)throw new Error(r.status);
          box.textContent='Thank you, you are on the list. We will email you before your borough launches.'}
        else{const to=window.LOCALS.CONTACT_EMAIL;const body=Object.entries(data).filter(([k])=>k!=='at').map(([k,v])=>k+': '+v).join('\n');
          location.href='mailto:'+to+'?subject='+encodeURIComponent('Doorstep Club early access: '+data.kind)+'&body='+encodeURIComponent(body);
          box.textContent='Your email app should open with your details ready. Press send to join the list.'}
        box.classList.add('show');f.reset();
      }catch(err){box.textContent='Something went wrong. Please try again.';box.classList.add('show')}finally{if(sb)sb.disabled=false}
    });
  });
})();
