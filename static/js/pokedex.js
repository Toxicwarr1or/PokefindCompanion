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

    // ---------- Pokedex list sort + search ----------
    function initDexList() {
        const grid = document.getElementById('dex-grid');
        if (!grid) return;
        const cards = Array.from(grid.querySelectorAll('.dex-card'));
        const sortButtons = document.querySelectorAll('.dex-sort button');
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

        function applyFilter(query) {
            const q = (query || '').trim().toLowerCase();
            let shown = 0;
            cards.forEach(function (c) {
                const match = !q || c.dataset.name.indexOf(q) !== -1;
                c.style.display = match ? '' : 'none';
                if (match) shown += 1;
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

        if (search) {
            search.addEventListener('input', function () { applyFilter(search.value); });
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
        });
    } else {
        initFormTabs();
        initDexList();
        initSectionOverlay();
    }
})();
