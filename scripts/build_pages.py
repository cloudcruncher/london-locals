import re
"""Compose static pages from site/_head.html + bodies + site/_foot.html."""

import pathlib

S = pathlib.Path(__file__).resolve().parent.parent / "site"
HEAD, FOOT = (S.parent / "scripts/templates/_head.html").read_text(), (S.parent / "scripts/templates/_foot.html").read_text()

ICON_ID = """<svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><rect x="8" y="14" width="48" height="36" rx="8" fill="#bfe3da"/><circle cx="24" cy="30" r="6" fill="#0f4a3d"/><path d="M14 44c1-7 6-9 10-9s9 2 10 9z" fill="#0f4a3d"/><rect x="38" y="25" width="14" height="3" rx="1.5" fill="#0f4a3d"/><rect x="38" y="32" width="10" height="3" rx="1.5" fill="#0f4a3d"/><path d="M44 42l4 4 8-9" stroke="#ff6b4a" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
ICON_PASS = """<svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><rect x="14" y="6" width="36" height="52" rx="8" fill="#0f4a3d"/><rect x="19" y="14" width="26" height="14" rx="4" fill="#ff6b4a"/><rect x="21" y="34" width="22" height="18" rx="3" fill="#fbf6ec"/><path d="M24 37h5v5h-5zM35 37h5v5h-5zM24 46h5v4h-5zM33 45h3v3h-3zM38 47h2v3h-2z" fill="#0f4a3d"/></svg>"""
ICON_SAVE = """<svg class="ico" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="24" fill="#f2b84b"/><circle cx="32" cy="32" r="18" fill="none" stroke="#fbf6ec" stroke-width="3" stroke-dasharray="4 4"/><text x="32" y="40" text-anchor="middle" font-size="24" font-weight="700" font-family="Georgia" fill="#0f4a3d">%</text><path d="M48 10l3 6 6 1-4 5 1 6-6-3-6 3 1-6-4-5 6-1z" fill="#ff6b4a"/></svg>"""
SKYLINE = """<svg class="skyline" viewBox="0 0 1200 120" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0 120V88h40V70h30v18h26V54h20V40h18v14h22v34h34V76h30V58h26v30h40V66h24V30h10V14h6v16h10v36h26v22h40V80h36V60h28v28h30V72h40V50h18V36h14v14h18v38h44V74h30V56h24v32h40V84h36V64h28V22h4V8h4v14h4v42h24v24h46V70h30V52h26v36h36V78h38V62h26v26h40V74h30V90h34v30z" opacity=".9"/></svg>"""

