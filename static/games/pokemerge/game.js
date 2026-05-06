// PokéMerge — vanilla JS merge game.
//
// Item shapes on the board:
//   { kind: 'egg', pool, tier, gen?, charges, maxCharges, regenAt }
//     pool: 'basic' | 'gen2' | 'gen3' | 'gen4' | 'gen5' | 'aura'
//     gen:  only set for pool='aura' (2..5) — controls coin multiplier
//   { kind: 'mon',   chain, tier: 1|2|3 }
//   { kind: 'shard', tier: 1|2, gen: 2..5 }
//   { kind: 'coin',  tier: 0|1|2|3|4, mult: 1|2|4|8 }
//
// Ladders:
//   basic → gen2 → gen3 → gen4 → gen5 by merging two T3s (egg promotion).
//   gen2..gen5 eggs occasionally drop Aura Shards (basic does not).
//   Shards are gen-stamped; gen-N shards forge a gen-N Aura Egg (T1 + T1 → T2,
//   T2 + T2 → Aura Egg of that gen).
//   Each gen of Aura Egg drops the same Pokémon pool but coin fragments with
//   double the multiplier of the previous gen (gen2=×1, gen3=×2, gen4=×4, gen5=×8).
//   Coin merge: same tier + same mult → next tier, same mult, capped at T4.

const COLS = 7;
const ROWS = 6;
const TOTAL = COLS * ROWS;

// ---------- Pokémon evolution chains, keyed by pool ----------
const EVOLUTION_CHAINS = {
  basic: [
    { id: 'bulbasaur',  stages: ['bulbasaur',  'ivysaur',    'venusaur']   },
    { id: 'charmander', stages: ['charmander', 'charmeleon', 'charizard']  },
    { id: 'squirtle',   stages: ['squirtle',   'wartortle',  'blastoise']  },
    { id: 'caterpie',   stages: ['caterpie',   'metapod',    'butterfree'] },
    { id: 'pidgey',     stages: ['pidgey',     'pidgeotto',  'pidgeot']    },
    { id: 'weedle',     stages: ['weedle',     'kakuna',     'beedrill']   },
    { id: 'geodude',    stages: ['geodude',    'graveler',   'golem']      },
  ],
  gen2: [
    { id: 'chikorita',  stages: ['chikorita',  'bayleef',    'meganium']   },
    { id: 'cyndaquil',  stages: ['cyndaquil',  'quilava',    'typhlosion'] },
    { id: 'totodile',   stages: ['totodile',   'croconaw',   'feraligatr'] },
    { id: 'mareep',     stages: ['mareep',     'flaaffy',    'ampharos']   },
    { id: 'larvitar',   stages: ['larvitar',   'pupitar',    'tyranitar']  },
  ],
  gen3: [
    { id: 'treecko',    stages: ['treecko',    'grovyle',    'sceptile']   },
    { id: 'torchic',    stages: ['torchic',    'combusken',  'blaziken']   },
    { id: 'mudkip',     stages: ['mudkip',     'marshtomp',  'swampert']   },
    { id: 'ralts',      stages: ['ralts',      'kirlia',     'gardevoir']  },
    { id: 'aron',       stages: ['aron',       'lairon',     'aggron']     },
  ],
  gen4: [
    { id: 'turtwig',    stages: ['turtwig',    'grotle',     'torterra']   },
    { id: 'chimchar',   stages: ['chimchar',   'monferno',   'infernape']  },
    { id: 'piplup',     stages: ['piplup',     'prinplup',   'empoleon']   },
    { id: 'starly',     stages: ['starly',     'staravia',   'staraptor']  },
    { id: 'gible',      stages: ['gible',      'gabite',     'garchomp']   },
  ],
  gen5: [
    { id: 'snivy',      stages: ['snivy',      'servine',    'serperior']  },
    { id: 'tepig',      stages: ['tepig',      'pignite',    'emboar']     },
    { id: 'oshawott',   stages: ['oshawott',   'dewott',     'samurott']   },
    { id: 'sewaddle',   stages: ['sewaddle',   'swadloon',   'leavanny']   },
    { id: 'axew',       stages: ['axew',       'fraxure',    'haxorus']    },
  ],
  aura: [
    { id: 'machop',     stages: ['machop',     'machoke',    'machamp']    },
    { id: 'abra',       stages: ['abra',       'kadabra',    'alakazam']   },
    { id: 'gastly',     stages: ['gastly',     'haunter',    'gengar']     },
    { id: 'poliwag',    stages: ['poliwag',    'poliwhirl',  'poliwrath']  },
    { id: 'dratini',    stages: ['dratini',    'dragonair',  'dragonite']  },
  ],
};
const CHAIN_BY_ID = {};
for (const pool of Object.keys(EVOLUTION_CHAINS)) {
  for (const chain of EVOLUTION_CHAINS[pool]) {
    CHAIN_BY_ID[chain.id] = { ...chain, pool };
  }
}

// ---------- Egg defs per pool ----------
// shardChance is 0 for basic — shards begin at gen 2.
const BASIC_EGG = {
  1: { sprite: 'assets/eggs/egg_common.png', name: 'Common Egg',
       maxCharges: 5, regenMs: 4500,  shardChance: 0,    anim: null },
  2: { sprite: 'assets/eggs/egg_rare.png',   name: 'Rare Egg',
       maxCharges: 4, regenMs: 7000,  shardChance: 0,    anim: null },
  3: { sprite: 'assets/eggs/egg_epic.png',   name: 'Epic Egg',
       maxCharges: 3, regenMs: 11000, shardChance: 0,    anim: null },
};
const GEN2_EGG = {
  1: { sprite: 'assets/eggs/egg_baby.png',   name: 'Baby Egg',
       maxCharges: 5, regenMs: 5500,  shardChance: 0.08, anim: null },
  2: { sprite: 'assets/eggs/egg_breed.png',  name: 'Breed Egg',
       maxCharges: 4, regenMs: 8500,  shardChance: 0.12, anim: null },
  3: { sprite: 'assets/eggs/egg_shiny.png',  name: 'Shiny Egg',
       maxCharges: 3, regenMs: 13000, shardChance: 0.16, anim: 'shiny' },
};
const GEN3_EGG = {
  1: { sprite: 'assets/eggs/egg_summer.png', name: 'Tropic Egg',
       maxCharges: 5, regenMs: 6000,  shardChance: 0.10, anim: null },
  2: { sprite: 'assets/eggs/egg_easter.png', name: 'Bloom Egg',
       maxCharges: 4, regenMs: 9500,  shardChance: 0.14, anim: null },
  3: { sprite: 'assets/eggs/egg_legendary.png', name: 'Legend Egg',
       maxCharges: 3, regenMs: 14500, shardChance: 0.18, anim: 'legend' },
};
const GEN4_EGG = {
  1: { sprite: 'assets/eggs/egg_lunar.png',  name: 'Lunar Egg',
       maxCharges: 5, regenMs: 6500,  shardChance: 0.12, anim: null },
  2: { sprite: 'assets/eggs/egg_cosmic.png', name: 'Cosmic Egg',
       maxCharges: 4, regenMs: 10500, shardChance: 0.16, anim: null },
  3: { sprite: 'assets/eggs/egg_avengers.png', name: 'Mythic Egg',
       maxCharges: 3, regenMs: 16000, shardChance: 0.20, anim: null },
};
const GEN5_EGG = {
  1: { sprite: 'assets/eggs/egg_disney.png', name: 'Fable Egg',
       maxCharges: 5, regenMs: 7000,  shardChance: 0.14, anim: null },
  2: { sprite: 'assets/eggs/egg_fusion.png', name: 'Fusion Egg',
       maxCharges: 4, regenMs: 12000, shardChance: 0.18, anim: null },
  3: { sprite: 'assets/eggs/egg_meme.png',   name: 'Apex Egg',
       maxCharges: 3, regenMs: 18000, shardChance: 0.22, anim: null },
};
const AURA_EGG = {
  1: { sprite: 'assets/eggs/egg_aura.png',   name: 'Aura Egg',
       maxCharges: 4, regenMs: 9000,  shardChance: 0,    anim: 'aura' },
};

