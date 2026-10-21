const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const code=fs.readFileSync('tracking.js','utf8');
function run({query='',referrer='',saved=null,blocked=false,legacy=false,href='https://link.amazon/B07uqwd3T'}={}) {
 const listeners={}, values={};
 const link={href,closest:()=>legacy?{querySelector:selector=>selector==='h3'?{textContent:'Brickell Clay'}:selector==='.k'?{textContent:'Styling'}:{getAttribute:()=>'/assets/shop/brickell.jpg'}}:null,dataset:legacy?{}:{productId:'brickell',productName:'Brickell Clay',productCategory:'Styling'},addEventListener:(k,v)=>listeners[k]=v};
 const context={URL,URLSearchParams,Date,location:{search:query,hostname:'www.theqsalonsrq.com'},sessionStorage:{getItem:()=>{if(blocked)throw Error();return JSON.stringify(saved)},setItem:(k,v)=>values[k]=JSON.parse(v)},document:{referrer,createElement:()=>({}),head:{appendChild:s=>values.loader=s.src},querySelectorAll:()=>[link]},window:{}};
 vm.runInNewContext(code,context); listeners.click();
 const event=Array.from(context.window.dataLayer.at(-1));
 assert.equal(event[1],'amazon_click');assert.equal(event[2].product_name,'Brickell Clay');
 return {link,event:event[2],saved:Object.values(values).find(x=>x?.channel),values};
}
const cases=[
 [{query:'?utm_source=google&utm_medium=gbp'},'google'],
 [{query:'?utm_source=FB'},'facebook'],
 [{query:'?utm_source=instagram'},'instagram'],
 [{referrer:'https://l.facebook.com/l.php'},'facebook'],
 [{referrer:'https://l.instagram.com/'},'instagram'],
 [{referrer:'https://www.google.com/search'},'google'],
 [{referrer:'https://google.com.evil.example/'},'website'],
 [{saved:{channel:'google',time:Date.now()-1000},referrer:'https://www.theqsalonsrq.com/'},'google'],
 [{saved:{channel:'google',time:Date.now()-1900000}},'website'],
 [{saved:{channel:'google',time:Date.now()-1000},query:'?utm_source=unknown'},'website'],
 [{query:'?utm_source=google',blocked:true},'google'],
 [{saved:{channel:'__proto__',time:Date.now()-1000}},'website'],
 [{query:'?utm_source=__proto__'},'website']
];
for(const [input,want] of cases) {const got=run(input);assert.equal(got.event.affiliate_channel,want,JSON.stringify(input));assert.equal(got.link.href,input.href||'https://link.amazon/B07uqwd3T');assert.equal(got.event.affiliate_link_status,'short_link_unverified');assert.equal(got.event.affiliate_tracking_id,undefined);}
const full=run({query:'?utm_source=google',href:'https://www.amazon.com/dp/B000000001?tag=old-20&th=1'});
assert.equal(new URL(full.link.href).searchParams.get('tag'),'qsalongoogle-20');assert.equal(new URL(full.link.href).searchParams.get('th'),'1');assert.equal(full.event.affiliate_link_status,'tagged');
const legacy=run({query:'?utm_source=google',legacy:true});assert.equal(legacy.event.product_id,'brickell');assert.equal(legacy.event.product_category,'Styling');
console.log('Passed 13 source attribution cases, shortened link preservation, product events, and canonical tag replacement.');
