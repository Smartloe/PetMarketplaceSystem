/* ==========================================================================
   宠物志 — motion primitives
   --------------------------------------------------------------------------
   Everything here degrades to a static page under prefers-reduced-motion, and
   every listener / rAF loop is torn down on unmount. The pattern throughout is
   "JS writes a custom property, CSS owns the movement" — one shared observer
   and one shared scroll loop for the whole app rather than per-component ones.
   ========================================================================== */

import { onBeforeUnmount, onMounted, ref } from 'vue';

const REDUCED_MOTION_QUERY = '(prefers-reduced-motion: reduce)';

export function prefersReducedMotion() {
  if (typeof window === 'undefined' || !window.matchMedia) {
    return false;
  }
  return window.matchMedia(REDUCED_MOTION_QUERY).matches;
}

function isTouchPrimary() {
  if (typeof window === 'undefined' || !window.matchMedia) {
    return false;
  }
  return window.matchMedia('(hover: none)').matches;
}

/* ==========================================================================
   v-reveal — play an entrance once the element enters the viewport
   --------------------------------------------------------------------------
   `v-reveal` on its own reveals the element. `v-reveal.stagger` also indexes
   the direct children so CSS can walk them in one after another. Targets
   unobserve themselves after playing, so nothing accumulates across routes.
   ========================================================================== */

const revealHandlers = new WeakMap();
let revealObserver = null;

function getRevealObserver() {
  if (revealObserver || typeof window === 'undefined' || !window.IntersectionObserver) {
    return revealObserver;
  }

  revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }
        const handler = revealHandlers.get(entry.target);
        if (handler) {
          handler();
        }
      });
    },
    { rootMargin: '0px 0px -12% 0px', threshold: 0.08 }
  );

  return revealObserver;
}

export const vReveal = {
  mounted(el, binding) {
    if (binding.modifiers.stagger) {
      Array.from(el.children).forEach((child, index) => {
        child.style.setProperty('--stagger-index', String(index));
      });
    }

    // Reduced motion: mark as shown immediately, never animate.
    if (prefersReducedMotion()) {
      el.classList.add('is-revealed');
      return;
    }

    el.classList.add('reveal-target');

    const observer = getRevealObserver();
    if (!observer) {
      el.classList.add('is-revealed');
      return;
    }

    const play = () => {
      el.classList.add('is-revealed');
      observer.unobserve(el);
      revealHandlers.delete(el);
    };

    revealHandlers.set(el, play);
    observer.observe(el);
  },

  unmounted(el) {
    if (revealObserver) {
      revealObserver.unobserve(el);
    }
    revealHandlers.delete(el);
  },
};

/* ==========================================================================
   v-tilt — pointer-reactive plate tilt
   --------------------------------------------------------------------------
   Writes --tilt-x / --tilt-y / --pointer-x / --pointer-y and lets the CSS
   decide what to do with them, so a card can tilt, shift a sheen, or both.
   Skipped entirely on touch-primary devices, where there is no hover to track.
   ========================================================================== */

export const vTilt = {
  mounted(el, binding) {
    if (prefersReducedMotion() || isTouchPrimary()) {
      return;
    }

    const strength = Number(binding.value) || 6;
    let frame = null;

    const write = (event) => {
      const rect = el.getBoundingClientRect();
      if (!rect.width || !rect.height) {
        return;
      }

      // Normalised to -0.5…0.5 from the element's centre.
      const relX = (event.clientX - rect.left) / rect.width - 0.5;
      const relY = (event.clientY - rect.top) / rect.height - 0.5;

      el.style.setProperty('--tilt-y', `${(relX * strength).toFixed(2)}deg`);
      el.style.setProperty('--tilt-x', `${(-relY * strength).toFixed(2)}deg`);
      el.style.setProperty('--pointer-x', `${((relX + 0.5) * 100).toFixed(2)}%`);
      el.style.setProperty('--pointer-y', `${((relY + 0.5) * 100).toFixed(2)}%`);
    };

    const onMove = (event) => {
      if (frame) {
        return;
      }
      frame = window.requestAnimationFrame(() => {
        frame = null;
        write(event);
      });
    };

    const onLeave = () => {
      if (frame) {
        window.cancelAnimationFrame(frame);
        frame = null;
      }
      el.style.setProperty('--tilt-x', '0deg');
      el.style.setProperty('--tilt-y', '0deg');
      el.style.setProperty('--pointer-x', '50%');
      el.style.setProperty('--pointer-y', '50%');
    };

    el.addEventListener('pointermove', onMove);
    el.addEventListener('pointerleave', onLeave);
    el.__tiltCleanup = () => {
      el.removeEventListener('pointermove', onMove);
      el.removeEventListener('pointerleave', onLeave);
      if (frame) {
        window.cancelAnimationFrame(frame);
      }
    };
  },

  unmounted(el) {
    if (el.__tiltCleanup) {
      el.__tiltCleanup();
      delete el.__tiltCleanup;
    }
  },
};