INDEX = f"""
<main id="main">
<section class="hero"><div class="wrap">
<div>
<span class="eyebrow">London &middot; launching Hackney, Lewisham, Lambeth</span>
<h1>Your postcode is the key to <em>your high street.</em></h1>
<p class="lead">Free neighbourhood rewards for people who live here, from the cafés, gyms, bars, classes and venues on your doorstep. Verified residents. Real savings. Money that stays local.</p>
<div class="cta"><a class="btn" href="#join">Get early access</a><a class="btn alt" href="business.html">I run a local business</a></div>
<span class="badge-live">Early access open &middot; no spam, one email before launch</span>
</div>
<div class="mapbox" >
<canvas id="map" role="img" aria-label="Animated dot map of every food and drink premises in London"></canvas>
<div class="tip" id="tip"></div>
<div class="mapnote">Every dot is a real food and drink premises (FSA register). Orange: launch boroughs. Hover or tap to explore.</div>
<div class="phone" aria-hidden="true"><div class="scr"><div class="pass"><b>Locals pass</b>Verified resident<div class="qr"></div></div><div class="mini"><i>Example</i> Free pastry with any coffee</div><div class="mini"><i>Example</i> First class free</div><div class="mini"><i>Example</i> 2-for-1 Tuesdays</div></div></div>
</div>
</div></section>
<div class="marquee" aria-hidden="true"><div><span>Cafés</span><span>Pubs and bars</span><span>Restaurants</span><span>Gyms and studios</span><span>Salons and barbers</span><span>Bookshops</span><span>Cinemas and theatres</span><span>Classes and workshops</span><span>Markets</span><span>Cafés</span><span>Pubs and bars</span><span>Restaurants</span><span>Gyms and studios</span><span>Salons and barbers</span><span>Bookshops</span><span>Cinemas and theatres</span><span>Classes and workshops</span><span>Markets</span></div></div>
<div class="stats"><div class="wrap">
<div><b data-count="42399">0</b><span>food and drink venues on the London map</span></div>
<div><b data-count="33">0</b><span>London boroughs we will grow into, starting with three</span></div>
<div><b data-count="3">0</b><span>launch boroughs, early access open</span></div>
<div><b data-pre="£" data-count="0">£0</b><span>cost to residents</span></div>
</div></div>

<section id="how"><div class="wrap">
<span class="num">HOW IT WORKS</span><h2 class="reveal">Three taps from your sofa to your local.</h2>
<div class="steps">
<div class="card reveal">{ICON_ID}<span class="num">01</span><h3>Prove you live here</h3><p>Sign up with your postcode, then verify once (method to be confirmed before launch). Only verified residents will get the pass, which is why local businesses can trust the scheme.</p></div>
<div class="card reveal">{ICON_PASS}<span class="num">02</span><h3>Get your pass</h3><p>At launch your pass will live in Apple or Google Wallet, with a rotating QR code designed to stop screenshots being reused. No paper cards.</p></div>
<div class="card reveal">{ICON_SAVE}<span class="num">03</span><h3>Show it, save, repeat</h3><p>Show it at the till. Perks are designed around quiet times and first visits, so venues welcome you and you save without the small print.</p></div>
</div></div></section>

<section id="offers" style="background:var(--paper)"><div class="wrap">
<span class="num">DEALS NEAR YOU</span><h2 class="reveal">Real offers, already out there.</h2>
<p class="lead">Venues in Hackney, Lewisham and Lambeth already advertise these deals publicly. They are not Locals partners and have not endorsed Locals. Confirm with the venue before you go.</p>
<div class="dir" id="teaser" aria-live="polite"></div>
<p style="margin-top:1.5rem"><a class="btn" href="offers.html">See all local offers</a></p>
<h3 style="margin-top:3rem">Resident Days <span class="fine">(planned, no venues confirmed yet)</span></h3>
<p>Days when local museums, theatres and leisure centres open their doors to residents.</p>
<div class="days">
<div class="day reveal"><b>Heritage Day</b>Free entry to local museums and historic buildings</div>
<div class="day reveal"><b>Carers Day</b>Free or heavily discounted perks for unpaid carers</div>
<div class="day reveal"><b>Over-60s Day</b>Events and offers for older neighbours</div>
<div class="day reveal"><b>Kids Free</b>Family activities where children go free</div>
</div>
</div></section>

<section><div class="wrap split">
<div>
<span class="num">FOR BUSINESSES</span><h2 class="reveal">Fill your quiet days with people who live round the corner.</h2>
<p>You choose the offer, the days and the cap. Residents show a code at your till and you see how many came, whether they were new, what they spent and whether it paid off. Listing is free; you only pay if you want more.</p>
<div class="cta"><a class="btn" href="business.html">See how it pays back</a></div>
</div>
<div class="dash reveal">
<h4>Sample dashboard &middot; illustrative numbers</h4>
<div class="kpis"><div><b>148</b><small>redemptions</small></div><div><b>62%</b><small>new customers</small></div><div><b>£4.1k</b><small>tracked spend</small></div></div>
<div class="bar"><span>Mon</span><i data-w="35"></i><b>22</b></div>
<div class="bar"><span>Tue</span><i data-w="60"></i><b>38</b></div>
<div class="bar"><span>Wed</span><i data-w="52"></i><b>33</b></div>
<div class="bar"><span>Thu</span><i data-w="44"></i><b>28</b></div>
<div class="bar"><span>Fri</span><i data-w="18"></i><b>12</b></div>
<div class="bar"><span>Sat</span><i data-w="25"></i><b>15</b></div>
</div>
</div></section>

<section id="boroughs"><div class="wrap">
<span class="num">WHERE</span><h2 class="reveal">Starting in three boroughs.</h2>
<p class="lead">Pick yours. The map shows its venues, and we use the sign-up count to decide the launch order.</p>
<div class="chips" id="bchips" role="group" aria-label="Borough"></div>
</div></section>

<section id="join" style="background:var(--paper)"><div class="wrap split">
<div><span class="num">EARLY ACCESS</span><h2>Be first on your high street.</h2><p>Free. We email once, before your borough launches, with your pass and the first offers.</p>
<ul><li>Verified-resident pass in your wallet</li><li>Offers from independents near you</li><li>Resident Days and neighbourhood picks</li></ul></div>
<form class="f" data-signup="resident" novalidate>
<label>Name<input name="name" autocomplete="name" required></label>
<label>Email<input name="email" type="email" autocomplete="email" required></label>
<div class="row"><label>Postcode<input name="postcode" autocomplete="postal-code" required></label>
<label>Borough<select name="borough" id="bsel"><option>Hackney</option><option>Lewisham</option><option>Lambeth</option><option>Another London borough</option></select></label></div>
<input name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
<label style="font-weight:400;display:flex;gap:.6rem"><input type="checkbox" name="consent" required style="width:auto">I agree to be emailed about Locals. See the <a href="privacy.html">privacy notice</a>.</label>
<button class="btn" type="submit">Join the list</button>
<div class="msg" role="status"></div>
</form>
</div></section>
</main>
<script src="js/model.js"></script>
<script src="js/map.js"></script>
<script src="js/main.js"></script>
<script src="js/teaser.js"></script>
<script>
(async()=>{{
  const meta=await fetch('data/boroughs.json').then(r=>r.json()), M=LocalsModel;
  const chips=document.getElementById('bchips'),sel=document.getElementById('bsel');
  LOCALS.LAUNCH_BOROUGHS.forEach(n=>{{const b=meta.boroughs.find(x=>x.name===n),c=document.createElement('button');c.type='button';c.className='chip';c.setAttribute('aria-pressed','false');
    c.textContent=n+' \\u00b7 '+b.venues.toLocaleString('en-GB')+' venues';
    c.onclick=()=>{{chips.querySelectorAll('.chip').forEach(x=>x.setAttribute('aria-pressed','false'));c.setAttribute('aria-pressed','true');sel.value=n;window.highlightBorough&&highlightBorough(n);document.querySelector('.hero').scrollIntoView({{behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}})}};chips.appendChild(c)}});
}})();
</script>
"""

