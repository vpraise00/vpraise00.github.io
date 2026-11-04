(function () {
'use strict';
const R=window.Radar,$=s=>document.querySelector(s),paper=JSON.parse($('#paper-data').textContent);
let config={categories:[]},selectionText='',noteDebounce=0;
function highlightCount(){const list=R.getHighlights(paper.id);$('#highlight-count').textContent=list.length;
 $('#highlights-list').innerHTML=list.length?list.map((q,i)=>`<div class="highlight-row"><blockquote>${R.esc(q)}</blockquote><div class="highlight-actions"><button data-highlight-ask="${i}">GPT에 질문 ↗</button><button data-highlight-remove="${i}">삭제 ×</button></div></div>`).join(''):'선택해 저장한 문장이 이곳에 표시됩니다.';
 paintHighlights(list);
}
function paintHighlights(list){
 if (!('highlights' in CSS)||!('Highlight' in window))return;
 const all=new Highlight(),nodes=[];
 const walker=document.createTreeWalker($('#article-body'),NodeFilter.SHOW_TEXT,{acceptNode(node){return node.parentElement.closest('button,a,script')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT;}});
 while(walker.nextNode())nodes.push(walker.currentNode);
 for(const quote of list){
  const tokens=quote.split(/\s+/).filter(Boolean);const first=tokens.slice(0,6).join(' ');
  const needle=first||quote;
  for(const node of nodes){let pos=node.textContent.indexOf(needle);if(pos===-1)continue;
    const length=(node.textContent.indexOf(quote,pos)===pos?quote:needle).length;
    const range=document.createRange();range.setStart(node,pos);range.setEnd(node,pos+length);all.add(range);break;
  }
 }
 CSS.highlights.set('radar-saved',all);
}
function updateSave(){const is=R.isSaved(paper.id);$('#save-paper').classList.toggle('is-saved',is);$('#save-paper').textContent=is?'★ 저장됨':'☆ 저장';}
function textSelected(){const sel=window.getSelection();const value=R.plain(sel?sel.toString():'');const ancestor=sel?.anchorNode;
 if(!value||value.length<4||!ancestor||!$('#article-body').contains(ancestor)){hideToolbar();return;}
 selectionText=value.slice(0,1400);const rect=sel.getRangeAt(0).getBoundingClientRect();const el=$('#selection-toolbar');
 el.classList.remove('hidden');el.style.top=Math.max(10,Math.min(window.innerHeight-60,rect.top-52))+'px';el.style.left=Math.max(10,Math.min(window.innerWidth-330,rect.left))+'px';
}
function hideToolbar(){$('#selection-toolbar').classList.add('hidden');}
function noteSaved(){R.setNote(paper.id,$('#paper-note').value);$('#note-status').textContent='✓ 브라우저에 자동 저장됨';}
function categoryOptions(){const select=$('#custom-paper-category');select.innerHTML='<option value="">+ 내 분류에 추가</option>'+R.getCategories(config).map(c=>`<option value="${R.esc(c.id)}">${R.esc(c.label)}</option>`).join('');}
function init(){
 try{const r=JSON.parse(localStorage.getItem('research-radar-v1')||'{}');if(r.theme==='dark')R.applyTheme();}catch(_){ }
 $('#save-paper').addEventListener('click',()=>{R.toggleSaved(paper.id);updateSave();R.toast(R.isSaved(paper.id)?'북마크에 저장했습니다.':'북마크를 해제했습니다.');});
 $('#share-paper').addEventListener('click',async()=>{await R.copy(location.href);R.toast('논문 링크를 복사했습니다.');});
 $('#article-theme').addEventListener('click',()=>R.toggleTheme());
 $('#ask-gpt').addEventListener('click',()=>R.openGPT(paper));
 $('#copy-gpt').addEventListener('click',async()=>{await R.copy(R.gptQuestion(paper));R.toast('GPT 질문을 복사했습니다.');});
 document.querySelectorAll('.ask-question').forEach(b=>b.addEventListener('click',()=>R.openGPT(paper,b.dataset.question)));
 $('#paper-note').value=R.note(paper.id);
 $('#paper-note').addEventListener('input',()=>{$('#note-status').textContent='저장 중...';clearTimeout(noteDebounce);noteDebounce=setTimeout(noteSaved,350);});
 $('#paper-note').addEventListener('blur',()=>{clearTimeout(noteDebounce);if($('#paper-note').value!==R.note(paper.id))noteSaved();});
 $('#highlights-list').addEventListener('click',ev=>{
  const ask=ev.target.closest('[data-highlight-ask]'),remove=ev.target.closest('[data-highlight-remove]');
  if(ask)R.openGPT(paper,R.getHighlights(paper.id)[Number(ask.dataset.highlightAsk)]);
  if(remove){const text=R.getHighlights(paper.id)[Number(remove.dataset.highlightRemove)];R.removeHighlight(paper.id,text);highlightCount();R.toast('하이라이트를 삭제했습니다.');}
 });
 $('#selection-save').addEventListener('click',()=>{R.addHighlight(paper.id,selectionText);highlightCount();hideToolbar();window.getSelection()?.removeAllRanges();R.toast('문장을 저장했습니다.');});
 $('#selection-ask').addEventListener('click',()=>{R.openGPT(paper,selectionText);hideToolbar();});
 document.addEventListener('mouseup',ev=>{if(ev.target instanceof Element && ev.target.closest('#selection-toolbar'))return;setTimeout(textSelected,30);});
 document.addEventListener('touchend',()=>setTimeout(textSelected,80),{passive:true});
 document.addEventListener('keyup',ev=>{if(ev.key==='Shift'||ev.key==='ArrowLeft'||ev.key==='ArrowRight')textSelected();});
 document.addEventListener('scroll',()=>{const root=document.documentElement;const max=root.scrollHeight-root.clientHeight;$('#reading-progress').style.width=(max>0?Math.min(100,100*root.scrollTop/max):0)+'%';hideToolbar();},{passive:true});
 $('#custom-paper-category').addEventListener('change',ev=>{const id=ev.target.value;if(!id)return;R.mutate(s=>{const list=s.manualCategories[paper.id]||[];if(!list.includes(id))s.manualCategories[paper.id]=[...list,id];});R.toast('논문을 내 분류에 추가했습니다.');ev.target.value='';});
 updateSave();highlightCount();
 fetch('../config/topics.json').then(r=>r.json()).then(v=>{config=v;categoryOptions();}).catch(()=>{});
}
init();
})();
