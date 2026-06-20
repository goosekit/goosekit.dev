(function () {
  var CONFIG = {
    apiKey: 'phc_qtYbnDv7TBtid67Z7rMhLefybboknUL5EzTpwVYUCtKe',
    apiHost: 'https://us.i.posthog.com',
    personProfiles: 'identified_only'
  };

  if (!CONFIG.apiKey || typeof window === 'undefined') return;
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') return;
  if (window.posthog) return;

  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split('.');2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement('script')).type='text/javascript',p.async=!0,p.src=s.api_host.replace('.i.posthog.com','-assets.i.posthog.com')+'/static/array.js',(r=t.getElementsByTagName('script')[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a='posthog',u.people=u.people||[],u.toString=function(t){var e='posthog';return'posthog'!==a&&(e+='.'+a),t||(e+=' (stub)'),e},u.people.toString=function(){return u.toString(1)+'.people (stub)'},o='init capture register register_once unregister unregister_once identify alias set_config reset opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing capture_pageview capture_session_replay get_session_replay_url onSessionId'.split(' '),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

  window.posthog.init(CONFIG.apiKey, {
    api_host: CONFIG.apiHost,
    person_profiles: CONFIG.personProfiles,
    capture_pageview: true,
    capture_pageleave: true,
    autocapture: true,
    persistence: 'localStorage+cookie'
  });

  window.posthog.register({
    site: 'goosekit',
    hostname: window.location.hostname
  });

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-ph-event]').forEach(function (el) {
      if (el.__goosekitPosthogBound) return;
      el.__goosekitPosthogBound = true;

      el.addEventListener('click', function () {
        var eventName = el.getAttribute('data-ph-event');
        if (!eventName || !window.posthog || typeof window.posthog.capture !== 'function') return;

        var href = el.getAttribute('href') || '';
        var product = el.getAttribute('data-ph-product') ||
          (href.indexOf('/offline-pack') !== -1 || href.indexOf('/go/offline-pack') !== -1 ? 'offline_pack' :
          (href.indexOf('/ship-it-kit') !== -1 || href.indexOf('/go/ship-it-kit') !== -1 ? 'ship_it_kit' :
          (href.indexOf('/stripe-supabase-billing-drift-check') !== -1 ||
           href.indexOf('/stripe-billing-reliability-checklist') !== -1 ||
           href.indexOf('/billing-health-support') !== -1 ||
           href.indexOf('/go/billing-reliability') !== -1 ||
           href.indexOf('/nextjs-supabase-stripe-setup-help') !== -1 ? 'billing_reliability' : 'unknown')));

        window.posthog.capture(eventName, {
          site: 'goosekit',
          product: product,
          location: el.getAttribute('data-ph-location') || 'unknown',
          path: window.location.pathname,
          target_href: href || null,
          ref: new URLSearchParams(window.location.search).get('ref') || null,
          score: el.getAttribute('data-ph-score') || null,
          risk_count: el.getAttribute('data-ph-risk-count') || null,
          recommended_scope: el.getAttribute('data-ph-recommended-scope') || null,
          unchecked_risk_keys: el.getAttribute('data-ph-unchecked-risk-keys') || null,
          price_eur: el.getAttribute('data-ph-price-eur') || null,
          price_eur_monthly: el.getAttribute('data-ph-price-eur-monthly') || null,
          request_context: el.getAttribute('data-ph-request-context') || null
        });

        if (href.indexOf('/go/offline-pack') !== -1 || href.indexOf('f897713c-9cd2-4aaa-bd95-abd5ecd6b757') !== -1) {
          window.posthog.capture('offline_pack_checkout_intent', {
            site: 'goosekit',
            product: 'offline_pack',
            location: el.getAttribute('data-ph-location') || 'unknown',
            path: window.location.pathname,
            target_href: href
          });
        }
      });
    });
  });
}());
