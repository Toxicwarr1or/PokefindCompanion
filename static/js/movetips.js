// Hover tooltips for move/ability links across the site.
// Loads /movetips.json once, attaches a single shared tooltip element,
// and shows the move/ability description when hovering any .movelink.

(function () {
  let tips = null;
  let loadPromise = null;
  let tipEl = null;
  let activeLink = null;

  function loadTips() {
    if (loadPromise) return loadPromise;
    loadPromise = fetch(new URL('/movetips.json', document.baseURI).href, { credentials: 'same-origin' })
      .then((r) => (r.ok ? r.json() : {}))
      .then((data) => { tips = data; })
      .catch(() => { tips = {}; });
    return loadPromise;
  }

  function ensureTipEl() {
    if (tipEl) return tipEl;
    tipEl = document.createElement('div');
    tipEl.className = 'movetip';
    tipEl.setAttribute('role', 'tooltip');
    tipEl.hidden = true;
    document.body.appendChild(tipEl);
    return tipEl;
  }

  function slugFromHref(href) {
    try {
      const u = new URL(href, document.baseURI);
      // /moves/<slug>/  → <slug>
      const m = u.pathname.match(/\/moves\/([^/]+)\/?$/);
      return m ? m[1] : null;
    } catch (_) { return null; }
  }

  function showTipFor(link) {
    const slug = slugFromHref(link.getAttribute('href') || '');
    if (!slug || !tips) return;
    const entry = tips[slug];
    if (!entry) return;
    const tip = ensureTipEl();
    const kindLabel = entry.k === 'ability' ? 'Ability' : 'Move';
    tip.innerHTML =
      '<div class="movetip-head"><span class="movetip-name"></span>' +
      '<span class="movetip-kind"></span></div>' +
      '<div class="movetip-body"></div>';
    tip.querySelector('.movetip-name').textContent = entry.n || slug;
    tip.querySelector('.movetip-kind').textContent = kindLabel;
    tip.querySelector('.movetip-body').textContent = entry.e || '';
    positionTip(tip, link);
    tip.hidden = false;
  }

  function positionTip(tip, anchor) {
    const r = anchor.getBoundingClientRect();
    tip.style.left = '0px';
    tip.style.top = '0px';
    tip.hidden = false;
    const tw = tip.offsetWidth;
    const th = tip.offsetHeight;
    const margin = 8;
    let left = r.left + window.scrollX + (r.width / 2) - (tw / 2);
    let top = r.bottom + window.scrollY + margin;
    // Keep within viewport horizontally
    const maxLeft = window.scrollX + document.documentElement.clientWidth - tw - margin;
    if (left > maxLeft) left = maxLeft;
    if (left < window.scrollX + margin) left = window.scrollX + margin;
    // Flip above if it would go off-screen below
    if (r.bottom + th + margin > document.documentElement.clientHeight) {
      top = r.top + window.scrollY - th - margin;
      tip.classList.add('above');
    } else {
      tip.classList.remove('above');
    }
    tip.style.left = left + 'px';
    tip.style.top = top + 'px';
  }

  function hideTip() {
    if (tipEl) tipEl.hidden = true;
    activeLink = null;
  }

  function onEnter(e) {
    const link = e.target.closest('a.movelink');
    if (!link) return;
    if (!slugFromHref(link.getAttribute('href') || '')) return;
    activeLink = link;
    loadTips().then(() => {
      if (activeLink === link) showTipFor(link);
    });
  }
  function onLeave(e) {
    const link = e.target.closest('a.movelink');
    if (!link) return;
    hideTip();
  }

  document.addEventListener('mouseover', onEnter, true);
  document.addEventListener('mouseout', onLeave, true);
  document.addEventListener('focusin', onEnter, true);
  document.addEventListener('focusout', onLeave, true);
  window.addEventListener('scroll', hideTip, { passive: true });
})();