BUSINESS = """
<main id="main">
<section style="padding-top:3.5rem"><div class="wrap split">
<div>
<span class="eyebrow">For local businesses</span>
<h1 style="font-size:clamp(2.2rem,5vw,3.8rem)">New customers on your quiet days. Proof it worked.</h1>
<p class="lead">Offer something to verified residents of your borough. We show you how many residents redeemed, what it cost you and, where you confirm it, what they spent. Free to list; pay only if you want more.</p>
<div class="cta"><a class="btn" href="#apply">Become a founding partner</a><a class="btn alt" href="#roi">Try the ROI calculator</a></div>
<p class="fine">Founding partners (first 50 businesses per borough to apply, while places last) will get the Growth tier free for six months from their borough's launch. Terms will be confirmed in writing before you sign up.</p>
</div>
<div class="dash"><h4>What you get</h4>
<div class="bar"><span style="width:auto">&#10003;</span> Verified residents only, with a rotating QR so passes cannot be shared (at launch)</div>
<div class="bar"><span style="width:auto">&#10003;</span> You set the days, times, cap and first-visit rules</div>
<div class="bar"><span style="width:auto">&#10003;</span> Scan from any phone. No hardware at launch: scan from any phone</div>
<div class="bar"><span style="width:auto">&#10003;</span> Dashboard: new vs returning, spend, cost of discounts (at launch)</div>
<div class="bar"><span style="width:auto">&#10003;</span> Planned: borough monthly email and a monthly featured slot</div></div>
</div></section>

<section style="background:var(--paper)"><div class="wrap">
<span class="num">PRICING</span><h2>Start free. Grow when it pays.</h2>
<div class="steps">
<div class="card"><h3>Listed</h3><div class="big" style="font:700 2.4rem Georgia,serif">£0</div><p>One offer, your page, scan-to-redeem, basic counts.</p></div>
<div class="card" style="border-color:var(--coral)"><h3>Growth</h3><div class="big" style="font:700 2.4rem Georgia,serif">£39<small style="font-size:1rem">/month</small></div><p>Several offers, full dashboard, featured slot in the monthly email. Free for six months for founding partners.</p></div>
<div class="card"><h3>Pay on results</h3><div class="big" style="font:700 2.4rem Georgia,serif">2%</div><p>Of spend tracked through the pass instead of a flat fee. No customers, no bill.</p></div>
</div>
<p class="fine">Launch pricing is provisional and may change before public launch.</p>
</div></section>

<section id="roi"><div class="wrap">
<span class="num">DOES IT PAY?</span><h2>Work it out for your venue.</h2>
<div class="ctl" id="roictl"></div>
<div class="hl" id="roiout"></div>
<p class="note" id="roinote"></p>
</div></section>

<section id="apply" style="background:var(--paper)"><div class="wrap split">
<div><span class="num">APPLY</span><h2>Become a founding partner.</h2><p>Tell us a bit about you. We aim to reply within a few working days and will help you write an offer that works on your quiet days.</p>
<h3>Offer ideas that protect margin</h3><ul><li>Free coffee with a pastry, Mon to Thu afternoons</li><li>First class free (studios)</li><li>10% off first visit (salons, barbers)</li><li>Kids eat free on Sundays with a paying adult</li></ul></div>
<form class="f" data-signup="business" novalidate>
<div class="row"><label>Business name<input name="business" required></label><label>Your name<input name="name" required></label></div>
<div class="row"><label>Email<input name="email" type="email" required></label><label>Postcode<input name="postcode" required></label></div>
<label>Type<select name="type"><option>Café or bakery</option><option>Restaurant or takeaway</option><option>Pub or bar</option><option>Gym or studio</option><option>Salon or barber</option><option>Shop</option><option>Venue or attraction</option><option>Other</option></select></label>
<label>What could you offer? (optional)<textarea name="offer" rows="3"></textarea></label>
<input name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
<label style="font-weight:400;display:flex;gap:.6rem"><input type="checkbox" name="consent" required style="width:auto">I agree to be contacted about Locals. See the <a href="privacy.html">privacy notice</a>.</label>
<button class="btn" type="submit">Send application</button><div class="msg" role="status"></div>
</form>
</div></section>
</main>
<script src="js/main.js"></script>
<script>
(()=>{
 const f=[['avg','Average spend per visit (£)',5,120,1,20,v=>'£'+v],['vis','Redemptions per month',5,400,5,60,v=>v],['neu','Share who are new or off-peak customers',0,100,1,45,v=>v+'%'],['dis','Discount you give',0,50,1,15,v=>v+'%'],['mar','Contribution margin on extra sales',20,80,1,55,v=>v+'%'],['fee','Plan',0,2,1,1,v=>['Listed (free)','Growth £39/mo','Pay 2% of tracked spend'][v]]];
 const c=document.getElementById('roictl'),S={};
 f.forEach(([id,l,mn,mx,st,d,fmt])=>{S[id]=d;const e=document.createElement('label');e.innerHTML=`${l}<output></output><input type="range" min="${mn}" max="${mx}" step="${st}" value="${d}">`;c.appendChild(e);
  const o=e.querySelector('output'),i=e.querySelector('input');const u=()=>{S[id]=+i.value;o.textContent=fmt(S[id]);calc()};i.oninput=u;o.textContent=fmt(d)});
 function calc(){
  const spend=S.vis*S.avg, listPrice=S.avg/(1-S.dis/100), disc=S.vis*(listPrice-S.avg);
  const extra=spend*S.neu/100*S.mar/100, fee=S.fee==1?39:S.fee==2?spend*.02:0, net=extra-disc-fee;
  const g=n=>(n<0?'-':'')+'£'+Math.round(Math.abs(n)).toLocaleString('en-GB');
  document.getElementById('roiout').innerHTML=`<div><b>${g(spend)}</b>spend through the pass</div><div><b>${g(extra)}</b>extra margin from new or off-peak customers</div><div><b class="neg">-${g(disc)}</b>discounts given</div><div><b class="neg">-${g(fee)}</b>Locals fee</div><div><b class="${net>=0?'pos':'neg'}">${g(net)}</b>net per month</div>`;
  document.getElementById('roinote').textContent=net>=0?'It pays at these settings. The lever that matters most is how many redemptions are genuinely new or off-peak customers.':'It does not pay at these settings. Lower the discount, restrict to quiet times or first visits, or only count customers you would not have had anyway.';
 }
 calc();
})();
</script>
"""

