const cacheName = "WebCache";
const filesToCache = [
    '/'
];

self.addEventListener('install', evt => {
    evt.waitUntil(
        caches.open(cacheName).then(cache => {
            cache.addAll(filesToCache);
        })
    );
});

self.addEventListener('fetch', evt => {
    if (evt.request.url.indexOf('http') === 0) {
        evt.respondWith(
            fetch(evt.request).then(fetchRes => {
                return caches.open(cacheName).then(cache => {
                    cache.put(evt.request.url, fetchRes.clone());
                    return fetchRes;
                })
            }).catch(() => {
                return caches.match(evt.request).then(cacheRes => {
                    return cacheRes;
                }).catch(() => {
                    return caches.match('');
                })
            })
        );
    }
});

self.addEventListener('activate', evt => {
    evt.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(keys
                .filter(key => key !== cacheName)
                .map(key => caches.delete(key))
            )
        })
    );
});