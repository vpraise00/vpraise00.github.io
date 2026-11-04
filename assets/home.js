(function () {
 'use strict';
 const R=window.Radar;
 let papers=[], config={}, data={};
 let channel='all', view='all', search='', sort='latest';
 const $=(s,root=document)=>root.querySelector(s);
 const $$=(s,root=document)=>[...root.querySelectorAll(s)];
 const e=R.esc;
 const category=id=>R.getCategories(config).find(x=>x.id===id)||{id,label:id.toUpperCase(),color:'#82959e'};
 const chip=(id,cl='cat-badge')=>{const c=category(id);return `<span class="${cl}" style="--cat-color:${R.safeColor(c.color)}">${e(c.label)}</span>`;};
 const isNote=p=>Boolean(R.note(p.id).trim()||R.getHighlights(p.id).length);
 const isNew=p=>R.ageDays(p.published)>=0&&R.ageDays(p.published)<=14;
 function counters(){
  const fresh=papers.filter(p=>R.ageDays(p.published)>=0&&R.ageDays(p.published)<=30).length;
  $('#total-count').textContent=papers.length; $('#count-all').textContent=papers.length;
  $('#fresh-count').textContent=fresh; $('#channel-count').textContent=String(R.getCategories(config).length).padStart(2,'0');
  $('#bookmarks-count').textContent=R.state().saved.length; $('#count-saved').textContent=R.state().saved.length;
  $('#count-noted').textContent=papers.filter(isNote).length;
 }
 function sideChannels(){
  $('#channels-nav').innerHTML=R.getCategories(config).map(c=>{
   const count=papers.filter(p=>R.categoriesFor(p,config).includes(c.id)).length;
   return `<button type="button" class="channel-link ${channel===c.id&&view==='all'?'selected':''}" data-channel="${e(c.id)}"><i class="channel-dot" style="background:${R.safeColor(c.color)}"></i><span>${e(c.label)}</span><span class="nav-count">${count}</span></button>`;
  }).join('');
  $$('.nav-link').forEach(b=>b.classList.toggle('active',b.dataset.view===view));
 }
 function tabs(){
  const buttons=[`<button class="filter-tab ${channel==='all'?'active':''}" data-filter="all">All Papers</button>`];
  R.getCategories(config).forEach(c=>buttons.push(`<button class="filter-tab ${channel===c.id?'active':''}" data-filter="${e(c.id)}">${e(c.label)}</button>`));
  $('#filter-tabs').innerHTML=buttons.join('');
 }
 function getFiltered(){
  const q=search.toLocaleLowerCase().trim();
  let filtered=papers.filter(p=>(channel==='all'||R.categoriesFor(p,config).includes(channel)) && (view==='all'||(view==='saved'?R.isSaved(p.id):isNote(p))) && (!q||[p.title,p.summary_ko,p.abstract,(p.tags||[]).join(' '),(p.authors||[]).join(' ')].join(' ').toLocaleLowerCase().includes(q)));
  filtered=[...filtered].sort((a,b)=>sort==='title'?a.title.localeCompare(b.title):sort==='featured'?(Number(b.featured)-Number(a.featured))||b.published.localeCompare(a.published):b.published.localeCompare(a.published));
  return filtered;
 }
 function decorate(p){const primary=category(p.primary_category);return `--paper-color:${R.safeColor(primary.color)}`;}
 function card(p){
  const title=e(p.title); const link=R.paperLink(p.id);
  const saved=R.isSaved(p.id);
  return `<article class="paper-card" style="${decorate(p)}">
     <div class="paper-card-top"><div class="card-cats">${chip(p.primary_category)}${isNew(p)?'<span class="new-badge">NEW</span>':p.featured?'<span class="editor-badge">✳ PICK</span>':''}${["2610.07922","2608.01397","2504.16054","2610.42021","2610.40026"].includes(p.id)?'<span class="visual-deep-badge">◈ 그림 해설</span>':''}</div><button type="button" class="bookmark-btn ${saved?'is-saved':''}" data-bookmark="${e(p.id)}" aria-label="${saved?'북마크 취소':'북마크 추가'}" title="북마크">${saved?'★':'☆'}</button></div>
     <a class="paper-card-link" href="${link}"><div class="card-art-pattern"><span>${e(p.primary_category.toUpperCase())}</span><b>↗</b></div><div class="paper-card-content"><div class="card-date">${e(R.showDate(p.published))} <i>·</i> ${Number(p.reading_minutes)||7} MIN READ</div><h3>${title}</h3><p>${e(p.summary_ko)}</p></div></a>
     <div class="paper-card-tags">${(p.tags||[]).slice(0,3).map(t=>`<span>#${e(t)}</span>`).join('')}</div>
     <div class="paper-card-bottom"><span>${e((p.authors||[]).slice(0,2).join(' · '))}</span><a href="${link}" title="논문 자세히 보기" aria-label="논문 자세히 보기">↗</a></div>
   </article>`;
 }
 function spotlightCard(p,idx){
  const desc=R.plain(p.summary_ko);
  return `<a class="spotlight-card sc-${idx}" href="${R.paperLink(p.id)}" style="${decorate(p)}"><div class="spotlight-top"><span>${idx===0?'01 / FEATURED ANALYSIS':'02 / RESEARCH HIGHLIGHT'}</span><span class="spotlight-arrow">↗</span></div><div class="spotlight-orbit" aria-hidden="true"><i></i><i></i><i></i></div><div class="spotlight-content">${chip(p.primary_category,'spotlight-chip')}<h3>${e(p.title)}</h3><p>${e(desc)}</p><div class="spotlight-meta">${e(R.showDate(p.published))} <span>·</span> Deep dive <span>→</span></div></div></a>`;
 }
 function spotlight(){
  const picks=[papers.find(p=>p.id==='2610.07922'),papers.find(p=>p.id==='2610.42021')].filter(Boolean);
  const options=picks.length===2?picks:papers.filter(p=>p.featured).sort((a,b)=>b.published.localeCompare(a.published)).slice(0,2);
  $('#spotlight-grid').innerHTML=options.map(spotlightCard).join('');
 }
 function render(){
  counters();sideChannels();tabs();
  const items=getFiltered(); $('#result-count').textContent=`${items.length} PAPERS FOUND`;
  $('#paper-grid').innerHTML=items.map(card).join('');
  $('#empty-results').classList.toggle('hidden',items.length!==0);
  if (view==='saved') $('.library-heading h2').innerHTML='Your bookmarks<span class="section-period">.</span>';
  else if (view==='noted') $('.library-heading h2').innerHTML='Your research notes<span class="section-period">.</span>';
  else $('.library-heading h2').innerHTML='Explore all papers<span class="section-period">.</span>';
 }
 function changeCategory(id){channel=id;view='all';render();$('#sidebar').classList.remove('mobile-open');document.getElementById('library-section').scrollIntoView({behavior:'smooth',block:'start'});}
 function openSettings(){renderCategoryEditor();$('#settings-modal').classList.remove('hidden');document.body.classList.add('modal-open');}
 function closeSettings(){$('#settings-modal').classList.add('hidden');document.body.classList.remove('modal-open');render();}
 function renderCategoryEditor(){
  const cats=R.getCategories(config);$('#category-edit-count').textContent=`${cats.length}개`;
  $('#category-editor').innerHTML=cats.map((c,i)=>`<div class="category-edit-row" data-edit-id="${e(c.id)}"><i style="background:${R.safeColor(c.color)}"></i><div class="category-edit-details"><strong>${e(c.label)}</strong><span>${e((c.keywords||[]).slice(0,5).join(', ')||'키워드 없음')}</span></div><div class="category-edit-actions"><button type="button" data-action="up" data-id="${e(c.id)}" title="위로" aria-label="위로" ${i===0?'disabled':''}>↑</button><button type="button" data-action="down" data-id="${e(c.id)}" title="아래로" aria-label="아래로" ${i===cats.length-1?'disabled':''}>↓</button><button type="button" data-action="edit" data-id="${e(c.id)}" title="수정" aria-label="수정">✎</button><button type="button" data-action="remove" data-id="${e(c.id)}" title="삭제" aria-label="삭제">×</button></div></div>`).join('');
 }
 function updateCategories(fn){const copy=R.getCategories(config).map(x=>({...x,keywords:[...(x.keywords||[])]}));fn(copy);R.mutate(s=>{s.categories=copy;});renderCategoryEditor();render();}
 function handleCategoryAction(ev){
  const btn=ev.target.closest('[data-action]');if(!btn)return;const {id,action}=btn.dataset;
  if(action==='up'||action==='down'){updateCategories(arr=>{const i=arr.findIndex(x=>x.id===id);const j=i+(action==='up'?-1:1);if(j>=0&&j<arr.length)[arr[i],arr[j]]=[arr[j],arr[i]];});}
  if(action==='remove'){
   if(R.getCategories(config).length<=1){R.toast('최소 하나의 분류는 유지해야 합니다.');return;}
   if(confirm('이 분류를 개인 보기에서 삭제할까요? (원본 논문은 보존됩니다)'))updateCategories(arr=>arr.splice(arr.findIndex(x=>x.id===id),1));
  }
  if(action==='edit'){
   const c=R.getCategories(config).find(x=>x.id===id);if(!c)return;
   const label=prompt('분류 표시 이름',c.label);if(label===null||!label.trim())return;
   const keywords=prompt('자동 매칭 키워드 (쉼표로 구분)',(c.keywords||[]).join(', '));if(keywords===null)return;
   updateCategories(arr=>{const x=arr.find(y=>y.id===id);x.label=label.trim().slice(0,44);x.keywords=keywords.split(',').map(y=>y.trim()).filter(Boolean).slice(0,30);});
  }
 }
 function addCategory(ev){ev.preventDefault();const label=$('#new-category-label').value.trim(), keywords=$('#new-category-keywords').value.split(',').map(s=>s.trim()).filter(Boolean);if(!label)return;
  let base=label.toLowerCase().normalize('NFKD').replace(/[^a-z0-9가-힣]+/g,'-').replace(/^-|-$/g,'').slice(0,34)||'custom';
  let id=base,num=2;while(R.getCategories(config).some(x=>x.id===id))id=`${base}-${num++}`;
  const colors=['#8d79b3','#658b9c','#ba8a45','#c56981','#72976c'];
  updateCategories(arr=>arr.push({id,label:label.slice(0,44),subtitle:'CUSTOM RESEARCH CHANNEL',description:'나의 맞춤 연구 분류',keywords,queries:[],color:colors[arr.length%colors.length]}));ev.target.reset();R.toast('새 연구 분류를 추가했습니다.');
 }
 function bindings(){
  $('#paper-search').addEventListener('input',ev=>{search=ev.target.value;render();});
  $('#sort-select').addEventListener('change',ev=>{sort=ev.target.value;render();});
  $('#filter-tabs').addEventListener('click',ev=>{const b=ev.target.closest('[data-filter]');if(b)changeCategory(b.dataset.filter);});
  $('#channels-nav').addEventListener('click',ev=>{const b=ev.target.closest('[data-channel]');if(b)changeCategory(b.dataset.channel);});
  $('#main-nav').addEventListener('click',ev=>{const b=ev.target.closest('[data-view]');if(!b)return;view=b.dataset.view;channel='all';render();$('#sidebar').classList.remove('mobile-open');$('#library-section').scrollIntoView({behavior:'smooth'});});
  $('#paper-grid').addEventListener('click',ev=>{const b=ev.target.closest('[data-bookmark]');if(!b)return;R.toggleSaved(b.dataset.bookmark);render();R.toast(R.isSaved(b.dataset.bookmark)?'북마크에 저장했습니다.':'북마크를 해제했습니다.');});
  $('#hero-browse').addEventListener('click',()=>$('#library-section').scrollIntoView({behavior:'smooth'}));
  $('#reset-filters').addEventListener('click',()=>{search='';channel='all';view='all';$('#paper-search').value='';render();});
  $('#settings-btn').addEventListener('click',openSettings);$('#customize-btn').addEventListener('click',openSettings);
  $('#close-settings').addEventListener('click',closeSettings);$('#done-settings').addEventListener('click',closeSettings);
  $('#settings-modal').addEventListener('mousedown',ev=>{if(ev.target.id==='settings-modal')closeSettings();});
  $('#category-editor').addEventListener('click',handleCategoryAction);$('#add-category-form').addEventListener('submit',addCategory);
  $('#reset-categories').addEventListener('click',()=>{if(confirm('개인 맞춤 분류를 기본값으로 되돌릴까요? 저장한 연구 노트는 유지됩니다.')){R.mutate(s=>{s.categories=null;});renderCategoryEditor();render();R.toast('기본 분류로 복원했습니다.');}});
  $('#export-data').addEventListener('click',()=>{R.exportData();R.toast('백업 파일을 저장했습니다.');});
  $('#import-data').addEventListener('change',async ev=>{const f=ev.target.files?.[0];if(!f)return;try{R.importData(JSON.parse(await f.text()));R.applyTheme();renderCategoryEditor();render();R.toast('연구 노트를 가져왔습니다.');}catch(err){R.toast(err.message);}ev.target.value='';});
  $('#theme-toggle').addEventListener('click',()=>R.toggleTheme());
  $('#menu-button').addEventListener('click',()=>$('#sidebar').classList.toggle('mobile-open'));
  document.addEventListener('keydown',ev=>{
   if(ev.key==='Escape'){if(!$('#settings-modal').classList.contains('hidden'))closeSettings();$('#sidebar').classList.remove('mobile-open');}
   if(ev.key==='/' && !['INPUT','TEXTAREA'].includes(document.activeElement?.tagName)){ev.preventDefault();$('#paper-search').focus();$('#library-section').scrollIntoView({behavior:'smooth'});}
  });
  document.addEventListener('radar:changed',()=>{counters();sideChannels();});
 }
 async function init(){
  try{const result=await R.load();data=result.data;config=result.config;papers=(data.papers||[]).slice();
   $('#today-date').innerHTML=`<span>LAST INDEXED</span><strong>${e(R.showDate((data.last_checked||'').slice(0,10)))}</strong>`;
   $('#sync-status').textContent=`Updated ${R.showDate((data.last_checked||'').slice(0,10))}`;
   const categoryFromLink=new URLSearchParams(window.location.search).get('category');
   if(categoryFromLink && R.getCategories(config).some(c=>c.id===categoryFromLink))channel=categoryFromLink;
   bindings();spotlight();render();
  }catch(err){$('#paper-grid').innerHTML=`<div class="error-loading"><h3>데이터를 불러오지 못했습니다.</h3><p>${e(err.message)} — 로컬에서 볼 때는 <code>python -m http.server</code>를 실행하세요.</p></div>`;}
 }
 init();
})();