/* ==========================================================================
   v-parallax — depth on scroll
   --------------------------------------------------------------------------
   One shared rAF-throttled scroll loop drives every registered element, so
   adding parallax to more elements costs no extra listeners.
   ========================================================================== */

const parallaxTargets = new Set();
let parallaxFrame = null;
let parallaxBound = false;

function paintParallax() {
  parallaxFrame = null;
  const viewportHeight = window.innerHeight || 1;

  parallaxTargets.forEach(({ el, depth }) => {
    const rect = el.getBoundingClientRect();
    if (rect.bottom < -200 || rect.top > viewportHeight + 200) {
      return;
    }

    // -1…1, where 0 means the element's centre sits on the viewport centre.
    const progress = (rect.top + rect.height / 2 - viewportHeight / 2) / viewportHeight;
    el.style.setProperty('--parallax-shift', `${(progress * depth * -1).toFixed(2)}px`);
    el.style.setProperty('--parallax-progress', progress.toFixed(4));
  });
}

function requestParallaxPaint() {
  if (parallaxFrame === null) {
    parallaxFrame = window.requestAnimationFrame(paintParallax);
  }
}

function bindParallaxLoop() {
  if (parallaxBound) {
    return;
  }
  window.addEventListener('scroll', requestParallaxPaint, { passive: true });
  window.addEventListener('resize', requestParallaxPaint, { passive: true });
  parallaxBound = true;
}

function unbindParallaxLoop() {
  if (!parallaxBound || parallaxTargets.size > 0) {
    return;
  }
  window.removeEventListener('scroll', requestParallaxPaint);
  window.removeEventListener('resize', requestParallaxPaint);
  if (parallaxFrame !== null) {
    window.cancelAnimationFrame(parallaxFrame);
    parallaxFrame = null;
  }
  parallaxBound = false;
}

export const vParallax = {
  mounted(el, binding) {
    if (prefersReducedMotion()) {
      return;
    }

    const entry = { el, depth: Number(binding.value) || 30 };
    el.__parallaxEntry = entry;
    parallaxTargets.add(entry);
    bindParallaxLoop();
    requestParallaxPaint();
  },

  unmounted(el) {
    if (el.__parallaxEntry) {
      parallaxTargets.delete(el.__parallaxEntry);
      delete el.__parallaxEntry;
    }
    unbindParallaxLoop();
  },
};

/* ==========================================================================
   useScrollProgress — 0…1 progress of the whole document
   ========================================================================== */

export function useScrollProgress() {
  const progress = ref(0);
  let frame = null;

  const measure = () => {
    frame = null;
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    progress.value = scrollable > 0 ? Math.min(1, Math.max(0, window.scrollY / scrollable)) : 0;
  };

  const onScroll = () => {
    if (frame === null) {
      frame = window.requestAnimationFrame(measure);
    }
  };

  onMounted(() => {
    measure();
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });
  });

  onBeforeUnmount(() => {
    window.removeEventListener('scroll', onScroll);
    window.removeEventListener('resize', onScroll);
    if (frame !== null) {
      window.cancelAnimationFrame(frame);
    }
  });

  return { progress };
}

/* ==========================================================================
   useCountUp — ease a number up to its target once, on demand
   ========================================================================== */

export function useCountUp(target, { duration = 1200 } = {}) {
  const value = ref(prefersReducedMotion() ? target : 0);
  let frame = null;

  const start = () => {
    if (prefersReducedMotion()) {
      value.value = target;
      return;
    }

    const startedAt = performance.now();
    const step = (now) => {
      const elapsed = Math.min(1, (now - startedAt) / duration);
      // easeOutExpo — fast commitment, soft landing.
      const eased = elapsed === 1 ? 1 : 1 - Math.pow(2, -10 * elapsed);
      value.value = target * eased;

      if (elapsed < 1) {
        frame = window.requestAnimationFrame(step);
      } else {
        frame = null;
        value.value = target;
      }
    };

    frame = window.requestAnimationFrame(step);
  };

  onBeforeUnmount(() => {
    if (frame !== null) {
      window.cancelAnimationFrame(frame);
    }
  });

  return { value, start };
}

export function registerMotion(app) {
  app.directive('reveal', vReveal);
  app.directive('tilt', vTilt);
  app.directive('parallax', vParallax);
}

