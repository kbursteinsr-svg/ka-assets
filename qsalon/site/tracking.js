/* Q Salon analytics. Source attribution is session-scoped, with 30 min inactivity. */
(() => {
  'use strict';
  if (window.__qsalonTrackingActive) return;
  window.__qsalonTrackingActive = true;
  const measurementId = 'G-V0NPW7N594';
  const tags = {
    google: 'qsalongoogle-20',
    facebook: 'qsalonfb-20',
    instagram: 'qsalonig-20',
    website: 'qsalonweb-20'
  };
  const aliases = {google: 'google', gbp: 'google', facebook: 'facebook', fb: 'facebook', instagram: 'instagram', ig: 'instagram'};
  const storageKey = 'qsalon-referral-v1';
  const now = Date.now();
  const ttl = 30 * 60 * 1000;
  let saved;
  try { saved = JSON.parse(sessionStorage.getItem(storageKey)); } catch (_) {}
  let channel = saved && now - saved.time >= 0 && now - saved.time < ttl && Object.hasOwn(tags, saved.channel)
    ? saved.channel : 'website';
  const query = new URLSearchParams(location.search);
  if (query.has('utm_source')) {
    const source = query.get('utm_source').toLowerCase();
    channel = Object.hasOwn(aliases, source) ? aliases[source] : 'website';
  } else if (document.referrer) {
    try {
      const host = new URL(document.referrer).hostname.toLowerCase();
      const ownHost = location.hostname.replace(/^www\./, '');
      if (host.replace(/^www\./, '') !== ownHost) {
        if (host === 'google.com' || host.endsWith('.google.com')) channel = 'google';
        else if (host === 'facebook.com' || host.endsWith('.facebook.com')) channel = 'facebook';
        else if (host === 'instagram.com' || host.endsWith('.instagram.com')) channel = 'instagram';
        else channel = 'website';
      }
    } catch (_) {}
  }
  try { sessionStorage.setItem(storageKey, JSON.stringify({channel, time: now})); } catch (_) {}

  window.dataLayer = window.dataLayer || [];
  window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', measurementId, {
    allow_google_signals: false,
    allow_ad_personalization_signals: false
  });
  const loader = document.createElement('script');
  loader.async = true;
  loader.src = 'https://www.googletagmanager.com/gtag/js?id=' + measurementId;
  document.head.appendChild(loader);

  document.querySelectorAll('a.aff-go').forEach(link => {
    // Netlify's site-wide snippet also supports the current prebuilt product cards.
    const card = link.closest('article.aff');
    const name = link.dataset.productName || card?.querySelector('h3')?.textContent.trim() || 'Unknown product';
    const category = link.dataset.productCategory || card?.querySelector('.k')?.textContent.trim() || 'Other';
    const image = card?.querySelector('img')?.getAttribute('src') || '';
    const productId = link.dataset.productId || image.split('/').pop().replace(/\.(jpg|webp)$/, '') || name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
    link.dataset.productId = productId;
    link.dataset.productName = name;
    link.dataset.productCategory = category;
    link.id = link.id || 'amazon-' + productId;
    const destination = new URL(link.href);
    const fullAmazonLink = destination.protocol === 'https:' &&
      ['amazon.com', 'www.amazon.com'].includes(destination.hostname);
    // Only full, verified product URLs support replacing an embedded tag.
    // Amazon short links must remain unchanged until their full URLs are verified.
    if (fullAmazonLink && /\/(?:dp|gp\/product)\/[A-Z0-9]{10}(?:\/|$)/.test(destination.pathname)) {
      destination.searchParams.set('tag', tags[channel]);
      link.href = destination.href;
    }
    const actualTag = fullAmazonLink ? destination.searchParams.get('tag') : null;
    link.addEventListener('click', () => {
      const params = {
        product_id: link.dataset.productId,
        product_name: link.dataset.productName,
        product_category: link.dataset.productCategory,
        affiliate_channel: channel,
        affiliate_link_status: actualTag === tags[channel] ? 'tagged' : 'short_link_unverified',
        link_url: link.href,
        link_domain: destination.hostname,
        transport_type: 'beacon'
      };
      if (actualTag) params.affiliate_tracking_id = actualTag;
      window.gtag('event', 'amazon_click', params);
    });
  });
})();
