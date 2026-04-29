// Interactive type chart — three modes (single matchup, defense profile,
// full grid). All effectiveness math uses the Gen 6+ chart, mirroring the
// CHART table in damage-calc.js. The Pokémon picker pulls /calcdata.json
// (already built by Hugo for the damage calc + team builder).

(function () {
  'use strict';

  const TYPES = [
    'Normal', 'Fire', 'Water', 'Electric', 'Grass', 'Ice',
    'Fighting', 'Poison', 'Ground', 'Flying', 'Psychic', 'Bug',
    'Rock', 'Ghost', 'Dragon', 'Dark', 'Steel', 'Fairy', 'Shadow'
  ];

  // Sparse offensive chart: only non-1× cells are listed. Anything missing
  // returns 1 (neutral). Mirrors Type.java in PokemonWorld-master, including
  // Shadow's row (×2 vs every non-Shadow type, ×0.5 vs Shadow itself).
  const CHART = {
    Normal:   { Rock: 0.5, Ghost: 0,   Steel: 0.5 },
    Fire:     { Fire: 0.5, Water: 0.5, Grass: 2,   Ice: 2,   Bug: 2,   Rock: 0.5, Dragon: 0.5, Steel: 2 },
    Water:    { Fire: 2,   Water: 0.5, Grass: 0.5, Ground: 2, Rock: 2,  Dragon: 0.5 },
    Electric: { Water: 2,  Electric: 0.5, Grass: 0.5, Ground: 0, Flying: 2, Dragon: 0.5 },
    Grass:    { Fire: 0.5, Water: 2,   Grass: 0.5, Poison: 0.5, Ground: 2, Flying: 0.5, Bug: 0.5, Rock: 2, Dragon: 0.5, Steel: 0.5 },
    Ice:      { Fire: 0.5, Water: 0.5, Grass: 2,   Ice: 0.5,  Ground: 2, Flying: 2, Dragon: 2, Steel: 0.5 },
    Fighting: { Normal: 2, Ice: 2, Poison: 0.5, Flying: 0.5, Psychic: 0.5, Bug: 0.5, Rock: 2, Ghost: 0, Dark: 2, Steel: 2, Fairy: 0.5 },
    Poison:   { Grass: 2, Poison: 0.5, Ground: 0.5, Rock: 0.5, Ghost: 0.5, Steel: 0, Fairy: 2 },
    Ground:   { Fire: 2, Electric: 2, Grass: 0.5, Poison: 2, Flying: 0, Bug: 0.5, Rock: 2, Steel: 2 },
    Flying:   { Electric: 0.5, Grass: 2, Fighting: 2, Bug: 2, Rock: 0.5, Steel: 0.5 },
    Psychic:  { Fighting: 2, Poison: 2, Psychic: 0.5, Dark: 0, Steel: 0.5 },
    Bug:      { Fire: 0.5, Grass: 2, Fighting: 0.5, Poison: 0.5, Flying: 0.5, Psychic: 2, Ghost: 0.5, Dark: 2, Steel: 0.5, Fairy: 0.5 },
    Rock:     { Fire: 2, Ice: 2, Fighting: 0.5, Ground: 0.5, Flying: 2, Bug: 2, Steel: 0.5 },
    Ghost:    { Normal: 0, Psychic: 2, Ghost: 2, Dark: 0.5 },
    Dragon:   { Dragon: 2, Steel: 0.5, Fairy: 0 },
    Dark:     { Fighting: 0.5, Psychic: 2, Ghost: 2, Dark: 0.5, Fairy: 0.5 },
    Steel:    { Fire: 0.5, Water: 0.5, Electric: 0.5, Ice: 2, Rock: 2, Steel: 0.5, Fairy: 2 },
    Fairy:    { Fire: 0.5, Fighting: 2, Poison: 0.5, Dragon: 2, Dark: 2, Steel: 0.5 },
    Shadow:   {
      Normal: 2, Fire: 2, Water: 2, Electric: 2, Grass: 2, Ice: 2,
      Fighting: 2, Poison: 2, Ground: 2, Flying: 2, Psychic: 2, Bug: 2,
      Rock: 2, Ghost: 2, Dragon: 2, Dark: 2, Steel: 2, Fairy: 2,
      Shadow: 0.5
    }
  };

  // Multiplier cap: Shadow's offensive math is capped at ×2 even against
  // dual-type defenders that would otherwise multiply to ×4. Mirrors the
  // `Math.min(2, multiplier)` clamp in Type.java#getMultiplier.
  function effectiveness(att, defenderTypes) {
    let m = 1;
    for (const t of defenderTypes) {
      if (!t) continue;
      const v = (CHART[att] || {})[t];
      m *= (v === undefined ? 1 : v);
    }
    if (att === 'Shadow') m = Math.min(2, m);
    return m;
  }

  function effClass(m) {
    // Map raw multiplier to a CSS class. The class names group ×4/×2 as
    // "advantage" and ×½/×¼ as "disadvantage" so the same colour palette
    // covers both single-type and multiplied dual-type results.
    if (m === 0) return 'x0';
    if (m === 0.25) return 'x025';
    if (m === 0.5) return 'x05';
    if (m === 1) return 'x1';
    if (m === 2) return 'x2';
    if (m === 4) return 'x4';
    return 'x1';
  }

  function effLabel(m) {
    if (m === 0) return 'No effect (×0)';
    if (m < 1) return 'Not very effective (×' + m + ')';
    if (m > 1) return 'Super effective (×' + m + ')';
    return 'Neutral (×1)';
  }

  // ---- Mode tabs ---------------------------------------------------------
  function initTabs() {
    const tabs = document.querySelectorAll('.tc-tab');
    const panels = document.querySelectorAll('.tc-panel');
    tabs.forEach(tab => {
      tab.addEventListener('click', () => {
        const mode = tab.dataset.tcMode;
        tabs.forEach(t => {
          const active = t === tab;
          t.classList.toggle('active', active);
          t.setAttribute('aria-selected', active ? 'true' : 'false');
        });
        panels.forEach(p => {
          const active = p.dataset.tcMode === mode;
          p.classList.toggle('active', active);
          if (active) p.removeAttribute('hidden'); else p.setAttribute('hidden', '');
        });
      });
    });
  }

  // ---- Type-button row helper -------------------------------------------
  function appendTypeButtons(container) {
    TYPES.forEach(t => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'tc-type-btn type-' + t.toLowerCase();
      b.dataset.type = t;
      b.textContent = t;
      container.appendChild(b);
    });
  }

  function setActiveType(container, type) {
    container.querySelectorAll('.tc-type-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.type === type);
    });
  }

  // ---- Mode 1: type vs type(s) ------------------------------------------
  function initCalcMode() {
    const att = document.getElementById('tc-att');
    const def1 = document.getElementById('tc-def1');
    const def2 = document.getElementById('tc-def2');
    const result = document.getElementById('tc-calc-result');
    if (!att || !def1 || !def2 || !result) return;

    appendTypeButtons(att);
    appendTypeButtons(def1);
    appendTypeButtons(def2);   // None button is already in HTML

    const state = { att: 'Fire', d1: 'Grass', d2: '' };

    function recompute() {
      const m = effectiveness(state.att, [state.d1, state.d2]);
      result.className = 'tc-result tc-eff ' + effClass(m);
      result.textContent = effLabel(m);
    }

    setActiveType(att, state.att);
    setActiveType(def1, state.d1);
    setActiveType(def2, state.d2);
    recompute();

    function onClick(container, target, key) {
      container.addEventListener('click', e => {
        const btn = e.target.closest('.tc-type-btn');
        if (!btn) return;
        state[key] = btn.dataset.type;
        setActiveType(container, btn.dataset.type);
        recompute();
      });
    }
    onClick(att, 'att', 'att');
    onClick(def1, 'def1', 'd1');
    onClick(def2, 'def2', 'd2');
  }

  // ---- Mode 2: defense profile by Pokémon -------------------------------
  function initDexMode() {
    const search = document.getElementById('tc-mon-search');
    const select = document.getElementById('tc-mon-select');
    const typesEl = document.getElementById('tc-mon-types');
    const gridEl = document.getElementById('tc-mon-grid');
    if (!select || !typesEl || !gridEl) return;

    let MONS = [];

    fetch(new URL('/calcdata.json', document.baseURI).href)
      .then(r => r.json())
      .then(data => {
        MONS = Object.entries(data.pokemon || {}).map(([slug, p]) => {
          const f0 = p.forms && p.forms[0];
          if (!f0) return null;
          return {
            slug,
            name: p.name || slug,
            types: f0.types || [],
            dex: parseInt(p.dex || '0', 10)
          };
        }).filter(m => m && m.types.length).sort((a, b) => a.dex - b.dex || a.name.localeCompare(b.name));

        MONS.forEach(m => {
          const o = document.createElement('option');
          o.value = m.slug;
          o.textContent = '#' + String(m.dex).padStart(3, '0') + ' ' + m.name;
          o.dataset.name = m.name.toLowerCase();
          select.appendChild(o);
        });

        select.addEventListener('change', () => render(select.value));
        if (search) {
          search.addEventListener('input', () => {
            const q = search.value.trim().toLowerCase();
            let firstMatch = null;
            for (const opt of select.options) {
              const matches = !q || (opt.dataset.name || '').indexOf(q) !== -1;
              opt.hidden = !matches;
              if (matches && !firstMatch) firstMatch = opt;
            }
            if (firstMatch && q) {
              select.value = firstMatch.value;
              render(firstMatch.value);
            }
          });
        }

        if (MONS.length) render(MONS[0].slug);
      })
      .catch(err => {
        typesEl.textContent = 'Failed to load Pokémon data: ' + (err && err.message || err);
      });

    function render(slug) {
      const m = MONS.find(x => x.slug === slug);
      if (!m) return;
      typesEl.innerHTML = '<strong>' + escapeHtml(m.name) + '</strong> · ' +
        m.types.map(t => `<span class="type-${t.toLowerCase()} type-pill-sm">${escapeHtml(t)}</span>`).join(' ');
      const cells = TYPES.map(att => {
        const factor = effectiveness(att, m.types);
        return `<div class="tc-mon-cell tc-eff ${effClass(factor)}">
          <span class="type-${att.toLowerCase()} type-pill-sm">${att}</span>
          <span class="tc-mon-factor">×${factor}</span>
        </div>`;
      });
      gridEl.innerHTML = cells.join('');
    }
  }

  // ---- Mode 3: full 18×18 chart -----------------------------------------
  function initGridMode() {
    const grid = document.getElementById('tc-grid');
    if (!grid) return;
    let head = '<thead><tr><th class="tc-grid-corner"></th>';
    for (const t of TYPES) {
      head += `<th class="tc-grid-head"><span class="type-${t.toLowerCase()} type-pill-sm">${t}</span></th>`;
    }
    head += '</tr></thead>';
    let body = '<tbody>';
    for (const att of TYPES) {
      body += `<tr><th class="tc-grid-row-head"><span class="type-${att.toLowerCase()} type-pill-sm">${att}</span></th>`;
      for (const def of TYPES) {
        const v = (CHART[att] || {})[def];
        const m = v === undefined ? 1 : v;
        const cls = effClass(m);
        const display = m === 1 ? '' : (m === 0 ? '0' : '×' + m);
        body += `<td class="tc-eff ${cls}" title="${att} → ${def}: ×${m}">${display}</td>`;
      }
      body += '</tr>';
    }
    body += '</tbody>';
    grid.innerHTML = head + body;
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, c =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]
    );
  }

  function init() {
    initTabs();
    initCalcMode();
    initDexMode();
    initGridMode();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
