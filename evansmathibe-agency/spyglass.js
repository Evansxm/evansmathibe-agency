/**
 * Spyglass Analytics & Interaction Engine
 * V2 Redesign - Evans Mathibe Agency
 */

document.addEventListener('DOMContentLoaded', () => {
    initBackgroundEngine();
    initScrollReveal();
    captureAnalytics();
});

/**
 * STEP 3: Intersection Observer for Background Swaps
 * Smoothly cross-fades background images based on section entry
 */
function initBackgroundEngine() {
    const container = document.getElementById('slider-container');
    const sections = document.querySelectorAll('section[data-bg]');
    const bgSlides = {};

    // Pre-create background slides
    sections.forEach((section, index) => {
        const bgFile = section.getAttribute('data-bg');
        const slide = document.createElement('div');
        slide.className = 'bg-slide';
        slide.style.backgroundImage = `url('assets/bg-images/${bgFile}')`;
        if (index === 0) slide.classList.add('active');
        container.appendChild(slide);
        bgSlides[bgFile] = slide;
    });

    const observerOptions = {
        threshold: 0.3,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bgFile = entry.target.getAttribute('data-bg');
                // Deactivate current slide, activate new one
                document.querySelectorAll('.bg-slide.active').forEach(s => s.classList.remove('active'));
                if (bgSlides[bgFile]) {
                    bgSlides[bgFile].classList.add('active');
                }
            }
        });
    }, observerOptions);

    sections.forEach(section => observer.observe(section));
}

/**
 * Scroll Reveal Logic
 */
function initScrollReveal() {
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.reveal, .reveal-delay-1, .reveal-delay-2').forEach(el => revealObserver.observe(el));
}

/**
 * Analytics: Capture and Notify
 */
function captureAnalytics() {
    const sessionStart = Date.now();
    const payload = {
        agent: navigator.userAgent,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        resolution: `${window.screen.width}x${window.screen.height}`,
        language: navigator.language,
        timestamp: new Date().toISOString(),
        event: 'SESSION_START'
    };

    console.log('[Spyglass] Initializing...', payload);
    
    // Webhook Placeholder
    // notifyWebhook(payload);

    window.addEventListener('beforeunload', () => {
        const duration = (Date.now() - sessionStart) / 1000;
        const exitPayload = {
            ...payload,
            event: 'SESSION_END',
            duration_seconds: duration
        };
        // Use sendBeacon for more reliable exit tracking
        // navigator.sendBeacon('YOUR_WEBHOOK_URL', JSON.stringify(exitPayload));
        console.log('[Spyglass] Session Duration:', duration, 's');
    });
}

function notifyWebhook(data) {
    // Placeholder for Discord/Slack/EmailJS
    fetch('https://webhook-endpoint.example.com/spyglass', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).catch(err => console.debug('Analytics offline'));
}