MONEY = """
<main id="main">
<section style="padding-top:3rem"><div class="wrap">
<span class="eyebrow">The money model</span>
<h1 style="font-size:clamp(2.2rem,5vw,3.8rem)">Show me the money.</h1>
<p class="lead">Built on the real number of food and drink venues in each borough (FSA register) and mid-2024 populations for six boroughs (ONS, via citypopulation.de). Everything else is an assumption you can change. The model is deliberately honest: the cautious case loses money.</p>
<div class="seg" role="group" aria-label="Scenario"><button data-s="cautious" aria-pressed="false">Cautious</button><button data-s="base" aria-pressed="true">Base</button><button data-s="stretch" aria-pressed="false">Stretch</button></div>
<h3>Boroughs <small class="fine">(first borough starts month 1, then one every 3 months)</small></h3>
<div class="chips" id="chips"></div>
<p><button class="chip" id="launch3" type="button">Launch three</button> <button class="chip" id="allLondon" type="button">All of London</button></p>
</div></section>

<section style="padding-top:0"><div class="wrap">
<div class="hl three">
<div><small>Year 1 revenue</small><b id="y1">&hellip;</b></div>
<div><small>Year 2 revenue</small><b id="y2">&hellip;</b></div>
<div><small>Year 3 revenue</small><b id="y3">&hellip;</b></div>
<div><small>Cash you must fund (low point)</small><b id="peak" class="neg">&hellip;</b><small id="peakNote"></small></div>
<div><small>Monthly revenue covers monthly cost</small><b id="be">&hellip;</b></div>
<div><small>Cumulative cash back to zero</small><b id="payback">&hellip;</b></div>
</div>
<div class="dash"><h4>Cumulative cash, 36 months (green) &middot; annualised revenue (gold dashed) &middot; annualised cost (orange dotted)</h4><div id="chart"></div></div>
</div></section>

<section style="background:var(--paper)"><div class="wrap split">
<div><span class="num">WHO PAYS</span><h2>Steady-state revenue: <span id="rev"></span> a year</h2><p>Against running costs of <b id="cost"></b> a year for <b id="nb"></b> boroughs. Steady state means once every borough is a year or more past launch.</p>
<div id="streams"></div><p class="note" id="mix"></p></div>
<div><span class="num">WHO WINS</span><h2>Everyone gets paid, or it does not work.</h2>
<div class="hl" style="grid-template-columns:1fr 1fr">
<div><small>Residents save</small><b id="w_res" class="pos">&hellip;</b></div>
<div><small>Venues keep (net)</small><b id="w_biz">&hellip;</b></div>
<div><small>Locals revenue</small><b id="w_us">&hellip;</b></div>
<div><small>Spent locally via pass</small><b id="w_track">&hellip;</b></div>
</div><p class="note" id="bizNote"></p></div>
</div></section>

<section><div class="wrap">
<span class="num">TUNE IT</span><h2>Every assumption, in your hands.</h2>
<div class="ctl" id="sliders"></div>
<h3 style="margin-top:2.5rem">By borough</h3>
<div class="tblwrap"><table class="tbl"><thead><tr><th>Borough</th><th>Venues (data)</th><th>Listed</th><th>Members</th><th>Spend via pass</th><th>Revenue</th></tr></thead><tbody id="tbody"></tbody></table></div>
<p class="fine">* No ONS population retrieved for this borough; 280,000 assumed. Venue counts are real (FSA register, data as of <span class="asof"></span>, 4 food and drink types). Gyms, salons, shops and attractions are not counted yet, so real supply is larger.</p>
<div class="note"><b>Read this before believing any number.</b> Penetration, conversion, redemption frequency, new-customer share, sponsor and council income are untested assumptions. The first job of the pilot is to replace them with measured values. Costs assume a lean team (about £260k fixed plus £20k per borough) and exclude founder pay beyond that.</div>
</div></section>
</main>
<script src="js/model.js"></script>
<script src="js/main.js"></script>
<script src="js/money.js"></script>
"""