const EGG_DEFS = {
  basic: BASIC_EGG, gen2: GEN2_EGG, gen3: GEN3_EGG,
  gen4: GEN4_EGG,  gen5: GEN5_EGG, aura: AURA_EGG,
};

// Each non-aura pool's T3 promotes to the next pool's T1 when merged.
const POOL_PROGRESSION = {
  basic: { next: 'gen2', promoteToast: 'Hatched a Baby Egg from Generation 2!' },
  gen2:  { next: 'gen3', promoteToast: 'Hatched a Tropic Egg from Generation 3!' },
  gen3:  { next: 'gen4', promoteToast: 'Hatched a Lunar Egg from Generation 4!' },
  gen4:  { next: 'gen5', promoteToast: 'Hatched a Fable Egg from Generation 5!' },
  gen5:  { next: null },
  aura:  { next: null },
};

// Eggs that source shards: shardGen tells us which "gen-N shard" they drop.
const POOL_SHARD_GEN = { basic: null, gen2: 2, gen3: 3, gen4: 4, gen5: 5, aura: null };

// Aura-egg → coin multiplier on dropped fragments (×2 per gen tier).
const AURA_COIN_MULT = { 2: 1, 3: 2, 4: 4, 5: 8 };
const AURA_GEN_LABEL = { 2: 'AURA·G2', 3: 'AURA·G3', 4: 'AURA·G4', 5: 'AURA·G5' };

// Standard drop table (used for all non-aura pools): T3 leans 70/25/5 toward stage 3.
const STANDARD_DROP_TABLE = {
  1: [ { stage: 1, weight: 1.00 } ],
  2: [ { stage: 2, weight: 1.00 } ],
  3: [
    { stage: 3, weight: 0.70 },
    { stage: 2, weight: 0.25 },
    { stage: 1, weight: 0.05 },
  ],
};
const DROP_TABLES = {
  basic: STANDARD_DROP_TABLE, gen2: STANDARD_DROP_TABLE,
  gen3: STANDARD_DROP_TABLE,  gen4: STANDARD_DROP_TABLE, gen5: STANDARD_DROP_TABLE,
};

const SHARD_DEF = {
  1: { name: 'Aura Shard',    scale: 0.55, opacity: 0.65 },
  2: { name: 'Aura Fragment', scale: 0.78, opacity: 0.85 },
};

const COIN_DEF = {
  0: { name: 'Coin Fragment', value: 0,   scale: 0.50, label: 'FRAG' },
  1: { name: 'Coin',          value: 1,   scale: 0.65 },
  2: { name: '10 Coins',      value: 10,  scale: 0.78 },
  3: { name: '50 Coins',      value: 50,  scale: 0.92 },
  4: { name: '100 Coins',     value: 100, scale: 1.00 },
};
const COIN_MAX_TIER = 4;

// Per-pool sell prices (scale gently with gen; aura beats raw gens).
const MON_SELL_PRICE = {
  basic: { 1: 2,  2: 10,  3: 60   },
  gen2:  { 1: 4,  2: 20,  3: 120  },
  gen3:  { 1: 7,  2: 35,  3: 210  },
  gen4:  { 1: 12, 2: 60,  3: 360  },
  gen5:  { 1: 20, 2: 100, 3: 600  },
  aura:  { 1: 5,  2: 25,  3: 150  },
};
const SHOP_PRICES = { 1: 50, 2: 300 };

// Aura-egg secondary drops.
const AURA_COIN_FRAG_CHANCE = 0.15;

// Sell prices for aura items. Gen multiplier reuses AURA_COIN_MULT so the
// scaling matches the coin-fragment doubling.
const SHARD_BASE_SELL  = { 1: 3, 2: 8 };
const AURA_EGG_BASE_SELL = 25;

