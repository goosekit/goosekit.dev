(function () {
  var HEADER_ID = 'gk-global-header';
  var STYLE_ID = 'gk-global-header-style';

  var navLinks = [
    ['Tools', '/tools/'],
    ['Developers', '/tools/for-developers/'],
    ['Designers', '/tools/for-designers/'],
    ['Students', '/tools/for-students/'],
    ['Compare', '/compare/'],
    ['Blog', '/blog/'],
    ['Offline Pack', '/offline-pack/']
  ];

  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = '' +
      '.gk-global-header{position:sticky;top:0;z-index:10000;width:100%;background:rgba(10,10,26,.88);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,.08);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}' +
      '.gk-global-header *{box-sizing:border-box}' +
      '.gk-global-header__inner{width:100%;min-height:56px;padding:8px 16px 8px 10px;display:flex;align-items:center;justify-content:space-between;gap:14px}' +
      '.gk-global-header__brand{display:inline-flex;align-items:center;text-decoration:none;flex-shrink:0;margin-right:10px}' +
      '.gk-global-header__brand img{width:100px;height:auto;display:block}' +
      '.gk-global-header__nav{display:flex;align-items:center;justify-content:flex-end;gap:4px;flex:1;min-width:0}' +
      '.gk-global-header__nav a{color:#cbd5e1;text-decoration:none;font-size:.9rem;font-weight:600;padding:8px 10px;border-radius:10px;white-space:nowrap;transition:background .16s ease,color .16s ease,transform .16s ease}' +
      '.gk-global-header__nav a:hover{color:#fff;background:rgba(255,255,255,.07);transform:translateY(-1px)}' +
      '.gk-global-header__cta{margin-left:4px!important;background:linear-gradient(135deg,#ff4800,#fb923c)!important;color:#fff!important;font-weight:800!important;box-shadow:0 10px 24px rgba(255,72,0,.22)}' +
      '.gk-global-header__toggle{display:none;align-items:center;justify-content:center;flex-direction:column;gap:4px;width:44px;height:44px;margin-left:auto;border:1px solid rgba(255,255,255,.10);border-radius:12px;background:rgba(15,23,42,.92);color:#e2e8f0;cursor:pointer;-webkit-tap-highlight-color:transparent}' +
      '.gk-global-header__toggle span{display:block;width:18px;height:2px;border-radius:999px;background:currentColor}' +
      '@media (max-width:900px){.gk-global-header__inner{padding:8px 12px}.gk-global-header__brand img{width:98px}.gk-global-header__toggle{display:flex}.gk-global-header__nav{position:absolute;left:10px;right:10px;top:calc(100% + 8px);display:none;flex-direction:column;align-items:stretch;gap:4px;padding:10px;border:1px solid rgba(255,255,255,.10);border-radius:16px;background:rgba(10,10,26,.98);box-shadow:0 20px 40px rgba(0,0,0,.32)}.gk-global-header__nav.is-open{display:flex}.gk-global-header__nav a{width:100%;padding:11px 12px}.gk-global-header__cta{margin-left:0!important;text-align:center}}';
    document.head.appendChild(style);
  }

  function shouldRemoveExistingHeader(el) {
    if (!el || el.id === HEADER_ID) return false;
    if (el.classList && el.classList.contains('site-header')) return true;
    if (el.querySelector && el.querySelector('.site-brand')) return true;
    if (el.querySelector && el.querySelector('.site-menu-toggle')) return true;
    if (el.querySelector && el.querySelector('.site-nav')) return true;
    if (el.querySelector && el.querySelector('.topbar')) return true;
    if (el.querySelector && el.querySelector('.brand') && el.querySelector('.nav-cta')) return true;
    if (el.querySelector && el.querySelector('.brand') && el.querySelector('nav')) return true;
    return false;
  }

  function removeOldHeaders() {
    var candidates = Array.prototype.slice.call(document.querySelectorAll('header'));
    candidates.forEach(function (header) {
      if (shouldRemoveExistingHeader(header)) header.remove();
    });
  }

  function buildHeader() {
    var header = document.createElement('header');
    header.id = HEADER_ID;
    header.className = 'gk-global-header';
    header.innerHTML = '' +
      '<div class="gk-global-header__inner">' +
        '<a class="gk-global-header__brand" href="/" aria-label="Goosekit home"><img src="/brand/logo-dark.png" alt="Goosekit"></a>' +
        '<button class="gk-global-header__toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="gk-global-header-nav"><span></span><span></span><span></span></button>' +
        '<nav class="gk-global-header__nav" id="gk-global-header-nav" aria-label="Main navigation">' +
          navLinks.map(function (link) { return '<a href="' + link[1] + '">' + link[0] + '</a>'; }).join('') +
          '<a class="gk-global-header__cta" href="/ship-it-kit/">Ship It Kit</a>' +
        '</nav>' +
      '</div>';
    return header;
  }

  function setupMobile(header) {
    var toggle = header.querySelector('.gk-global-header__toggle');
    var nav = header.querySelector('.gk-global-header__nav');
    if (!toggle || !nav) return;
    var mq = window.matchMedia('(max-width: 900px)');

    function closeMenu() {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    }

    function openMenu() {
      toggle.setAttribute('aria-expanded', 'true');
      nav.classList.add('is-open');
    }

    function isOpen() { return nav.classList.contains('is-open'); }

    toggle.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopPropagation();
      if (isOpen()) closeMenu();
      else openMenu();
    });

    nav.addEventListener('click', function (event) { event.stopPropagation(); });
    document.addEventListener('click', function (event) {
      if (!mq.matches || !isOpen()) return;
      if (!header.contains(event.target)) closeMenu();
    });
    document.addEventListener('keydown', function (event) { if (event.key === 'Escape') closeMenu(); });

    function handleViewportChange() { if (!mq.matches) closeMenu(); }
    if (typeof mq.addEventListener === 'function') mq.addEventListener('change', handleViewportChange);
    else if (typeof mq.addListener === 'function') mq.addListener(handleViewportChange);
  }

  function init() {
    if (!document.body) return;
    injectStyles();
    removeOldHeaders();
    var existing = document.getElementById(HEADER_ID);
    var header = existing || buildHeader();
    if (!existing) document.body.insertBefore(header, document.body.firstChild);
    setupMobile(header);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
