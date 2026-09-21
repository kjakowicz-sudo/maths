/* Service worker: makes the trainer open instantly and work with no connection.
   Cache-first so a launch never waits on the network, with a quiet background
   refresh so a new version is picked up the next time the app is opened. */
var VERSION = 'nrt-2026-09-21';
var SHELL = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png'
];

self.addEventListener('install', function(e){
  e.waitUntil(
    caches.open(VERSION)
      .then(function(c){ return c.addAll(SHELL); })
      .then(function(){ return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function(e){
  e.waitUntil(
    caches.keys().then(function(keys){
      return Promise.all(keys.map(function(k){
        return k === VERSION ? null : caches.delete(k);
      }));
    }).then(function(){ return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function(e){
  var req = e.request;
  if(req.method !== 'GET') return;
  var url;
  try { url = new URL(req.url); } catch(err){ return; }
  if(url.origin !== self.location.origin) return;

  /* opening the app: serve the cached page at once, refresh it behind the scenes */
  if(req.mode === 'navigate'){
    e.respondWith((async function(){
      var cache = await caches.open(VERSION);
      var cached = await cache.match('./index.html') || await cache.match('./');
      var net = fetch(req).then(function(res){
        if(res && res.ok) cache.put('./index.html', res.clone());
        return res;
      }).catch(function(){ return null; });
      if(cached) return cached;
      var fresh = await net;
      return fresh || new Response(
        '<h1>Offline</h1><p>Open the app once while connected and it will work offline from then on.</p>',
        { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8' } }
      );
    })());
    return;
  }

  e.respondWith((async function(){
    var cache = await caches.open(VERSION);
    var cached = await cache.match(req);
    var net = fetch(req).then(function(res){
      if(res && res.ok && res.type === 'basic') cache.put(req, res.clone());
      return res;
    }).catch(function(){ return null; });
    return cached || (await net) || Response.error();
  })());
});