// ---------- Special-offer buyers ----------
const NPCS = [
  { name: 'Mailman',        sprite: 'assets/npcs/01_mailman.png',
    quotes: ['Special delivery!', 'Got these to drop off?'] },
  { name: 'Captain Benry',  sprite: 'assets/npcs/07_captainbenry.png',
    quotes: ['Aye, fetch me these.', 'Cargo for the ship.'] },
  { name: 'The Farmer',     sprite: 'assets/npcs/14_farmer.png',
    quotes: ['Tradin\' for the ranch.', 'Got any to spare?'] },
  { name: 'Grandma Lucy',   sprite: 'assets/npcs/16_grandma_lucy.png',
    quotes: ['For the grandkids…', 'Help an old lady out?'] },
  { name: 'Kevin',          sprite: 'assets/npcs/22_kevin.png',
    quotes: ['Hook me up, friend.', 'Easy money.'] },
  { name: 'Mia',            sprite: 'assets/npcs/25_mia.png',
    quotes: ['I collect these!', 'Pretty please?'] },
  { name: 'Michael',        sprite: 'assets/npcs/27_michael.png',
    quotes: ['Stocking the locker.', 'Trade?'] },
  { name: 'Old Man',        sprite: 'assets/npcs/29_oldman.png',
    quotes: ['Reminds me o\' the old days.', 'I\'ll pay top coin.'] },
  { name: 'Professor',      sprite: 'assets/npcs/30_professor.png',
    quotes: ['For my research, of course.', 'Fascinating specimens.'] },
  { name: 'Sparkle',        sprite: 'assets/npcs/31_sparkle.png',
    quotes: ['Look at the shimmer!', 'Gotta have it!'] },
  { name: 'Tessa',          sprite: 'assets/npcs/33_tessa.png',
    quotes: ['Quick trade?', 'Nothing personal — business.'] },
  { name: 'Alder',          sprite: 'assets/npcs/45_alder.png',
    quotes: ['A worthy challenge.', 'Bring me your best.'] },
  { name: 'Officer Jenny',  sprite: 'assets/npcs/50_officerjen.png',
    quotes: ['Police business!', 'Need these for the case.'] },
  { name: 'Nurse Joy',      sprite: 'assets/npcs/51_nurse.png',
    quotes: ['For the centre…', 'These will help patients.'] },
  { name: 'PokéMart Clerk', sprite: 'assets/npcs/52_pokemartemployee.png',
    quotes: ['Restocking shelves.', 'Cash on delivery.'] },
  { name: 'Evan',           sprite: 'assets/npcs/13_evan.png',
    quotes: ['I\'ve got coins burnin\' a hole.', 'Fancy a deal?'] },
];

const MAX_OFFERS         = 3;
const OFFER_INTERVAL_MS  = 30_000;
const OFFER_INITIAL_DELAY = 12_000;
const OFFER_BONUS_RANGE  = [1.4, 1.8];

const STORAGE_KEY = 'pokemerge.save.v3';
const LEGACY_KEYS = ['pokemerge.save.v2', 'pokemerge.save.v1'];

const TICK_MS = 100;

// ---------- State ----------
const state = {
  coins: 0,
  cells: new Array(TOTAL).fill(null),
  // Progression — drives what offers can request.
  maxGen: 1,           // highest non-aura gen ever reached (1..5)
  hasAura: false,      // ever forged any aura egg
  // Offer marketplace.
  offers: [],          // active offer cards (max MAX_OFFERS)
  nextOfferAt: 0,      // timestamp at which we next try to fill a slot
};

const POOL_GEN_NUM = { basic: 1, gen2: 2, gen3: 3, gen4: 4, gen5: 5 };

function updateProgress(item) {
  if (!item) return;
  if (item.kind !== 'egg') return;
  if (item.pool === 'aura') { state.hasAura = true; return; }
  const g = POOL_GEN_NUM[item.pool];
  if (g && g > state.maxGen) state.maxGen = g;
}

function rescanProgress() {
  for (const c of state.cells) updateProgress(c);
}

// ---------- Save / load ----------
function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({
    coins: state.coins,
    cells: state.cells,
    maxGen: state.maxGen,
    hasAura: state.hasAura,
    offers: state.offers,
    nextOfferAt: state.nextOfferAt,
  }));
}

function migrate(cells) {
  for (const c of cells) {
    if (!c) continue;
    if (c.kind === 'egg') {
      if (!c.pool) c.pool = 'basic';
      if (c.pool === 'aura' && !c.gen) c.gen = 2;
    } else if (c.kind === 'shard') {
      if (!c.gen) c.gen = 2;
    } else if (c.kind === 'coin') {
      if (c.mult == null) c.mult = 1;
    }
  }
  return cells;
}

function load() {
  try {
    let raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      for (const k of LEGACY_KEYS) {
        raw = localStorage.getItem(k);
        if (raw) break;
      }
    }
    if (!raw) return false;
    const data = JSON.parse(raw);
    if (!data || !Array.isArray(data.cells) || data.cells.length !== TOTAL) return false;
    state.coins = data.coins | 0;
    state.cells = migrate(data.cells);
    state.maxGen = Math.max(1, data.maxGen | 0);
    state.hasAura = !!data.hasAura;
    state.offers = Array.isArray(data.offers) ? data.offers : [];
    state.nextOfferAt = data.nextOfferAt | 0;
    rescanProgress();
    if (!state.nextOfferAt) state.nextOfferAt = Date.now() + OFFER_INITIAL_DELAY;
    const now = Date.now();
    for (const c of state.cells) {
      if (c && c.kind === 'egg' && c.regenAt && c.regenAt < now - 60_000) {
        c.regenAt = now;
        if (c.charges < c.maxCharges) c.charges = c.maxCharges;
      }
    }
    return true;
  } catch (e) {
    console.warn('load failed', e);
    return false;
  }
}

// ---------- Helpers ----------
function eggDef(item) {
  const defs = EGG_DEFS[item.pool] || BASIC_EGG;
  return defs[item.tier];
}

function findFirstEmpty() {
  for (let i = 0; i < TOTAL; i++) if (!state.cells[i]) return i;
  return -1;
}
function findEmptyNear(idx) {
  const seen = new Set([idx]);
  const queue = [idx];
  while (queue.length) {
    const i = queue.shift();
    const r = Math.floor(i / COLS);
    const c = i % COLS;
    const neighbors = [
      [r-1, c], [r+1, c], [r, c-1], [r, c+1],
      [r-1, c-1], [r-1, c+1], [r+1, c-1], [r+1, c+1],
    ];
    for (const [nr, nc] of neighbors) {
      if (nr < 0 || nr >= ROWS || nc < 0 || nc >= COLS) continue;
      const ni = nr * COLS + nc;
      if (seen.has(ni)) continue;
      if (!state.cells[ni]) return ni;
      seen.add(ni);
      queue.push(ni);
    }
  }
  return findFirstEmpty();
}

function newEgg(pool, tier, opts = {}) {
  const def = (EGG_DEFS[pool] || BASIC_EGG)[tier];
  const item = {
    kind: 'egg', pool, tier,
    charges: def.maxCharges,
    maxCharges: def.maxCharges,
    regenAt: 0,
  };
  if (pool === 'aura') item.gen = opts.gen || 2;
  return item;
}
function newAuraEgg(gen) { return newEgg('aura', 1, { gen }); }

function randomMonFromPool(pool, tier) {
  const chains = EVOLUTION_CHAINS[pool];
  const chain = chains[Math.floor(Math.random() * chains.length)];
  return { kind: 'mon', chain: chain.id, tier };
}

