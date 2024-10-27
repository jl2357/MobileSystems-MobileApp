//service worker 

self.addEventListener('install', function(event) {
    console.log('SW Installing Service Worker: ', event);
  });
  self.addEventListener('activate', function(event) {
    console.log('SW Activating Service Worker: ', event);
  });
  self.addEventListener('fetch', function(event) {
    console.log('SW Fetching something: ', event);
  });