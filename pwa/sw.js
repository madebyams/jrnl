// jrnl. service worker — caches the app shell for offline use.
// No user data is ever cached or transmitted; jrnl. is ephemeral by design.

const CACHE = 'jrnl-v1';
const PRECACHE = ['/', '/manifest.json', '/icons/icon.svg'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(PRECACHE))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  // Remove any old cache versions left over from previous installs.
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  // Cache-first: serve from cache, fall back to network.
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request))
  );
});
