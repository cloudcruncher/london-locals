// Animated London map: every dot is a real food and drink premises from the FSA register (via london-pulse).
(async function(){
  const canvas=document.getElementById('map'); if(!canvas) return;
  const tip=document.getElementById('tip'), ctx=canvas.getContext('2d');
  const rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const [meta,buf]=await Promise.all([fetch('data/boroughs.json').then(r=>r.json()),fetch('data/points.bin').then(r=>r.arrayBuffer())]);
  const n=buf.byteLength/5, dv=new DataView(buf), X=new Float32Array(n),Y=new Float32Array(n),B=new Uint8Array(n);
  for(let i=0;i<n;i++){X[i]=dv.getUint16(i*5,true)/65535;Y[i]=1-dv.getUint16(i*5+2,true)/65535;B[i]=dv.getUint8(i*5+4)}
  const launch=new Set(window.LOCALS.LAUNCH_BOROUGHS), names=meta.boroughs.map(b=>b.name);
  const isLaunch=meta.boroughs.map(b=>launch.has(b.name));
  let sel=-1, W=0,H=0,dpr=1,t0=performance.now();
  // distance from centre for the reveal sweep
  const D=new Float32Array(n); for(let i=0;i<n;i++)D[i]=Math.hypot(X[i]-.5,(Y[i]-.5)*0.8);
  function size(){const r=canvas.getBoundingClientRect();dpr=Math.min(2,devicePixelRatio||1);W=canvas.width=r.width*dpr;H=canvas.height=r.height*dpr}
  let draw;const redraw=()=>{if(rm&&draw)requestAnimationFrame(draw)};addEventListener('resize',()=>{size();redraw()});size();
  // bucket points by class so each frame only touches what it draws
  const cls=i=>isLaunch[B[i]]?1:0, lists=[[],[]];
  for(let i=0;i<n;i++)lists[cls(i)].push(i);
  let visible=true;new IntersectionObserver(e=>{visible=e[0].isIntersecting;if(visible&&!rm)requestAnimationFrame(draw)}).observe(canvas);
  draw=function(now){
    const t=(now-t0)/1000, reveal=rm?9:Math.min(1.1,t/2.6), lim=reveal*.62;
    ctx.clearRect(0,0,W,H);
    const s=Math.max(1.1*dpr,W/520);
    [[lists[0],'#bfe3da',.5],[lists[1],'#ff8a5c',.95]].forEach(([L,col,al])=>{
      ctx.fillStyle=col;
      for(let q=0;q<L.length;q++){const i=L[q]; if(B[i]===sel||D[i]>lim)continue;
        ctx.globalAlpha=al*(rm?1:(.75+.25*Math.sin(t*2+i*12.9898)));
        ctx.fillRect(X[i]*W-s/2,Y[i]*H-s/2,s,s)}
    });
    if(sel>=0){ctx.fillStyle='#fff';ctx.globalAlpha=1;const z=s*1.6;
      for(let i=0;i<n;i++)if(B[i]===sel&&D[i]<=lim)ctx.fillRect(X[i]*W-z/2,Y[i]*H-z/2,z,z)}
    ctx.globalAlpha=1;
    if(!rm&&visible)requestAnimationFrame(draw)
  }
  requestAnimationFrame(draw);
  function pick(ev){
    const r=canvas.getBoundingClientRect(), x=(ev.clientX-r.left)/r.width, y=(ev.clientY-r.top)/r.height;
    let best=-1,bd=1e9; for(let i=0;i<n;i++){const d=(X[i]-x)**2+((Y[i]-y)*.79)**2;if(d<bd){bd=d;best=i}}
    return bd<0.0009?B[best]:-1;
  }
  const onPoint=ev=>{
    const b=pick(ev); sel=b;
    if(b<0){tip.style.opacity=0;return}
    const m=meta.boroughs[b], r=canvas.getBoundingClientRect();
    tip.innerHTML=`<b>${m.name}</b><br>${m.venues.toLocaleString('en-GB')} food and drink venues${isLaunch[b]?' &middot; <b style="color:#d9482b">launch borough</b>':''}`;
    tip.style.left=(ev.clientX-r.left)+'px';tip.style.top=(ev.clientY-r.top)+'px';tip.style.opacity=1;redraw();
  };
  canvas.addEventListener('mousemove',onPoint);canvas.addEventListener('pointerdown',onPoint);
  canvas.addEventListener('mouseleave',()=>{sel=-1;tip.style.opacity=0});
  // external hook: chips choose a borough
  window.highlightBorough=name=>{sel=names.indexOf(name);redraw()};
  window.LOCALS_META=meta;
  document.dispatchEvent(new CustomEvent('locals-meta',{detail:meta}));
})();
