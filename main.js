// Scroll choreography modelled on era-residence.com: Lenis smooth scroll driving GSAP ScrollTrigger.
gsap.registerPlugin(ScrollTrigger, SplitText);

const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const isDesktop = () => innerWidth >= 992;
const EASE_OUT = 'power4.out'; // close to ERA's "Out" curve (0.25, 1, 0.5, 1)

document.fonts.ready.then(() => (reduceMotion ? initHeaderTheme() : init()));

// Phones get the doors clip as a tall crop centred on the doors, so they need a poster cut from that crop too;
// otherwise the landscape poster shows off-centre until the video loads, then the doors jump to the middle.
// Runs for everyone (reduced motion included), since the poster is all those visitors see.
const bookVideo = document.querySelector('.book-video');
if (bookVideo && matchMedia('(max-width: 767px)').matches) bookVideo.poster = 'assets/img/entrance-doors-mobile.jpg';

function init() {
  // Smooth scroll, ticked by GSAP so ScrollTrigger and Lenis share one frame loop
  const lenis = new Lenis({ duration: 1.2, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), anchors: true });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add(t => lenis.raf(t * 1000));
  gsap.ticker.lagSmoothing(0);

  // Shared by index.html and rooms.html: section-specific effects only run where their section exists
  const has = sel => document.querySelector(sel);
  if (has('.rooms-track')) initRooms();   // creates a pin, so it goes before triggers further down the page
  if (has('.hero-video')) initHero();
  if (has('.arch')) initArch();
  initTextReveals();
  initImageReveals();
  initParallax();
  if (has('.balcony')) initBalcony();
  initDepth();
  initFlora();
  if (has('.siolim-line')) initSiolim();
  if (has('.coast')) initCoast();
  if (has('.map-dot')) initPlaceLinks();
  initAutoplay();
  if (has('.book-video')) initBook();
  initHeaderTheme();

  // A link like index.html#spaces makes the browser jump on load, before the room pan's pin adds its scroll
  // height, so it lands a screen short. Jump again once every trigger is in place.
  const target = location.hash && document.querySelector(location.hash);
  if (target) { ScrollTrigger.refresh(); lenis.scrollTo(target, { immediate: true, force: true }); }
}

// Big headings: letters rise and turn into place (ERA's heading reveal)
function initTextReveals() {
  document.querySelectorAll('[data-split]').forEach(el => {
    const split = SplitText.create(el, { type: 'words,chars' });
    const isHero = !!el.closest('.hero-title');
    gsap.from(split.chars, {
      yPercent: 50, rotateY: 90, opacity: 0,
      duration: 1.2, ease: EASE_OUT, stagger: 0.04,
      delay: isHero ? 0.3 : 0,
      scrollTrigger: isHero ? undefined : { trigger: el, start: 'top 85%', once: true },
    });
  });

  // Body copy: lines slide up from behind a mask
  document.querySelectorAll('[data-lines]').forEach(el => {
    SplitText.create(el, {
      type: 'lines', mask: 'lines', autoSplit: true,
      onSplit: self => gsap.from(self.lines, {
        yPercent: 110, duration: 1.2, ease: EASE_OUT, stagger: 0.1,
        scrollTrigger: { trigger: el, start: 'top 88%', once: true },
      }),
    });
  });

  // Script words write themselves in from left to right (the clip leaves room for swashes)
  document.querySelectorAll('[data-write]').forEach(el => {
    const isHero = !!el.closest('.hero-title');
    gsap.fromTo(el, { clipPath: 'inset(-30% 100% -30% -10%)' }, {
      clipPath: 'inset(-30% -10% -30% -10%)', duration: 1.6, ease: 'power2.inOut',
      delay: isHero ? 1 : 0.4,
      scrollTrigger: isHero ? undefined : { trigger: el, start: 'top 88%', once: true },
    });
  });

  if (document.querySelector('.hero-sub')) gsap.from('.hero-sub, .hero-ctas', { y: 30, opacity: 0, duration: 1.2, ease: EASE_OUT, delay: 0.8, stagger: 0.12 });
}

// Drives a video from scroll progress. The scroll animation only records where the video should be (p, 0 to 1);
// each frame we seek there, but only once the previous seek has finished. Setting currentTime on every tick
// queues seeks faster than the browser can decode them, and the picture falls behind the scroll.
function scrubVideo(video) {
  const target = { p: 0 };
  gsap.ticker.add(() => {
    const t = target.p * (video.duration - 0.05);
    if (!video.seeking && Math.abs(video.currentTime - t) > 0.02) video.currentTime = t;
  });
  return target;
}

