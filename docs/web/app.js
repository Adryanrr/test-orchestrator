// --- Tema dark/light ---
const toggle = document.getElementById('theme-toggle');

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  toggle.textContent = theme === 'light' ? '🌙' : '☀️';
  toggle.setAttribute('aria-label', theme === 'light' ? 'Alternar para tema escuro' : 'Alternar para tema claro');
  localStorage.setItem('theme', theme);
}

setTheme(localStorage.getItem('theme') || 'dark');
toggle.addEventListener('click', () => {
  const current = document.documentElement.getAttribute('data-theme');
  setTheme(current === 'dark' ? 'light' : 'dark');
});

// --- Scroll-spy sidebar ---
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('#sidebar a');

const spy = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    navLinks.forEach(l => l.classList.remove('active'));
    const link = document.querySelector(`#sidebar a[href="#${entry.target.id}"]`);
    if (link) link.classList.add('active');
  });
}, { rootMargin: '-15% 0px -70% 0px' });

sections.forEach(s => spy.observe(s));

// --- Botões de copiar ---
document.querySelectorAll('pre').forEach(pre => {
  const btn = document.createElement('button');
  btn.className = 'copy-btn';
  btn.textContent = 'Copiar';
  btn.addEventListener('click', () => {
    const codeEl = pre.querySelector('code');
    const text = codeEl ? codeEl.textContent : pre.textContent;
    const reset = () => setTimeout(() => { btn.textContent = 'Copiar'; }, 2000);
    if (!navigator.clipboard) {
      const ta = document.createElement('textarea');
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); btn.textContent = 'Copiado!'; } catch { btn.textContent = 'Erro!'; }
      document.body.removeChild(ta); reset(); return;
    }
    navigator.clipboard.writeText(text)
      .then(() => { btn.textContent = 'Copiado!'; reset(); })
      .catch(() => { btn.textContent = 'Erro!'; reset(); });
  });
  pre.appendChild(btn);
});
