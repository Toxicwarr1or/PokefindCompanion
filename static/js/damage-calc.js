// Pokefind damage calculator. Loads /calcdata.json (built by Hugo) and runs
// the Gen-8 damage formula client-side. No framework, no build step.
// Spec: https://bulbapedia.bulbagarden.net/wiki/Damage

(function () {
  'use strict';

  // ---- Type effectiveness chart (Gen 6+) ---------------------------------
  // 0 = immune, 0.5 = NVE, 1 = neutral, 2 = SE.
  const TYPES = ['Normal','Fire','Water','Electric','Grass','Ice','Fighting','Poison','Ground','Flying','Psychic','Bug','Rock','Ghost','Dragon','Dark','Steel','Fairy'];
  const CHART = {
    Normal:    { Rock: 0.5, Ghost: 0,   Steel: 0.5 },
    Fire:      { Fire: 0.5, Water: 0.5, Grass: 2,   Ice: 2,   Bug: 2,   Rock: 0.5, Dragon: 0.5, Steel: 2 },
    Water:     { Fire: 2,   Water: 0.5, Grass: 0.5, Ground: 2, Rock: 2,  Dragon: 0.5 },
    Electric:  { Water: 2,  Electric: 0.5, Grass: 0.5, Ground: 0, Flying: 2, Dragon: 0.5 },
    Grass:     { Fire: 0.5, Water: 2,   Grass: 0.5, Poison: 0.5, Ground: 2, Flying: 0.5, Bug: 0.5, Rock: 2, Dragon: 0.5, Steel: 0.5 },
    Ice:       { Fire: 0.5, Water: 0.5, Grass: 2,   Ice: 0.5,  Ground: 2, Flying: 2, Dragon: 2, Steel: 0.5 },
    Fighting:  { Normal: 2, Ice: 2, Poison: 0.5, Flying: 0.5, Psychic: 0.5, Bug: 0.5, Rock: 2, Ghost: 0, Dark: 2, Steel: 2, Fairy: 0.5 },
    Poison:    { Grass: 2, Poison: 0.5, Ground: 0.5, Rock: 0.5, Ghost: 0.5, Steel: 0, Fairy: 2 },
    Ground:    { Fire: 2, Electric: 2, Grass: 0.5, Poison: 2, Flying: 0, Bug: 0.5, Rock: 2, Steel: 2 },
    Flying:    { Electric: 0.5, Grass: 2, Fighting: 2, Bug: 2, Rock: 0.5, Steel: 0.5 },
    Psychic:   { Fighting: 2, Poison: 2, Psychic: 0.5, Dark: 0, Steel: 0.5 },
    Bug:       { Fire: 0.5, Grass: 2, Fighting: 0.5, Poison: 0.5, Flying: 0.5, Psychic: 2, Ghost: 0.5, Dark: 2, Steel: 0.5, Fairy: 0.5 },
    Rock:      { Fire: 2, Ice: 2, Fighting: 0.5, Ground: 0.5, Flying: 2, Bug: 2, Steel: 0.5 },
    Ghost:     { Normal: 0, Psychic: 2, Ghost: 2, Dark: 0.5 },
    Dragon:    { Dragon: 2, Steel: 0.5, Fairy: 0 },
    Dark:      { Fighting: 0.5, Psychic: 2, Ghost: 2, Dark: 0.5, Fairy: 0.5 },
    Steel:     { Fire: 0.5, Water: 0.5, Electric: 0.5, Ice: 2, Rock: 2, Steel: 0.5, Fairy: 2 },
    Fairy:     { Fire: 0.5, Fighting: 2, Poison: 0.5, Dragon: 2, Dark: 2, Steel: 0.5 }
  };
  const STAGE_MULT = [0.25, 0.285714, 0.333333, 0.4, 0.5, 0.666667, 1, 1.5, 2, 2.5, 3, 3.5, 4]; // -6..+6

  // ---- Ability effects ---------------------------------------------------
  // Each entry encodes a single ability's contribution to the damage formula.
  //   stab:           override the STAB multiplier (Adaptability sets ×2)
  //   normalToType:   re-type Normal-type moves to the given type, ×mult
  //   atkMult:        multiply attacker's effective Atk/SpA
  //   typeMult:       per-move-type damage multiplier (offensive)
  //   resistedMult:   multiplier when the target resists (eff < 1)
  //   superEffMult:   multiplier when the move is super-effective (eff > 1).
  //                   Used by both attacker (Neuroforce ×1.25) and defender
  //                   (Filter / Solid Rock / Prism Armor ×0.75).
  //   defTypeMult:    incoming-damage multiplier by move type (defender)
  //   specialMult:    incoming-special multiplier (defender)
  //   sandTypes:      apply mult to these types when sandstorm is active
  //   sunSpaMult:     SpA multiplier in harsh sun (Solar Power)
  //   immune:         move-type immunity (defender)
  //   wonderGuard:    only super-effective hits land
  //   mult:           generic flat damage multiplier (offensive or defensive,
  //                   tagged via `side`)
  const ABILITY_EFFECTS = {
    'Adaptability':         { side: 'att', stab: 2.0 },
    'Aerilate':             { side: 'att', normalToType: 'Flying', mult: 1.2 },
    'Pixilate':             { side: 'att', normalToType: 'Fairy',  mult: 1.2 },
    'Galvanize':            { side: 'att', normalToType: 'Electric', mult: 1.2 },
    'Refrigerate':          { side: 'att', normalToType: 'Ice',    mult: 1.2 },
    'Huge Power':           { side: 'att', atkMult: 2 },
    'Pure Power':           { side: 'att', atkMult: 2 },
    'Gorilla Tactics':      { side: 'att', atkMult: 1.5 },
    'Hustle':               { side: 'att', atkMult: 1.5 },
    'Guts':                 { side: 'att', atkMult: 1.5 },     // assumes statused
    'Tinted Lens':          { side: 'att', resistedMult: 2 },
    'Sheer Force':          { side: 'att', mult: 1.3 },        // assumes secondary-effect move
    'Sand Force':           { side: 'att', sandTypes: ['Rock', 'Ground', 'Steel'], mult: 1.3 },
    'Solar Power':          { side: 'att', sunSpaMult: 1.5 },
    'Flash Fire':           { side: 'att', typeMult: { Fire: 1.5 } },     // attacker — assumes powered up
    'Steelworker':          { side: 'att', typeMult: { Steel: 1.5 } },
    'Steely Spirit':        { side: 'att', typeMult: { Steel: 1.5 } },
    'Transistor':           { side: 'att', typeMult: { Electric: 1.5 } },
    'Water Bubble':         { side: 'both', typeMult: { Water: 2 }, defTypeMult: { Fire: 0.5 } },
    "Dragon's Maw":         { side: 'att', typeMult: { Dragon: 1.5 } },
    'Dragons Maw':          { side: 'att', typeMult: { Dragon: 1.5 } },
    'Neuroforce':           { side: 'att', superEffMult: 1.25 },
    'Blaze':                { side: 'att', typeMult: { Fire: 1.5 } },     // pinch trigger; we apply blanketly
    'Overgrow':             { side: 'att', typeMult: { Grass: 1.5 } },
    'Torrent':              { side: 'att', typeMult: { Water: 1.5 } },
    'Swarm':                { side: 'att', typeMult: { Bug: 1.5 } },
    'Multiscale':           { side: 'def', mult: 0.5 },
    'Shadow Shield':        { side: 'def', mult: 0.5 },
    'Filter':               { side: 'def', superEffMult: 0.75 },
    'Solid Rock':           { side: 'def', superEffMult: 0.75 },
    'Prism Armor':          { side: 'def', superEffMult: 0.75 },
    'Heatproof':            { side: 'def', defTypeMult: { Fire: 0.5 } },
    'Thick Fat':            { side: 'def', defTypeMult: { Fire: 0.5, Ice: 0.5 } },
    'Ice Scales':           { side: 'def', specialMult: 0.5 },
    'Fluffy':               { side: 'def', defTypeMult: { Fire: 2 } },     // contact halving omitted (no contact flag)
    'Levitate':             { side: 'def', immune: 'Ground' },
    'Sap Sipper':           { side: 'def', immune: 'Grass' },
    'Volt Absorb':          { side: 'def', immune: 'Electric' },
    'Lightning Rod':        { side: 'def', immune: 'Electric' },
    'Motor Drive':          { side: 'def', immune: 'Electric' },
    'Water Absorb':         { side: 'def', immune: 'Water' },
    'Storm Drain':          { side: 'def', immune: 'Water' },
    'Dry Skin':             { side: 'def', immune: 'Water', defTypeMult: { Fire: 1.25 } },
    'Wonder Guard':         { side: 'def', wonderGuard: true }
  };
  function abilityEffect(name) { return name ? ABILITY_EFFECTS[name] : null; }

  // ---- Hazard damage on switch-in ----------------------------------------
  // Stealth Rock: Rock-type effectiveness on the defender × maxHP / 8.
  // Spikes: 1/8, 1/6, 1/4 maxHP for 1/2/3 layers (assumes grounded).
  // Sticky Web: no damage (-1 Speed handled separately in the speed calc).
  function rockEffectiveness(types) {
    let m = 1;
    (types || []).forEach(t => { const v = (CHART['Rock'] || {})[t]; m *= (v === undefined ? 1 : v); });
    return m;
  }
  function hazardDamage(hp, hazards, types) {
    if (!hp || !hazards) return 0;
    let dmg = 0;
    if (hazards.sr) dmg += Math.floor(hp * rockEffectiveness(types) / 8);
    const spikesTable = [0, 1 / 8, 1 / 6, 1 / 4];
    if (hazards.spikes >= 1 && hazards.spikes <= 3) dmg += Math.floor(hp * spikesTable[hazards.spikes]);
    return Math.min(hp, dmg);
  }

  // ---- DOM helpers --------------------------------------------------------
  function $(id) { return document.getElementById(id); }
  function intVal(el, def) { const v = parseInt(el.value, 10); return isFinite(v) ? v : def; }

  // ---- State --------------------------------------------------------------
  let DATA = null;        // { pokemon: {...}, moves: {...} }
  let monIndex = [];      // [{slug,name,dex}] sorted by dex
  let moveIndex = [];     // [{slug,name,type,category,power}] sorted by name

  function load() {
    return fetch(new URL('/calcdata.json', document.baseURI).href)
      .then(r => r.json())
      .then(d => { DATA = d; buildIndexes(); populateSelects(); selectDefaults(); recompute(); });
  }

  function buildIndexes() {
    monIndex = Object.entries(DATA.pokemon).map(([slug, p]) => ({
      slug, name: p.name, dex: parseInt(p.dex || '0', 10)
    })).sort((a, b) => a.dex - b.dex || a.name.localeCompare(b.name));

    moveIndex = Object.entries(DATA.moves).map(([slug, m]) => ({
      slug, name: m.name, type: m.type, category: m.category, power: m.power
    })).filter(m => m.category !== 'Status' && parseInt(m.power, 10) > 0)
       .sort((a, b) => a.name.localeCompare(b.name));
  }

  function populateSelects() {
    ['dc-att-mon', 'dc-def-mon'].forEach(id => {
      const sel = $(id);
      sel.innerHTML = '';
      monIndex.forEach(m => {
        const o = document.createElement('option');
        o.value = m.slug;
        o.textContent = '#' + String(m.dex).padStart(3, '0') + ' ' + m.name;
        sel.appendChild(o);
      });
    });
    const mv = $('dc-move-name');
    mv.innerHTML = '';
    moveIndex.forEach(m => {
      const o = document.createElement('option');
      o.value = m.slug;
      o.textContent = m.name + ' — ' + m.type + ' ' + m.category + ' · ' + m.power + ' BP';
      mv.appendChild(o);
    });
  }

  // ---- Stat builders ------------------------------------------------------
  // Standard mainline formula (Gen 3+):
  //   HP    = floor((2*B + IV + floor(EV/4)) * L / 100) + L + 10
  //   other = floor(((2*B + IV + floor(EV/4)) * L / 100 + 5) * nature)
  function computeStat(stat, base, iv, ev, level, natureMult) {
    const inner = Math.floor((2 * base + iv + Math.floor(ev / 4)) * level / 100);
    if (stat === 'hp') return inner + level + 10;
    return Math.floor((inner + 5) * natureMult);
  }

  function readSide(prefix, stats) {
    const sideClass = prefix === 'att' ? 'dc-attacker' : 'dc-defender';
    const side = $('dc-' + prefix + '-mon');
    const formSel = $('dc-' + prefix + '-form');
    const monSlug = side.value;
    const mon = monSlug && DATA.pokemon[monSlug];
    const formIdx = formSel.value !== '' ? parseInt(formSel.value, 10) : 0;
    const form = mon && mon.forms[formIdx];
    const level = intVal($('dc-' + prefix + '-level'), 100);
    const burn = $('dc-' + prefix + '-burn') ? $('dc-' + prefix + '-burn').checked : false;
    const item = ($('dc-' + prefix + '-item') || {}).value || 'none';
    const ability = ($('dc-' + prefix + '-ability') || {}).value || '';
    const hazards = {
      sr:     $('dc-' + prefix + '-sr') ? $('dc-' + prefix + '-sr').checked : false,
      spikes: $('dc-' + prefix + '-spikes') ? parseInt($('dc-' + prefix + '-spikes').value || '0', 10) : 0,
      web:    $('dc-' + prefix + '-web') ? $('dc-' + prefix + '-web').checked : false
    };

    // Nature parsing: stored as "<mult>|<stat>" (e.g. "1.1|atk") or "1.0".
    const natureSel = document.querySelector('.' + sideClass + ' .dc-nature');
    const natureRaw = natureSel ? natureSel.value : '1.0';
    let natureBoosted = null, natureMult = 1.0;
    if (natureRaw.indexOf('|') !== -1) {
      const [m, s] = natureRaw.split('|');
      natureMult = parseFloat(m);
      natureBoosted = s;
    }

    const result = { mon, form, level, burn, item, ability, hazards, stats: {}, stages: {} };
    const rows = document.querySelectorAll('.' + sideClass + ' .dc-stat-builder tbody tr');
    rows.forEach(row => {
      const stat = row.dataset.stat;
      const base = (form && form.stats[stat]) || 0;
      row.querySelector('.dc-base').textContent = base || '—';
      const inputs = row.querySelectorAll('input');
      const iv = intVal(inputs[0], 31);
      const ev = intVal(inputs[1], 0);
      const stageSel = row.querySelector('.dc-stage');
      const stage = stageSel ? parseInt(stageSel.value.replace('+', ''), 10) : 0;
      const isBoostedStat = stat === natureBoosted ? natureMult : 1.0;
      const final = computeStat(stat, base, iv, ev, level, isBoostedStat);
      result.stats[stat] = final;
      result.stages[stat] = stage;
      row.querySelector('.dc-final').textContent = final;
    });
    // Update types display
    const typesEl = $('dc-' + prefix + '-types');
    typesEl.innerHTML = '';
    if (form && form.types) {
      form.types.forEach(t => {
        const span = document.createElement('span');
        span.className = 'type-' + t.toLowerCase();
        span.textContent = t;
        typesEl.appendChild(span);
      });
    }
    return result;
  }

  function readMove() {
    const slug = $('dc-move-name').value;
    if (!slug) return null;
    const m = DATA.moves[slug];
    if (!m) return null;
    $('dc-move-type').textContent = m.type;
    $('dc-move-type').className = 'dc-chip type-' + m.type.toLowerCase();
    $('dc-move-cat').textContent = m.category;
    $('dc-move-power').textContent = m.power;
    return m;
  }

  function effectiveness(moveType, defenderTypes) {
    let mult = 1;
    defenderTypes.forEach(t => {
      const v = (CHART[moveType] || {})[t];
      mult *= (v === undefined ? 1 : v);
    });
    return mult;
  }

  function applyStage(stat, stage) {
    return Math.max(-6, Math.min(6, stage)) + 6;
  }

  // ---- Damage formula -----------------------------------------------------
  function calcDamage(att, def, move) {
    if (!att.form || !def.form || !move || move.category === 'Status') return null;
    const power = parseInt(move.power, 10);
    if (!isFinite(power) || power <= 0) return null;

    const isPhysical = move.category === 'Physical';
    const attackStatKey = isPhysical ? 'atk' : 'spa';
    const defenseStatKey = isPhysical ? 'def' : 'spd';

    // ---- Ability lookups ----
    const aEff = abilityEffect(att.ability);
    const dEff = abilityEffect(def.ability);

    // Aerilate / Pixilate / Galvanize / Refrigerate retype Normal moves to
    // the matching type, with a ×1.2 power boost. We apply both the type
    // change (so STAB/effectiveness recompute) and the multiplier later.
    let moveType = move.type;
    let aerilateMult = 1;
    if (aEff && aEff.normalToType && moveType === 'Normal') {
      moveType = aEff.normalToType;
      aerilateMult = aEff.mult || 1;
    }

    // Stat with stage boost (crit ignores defender's positive boosts and
    // attacker's negative boosts, per Gen-6+).
    const crit = parseFloat($('dc-crit').value);
    let A = att.stats[attackStatKey];
    let D = def.stats[defenseStatKey];
    let aStage = att.stages[attackStatKey];
    let dStage = def.stages[defenseStatKey];
    if (crit > 1) {
      if (aStage < 0) aStage = 0;
      if (dStage > 0) dStage = 0;
    }
    A = Math.floor(A * STAGE_MULT[applyStage('a', aStage)]);
    D = Math.floor(D * STAGE_MULT[applyStage('d', dStage)]);

    // Attacker ability stat multipliers (Huge Power / Pure Power / Hustle /
    // Gorilla Tactics / Guts × Atk; Solar Power × SpA in sun).
    if (aEff && aEff.atkMult) A = Math.floor(A * aEff.atkMult);
    if (aEff && aEff.sunSpaMult && !isPhysical && $('dc-weather').value === 'sun') {
      A = Math.floor(A * aEff.sunSpaMult);
    }

    // Burn halves physical Atk (unless ability prevents — out of scope).
    if (isPhysical && att.burn) A = Math.floor(A / 2);

    // Base damage (Gen 5+ floor sequence).
    let dmg = Math.floor(Math.floor(Math.floor(2 * att.level / 5 + 2) * power * A / D) / 50) + 2;

    // Modifiers (multiplied in sequence).
    let mod = 1;

    // Weather — sun/rain ×1.5 same-type, ×0.5 opposite. Ice/Rock immune to its-own-weather residual but that's HP, not damage.
    const weather = $('dc-weather').value;
    if (weather === 'sun')  { if (moveType === 'Fire')  mod *= 1.5; if (moveType === 'Water') mod *= 0.5; }
    if (weather === 'rain') { if (moveType === 'Water') mod *= 1.5; if (moveType === 'Fire')  mod *= 0.5; }
    if (weather === 'sand' && def.form.types.indexOf('Rock') !== -1 && !isPhysical) mod *= 1.5; // sand SpD boost

    // Terrain (Gen 8 multiplier ×1.3, only if user is "grounded" — the calc assumes grounded).
    const terrain = $('dc-terrain').value;
    if (terrain === 'electric' && moveType === 'Electric') mod *= 1.3;
    if (terrain === 'grassy'   && moveType === 'Grass')    mod *= 1.3;
    if (terrain === 'psychic'  && moveType === 'Psychic')  mod *= 1.3;
    if (terrain === 'misty'    && moveType === 'Dragon')   mod *= 0.5;

    // Screens (Reflect/Light Screen). Ignored on crits.
    if ($('dc-screen').checked && crit === 1) mod *= 0.5;

    // STAB. Adaptability bumps it from ×1.5 to ×2.
    if (att.form.types.indexOf(moveType) !== -1) {
      mod *= (aEff && aEff.stab) ? aEff.stab : 1.5;
    }

    // Aerilate-style retype boost (the type change is reflected in moveType).
    if (aerilateMult !== 1) mod *= aerilateMult;

    // Defender ability immunities and Wonder Guard (computed before eff).
    let eff = effectiveness(moveType, def.form.types);
    if (dEff && dEff.immune && dEff.immune === moveType) eff = 0;
    if (dEff && dEff.wonderGuard && eff <= 1) eff = 0;

    // Crit.
    mod *= crit;

    // ---- Attacker ability mods ----
    if (aEff && aEff.typeMult && aEff.typeMult[moveType]) mod *= aEff.typeMult[moveType];
    if (aEff && aEff.sandTypes && aEff.sandTypes.indexOf(moveType) !== -1 && weather === 'sand') mod *= aEff.mult;
    if (aEff && aEff.superEffMult && eff > 1) mod *= aEff.superEffMult;
    if (aEff && aEff.resistedMult && eff < 1 && eff > 0) mod *= aEff.resistedMult;
    if (aEff && aEff.mult && !aEff.sandTypes && !aEff.normalToType) mod *= aEff.mult;

    // ---- Defender ability mods ----
    if (dEff && dEff.defTypeMult && dEff.defTypeMult[moveType]) mod *= dEff.defTypeMult[moveType];
    if (dEff && dEff.specialMult && !isPhysical) mod *= dEff.specialMult;
    if (dEff && dEff.superEffMult && eff > 1) mod *= dEff.superEffMult;
    if (dEff && dEff.mult) mod *= dEff.mult;

    // Water Bubble (attacker ×2 Water; defender ×0.5 Fire) — already covered
    // by typeMult / defTypeMult depending on which side selected it.


    // ---- Attacker items ----
    const aItem = att.item;
    // General offensive multipliers
    if (aItem === 'life-orb')                                           mod *= 1.3;
    if (aItem === 'choice-band' && isPhysical)                          mod *= 1.5;
    if (aItem === 'choice-specs' && !isPhysical)                        mod *= 1.5;
    if (aItem === 'expert-belt' && eff > 1)                             mod *= 1.2;
    if (aItem === 'muscle-band' && isPhysical)                          mod *= 1.1;
    if (aItem === 'wise-glasses' && !isPhysical)                        mod *= 1.1;
    if (aItem === 'metronome')                                          mod *= 1.2; // 1st-hit estimate
    // Type-boost trinkets (×1.2 of matching type)
    const TYPE_BOOST_TRINKETS = {
      'black-belt': 'Fighting', 'black-glasses': 'Dark', 'charcoal': 'Fire',
      'dragon-fang': 'Dragon', 'hard-stone': 'Rock', 'magnet': 'Electric',
      'metal-coat': 'Steel', 'miracle-seed': 'Grass', 'mystic-water': 'Water',
      'never-melt-ice': 'Ice', 'odd-incense': 'Psychic', 'poison-barb': 'Poison',
      'rose-incense': 'Grass', 'sea-incense': 'Water', 'sharp-beak': 'Flying',
      'silk-scarf': 'Normal', 'silver-powder': 'Bug', 'soft-sand': 'Ground',
      'spell-tag': 'Ghost'
    };
    if (TYPE_BOOST_TRINKETS[aItem] === move.type) mod *= 1.2;
    // Arceus plates (also ×1.2 of matching type — same multiplier)
    const PLATES = {
      'draco-plate': 'Dragon', 'dread-plate': 'Dark', 'earth-plate': 'Ground',
      'fist-plate': 'Fighting', 'flame-plate': 'Fire', 'icicle-plate': 'Ice',
      'insect-plate': 'Bug', 'iron-plate': 'Steel', 'meadow-plate': 'Grass',
      'mind-plate': 'Psychic', 'pixie-plate': 'Fairy', 'sky-plate': 'Flying',
      'splash-plate': 'Water', 'spooky-plate': 'Ghost', 'stone-plate': 'Rock',
      'toxic-plate': 'Poison', 'zap-plate': 'Electric'
    };
    if (PLATES[aItem] === move.type) mod *= 1.2;
    // Species-specific items (multiplier on the base stat is the canonical
    // implementation; here we approximate as a damage multiplier when the
    // holder is the right species).
    const monName = (att.mon && att.mon.name || '').toLowerCase();
    if (aItem === 'light-ball' && monName === 'pikachu')                mod *= 2;
    if (aItem === 'thick-club' && (monName === 'cubone' || monName === 'marowak') && isPhysical) mod *= 2;
    if (aItem === 'deep-sea-tooth' && monName === 'clamperl' && !isPhysical) mod *= 2;
    if (aItem === 'metal-powder' && monName === 'ditto' && isPhysical)  mod *= 2; // boosts Def — affects damage taken; included for completeness

    // ---- Defender items ----
    const dItem = def.item;
    if (dItem === 'eviolite')                                           mod *= 1 / 1.5;
    if (dItem === 'assault-vest' && !isPhysical)                        mod *= 1 / 1.5;
    const monNameD = (def.mon && def.mon.name || '').toLowerCase();
    if (dItem === 'deep-sea-scale' && monNameD === 'clamperl' && !isPhysical) mod *= 1 / 2;
    // Resist berries — halve damage from one super-effective hit of that
    // type. Chilan halves any Normal-type hit (regardless of effectiveness).
    const RESIST_BERRIES = {
      'occa-berry': 'Fire', 'passho-berry': 'Water', 'wacan-berry': 'Electric',
      'rindo-berry': 'Grass', 'yache-berry': 'Ice', 'chople-berry': 'Fighting',
      'kebia-berry': 'Poison', 'shuca-berry': 'Ground', 'coba-berry': 'Flying',
      'payapa-berry': 'Psychic', 'tanga-berry': 'Bug', 'charti-berry': 'Rock',
      'kasib-berry': 'Ghost', 'haban-berry': 'Dragon', 'colbur-berry': 'Dark',
      'babiri-berry': 'Steel', 'roseli-berry': 'Fairy'
    };
    if (RESIST_BERRIES[dItem] === move.type && eff > 1)                 mod *= 0.5;
    if (dItem === 'chilan-berry' && move.type === 'Normal')             mod *= 0.5;

    // Apply mods, then effectiveness (effectiveness is multiplicative).
    const baseAfterMods = dmg * mod * eff;

    // Random factor 0.85..1.00 (16-step Gen-3+ roll).
    const minDmg = Math.max(1, Math.floor(baseAfterMods * 0.85));
    const maxDmg = Math.max(1, Math.floor(baseAfterMods * 1.00));
    const rolls = [];
    for (let i = 0; i < 16; i++) {
      const factor = 0.85 + i / 100;
      rolls.push(Math.max(1, Math.floor(baseAfterMods * factor)));
    }
    return { min: minDmg, max: maxDmg, rolls, eff };
  }

  // ---- KO probability -----------------------------------------------------
  // Rough single-hit KO chance: fraction of the 16 rolls that >= defender HP.
  function koProbability(rolls, hp) {
    if (!rolls || !hp) return null;
    const ok = rolls.filter(r => r >= hp).length;
    return ok / rolls.length;
  }

  // ---- Form picker handling ------------------------------------------------
  function rebuildForms(prefix) {
    const slug = $('dc-' + prefix + '-mon').value;
    const formSel = $('dc-' + prefix + '-form');
    const previousValue = formSel.value;
    formSel.innerHTML = '';
    if (!slug || !DATA.pokemon[slug]) return;
    const mon = DATA.pokemon[slug];
    mon.forms.forEach((f, i) => {
      const o = document.createElement('option');
      o.value = String(i);
      o.textContent = f.name;
      formSel.appendChild(o);
    });
    if (previousValue && formSel.querySelector('option[value="' + previousValue + '"]')) {
      formSel.value = previousValue;
    }
    rebuildAbilities(prefix);
  }

  // Repopulate the ability dropdown from the chosen Pokémon's abilities
  // + hidden ability. Preserves the previous selection when still legal.
  function rebuildAbilities(prefix) {
    const abilSel = $('dc-' + prefix + '-ability');
    if (!abilSel) return;
    const slug = $('dc-' + prefix + '-mon').value;
    const formIdx = parseInt($('dc-' + prefix + '-form').value || '0', 10);
    const mon = slug && DATA.pokemon[slug];
    const form = mon && mon.forms[formIdx];
    const previous = abilSel.value;
    abilSel.innerHTML = '';
    const none = document.createElement('option');
    none.value = '';
    none.textContent = 'None';
    abilSel.appendChild(none);
    if (form) {
      (form.abilities || []).forEach(a => {
        const o = document.createElement('option');
        o.value = a; o.textContent = a;
        abilSel.appendChild(o);
      });
      if (form.hidden) {
        const o = document.createElement('option');
        o.value = form.hidden;
        o.textContent = form.hidden + ' (Hidden)';
        abilSel.appendChild(o);
      }
    }
    if (previous && abilSel.querySelector('option[value="' + previous.replace(/"/g, '\\"') + '"]')) {
      abilSel.value = previous;
    }
    abilSel.dispatchEvent(new Event('change'));
  }

  // ---- Main update --------------------------------------------------------
  function recompute() {
    if (!DATA) return;
    rebuildForms('att');
    rebuildForms('def');
    const att = readSide('att');
    const def = readSide('def');
    const move = readMove();
    const out = calcDamage(att, def, move);
    if (!out) {
      $('dc-result-range').textContent = '—';
      $('dc-result-pct').textContent = '—';
      $('dc-result-eff').textContent = '—';
      $('dc-result-ko').textContent = '—';
      $('dc-result-note').textContent = '';
      return;
    }
    const hp = def.stats.hp;
    // Effective HP after the defender's hazards have chipped on switch-in.
    const hzDmg = hazardDamage(hp, def.hazards, def.form.types);
    const effectiveHp = Math.max(1, hp - hzDmg);
    $('dc-result-range').textContent = out.min + ' – ' + out.max;
    $('dc-result-pct').textContent = ((out.min / effectiveHp) * 100).toFixed(1) + '% – ' +
                                      ((out.max / effectiveHp) * 100).toFixed(1) + '%';
    let effLabel;
    if (out.eff === 0) effLabel = 'Immune (×0)';
    else if (out.eff < 1) effLabel = 'Not very effective (×' + out.eff + ')';
    else if (out.eff > 1) effLabel = 'Super effective (×' + out.eff + ')';
    else effLabel = 'Neutral (×1)';
    $('dc-result-eff').textContent = effLabel;
    const ko = koProbability(out.rolls, effectiveHp);
    if (ko === null) $('dc-result-ko').textContent = '—';
    else if (ko === 1) $('dc-result-ko').textContent = 'Guaranteed OHKO';
    else if (ko === 0) $('dc-result-ko').textContent = 'No OHKO chance';
    else $('dc-result-ko').textContent = (ko * 100).toFixed(1) + '% OHKO';
    let note = 'Defender HP: ' + hp;
    if (hzDmg > 0) note += ' · After hazards: ' + effectiveHp + ' (-' + hzDmg + ')';
    note += ' · Attacker level: ' + att.level + ' · Random factor 0.85–1.00 (16 rolls)';
    $('dc-result-note').textContent = note;
  }

  // ---- Event wiring -------------------------------------------------------
  function selectDefaults() {
    if (monIndex.length) {
      $('dc-att-mon').value = monIndex[0].slug;
      $('dc-def-mon').value = monIndex.length > 1 ? monIndex[1].slug : monIndex[0].slug;
    }
    if (moveIndex.length) $('dc-move-name').value = moveIndex[0].slug;
  }

  // ---- Searchable combobox (replaces native <select> for long lists) ------
  // The native <select> remains in the DOM as the canonical source of truth
  // (so existing read sites that look at `el.value` still work). It's hidden
  // visually; a custom combobox UI sits next to it, lets the user filter
  // options by typing, and writes the chosen value back to the select before
  // dispatching a 'change' event so recompute() runs.
  const comboboxes = [];
  function attachCombobox(selectEl) {
    const wrapper = document.createElement('div');
    wrapper.className = 'dc-combobox';
    selectEl.parentNode.insertBefore(wrapper, selectEl);
    wrapper.appendChild(selectEl);
    selectEl.classList.add('dc-hidden-select');

    const display = document.createElement('button');
    display.type = 'button';
    display.className = 'dc-combobox-display';

    const panel = document.createElement('div');
    panel.className = 'dc-combobox-panel';
    panel.hidden = true;

    const search = document.createElement('input');
    search.type = 'text';
    search.className = 'dc-combobox-search';
    search.placeholder = 'Type to filter…';
    search.autocomplete = 'off';

    const list = document.createElement('ul');
    list.className = 'dc-combobox-list';
    list.setAttribute('role', 'listbox');

    panel.appendChild(search);
    panel.appendChild(list);
    wrapper.appendChild(display);
    wrapper.appendChild(panel);

    let activeIdx = -1;
    let filtered = [];

    function refreshDisplay() {
      const opt = selectEl.options[selectEl.selectedIndex];
      display.textContent = opt ? opt.textContent : '—';
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
        li.className = 'dc-combobox-item';
        if (opt.value === selectEl.value) {
          li.classList.add('selected');
          activeIdx = filtered.length;
        }
        li.textContent = text;
        li.addEventListener('mousedown', e => {
          e.preventDefault();
          selectOption(opt.value);
        });
        list.appendChild(li);
        filtered.push({ li, value: opt.value });
      });
      if (activeIdx === -1 && filtered.length) activeIdx = 0;
      highlightActive();
    }
    function highlightActive() {
      filtered.forEach((f, i) => f.li.classList.toggle('active', i === activeIdx));
      if (activeIdx >= 0 && filtered[activeIdx]) {
        filtered[activeIdx].li.scrollIntoView({ block: 'nearest' });
      }
    }
    function selectOption(value) {
      selectEl.value = value;
      selectEl.dispatchEvent(new Event('change', { bubbles: true }));
      refreshDisplay();
      close();
      display.focus();
    }
    function open() {
      panel.hidden = false;
      search.value = '';
      rebuildList('');
      setTimeout(() => search.focus(), 0);
    }
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
    comboboxes.push({ refresh: refreshDisplay });
    return refreshDisplay;
  }

  // ---- Shared item list (populates both Attacker and Defender pickers) ----
  // Damage-relevant held items extracted from
  //   PokemonWorld-master/.../co/pokefind/pokemon/item/Item.java
  // The label includes a category prefix so the combobox search matches both
  // by item name ("life orb") and by category ("plate", "berry").
  const ITEMS = [
    { value: 'none', label: 'None' },
    // ---- General offensive ----
    { value: 'life-orb',     label: '[Offensive] Life Orb (×1.3, all damaging)' },
    { value: 'choice-band',  label: '[Offensive] Choice Band (×1.5 Atk)' },
    { value: 'choice-specs', label: '[Offensive] Choice Specs (×1.5 SpA)' },
    { value: 'muscle-band',  label: '[Offensive] Muscle Band (×1.1 physical)' },
    { value: 'wise-glasses', label: '[Offensive] Wise Glasses (×1.1 special)' },
    { value: 'expert-belt',  label: '[Offensive] Expert Belt (×1.2 super-effective)' },
    { value: 'metronome',    label: '[Offensive] Metronome (×1.2 same-move first hit)' },
    { value: 'shell-bell',   label: '[Offensive] Shell Bell (heals 1/8 — no damage mod)' },
    // ---- Type-boost trinkets (×1.2 of matching type) ----
    { value: 'black-belt',     label: '[Type-boost] Black Belt (Fighting)' },
    { value: 'black-glasses',  label: '[Type-boost] Black Glasses (Dark)' },
    { value: 'charcoal',       label: '[Type-boost] Charcoal (Fire)' },
    { value: 'dragon-fang',    label: '[Type-boost] Dragon Fang (Dragon)' },
    { value: 'hard-stone',     label: '[Type-boost] Hard Stone (Rock)' },
    { value: 'magnet',         label: '[Type-boost] Magnet (Electric)' },
    { value: 'metal-coat',     label: '[Type-boost] Metal Coat (Steel)' },
    { value: 'miracle-seed',   label: '[Type-boost] Miracle Seed (Grass)' },
    { value: 'mystic-water',   label: '[Type-boost] Mystic Water (Water)' },
    { value: 'never-melt-ice', label: '[Type-boost] Never-Melt Ice (Ice)' },
    { value: 'odd-incense',    label: '[Type-boost] Odd Incense (Psychic)' },
    { value: 'poison-barb',    label: '[Type-boost] Poison Barb (Poison)' },
    { value: 'rose-incense',   label: '[Type-boost] Rose Incense (Grass)' },
    { value: 'sea-incense',    label: '[Type-boost] Sea Incense (Water)' },
    { value: 'sharp-beak',     label: '[Type-boost] Sharp Beak (Flying)' },
    { value: 'silk-scarf',     label: '[Type-boost] Silk Scarf (Normal)' },
    { value: 'silver-powder',  label: '[Type-boost] Silver Powder (Bug)' },
    { value: 'soft-sand',      label: '[Type-boost] Soft Sand (Ground)' },
    { value: 'spell-tag',      label: '[Type-boost] Spell Tag (Ghost)' },
    // ---- Arceus plates (×1.2 of plate type) ----
    { value: 'draco-plate',  label: '[Plate] Draco Plate (Dragon)' },
    { value: 'dread-plate',  label: '[Plate] Dread Plate (Dark)' },
    { value: 'earth-plate',  label: '[Plate] Earth Plate (Ground)' },
    { value: 'fist-plate',   label: '[Plate] Fist Plate (Fighting)' },
    { value: 'flame-plate',  label: '[Plate] Flame Plate (Fire)' },
    { value: 'icicle-plate', label: '[Plate] Icicle Plate (Ice)' },
    { value: 'insect-plate', label: '[Plate] Insect Plate (Bug)' },
    { value: 'iron-plate',   label: '[Plate] Iron Plate (Steel)' },
    { value: 'meadow-plate', label: '[Plate] Meadow Plate (Grass)' },
    { value: 'mind-plate',   label: '[Plate] Mind Plate (Psychic)' },
    { value: 'pixie-plate',  label: '[Plate] Pixie Plate (Fairy)' },
    { value: 'sky-plate',    label: '[Plate] Sky Plate (Flying)' },
    { value: 'splash-plate', label: '[Plate] Splash Plate (Water)' },
    { value: 'spooky-plate', label: '[Plate] Spooky Plate (Ghost)' },
    { value: 'stone-plate',  label: '[Plate] Stone Plate (Rock)' },
    { value: 'toxic-plate',  label: '[Plate] Toxic Plate (Poison)' },
    { value: 'zap-plate',    label: '[Plate] Zap Plate (Electric)' },
    // ---- Species-specific ----
    { value: 'light-ball',     label: '[Species] Light Ball — Pikachu (×2 Atk & SpA)' },
    { value: 'thick-club',     label: '[Species] Thick Club — Cubone/Marowak (×2 Atk)' },
    { value: 'deep-sea-tooth', label: '[Species] Deep Sea Tooth — Clamperl (×2 SpA)' },
    { value: 'metal-powder',   label: '[Species] Metal Powder — Ditto (×2 Def)' },
    { value: 'lucky-punch',    label: '[Species] Lucky Punch — Chansey (crit boost)' },
    // ---- Defensive multipliers ----
    { value: 'eviolite',       label: '[Defensive] Eviolite (×1.5 Def & SpD, NFE)' },
    { value: 'assault-vest',   label: '[Defensive] Assault Vest (×1.5 SpD)' },
    { value: 'rocky-helmet',   label: '[Defensive] Rocky Helmet (chip on contact — no damage mod)' },
    { value: 'deep-sea-scale', label: '[Defensive] Deep Sea Scale — Clamperl (×2 SpD)' },
    // ---- Resist berries ----
    { value: 'occa-berry',    label: '[Berry] Occa (½ super-effective Fire)' },
    { value: 'passho-berry',  label: '[Berry] Passho (½ super-effective Water)' },
    { value: 'wacan-berry',   label: '[Berry] Wacan (½ super-effective Electric)' },
    { value: 'rindo-berry',   label: '[Berry] Rindo (½ super-effective Grass)' },
    { value: 'yache-berry',   label: '[Berry] Yache (½ super-effective Ice)' },
    { value: 'chople-berry',  label: '[Berry] Chople (½ super-effective Fighting)' },
    { value: 'kebia-berry',   label: '[Berry] Kebia (½ super-effective Poison)' },
    { value: 'shuca-berry',   label: '[Berry] Shuca (½ super-effective Ground)' },
    { value: 'coba-berry',    label: '[Berry] Coba (½ super-effective Flying)' },
    { value: 'payapa-berry',  label: '[Berry] Payapa (½ super-effective Psychic)' },
    { value: 'tanga-berry',   label: '[Berry] Tanga (½ super-effective Bug)' },
    { value: 'charti-berry',  label: '[Berry] Charti (½ super-effective Rock)' },
    { value: 'kasib-berry',   label: '[Berry] Kasib (½ super-effective Ghost)' },
    { value: 'haban-berry',   label: '[Berry] Haban (½ super-effective Dragon)' },
    { value: 'colbur-berry',  label: '[Berry] Colbur (½ super-effective Dark)' },
    { value: 'babiri-berry',  label: '[Berry] Babiri (½ super-effective Steel)' },
    { value: 'roseli-berry',  label: '[Berry] Roseli (½ super-effective Fairy)' },
    { value: 'chilan-berry',  label: '[Berry] Chilan (½ any Normal hit)' },
  ];
  function populateItemSelects() {
    ['dc-att-item', 'dc-def-item'].forEach(id => {
      const sel = $(id);
      sel.innerHTML = '';
      ITEMS.forEach(it => {
        const o = document.createElement('option');
        o.value = it.value;
        o.textContent = it.label;
        sel.appendChild(o);
      });
    });
  }

  // ---- Speed Calculator ---------------------------------------------------
  const SPEED_ITEM_MULT = {
    'choice-scarf': 1.5,
    'iron-ball':    0.5,
    'macho-brace':  0.5,
    'quick-powder': 2.0,        // Ditto only (gated below)
    'lagging-tail': 1.0,        // ranking handled separately ("always last")
    'full-incense': 1.0
  };
  function readSpeedSide(prefix) {
    const sideClass = prefix === 'att' ? 'dc-speed-attacker' : 'dc-speed-defender';
    const dmgSide = readSide(prefix);              // share Pokémon, level, form
    const form = dmgSide.form;
    const base = (form && form.stats.spe) || 0;
    const row = document.querySelector('.' + sideClass + ' .dc-stat-builder tbody tr[data-stat="spe"]');
    const baseCell = row.querySelector('.dc-base');
    baseCell.textContent = base || '—';
    const inputs = row.querySelectorAll('input');
    const iv = intVal(inputs[0], 31);
    const ev = intVal(inputs[1], 0);
    const stage = parseInt(row.querySelector('.dc-stage').value.replace('+', ''), 10) || 0;
    const natureRaw = document.querySelector('.' + sideClass + ' .dc-nature').value;
    const natureMult = (natureRaw.indexOf('|') !== -1 && natureRaw.split('|')[1] === 'spe')
      ? parseFloat(natureRaw.split('|')[0])
      : 1.0;
    let speed = computeStat('spe', base, iv, ev, dmgSide.level, natureMult);
    // Sticky Web on this side drops 1 Speed stage on switch-in.
    if (dmgSide.hazards && dmgSide.hazards.web) stage -= 1;
    // Stage modifier
    speed = Math.floor(speed * STAGE_MULT[applyStage('s', stage)]);
    // Item
    const item = $('dc-' + prefix + '-spd-item').value;
    const monName = (dmgSide.mon && dmgSide.mon.name || '').toLowerCase();
    if (item === 'quick-powder' && monName !== 'ditto') {
      // Quick Powder only doubles for Ditto; otherwise no effect.
    } else if (SPEED_ITEM_MULT[item]) {
      speed = Math.floor(speed * SPEED_ITEM_MULT[item]);
    }
    // Status
    if ($('dc-' + prefix + '-paralysis').checked)  speed = Math.floor(speed * 0.5);
    if ($('dc-' + prefix + '-tailwind').checked)   speed = Math.floor(speed * 2);
    row.querySelector('.dc-final').textContent = speed;
    const movesLast = item === 'lagging-tail' || item === 'full-incense';
    return { speed, movesLast };
  }

  function recomputeSpeed() {
    if (!DATA) return;
    const att = readSpeedSide('att');
    const def = readSpeedSide('def');
    $('dc-speed-att').textContent = att.speed;
    $('dc-speed-def').textContent = def.speed;
    const trickRoom = $('dc-trick-room').checked;
    let outcome;
    // "Always-last" items override the speed comparison entirely.
    if (att.movesLast && def.movesLast) {
      outcome = att.speed === def.speed ? 'Speed tie (both move last)' :
        (att.speed > def.speed ? 'Defender first (both move last; slower wins)' : 'Attacker first (both move last; slower wins)');
    } else if (att.movesLast) {
      outcome = 'Defender moves first (Attacker holds an "always last" item)';
    } else if (def.movesLast) {
      outcome = 'Attacker moves first (Defender holds an "always last" item)';
    } else if (att.speed === def.speed) {
      outcome = 'Speed tie — 50/50 coin flip';
    } else {
      const attFaster = att.speed > def.speed;
      const winner = trickRoom ? !attFaster : attFaster;
      outcome = (winner ? 'Attacker' : 'Defender') + ' moves first' +
        (trickRoom ? ' (Trick Room: slower goes first)' : '');
    }
    $('dc-speed-result').textContent = outcome;
  }

  // Hook speed recompute into the main recompute pipeline.
  // Re-entry guard: rebuildAbilities() dispatches a `change` event on the
  // ability <select> so the combobox display updates, but the global
  // change listener (every input/select on the page) calls recompute,
  // which re-runs rebuildForms → rebuildAbilities → dispatch — an
  // infinite loop that hangs the page. The flag breaks that cycle.
  const _origRecompute = recompute;
  let _recomputeInFlight = false;
  recompute = function () {
    if (_recomputeInFlight) return;
    _recomputeInFlight = true;
    try { _origRecompute(); recomputeSpeed(); }
    finally { _recomputeInFlight = false; }
  };

  function init() {
    populateItemSelects();
    document.querySelectorAll('.damage-calc-page input, .damage-calc-page select')
      .forEach(el => el.addEventListener('input', recompute));
    document.querySelectorAll('.damage-calc-page input, .damage-calc-page select')
      .forEach(el => el.addEventListener('change', recompute));
    load().then(() => {
      // Attach combobox UI after the selects are populated and defaults applied.
      ['dc-att-mon', 'dc-def-mon', 'dc-move-name',
       'dc-att-item', 'dc-def-item',
       'dc-att-ability', 'dc-def-ability']
        .forEach(id => attachCombobox($(id)));
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
