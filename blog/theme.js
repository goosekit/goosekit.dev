(() => {
  const root = document.documentElement;
  const storageKey = 'goosekit-theme';

  const getPreferredTheme = () => {
    const saved = localStorage.getItem(storageKey);
    if (saved === 'light' || saved === 'dark') return saved;
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  };

  const applyTheme = (theme) => {
    root.setAttribute('data-theme', theme);
    const toggle = document.getElementById('darkModeToggle');
    if (toggle) toggle.textContent = theme === 'dark' ? '☀️' : '🌙';
  };

  const nextTheme = () => (root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');

  document.addEventListener('DOMContentLoaded', () => {
    applyTheme(getPreferredTheme());

    const toggle = document.getElementById('darkModeToggle');
    if (toggle) {
      toggle.addEventListener('click', () => {
        const theme = nextTheme();
        localStorage.setItem(storageKey, theme);
        applyTheme(theme);
      });
    }
  });
})();
