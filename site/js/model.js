// Pure business-case model. All numbers are assumptions unless marked as data (venue counts, populations).
(function(root){
  const SCENARIOS={
    cautious:{listedPct:.04,paidPct:.15,pen:.01,active:.30,red:1.2,spend:26,newShare:.30,fee:.02,price:39,spon:15000,cont:0,disc:.12,margin:.55,pr:.5,cap:60},
    base:    {listedPct:.08,paidPct:.25,pen:.025,active:.40,red:1.5,spend:28,newShare:.45,fee:.02,price:39,spon:30000,cont:40000,disc:.12,margin:.55,pr:.5,cap:60},
    stretch: {listedPct:.15,paidPct:.35,pen:.05,active:.50,red:2.0,spend:30,newShare:.60,fee:.025,price:49,spon:45000,cont:60000,disc:.12,margin:.55,pr:.5,cap:60}
  };
  const COST={fixed:260000,perBorough:20000};
  const DEFAULT_POP=280000; // assumption for boroughs where no ONS figure was retrieved
  function steady(b,p){
    const pop=b.pop_2024||DEFAULT_POP, listed=b.venues*p.listedPct, paid=listed*p.paidPct;
    const sub=paid*p.price*12, members=pop*p.pen;
    const demand=members*p.active*p.red, supply=listed*p.cap; // redemptions/month, limited by what listed venues can serve
    const tracked=Math.min(demand,supply)*p.spend*12, perf=tracked*(1-p.paidPct)*p.pr*p.fee; // fee only on pay-on-results venues
    const savings=tracked*p.disc/(1-p.disc), incr=tracked*p.newShare;
    const bizGain=incr*p.margin-savings-sub-perf;
    return {name:b.name,venues:b.venues,pop,assumedPop:!b.pop_2024,listed,paid,members,tracked,sub,perf,spon:p.spon,cont:p.cont,savings,incr,bizGain};
  }
  function run(boroughs,p){
    const per=boroughs.map(b=>steady(b,p)), sum=k=>per.reduce((a,x)=>a+x[k],0);
    const tot={};['listed','paid','members','tracked','sub','perf','spon','cont','savings','incr','bizGain'].forEach(k=>tot[k]=sum(k));
    tot.revenue=tot.sub+tot.perf+tot.spon+tot.cont;
    tot.cost=COST.fixed+COST.perBorough*boroughs.length;
    // 36-month ramp
    const months=[];let cum=0,low=0,lowM=0,be=null,payback=null;const yr=[0,0,0],cy=[0,0,0];
    for(let t=0;t<36;t++){
      let rev=0,cost=COST.fixed/12;
      per.forEach((s,k)=>{
        const L=k===0?0:3+(k-1)*3, a=t-L;
        if(a>=0){
          const f=Math.min(1,(a+1)/12);
          rev+=(a>=6?s.sub/12*f:0)+s.perf/12*f; // founding partners: Growth tier free for 6 months
          if(a>=4)rev+=s.spon/12*Math.min(1,(a-3)/6);
          if(a>=6)rev+=s.cont/12*Math.min(1,(a-5)/6);
          cost+=COST.perBorough/12;
        }
      });
      cum+=rev-cost; yr[Math.floor(t/12)]+=rev; cy[Math.floor(t/12)]+=cost;
      if(cum<low){low=cum;lowM=t}
      if(be===null&&rev>=cost&&t>0)be=t+1;
      if(payback===null&&cum>=0&&t>6)payback=t+1;
      months.push({t:t+1,rev,cost,cum});
    }
    return {per,tot,months,yr,cy,peakFunding:-low,peakMonth:lowM+1,breakeven:be,payback};
  }
  const api={SCENARIOS,COST,DEFAULT_POP,run,steady};
  if(typeof module!=='undefined')module.exports=api;else root.LocalsModel=api;
})(this);
