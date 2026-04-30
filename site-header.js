(function () {
  var HEADER_ID = 'gk-global-header';
  var STYLE_ID = 'gk-homepage-header-style';
  var LEGACY_STYLE_IDS = ['gk-homepage-header-copy-styles'];

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
      'html,body{margin:0!important;padding-top:0!important;}' +
      'body{margin-left:0!important;margin-right:0!important;padding-left:0!important;padding-right:0!important;}' +
      '.site-header{position:sticky!important;top:0!important;z-index:10000!important;padding:0!important;text-align:left!important;background:rgba(10,10,26,0.78)!important;backdrop-filter:blur(14px)!important;-webkit-backdrop-filter:blur(14px)!important;border-bottom:1px solid rgba(255,255,255,0.06)!important;font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif!important;margin:0!important;width:100%!important;max-width:none!important;}' +
      '.site-header *{box-sizing:border-box;}' +
      '.site-header-inner{width:100%!important;max-width:none!important;margin:0!important;padding:8px 16px 8px 10px!important;display:flex!important;align-items:center!important;justify-content:space-between!important;gap:14px!important;position:relative!important;}' +
      '.site-brand{display:inline-flex!important;align-items:center!important;text-decoration:none!important;flex-shrink:0!important;margin:0 10px 0 0!important;padding:0!important;min-height:0!important;height:auto!important;line-height:1!important;}' +
      '.site-brand img{width:100px!important;height:auto!important;display:block!important;margin:0!important;}' +
      '.site-nav{display:flex!important;align-items:center!important;justify-content:flex-end!important;flex-wrap:wrap!important;flex:1 1 auto!important;gap:8px 14px!important;margin:0!important;padding:0!important;}' +
      '.site-nav a{color:var(--text-muted,#94a3b8)!important;text-decoration:none!important;font-size:0.9rem!important;font-weight:600!important;line-height:1!important;margin:0!important;transition:color .18s ease,background .18s ease,border-color .18s ease;}' +
      '.site-nav a:hover{color:var(--text,#f8fafc);}' +
      '.site-nav .nav-cta{display:inline-flex!important;align-items:center!important;justify-content:center!important;color:#fff!important;background:rgba(255,72,0,0.95)!important;border:1px solid rgba(255,72,0,0.9)!important;padding:8px 12px!important;border-radius:11px!important;box-shadow:0 8px 22px rgba(255,72,0,0.16)!important;}' +
      '.site-nav .nav-cta:hover{color:#fff;background:#ff4800;border-color:#ff4800;}' +
      '.site-menu-toggle{display:none!important;align-items:center!important;justify-content:center!important;flex-direction:column!important;gap:4px!important;width:44px!important;height:44px!important;min-width:44px!important;min-height:44px!important;margin-left:auto!important;padding:0!important;border:1px solid rgba(255,255,255,0.08)!important;border-radius:12px!important;background:rgba(15,23,42,0.92)!important;color:#e2e8f0!important;cursor:pointer!important;-webkit-tap-highlight-color:transparent!important;}' +
      '.site-menu-toggle span{display:block!important;width:18px!important;height:2px!important;border-radius:999px!important;background:currentColor!important;margin:0!important;padding:0!important;}' +
      '@media (max-width:900px){.site-header-inner{padding:8px 12px!important;}.site-brand img{width:98px!important;}.site-menu-toggle{display:flex!important;}.site-nav{position:absolute!important;left:10px!important;right:10px!important;top:calc(100% + 8px)!important;display:none!important;flex-direction:column!important;align-items:stretch!important;gap:4px!important;padding:10px!important;border:1px solid rgba(255,255,255,0.10)!important;border-radius:16px!important;background:rgba(10,10,26,0.98)!important;box-shadow:0 20px 40px rgba(0,0,0,0.32)!important;}.site-nav.is-open{display:flex!important;}.site-nav a{width:100%!important;padding:11px 12px!important;}.site-nav .nav-cta{margin-left:0!important;text-align:center!important;display:flex!important;}}';
    document.head.appendChild(style);
  }

  function removeLegacyHeaderStyles() {
    LEGACY_STYLE_IDS.forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.remove();
    });
    Array.prototype.slice.call(document.querySelectorAll('style')).forEach(function (style) {
      if (style.id === STYLE_ID) return;
      var css = style.textContent || '';
      if (css.indexOf('.site-header') !== -1 && css.indexOf('.site-header-inner') !== -1 && css.indexOf('.nav-cta') !== -1) style.remove();
    });
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
    removeLegacyHeaderStyles();
    injectStyles();
    removeLegacyHeaderStyles();
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
