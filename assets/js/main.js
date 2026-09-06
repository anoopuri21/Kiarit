/* ==========================================================================
   KIARIT — main.js
   Header behaviour, mobile nav, products dropdown, floating buttons,
   scroll progress, current-year, lazy video.
   ========================================================================== */
(function () {
  'use strict';

  var header  = document.querySelector('.site-header');
  var nav     = document.querySelector('.nav');
  var menu    = document.getElementById('navMenu');
  var burger  = document.querySelector('.burger');
  var overlay = document.querySelector('.nav-overlay');
  var progress= document.querySelector('.nav__progress');
  var topBtn  = document.querySelector('.float-btn--top');
  var ringFg  = document.querySelector('.float-btn__ring .fg');

  /* ---------- MOBILE MENU ---------- */
  function setMenu(open) {
    if (!menu || !burger) return;
    menu.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', String(open));
    if (overlay) overlay.classList.toggle('is-open', open);
    document.body.classList.toggle('no-scroll', open);
    if (open) {
      menu.querySelectorAll('.nav__item').forEach(function (it, i) {
        it.style.setProperty('--i', (60 + i * 70) + 'ms');
      });
    }
  }
  if (burger) burger.addEventListener('click', function () {
    setMenu(burger.getAttribute('aria-expanded') !== 'true');
  });
  if (overlay) overlay.addEventListener('click', function () { setMenu(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      setMenu(false);
      document.querySelectorAll('.nav__item.is-open').forEach(function (i) {
        i.classList.remove('is-open');
        var t = i.querySelector('[aria-expanded]');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
    }
  });

  /* ---------- PRODUCTS DROPDOWN (click on mobile, hover+keyboard on desktop) ---------- */
  document.querySelectorAll('.nav__item--has-dropdown').forEach(function (item) {
    var trigger = item.querySelector('.nav__link');
    if (!trigger) return;
    trigger.setAttribute('aria-expanded', 'false');

    trigger.addEventListener('click', function (e) {
      // On mobile the parent link acts purely as an accordion toggle
      if (window.innerWidth <= 1024) {
        e.preventDefault();
        var open = !item.classList.contains('is-open');
        item.classList.toggle('is-open', open);
        trigger.setAttribute('aria-expanded', String(open));
      }
    });
    // Desktop keyboard support
    trigger.addEventListener('keydown', function (e) {
      if (window.innerWidth > 1024 && (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowDown')) {
        e.preventDefault();
        var open = !item.classList.contains('is-open');
        item.classList.toggle('is-open', open);
        trigger.setAttribute('aria-expanded', String(open));
        if (open) { var f = item.querySelector('.dropdown a'); if (f) f.focus(); }
      }
    });
    item.addEventListener('focusout', function () {
      setTimeout(function () {
        if (!item.contains(document.activeElement) && window.innerWidth > 1024) {
          item.classList.remove('is-open');
          trigger.setAttribute('aria-expanded', 'false');
        }
      }, 10);
    });
  });

  document.addEventListener('click', function (e) {
    if (window.innerWidth > 1024 && !e.target.closest('.nav__item--has-dropdown')) {
      document.querySelectorAll('.nav__item.is-open').forEach(function (i) {
        i.classList.remove('is-open');
        var t = i.querySelector('[aria-expanded]');
        if (t) t.setAttribute('aria-expanded', 'false');
      });
    }
  });

  // Close mobile menu when a real link is tapped
  if (menu) menu.querySelectorAll('a[href]').forEach(function (a) {
    a.addEventListener('click', function () {
      if (window.innerWidth <= 1024) setMenu(false);
    });
  });

  window.addEventListener('resize', function () {
    if (window.innerWidth > 1024) {
      setMenu(false);
      document.querySelectorAll('.nav__item.is-open').forEach(function (i) { i.classList.remove('is-open'); });
    }
  });

  /* ---------- SCROLL: header state, progress ring, scroll-to-top ---------- */
  var lastY = window.scrollY;
  var RING_LEN = 150.8; // 2πr with r=24
  if (ringFg) {
    ringFg.style.strokeDasharray = RING_LEN;
    ringFg.style.strokeDashoffset = RING_LEN;
  }

  var raf = false;
  function onScroll() {
    if (raf) return;
    raf = true;
    requestAnimationFrame(function () {
      var y = window.scrollY;
      var docH = document.documentElement.scrollHeight - window.innerHeight;
      var pct = docH > 0 ? Math.min(y / docH, 1) : 0;

      if (header) {
        header.classList.toggle('is-scrolled', y > 12);
        // Hide the thin top bar after scrolling down past it
        header.classList.toggle('is-pinned', y > 140 && y > lastY);
      }
      if (progress) progress.style.transform = 'scaleX(' + pct + ')';
      if (topBtn) topBtn.classList.toggle('is-visible', y > 400);
      if (ringFg) ringFg.style.strokeDashoffset = String(RING_LEN * (1 - pct));

      lastY = y;
      raf = false;
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (topBtn) topBtn.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  });

  /* ---------- FOOTER YEAR ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- HERO VIDEO: guarantee autoplay / graceful fallback ---------- */
  var vid = document.querySelector('.hero__video');
  if (vid) {
    var motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

    vid.muted = true;
    vid.setAttribute('muted', '');
    vid.addEventListener('loadeddata', function () { vid.classList.add('is-loaded'); });
    if (vid.readyState >= 2) vid.classList.add('is-loaded');

    function startVideo() {
      var play = vid.play();
      if (play && play.catch) play.catch(function () { /* poster stays visible */ });
    }

    function applyMotionPreference() {
      if (motionQuery.matches) {
        /* Respect prefers-reduced-motion: freeze on the first frame so the
           hero still reads as a rich image without animating. */
        vid.pause();
        vid.removeAttribute('autoplay');
        try { vid.currentTime = 0; } catch (e) { /* not seekable yet */ }
      } else {
        startVideo();
      }
    }

    applyMotionPreference();
    if (motionQuery.addEventListener) {
      motionQuery.addEventListener('change', applyMotionPreference);
    } else if (motionQuery.addListener) {
      motionQuery.addListener(applyMotionPreference);
    }

    /* Pause while off-screen or on a hidden tab to save battery and data. */
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) vid.pause();
      else if (!motionQuery.matches) startVideo();
    });

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (motionQuery.matches) return;
          if (entry.isIntersecting) startVideo();
          else vid.pause();
        });
      }, { threshold: 0.15 }).observe(vid);
    }
  }

  /* ---------- MAGNETIC BUTTONS (desktop, fine pointer only) ---------- */
  if (window.matchMedia('(hover:hover) and (pointer:fine)').matches &&
      !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    document.querySelectorAll('[data-magnetic]').forEach(function (el) {
      el.addEventListener('mousemove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left - r.width / 2) * 0.18;
        var y = (e.clientY - r.top - r.height / 2) * 0.28;
        el.style.transform = 'translate(' + x.toFixed(1) + 'px,' + (y - 2).toFixed(1) + 'px)';
      });
      el.addEventListener('mouseleave', function () { el.style.transform = ''; });
    });
  }
})();