OFFERS = """
<main id="main">
<section class="pagehead"><div class="wrap">
<span class="num">LIVE DIRECTORY</span><h1>Real local offers, found for you.</h1>
<p class="lead">Offers that independent venues in Hackney, Lewisham and Lambeth already advertise publicly. Every card links to the venue's own page so you can check it.</p>
<p class="fine">These venues are not Locals partners yet and have not paid or asked to be listed. Offers change: always confirm with the venue. Venue owner? <a href="business.html#apply">Claim your listing</a> to edit it, or email <a href="mailto:REMOVAL_EMAIL">REMOVAL_EMAIL</a> to have it removed within 48 hours.</p>
</div></section>
<section><div class="wrap">
<div class="chips" id="bchips" role="group" aria-label="Borough"></div>
<div class="chips" id="tchips" role="group" aria-label="Venue type"></div>
<label class="sr" for="q">Search offers</label><input id="q" type="search" placeholder="Search by name, area or offer" style="width:100%;max-width:420px;padding:.7rem 1rem;border-radius:12px;border:1.5px solid var(--line);background:var(--paper);color:var(--ink)">
<p id="count" class="fine" aria-live="polite"></p>
<div class="offers" id="grid"></div>
<p class="fine asof" id="asof"></p>
</div></section>
</main>
<script src="js/offers.js"></script>
"""

