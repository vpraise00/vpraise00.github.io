(function () {
  'use strict';
  const KEY = 'research-radar-v1';
  const defaults = { saved: [], notes: {}, highlights: {}, categories: null, manualCategories: {}, theme: 'light' };
  const parse = () => {
    try {
      const item = JSON.parse(localStorage.getItem(KEY) || '{}');
      if (item && typeof item === 'object' && !Array.isArray(item)) {
        return { ...defaults, ...item, saved: Array.isArray(item.saved) ? item.saved : [],
          notes: item.notes && typeof item.notes === 'object' ? item.notes : {},
          highlights: item.highlights && typeof item.highlights === 'object' ? item.highlights : {},
          manualCategories: item.manualCategories && typeof item.manualCategories === 'object' ? item.manualCategories : {} };
      }
    } catch (_) { /* invalid local storage */ }
    return { ...defaults };
  };
  let state = parse();
  function save() { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (_) { toast('저장 공간이 부족합니다. JSON으로 내보내세요.'); } document.dispatchEvent(new CustomEvent('radar:changed')); }
  function mutate(fn) { fn(state); save(); }
  function esc(v) { return String(v ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }
  function plain(v) { return String(v ?? '').replace(/\s+/g,' ').trim(); }
  function safeColor(c) { return /^#[0-9a-fA-F]{6}$/.test(c || '') ? c : '#7f9295'; }
  function getCategories(config) { return Array.isArray(state.categories) ? state.categories : config.categories; }
  function categoriesFor(p, config) {
    const categories = getCategories(config);
    const matched = new Set(Array.isArray(p.categories) ? p.categories : [p.primary_category]);
    const haystack = `${p.title || ''} ${p.abstract || ''} ${(p.tags || []).join(' ')}`.toLowerCase();
    for (const c of categories) {
      if (Array.isArray(c.keywords) && c.keywords.some(k => k && haystack.includes(String(k).toLowerCase()))) matched.add(c.id);
    }
    for (const c of state.manualCategories[p.id] || []) matched.add(c);
    return [...matched];
  }
  function isSaved(id) { return state.saved.includes(id); }
  function toggleSaved(id) { mutate(s => { s.saved = s.saved.includes(id) ? s.saved.filter(v=>v!==id) : [...s.saved, id]; }); return isSaved(id); }
  function note(id) { return state.notes[id] || ''; }
  function setNote(id, text) { mutate(s => { if (text.trim()) s.notes[id]=text.slice(0,30000); else delete s.notes[id]; }); }
  function getHighlights(id) { return Array.isArray(state.highlights[id]) ? state.highlights[id] : []; }
  function addHighlight(id, quote) {
    const clean = plain(quote).slice(0,1400); if (!clean) return;
    mutate(s => { const list = s.highlights[id] || []; if (!list.includes(clean)) s.highlights[id] = [...list, clean].slice(-70); });
  }
  function removeHighlight(id, quote) { mutate(s => { s.highlights[id] = getHighlights(id).filter(v => v !== quote); }); }
  function showDate(date) { try { return new Intl.DateTimeFormat('ko-KR', {year:'numeric',month:'short',day:'numeric'}).format(new Date(date)); } catch (_) { return date; } }
  function ageDays(date) { return Math.floor((new Date().getTime() - new Date(`${date}T00:00:00Z`).getTime()) / 86400000); }
  function gptQuestion(p, selected = '') {
    const quotation = selected ? `\n내가 선택한 부분: “${plain(selected).slice(0,2000)}”` : '';
    return `다음 로보틱스 연구 논문을 한국어로 설명해줘. 논문의 실제 내용과 추론을 구분하고, 수식·아키텍처·데이터·평가 프로토콜을 가능하면 구체적으로 설명해줘. 확실하지 않은 내용은 확인이 필요하다고 밝혀줘.\n논문: ${p.title}\n원문: ${p.source_url}${quotation}\n특히 이 부분이 왜 중요하고 기존 연구와 무엇이 다른지 알려줘.`;
  }
  function openGPT(p, selected='') {
    const prompt = gptQuestion(p, selected);
    const url = 'https://chatgpt.com/?q=' + encodeURIComponent(prompt);
    // Long URLs can exceed service limits; a copy fallback remains available.
    if (url.length > 7500) { copy(prompt); window.open('https://chatgpt.com/', '_blank', 'noopener,noreferrer'); toast('질문을 복사했습니다. ChatGPT에 붙여 넣으세요.'); }
    else window.open(url, '_blank', 'noopener,noreferrer');
  }
  async function copy(text) {
    try { await navigator.clipboard.writeText(text); } catch (_) {
      const ta = document.createElement('textarea'); ta.value=text; ta.style.position='fixed'; ta.style.opacity='0'; document.body.append(ta); ta.select(); document.execCommand('copy'); ta.remove();
    }
  }
  let toastTimer;
  function toast(msg) { const el = document.querySelector('#toast'); if (!el) return; el.textContent=msg; el.classList.remove('hidden'); clearTimeout(toastTimer); toastTimer=setTimeout(()=>el.classList.add('hidden'),2800); }
  async function load() {
    const [papersResponse, configResponse] = await Promise.all([fetch('data/papers.json'),fetch('config/topics.json')]);
    if (!papersResponse.ok || !configResponse.ok) throw new Error('연구 데이터 로드 실패');
    const [data, config] = await Promise.all([papersResponse.json(),configResponse.json()]);
    return { data, config };
  }
  function exportData() {
    const blob = new Blob([JSON.stringify({ version:1, exported_at: new Date().toISOString(), ...state }, null, 2)], {type:'application/json'});
    const url=URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download='research-radar-notes.json'; document.body.append(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function importData(obj) {
    if (!obj || typeof obj!=='object' || !Array.isArray(obj.saved)) throw new Error('백업 파일의 형식이 잘못되었습니다.');
    state = { ...defaults, saved: obj.saved.filter(x=>typeof x==='string'), notes: obj.notes || {}, highlights: obj.highlights || {},
      categories: Array.isArray(obj.categories) ? obj.categories : null, manualCategories: obj.manualCategories || {},
      theme: obj.theme === 'dark' ? 'dark' : 'light' };
    save();
  }
  function applyTheme() { document.documentElement.dataset.theme = state.theme === 'dark' ? 'dark' : 'light'; }
  function toggleTheme() { mutate(s => {s.theme=s.theme==='dark'?'light':'dark';}); applyTheme(); }
  function paperLink(id) { return 'papers/' + encodeURIComponent(id) + '.html'; }
  applyTheme();
  window.Radar = { state:()=>state, save, mutate, esc, plain, safeColor, getCategories, categoriesFor,
    isSaved, toggleSaved, note, setNote, getHighlights, addHighlight, removeHighlight,
    showDate, ageDays, gptQuestion, openGPT, copy, toast, load, exportData, importData,
    applyTheme, toggleTheme, paperLink };
})();