function rollStageForEgg(pool, eggTier) {
  const table = DROP_TABLES[pool] && DROP_TABLES[pool][eggTier];
  if (!table) return eggTier;
  const r = Math.random();
  let acc = 0;
  for (const entry of table) {
    acc += entry.weight;
    if (r < acc) return entry.stage;
  }
  return table[table.length - 1].stage;
}

function spritePathForMon(mon) {
  const chain = CHAIN_BY_ID[mon.chain];
  if (!chain) return '';
  return `assets/pokemon/${chain.stages[mon.tier - 1]}.png`;
}
function monDisplayName(mon) {
  const chain = CHAIN_BY_ID[mon.chain];
  if (!chain) return '?';
  const s = chain.stages[mon.tier - 1];
  return s.charAt(0).toUpperCase() + s.slice(1);
}

function coinValue(item) {
  return COIN_DEF[item.tier].value * (item.mult || 1);
}

function sellValue(item) {
  if (!item) return 0;
  if (item.kind === 'mon') {
    const chain = CHAIN_BY_ID[item.chain];
    const pool = chain ? chain.pool : 'basic';
    return (MON_SELL_PRICE[pool] && MON_SELL_PRICE[pool][item.tier]) || 0;
  }
  if (item.kind === 'coin') return item.tier === 0 ? 0 : coinValue(item);
  if (item.kind === 'shard') {
    return (SHARD_BASE_SELL[item.tier] || 0) * (AURA_COIN_MULT[item.gen] || 1);
  }
  if (item.kind === 'egg' && item.pool === 'aura') {
    return AURA_EGG_BASE_SELL * (AURA_COIN_MULT[item.gen] || 1);
  }
  return 0;
}
function coinMultClass(mult) {
  if (mult >= 8) return 'mult-8';
  if (mult >= 4) return 'mult-4';
  if (mult >= 2) return 'mult-2';
  return 'mult-1';
}

// ---------- Mutations ----------
function tryMerge(srcIdx, dstIdx) {
  if (srcIdx === dstIdx) return false;
  const src = state.cells[srcIdx];
  const dst = state.cells[dstIdx];
  if (!src || !dst) return false;

  // Egg + egg: in-pool T1→T2→T3, then T3 promotes to next-pool T1.
  if (src.kind === 'egg' && dst.kind === 'egg'
      && src.pool === dst.pool && src.tier === dst.tier
      && (src.gen || null) === (dst.gen || null)) {
    if (src.tier < 3) {
      const nextDef = (EGG_DEFS[src.pool] || {})[src.tier + 1];
      if (!nextDef) return false;
      const merged = newEgg(src.pool, src.tier + 1, { gen: src.gen });
      state.cells[dstIdx] = merged;
      state.cells[srcIdx] = null;
      updateProgress(merged);
      flashCell(dstIdx, 'merge-pop');
      toast(`Merged into ${nextDef.name}!`);
      return true;
    }
    const prog = POOL_PROGRESSION[src.pool];
    if (!prog || !prog.next) return false;
    const promotedDef = (EGG_DEFS[prog.next] || {})[1];
    if (!promotedDef) return false;
    const promoted = newEgg(prog.next, 1);
    state.cells[dstIdx] = promoted;
    state.cells[srcIdx] = null;
    updateProgress(promoted);
    flashCell(dstIdx, 'gen-pop');
    toast(prog.promoteToast || `Hatched a ${promotedDef.name}!`);
    return true;
  }

  // Mon + mon: same chain + same tier evolves up the chain.
  if (src.kind === 'mon' && dst.kind === 'mon'
      && src.chain === dst.chain && src.tier === dst.tier) {
    if (src.tier >= 3) return false;
    const evolved = { kind: 'mon', chain: src.chain, tier: src.tier + 1 };
    state.cells[dstIdx] = evolved;
    state.cells[srcIdx] = null;
    flashCell(dstIdx, 'merge-pop');
    toast(`Evolved into ${monDisplayName(evolved)}!`);
    return true;
  }

  // Shard merge: gen-stamped. T1+T1 → T2; T2+T2 → Aura Egg of that gen.
  if (src.kind === 'shard' && dst.kind === 'shard'
      && src.tier === dst.tier && src.gen === dst.gen) {
    if (src.tier === 1) {
      state.cells[dstIdx] = { kind: 'shard', tier: 2, gen: src.gen };
      state.cells[srcIdx] = null;
      flashCell(dstIdx, 'merge-pop');
      toast('Combined into Aura Fragment!');
      return true;
    }
    if (src.tier === 2) {
      const auraEgg = newAuraEgg(src.gen);
      state.cells[dstIdx] = auraEgg;
      state.cells[srcIdx] = null;
      updateProgress(auraEgg);
      flashCell(dstIdx, 'aura-pop');
      toast(`Forged a Gen ${src.gen} Aura Egg!`);
      return true;
    }
  }

  // Coin merge: tier+mult must both match; merged result keeps mult.
  if (src.kind === 'coin' && dst.kind === 'coin'
      && src.tier === dst.tier && (src.mult || 1) === (dst.mult || 1)) {
    if (src.tier >= COIN_MAX_TIER) return false;
    const mult = src.mult || 1;
    const merged = { kind: 'coin', tier: src.tier + 1, mult };
    state.cells[dstIdx] = merged;
    state.cells[srcIdx] = null;
    flashCell(dstIdx, 'coin-pop');
    toast(`Merged into ${COIN_DEF[merged.tier].value * mult} coins!`);
    return true;
  }

  return false;
}

function tryMove(srcIdx, dstIdx) {
  if (srcIdx === dstIdx) return false;
  if (state.cells[dstIdx]) return false;
  state.cells[dstIdx] = state.cells[srcIdx];
  state.cells[srcIdx] = null;
  return true;
}

function sellAt(idx) {
  const it = state.cells[idx];
  if (!it) return false;
  if (it.kind === 'coin' && it.tier === 0) {
    toast('Coin Fragments must be merged first.');
    return false;
  }
  const price = sellValue(it);
  if (price <= 0) return false;
  state.coins += price;
  state.cells[idx] = null;
  toast(`+${price} coins`);
  return true;
}

