// Team Builder — six-slot Pokémon team editor with Showdown-format
// import/export. Reuses /calcdata.json for Pokémon and move data so the
// data is built once at site-build time rather than fetched separately.

(function () {
  'use strict';

  const STATS = ['hp', 'atk', 'def', 'spa', 'spd', 'spe'];
  const STAT_LABELS = ['HP', 'Atk', 'Def', 'SpA', 'SpD', 'Spe'];
  const NATURES = [
    'Hardy', 'Lonely', 'Brave', 'Adamant', 'Naughty',
    'Bold', 'Docile', 'Relaxed', 'Impish', 'Lax',
    'Timid', 'Hasty', 'Serious', 'Jolly', 'Naive',
    'Modest', 'Mild', 'Quiet', 'Bashful', 'Rash',
    'Calm', 'Gentle', 'Sassy', 'Careful', 'Quirky'
  ];
  const SLOT_COUNT = 6;

  let DATA = null;            // { pokemon: {...}, moves: {...} }
  let monIndex = [];          // [{slug,name,dex}] sorted by dex
  let moveIndex = [];         // [{slug,name}] sorted by name (incl. status)
  let monByName = {};         // lower(name) -> slug
  let moveByName = {};        // lower(name) -> slug
  let team = [];              // SLOT_COUNT entries (some empty)

  function $(id) { return document.getElementById(id); }
  function intVal(s, def) { const v = parseInt(s, 10); return isFinite(v) ? v : def; }

  function emptySlot() {
    return {
      species: '', nickname: '', item: '', ability: '',
      level: 100, nature: 'Hardy',
      shiny: false, gender: '', happiness: 255,
      evs: { hp: 0, atk: 0, def: 0, spa: 0, spd: 0, spe: 0 },
      ivs: { hp: 31, atk: 31, def: 31, spa: 31, spd: 31, spe: 31 },
      moves: ['', '', '', '']
    };
  }

  // ---- Searchable combobox (same idiom used on the damage calc) ----------
  function attachCombobox(selectEl) {
    const wrapper = document.createElement('div');
    wrapper.className = 'tb-combobox';
    selectEl.parentNode.insertBefore(wrapper, selectEl);
    wrapper.appendChild(selectEl);
    selectEl.classList.add('tb-hidden-select');

    const display = document.createElement('button');
    display.type = 'button';
    display.className = 'tb-combobox-display';

    const panel = document.createElement('div');
    panel.className = 'tb-combobox-panel';
    panel.hidden = true;

    const search = document.createElement('input');
    search.type = 'text';
    search.className = 'tb-combobox-search';
    search.placeholder = 'Type to filter…';
    search.autocomplete = 'off';

    const list = document.createElement('ul');
    list.className = 'tb-combobox-list';
    list.setAttribute('role', 'listbox');

    panel.appendChild(search);
    panel.appendChild(list);
    wrapper.appendChild(display);
    wrapper.appendChild(panel);

    let activeIdx = -1;
    let filtered = [];

    function refreshDisplay() {
      const opt = selectEl.options[selectEl.selectedIndex];
      display.textContent = opt && opt.value ? opt.textContent : (selectEl.dataset.placeholder || '— select —');
    }
    function rebuildList(query) {
      const q = (query || '').trim().toLowerCase();
      list.innerHTML = '';
      filtered = [];
      activeIdx = -1;
      Array.from(selectEl.options).forEach(opt => {
        const text = opt.textContent;
        if (q && text.toLowerCase().indexOf(q) === -1) return;
        const li = document.createElement('li');
        li.className = 'tb-combobox-item';
        if (opt.value === selectEl.value) {
          li.classList.add('selected');
          activeIdx = filtered.length;
        }
        li.textContent = text;
        li.addEventListener('mousedown', e => { e.preventDefault(); selectOption(opt.value); });
        list.appendChild(li);
        filtered.push({ li, value: opt.value });
      });
      if (activeIdx === -1 && filtered.length) activeIdx = 0;
      highlightActive();
    }
    function highlightActive() {
      filtered.forEach((f, i) => f.li.classList.toggle('active', i === activeIdx));
      if (activeIdx >= 0 && filtered[activeIdx]) filtered[activeIdx].li.scrollIntoView({ block: 'nearest' });
    }
    function selectOption(value) {
      selectEl.value = value;
      selectEl.dispatchEvent(new Event('change', { bubbles: true }));
      refreshDisplay();
      close();
      display.focus();
    }
    function open()  { panel.hidden = false; search.value = ''; rebuildList(''); setTimeout(() => search.focus(), 0); }
    function close() { panel.hidden = true; }

    display.addEventListener('click', () => panel.hidden ? open() : close());
    search.addEventListener('input', () => rebuildList(search.value));
    search.addEventListener('keydown', e => {
      if (e.key === 'ArrowDown') { e.preventDefault(); if (filtered.length) { activeIdx = (activeIdx + 1) % filtered.length; highlightActive(); } }
      else if (e.key === 'ArrowUp') { e.preventDefault(); if (filtered.length) { activeIdx = (activeIdx - 1 + filtered.length) % filtered.length; highlightActive(); } }
      else if (e.key === 'Enter') { e.preventDefault(); if (activeIdx >= 0 && filtered[activeIdx]) selectOption(filtered[activeIdx].value); }
      else if (e.key === 'Escape') { close(); display.focus(); }
    });
    document.addEventListener('mousedown', e => { if (!wrapper.contains(e.target)) close(); });
    selectEl.addEventListener('change', refreshDisplay);
    refreshDisplay();
    return refreshDisplay;
  }

  // ---- Data load ---------------------------------------------------------
  function load() {
    return fetch(new URL('/calcdata.json', document.baseURI).href)
      .then(r => r.json())
      .then(d => {
        DATA = d;
        monIndex = Object.entries(d.pokemon).map(([slug, p]) => ({
          slug, name: p.name, dex: parseInt(p.dex || '0', 10)
        })).sort((a, b) => a.dex - b.dex || a.name.localeCompare(b.name));
        monIndex.forEach(m => { monByName[m.name.toLowerCase()] = m.slug; });
        moveIndex = Object.entries(d.moves).map(([slug, m]) => ({
          slug, name: m.name
        })).sort((a, b) => a.name.localeCompare(b.name));
        moveIndex.forEach(m => { moveByName[m.name.toLowerCase()] = m.slug; });
      });
  }

  // ---- UI construction ---------------------------------------------------
  function buildUI() {
    const slotsEl = $('tb-slots');
    slotsEl.innerHTML = '';
    for (let i = 0; i < SLOT_COUNT; i++) slotsEl.appendChild(buildSlot(i));
    // Wire global buttons
    $('tb-import-btn').addEventListener('click', importFromText);
    $('tb-copy-btn').addEventListener('click', copyExport);
    $('tb-clear-btn').addEventListener('click', clearTeam);
    $('tb-fill-btn').addEventListener('click', fillDefaults);
    refreshExport();
  }

  function buildSlot(idx) {
    const card = document.createElement('article');
    card.className = 'tb-slot';
    card.dataset.slot = String(idx);

    // ---- Header row: Pokémon picker + level + remove ----
    const head = document.createElement('div');
    head.className = 'tb-slot-head';

    const monLabel = document.createElement('label');
    monLabel.className = 'tb-field tb-field-mon';
    monLabel.innerHTML = '<span>Pokémon</span>';
    const monSel = document.createElement('select');
    monSel.className = 'tb-mon-select';
    monSel.dataset.placeholder = '— pick a Pokémon —';
    monSel.appendChild(makeOption('', '— pick a Pokémon —'));
    monIndex.forEach(m => monSel.appendChild(makeOption(m.slug, '#' + String(m.dex).padStart(3, '0') + ' ' + m.name)));
    monSel.addEventListener('change', () => onMonChange(idx));
    monLabel.appendChild(monSel);
    head.appendChild(monLabel);

    const nickLabel = document.createElement('label');
    nickLabel.className = 'tb-field tb-field-nickname';
    nickLabel.innerHTML = '<span>Nickname</span><input type="text" class="tb-nickname" placeholder="(optional)" maxlength="12">';
    head.appendChild(nickLabel);

    const lvlLabel = document.createElement('label');
    lvlLabel.className = 'tb-field tb-field-level';
    lvlLabel.innerHTML = '<span>Level</span><input type="number" class="tb-level" min="1" max="100" value="100">';
    head.appendChild(lvlLabel);

    const removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.className = 'tb-slot-remove';
    removeBtn.title = 'Clear this slot';
    removeBtn.textContent = '✕';
    removeBtn.addEventListener('click', () => clearSlot(idx));
    head.appendChild(removeBtn);
    card.appendChild(head);

    // ---- Item / Ability / Nature row ----
    const ana = document.createElement('div');
    ana.className = 'tb-slot-row';

    const itemLabel = document.createElement('label');
    itemLabel.className = 'tb-field';
    itemLabel.innerHTML = '<span>Item</span>';
    const itemInput = document.createElement('input');
    itemInput.type = 'text';
    itemInput.className = 'tb-item';
    itemInput.placeholder = '(none)';
    itemInput.setAttribute('list', 'tb-items-list');
    itemLabel.appendChild(itemInput);
    ana.appendChild(itemLabel);

    const abilLabel = document.createElement('label');
    abilLabel.className = 'tb-field';
    abilLabel.innerHTML = '<span>Ability</span>';
    const abilSel = document.createElement('select');
    abilSel.className = 'tb-ability-select';
    abilSel.dataset.placeholder = '—';
    abilSel.appendChild(makeOption('', '—'));
    abilLabel.appendChild(abilSel);
    ana.appendChild(abilLabel);

    const natLabel = document.createElement('label');
    natLabel.className = 'tb-field';
    natLabel.innerHTML = '<span>Nature</span>';
    const natSel = document.createElement('select');
    natSel.className = 'tb-nature';
    NATURES.forEach(n => natSel.appendChild(makeOption(n, n + natureSuffix(n))));
    natSel.value = 'Hardy';
    natLabel.appendChild(natSel);
    ana.appendChild(natLabel);

    card.appendChild(ana);

    // ---- IV / EV grid ----
    const stats = document.createElement('div');
    stats.className = 'tb-stats';
    const head2 = document.createElement('div');
    head2.className = 'tb-stats-head';
    head2.innerHTML = '<span></span>' + STAT_LABELS.map(l => '<span>' + l + '</span>').join('');
    stats.appendChild(head2);

    function statRow(label, cls, defaultValue, max) {
      const row = document.createElement('div');
      row.className = 'tb-stats-row';
      row.innerHTML = '<span class="tb-stats-label">' + label + '</span>';
      STATS.forEach(s => {
        const cell = document.createElement('input');
        cell.type = 'text';
        cell.inputMode = 'numeric';
        cell.pattern = '\\d*';
        cell.maxLength = String(max).length;
        cell.className = cls;
        cell.dataset.stat = s;
        cell.value = String(defaultValue);
        row.appendChild(cell);
      });
      return row;
    }
    stats.appendChild(statRow('IVs', 'tb-iv', 31, 31));
    stats.appendChild(statRow('EVs', 'tb-ev',  0, 252));
    card.appendChild(stats);

    // ---- 4 Moves ----
    // Move dropdowns start with just "— select —". Their full option list
    // is populated per-Pokémon by `rebuildMoveSelects()` from the chosen
    // species's learnset (level-up + TMs + tutor + egg moves) in
    // calcdata.json. Pick a Pokémon first, then the move pickers fill in.
    const moves = document.createElement('div');
    moves.className = 'tb-moves';
    moves.innerHTML = '<div class="tb-moves-title">Moves <span class="tb-moves-hint">(filled from the chosen Pokémon\'s learnset)</span></div>';
    for (let m = 0; m < 4; m++) {
      const lbl = document.createElement('label');
      lbl.className = 'tb-field tb-field-move';
      lbl.innerHTML = '<span>' + (m + 1) + '</span>';
      const sel = document.createElement('select');
      sel.className = 'tb-move-select';
      sel.dataset.moveIdx = String(m);
      sel.dataset.placeholder = '— pick a Pokémon first —';
      sel.appendChild(makeOption('', '— pick a Pokémon first —'));
      lbl.appendChild(sel);
      moves.appendChild(lbl);
    }
    card.appendChild(moves);

    // ---- Wire change events for live export update ----
    card.querySelectorAll('input, select').forEach(el => {
      el.addEventListener('input', refreshExport);
      el.addEventListener('change', refreshExport);
    });

    // ---- Attach searchable combobox to Pokémon, Ability, and Move selects ----
    setTimeout(() => {
      attachCombobox(monSel);
      attachCombobox(abilSel);
      Array.from(card.querySelectorAll('.tb-move-select')).forEach(s => attachCombobox(s));
    }, 0);

    return card;
  }

  function makeOption(value, text) {
    const o = document.createElement('option');
    o.value = value;
    o.textContent = text;
    return o;
  }

  function natureSuffix(name) {
    const NATURE_EFFECT = {
      Lonely: ' (+Atk -Def)',  Brave:   ' (+Atk -Spe)',  Adamant: ' (+Atk -SpA)', Naughty: ' (+Atk -SpD)',
      Bold:   ' (+Def -Atk)',  Relaxed: ' (+Def -Spe)',  Impish:  ' (+Def -SpA)', Lax:     ' (+Def -SpD)',
      Timid:  ' (+Spe -Atk)',  Hasty:   ' (+Spe -Def)',  Jolly:   ' (+Spe -SpA)', Naive:   ' (+Spe -SpD)',
      Modest: ' (+SpA -Atk)',  Mild:    ' (+SpA -Def)',  Quiet:   ' (+SpA -Spe)', Rash:    ' (+SpA -SpD)',
      Calm:   ' (+SpD -Atk)',  Gentle:  ' (+SpD -Def)',  Sassy:   ' (+SpD -Spe)', Careful: ' (+SpD -SpA)'
    };
    return NATURE_EFFECT[name] || '';
  }

  // ---- Pokémon → ability + move list ------------------------------------
  function onMonChange(idx) {
    const card = slotCard(idx);
    const monSel = card.querySelector('.tb-mon-select');
    const abilSel = card.querySelector('.tb-ability-select');
    const slug = monSel.value;

    // Abilities: refill from the species's standard + hidden ability set.
    const previousAbil = abilSel.value;
    abilSel.innerHTML = '';
    abilSel.appendChild(makeOption('', '—'));
    if (slug && DATA.pokemon[slug]) {
      const form0 = DATA.pokemon[slug].forms[0] || {};
      const abilities = (form0.abilities || []).slice();
      if (form0.hidden) abilities.push(form0.hidden + ' (Hidden)');
      abilities.forEach(a => abilSel.appendChild(makeOption(a.replace(/ \(Hidden\)$/, ''), a)));
    }
    if (previousAbil && abilSel.querySelector('option[value="' + cssEscape(previousAbil) + '"]')) {
      abilSel.value = previousAbil;
    }
    abilSel.dispatchEvent(new Event('change'));

    // Moves: refill each of the four dropdowns from this species's learnset.
    rebuildMoveSelects(card, slug);
  }

  // Compute the list of move {slug,name} entries the given species can learn,
  // sourced from notable_moves + tms + tutor_moves + egg_moves baked into
  // calcdata.json — and recursively merged from every pre-evolution in the
  // species's evolution family. That's why Cloyster includes Shellder's
  // Icicle Spear, Charizard includes Charmander's Ember, and so on.
  // Returns sorted by display name.
  function getLearnsetForSlug(slug) {
    const visited = new Set();
    const lower = new Set();
    (function walk(s) {
      if (!s || visited.has(s)) return;
      visited.add(s);
      const mon = DATA.pokemon[s];
      if (!mon) return;
      const form0 = mon.forms[0] || {};
      (form0.learnset || []).forEach(n => lower.add(n.toLowerCase()));
      (mon.preEvos || []).forEach(walk);
    })(slug);
    const out = [];
    moveIndex.forEach(m => { if (lower.has(m.name.toLowerCase())) out.push(m); });
    return out.sort((a, b) => a.name.localeCompare(b.name));
  }

  // Replace each of the slot's four move-select option lists with the
  // chosen species's learnset. If a move was previously selected and is
  // no longer in the legal pool (e.g. after switching species, or after
  // importing a Showdown set with an out-of-learnset move), preserve it
  // as a synthetic option marked "(not in learnset)" so the value isn't
  // silently dropped.
  function rebuildMoveSelects(card, slug) {
    const learnset = getLearnsetForSlug(slug);
    const empty = slug ? '— select —' : '— pick a Pokémon first —';
    Array.from(card.querySelectorAll('.tb-move-select')).forEach(sel => {
      const previous = sel.value;
      const previousText = previous
        ? (Array.from(sel.options).find(o => o.value === previous) || {}).textContent
        : '';
      sel.innerHTML = '';
      sel.appendChild(makeOption('', empty));
      sel.dataset.placeholder = empty;
      learnset.forEach(m => sel.appendChild(makeOption(m.slug, m.name)));
      if (previous) {
        const stillLegal = learnset.find(m => m.slug === previous);
        if (!stillLegal) {
          // Out-of-learnset move from a previous selection or import — keep it.
          const m = DATA.moves[previous];
          const text = (m ? m.name : (previousText || previous)) + ' (not in learnset)';
          sel.appendChild(makeOption(previous, text));
        }
        sel.value = previous;
      }
      sel.dispatchEvent(new Event('change'));
    });
  }
  function cssEscape(s) { return (window.CSS && CSS.escape ? CSS.escape(s) : String(s).replace(/"/g, '\\"')); }
  function slotCard(idx) { return document.querySelector('.tb-slot[data-slot="' + idx + '"]'); }

  // ---- Sync UI ↔ team[] -------------------------------------------------
  function readSlotFromUI(idx) {
    const card = slotCard(idx);
    const slug = card.querySelector('.tb-mon-select').value;
    if (!slug) return null;
    const slot = emptySlot();
    slot.species = (DATA.pokemon[slug] || {}).name || slug;
    slot.nickname = card.querySelector('.tb-nickname').value.trim();
    slot.level = intVal(card.querySelector('.tb-level').value, 100);
    slot.item = card.querySelector('.tb-item').value.trim();
    slot.ability = card.querySelector('.tb-ability-select').value;
    slot.nature = card.querySelector('.tb-nature').value || 'Hardy';
    card.querySelectorAll('.tb-iv').forEach(inp => slot.ivs[inp.dataset.stat] = clamp(intVal(inp.value, 31), 0, 31));
    card.querySelectorAll('.tb-ev').forEach(inp => slot.evs[inp.dataset.stat] = clamp(intVal(inp.value, 0), 0, 252));
    Array.from(card.querySelectorAll('.tb-move-select')).forEach((sel, m) => {
      const v = sel.value;
      slot.moves[m] = v ? ((DATA.moves[v] || {}).name || '') : '';
    });
    return slot;
  }
  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  function writeSlotToUI(idx, slot) {
    const card = slotCard(idx);
    if (!slot) {
      card.querySelector('.tb-mon-select').value = '';
      card.querySelector('.tb-nickname').value = '';
      card.querySelector('.tb-level').value = '100';
      card.querySelector('.tb-item').value = '';
      card.querySelector('.tb-nature').value = 'Hardy';
      card.querySelectorAll('.tb-iv').forEach(inp => inp.value = '31');
      card.querySelectorAll('.tb-ev').forEach(inp => inp.value = '0');
      card.querySelectorAll('.tb-move-select').forEach(sel => sel.value = '');
      onMonChange(idx);
      return;
    }
    const slug = monByName[(slot.species || '').toLowerCase()];
    card.querySelector('.tb-mon-select').value = slug || '';
    card.querySelector('.tb-nickname').value = slot.nickname || '';
    card.querySelector('.tb-level').value = String(slot.level || 100);
    card.querySelector('.tb-item').value = slot.item || '';
    card.querySelector('.tb-nature').value = NATURES.indexOf(slot.nature) !== -1 ? slot.nature : 'Hardy';
    card.querySelectorAll('.tb-iv').forEach(inp => inp.value = String((slot.ivs && slot.ivs[inp.dataset.stat]) ?? 31));
    card.querySelectorAll('.tb-ev').forEach(inp => inp.value = String((slot.evs && slot.evs[inp.dataset.stat]) ?? 0));
    onMonChange(idx);
    // Ability after rebuild
    if (slot.ability) card.querySelector('.tb-ability-select').value = slot.ability;
    // Moves — if an imported move isn't in this species's learnset, append
    // it as a synthetic option marked "(not in learnset)" so the value is
    // preserved (the user can see and re-export it).
    Array.from(card.querySelectorAll('.tb-move-select')).forEach((sel, m) => {
      const moveName = (slot.moves || [])[m];
      if (!moveName) { sel.value = ''; return; }
      const moveSlug = moveByName[moveName.toLowerCase()];
      if (!moveSlug) { sel.value = ''; return; }
      if (!Array.from(sel.options).find(o => o.value === moveSlug)) {
        sel.appendChild(makeOption(moveSlug, moveName + ' (not in learnset)'));
      }
      sel.value = moveSlug;
    });
    // Trigger combobox refresh on all wrapped selects
    card.querySelectorAll('select').forEach(s => s.dispatchEvent(new Event('change')));
  }

  function clearSlot(idx) { writeSlotToUI(idx, null); refreshExport(); }
  function clearTeam() { for (let i = 0; i < SLOT_COUNT; i++) clearSlot(i); }
  function fillDefaults() {
    for (let i = 0; i < SLOT_COUNT; i++) {
      const card = slotCard(i);
      if (!card.querySelector('.tb-mon-select').value) continue;
      card.querySelector('.tb-level').value = '100';
      card.querySelectorAll('.tb-iv').forEach(inp => { if (!inp.value) inp.value = '31'; });
    }
    refreshExport();
  }

  // ---- Showdown serializer ----------------------------------------------
  function slotToShowdown(s) {
    if (!s || !s.species) return null;
    const lines = [];
    let head = s.nickname ? (s.nickname + ' (' + s.species + ')') : s.species;
    if (s.gender) head += ' (' + s.gender + ')';
    if (s.item) head += ' @ ' + s.item;
    lines.push(head);
    if (s.ability) lines.push('Ability: ' + s.ability);
    if (s.level && s.level !== 100) lines.push('Level: ' + s.level);
    if (s.shiny) lines.push('Shiny: Yes');
    if (s.happiness != null && s.happiness !== 255) lines.push('Happiness: ' + s.happiness);
    const evParts = STATS.map((st, i) => s.evs[st] ? (s.evs[st] + ' ' + STAT_LABELS[i]) : null).filter(Boolean);
    if (evParts.length) lines.push('EVs: ' + evParts.join(' / '));
    lines.push((s.nature || 'Hardy') + ' Nature');
    const ivParts = STATS.map((st, i) => (s.ivs[st] !== 31 ? (s.ivs[st] + ' ' + STAT_LABELS[i]) : null)).filter(Boolean);
    if (ivParts.length) lines.push('IVs: ' + ivParts.join(' / '));
    s.moves.filter(Boolean).forEach(m => lines.push('- ' + m));
    return lines.join('\n');
  }

  function exportShowdown() {
    const blocks = [];
    for (let i = 0; i < SLOT_COUNT; i++) {
      const slot = readSlotFromUI(i);
      const text = slotToShowdown(slot);
      if (text) blocks.push(text);
    }
    return blocks.join('\n\n');
  }

  function refreshExport() {
    $('tb-export').value = exportShowdown();
  }

  function copyExport() {
    const ta = $('tb-export');
    ta.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch (_) {}
    if (!ok && navigator.clipboard) navigator.clipboard.writeText(ta.value);
    const btn = $('tb-copy-btn');
    const old = btn.textContent;
    btn.textContent = 'Copied!';
    setTimeout(() => { btn.textContent = old; }, 1500);
  }

  // ---- Showdown parser ---------------------------------------------------
  function parseShowdown(text) {
    if (!text) return [];
    const blocks = text.replace(/\r\n/g, '\n').split(/\n\s*\n+/);
    return blocks.map(parseBlock).filter(Boolean);
  }

  function parseBlock(block) {
    const lines = block.split('\n').map(l => l.trim()).filter(Boolean);
    if (!lines.length) return null;
    const slot = emptySlot();

    // Header: "Nickname (Species) (Gender) @ Item" — every piece optional
    let header = lines[0];
    const atIdx = header.lastIndexOf(' @ ');
    if (atIdx !== -1) {
      slot.item = header.slice(atIdx + 3).trim();
      header = header.slice(0, atIdx).trim();
    }
    const gMatch = header.match(/\s+\((M|F)\)\s*$/);
    if (gMatch) {
      slot.gender = gMatch[1];
      header = header.slice(0, gMatch.index).trim();
    }
    const speciesMatch = header.match(/^(.+?)\s+\((.+)\)\s*$/);
    if (speciesMatch) {
      slot.nickname = speciesMatch[1].trim();
      slot.species = speciesMatch[2].trim();
    } else {
      slot.species = header.trim();
    }

    for (let i = 1; i < lines.length; i++) {
      const ln = lines[i];
      let mm;
      if ((mm = ln.match(/^Ability:\s*(.+)$/i)))   slot.ability = mm[1].trim();
      else if ((mm = ln.match(/^Level:\s*(\d+)$/i))) slot.level = parseInt(mm[1], 10);
      else if (ln.match(/^Shiny:\s*Yes$/i))         slot.shiny = true;
      else if ((mm = ln.match(/^Happiness:\s*(\d+)$/i))) slot.happiness = parseInt(mm[1], 10);
      else if ((mm = ln.match(/^EVs:\s*(.+)$/i)))   parseStatLine(mm[1], slot.evs);
      else if ((mm = ln.match(/^IVs:\s*(.+)$/i)))   parseStatLine(mm[1], slot.ivs);
      else if ((mm = ln.match(/^([A-Za-z]+)\s+Nature\s*$/i))) slot.nature = capitalize(mm[1]);
      else if ((mm = ln.match(/^[-•]\s*(.+)$/)))    {
        const idx = slot.moves.findIndex(x => !x);
        if (idx !== -1) slot.moves[idx] = mm[1].trim();
      }
      else if ((mm = ln.match(/^Tera Type:\s*(.+)$/i))) { /* ignored — not used on Pokefind */ }
    }
    return slot;
  }
  function parseStatLine(s, target) {
    s.split('/').forEach(part => {
      const [n, label] = part.trim().split(/\s+/);
      const idx = STAT_LABELS.findIndex(l => l.toLowerCase() === (label || '').toLowerCase());
      if (idx !== -1) target[STATS[idx]] = parseInt(n, 10);
    });
  }
  function capitalize(s) { return s ? s[0].toUpperCase() + s.slice(1).toLowerCase() : s; }

  function importFromText() {
    const text = $('tb-import').value;
    const team = parseShowdown(text);
    // Clear slots first, then write up to SLOT_COUNT
    for (let i = 0; i < SLOT_COUNT; i++) {
      writeSlotToUI(i, i < team.length ? team[i] : null);
    }
    refreshExport();
  }

  // ---- Init --------------------------------------------------------------
  function init() {
    load().then(buildUI);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
