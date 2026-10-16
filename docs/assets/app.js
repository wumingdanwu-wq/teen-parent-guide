(() => {
  'use strict';
  document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
  const input = document.querySelector('#search');
  if (!input) return;
  const cards = [...document.querySelectorAll('.event-card')];
  const buttons = [...document.querySelectorAll('[data-filter]')];
  let category = '全部事件';
  function update() {
    const terms = input.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let count = 0;
    for (const card of cards) {
      const matches = (category === '全部事件' || card.dataset.category === category) && terms.every(term => card.dataset.search.toLocaleLowerCase().includes(term));
      card.hidden = !matches;
      if (matches) count++;
    }
    document.querySelector('#result-count').textContent = `找到 ${count} 个事件`;
    document.querySelector('#empty').hidden = count !== 0;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
  }
  input.addEventListener('input', update);
  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; update(); }));
  document.querySelector('#reset').addEventListener('click', () => { input.value = ''; category = '全部事件'; update(); input.focus(); });
})();
