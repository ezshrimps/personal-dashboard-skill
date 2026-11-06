// Local stand-in for the claude.ai runtime: in-memory db with live snapshots, a rule-based "sample", no mcp.
// Only for previewing the template outside claude.ai (build.py --mock). Data lives in localStorage so reloads keep it.
(() => {
  const KEY = 'pd-mock-db';
  let store = {};
  try { store = JSON.parse(localStorage.getItem(KEY) || 'null') || {}; } catch { store = {}; }
  if (!Object.keys(store).length && window.__SEED__) store = structuredClone(window.__SEED__);
  const persist = () => { try { localStorage.setItem(KEY, JSON.stringify(store)); } catch {} };
  const listeners = new Set();
  const notify = () => { persist(); setTimeout(() => listeners.forEach(fn => fn()), 0); };
  const docSnap = path => ({ id: path.split('/').pop(), exists: path in store, data: () => structuredClone(store[path]) });
  const children = col => Object.keys(store).filter(p => p.startsWith(col + '/') && p.split('/').length === col.split('/').length + 1);
  const cmp = { '==': (a, b) => a === b, '!=': (a, b) => a !== b, '<': (a, b) => a < b, '<=': (a, b) => a <= b, '>': (a, b) => a > b, '>=': (a, b) => a >= b };
  function query(col, filters = [], order = null, lim = null) {
    const run = () => {
      let ps = children(col).filter(p => filters.every(([f, op, v]) => cmp[op] ? cmp[op]((store[p] || {})[f], v) : true));
      if (order) ps.sort((a, b) => { const x = store[a][order[0]], y = store[b][order[0]]; const r = x == null ? 1 : y == null ? -1 : x < y ? -1 : x > y ? 1 : 0; return order[1] === 'desc' ? -r : r; });
      if (lim) ps = ps.slice(0, lim);
      return { docs: ps.map(docSnap), size: ps.length, empty: !ps.length };
    };
    return {
      where: (f, op, v) => query(col, [...filters, [f, op, v]], order, lim), orderBy: (f, d) => query(col, filters, [f, d || 'asc'], lim), limit: n => query(col, filters, order, n),
      get: async () => run(),
      onSnapshot(fn) { const l = () => fn(run()); listeners.add(l); setTimeout(l, 0); return () => listeners.delete(l); },
      doc: id => doc(col + '/' + (id || Math.random().toString(36).slice(2))),
      add: async data => { const p = col + '/' + Math.random().toString(36).slice(2); store[p] = structuredClone(data); notify(); return doc(p); },
    };
  }
  function doc(path) {
    return {
      id: path.split('/').pop(), path,
      get: async () => docSnap(path),
      set: async data => { store[path] = structuredClone(data); notify(); },
      update: async data => { if (!(path in store)) throw Object.assign(new Error('not found'), { code: 'not_found' }); store[path] = { ...store[path], ...structuredClone(data) }; notify(); },
      delete: async () => { delete store[path]; notify(); },
      onSnapshot(fn) { const l = () => fn(docSnap(path)); listeners.add(l); setTimeout(l, 0); return () => listeners.delete(l); },
      collection: sub => query(path + '/' + sub),
    };
  }
  const db = { doc, collection: c => query(c) };

  // Rule-based stand-in for Claude: enough to exercise each record type.
  const today = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
  async function json(prompt) {
    await new Promise(r => setTimeout(r, 150));
    const said = (prompt.match(/«([\s\S]*)»/) || [])[1];
    if (said != null) {
      const n = +(said.match(/\d+(\.\d+)?/) || [0])[0], acts = [];
      const trk = (prompt.match(/trackers: (.*)/) || [])[1] || '';
      const trkHit = trk.split('; ').map(x => x.match(/^(\w+)=([^ (]+)/)).find(m => m && said.includes(m[2]));
      if (trkHit) acts.push({ type: 'track', tracker: trkHit[1], value: n || 1 });
      else if (/饭|lunch|coffee|咖啡|买|spent|\$/.test(said) && n) acts.push({ type: 'expense', amount: n, cat: 'c1', note: said.slice(0, 20) });
      else if (/考试|exam|deadline|截止/.test(said)) acts.push({ type: 'deadline', title: said.slice(0, 20), date: today().slice(0, 8) + '28' });
      else if (/开会|meeting/.test(said)) acts.push({ type: 'event', title: said.slice(0, 20), date: today(), start: '15:00' });
      else acts.push({ type: 'todo', text: said });
      return { actions: acts, reply: 'ok' };
    }
    if (/bank|statement|账单/i.test(prompt) && /transactions/.test(prompt)) return { transactions: [{ ref: 'mock1', date: today(), amount: 12.5, merchant: 'Mock Cafe', isSpend: true }, { ref: 'mock2', date: today(), amount: 300, merchant: 'Card payment', isSpend: false }] };
    if (/headline/.test(prompt)) return { headline: 'Mock analysis', points: ['point 1'], tips: ['tip 1'] };
    return {};
  }
  const sample = Object.assign(async p => ({ text: JSON.stringify(await json(p)), truncated: false }), { json, limits: async () => ({ images: null }) });
  const caps = { db, sample, mcp: null };
  window.claude = { use: async name => caps[name] ?? null };
  window.__mockReset = () => { try { localStorage.removeItem(KEY); } catch {} location.reload(); };
  window.__mockStore = () => store;
})();
