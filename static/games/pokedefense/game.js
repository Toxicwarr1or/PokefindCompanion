/* PokéDefense — tower defence game logic.
 * Plain ES6, no bundler. Mounted inside .pokedefense-app from layouts/games/pokedefense.html.
 */

(function () {
  'use strict';

  // === CONFIG & CONSTANTS ===
  const CELL = 40;
  const COLS = 20;
  const ROWS = 12;
  const WIDTH = COLS * CELL;   // 800
  const HEIGHT = ROWS * CELL;  // 500
  const DT_CAP = 0.05;         // seconds; clamp deltaTime to avoid spiral-of-death

  const SPEEDS = { slow: 1.5, normal: 2.5, fast: 4.0 }; // cells/sec

  const COLORS = {
    grass: '#4a7c59',
    grassAlt: '#43705071',
    path: '#c8a96e',
    pathEdge: '#a4895a',
    entrance: '#d44',
    exit: '#3eb045',
    rangeFill: 'rgba(62,176,69,0.10)',
    rangeStroke: 'rgba(62,176,69,0.55)',
    hpBack: 'rgba(0,0,0,0.55)',
    hpFront: '#7ad07b',
    hpBoss: '#e0535c'
  };

  const STATUS_COLORS = {
    slow: 'rgba(96,160,255,0.85)',
    freeze: 'rgba(140,220,255,0.95)',
    burn: 'rgba(255,140,60,0.9)',
    poison: 'rgba(190,90,220,0.9)'
  };

  const TYPE_COLORS = {
    Normal:   '#a8a878', Fire:     '#f08030', Water:    '#6890f0',
    Electric: '#f8d030', Grass:    '#78c850', Ice:      '#98d8d8',
    Fighting: '#c03028', Poison:   '#a040a0', Ground:   '#e0c068',
    Flying:   '#a890f0', Psychic:  '#f85888', Bug:      '#a8b820',
    Rock:     '#b8a038', Ghost:    '#705898', Dragon:   '#7038f8',
    Dark:     '#705848', Steel:    '#b8b8d0', Fairy:    '#ee99ac'
  };

  // === TYPE CHART (Gen 6+) ===
  // CHART[attacker][defender] -> multiplier; default 1 when missing.
  const CHART = {
    Normal:   { Rock: 0.5, Ghost: 0,   Steel: 0.5 },
    Fire:     { Fire: 0.5, Water: 0.5, Grass: 2, Ice: 2, Bug: 2, Rock: 0.5, Dragon: 0.5, Steel: 2 },
    Water:    { Fire: 2,   Water: 0.5, Grass: 0.5, Ground: 2, Rock: 2, Dragon: 0.5 },
    Electric: { Water: 2,  Electric: 0.5, Grass: 0.5, Ground: 0, Flying: 2, Dragon: 0.5 },
    Ice:      { Fire: 0.5, Water: 0.5, Grass: 2, Ice: 0.5, Ground: 2, Flying: 2, Dragon: 2, Steel: 0.5 },
    Fighting: { Normal: 2, Ice: 2, Poison: 0.5, Flying: 0.5, Psychic: 0.5, Bug: 0.5, Rock: 2, Ghost: 0, Dark: 2, Steel: 2, Fairy: 0.5 },
    Poison:   { Grass: 2, Poison: 0.5, Ground: 0.5, Rock: 0.5, Ghost: 0.5, Steel: 0, Fairy: 2 },
    Flying:   { Electric: 0.5, Grass: 2, Fighting: 2, Bug: 2, Rock: 0.5, Steel: 0.5 },
    Psychic:  { Fighting: 2, Poison: 2, Psychic: 0.5, Dark: 0, Steel: 0.5 },
    Bug:      { Fire: 0.5, Grass: 2, Fighting: 0.5, Poison: 0.5, Flying: 0.5, Psychic: 2, Ghost: 0.5, Dark: 2, Steel: 0.5, Fairy: 0.5 },
    Ghost:    { Normal: 0, Psychic: 2, Ghost: 2, Dark: 0.5 },
    Dragon:   { Dragon: 2, Steel: 0.5, Fairy: 0 }
  };

  function typeMultiplier(attackType, defTypes) {
    if (!attackType || !defTypes || !defTypes.length) return 1;
    const row = CHART[attackType] || {};
    let m = 1;
    for (let i = 0; i < defTypes.length; i++) {
      const v = row[defTypes[i]];
      if (v !== undefined) m *= v;
    }
    return m;
  }

  // === TOWER DEFINITIONS ===
  // Range is in cells. Fire rate is shots/sec.
  const TOWERS = [
    { id: 'pidgey',   name: 'Pidgey',   slug: 'pidgey',   type: 'Normal',   cost: 50,
      dmg: 13, range: 2.5, rate: 2.0,  projColor: '#cfcfcf', special: null,
      desc: 'Cheap, fast attacks. Useless against Ghost enemies — type mismatch.' },
    { id: 'fearow',   name: 'Fearow',   slug: 'fearow',   type: 'Flying',   cost: 120,
      dmg: 40, range: 5.5, rate: 0.7,  projColor: '#d0c060', special: 'sniper',
      desc: 'Long range. Targets the farthest enemy along the path.' },
    { id: 'poliwag',  name: 'Poliwag',  slug: 'poliwag',  type: 'Water',    cost: 100,
      dmg: 15, range: 3.0, rate: 1.2,  projColor: '#6890f0', special: 'splash', splashRadius: 1.0,
      desc: 'Splash damage in a small radius around the impact.' },
    { id: 'slowpoke', name: 'Slowpoke', slug: 'slowpoke', type: 'Water',    cost: 80,
      dmg: 5,  range: 2.8, rate: 1.2,  projColor: '#f0a0c0', special: 'slow', slowFactor: 0.4, slowDur: 2.0,
      desc: 'Slows hit enemies by 40% for 2 seconds.' },
    { id: 'beedrill', name: 'Beedrill', slug: 'beedrill', type: 'Poison',   cost: 110,
      dmg: 6,  range: 2.8, rate: 1.6,  projColor: '#a040a0', special: 'poison', dotDmg: 8, dotDur: 4.0, dotStackCap: 3,
      desc: 'Applies poison damage-over-time. Stacks up to 3× on the same target.' },
    { id: 'jolteon',  name: 'Jolteon',  slug: 'jolteon',  type: 'Electric', cost: 200,
      dmg: 50, range: 3.2, rate: 1.0,  projColor: '#f8d030', special: 'chain', chainCount: 2, chainRange: 2.0, chainFalloff: 0.5,
      desc: 'Bolt chains to 2 nearby enemies at half damage each.' },
    { id: 'arcanine', name: 'Arcanine', slug: 'arcanine', type: 'Fire',     cost: 180,
      dmg: 35, range: 3.0, rate: 1.4,  projColor: '#f08030', special: 'burn', dotDmg: 5, dotDur: 3.0, dotStackCap: 3,
      desc: 'Ignites enemies for damage-over-time. Stacks up to 3×.' },
    { id: 'alakazam', name: 'Alakazam', slug: 'alakazam', type: 'Psychic',  cost: 250,
      dmg: 60, range: 4.5, rate: 0.8,  projColor: '#f85888', special: 'pierce',
      desc: 'Ignores type resistances — damage never falls below 1× multiplier.' },
    { id: 'lapras',   name: 'Lapras',   slug: 'lapras',   type: 'Ice',      cost: 220,
      dmg: 25, range: 3.0, rate: 1.0,  projColor: '#98d8d8', special: 'freeze', freezeDur: 1.0,
      desc: 'Damages and freezes the target solid for 1 second.' },
    { id: 'ho-oh',    name: 'Ho-Oh',    slug: 'ho-oh',    type: 'Fire',     cost: 500,
      dmg: 120, range: 6.5, rate: 0.8, projColor: '#ffa040', special: 'pierce',
      desc: 'Legendary. Long range, heavy damage, ignores all resistances.' }
  ];
  const TOWER_BY_ID = Object.fromEntries(TOWERS.map(t => [t.id, t]));

  // Upgrade scaling — applied multiplicatively per level above 1.
  const UPGRADE = {
    dmgMul: 1.4,
    rateMul: 1.15,
    rangeMul: 1.1,
    dotDmgMul: 1.35,
    splashRadiusAdd: 0.5,
    chainCountAddPerLevel: 1, // level 1: 2, level 2: 3, level 3: 4
    costFactor: 0.6           // each upgrade costs 60% of base, per spec
  };

  function towerStat(t, level, key) {
    // Compute upgraded stat. level is 1..3.
    const lvl = Math.max(1, level | 0);
    const exp = lvl - 1;
    const base = t.def[key];
    if (base === undefined) return undefined;
    if (key === 'dmg')   return Math.round(base * Math.pow(UPGRADE.dmgMul, exp));
    if (key === 'rate')  return +(base * Math.pow(UPGRADE.rateMul, exp)).toFixed(2);
    if (key === 'range') return +(base * Math.pow(UPGRADE.rangeMul, exp)).toFixed(2);
    if (key === 'dotDmg') return Math.round(base * Math.pow(UPGRADE.dotDmgMul, exp));
    if (key === 'splashRadius') return +(base + UPGRADE.splashRadiusAdd * exp).toFixed(2);
    if (key === 'chainCount')   return base + UPGRADE.chainCountAddPerLevel * exp;
    return base;
  }

  function upgradeCost(def) {
    return Math.round(def.cost * UPGRADE.costFactor);
  }

  function totalInvested(tower) {
    return tower.totalSpent;
  }

  // === ENEMY DEFINITIONS ===
  const ENEMIES = {
    caterpie:  { name: 'Caterpie',  slug: 'caterpie',  hp: 40,   speed: 'slow',   reward: 5,   types: ['Bug'],            flying: false },
    rattata:   { name: 'Rattata',   slug: 'rattata',   hp: 70,   speed: 'normal', reward: 8,   types: ['Normal'],         flying: false },
    zubat:     { name: 'Zubat',     slug: 'zubat',     hp: 110,  speed: 'normal', reward: 10,  types: ['Poison','Flying'], flying: true },
    machop:    { name: 'Machop',    slug: 'machop',    hp: 170,  speed: 'normal', reward: 15,  types: ['Fighting'],       flying: false },
    haunter:   { name: 'Haunter',   slug: 'haunter',   hp: 260,  speed: 'fast',   reward: 20,  types: ['Ghost','Poison'], flying: false },
    gyarados:  { name: 'Gyarados',  slug: 'gyarados',  hp: 400,  speed: 'normal', reward: 30,  types: ['Water'],          flying: false },
    dragonite: { name: 'Dragonite', slug: 'dragonite', hp: 600,  speed: 'fast',   reward: 40,  types: ['Dragon','Flying'], flying: true },
    mewtwo:    { name: 'Mewtwo',    slug: 'mewtwo',    hp: 2000, speed: 'slow',   reward: 150, types: ['Psychic'],        flying: false, boss: true }
  };

  // === WAVE DEFINITIONS ===
  // Each wave is a list of [enemyKey, count] groups, with optional hpMul / speedMul.
  function buildWaves() {
    const w = [];
    w.push({ groups: [['caterpie', 8]] });
    w.push({ groups: [['caterpie', 10], ['rattata', 4]] });
    w.push({ groups: [['rattata', 8], ['zubat', 6]] });
    w.push({ groups: [['rattata', 12], ['zubat', 4], ['machop', 2]] });
    w.push({ groups: [['zubat', 8], ['machop', 4], ['mewtwo', 1]], boss: true });
    w.push({ groups: [['zubat', 10], ['machop', 6]] });
    w.push({ groups: [['machop', 8], ['haunter', 6]] });
    w.push({ groups: [['haunter', 12], ['gyarados', 4]] });
    w.push({ groups: [['gyarados', 6], ['haunter', 8], ['dragonite', 4]] });
    w.push({ groups: [['dragonite', 4], ['gyarados', 2], ['mewtwo', 1]], boss: true, hpMul: 1.5 });
    // Waves 11–19: +15% HP per wave vs wave 10, mix higher tiers.
    for (let i = 11; i <= 19; i++) {
      const hp = 1.5 * Math.pow(1.15, i - 10);
      const groups = [
        ['haunter', 6 + (i - 11)],
        ['gyarados', 4 + Math.floor((i - 10) / 2)],
        ['dragonite', 3 + Math.floor((i - 10) / 2)]
      ];
      if (i % 5 === 0) groups.push(['mewtwo', 1]);
      w.push({ groups, boss: (i % 5 === 0), hpMul: hp });
    }
    w.push({
      groups: [['dragonite', 6], ['gyarados', 3], ['mewtwo', 2]],
      boss: true, final: true, hpMul: 3.0, speedMul: 1.2
    });
    return w;
  }
  const WAVES = buildWaves();

  // === PATH DATA ===
  // Waypoints in cell-centre coords (gx + 0.5, gy + 0.5).
  const WAYPOINTS_CELLS = [
    [0, 6], [5, 6], [5, 2], [12, 2], [12, 9], [16, 9], [16, 5], [19, 5]
  ];
  // Convert to pixel coordinates (centre of cell).
  const WAYPOINTS = WAYPOINTS_CELLS.map(([gx, gy]) => [gx * CELL + CELL / 2, gy * CELL + CELL / 2]);

  // Pre-compute set of path cells (used to block tower placement).
  const PATH_CELLS = (function () {
    const s = new Set();
    for (let i = 0; i < WAYPOINTS_CELLS.length - 1; i++) {
      const [x0, y0] = WAYPOINTS_CELLS[i];
      const [x1, y1] = WAYPOINTS_CELLS[i + 1];
      const dx = Math.sign(x1 - x0), dy = Math.sign(y1 - y0);
      let cx = x0, cy = y0;
      s.add(`${cx},${cy}`);
      while (cx !== x1 || cy !== y1) { cx += dx; cy += dy; s.add(`${cx},${cy}`); }
    }
    return s;
  })();

  // Segment lengths and total path length in cells (for speed bookkeeping).
  const SEGMENT_LEN_CELLS = (function () {
    const out = [];
    for (let i = 0; i < WAYPOINTS_CELLS.length - 1; i++) {
      const [x0, y0] = WAYPOINTS_CELLS[i];
      const [x1, y1] = WAYPOINTS_CELLS[i + 1];
      out.push(Math.abs(x1 - x0) + Math.abs(y1 - y0));
    }
    return out;
  })();

  // Map a path parameter `t` (cells traveled) -> {x, y} in pixels.
  function pathPosition(tCells) {
    let remaining = tCells;
    for (let i = 0; i < SEGMENT_LEN_CELLS.length; i++) {
      const segLen = SEGMENT_LEN_CELLS[i];
      if (remaining <= segLen) {
        const [ax, ay] = WAYPOINTS[i];
        const [bx, by] = WAYPOINTS[i + 1];
        const f = segLen === 0 ? 0 : remaining / segLen;
        return { x: ax + (bx - ax) * f, y: ay + (by - ay) * f, done: false };
      }
      remaining -= segLen;
    }
    // Past the end of the path.
    const last = WAYPOINTS[WAYPOINTS.length - 1];
    return { x: last[0], y: last[1], done: true };
  }

  // === GAME STATE ===
  const state = {
    coins: 150,
    lives: 20,
    wave: 1,
    waveActive: false,
    awaitingWave: true,
    gameOver: false,
    victory: false,
    enemies: [],
    towers: [],
    projectiles: [],
    floats: [],
    speedMul: 1,
    enemiesKilled: 0,
    coinsEarned: 0,
    selectedShopId: null,    // tower-def id staged for placement
    selectedPlacedIdx: -1,   // index into state.towers
    spawnQueue: [],          // list of {enemyKey, hpMul, speedMul, delay}
    spawnTimer: 0,
    waveBoss: false,
    waveFinal: false,
    waveStartTime: 0,
    bestScore: 0,
    bestWave: 0,
    hoverCell: null
  };

  // === SPRITE LOADING ===
  const spriteCache = new Map();   // slug -> { img, ok }
  let spriteBase = '/images/pokedex/';

  function getSprite(slug) {
    if (!slug) return null;
    let entry = spriteCache.get(slug);
    if (entry) return entry;
    const img = new Image();
    entry = { img, ok: false, failed: false };
    img.onload = () => { entry.ok = true; };
    img.onerror = () => { entry.failed = true; };
    img.src = spriteBase + slug + '.png';
    spriteCache.set(slug, entry);
    return entry;
  }

  function drawSpriteOrFallback(ctx, slug, name, type, cx, cy, size) {
    const entry = getSprite(slug);
    if (entry && entry.ok) {
      ctx.drawImage(entry.img, cx - size / 2, cy - size / 2, size, size);
      return;
    }
    // Fallback: type-colored circle with 3-letter abbreviation.
    const color = TYPE_COLORS[type] || '#888';
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(cx, cy, size / 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#fff';
    ctx.font = `${Math.round(size * 0.35)}px sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText((name || '???').slice(0, 3).toUpperCase(), cx, cy);
  }

  // === RENDERING ===
  let canvas, ctx;

  function drawBackground() {
    // Grass tiles.
    for (let y = 0; y < ROWS; y++) {
      for (let x = 0; x < COLS; x++) {
        ctx.fillStyle = ((x + y) & 1) ? COLORS.grass : COLORS.grassAlt;
        ctx.fillRect(x * CELL, y * CELL, CELL, CELL);
      }
    }
    // Path tiles.
    PATH_CELLS.forEach(key => {
      const [gx, gy] = key.split(',').map(Number);
      ctx.fillStyle = COLORS.path;
      ctx.fillRect(gx * CELL + 1, gy * CELL + 1, CELL - 2, CELL - 2);
    });

    // Entrance + exit markers.
    const start = WAYPOINTS[0];
    const end = WAYPOINTS[WAYPOINTS.length - 1];
    // Poké Ball start
    ctx.beginPath(); ctx.arc(start[0], start[1], 12, 0, Math.PI * 2);
    ctx.fillStyle = '#e0535c'; ctx.fill();
    ctx.beginPath(); ctx.arc(start[0], start[1], 12, 0, Math.PI, false);
    ctx.fillStyle = '#f4f4f4'; ctx.fill();
    ctx.strokeStyle = '#1a1f33'; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.arc(start[0], start[1], 12, 0, Math.PI * 2); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(start[0] - 12, start[1]); ctx.lineTo(start[0] + 12, start[1]); ctx.stroke();
    ctx.beginPath(); ctx.arc(start[0], start[1], 4, 0, Math.PI * 2);
    ctx.fillStyle = '#fff'; ctx.fill();
    ctx.strokeStyle = '#1a1f33'; ctx.stroke();
    // Base goal marker
    ctx.fillStyle = COLORS.exit;
    ctx.fillRect(end[0] - 14, end[1] - 14, 28, 28);
    ctx.strokeStyle = '#1a1f33'; ctx.lineWidth = 2;
    ctx.strokeRect(end[0] - 14, end[1] - 14, 28, 28);
    ctx.fillStyle = '#fff';
    ctx.font = 'bold 14px sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('PC', end[0], end[1]);
  }

  function drawTowers() {
    for (let i = 0; i < state.towers.length; i++) {
      const t = state.towers[i];
      const cx = t.gx * CELL + CELL / 2;
      const cy = t.gy * CELL + CELL / 2;
      drawSpriteOrFallback(ctx, t.def.slug, t.def.name, t.def.type, cx, cy, 34);
      // Level pips.
      ctx.fillStyle = '#fff';
      for (let p = 0; p < t.level; p++) {
        ctx.beginPath();
        ctx.arc(t.gx * CELL + 6 + p * 6, t.gy * CELL + CELL - 6, 2.5, 0, Math.PI * 2);
        ctx.fill();
      }
    }
    // Range circle for selected/hovered tower.
    if (state.selectedPlacedIdx >= 0) {
      const t = state.towers[state.selectedPlacedIdx];
      if (t) drawRange(t.gx * CELL + CELL / 2, t.gy * CELL + CELL / 2, towerStat(t, t.level, 'range') * CELL);
    } else if (state.selectedShopId && state.hoverCell) {
      const def = TOWER_BY_ID[state.selectedShopId];
      drawRange(state.hoverCell.gx * CELL + CELL / 2, state.hoverCell.gy * CELL + CELL / 2, def.range * CELL);
      // Placement preview tint.
      const blocked = !canPlaceAt(state.hoverCell.gx, state.hoverCell.gy) || state.coins < def.cost;
      ctx.fillStyle = blocked ? 'rgba(224,83,92,0.25)' : 'rgba(62,176,69,0.25)';
      ctx.fillRect(state.hoverCell.gx * CELL, state.hoverCell.gy * CELL, CELL, CELL);
    }
  }

  function drawRange(cx, cy, r) {
    ctx.fillStyle = COLORS.rangeFill;
    ctx.strokeStyle = COLORS.rangeStroke;
    ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  }

  function drawEnemies() {
    for (let i = 0; i < state.enemies.length; i++) {
      const e = state.enemies[i];
      // Status ring (drawn first so sprite covers centre).
      const ring = e.freezeT > 0 ? STATUS_COLORS.freeze
        : e.burnStacks ? STATUS_COLORS.burn
        : e.poisonStacks ? STATUS_COLORS.poison
        : e.slowT > 0 ? STATUS_COLORS.slow
        : null;
      if (ring) {
        ctx.strokeStyle = ring; ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.arc(e.x, e.y, 18, 0, Math.PI * 2); ctx.stroke();
      }
      const size = e.def.boss ? 40 : 30;
      drawSpriteOrFallback(ctx, e.def.slug, e.def.name, e.def.types[0], e.x, e.y, size);

      // Flying wing icon overlay.
      if (e.def.flying) {
        ctx.fillStyle = 'rgba(255,255,255,0.85)';
        ctx.font = '12px sans-serif'; ctx.textAlign = 'center';
        ctx.fillText('✈', e.x + size / 2 - 2, e.y - size / 2 + 8);
      }

      // HP bar above sprite.
      const w = size, h = 4;
      const px = e.x - w / 2, py = e.y - size / 2 - 7;
      ctx.fillStyle = COLORS.hpBack;
      ctx.fillRect(px - 1, py - 1, w + 2, h + 2);
      ctx.fillStyle = e.def.boss ? COLORS.hpBoss : COLORS.hpFront;
      ctx.fillRect(px, py, w * Math.max(0, e.hp / e.maxHp), h);
    }
  }

  function drawProjectiles() {
    for (let i = 0; i < state.projectiles.length; i++) {
      const p = state.projectiles[i];
      ctx.fillStyle = p.color;
      ctx.beginPath(); ctx.arc(p.x, p.y, 4, 0, Math.PI * 2); ctx.fill();
    }
  }

  function drawFloats() {
    for (let i = 0; i < state.floats.length; i++) {
      const f = state.floats[i];
      const a = Math.max(0, 1 - f.t / f.life);
      ctx.globalAlpha = a;
      ctx.fillStyle = f.color || '#fff';
      ctx.font = 'bold 13px sans-serif'; ctx.textAlign = 'center';
      ctx.fillText(f.text, f.x, f.y - 24 * (f.t / f.life));
      ctx.globalAlpha = 1;
    }
  }

  function render() {
    ctx.clearRect(0, 0, WIDTH, HEIGHT);
    drawBackground();
    drawTowers();
    drawEnemies();
    drawProjectiles();
    drawFloats();
  }

  // === COMBAT / DAMAGE ===
  function applyDamage(enemy, rawDmg, attackType, options) {
    options = options || {};
    let mul = typeMultiplier(attackType, enemy.def.types);
    if (options.pierce && mul < 1) mul = 1;   // Alakazam / Ho-Oh special
    const dmg = Math.max(1, Math.round(rawDmg * mul));
    enemy.hp -= dmg;
    spawnFloat(enemy.x, enemy.y, String(dmg), mul >= 2 ? '#ffdf60' : (mul === 0 ? '#888' : '#fff'));
    if (enemy.hp <= 0 && !enemy.dead) {
      enemy.dead = true;
      state.coins += enemy.def.reward;
      state.coinsEarned += enemy.def.reward;
      state.enemiesKilled++;
    }
  }

  function spawnFloat(x, y, text, color) {
    state.floats.push({ x, y, text, color: color || '#fff', t: 0, life: 0.8 });
  }

  function applyStatus(enemy, kind, srcTower) {
    if (kind === 'slow') {
      const dur = srcTower.def.slowDur;
      const factor = srcTower.def.slowFactor;
      // Use the strongest active slow.
      if (!enemy.slowT || factor > enemy.slowFactor) enemy.slowFactor = factor;
      enemy.slowT = Math.max(enemy.slowT || 0, dur);
    } else if (kind === 'freeze') {
      enemy.freezeT = Math.max(enemy.freezeT || 0, srcTower.def.freezeDur);
    } else if (kind === 'burn' || kind === 'poison') {
      const stackKey = kind + 'Stacks';
      const dmgKey   = kind + 'Dmg';
      const durKey   = kind + 'T';
      const stacks = (enemy[stackKey] || 0) + 1;
      const cap = srcTower.def.dotStackCap || 3;
      enemy[stackKey] = Math.min(stacks, cap);
      enemy[dmgKey] = towerStat(srcTower, srcTower.level, 'dotDmg');
      enemy[durKey] = srcTower.def.dotDur; // refresh
      enemy[kind + 'TickAcc'] = enemy[kind + 'TickAcc'] || 0;
      enemy[kind + 'Type'] = (kind === 'burn') ? 'Fire' : 'Poison';
    }
  }

  function applyHit(tower, projectile, primary) {
    const def = tower.def;
    const baseDmg = towerStat(tower, tower.level, 'dmg');
    const pierce = def.special === 'pierce';
    applyDamage(primary, baseDmg, def.type, { pierce });

    if (def.special === 'splash') {
      const r = towerStat(tower, tower.level, 'splashRadius') * CELL;
      for (let i = 0; i < state.enemies.length; i++) {
        const e = state.enemies[i];
        if (e === primary || e.dead) continue;
        const dx = e.x - primary.x, dy = e.y - primary.y;
        if (dx * dx + dy * dy <= r * r) applyDamage(e, baseDmg, def.type, { pierce });
      }
    } else if (def.special === 'chain') {
      const r = def.chainRange * CELL;
      const count = towerStat(tower, tower.level, 'chainCount');
      let prev = primary;
      const hit = new Set([primary]);
      let dmg = baseDmg * def.chainFalloff;
      for (let c = 0; c < count; c++) {
        let best = null, bestD = Infinity;
        for (let i = 0; i < state.enemies.length; i++) {
          const e = state.enemies[i];
          if (hit.has(e) || e.dead) continue;
          const dx = e.x - prev.x, dy = e.y - prev.y;
          const d2 = dx * dx + dy * dy;
          if (d2 <= r * r && d2 < bestD) { best = e; bestD = d2; }
        }
        if (!best) break;
        applyDamage(best, dmg, def.type, { pierce });
        hit.add(best);
        prev = best;
        dmg *= def.chainFalloff;
      }
    } else if (def.special === 'slow' || def.special === 'freeze' ||
               def.special === 'burn' || def.special === 'poison') {
      applyStatus(primary, def.special, tower);
    }
  }

  // === TARGETING ===
  function pickTarget(tower) {
    const range = towerStat(tower, tower.level, 'range') * CELL;
    const cx = tower.gx * CELL + CELL / 2;
    const cy = tower.gy * CELL + CELL / 2;
    let best = null;
    let bestKey = -Infinity;
    for (let i = 0; i < state.enemies.length; i++) {
      const e = state.enemies[i];
      if (e.dead) continue;
      const dx = e.x - cx, dy = e.y - cy;
      if (dx * dx + dy * dy > range * range) continue;
      let key;
      if (tower.def.special === 'sniper') {
        key = e.pathT; // farthest along
      } else {
        key = e.pathT; // default: farthest along (closer to base) — common TD heuristic
      }
      if (key > bestKey) { bestKey = key; best = e; }
    }
    return best;
  }

  // === TOWER PLACEMENT ===
  function canPlaceAt(gx, gy) {
    if (gx < 0 || gy < 0 || gx >= COLS || gy >= ROWS) return false;
    if (PATH_CELLS.has(`${gx},${gy}`)) return false;
    for (let i = 0; i < state.towers.length; i++) {
      if (state.towers[i].gx === gx && state.towers[i].gy === gy) return false;
    }
    return true;
  }

  function placeTower(defId, gx, gy) {
    const def = TOWER_BY_ID[defId];
    if (!def) return false;
    if (!canPlaceAt(gx, gy)) return false;
    if (state.coins < def.cost) return false;
    state.coins -= def.cost;
    state.towers.push({
      def, gx, gy,
      level: 1,
      totalSpent: def.cost,
      cooldown: 0
    });
    state.selectedShopId = null;
    state.selectedPlacedIdx = state.towers.length - 1;
    refreshUI();
    return true;
  }

  function upgradeSelected() {
    const t = state.towers[state.selectedPlacedIdx];
    if (!t || t.level >= 3) return;
    const cost = upgradeCost(t.def);
    if (state.coins < cost) return;
    state.coins -= cost;
    t.totalSpent += cost;
    t.level++;
    refreshUI();
  }

  function sellSelected() {
    const idx = state.selectedPlacedIdx;
    const t = state.towers[idx];
    if (!t) return;
    const refund = Math.round(t.totalSpent * 0.5);
    state.coins += refund;
    state.towers.splice(idx, 1);
    state.selectedPlacedIdx = -1;
    refreshUI();
  }

  // === ENEMY UPDATE ===
  function updateEnemies(dt) {
    for (let i = state.enemies.length - 1; i >= 0; i--) {
      const e = state.enemies[i];
      if (e.dead) {
        state.enemies.splice(i, 1);
        continue;
      }
      // DoTs.
      if (e.burnT > 0) {
        e.burnTickAcc += dt;
        while (e.burnTickAcc >= 1) {
          e.burnTickAcc -= 1;
          applyDamage(e, e.burnDmg * e.burnStacks, 'Fire', { pierce: false });
        }
        e.burnT -= dt;
        if (e.burnT <= 0) { e.burnStacks = 0; e.burnT = 0; }
      }
      if (e.poisonT > 0) {
        e.poisonTickAcc += dt;
        while (e.poisonTickAcc >= 1) {
          e.poisonTickAcc -= 1;
          applyDamage(e, e.poisonDmg * e.poisonStacks, 'Poison', { pierce: false });
        }
        e.poisonT -= dt;
        if (e.poisonT <= 0) { e.poisonStacks = 0; e.poisonT = 0; }
      }
      if (e.dead) { state.enemies.splice(i, 1); continue; }
      // Statuses.
      if (e.freezeT > 0) {
        e.freezeT -= dt;
        // Movement halted; skip move step.
      } else {
        let speed = SPEEDS[e.def.speed] * (e.speedMul || 1);
        if (e.slowT > 0) {
          speed *= (1 - (e.slowFactor || 0));
          e.slowT -= dt;
        }
        e.pathT += speed * dt;
        const p = pathPosition(e.pathT);
        e.x = p.x; e.y = p.y;
        if (p.done) {
          state.lives--;
          state.enemies.splice(i, 1);
          refreshUI();
          if (state.lives <= 0) gameOver();
        }
      }
    }
  }

  // === TOWER UPDATE ===
  function updateTowers(dt) {
    for (let i = 0; i < state.towers.length; i++) {
      const t = state.towers[i];
      t.cooldown -= dt;
      if (t.cooldown > 0) continue;
      const target = pickTarget(t);
      if (!target) continue;
      t.cooldown = 1 / towerStat(t, t.level, 'rate');
      const cx = t.gx * CELL + CELL / 2;
      const cy = t.gy * CELL + CELL / 2;
      state.projectiles.push({
        x: cx, y: cy, target, towerIdx: i,
        speed: 360, // px/sec
        color: t.def.projColor
      });
    }
  }

  // === PROJECTILE UPDATE ===
  function updateProjectiles(dt) {
    for (let i = state.projectiles.length - 1; i >= 0; i--) {
      const p = state.projectiles[i];
      const tgt = p.target;
      if (!tgt || tgt.dead) { state.projectiles.splice(i, 1); continue; }
      const dx = tgt.x - p.x, dy = tgt.y - p.y;
      const d = Math.hypot(dx, dy);
      const step = p.speed * dt;
      if (d <= step) {
        const tower = state.towers[p.towerIdx];
        if (tower) applyHit(tower, p, tgt);
        state.projectiles.splice(i, 1);
      } else {
        p.x += (dx / d) * step;
        p.y += (dy / d) * step;
      }
    }
  }

  // === FLOATS / WAVE / SPAWNING ===
  function updateFloats(dt) {
    for (let i = state.floats.length - 1; i >= 0; i--) {
      state.floats[i].t += dt;
      if (state.floats[i].t >= state.floats[i].life) state.floats.splice(i, 1);
    }
  }

  function startWave(early) {
    if (state.gameOver || state.victory) return;
    if (state.waveActive) return;
    if (state.wave > WAVES.length) return;
    const def = WAVES[state.wave - 1];
    state.spawnQueue = [];
    const spacing = 0.55;
    let t = 0;
    for (let g = 0; g < def.groups.length; g++) {
      const [key, count] = def.groups[g];
      for (let n = 0; n < count; n++) {
        state.spawnQueue.push({
          key,
          hpMul: def.hpMul || 1,
          speedMul: def.speedMul || 1,
          delay: t
        });
        t += spacing;
      }
    }
    state.spawnTimer = 0;
    state.waveActive = true;
    state.awaitingWave = false;
    state.waveBoss = !!def.boss;
    state.waveFinal = !!def.final;
    if (early) { state.coins += 10; state.coinsEarned += 10; }
    if (def.boss) showBanner(def.final ? 'FINAL WAVE' : 'BOSS WAVE', def.final);
    refreshUI();
  }

  function updateSpawning(dt) {
    if (!state.waveActive) return;
    state.spawnTimer += dt;
    while (state.spawnQueue.length && state.spawnQueue[0].delay <= state.spawnTimer) {
      const s = state.spawnQueue.shift();
      const def = ENEMIES[s.key];
      const p = pathPosition(0);
      state.enemies.push({
        def,
        hp: def.hp * s.hpMul,
        maxHp: def.hp * s.hpMul,
        speedMul: s.speedMul,
        x: p.x, y: p.y,
        pathT: 0,
        slowT: 0, slowFactor: 0,
        freezeT: 0,
        burnT: 0, burnStacks: 0, burnDmg: 0, burnTickAcc: 0,
        poisonT: 0, poisonStacks: 0, poisonDmg: 0, poisonTickAcc: 0,
        dead: false
      });
    }
    // Wave complete?
    if (!state.spawnQueue.length && !state.enemies.length) {
      state.waveActive = false;
      state.awaitingWave = true;
      state.coins += 20;
      state.coinsEarned += 20;
      if (state.wave >= WAVES.length) { victory(); return; }
      state.wave++;
      refreshUI();
    }
  }

  // === GAME LOOP ===
  let lastFrameT = 0;
  function frame(nowMs) {
    if (!lastFrameT) lastFrameT = nowMs;
    let dt = (nowMs - lastFrameT) / 1000;
    lastFrameT = nowMs;
    if (dt > DT_CAP) dt = DT_CAP;
    dt *= state.speedMul;

    if (!state.gameOver && !state.victory) {
      updateSpawning(dt);
      updateEnemies(dt);
      updateTowers(dt);
      updateProjectiles(dt);
    }
    updateFloats(dt);
    render();
    updateHUD();
    requestAnimationFrame(frame);
  }

  // === GAME OVER / VICTORY ===
  function computeScore() {
    return Math.round(state.wave * 100 + state.coinsEarned * 0.5);
  }
  function gameOver() {
    if (state.gameOver) return;
    state.gameOver = true;
    state.waveActive = false;
    saveBest();
    showOverlay({
      title: 'Defeated!',
      text: 'The wild Pokémon broke through!',
      stats: [
        ['Waves reached', String(state.wave)],
        ['Enemies defeated', String(state.enemiesKilled)],
        ['Coins earned', String(state.coinsEarned)],
        ['Score', String(computeScore())]
      ],
      primaryLabel: 'Try Again'
    });
  }
  function victory() {
    if (state.victory) return;
    state.victory = true;
    state.waveActive = false;
    saveBest();
    showOverlay({
      title: 'You defended Pokéfind! 🏆',
      text: 'Wave 20 cleared. The wild Pokémon retreat.',
      stats: [
        ['Waves cleared', String(WAVES.length)],
        ['Enemies defeated', String(state.enemiesKilled)],
        ['Coins earned', String(state.coinsEarned)],
        ['Score', String(computeScore())]
      ],
      primaryLabel: 'Play Again'
    });
  }

  // === PERSISTENCE ===
  const STORAGE_KEY = 'pokedefense_best_v1';
  function loadBest() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      const v = JSON.parse(raw);
      state.bestScore = v.score || 0;
      state.bestWave = v.wave || 0;
    } catch (_) { /* ignore */ }
  }
  function saveBest() {
    const score = computeScore();
    const wave = state.wave - (state.victory ? 0 : (state.awaitingWave ? 1 : 0));
    if (score > state.bestScore) {
      state.bestScore = score;
      state.bestWave = Math.max(state.bestWave, wave);
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({ score: state.bestScore, wave: state.bestWave }));
      } catch (_) { /* ignore */ }
    }
  }

  // === DOM / UI ===
  const dom = {};

  function $(id) { return document.getElementById(id); }

  function buildShopList() {
    dom.shopList.innerHTML = '';
    for (let i = 0; i < TOWERS.length; i++) {
      const def = TOWERS[i];
      const card = document.createElement('button');
      card.type = 'button';
      card.className = 'pd-tower-card';
      card.dataset.towerId = def.id;
      const img = new Image();
      img.alt = '';
      img.src = spriteBase + def.slug + '.png';
      img.onerror = function () {
        img.replaceWith(makeFallback(def.name, def.type));
      };
      card.appendChild(img);
      const tag = document.createElement('span');
      tag.className = 'pd-tower-type';
      tag.style.background = TYPE_COLORS[def.type] || '#444';
      tag.textContent = def.type;
      card.appendChild(tag);
      const name = document.createElement('div');
      name.className = 'pd-tower-name';
      name.textContent = def.name;
      card.appendChild(name);
      const cost = document.createElement('div');
      cost.className = 'pd-tower-cost';
      cost.textContent = '🪙 ' + def.cost;
      card.appendChild(cost);
      card.title = def.desc;
      card.addEventListener('click', () => onShopCardClick(def.id));
      dom.shopList.appendChild(card);
    }
  }

  function makeFallback(name, type) {
    const div = document.createElement('div');
    div.className = 'pd-fallback';
    div.style.background = TYPE_COLORS[type] || '#888';
    div.textContent = (name || '???').slice(0, 3).toUpperCase();
    return div;
  }

  function onShopCardClick(id) {
    if (state.gameOver || state.victory) return;
    state.selectedShopId = (state.selectedShopId === id) ? null : id;
    state.selectedPlacedIdx = -1;
    refreshUI();
  }

  // Cheap per-frame HUD update: text fields, button states, shop affordability,
  // and the upgrade button's affordability if a tower is selected. Does NOT
  // rebuild the selected panel's inner HTML.
  function updateHUD() {
    dom.lives.textContent = state.lives;
    dom.coins.textContent = state.coins;
    dom.bestWave.textContent = state.bestWave;
    dom.waveNum.textContent = Math.min(state.wave, WAVES.length);

    dom.sendWave.disabled = state.waveActive || state.gameOver || state.victory;
    dom.sendWave.textContent = state.waveActive
      ? 'Wave in progress…'
      : (state.wave === 1 && state.awaitingWave ? 'Send Wave ▶' : 'Send Wave ▶ (+10)');

    if (state.waveActive) {
      const remaining = state.spawnQueue.length + state.enemies.length;
      dom.waveRemaining.textContent = `· ${remaining} enemies left`;
    } else {
      dom.waveRemaining.textContent = '';
    }

    const cards = dom.shopList.querySelectorAll('.pd-tower-card');
    cards.forEach(c => {
      const def = TOWER_BY_ID[c.dataset.towerId];
      c.classList.toggle('is-selected', state.selectedShopId === def.id);
      c.classList.toggle('is-unaffordable', state.coins < def.cost);
    });

    // Live-update the upgrade button affordability without rebuilding the panel.
    const sel = state.towers[state.selectedPlacedIdx];
    if (sel && !dom.selected.hidden) {
      if (sel.level >= 3) {
        dom.upgrade.disabled = true;
        dom.upgrade.textContent = 'Maxed';
      } else {
        const cost = upgradeCost(sel.def);
        dom.upgrade.disabled = state.coins < cost;
        dom.upgrade.textContent = `Upgrade (🪙 ${cost})`;
      }
    }
  }

  function refreshUI() {
    updateHUD();
    if (state.selectedPlacedIdx >= 0 && state.towers[state.selectedPlacedIdx]) {
      dom.selected.hidden = false;
      renderSelectedTowerPanel(state.towers[state.selectedPlacedIdx]);
    } else {
      dom.selected.hidden = true;
    }
  }

  function renderSelectedTowerPanel(t) {
    const def = t.def;
    const lvl = t.level;
    const next = lvl < 3 ? lvl + 1 : null;
    const rows = [];
    rows.push(['Damage', towerStat(t, lvl, 'dmg'), next ? towerStat(t, next, 'dmg') : null]);
    rows.push(['Range', towerStat(t, lvl, 'range').toFixed(1), next ? towerStat(t, next, 'range').toFixed(1) : null]);
    rows.push(['Fire rate', towerStat(t, lvl, 'rate').toFixed(2) + '/s', next ? towerStat(t, next, 'rate').toFixed(2) + '/s' : null]);
    if (def.dotDmg !== undefined) {
      rows.push(['DoT/sec', towerStat(t, lvl, 'dotDmg'), next ? towerStat(t, next, 'dotDmg') : null]);
    }
    if (def.splashRadius !== undefined) {
      rows.push(['Splash', towerStat(t, lvl, 'splashRadius').toFixed(1), next ? towerStat(t, next, 'splashRadius').toFixed(1) : null]);
    }
    if (def.chainCount !== undefined) {
      rows.push(['Chain', towerStat(t, lvl, 'chainCount'), next ? towerStat(t, next, 'chainCount') : null]);
    }

    const cost = next ? upgradeCost(def) : null;
    const refund = Math.round(t.totalSpent * 0.5);

    const html = [
      '<div class="pd-tower-head">',
        `<div data-fallback-slot></div>`,
        `<div><strong>${def.name}</strong><br><small style="color:var(--pd-text-dim)">Lv ${lvl} · ${def.type}</small></div>`,
      '</div>',
      '<table>',
      ...rows.map(([k, c, n]) =>
        `<tr><td class="k">${k}</td><td class="cur">${c}</td><td class="next">${n !== null && n !== undefined ? '→ ' + n : ''}</td></tr>`),
      '</table>',
      def.desc ? `<div class="pd-special">${def.desc}</div>` : ''
    ].join('');
    dom.selectedBody.innerHTML = html;
    // Inject sprite or fallback in head slot.
    const slot = dom.selectedBody.querySelector('[data-fallback-slot]');
    const entry = getSprite(def.slug);
    if (entry && entry.ok) {
      const img = new Image();
      img.src = entry.img.src;
      img.alt = '';
      slot.replaceWith(img);
    } else {
      slot.replaceWith(makeFallback(def.name, def.type));
    }

    dom.upgrade.disabled = !next || state.coins < (cost || 0);
    dom.upgrade.textContent = next ? `Upgrade (🪙 ${cost})` : 'Maxed';
    dom.sell.textContent = `Sell (🪙 ${refund})`;
  }

  function showOverlay({ title, text, stats, primaryLabel }) {
    dom.overlay.hidden = false;
    dom.overlayTitle.textContent = title;
    dom.overlayText.textContent = text;
    dom.overlayStats.innerHTML = stats.map(([k, v]) => `<dt>${k}</dt><dd>${v}</dd>`).join('');
    dom.overlayPrimary.textContent = primaryLabel;
  }
  function hideOverlay() { dom.overlay.hidden = true; }

  function showBanner(text, isFinal) {
    dom.waveBanner.textContent = text;
    dom.waveBanner.classList.toggle('is-final', !!isFinal);
    dom.waveBanner.hidden = false;
    clearTimeout(showBanner._t);
    showBanner._t = setTimeout(() => { dom.waveBanner.hidden = true; }, 2200);
  }

  // === INPUT HANDLING ===
  function canvasToCell(evt) {
    const rect = canvas.getBoundingClientRect();
    const cx = ('touches' in evt && evt.touches[0])
      ? evt.touches[0].clientX
      : (evt.clientX !== undefined ? evt.clientX : (evt.changedTouches && evt.changedTouches[0].clientX));
    const cy = ('touches' in evt && evt.touches[0])
      ? evt.touches[0].clientY
      : (evt.clientY !== undefined ? evt.clientY : (evt.changedTouches && evt.changedTouches[0].clientY));
    const x = (cx - rect.left) * (WIDTH / rect.width);
    const y = (cy - rect.top) * (HEIGHT / rect.height);
    return { gx: Math.floor(x / CELL), gy: Math.floor(y / CELL) };
  }

  function onCanvasClick(evt) {
    if (state.gameOver || state.victory) return;
    const { gx, gy } = canvasToCell(evt);
    if (gx < 0 || gy < 0 || gx >= COLS || gy >= ROWS) return;
    // Try placing.
    if (state.selectedShopId) {
      if (placeTower(state.selectedShopId, gx, gy)) return;
    }
    // Click on existing tower? Select it.
    for (let i = 0; i < state.towers.length; i++) {
      if (state.towers[i].gx === gx && state.towers[i].gy === gy) {
        state.selectedPlacedIdx = i;
        state.selectedShopId = null;
        refreshUI();
        return;
      }
    }
    // Otherwise deselect.
    state.selectedPlacedIdx = -1;
    refreshUI();
  }

  function onCanvasMove(evt) {
    const { gx, gy } = canvasToCell(evt);
    if (gx < 0 || gy < 0 || gx >= COLS || gy >= ROWS) {
      state.hoverCell = null; return;
    }
    state.hoverCell = { gx, gy };
  }

  function onSendWave() {
    if (!state.waveActive) {
      // "Early" if there are no enemies pending and the player hasn't yet started this wave.
      const early = state.awaitingWave && state.wave > 1;
      startWave(early);
    }
  }

  function setSpeed(mul) {
    state.speedMul = mul;
    document.querySelectorAll('.pd-speed-btn').forEach(b => {
      b.classList.toggle('is-active', Number(b.dataset.speed) === mul);
    });
  }

  function resetGame() {
    state.coins = 150;
    state.lives = 20;
    state.wave = 1;
    state.waveActive = false;
    state.awaitingWave = true;
    state.gameOver = false;
    state.victory = false;
    state.enemies = [];
    state.towers = [];
    state.projectiles = [];
    state.floats = [];
    state.enemiesKilled = 0;
    state.coinsEarned = 0;
    state.selectedShopId = null;
    state.selectedPlacedIdx = -1;
    state.spawnQueue = [];
    state.waveBoss = false;
    state.waveFinal = false;
    hideOverlay();
    refreshUI();
  }

  // === INIT ===
  function init() {
    const app = document.querySelector('.pokedefense-app');
    if (!app) return;
    spriteBase = app.dataset.spriteBase || spriteBase;

    canvas = $('pd-canvas');
    if (!canvas) return;
    ctx = canvas.getContext('2d');

    dom.lives = $('pd-lives');
    dom.coins = $('pd-coins');
    dom.bestWave = $('pd-best-wave');
    dom.waveNum = $('pd-wave-num');
    dom.waveRemaining = $('pd-wave-remaining');
    dom.sendWave = $('pd-send-wave');
    dom.shopList = $('pd-shop-list');
    dom.selected = $('pd-selected');
    dom.selectedBody = $('pd-selected-body');
    dom.upgrade = $('pd-upgrade');
    dom.sell = $('pd-sell');
    dom.overlay = $('pd-overlay');
    dom.overlayTitle = $('pd-overlay-title');
    dom.overlayText = $('pd-overlay-text');
    dom.overlayStats = $('pd-overlay-stats');
    dom.overlayPrimary = $('pd-overlay-primary');
    dom.overlayMenu = $('pd-overlay-menu');
    dom.waveBanner = $('pd-wave-banner');

    const menuHref = app.dataset.gamesHref || '/games/';
    dom.overlayMenu.href = menuHref;

    loadBest();
    buildShopList();
    refreshUI();

    canvas.addEventListener('click', onCanvasClick);
    canvas.addEventListener('mousemove', onCanvasMove);
    canvas.addEventListener('mouseleave', () => { state.hoverCell = null; });
    canvas.addEventListener('touchstart', (e) => { onCanvasMove(e); }, { passive: true });

    dom.sendWave.addEventListener('click', onSendWave);
    dom.upgrade.addEventListener('click', upgradeSelected);
    dom.sell.addEventListener('click', sellSelected);
    dom.overlayPrimary.addEventListener('click', resetGame);
    document.querySelectorAll('.pd-speed-btn').forEach(b => {
      b.addEventListener('click', () => setSpeed(Number(b.dataset.speed)));
    });

    // Keyboard accessibility: Esc deselects.
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        state.selectedShopId = null;
        state.selectedPlacedIdx = -1;
        refreshUI();
      }
    });

    requestAnimationFrame(frame);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