function clickEgg(idx) {
  const it = state.cells[idx];
  if (!it || it.kind !== 'egg') return;
  if (it.charges <= 0) {
    toast('Egg is recharging…');
    return;
  }
  const target = findEmptyNear(idx);
  if (target < 0) {
    toast('No empty space!');
    return;
  }
  const def = eggDef(it);
  it.charges -= 1;
  if (it.charges < it.maxCharges && !it.regenAt) {
    it.regenAt = Date.now() + def.regenMs;
  }

  let drop;
  if (it.pool === 'aura') {
    if (Math.random() < AURA_COIN_FRAG_CHANCE) {
      drop = { kind: 'coin', tier: 0, mult: AURA_COIN_MULT[it.gen] || 1 };
      state.cells[target] = drop;
      flashCell(target, 'coin-pop');
      toast(`★ Coin Fragment (×${drop.mult})`);
    } else {
      drop = randomMonFromPool('aura', it.tier);
      state.cells[target] = drop;
      flashCell(target, 'spawn-burst');
    }
  } else {
    const shardGen = POOL_SHARD_GEN[it.pool];
    if (shardGen != null && def.shardChance > 0 && Math.random() < def.shardChance) {
      drop = { kind: 'shard', tier: 1, gen: shardGen };
      state.cells[target] = drop;
      flashCell(target, 'aura-pop');
      toast(`✦ Gen ${shardGen} Aura Shard!`);
    } else {
      const stage = rollStageForEgg(it.pool, it.tier);
      drop = randomMonFromPool(it.pool, stage);
      state.cells[target] = drop;
      flashCell(target, 'spawn-burst');
    }
  }
  save();
  render();
}

// ---------- Offers ----------
function weightedPick(cands) {
  let total = 0;
  for (const c of cands) total += c.weight || 1;
  let r = Math.random() * total;
  for (const c of cands) {
    r -= c.weight || 1;
    if (r <= 0) return c;
  }
  return cands[cands.length - 1];
}

function reqUnitValue(req) {
  if (req.kind === 'mon') {
    const chain = CHAIN_BY_ID[req.match.chain];
    const pool = chain ? chain.pool : 'basic';
    return (MON_SELL_PRICE[pool] && MON_SELL_PRICE[pool][req.match.tier]) || 0;
  }
  if (req.kind === 'shard') {
    return (SHARD_BASE_SELL[req.match.tier] || 0) * (AURA_COIN_MULT[req.match.gen] || 1);
  }
  return 0;
}

function buildOfferCandidates() {
  const cands = [];
  for (let g = 1; g <= state.maxGen; g++) {
    const pool = g === 1 ? 'basic' : 'gen' + g;
    const chains = EVOLUTION_CHAINS[pool] || [];
    for (const chain of chains) {
      // Stage 1 most common, stage 3 rarest in offers — but each stage's
      // intrinsic value is higher, so the bonus payout scales naturally.
      cands.push({ kind: 'mon', match: { chain: chain.id, tier: 1 }, weight: 5 });
      cands.push({ kind: 'mon', match: { chain: chain.id, tier: 2 }, weight: 2 });
      cands.push({ kind: 'mon', match: { chain: chain.id, tier: 3 }, weight: 1 });
    }
    if (g >= 2) {
      cands.push({ kind: 'shard', match: { tier: 1, gen: g }, weight: 2 });
      cands.push({ kind: 'shard', match: { tier: 2, gen: g }, weight: 1 });
    }
  }
  if (state.hasAura) {
    for (const chain of EVOLUTION_CHAINS.aura) {
      cands.push({ kind: 'mon', match: { chain: chain.id, tier: 1 }, weight: 2 });
      cands.push({ kind: 'mon', match: { chain: chain.id, tier: 2 }, weight: 1 });
    }
  }
  return cands;
}

function generateOffer() {
  const cands = buildOfferCandidates();
  if (cands.length < 2) return null;
  const npc = NPCS[Math.floor(Math.random() * NPCS.length)];
  const quote = npc.quotes && npc.quotes.length
    ? npc.quotes[Math.floor(Math.random() * npc.quotes.length)]
    : 'I\'ll buy these.';
  const desiredCount = 2 + (Math.random() < 0.4 ? 1 : 0);
  const seenKeys = new Set();
  const requests = [];
  let baseValue = 0;
  for (let attempts = 0; requests.length < desiredCount && attempts < 40; attempts++) {
    const c = weightedPick(cands);
    const key = `${c.kind}:${JSON.stringify(c.match)}`;
    if (seenKeys.has(key)) continue;
    const unitValue = reqUnitValue(c);
    if (unitValue <= 0) continue;
    seenKeys.add(key);
    const count = 1;
    requests.push({ kind: c.kind, match: c.match, count });
    baseValue += unitValue * count;
  }
  if (requests.length === 0) return null;
  const [lo, hi] = OFFER_BONUS_RANGE;
  const bonus = lo + Math.random() * (hi - lo);
  const reward = Math.max(1, Math.round(baseValue * bonus));
  return {
    id: 'o' + Date.now() + '-' + Math.floor(Math.random() * 10000),
    npc: { name: npc.name, sprite: npc.sprite },
    quote,
    requests,
    reward,
    bonus: Math.round((bonus - 1) * 100),
    createdAt: Date.now(),
  };
}

function itemMatchesReq(item, req) {
  if (!item || item.kind !== req.kind) return false;
  const m = req.match;
  if (req.kind === 'mon')   return item.chain === m.chain && item.tier === m.tier;
  if (req.kind === 'shard') return item.tier === m.tier && item.gen === m.gen;
  return false;
}

// Returns the cell indices that would satisfy the offer, or null if not possible.
function planFulfillment(offer) {
  const used = new Set();
  for (const req of offer.requests) {
    let matched = 0;
    for (let i = 0; i < TOTAL; i++) {
      if (used.has(i)) continue;
      const c = state.cells[i];
      if (!itemMatchesReq(c, req)) continue;
      used.add(i);
      matched++;
      if (matched >= req.count) break;
    }
    if (matched < req.count) return null;
  }
  return [...used];
}

function canFulfillOffer(offer) { return planFulfillment(offer) !== null; }

function fulfillOffer(offerId) {
  const offer = state.offers.find(o => o.id === offerId);
  if (!offer) return;
  const cells = planFulfillment(offer);
  if (!cells) {
    toast('You\'re missing some items.');
    return;
  }
  for (const i of cells) {
    flashCell(i, 'spawn-burst');
    state.cells[i] = null;
  }
  state.coins += offer.reward;
  state.offers = state.offers.filter(o => o.id !== offerId);
  toast(`+${offer.reward} coins from ${offer.npc.name}!`);
  save();
  render();
}

function skipOffer(offerId) {
  state.offers = state.offers.filter(o => o.id !== offerId);
  save();
  render();
}

function tickOffers() {
  if (state.offers.length >= MAX_OFFERS) return false;
  if (Date.now() < (state.nextOfferAt || 0)) return false;
  const offer = generateOffer();
  if (!offer) {
    state.nextOfferAt = Date.now() + 5000;
    return false;
  }
  state.offers.push(offer);
  state.nextOfferAt = Date.now() + OFFER_INTERVAL_MS;
  save();
  return true;
}