PRIVACY = """
<main id="main"><section><div class="wrap" style="max-width:720px">
<h1 style="font-size:2.6rem">Privacy notice (draft)</h1>
<p class="note"><b>Early-access notice. Not yet legally reviewed.</b> <span id="ctrl">Data controller: Robin Saini, sole trader, London. Contact: REMOVAL_EMAIL. ICO registration number: [to be added once registered].</span></p>
<h3>What we collect</h3><p>Name, email, postcode and borough (residents); business name, contact, postcode and type (businesses). Nothing else on this site collects personal data. The site sets no cookies and uses no advertising trackers. If privacy-friendly, cookieless analytics (Plausible) is switched on, this notice will say so. Sign-up forms are processed by our form provider, named here before launch. Not used: third-party trackers. Our web host (GitHub Pages) processes visitor IP addresses in its server logs. If a form backend is not yet connected, a submission is held only in your own browser storage.</p>
<h3>Why</h3><p>To tell you when Locals launches in your borough, to decide launch order, and to contact businesses who applied. Legal basis: your consent. You can withdraw it at any time. When the full service launches, businesses will see aggregated redemption counts and spend; any further disclosure of who redeemed will be covered by an updated notice before it happens.</p>
<h3>Who sees it</h3><p>Only the Locals team and our form and email providers acting on our instructions. We will never sell personal data. Sponsors and councils receive anonymised, aggregated figures only.</p>
<h3>Keeping it</h3><p>Until launch plus 12 months, or until you ask us to delete it.</p>
<h3>Your rights</h3><p>Access, correction, deletion, objection, and complaint to the Information Commissioner's Office.</p>
</div></section></main>
<script src="js/main.js"></script>
"""

