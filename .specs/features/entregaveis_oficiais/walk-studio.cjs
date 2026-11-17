/* Local browser walk: real controls, import/export and gallery links; no remote service. */
const {spawn} = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const assert = require('node:assert/strict');
const {pathToFileURL} = require('node:url');
const root = path.resolve(__dirname, '../../..');
const chrome = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const profile = fs.mkdtempSync(path.join(os.tmpdir(), 'eric-official-chrome-'));
const browser = spawn(chrome, ['--headless', '--disable-gpu', '--no-first-run', '--no-default-browser-check', '--remote-debugging-port=0', '--user-data-dir='+profile, 'about:blank'], {stdio:'ignore'});
let socket;
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
(async () => {
  const active = path.join(profile,'DevToolsActivePort');
  for(let i=0;i<150 && !fs.existsSync(active);i++) await sleep(100);
  assert(fs.existsSync(active),'Chrome did not expose a local debugging endpoint');
  const port = fs.readFileSync(active,'utf8').split('\n')[0];
  const targets = await (await fetch('http://127.0.0.1:'+port+'/json/list')).json();
  socket = new WebSocket(targets.find(t=>t.type==='page').webSocketDebuggerUrl);
  await new Promise((resolve,reject)=>{socket.addEventListener('open',resolve,{once:true});socket.addEventListener('error',reject,{once:true});});
  let sequence=0;const pending=new Map();
  socket.addEventListener('message',event=>{const data=JSON.parse(event.data);const p=pending.get(data.id);if(p){pending.delete(data.id);data.error?p.reject(data.error):p.resolve(data.result);}});
  const send=(method,params={})=>new Promise((resolve,reject)=>{const id=++sequence;pending.set(id,{resolve,reject});socket.send(JSON.stringify({id,method,params}));});
  const run=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
  const navigate=async file=>{await send('Page.navigate',{url:pathToFileURL(file).href});await sleep(300);for(let i=0;i<50;i++){if(await run('document.readyState')==='complete')return;await sleep(100);}throw new Error('Page did not load');};
  await navigate(path.join(root,'_LAYOUT_STUDIO/index.html'));
  const walks=[];
  for(const method of ['four_d','three_e','five_c']) {
    const type=method+'_official_presentation';
    await run(`document.querySelector('#deliverableType').value=${JSON.stringify(type)};document.querySelector('#deliverableType').dispatchEvent(new Event('change'));`);
    await run(`window.prompt=()=>JSON.stringify([{id:'remoto_x',label:'Explorar',meaning:'Compreender experiências',official_stage_ids:[]}]);document.querySelector('#configureStagesBtn').click();`);
    await run(`document.querySelector('#previewBtn').click()`);
    const payload=await run(`JSON.parse(document.querySelector('#previewContent').textContent)`);
    assert.equal(payload.applied_stages[0].id,'remoto_x');
    await run(`(()=>{document.querySelector('#previewCloseBtn').click();const dt=new DataTransfer();dt.items.add(new File([${JSON.stringify(JSON.stringify(payload))}],'test.layout.json',{type:'application/json'}));const input=document.querySelector('#importFile');input.files=dt.files;input.dispatchEvent(new Event('change'));})()`);
    await sleep(150);
    await run(`document.querySelector('#previewBtn').click()`);
    assert.equal(await run(`JSON.parse(document.querySelector('#previewContent').textContent).applied_stages[0].id`),'remoto_x');
    await run(`document.querySelector('#previewCloseBtn').click()`);
    walks.push(type+': selected, configured, exported, reimported');
  }
  await run(`document.querySelector('#drawModeBtn').click()`);
  const rect=await run(`(()=>{const r=document.querySelector('#page').getBoundingClientRect();return {x:r.x,y:r.y}})()`);
  await send('Input.dispatchMouseEvent',{type:'mousePressed',x:rect.x+35,y:rect.y+35,button:'left',clickCount:1});
  await send('Input.dispatchMouseEvent',{type:'mouseMoved',x:rect.x+180,y:rect.y+110,button:'left',buttons:1});
  await send('Input.dispatchMouseEvent',{type:'mouseReleased',x:rect.x+180,y:rect.y+110,button:'left',clickCount:1});
  assert.equal(await run(`document.querySelector('#slotCount').textContent`),'1');
  assert(await run(`Array.from(document.querySelectorAll('#slotList option')).some(o=>o.value==='execution_remoto_x')`));
  const output=path.join(__dirname,'evidence');fs.mkdirSync(output,{recursive:true});
  const png=await send('Page.captureScreenshot',{format:'png'});fs.writeFileSync(path.join(output,'studio-walk.png'),Buffer.from(png.data,'base64'));
  await navigate(path.join(root,'_GALERIA/index.html'));
  const galleryText=await run(`document.body.innerText`);
  assert(galleryText.includes('oficial') && galleryText.includes('depreciad'));
  for(const method of ['four_d','three_e','five_c']) for(const form of ['report','presentation']) {
    const kind=method+'_official_'+form;
    await run(`document.querySelector('button[data-kind="${kind}"]').click()`);
    assert(await run(`Array.from(document.querySelectorAll('iframe')).some(f=>f.getAttribute('src').includes(${JSON.stringify(kind)}))`));
    assert.equal(await run(`document.querySelector('#alert').hidden`),true);
  }
  fs.writeFileSync(path.join(output,'walk.json'),JSON.stringify({status:'PASS',studio:walks,slot:'drawn; configured data source available',gallery:'six official types and deprecated labels available'},null,2)+'\n');
  console.log('PASS: Studio configuration/import/export, data sources and gallery links');
})().catch(error=>{console.error(error);process.exitCode=1;}).finally(()=>{if(socket)socket.close();browser.kill();});