// ---------- Tick (egg regen) ----------
// Charge regen happens every TICK_MS but does NOT trigger a full render — that
// was rebuilding 42 cells + all listeners 10× per second across many eggs and
// driving the browser into the ground over long sessions. We only full-render
// when something structural changes (a new offer arrived, or a user action).
let lastChargeSaveAt = 0;
function tick() {
  try {
    const now = Date.now();
    let charged = false;
    for (const c of state.cells) {
      if (!c || c.kind !== 'egg') continue;
      if (c.charges >= c.maxCharges) {
        c.regenAt = 0;
        continue;
      }
      const def = eggDef(c);
      if (!c.regenAt) c.regenAt = now + def.regenMs;
      while (c.regenAt && now >= c.regenAt && c.charges < c.maxCharges) {
        c.charges += 1;
        if (c.charges < c.maxCharges) c.regenAt += def.regenMs;
        else c.regenAt = 0;
        charged = true;
      }
    }
    const offerArrived = tickOffers();
    if (offerArrived) {
      render();
    } else {
      updateChargeProgress();
      if (charged && now - lastChargeSaveAt > 5000) {
        lastChargeSaveAt = now;
        save();
      }
    }
  } catch (e) {
    console.error('tick error', e);
  }
}

// ---------- Rendering ----------
const boardEl = document.getElementById('board');
const coinsEl = document.getElementById('coins');
const trashEl = document.getElementById('trash');

function eggFillPct(item, now) {
  const def = eggDef(item);
  if (!item.regenAt || item.charges >= item.maxCharges) return 0;
  const remaining = Math.max(0, item.regenAt - now);
  return Math.max(0, Math.min(1, 1 - remaining / def.regenMs));
}

function render() {
  boardEl.style.setProperty('--cols', COLS);
  boardEl.style.setProperty('--rows', ROWS);
  boardEl.innerHTML = '';
  const now = Date.now();
  for (let i = 0; i < TOTAL; i++) {
    const cell = document.createElement('div');
    cell.className = 'cell';
    cell.dataset.idx = String(i);
    attachCellDnd(cell, i);
    const item = state.cells[i];
    if (item) renderItemInto(cell, item, i, now);
    boardEl.appendChild(cell);
  }
  coinsEl.textContent = state.coins;
  document.getElementById('buy-common').toggleAttribute('disabled', state.coins < SHOP_PRICES[1]);
  document.getElementById('buy-rare').toggleAttribute('disabled', state.coins < SHOP_PRICES[2]);
  renderOffers();
}

function reqDisplayInfo(req) {
  if (req.kind === 'mon') {
    const chain = CHAIN_BY_ID[req.match.chain];
    if (!chain) return { type: 'img', src: '', name: '?' };
    const stage = chain.stages[req.match.tier - 1];
    const name = stage.charAt(0).toUpperCase() + stage.slice(1) + ` (S${req.match.tier})`;
    return { type: 'img', src: `assets/pokemon/${stage}.png`, name };
  }
  if (req.kind === 'shard') {
    const label = req.match.tier === 1 ? 'Shard' : 'Fragment';
    return {
      type: 'sprite',
      cls: 'sprite aura-sprite shard-gen-' + req.match.gen,
      name: `Gen ${req.match.gen} Aura ${label}`,
    };
  }
  return { type: 'img', src: '', name: '?' };
}

function renderOffers() {
  const listEl = document.getElementById('offer-list');
  const emptyEl = document.getElementById('offer-empty');
  if (!listEl) return;
  listEl.innerHTML = '';
  if (state.offers.length === 0) {
    emptyEl.style.display = 'block';
    return;
  }
  emptyEl.style.display = 'none';
  const now = Date.now();
  for (const offer of state.offers) {
    const card = document.createElement('div');
    card.className = 'offer';
    if (now - (offer.createdAt || 0) < 1000) card.classList.add('just-arrived');

    const portrait = document.createElement('div');
    portrait.className = 'offer-portrait';
    const portraitImg = document.createElement('img');
    portraitImg.src = offer.npc.sprite;
    portraitImg.alt = offer.npc.name;
    portrait.appendChild(portraitImg);
    card.appendChild(portrait);

    const name = document.createElement('div');
    name.className = 'offer-name';
    name.textContent = offer.npc.name;
    card.appendChild(name);

    const quote = document.createElement('div');
    quote.className = 'offer-quote';
    quote.textContent = `“${offer.quote}”`;
    card.appendChild(quote);

    const items = document.createElement('div');
    items.className = 'offer-items';
    const plan = planFulfillment(offer);
    const haveAll = plan !== null;
    for (const req of offer.requests) {
      const it = document.createElement('div');
      it.className = 'offer-item';
      const have = countAvailableForReq(req);
      if (have >= req.count) it.classList.add('have');
      else it.classList.add('miss');
      const info = reqDisplayInfo(req);
      const thumb = document.createElement('div');
      thumb.className = 'thumb';
      if (info.type === 'sprite') {
        const div = document.createElement('div');
        div.className = info.cls;
        thumb.appendChild(div);
      } else {
        const img = document.createElement('img');
        img.src = info.src;
        img.alt = info.name;
        thumb.appendChild(img);
      }
      it.appendChild(thumb);
      const lbl = document.createElement('span');
      lbl.textContent = `×${req.count}`;
      it.appendChild(lbl);
      it.title = `${info.name} — you have ${have}/${req.count}`;
      items.appendChild(it);
    }
    card.appendChild(items);

    const actions = document.createElement('div');
    actions.className = 'offer-actions';
    const buy = document.createElement('button');
    buy.className = 'offer-buy';
    buy.textContent = `Sell — ${offer.reward} coins`;
    if (!haveAll) buy.disabled = true;
    buy.title = `+${offer.bonus}% bonus over individual sale`;
    buy.addEventListener('click', () => fulfillOffer(offer.id));
    actions.appendChild(buy);
    const skip = document.createElement('button');
    skip.className = 'offer-skip';
    skip.textContent = 'Skip';
    skip.addEventListener('click', () => skipOffer(offer.id));
    actions.appendChild(skip);
    card.appendChild(actions);

    listEl.appendChild(card);
  }
}

function countAvailableForReq(req) {
  let n = 0;
  for (const c of state.cells) if (itemMatchesReq(c, req)) n++;
  return n;
}