NOTFOUND = """
<main id="main">
<section class="pagehead"><div class="wrap"><span class="num">404</span><h1>That page has moved on.</h1>
<p class="lead">Try the <a href="index.html">resident home page</a>, the <a href="offers.html">offers directory</a> or the <a href="business.html">business page</a>.</p></div></section></main>
"""

pages = {
    "index.html": (
        "Locals: free rewards for London residents, from your own high street",
        "Verified-resident rewards from local businesses. Launching in Hackney, Lewisham and Lambeth.",
        INDEX,
    ),
    "business.html": (
        "Locals for businesses: new local customers, with proof",
        "Offer deals to verified residents of your borough and see exactly what it earns you.",
        BUSINESS,
    ),
    "money.html": (
        "Locals: the money model",
        "Partner briefing: modelled business case built on real London venue data.",
        MONEY,
    ),
    "offers.html": (
        "Locals: real local offers in Hackney, Lewisham and Lambeth",
        "Publicly advertised offers from independent London venues, each linked to its source.",
        OFFERS,
    ),
    "404.html": ("Locals: page not found", "Page not found.", NOTFOUND),
    "privacy.html": (
        "Locals: privacy notice (draft)",
        "How Locals handles your data.",
        PRIVACY,
    ),
}
_m = re.search(r'SITE_URL:\s*"([^"]*)"', (S / "config.js").read_text())
site0 = (_m.group(1) if _m else "").rstrip("/")
NAV_RES = '<nav class="main" aria-label="Main"><a class="hide-sm" href="index.html#how">How it works</a><a href="offers.html">Offers</a><a href="index.html#boroughs">Boroughs</a><a class="aud" href="business.html">For businesses &rarr;</a><a class="btn sm" href="index.html#join">Join free</a></nav>'
NAV_BIZ = '<nav class="main" aria-label="Main"><a href="business.html">Why list</a><a href="business.html#roi">Your ROI</a><a class="aud" href="index.html">&larr; Resident site</a><a class="btn sm" href="business.html#apply">Get listed</a></nav>'
BIZ = {"business.html", "money.html"}
_e = re.search(r'CONTACT_EMAIL:\s*"([^"]*)"', (S / "config.js").read_text())
CONTACT = _e.group(1) if _e and _e.group(1) else "[contact email to be added]"
for fn, (t, d, body) in pages.items():
    body = body.replace("REMOVAL_EMAIL", CONTACT)
    html = (
        HEAD.replace("%NAV%", NAV_BIZ if fn in BIZ else NAV_RES).replace("%BODYCLS%", "biz" if fn in BIZ else "res").replace("%OGIMG%", (site0 + "/" if site0 else "") + "img/og.png").replace("%ROBOTS%", '<meta name="robots" content="noindex">' if fn == "money.html" else "").replace("%TITLE%", t).replace("%DESC%", d)
        + body
        + FOOT.split('<script src="config.js"></script>')[0]
        + "</body></html>\n"
    )
    # config.js must load before page scripts: inject at top of body scripts
    html = html.replace(
        '<script src="js/', '<script src="config.js"></script>\n<script src="js/', 1
    )
    (S / fn).write_text(html)
print("built", list(pages))

# robots.txt and sitemap.xml (sitemap only when SITE_URL is set in config.js)
import re as _re
cfg = (S / "config.js").read_text()
m = _re.search(r'SITE_URL:\s*"([^"]*)"', cfg)
site = (m.group(1) if m else "").rstrip("/")
robots = "User-agent: *\nAllow: /\n"
if site:
    robots += f"Sitemap: {site}/sitemap.xml\n"
    urls = [f for f in pages if f != "404.html"]
    (S / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"<url><loc>{site}/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
(S / "robots.txt").write_text(robots)
