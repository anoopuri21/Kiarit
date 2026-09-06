/* ==========================================================================
   KIARIT — reveal.js
   Cinematic scroll system: IntersectionObserver reveals, staggering,
   parallax and counters. Zero dependencies.
   ========================================================================== */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. REVEAL OBSERVER ---------- */
  var revealEls = document.querySelectorAll('[data-reveal]');

  if (reduce || !('IntersectionObserver' in window)) {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  } else {
    // Apply stagger delays declared via data-stagger on a parent
    document.querySelectorAll('[data-stagger]').forEach(function (parent) {
      var step = parseInt(parent.dataset.stagger, 10) || 60;
      var kids = parent.querySelectorAll(':scope > [data-reveal]');
      kids.forEach(function (k, i) {
        if (!k.style.getPropertyValue('--reveal-delay')) {
          k.style.setProperty('--reveal-delay', (i * step) + 'ms');
        }
      });
    });
    // Individual delays
    document.querySelectorAll('[data-delay]').forEach(function (el) {
      el.style.setProperty('--reveal-delay', el.dataset.delay + 'ms');
    });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          if (e.target.dataset.revealOnce !== 'false') io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

    revealEls.forEach(function (el) { io.observe(el); });

    // Safety net: anything still hidden after load + 2.5s is force-revealed,
    // so a missed intersection (clipped/transformed targets, odd layouts)
    // can never leave real content — e.g. product images — invisible.
    // Only elements currently inside the viewport are touched, so below-the-
    // fold content still animates in on scroll as designed.
    function revealStuckInView() {
      var vh = window.innerHeight || document.documentElement.clientHeight;
      revealEls.forEach(function (el) {
        if (el.classList.contains('is-visible')) return;
        var r = el.getBoundingClientRect();
        if (r.bottom > 0 && r.top < vh) {
          el.classList.add('is-visible');
          io.unobserve(el);
        }
      });
    }
    window.addEventListener('load', function () { setTimeout(revealStuckInView, 2500); });
  }

  /* ---------- 2. COUNTERS ---------- */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target;
        cio.unobserve(el);
        if (reduce) { el.textContent = el.dataset.count; return; }
        var target = parseFloat(el.dataset.count);
        var dur = parseInt(el.dataset.countDur, 10) || 1700;
        var dec = (el.dataset.count.split('.')[1] || '').length;
        var start = null;
        function step(ts) {
          if (!start) start = ts;
          var p = Math.min((ts - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = (target * eased).toFixed(dec);
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      });
    }, { threshold: 0.5 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  /* ---------- 3. PARALLAX (rAF-throttled) ---------- */
  var pxEls = Array.prototype.slice.call(document.querySelectorAll('[data-parallax]'));
  if (pxEls.length && !reduce) {
    var ticking = false;
    var vh = window.innerHeight;

    function updateParallax() {
      pxEls.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var speed = parseFloat(el.dataset.parallax) || 0.15;
        // progress: -1 (below viewport) .. 1 (above viewport)
        var progress = (r.top + r.height / 2 - vh / 2) / (vh / 2 + r.height / 2);
        var y = progress * speed * 100;
        var scale = el.dataset.parallaxScale ? parseFloat(el.dataset.parallaxScale) : 1;
        el.style.transform = 'translate3d(0,' + y.toFixed(2) + 'px,0)' + (scale !== 1 ? ' scale(' + scale + ')' : '');
      });
      ticking = false;
    }
    function onScroll() {
      if (!ticking) { requestAnimationFrame(updateParallax); ticking = true; }
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', function () { vh = window.innerHeight; onScroll(); }, { passive: true });
    updateParallax();
  }

  /* ---------- 4. HERO KEN-BURNS TRIGGER ---------- */
  var hero = document.querySelector('[data-hero]');
  if (hero) {
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { hero.classList.add('is-ready'); });
    });
  }
})();