function renderItemInto(cell, item, idx, now) {
  const el = document.createElement('div');
  el.className = 'item';
  el.draggable = true;
  el.dataset.idx = String(idx);
  attachItemDnd(el, idx);

  if (item.kind === 'egg') {
    const def = eggDef(item);
    el.classList.add('egg');
    el.classList.add('egg-' + item.pool);
    if (item.pool === 'aura') {
      el.classList.add('aura');
      el.classList.add('aura-gen-' + (item.gen || 2));
    }
    if (item.charges > 0) el.classList.add('ready');
    if (item.charges === 0) el.classList.add('empty');

    let sprite;
    if (def.anim === 'aura') {
      sprite = document.createElement('div');
      sprite.className = 'sprite aura-sprite';
    } else if (def.anim === 'shiny') {
      sprite = document.createElement('div');
      sprite.className = 'sprite shiny-sprite';
    } else if (def.anim === 'legend') {
      sprite = document.createElement('div');
      sprite.className = 'sprite legend-sprite';
    } else {
      sprite = document.createElement('img');
      sprite.src = def.sprite;
      sprite.alt = def.name;
    }
    if (item.pool === 'aura') {
      sprite.title = `${def.name} (Gen ${item.gen}) — sell for ${sellValue(item)}`;
    } else {
      sprite.title = def.name;
    }
    el.appendChild(sprite);

    const badge = document.createElement('div');
    badge.className = 'tier-badge';
    if (item.pool === 'aura') {
      badge.classList.add('aura');
      badge.textContent = AURA_GEN_LABEL[item.gen] || 'AURA';
    } else if (item.pool === 'gen2') { badge.classList.add('gen2'); badge.textContent = 'G2·T' + item.tier; }
    else if (item.pool === 'gen3') { badge.classList.add('gen3'); badge.textContent = 'G3·T' + item.tier; }
    else if (item.pool === 'gen4') { badge.classList.add('gen4'); badge.textContent = 'G4·T' + item.tier; }
    else if (item.pool === 'gen5') { badge.classList.add('gen5'); badge.textContent = 'G5·T' + item.tier; }
    else { badge.textContent = 'T' + item.tier; }
    el.appendChild(badge);

    const chargeBar = document.createElement('div');
    chargeBar.className = 'charges';
    const pct = eggFillPct(item, now) * 100;
    for (let p = 0; p < item.maxCharges; p++) {
      const pip = document.createElement('div');
      pip.className = 'charge-pip';
      if (p < item.charges) {
        pip.classList.add('full');
      } else if (p === item.charges) {
        const fill = document.createElement('span');
        fill.className = 'fill';
        fill.style.width = pct.toFixed(1) + '%';
        pip.appendChild(fill);
      }
      chargeBar.appendChild(pip);
    }
    el.appendChild(chargeBar);

    el.addEventListener('click', () => {
      if (el.classList.contains('dragging')) return;
      clickEgg(idx);
    });
  } else if (item.kind === 'mon') {
    const img = document.createElement('img');
    img.src = spritePathForMon(item);
    img.alt = monDisplayName(item);
    img.title = monDisplayName(item);
    el.appendChild(img);
    const badge = document.createElement('div');
    badge.className = 'tier-badge';
    badge.textContent = 'S' + item.tier;
    el.appendChild(badge);
  } else if (item.kind === 'shard') {
    el.classList.add('shard');
    el.classList.add('shard-t' + item.tier);
    el.classList.add('shard-gen-' + item.gen);
    const def = SHARD_DEF[item.tier];
    const sprite = document.createElement('div');
    sprite.className = 'sprite aura-sprite';
    sprite.title = `${def.name} (Gen ${item.gen}) — merge or sell for ${sellValue(item)}`;
    sprite.style.setProperty('--shard-scale', String(def.scale));
    sprite.style.setProperty('--shard-opacity', String(def.opacity));
    el.appendChild(sprite);
    const badge = document.createElement('div');
    badge.className = 'tier-badge aura';
    badge.textContent = (item.tier === 1 ? 'SHARD' : 'FRAG') + '·G' + item.gen;
    el.appendChild(badge);
  } else if (item.kind === 'coin') {
    const mult = item.mult || 1;
    el.classList.add('coin');
    el.classList.add('coin-t' + item.tier);
    el.classList.add(coinMultClass(mult));
    const def = COIN_DEF[item.tier];
    const img = document.createElement('img');
    img.src = 'assets/coins.png';
    img.alt = def.name;
    const value = coinValue(item);
    img.title = item.tier === 0
      ? `Coin Fragment (×${mult}) — merge two to make a ${mult}-coin`
      : (item.tier < COIN_MAX_TIER
          ? `${value} coins (×${mult}) — merge or sell for ${value}`
          : `${value} coins (×${mult}) — sell for ${value}`);
    img.style.transform = `scale(${def.scale})`;
    el.appendChild(img);
    const badge = document.createElement('div');
    badge.className = 'tier-badge coin';
    badge.textContent = item.tier === 0 ? `FRAG×${mult}` : String(value);
    el.appendChild(badge);
  }

  cell.appendChild(el);
}

// Targeted DOM update for the charge bar. Updates pip fullness, fill widths,
// and ready/empty classes without rebuilding the whole board.
function updateChargeProgress() {
  const now = Date.now();
  const items = boardEl.querySelectorAll('.item.egg');
  items.forEach(el => {
    const i = parseInt(el.dataset.idx, 10);
    const it = state.cells[i];
    if (!it || it.kind !== 'egg') return;
    el.classList.toggle('ready', it.charges > 0);
    el.classList.toggle('empty', it.charges === 0);
    const pips = el.querySelectorAll('.charge-pip');
    pips.forEach((pip, p) => {
      const isFull = p < it.charges;
      pip.classList.toggle('full', isFull);
      const existingFill = pip.querySelector('.fill');
      if (!isFull && p === it.charges) {
        // Active pip — needs a fill span
        let fill = existingFill;
        if (!fill) {
          fill = document.createElement('span');
          fill.className = 'fill';
          pip.appendChild(fill);
        }
        if (it.regenAt) {
          fill.style.width = (eggFillPct(it, now) * 100).toFixed(1) + '%';
        }
      } else if (existingFill) {
        existingFill.remove();
      }
    });
  });
}

function flashCell(idx, kindClass) {
  const cell = boardEl.querySelector(`.cell[data-idx="${idx}"]`);
  if (!cell) return;
  const fx = document.createElement('div');
  fx.className = kindClass;
  cell.appendChild(fx);
  setTimeout(() => fx.remove(), 700);
}

let toastTimer;
function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.remove('show'), 1300);
}

// ---------- Drag and drop ----------
let dragSrcIdx = -1;

