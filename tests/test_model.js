const M = require('../site/js/model.js'), d = require('../site/data/boroughs.json').boroughs, assert = require('assert');
const three = d.filter(b => ['Hackney', 'Lewisham', 'Lambeth'].includes(b.name));
const run = s => M.run(three, M.SCENARIOS[s]);
const caut = run('cautious'), base = run('base'), str = run('stretch');
assert.equal(d.length, 33);
assert.equal(d.reduce((a, b) => a + b.venues, 0), 42399);
assert(caut.tot.revenue < base.tot.revenue && base.tot.revenue < str.tot.revenue, 'scenario ordering');
assert(caut.peakFunding > base.peakFunding && base.peakFunding > str.peakFunding, 'funding need ordering');
assert(str.breakeven > 0, 'stretch breaks even');
// stream totals must equal reported revenue (guards the double-count bug)
for (const r of [caut, base, str]) assert(Math.abs(r.tot.sub + r.tot.perf + r.tot.spon + r.tot.cont - r.tot.revenue) < 1e-6, 'streams sum');
// no listed venues -> no tracked spend, no fees, no subscriptions
const none = M.run(three, Object.assign({}, M.SCENARIOS.base, { listedPct: 0 }));
assert(none.tot.tracked === 0 && none.tot.perf === 0 && none.tot.sub === 0, 'zero supply means zero tracked spend');
// steady state is not below year 3 now that the ramp is capped at 1
assert(base.yr[2] <= base.tot.revenue * 1.0001, 'year 3 does not exceed steady state');
// sliders at zero must not produce NaN
const zero = M.run(three, Object.assign({}, M.SCENARIOS.base, { pen: 0, price: 0, spon: 0, cont: 0, fee: 0 }));
assert(Number.isFinite(zero.tot.revenue) && zero.months.every(m => Number.isFinite(m.cum)), 'finite at zero');
console.log('model ok: base steady revenue', Math.round(base.tot.revenue), 'peak funding', Math.round(base.peakFunding), 'stretch breakeven month', str.breakeven);
