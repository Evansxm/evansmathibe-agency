/**
 * Evans Mathibe Agency - Interaction Engine
 */

document.addEventListener('DOMContentLoaded', () => {
    initBackgroundSlider();
    initScrollReveal();
    initHeaderControl();
    initMobileMenu();
    initSpyglassAnalytics();
});

/**
 * Phase 2: Background Slider
 * Implements a Cross-Fade Slider with a Ken Burns effect
 */
function initBackgroundSlider() {
    const images = [
        'assets/bg-images/Generated image 1 (17).webp',
        'assets/bg-images/Generated image 1 (19).webp',
        'assets/bg-images/Generated image 1 - 2025-11-15T123734.061.webp',
        'assets/bg-images/Generated image 1 - 2025-11-15T144736.481.webp',
        'assets/bg-images/Generated image 1 - 2025-11-15T144947.944.webp',
        'assets/bg-images/Generated image 1 - 2025-11-15T145413.675.webp'
    ];
    
    const container = document.getElementById('slider-container');
    if (!container) return;

    // Create slider elements
    images.forEach((src, index) => {
        const div = document.createElement('div');
        div.style.backgroundImage = `url('${src}')`;
        if (index === 0) div.classList.add('active');
        container.appendChild(div);
    });

    let current = 0;
    const slides = container.querySelectorAll('div');

    setInterval(() => {
        slides[current].classList.remove('active');
        current = (current + 1) % slides.length;
        slides[current].classList.add('active');
    }, 5000); // 5s interval as per Agent: Layout Architect requirements
}

/**
 * Phase 4: Scroll Reveal
 * Uses Intersection Observer API for smooth transitions
 */
function initScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                // Optional: Unobserve after revealing
                // observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const revealElements = document.querySelectorAll('.reveal, .reveal-delay-1, .reveal-delay-2');
    revealElements.forEach(el => observer.observe(el));
}

/**
 * Sticky Header Control
 */
function initHeaderControl() {
    const header = document.getElementById('main-header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            header.classList.add('shrunk');
        } else {
            header.classList.remove('shrunk');
        }
    });
}

/**
 * Mobile Menu Toggle
 */
function initMobileMenu() {
    const toggle = document.getElementById('menu-toggle');
    const close = document.getElementById('menu-close');
    const menu = document.getElementById('mobile-menu');
    const links = document.querySelectorAll('.menu-link');

    toggle.addEventListener('click', () => {
        menu.classList.remove('opacity-0', 'pointer-events-none');
    });

    const hideMenu = () => {
        menu.classList.add('opacity-0', 'pointer-events-none');
    };

    close.addEventListener('click', hideMenu);
    links.forEach(link => link.addEventListener('click', hideMenu));
}

/**
 * Phase 3: The Spyglass Script
 * Lightweight analytics hook for tracking session duration and metadata
 */
function initSpyglassAnalytics() {
    const startTime = Date.now();
    const visitorData = {
        userAgent: navigator.userAgent,
        screenResolution: `${window.screen.width}x${window.screen.height}`,
        language: navigator.language,
        referrer: document.referrer || 'Direct',
        timestamp: new Date().toISOString()
    };

    // Trigger on landing
    logToSpyglass('Session Started', visitorData);

    // Trigger on long session (e.g., 30 seconds)
    setTimeout(() => {
        logToSpyglass('Session Milestone: 30s', { ...visitorData, timeSpent: '30s' });
    }, 30000);

    // Trigger before unload
    window.addEventListener('beforeunload', () => {
        const endTime = Date.now();
        const duration = (endTime - startTime) / 1000;
        logToSpyglass('Session Ended', { ...visitorData, duration: `${duration}s` });
    });
}

/**
 * Webhook Dispatcher
 * In a real scenario, this would point to a secure edge function
 */
function logToSpyglass(event, data) {
    console.log(`[Spyglass Analytics] ${event}:`, data);
    
    // Placeholder for Webhook or GitHub Action trigger
    // fetch('https://webhook-endpoint.example.com/spyglass', {
    //     method: 'POST',
    //     mode: 'no-cors',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ event, data })
    // }).catch(err => console.debug('Spyglass silent error'));
}