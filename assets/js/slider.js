/* ==========================================================================
   KIARIT — slider.js
   Accessible, swipeable, autoplaying testimonial slider. No dependencies.
   Usage: <div class="slider" data-slider data-autoplay="5500">
   ========================================================================== */
(function () {
  'use strict';

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function initSlider(root) {
    var track  = root.querySelector('.slider__track');
    var slides = Array.prototype.slice.call(root.querySelectorAll('.slider__slide'));
    var prev   = root.querySelector('[data-slider-prev]');
    var next   = root.querySelector('[data-slider-next]');
    var dotsWrap = root.querySelector('.slider__dots');
    if (!track || slides.length === 0) return;

    var index = 0;
    var perView = 1;
    var timer = null;
    var autoplayMs = parseInt(root.dataset.autoplay, 10) || 0;

    function computePerView() {
      var w = window.innerWidth;
      var pv = 1;
      if (root.dataset.perView3 && w >= 1100) pv = 3;
      else if (root.dataset.perView2 && w >= 720) pv = 2;
      return pv;
    }

    function maxIndex() { return Math.max(0, slides.length - perView); }

    function layout() {
      perView = computePerView();
      slides.forEach(function (s) { s.style.flexBasis = (100 / perView) + '%'; });
      if (index > maxIndex()) index = maxIndex();
      apply();
      buildDots();
    }

    function apply() {
      track.style.transform = 'translate3d(' + (-index * (100 / perView)) + '%,0,0)';
      slides.forEach(function (s, i) {
        var active = i >= index && i < index + perView;
        s.classList.toggle('is-active', active);
        s.setAttribute('aria-hidden', String(!active));
        s.querySelectorAll('a,button').forEach(function (f) {
          f.tabIndex = active ? 0 : -1;
        });
      });
      if (dotsWrap) {
        dotsWrap.querySelectorAll('.slider__dot').forEach(function (d, i) {
          var on = i === index;
          d.classList.toggle('is-active', on);
          d.setAttribute('aria-selected', String(on));
        });
      }
      if (prev) prev.disabled = false;
      if (next) next.disabled = false;
    }

    function buildDots() {
      if (!dotsWrap) return;
      var count = maxIndex() + 1;
      if (dotsWrap.children.length === count) { apply(); return; }
      dotsWrap.innerHTML = '';
      for (var i = 0; i < count; i++) {
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'slider__dot';
        b.setAttribute('role', 'tab');
        b.setAttribute('aria-label', 'Go to testimonial ' + (i + 1));
        (function (n) {
          b.addEventListener('click', function () { go(n); restart(); });
        })(i);
        dotsWrap.appendChild(b);
      }
      apply();
    }

    function go(n) {
      var m = maxIndex();
      index = n < 0 ? m : (n > m ? 0 : n);
      apply();
    }

    function start() {
      if (!autoplayMs || reduce) return;
      stop();
      timer = setInterval(function () { go(index + 1); }, autoplayMs);
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function restart() { stop(); start(); }

    if (prev) prev.addEventListener('click', function () { go(index - 1); restart(); });
    if (next) next.addEventListener('click', function () { go(index + 1); restart(); });

    root.addEventListener('mouseenter', stop);
    root.addEventListener('mouseleave', start);
    root.addEventListener('focusin', stop);
    root.addEventListener('focusout', start);

    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft')  { go(index - 1); restart(); }
      if (e.key === 'ArrowRight') { go(index + 1); restart(); }
    });

    /* Touch / drag swipe */
    var startX = 0, startY = 0, dragging = false, locked = false;
    var vp = root.querySelector('.slider__viewport') || root;

    vp.addEventListener('touchstart', function (e) {
      startX = e.touches[0].clientX; startY = e.touches[0].clientY;
      dragging = true; locked = false; stop();
    }, { passive: true });

    vp.addEventListener('touchmove', function (e) {
      if (!dragging) return;
      var dx = e.touches[0].clientX - startX;
      var dy = e.touches[0].clientY - startY;
      if (!locked && Math.abs(dx) > Math.abs(dy) + 4) locked = true;
      if (locked) {
        track.style.transition = 'none';
        track.style.transform = 'translate3d(calc(' + (-index * (100 / perView)) + '% + ' + dx + 'px),0,0)';
      }
    }, { passive: true });

    vp.addEventListener('touchend', function (e) {
      if (!dragging) return;
      dragging = false;
      track.style.transition = '';
      var dx = e.changedTouches[0].clientX - startX;
      if (Math.abs(dx) > 48) go(index + (dx < 0 ? 1 : -1));
      else apply();
      start();
    });

    window.addEventListener('resize', layout, { passive: true });

    // Pause when off-screen (battery + perf)
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (en) { en.isIntersecting ? start() : stop(); });
      }, { threshold: 0.25 }).observe(root);
    }

    layout();
    start();
  }

  document.querySelectorAll('[data-slider]').forEach(initSlider);
})();
