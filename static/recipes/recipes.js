/* PokéSurvival recipe browser.
   Loads recipes.json (built by scripts/build_survival_recipes.py), lists recipes by
   the in-game menu's categories, and draws the selected one on its station panel. */
(function () {
  'use strict';
  const app = document.querySelector('.rb-app');
  if (!app) return;
  const BASE = app.dataset.base;
  const $ = (sel, el = app) => el.querySelector(sel);
  const listEl = $('.rb-list'), tabsEl = $('.rb-tabs'), detailEl = $('.rb-detail'),
        detailInner = $('.rb-detail-inner'), searchEl = $('.rb-search'), statusEl = $('.rb-status');

  const EXTRA_GROUPS = ['Everyday crafting', 'Old-season conversions'];
  const UNLOCKS_TAB = 'How to unlock';

  let DATA, byId, byOutputName, usesOf, icons, gui, unlocks, sheet, activeCat = null, activeId = null;

  function unlockInfo(key) { return key ? (unlocks[key] || { label: 'Unlock required', how: 'How to earn this is not documented yet.' }) : null; }
  function unlockShort(key) {           // compact text for list cards: "Catch 25", "Defeat 100 wild"
    const u = unlockInfo(key); if (!u) return '';
    if (u.progress == null || !u.attribute) return u.label;
    return u.trait.replace(/ Pokémon$/, '').replace('Defeat wild', 'Defeat') .replace('Catch', 'Catch') + ' ' + u.progress + (u.attribute === 'defeat_wild' ? ' wild' : '');
  }

  fetch(BASE + 'recipes.json').then(r => r.json()).then(init).catch(err => {
    statusEl.textContent = 'Could not load the recipe list. ' + err;
  });

  function init(data) {
    DATA = data; icons = data.icons; gui = data.gui.slots; unlocks = data.unlocks || {}; sheet = data.sheet;
    app.style.setProperty('--rb-cols', sheet.cols); app.style.setProperty('--rb-rows', sheet.rows);
    app.style.setProperty('--rb-icons', `url('${BASE}icons.png')`); app.style.setProperty('--rb-gui', `url('${BASE}gui.png')`);
    DATA.guiRects = data.gui.rects;
    byId = new Map(data.recipes.map(r => [r.id, r]));
    byOutputName = new Map();
    usesOf = new Map();
    for (const r of data.recipes) {
      const k = r.output.name;
      if (!byOutputName.has(k)) byOutputName.set(k, []);
      byOutputName.get(k).push(r);
      for (const s of slotsOf(r)) for (const a of s.accepts) {
        if (!usesOf.has(a)) usesOf.set(a, new Set());
        usesOf.get(a).add(r.id);
      }
    }
    // categories: game menu order, then the two extra groups
    const cats = data.menu.map(c => ({ name: c.name, description: c.description, icon: c.icon, color: c.color,
      subs: c.subcategories.map(s => ({ name: s.name, ids: s.recipe_ids, nocraft: s.listed_without_recipe })) }));
    for (const g of EXTRA_GROUPS) {
      const ids = data.recipes.filter(r => r.category === g).map(r => r.id);
      if (ids.length) cats.push({ name: g, description: g === 'Everyday crafting' ? 'Vanilla conveniences the server adds.' : 'Turn leftovers from a previous season into their current equivalent.', icon: null, subs: [{ name: null, ids, nocraft: [] }] });
    }
    cats.push({ name: UNLOCKS_TAB, description: null, icon: null, subs: [], unlocksView: true });
    DATA.cats = cats;
    renderTabs();
    searchEl.addEventListener('input', () => { activeCat = null; renderTabs(); renderList(); });
    $('.rb-close').addEventListener('click', closeDetail);
    window.addEventListener('hashchange', openFromHash);
    app.classList.add('is-ready');
    fitPanelScale(); window.addEventListener('resize', fitPanelScale);
    activeCat = cats[0].name;
    renderTabs(); renderList();
    openFromHash();
  }

  // ---------- helpers ----------
  function slotsOf(r) {
    const out = [];
    for (const k of ['ingredient', 'bottle', 'template', 'base', 'addition', 'input']) if (r[k]) out.push(r[k]);
    if (r.inputs) for (const s of r.inputs) if (s) out.push(s);
    if (r.grid) for (const row of r.grid) for (const s of row) if (s) out.push(s);
    return out;
  }
  function iconFor(id) { return id && icons[id] ? icons[id] : null; }          // [col, row] in the sheet
  function iconForSlot(slot) {
    for (const a of slot.accepts) { const u = iconFor(a); if (u) return u; }
    return null;
  }
  // An icon from the sprite sheet. `cell` is [col,row]; null draws the generic "?" tile.
  function ic(cell, cls = '', alt = '') {
    const c = cell || icons.any;
    return `<span class="rb-ic ${cls}" style="--ix:${c[0]};--iy:${c[1]}" role="img" aria-label="${esc(alt)}"></span>`;
  }
  function recipeFor(slot) {  // a recipe that produces this ingredient, for cross-linking
    for (const a of slot.accepts) for (const r of DATA.recipes) if (r.output.id === a) return r;
    const hit = byOutputName.get(slot.name); return hit ? hit[0] : null;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c])); }
  function matches(r, q) {
    if (!q) return true;
    const hay = [r.output.name, r.title || '', ...slotsOf(r).map(s => s.name)].join(' ').toLowerCase();
    return q.split(/\s+/).every(t => hay.includes(t));
  }

  // ---------- tabs + list ----------
  function renderTabs() {
    const q = searchEl.value.trim().toLowerCase();
    tabsEl.innerHTML = '';
    for (const c of DATA.cats) {
      const n = c.subs.reduce((a, s) => a + s.ids.filter(id => matches(byId.get(id), q)).length, 0);
      if (q && !n && !c.unlocksView) continue;
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'rb-tab' + (c.name === activeCat ? ' is-active' : '');
      const ic0 = iconFor(c.icon);
      b.innerHTML = (ic0 ? ic(ic0, 'rb-ic-tab') : (c.unlocksView ? '🔒 ' : '')) + esc(c.name) + (q && !c.unlocksView ? ` <small>(${n})</small>` : '');
      b.addEventListener('click', () => { activeCat = c.name; renderTabs(); renderList(); });
      tabsEl.appendChild(b);
    }
  }

  function renderList() {
    const q = searchEl.value.trim().toLowerCase();
    listEl.innerHTML = '';
    const cats = q && !activeCat ? DATA.cats : DATA.cats.filter(c => c.name === activeCat);
    let shown = 0;
    if (cats.length === 1 && cats[0].unlocksView) { renderUnlocks(); return; }
    for (const c of cats) {
      if (!q && c.description) { const p = document.createElement('p'); p.className = 'rb-cat-desc'; p.textContent = c.description; listEl.appendChild(p); }
      for (const s of c.subs) {
        const seen = new Set(); const items = [];
        for (const id of s.ids) {
          const r = byId.get(id); if (!r || !matches(r, q)) continue;
          const key = r.output.name;            // one card per output; variants live in the detail panel
          if (seen.has(key)) continue; seen.add(key); items.push(r);
        }
        if (!items.length && !(s.nocraft.length && !q)) continue;
        const h = document.createElement('h3'); h.textContent = (q && cats.length > 1 ? c.name + ' · ' : '') + (s.name || c.name); listEl.appendChild(h);
        const grid = document.createElement('div'); grid.className = 'rb-grid';
        for (const r of items) {
          const n = byOutputName.get(r.output.name).length;
          const b = document.createElement('button'); b.type = 'button';
          b.className = 'rb-item' + (r.unlock ? ' is-locked' : '') + (r.id === activeId ? ' is-active' : '');
          b.dataset.id = r.id;
          const sub = r.unlock ? unlockShort(r.unlock) : (n > 1 ? `${n} recipes` : '');
          b.innerHTML = `${ic(iconFor(r.output.id), 'rb-ic-card')}<span>${esc(r.title || r.output.name)}${sub ? `<small>${esc(sub)}</small>` : ''}</span>`;
          b.addEventListener('click', () => { location.hash = r.id; });
          grid.appendChild(b); shown++;
        }
        if (!q) for (const name of s.nocraft) {
          const d = document.createElement('div'); d.className = 'rb-item is-nocraft'; d.title = 'Shown in the game menu but has no recipe';
          d.innerHTML = `<span>${esc(name)}<small>not craftable</small></span>`; grid.appendChild(d);
        }
        listEl.appendChild(grid);
      }
    }
    if (!shown) { const p = document.createElement('p'); p.className = 'rb-empty'; p.textContent = 'No recipes match.'; listEl.appendChild(p); }
  }

  // ---------- detail ----------
  function openFromHash() {
    const id = decodeURIComponent(location.hash.slice(1));
    if (id === 'unlocks') { activeCat = UNLOCKS_TAB; renderTabs(); renderList(); return; }
    if (id && byId.has(id)) showRecipe(byId.get(id));
  }
  function closeDetail() { detailEl.hidden = true; activeId = null; history.replaceState(null, '', location.pathname); renderList(); }

  function showRecipe(r) {
    activeId = r.id;
    if (!searchEl.value.trim()) { activeCat = r.category; renderTabs(); }
    const variants = byOutputName.get(r.output.name) || [r];
    const vi = variants.indexOf(r);
    const out = r.output;
    let html = `<div class="rb-result">${ic(iconFor(out.id), 'rb-ic-result')}
      <div><h2>${esc(r.title || out.name)}${out.count > 1 ? ` <span class="rb-count">×${out.count}</span>` : ''}</h2>
      <small>${esc(stationLabel(r.station))}${r.station === 'crafting_table' ? (r.shaped ? ' · shaped' : ' · shapeless, any arrangement') : ''}</small></div></div>`;
    const badges = [];
    if (r.unlock) {
      const u = unlockInfo(r.unlock);
      const tip = u.how ? u.how : (u.progress != null ? `Trait: ${u.trait}. Reach ${u.progress} to unlock — track it with /traits.` : 'How to earn this is not documented yet.');
      badges.push(`<span class="rb-badge lock" title="${esc(tip)}">🔒 ${esc(u.label)}</span>`);
    }
    if (r.rule) badges.push('<span class="rb-badge">Pattern — stands for a family of recipes</span>');
    if (badges.length) html += `<div class="rb-badges">${badges.join('')}</div>`;
    if (variants.length > 1) html += `<div class="rb-variants">${variants.map((v, i) => `<button type="button" class="rb-variant${i === vi ? ' is-active' : ''}" data-id="${esc(v.id)}">${esc(variantLabel(v, i))}</button>`).join('')}</div>`;
    html += `<div class="rb-panel-wrap">${panelHtml(r)}</div>`;
    html += ingredientsHtml(r);
    if (r.note) html += `<p class="rb-note">${esc(r.note)}</p>`;
    const uses = out.id && usesOf.get(out.id);
    if (uses && uses.size) {
      const seen = new Set();
      const links = [...uses].map(id => byId.get(id)).filter(u => u && !seen.has(u.output.name) && seen.add(u.output.name)).map(u => `<a href="#${esc(u.id)}">${esc(u.title || u.output.name)}</a>`);
      html += `<p class="rb-uses">Used in: ${links.join(', ')}</p>`;
    }
    detailInner.innerHTML = html;
    detailEl.hidden = false;
    detailInner.querySelectorAll('.rb-variant').forEach(b => b.addEventListener('click', () => { location.hash = b.dataset.id; }));
    bindTooltips();
    renderList();
    const card = listEl.querySelector(`.rb-item[data-id="${CSS.escape(r.id)}"]`);
    if (card && window.innerWidth > 860) card.scrollIntoView({ block: 'nearest' });
  }

  function stationLabel(s) {
    return { crafting_table: 'Crafting Table', brewing_stand: 'Brewing Stand', smithing_table: 'Smithing Table', furnace: 'Furnace', smoker: 'Smoker' }[s] || s;
  }
  function variantLabel(v, i) {
    // name the variant by its distinguishing ingredient; if two variants share it, add the station
    const s = v.ingredient || slotsOf(v)[0];
    const base = s ? s.name : `Recipe ${i + 1}`;
    const sibs = byOutputName.get(v.output.name) || [];
    const clash = sibs.some(o => o !== v && (o.ingredient || slotsOf(o)[0] || {}).name === base);
    return clash ? `${base} (${stationLabel(v.station)})` : base;
  }

  function slotHtml(slot, x, y, opts = {}) {
    const style = `style="--x:${x};--y:${y}"`;
    if (!slot) return '';
    const names = slot.name;
    const tip = esc(names) + (opts.tip ? '\n' + esc(opts.tip) : '');
    if (!slot.accepts || !slot.accepts.length) {
      return `<div class="rb-slot rb-any" ${style} data-tip="${tip}">?</div>`;
    }
    const cell = iconForSlot(slot);
    const link = recipeFor(slot);
    const qty = opts.count && opts.count > 1 ? `<span class="rb-qty">${opts.count}</span>` : '';
    const inner = `${ic(cell, 'rb-ic-slot', names)}${qty}`;
    const cls = 'rb-slot' + (opts.faded ? ' rb-faded' : '');
    return link && link.id !== activeId
      ? `<a class="${cls}" ${style} href="#${esc(link.id)}" data-tip="${tip}\n<small>Click for its recipe</small>">${inner}</a>`
      : `<div class="${cls}" ${style} data-tip="${tip}">${inner}</div>`;
  }

  // background-image/size/position for a rectangle of the packed GUI sheet, scaled by --s
  function guiStyle(name) {
    const [x, y, w, h] = DATA.guiRects[name];
    const sheetW = Math.max(...Object.values(DATA.guiRects).map(r => r[0] + r[2]));
    const sheetH = Math.max(...Object.values(DATA.guiRects).map(r => r[1] + r[3]));
    return `background-image:var(--rb-gui);background-repeat:no-repeat;background-size:calc(${sheetW}px*var(--s)) calc(${sheetH}px*var(--s));background-position:calc(${-x}px*var(--s)) calc(${-y}px*var(--s))`;
  }

  function panelHtml(r) {
    const st = r.station, g = gui[st];
    const R = DATA.guiRects;
    const bg = `style="${guiStyle(st)}"`;
    const sprite = (name, x, y) => { const [sx, sy, w, h] = R[name]; return `<span class="rb-sprite" style="${guiStyle(name)};left:calc(${x}px*var(--s));top:calc(${y}px*var(--s));width:calc(${w}px*var(--s));height:calc(${h}px*var(--s))"></span>`; };
    let s = '';
    const outSlot = r.output.id || r.rule ? { name: r.output.name + (r.output.count > 1 ? ` ×${r.output.count}` : ''), accepts: r.output.id ? [r.output.id] : [] } : null;
    if (st === 'crafting_table') {
      const cells = r.shaped ? r.grid.flat() : Array.from({ length: 9 }, (_, i) => r.inputs[i] || null);
      cells.forEach((c, i) => { s += slotHtml(c, g.grid[i][0], g.grid[i][1]); });
      s += slotHtml(outSlot, g.out[0], g.out[1], { count: r.output.count });
    } else if (st === 'brewing_stand') {
      s += slotHtml(r.ingredient, g.ingredient[0], g.ingredient[1]);
      for (const b of g.bottles) s += slotHtml(r.bottle, b[0], b[1], { tip: 'Each bottle becomes one ' + r.output.name });
      s += slotHtml({ name: 'Blaze Powder (fuel)', accepts: ['minecraft:BLAZE_POWDER'] }, g.fuel[0], g.fuel[1], { faded: true });
      s += sprite('brew_arrow', g.arrow[0], g.arrow[1]);
    } else if (st === 'smithing_table') {
      s += slotHtml(r.template, g.template[0], g.template[1]);
      s += slotHtml(r.base, g.base[0], g.base[1]);
      s += slotHtml(r.addition, g.addition[0], g.addition[1]);
      s += slotHtml(outSlot, g.out[0], g.out[1], { count: r.output.count });
    } else { // furnace / smoker
      s += slotHtml(r.input, g.in[0], g.in[1]);
      s += slotHtml({ name: 'Any fuel', accepts: ['minecraft:COAL'] }, g.fuel[0], g.fuel[1], { faded: true });
      s += slotHtml(outSlot, g.out[0], g.out[1], { count: r.output.count });
      s += sprite('furnace_flame', g.flame[0], g.flame[1]);
      s += sprite('furnace_arrow', g.arrow[0], g.arrow[1]);
    }
    return `<div class="rb-panel" ${bg} role="img" aria-label="${esc(stationLabel(st))} layout">${s}</div>`;
  }

  function ingredientsHtml(r) {
    const counts = new Map();
    for (const s of slotsOf(r)) {
      const k = s.name; const e = counts.get(k) || { n: 0, slot: s }; e.n++; counts.set(k, e);
    }
    if (r.station === 'brewing_stand') { const b = counts.get(r.bottle.name); if (b) b.n = 3; }
    const rows = [...counts.entries()].map(([name, e]) => {
      const cell = iconForSlot(e.slot); const link = recipeFor(e.slot);
      const label = link && link.id !== r.id ? `<a href="#${esc(link.id)}">${esc(name)}</a>` : esc(name);
      return `<li><span class="rb-n">${e.n}×</span>${ic(cell, 'rb-ic-row')}<span>${label}</span></li>`;
    });
    return `<ul class="rb-ingredients">${rows.join('')}</ul>`;
  }

  // ---------- unlocks view ----------
  function renderUnlocks() {
    const intro = document.createElement('p'); intro.className = 'rb-cat-desc';
    intro.textContent = 'Locked recipes open as your traits grow. Traits count things you do in the world — catches, wild battles won — and each threshold hands you a set of recipes. Check your progress in game with /traits. One recipe is tied to the gym gauntlet instead.';
    listEl.appendChild(intro);
    // group recipe unlock keys by trait, in threshold order
    const byTrait = new Map();
    for (const [key, u] of Object.entries(unlocks)) {
      if (u.progress == null) continue;
      if (!byTrait.has(u.trait)) byTrait.set(u.trait, []);
      byTrait.get(u.trait).push([key, u]);
    }
    for (const [trait, tiers] of byTrait) {
      tiers.sort((a, b) => a[1].progress - b[1].progress);
      const h = document.createElement('h3'); h.textContent = trait; listEl.appendChild(h);
      for (const [key, u] of tiers) {
        const recs = DATA.recipes.filter(r => r.unlock === key);
        const seen = new Set(); const items = recs.filter(r => !seen.has(r.output.name) && seen.add(r.output.name));
        const row = document.createElement('div'); row.className = 'rb-unlock-tier';
        row.innerHTML = `<div class="rb-unlock-head"><strong>${esc(u.label)}</strong><small>${esc(items.length ? (u.how || '') : (u.reward || ''))}</small></div>`;
        const grid = document.createElement('div'); grid.className = 'rb-grid';
        for (const r of items) {
          const b = document.createElement('button'); b.type = 'button'; b.className = 'rb-item'; b.dataset.id = r.id;
          b.innerHTML = `${ic(iconFor(r.output.id), 'rb-ic-card')}<span>${esc(r.output.name)}</span>`;
          b.addEventListener('click', () => { location.hash = r.id; });
          grid.appendChild(b);
        }
        row.appendChild(grid); listEl.appendChild(row);
      }
    }
    // keys with no trait source
    const other = Object.entries(unlocks).filter(([, u]) => u.progress == null);
    const usedOther = [...new Set(DATA.recipes.map(r => r.unlock).filter(k => k && !(unlocks[k] && unlocks[k].progress != null)))];
    if (usedOther.length) {
      const h = document.createElement('h3'); h.textContent = 'Other unlocks'; listEl.appendChild(h);
      for (const key of usedOther) {
        const u = unlockInfo(key);
        const recs = DATA.recipes.filter(r => r.unlock === key);
        const row = document.createElement('div'); row.className = 'rb-unlock-tier';
        row.innerHTML = `<div class="rb-unlock-head"><strong>${esc(u.label)}</strong><small>${esc(u.how || '')}</small></div>`;
        const grid = document.createElement('div'); grid.className = 'rb-grid';
        const seen = new Set();
        for (const r of recs) {
          if (seen.has(r.output.name)) continue; seen.add(r.output.name);
          const b = document.createElement('button'); b.type = 'button'; b.className = 'rb-item'; b.dataset.id = r.id;
          b.innerHTML = `${ic(iconFor(r.output.id), 'rb-ic-card')}<span>${esc(r.output.name)}</span>`;
          b.addEventListener('click', () => { location.hash = r.id; });
          grid.appendChild(b);
        }
        row.appendChild(grid); listEl.appendChild(row);
      }
    }
  }

  // ---------- tooltips ----------
  let tipEl = null;
  function bindTooltips() {
    detailInner.querySelectorAll('[data-tip]').forEach(el => {
      el.addEventListener('mouseenter', e => showTip(el, e));
      el.addEventListener('mousemove', e => moveTip(e));
      el.addEventListener('mouseleave', hideTip);
      el.addEventListener('touchstart', e => { showTip(el, e.touches[0]); setTimeout(hideTip, 1800); }, { passive: true });
    });
  }
  function showTip(el, e) {
    if (!tipEl) { tipEl = document.createElement('div'); tipEl.className = 'rb-tip'; document.body.appendChild(tipEl); }
    tipEl.innerHTML = el.dataset.tip; tipEl.style.display = 'block'; moveTip(e);
  }
  function moveTip(e) {
    if (!tipEl) return;
    const x = Math.min(e.clientX + 14, window.innerWidth - tipEl.offsetWidth - 8);
    const y = Math.min(e.clientY + 14, window.innerHeight - tipEl.offsetHeight - 8);
    tipEl.style.left = x + 'px'; tipEl.style.top = y + 'px';
  }
  function hideTip() { if (tipEl) tipEl.style.display = 'none'; }

  // ---------- panel scale ----------
  function fitPanelScale() {
    const avail = Math.min(window.innerWidth - 48, 440 - 34);
    const s = Math.max(1, Math.min(2, Math.floor((avail / 176) * 4) / 4));
    app.style.setProperty('--s', s);
  }
})();
