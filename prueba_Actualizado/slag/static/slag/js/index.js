document.addEventListener('DOMContentLoaded', function() {
        const btnInicio = document.getElementById('home-tab');
        const header = document.getElementById('inicio');
        if (btnInicio && header) {
          btnInicio.addEventListener('click', function(e) {
            e.preventDefault();
            smoothScrollTo(header.offsetTop, 1200); // 1200 ms = 1.2 segundos
          });
        }

        function smoothScrollTo(target, duration) {
          const start = window.scrollY;
          const change = target - start;
          const startTime = performance.now();

          function animateScroll(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const ease = progress < 0.5
              ? 2 * progress * progress
              : -1 + (4 - 2 * progress) * progress;
            window.scrollTo(0, start + change * ease);
            if (progress < 1) {
              requestAnimationFrame(animateScroll);
            }
          }
          requestAnimationFrame(animateScroll);
        }
      });