// Hero: the frame opens to full bleed and the video plays in step with the scroll
function initHero() {
  const video = document.querySelector('.hero-video');
  // Start frame: an arch-topped window (the oversized radius clamps to a semicircle). Spelled out in full,
  // matching style.css: the browser reports the CSS value in shorthand and GSAP would snap the missing sides open.
  const frame = matchMedia('(max-width: 767px)').matches ? 'inset(9% 4% 9% 4% round 999px 999px 0px 0px)' : 'inset(11% 17% 11% 17% round 999px 999px 0px 0px)';
  const build = () => {
    gsap.timeline({ scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom bottom', scrub: true } })
      .fromTo('.hero-media', { clipPath: frame }, { clipPath: 'inset(0% 0% 0% 0% round 0px 0px 0px 0px)', ease: 'none', duration: 0.18 }, 0)
      .to('.hero-copy', { yPercent: -25, autoAlpha: 0, ease: 'none', duration: 0.14 }, 0)
      // Two lines rise in and drift away over the balcony part of the glide
      .fromTo('.hero-line:nth-of-type(1)', { autoAlpha: 0, yPercent: 12 }, { autoAlpha: 1, yPercent: 0, ease: 'none', duration: 0.08 }, 0.3)
      .to('.hero-line:nth-of-type(1)', { autoAlpha: 0, yPercent: -12, ease: 'none', duration: 0.08 }, 0.46)
      .fromTo('.hero-line:nth-of-type(2)', { autoAlpha: 0, yPercent: 12 }, { autoAlpha: 1, yPercent: 0, ease: 'none', duration: 0.08 }, 0.6)
      .to('.hero-line:nth-of-type(2)', { autoAlpha: 0, yPercent: -12, ease: 'none', duration: 0.08 }, 0.8)
      .fromTo(scrubVideo(video), { p: 0 }, { p: 1, ease: 'none', duration: 1 }, 0);
    ScrollTrigger.refresh();
  };
  video.readyState >= 1 ? build() : video.addEventListener('loadedmetadata', build, { once: true });

  // iOS Safari only seeks a video after it has played once from a user gesture
  addEventListener('touchstart', () => video.play().then(() => video.pause()).catch(() => {}), { once: true });
}

// The peach circle from the logo widens as it rises over the hero
function initArch() {
  gsap.fromTo('.arch', { scaleX: 0.55 }, {
    scaleX: 1, ease: 'none',
    scrollTrigger: { trigger: '.arch', start: 'top bottom', end: 'bottom 45%', scrub: true },
  });
}

// Rooms: vertical scroll pans the row sideways (desktop only; mobile stays stacked)
function initRooms() {
  gsap.matchMedia().add('(min-width: 992px)', () => {
    const track = document.querySelector('.rooms-track');
    const distance = () => track.scrollWidth - innerWidth;
    const pan = gsap.to(track, {
      x: () => -distance(), ease: 'none',
      scrollTrigger: { trigger: '.rooms', start: 'top top', end: () => `+=${distance()}`, pin: true, scrub: 0.5, invalidateOnRefresh: true },
    });
    // Each photo drifts inside its frame as it crosses the screen
    gsap.utils.toArray('.room-media > *').forEach(img => {
      gsap.fromTo(img, { xPercent: -6 }, {
        xPercent: 6, ease: 'none',
        scrollTrigger: { trigger: img.parentElement, containerAnimation: pan, start: 'left right', end: 'right left', scrub: true },
      });
    });
  });
}

// Photos unveil upwards from their bottom edge the first time they come into view
function initImageReveals() {
  gsap.utils.toArray('[data-reveal]').forEach(el => {
    gsap.fromTo(el, { clipPath: 'inset(100% 0% 0% 0%)' }, {
      clipPath: 'inset(0% 0% 0% 0%)', duration: 1.4, ease: EASE_OUT,
      scrollTrigger: { trigger: el, start: 'top 88%', once: true },
    });
  });
}

// Images taller than their frame slide slowly as they pass
function initParallax() {
  gsap.utils.toArray('[data-parallax]').forEach(img => {
    gsap.fromTo(img, { yPercent: 0 }, {
      yPercent: -16, ease: 'none',
      scrollTrigger: { trigger: img.parentElement, start: 'top bottom', end: 'bottom top', scrub: true },
    });
  });
}

// Balcony photo settles from a slight zoom; the small overhead photo rises faster, across the section edge
function initBalcony() {
  const zoom = matchMedia('(max-width: 767px)').matches ? 1.05 : 1.18;   // phones already crop the photo hard
  gsap.fromTo('.balcony-media img', { scale: zoom }, {
    scale: 1, ease: 'none',
    scrollTrigger: { trigger: '.balcony', start: 'top bottom', end: 'bottom bottom', scrub: true },
  });
  gsap.fromTo('.balcony-float', { yPercent: 35 }, {
    yPercent: -15, ease: 'none',
    scrollTrigger: { trigger: '.balcony', start: 'top bottom', end: 'bottom top', scrub: true },
  });
}

// Flowers drift and turn a little as they pass, so they feel like they're swaying in front of the page
function initFlora() {
  gsap.utils.toArray('[data-drift]').forEach((el, i) => {
    const d = +el.dataset.drift, turn = i % 2 ? 6 : -6, spin = +el.dataset.spin || 0;   // spin: a slow turn for round motifs
    gsap.fromTo(el, { yPercent: d, rotate: spin ? 0 : -turn }, {
      yPercent: -d, rotate: spin || turn, ease: 'none',
      scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true },
    });
  });
}

// Coast stops pop in one after another along the line
function initCoast() {
  gsap.from('.coast li', {
    y: 24, autoAlpha: 0, duration: 0.9, ease: EASE_OUT, stagger: 0.08,
    scrollTrigger: { trigger: '.coast', start: 'top 85%', once: true },
  });
}

// Hovering a place in the list lights up its marker, draws a route to it from the stay's pin,
// and adds the drive time to the marker's label
function initPlaceLinks() {
  const items = document.querySelectorAll('[data-place]');
  const route = document.querySelector('.map-route'), path = route.querySelector('path');
  const pin = document.querySelector('.map-pin');
  const at = el => [parseFloat(el.style.left) * 11.2, parseFloat(el.style.top) * 14];   // % -> the 1120x1400 map
  const set = (id, on) => {
    items.forEach(el => el.dataset.place === id && el.classList.toggle('is-active', on));
    const dot = document.querySelector(`.map-dot[data-place="${id}"]`);
    if (!dot) return;
    const label = dot.querySelector('b');
    label.dataset.name ??= label.textContent;
    const time = document.querySelector(`li[data-place="${id}"] .coast-time`)?.textContent;
    label.textContent = on && time ? `${label.dataset.name} \u00b7 ${time}` : label.dataset.name;
    if (on) {
      const [x1, y1] = at(pin), [x2, y2] = at(dot);
      const cx = (x1 + x2) / 2 + (y2 - y1) * 0.18, cy = (y1 + y2) / 2 - (x2 - x1) * 0.18;   // a gentle arc
      path.setAttribute('d', `M${x1},${y1} Q${cx},${cy} ${x2},${y2}`);
    }
    route.classList.toggle('is-on', on);
  };
  items.forEach(el => {
    el.addEventListener('mouseenter', () => set(el.dataset.place, true));
    el.addEventListener('mouseleave', () => set(el.dataset.place, false));
  });
}

// Grid tiles drift at slightly different speeds, so the "Room to play" grid reads as layers (desktop only)
function initDepth() {
  gsap.matchMedia().add('(min-width: 768px)', () => {
    gsap.utils.toArray('[data-depth]').forEach(el => {
      const d = +el.dataset.depth;
      gsap.fromTo(el, { y: d }, { y: -d, ease: 'none', scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
  });
}

// Place names drift in opposite directions
function initSiolim() {
  const from = [0, 10, -3], to = [8, -8, 8];   // every line starts inside the left edge
  gsap.utils.toArray('.siolim-line').forEach((line, i) => {
    gsap.fromTo(line, { xPercent: from[i] }, {
      xPercent: to[i], ease: 'none',
      scrollTrigger: { trigger: '.siolim', start: 'top bottom', end: 'bottom top', scrub: true },
    });
  });
}

// Looping clips (rooms, river) play only while on screen (never under reduced motion, since init() doesn't run).
// IntersectionObserver sees the real position, so it works inside the sideways room pan too.
function initAutoplay() {
  const io = new IntersectionObserver(entries => entries.forEach(e => {
    e.isIntersecting ? e.target.play().catch(() => {}) : e.target.pause();
  }), { threshold: 0.25 });
  document.querySelectorAll('[data-autoplay]').forEach(v => io.observe(v));
}

// Closing, a bookend to the hero: the frame opens while the entrance doors swing open with the scroll,
// then the sign-off rises in over the hall
function initBook() {
  const video = document.querySelector('.book-video');
  // Same arch window as the hero; wide enough to keep the welcome sign in view
  const frame = isDesktop() ? 'inset(10% 14% 10% 14% round 999px 999px 0px 0px)' : 'inset(10% 4% 10% 4% round 999px 999px 0px 0px)';
  const build = () => {
    gsap.timeline({ scrollTrigger: { trigger: '.book', start: 'top top', end: 'bottom bottom', scrub: true } })
      .fromTo('.book-media', { clipPath: frame }, { clipPath: 'inset(0% 0% 0% 0% round 0px 0px 0px 0px)', ease: 'none', duration: 0.3 }, 0)
      .fromTo(scrubVideo(video), { p: 0 }, { p: 1, ease: 'none', duration: 0.75 }, 0)
      .fromTo('.book-copy', { autoAlpha: 0, y: 60 }, { autoAlpha: 1, y: 0, ease: 'none', duration: 0.2 }, 0.8);
    ScrollTrigger.refresh();
  };
  video.readyState >= 1 ? build() : video.addEventListener('loadedmetadata', build, { once: true });
  addEventListener('touchstart', () => video.play().then(() => video.pause()).catch(() => {}), { once: true });
}

// Header text turns light over dark sections. Checks what is actually under the nav,
// so the arch (which overlaps the hero) counts as light before its section starts.
function initHeaderTheme() {
  const header = document.querySelector('.site-header');
  const check = () => {
    const under = document.elementsFromPoint(innerWidth - 160, 44).find(el => !header.contains(el));
    const zone = under?.closest('[data-header]');
    if (zone) header.classList.toggle('on-dark', zone.dataset.header === 'dark');
  };
  ScrollTrigger.create({ start: 0, end: 'max', onUpdate: check, onRefresh: check });
}
