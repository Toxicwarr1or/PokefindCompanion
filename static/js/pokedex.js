// Pokedex client-side enhancements: form-tab switcher + list sort + search.
// No framework, no build step.

(function () {
    'use strict';

    // ---------- Form tabs (single Pokemon page) ----------
    function initFormTabs() {
        const tabs = document.querySelectorAll('.form-tab');
        if (!tabs.length) return;
        const panels = document.querySelectorAll('.form-panel');
        tabs.forEach(function (tab) {
            tab.addEventListener('click', function () {
                const idx = tab.getAttribute('data-form-index');
                tabs.forEach(function (t) {
                    const active = t.getAttribute('data-form-index') === idx;
                    t.classList.toggle('active', active);
                    t.setAttribute('aria-selected', active ? 'true' : 'false');
                });
                panels.forEach(function (p) {
                    const active = p.getAttribute('data-form-index') === idx;
                    p.classList.toggle('active', active);
                    if (active) p.removeAttribute('hidden'); else p.setAttribute('hidden', '');
                });
            });
        });
    }

    // ---------- Pokedex list sort + search + anim/skin filter ----------
    function initDexList() {
        const grid = document.getElementById('dex-grid');
        if (!grid) return;
        const cards = Array.from(grid.querySelectorAll('.dex-card'));
        const sortButtons = document.querySelectorAll('.dex-sort button');
        const filterButtons = document.querySelectorAll('.dex-filter button');
        const skinFilterButtons = document.querySelectorAll('.dex-skin-filter button');
        const skinFilterClear = document.querySelector('.dex-skin-filter-clear');
        const search = document.getElementById('dex-search');
        const visibleCount = document.getElementById('dex-visible');

        const comparators = {
            'dex-asc':  function (a, b) { return parseInt(a.dataset.dex, 10) - parseInt(b.dataset.dex, 10); },
            'dex-desc': function (a, b) { return parseInt(b.dataset.dex, 10) - parseInt(a.dataset.dex, 10); },
            'name-asc':  function (a, b) { return a.dataset.name.localeCompare(b.dataset.name); },
            'name-desc': function (a, b) { return b.dataset.name.localeCompare(a.dataset.name); }
        };

        function applySort(mode) {
            const cmp = comparators[mode];
            if (!cmp) return;
            const sorted = cards.slice().sort(cmp);
            sorted.forEach(function (c) { grid.appendChild(c); });
        }

        function activeAnimFilters() {
            const set = new Set();
            filterButtons.forEach(function (btn) {
                if (btn.classList.contains('active')) set.add(btn.getAttribute('data-anim-filter'));
            });
            return set;
        }

        function activeSkinFilters() {
            const set = new Set();
            skinFilterButtons.forEach(function (btn) {
                if (btn.classList.contains('active')) set.add(btn.getAttribute('data-skin-filter'));
            });
            return set;
        }

        function applyFilter() {
            const q = (search ? search.value : '').trim().toLowerCase();
            const anims = activeAnimFilters();
            const skins = activeSkinFilters();
            let shown = 0;
            cards.forEach(function (c) {
                const matchName = !q || c.dataset.name.indexOf(q) !== -1;
                const matchAnim = anims.size === 0 || anims.has(c.dataset.anim || 'static');
                let matchSkin = true;
                if (skins.size > 0) {
                    const cardSkins = (c.dataset.skins || '').split(/\s+/).filter(Boolean);
                    // OR semantics: card matches if it has ANY of the selected skins
                    matchSkin = cardSkins.some(function (s) { return skins.has(s); });
                }
                const visible = matchName && matchAnim && matchSkin;
                c.style.display = visible ? '' : 'none';
                if (visible) shown += 1;
            });
            if (visibleCount) visibleCount.textContent = shown;
        }

        sortButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                sortButtons.forEach(function (b) { b.classList.remove('active'); });
                btn.classList.add('active');
                applySort(btn.getAttribute('data-sort'));
            });
        });

        filterButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                const on = !btn.classList.contains('active');
                btn.classList.toggle('active', on);
                btn.setAttribute('aria-pressed', on ? 'true' : 'false');
                applyFilter();
            });
        });

        skinFilterButtons.forEach(function (btn) {
            btn.addEventListener('click', function () {
                const on = !btn.classList.contains('active');
                btn.classList.toggle('active', on);
                btn.setAttribute('aria-pressed', on ? 'true' : 'false');
                applyFilter();
            });
        });

        if (skinFilterClear) {
            skinFilterClear.addEventListener('click', function () {
                skinFilterButtons.forEach(function (btn) {
                    btn.classList.remove('active');
                    btn.setAttribute('aria-pressed', 'false');
                });
                applyFilter();
            });
        }

        if (search) {
            search.addEventListener('input', applyFilter);
        }

        // Default sort = dex-asc (already rendered in dex order; this is a no-op if so)
        applySort('dex-asc');
    }

    // ---------- Section browse overlay (FAB → modal) ----------
    function initSectionOverlay() {
        const fab = document.querySelector('.section-fab');
        const overlay = document.querySelector('.section-overlay');
        if (!fab || !overlay) return;
        const search = overlay.querySelector('.section-overlay-search');
        const list = overlay.querySelector('.section-overlay-list');
        const closers = overlay.querySelectorAll('[data-overlay-close]');
        if (!search || !list) return;

        const items = Array.from(list.querySelectorAll('li'));
        const empty = document.createElement('li');
        empty.className = 'section-overlay-empty';
        empty.textContent = 'No matches.';
        empty.hidden = true;
        list.appendChild(empty);

        function open() {
            overlay.removeAttribute('hidden');
            search.value = '';
            items.forEach(function (li) { li.hidden = false; });
            empty.hidden = true;
            setTimeout(function () { search.focus(); }, 0);
            document.addEventListener('keydown', onKey, true);
            const active = list.querySelector('a.active');
            if (active) setTimeout(function () { active.scrollIntoView({ block: 'center' }); }, 10);
        }
        function close() {
            overlay.setAttribute('hidden', '');
            document.removeEventListener('keydown', onKey, true);
            fab.focus();
        }
        function onKey(e) {
            if (e.key === 'Escape') close();
        }

        fab.addEventListener('click', open);
        closers.forEach(function (el) { el.addEventListener('click', close); });

        // Global "/" shortcut to summon the overlay (only when not typing in another field)
        document.addEventListener('keydown', function (e) {
            if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
            const t = e.target;
            const isTyping = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.isContentEditable);
            if (isTyping) return;
            e.preventDefault();
            open();
        });

        search.addEventListener('input', function () {
            const q = search.value.trim().toLowerCase();
            let shown = 0;
            items.forEach(function (li) {
                const a = li.querySelector('a');
                const name = a ? a.dataset.name || a.textContent.trim().toLowerCase() : '';
                const match = !q || name.indexOf(q) !== -1;
                li.hidden = !match;
                if (match) shown += 1;
            });
            empty.hidden = shown !== 0;
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            initFormTabs();
            initDexList();
            initSectionOverlay();
            initGymTabs();
            initQuestSubtabs();
        });
    } else {
        initFormTabs();
        initDexList();
        initSectionOverlay();
        initGymTabs();
        initQuestSubtabs();
    }

    // ---------- Gym card tabs (Team / Counters) ----------
    // Each `.gym-card` on the gym-teams page hosts its own tab strip — we
    // scope queries to the card so cards don't fight over each other's
    // active state. Mirrors the form-tab pattern but per-card-scoped.
    function initGymTabs() {
        document.querySelectorAll('.gym-card').forEach(function (card) {
            const tabs = card.querySelectorAll('.gym-tab');
            const panels = card.querySelectorAll('.gym-panel');
            if (!tabs.length) return;
            tabs.forEach(function (tab) {
                tab.addEventListener('click', function () {
                    const target = tab.getAttribute('data-gym-tab');
                    tabs.forEach(function (t) {
                        const active = t.getAttribute('data-gym-tab') === target;
                        t.classList.toggle('active', active);
                        t.setAttribute('aria-selected', active ? 'true' : 'false');
                    });
                    panels.forEach(function (p) {
                        const active = p.getAttribute('data-gym-tab') === target;
                        p.classList.toggle('active', active);
                        if (active) p.removeAttribute('hidden'); else p.setAttribute('hidden', '');
                    });
                });
            });
        });
    }

    // ---------- Main Quests vs Side Quests sub-tabs (Quests page) ----------
    function initQuestSubtabs() {
        document.querySelectorAll('.quest-subtabs').forEach(function (nav) {
            var panel = nav.parentElement;
            var buttons = nav.querySelectorAll('.quest-subtab');
            buttons.forEach(function (btn) {
                btn.addEventListener('click', function () {
                    var cat = btn.dataset.questCat;
                    buttons.forEach(function (b) {
                        var on = b === btn;
                        b.classList.toggle('active', on);
                        b.setAttribute('aria-selected', on ? 'true' : 'false');
                    });
                    panel.querySelectorAll('.quest-subpanel').forEach(function (p) {
                        var on = p.dataset.questCat === cat;
                        p.classList.toggle('active', on);
                        if (on) p.removeAttribute('hidden');
                        else p.setAttribute('hidden', '');
                    });
                });
            });
        });
    }
})();
