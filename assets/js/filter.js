/* KIARIT — product category filter (progressive enhancement) */
(function () {
  'use strict';
  var chips = document.querySelectorAll('.chip[data-filter]');
  var grid = document.getElementById('grid');
  if (!chips.length || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll('[data-cat]'));
  var empty = document.querySelector('.chips__empty');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function apply(filter) {
    var shown = 0;
    cards.forEach(function (card) {
      var match = filter === 'all' || card.getAttribute('data-cat') === filter;
      if (match) shown++;
      if (reduce) {
        card.hidden = !match;
        return;
      }
      if (match) {
        card.hidden = false;
        card.classList.remove('is-filtered');
      } else {
        card.classList.add('is-filtered');
        window.setTimeout(function () {
          if (card.classList.contains('is-filtered')) card.hidden = true;
        }, 260);
      }
    });
    if (empty) empty.hidden = shown !== 0;
  }

  chips.forEach(function (chip) {
    chip.addEventListener('click', function () {
      chips.forEach(function (c) {
        c.classList.remove('is-active');
        c.setAttribute('aria-pressed', 'false');
      });
      chip.classList.add('is-active');
      chip.setAttribute('aria-pressed', 'true');
      apply(chip.getAttribute('data-filter'));
    });
    chip.setAttribute('aria-pressed', chip.classList.contains('is-active') ? 'true' : 'false');
  });
})();
