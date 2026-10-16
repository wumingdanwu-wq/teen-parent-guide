(() => {
  'use strict';
  document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
  document.querySelectorAll('[data-copy-prompt]').forEach(button => button.addEventListener('click', async () => {
    const panel = button.closest('.practice-box');
    const field = panel.querySelector('.ai-prompt');
    const status = panel.querySelector('.copy-status');
    try {
      await navigator.clipboard.writeText(field.value);
      status.textContent = '已复制，可以粘贴到你的 AI 对话中。';
    } catch {
      field.focus(); field.select();
      status.textContent = '已选中模板，请按 Ctrl+C（Mac 按 ⌘C）复制。';
    }
  }));
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
    document.querySelector('#result-count').textContent = `找到 ${count} 篇资料`;
    document.querySelector('#empty').hidden = count !== 0;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
  }
  input.addEventListener('input', update);
  document.querySelector('#search-form')?.addEventListener('submit', event => {
    event.preventDefault();
    update();
    const results = document.querySelector('#result-count');
    results.focus({ preventScroll: true });
    results.scrollIntoView({ block: 'nearest' });
  });
  buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; update(); }));
  document.querySelector('#reset').addEventListener('click', () => { input.value = ''; category = '全部事件'; update(); input.focus(); });
})();