function attachItemDnd(el, idx) {
  el.addEventListener('dragstart', (e) => {
    dragSrcIdx = idx;
    el.classList.add('dragging');
    try {
      e.dataTransfer.setData('text/plain', String(idx));
      e.dataTransfer.effectAllowed = 'move';
    } catch (_) {}
  });
  el.addEventListener('dragend', () => {
    el.classList.remove('dragging');
    dragSrcIdx = -1;
    boardEl.querySelectorAll('.cell').forEach(c => {
      c.classList.remove('drop-ok', 'drop-merge', 'drop-bad');
    });
    trashEl.classList.remove('drop-ok');
  });
}

function classifyDrop(srcIdx, dstIdx) {
  if (srcIdx < 0 || dstIdx < 0 || srcIdx === dstIdx) return 'none';
  const src = state.cells[srcIdx];
  const dst = state.cells[dstIdx];
  if (!src) return 'none';
  if (!dst) return 'move';
  if (src.kind === 'egg' && dst.kind === 'egg'
      && src.pool === dst.pool && src.tier === dst.tier
      && (src.gen || null) === (dst.gen || null)) {
    if (src.tier < 3 && (EGG_DEFS[src.pool] || {})[src.tier + 1]) return 'merge';
    if (src.tier === 3 && POOL_PROGRESSION[src.pool] && POOL_PROGRESSION[src.pool].next) return 'merge';
  }
  if (src.kind === 'mon' && dst.kind === 'mon'
      && src.chain === dst.chain && src.tier === dst.tier && src.tier < 3) return 'merge';
  if (src.kind === 'shard' && dst.kind === 'shard'
      && src.tier === dst.tier && src.gen === dst.gen) return 'merge';
  if (src.kind === 'coin' && dst.kind === 'coin'
      && src.tier === dst.tier && (src.mult || 1) === (dst.mult || 1)
      && src.tier < COIN_MAX_TIER) return 'merge';
  return 'bad';
}

function attachCellDnd(cell, idx) {
  cell.addEventListener('dragover', (e) => {
    if (dragSrcIdx < 0) return;
    const kind = classifyDrop(dragSrcIdx, idx);
    if (kind === 'none') return;
    e.preventDefault();
    cell.classList.remove('drop-ok', 'drop-merge', 'drop-bad');
    if (kind === 'move') cell.classList.add('drop-ok');
    else if (kind === 'merge') cell.classList.add('drop-merge');
    else cell.classList.add('drop-bad');
  });
  cell.addEventListener('dragleave', () => {
    cell.classList.remove('drop-ok', 'drop-merge', 'drop-bad');
  });
  cell.addEventListener('drop', (e) => {
    e.preventDefault();
    const srcIdx = dragSrcIdx >= 0 ? dragSrcIdx : parseInt(e.dataTransfer.getData('text/plain') || '-1', 10);
    cell.classList.remove('drop-ok', 'drop-merge', 'drop-bad');
    if (srcIdx < 0) return;
    const kind = classifyDrop(srcIdx, idx);
    if (kind === 'merge') {
      tryMerge(srcIdx, idx);
    } else if (kind === 'move') {
      tryMove(srcIdx, idx);
    } else {
      return;
    }
    save();
    render();
  });
}

function isSellable(item) {
  if (!item) return false;
  if (item.kind === 'mon') return true;
  if (item.kind === 'coin' && item.tier >= 1) return true;
  if (item.kind === 'shard') return true;
  if (item.kind === 'egg' && item.pool === 'aura') return true;
  return false;
}

function attachTrashDnd() {
  trashEl.addEventListener('dragover', (e) => {
    if (dragSrcIdx < 0) return;
    if (!isSellable(state.cells[dragSrcIdx])) return;
    e.preventDefault();
    trashEl.classList.add('drop-ok');
  });
  trashEl.addEventListener('dragleave', () => trashEl.classList.remove('drop-ok'));
  trashEl.addEventListener('drop', (e) => {
    e.preventDefault();
    trashEl.classList.remove('drop-ok');
    const srcIdx = dragSrcIdx >= 0 ? dragSrcIdx : parseInt(e.dataTransfer.getData('text/plain') || '-1', 10);
    if (srcIdx < 0) return;
    if (sellAt(srcIdx)) {
      save();
      render();
    }
  });
}

// ---------- Shop ----------
function buyEgg(tier) {
  const price = SHOP_PRICES[tier];
  if (!price) return;
  if (state.coins < price) {
    toast('Not enough coins.');
    return;
  }
  const slot = findFirstEmpty();
  if (slot < 0) {
    toast('Board is full!');
    return;
  }
  state.coins -= price;
  const egg = newEgg('basic', tier);
  state.cells[slot] = egg;
  updateProgress(egg);
  toast(`Bought ${BASIC_EGG[tier].name}`);
  save();
  render();
}

document.getElementById('buy-common').addEventListener('click', () => buyEgg(1));
document.getElementById('buy-rare').addEventListener('click', () => buyEgg(2));
document.getElementById('reset').addEventListener('click', () => {
  if (!confirm('Reset all progress?')) return;
  localStorage.removeItem(STORAGE_KEY);
  for (const k of LEGACY_KEYS) localStorage.removeItem(k);
  state.coins = 30;
  state.cells = new Array(TOTAL).fill(null);
  state.cells[Math.floor(TOTAL / 2)] = newEgg('basic', 1);
  state.maxGen = 1;
  state.hasAura = false;
  state.offers = [];
  state.nextOfferAt = Date.now() + OFFER_INITIAL_DELAY;
  save();
  render();
  toast('Save cleared.');
});

// ---------- Boot ----------
let tickIntervalId = null;
function startTicking() {
  if (tickIntervalId !== null) return;
  tickIntervalId = setInterval(tick, TICK_MS);
}
function stopTicking() {
  if (tickIntervalId === null) return;
  clearInterval(tickIntervalId);
  tickIntervalId = null;
}

function boot() {
  const loaded = load();
  if (!loaded) {
    state.coins = 30;
    state.cells[Math.floor(TOTAL / 2)] = newEgg('basic', 1);
    state.maxGen = 1;
    state.hasAura = false;
    state.offers = [];
    state.nextOfferAt = Date.now() + OFFER_INITIAL_DELAY;
    save();
  }
  render();
  attachTrashDnd();
  startTicking();
  // Pause the loop when the tab is hidden — browsers throttle setInterval
  // there anyway, but explicit pause avoids any GPU work for animated
  // sprites that the OS might keep compositing.
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stopTicking();
    else { startTicking(); render(); }
  });
}

boot();
