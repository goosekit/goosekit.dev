(function () {
  function setupHeader(header) {
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

    function isOpen() {
      return nav.classList.contains('is-open');
    }

    toggle.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopPropagation();
      if (isOpen()) closeMenu();
      else openMenu();
    });

    nav.addEventListener('click', function (event) {
      event.stopPropagation();
    });

    document.addEventListener('click', function (event) {
      if (!mq.matches || !isOpen()) return;
      if (!header.contains(event.target)) closeMenu();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') closeMenu();
    });

    function handleViewportChange() {
      if (!mq.matches) closeMenu();
    }

    if (typeof mq.addEventListener === 'function') mq.addEventListener('change', handleViewportChange);
    else if (typeof mq.addListener === 'function') mq.addListener(handleViewportChange);
  }

  function init() {
    var headers = document.querySelectorAll('.site-header');
    for (var i = 0; i < headers.length; i += 1) setupHeader(headers[i]);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
