'use strict';

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const motionButton = document.querySelector('.motion-toggle');
let paused = reducedMotion.matches;
function applyMotion() {
  document.body.classList.toggle('motion-paused', paused);
  motionButton.setAttribute('aria-pressed', String(paused));
  motionButton.setAttribute('aria-label', paused ? 'Resume animations' : 'Pause animations');
  motionButton.querySelector('.motion-label').textContent = paused ? 'Resume motion' : 'Pause motion';
  motionButton.querySelector('.motion-symbol').textContent = paused ? '▷' : 'Ⅱ';
}
applyMotion();
motionButton.addEventListener('click', () => { paused = !paused; applyMotion(); });
reducedMotion.addEventListener('change', event => { paused = event.matches; applyMotion(); });

if ('IntersectionObserver' in window && !reducedMotion.matches) {
  document.body.classList.add('js-motion');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); } });
  }, { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach(element => observer.observe(element));
}

const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
function closeMenu() { menuButton.setAttribute('aria-expanded', 'false'); menuButton.setAttribute('aria-label', 'Open navigation'); mobileNav.hidden = true; }
menuButton.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!expanded));
  menuButton.setAttribute('aria-label', expanded ? 'Open navigation' : 'Close navigation');
  mobileNav.hidden = expanded;
});
mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && !mobileNav.hidden) { closeMenu(); menuButton.focus(); } });
window.matchMedia('(min-width: 761px)').addEventListener('change', event => { if (event.matches) closeMenu(); });

const countLabels = { capsules: 'THREE BLENDS. YOUR KIND OF COFFEE.', bags: 'SMALL & LARGE BAGS. COMING SOON.', all: 'THE COFFEE FACTORY COLLECTION.' };
document.querySelectorAll('.filter').forEach(button => button.addEventListener('click', () => {
  const selected = button.dataset.filter;
  document.querySelectorAll('.filter').forEach(filter => { const active = filter === button; filter.classList.toggle('active', active); filter.setAttribute('aria-pressed', String(active)); });
  document.querySelectorAll('.product-card').forEach(card => { card.hidden = selected !== 'all' && card.dataset.category !== selected; if (!card.hidden) card.classList.add('is-visible'); });
  document.querySelector('#collection-count').textContent = countLabels[selected];
}));

const products = {
  crema: { name: 'CREMA', type: 'THE SMOOTH ONE / MEDIUM ROAST', flavors: 'Smooth · Creamy · Balanced', description: 'A smooth, creamy, balanced medium roast. An easygoing companion for your everyday coffee moment.', facts: [['FORMAT', '10 aluminum capsules'], ['ROAST', 'Medium']], image: 'crema.svg' },
  classico: { name: 'CLASSICO', type: 'THE EVERYDAY CLASSIC / MEDIUM ROAST', flavors: 'Balanced · Smooth · Aromatic', description: 'Balanced, smooth and aromatic. Classico is the medium-roast blend for those who love a classic cup.', facts: [['FORMAT', '10 aluminum capsules'], ['ROAST', 'Medium']], image: 'classico.svg' },
  intenso: { name: 'INTENSO', type: 'THE BOLD ONE / DARK ROAST', flavors: 'Bold · Rich · Full bodied', description: 'A bold, rich, full-bodied dark roast. For the mornings when you want a little more character in your cup.', facts: [['FORMAT', '10 aluminum capsules'], ['ROAST', 'Dark']], image: 'intenso.svg' },
  smallBag: { name: 'THE DAILY BAG', type: 'SMALL COFFEE BAG / CONCEPT PREVIEW', flavors: 'A little bag. A brighter morning.', description: 'A smaller coffee bag for your at-home ritual. This packaging is an early design concept; blend options, grind, weight and pricing will be announced with the collection.', facts: [['FORMAT', 'Small coffee bag'], ['AVAILABILITY', 'Coming soon']], image: 'small-bag.svg' },
  largeBag: { name: 'THE SHARING BAG', type: 'LARGE COFFEE BAG / CONCEPT PREVIEW', flavors: 'More good to go around.', description: 'A larger coffee bag for full kitchens and good company. This packaging is an early design concept; blend options, grind, weight and pricing will be announced with the collection.', facts: [['FORMAT', 'Large coffee bag'], ['AVAILABILITY', 'Coming soon']], image: 'large-bag.svg' }
};
const dialog = document.querySelector('.product-dialog');
let dialogOpener;
document.querySelectorAll('[data-product]').forEach(button => button.addEventListener('click', () => {
  const product = products[button.dataset.product];
  dialogOpener = button;
  document.querySelector('#dialog-title').textContent = product.name;
  document.querySelector('#dialog-type').textContent = product.type;
  document.querySelector('#dialog-flavors').textContent = product.flavors;
  document.querySelector('#dialog-description').textContent = product.description;
  const image = document.querySelector('#dialog-image');
  image.src = './assets/images/' + product.image + '?v=3';
  image.alt = 'Coffee Factory ' + product.name.toLowerCase() + ' packaging preview';
  const facts = document.querySelector('#dialog-facts');
  facts.replaceChildren(...product.facts.map(([label, value]) => { const item = document.createElement('div'); const title = document.createElement('span'); title.textContent = label; item.append(title, document.createTextNode(value)); return item; }));
  dialog.showModal();
  document.body.classList.add('modal-open');
}));
document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
document.querySelector('#dialog-visit').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target !== dialog) return; const box = dialog.getBoundingClientRect(); if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close(); });
dialog.addEventListener('close', () => { document.body.classList.remove('modal-open'); if (dialogOpener && document.activeElement === document.body) dialogOpener.focus(); });

const mapDialog = document.querySelector('.map-dialog');
let mapOpener;
document.querySelectorAll('[data-map-chooser]').forEach(link => link.addEventListener('click', event => {
  // The address links still open Google Maps when native dialogs are unavailable.
  if (!mapDialog || typeof mapDialog.showModal !== 'function') return;
  event.preventDefault();
  mapOpener = link;
  mapDialog.showModal();
  document.body.classList.add('modal-open');
}));
mapDialog.querySelector('.map-close').addEventListener('click', () => mapDialog.close());
mapDialog.querySelectorAll('a').forEach(link => link.addEventListener('click', () => mapDialog.close()));
mapDialog.addEventListener('click', event => {
  if (event.target !== mapDialog) return;
  const box = mapDialog.getBoundingClientRect();
  if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) mapDialog.close();
});
mapDialog.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  if (mapOpener) mapOpener.focus();
});

const toast = document.querySelector('.toast');
let toastTimeout;
document.querySelectorAll('[data-coming-soon]').forEach(button => button.addEventListener('click', () => {
  clearTimeout(toastTimeout);
  document.querySelector('#toast-message').textContent = button.dataset.comingSoon === 'Online ordering' ? 'Our online shop is on the way. Good coffee is worth the wait.' : 'Our ' + button.dataset.comingSoon + ' page is coming soon. Stay close.';
  toast.hidden = false;
  toastTimeout = setTimeout(() => { toast.hidden = true; }, 6500);
}));
toast.querySelector('button').addEventListener('click', () => { toast.hidden = true; clearTimeout(toastTimeout); });
document.querySelector('#year').textContent = new Date().getFullYear();
