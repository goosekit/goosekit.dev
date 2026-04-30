(function () {
  var HEADER_ID = 'gk-global-header';
  var STYLE_ID = 'gk-homepage-header-style';

  var navLinks = [
    ['Tools', '/tools/'],
    ['Developers', '/tools/for-developers/'],
    ['Designers', '/tools/for-designers/'],
    ['Students', '/tools/for-students/'],
    ['Compare', '/compare/'],
    ['Blog', '/blog/'],
    ['Offline Pack', '/offline-pack/?ref=global_nav'],
    ['API', '/api/'],
    ['Extension', 'https://chromewebstore.google.com/detail/maodnbppejkbnmjkcohhapmoajedkend'],
  ];

  function injectStyles() {
    if (document.getElementById(STYLE_ID)) return;
    var style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = '' +
      'html,body{margin-top:0!important;}' +
      'body{margin-left:0!important;margin-right:0!important;}' +
      '.site-header{position:sticky;top:0;z-index:10000;background:rgba(10,10,26,0.78);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border-bottom:1px solid rgba(255,255,255,0.06);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;margin:0!important;width:100%;}' +
      '.site-header *{box-sizing:border-box;}' +
      '.site-header-inner{width:100%;margin:0;padding:8px 16px 8px 10px;display:flex;align-items:center;justify-content:space-between;gap:14px;}' +
      '.site-brand{display:inline-flex;align-items:center;text-decoration:none;flex-shrink:0;margin-right:10px;}' +
      '.site-brand img{width:100px;height:auto;display:block;}' +
      '.site-nav{display:flex;align-items:center;justify-content:flex-end;flex-wrap:wrap;flex:1;gap:8px 14px;}' +
      '.site-nav a{color:var(--text-muted,#94a3b8);text-decoration:none;font-size:0.9rem;font-weight:600;line-height:1;transition:color .18s ease,background .18s ease,border-color .18s ease;}' +
      '.site-nav a:hover{color:var(--text,#f8fafc);}' +
      '.site-nav .nav-cta{color:#fff;background:rgba(255,72,0,0.95);border:1px solid rgba(255,72,0,0.9);padding:8px 12px;border-radius:11px;box-shadow:0 8px 22px rgba(255,72,0,0.16);}' +
      '.site-nav .nav-cta:hover{color:#fff;background:#ff4800;border-color:#ff4800;}' +
      '.site-menu-toggle{display:none;align-items:center;justify-content:center;flex-direction:column;gap:4px;width:44px;height:44px;margin-left:auto;border:1px solid rgba(255,255,255,0.08);border-radius:12px;background:rgba(15,23,42,0.92);color:#e2e8f0;cursor:pointer;-webkit-tap-highlight-color:transparent;}' +
      '.site-menu-toggle span{display:block;width:18px;height:2px;border-radius:999px;background:currentColor;}' +
      '@media (max-width:900px){.site-header-inner{padding:8px 12px;}.site-brand img{width:98px;}.site-menu-toggle{display:flex;}.site-nav{position:absolute;left:10px;right:10px;top:calc(100% + 8px);display:none;flex-direction:column;align-items:stretch;gap:4px;padding:10px;border:1px solid rgba(255,255,255,0.10);border-radius:16px;background:rgba(10,10,26,0.98);box-shadow:0 20px 40px rgba(0,0,0,0.32);}.site-nav.is-open{display:flex;}.site-nav a{width:100%;padding:11px 12px;}.site-nav .nav-cta{margin-left:0;text-align:center;}}';
    document.head.appendChild(style);
  }

  function isGlobalHeader(el) {
    return el && el.id === HEADER_ID;
  }

  function shouldRemoveExistingHeader(el) {
    if (!el || isGlobalHeader(el)) return false;
    if (el.classList && el.classList.contains('hero')) return false;
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
    Array.prototype.slice.call(document.querySelectorAll('header')).forEach(function (header) {
      if (shouldRemoveExistingHeader(header)) header.remove();
    });
  }

  function buildHeader() {
    var header = document.createElement('header');
    header.id = HEADER_ID;
    header.className = 'site-header';
    header.innerHTML = '' +
      '<div class="site-header-inner">' +
        '<a class="site-brand" href="/" aria-label="Goosekit home"><img src="/logo-dark.png" alt="Goosekit"></a>' +
        '<button class="site-menu-toggle" type="button" aria-label="Open navigation menu" aria-controls="site-navigation" aria-expanded="false"><span></span><span></span><span></span></button>' +
        '<nav class="site-nav" id="site-navigation" aria-label="Primary navigation">' +
          navLinks.map(function (link) {
            var external = link[1].indexOf('http') === 0;
            return '<a href="' + link[1] + '"' + (external ? ' target="_blank" rel="noopener"' : '') + '>' + link[0] + '</a>';
          }).join('') +
          '<a class="nav-cta" href="/go/ship-it-kit/home-nav/">Ship It Kit</a>' +
        '</nav>' +
      '</div>';
    return header;
  }

  function setupMobile(header) {
    var toggle = header.querySelector('.site-menu-toggle');
    var nav = header.querySelector('.site-nav');
    if (!toggle || !nav || nav.dataset.mobileHeaderBound === 'true') return;
    nav.dataset.mobileHeaderBound = 'true';
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
