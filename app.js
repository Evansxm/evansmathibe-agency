/**
 * Evans Mathibe Agency - Interaction Engine
 * Features: Cinematic Slider, Scroll Reveals, Visitor Tracking
 */

document.addEventListener('DOMContentLoaded', () => {
    initCinematicSlider();
    initScrollReveal();
    initNavigation();
    initVisitorTracking();
});

/**
 * Cinematic Background Slider
 * Uses all optimized .webp images from assets/bg-images/
 */
function initCinematicSlider() {
    const images = [
        'Evans mathibe Logo.webp',
        'Generated image 1 (17).webp',
        'Generated image 1 (19).webp',
        'Generated image 1 - 2025-11-15T123734.061.webp',
        'Generated image 1 - 2025-11-15T144736.481.webp',
        'Generated image 1 - 2025-11-15T144947.944.webp',
        'Generated image 1 - 2025-11-15T145413.675.webp',
        'Generated image 1 - 2025-11-16T092719.365.webp'
    ];

    const container = document.getElementById('slider-container');
    if (!container) return;

    // Preload and Create Slides
    images.forEach((img, index) => {
        const slide = document.createElement('div');
        slide.style.backgroundImage = `url('assets/bg-images/${img}')`;
        if (index === 0) slide.classList.add('active');
        container.appendChild(slide);
    });

    let currentSlide = 0;
    const slides = container.querySelectorAll('div');

    setInterval(() => {
        slides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % slides.length;
        slides[currentSlide].classList.add('active');
    }, 6000); // 6 second interval
}

/**
 * Intersection Observer for Scroll Reveals
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
            }
        });
    }, observerOptions);

    const revealElements = document.querySelectorAll('.reveal, .reveal-delay-1, .reveal-delay-2, .reveal-delay-3');
    revealElements.forEach(el => observer.observe(el));
}

/**
 * Navigation Effects
 */
function initNavigation() {
    const nav = document.getElementById('main-nav');
    const menuToggle = document.getElementById('menu-toggle');
    const menuClose = document.getElementById('menu-close');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuLinks = document.querySelectorAll('.menu-link');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    });

    const toggleMenu = () => mobileMenu.classList.toggle('active');

    menuToggle.addEventListener('click', toggleMenu);
    menuClose.addEventListener('click', toggleMenu);
    menuLinks.forEach(link => link.addEventListener('click', toggleMenu));
}

/**
 * Visitor Tracking & Notifications (GA4 + EmailJS)
 */
function initVisitorTracking() {
    // GA4 Placeholder (Replace with your actual Measurement ID)
    // window.dataLayer = window.dataLayer || [];
    // function gtag(){dataLayer.push(arguments);}
    // gtag('js', new Date());
    // gtag('config', 'G-XXXXXXXXXX');

    const startTime = Date.now();
    
    // Capture basic metadata
    const visitorInfo = {
        userAgent: navigator.userAgent,
        screenRes: `${window.screen.width}x${window.screen.height}`,
        language: navigator.language,
        referrer: document.referrer || 'Direct Entry',
        timestamp: new Date().toLocaleString()
    };

    // Lightweight Session Logger via EmailJS
    // Note: User needs to set up EmailJS and provide Service/Template/Public Key
    // emailjs.init("YOUR_PUBLIC_KEY");

    window.addEventListener('beforeunload', () => {
        const timeSpent = Math.round((Date.now() - startTime) / 1000);
        console.log(`[Analytics] Session ended. Duration: ${timeSpent}s`);
        
        // Example EmailJS Dispatch (Uncomment and configure to use)
        /*
        emailjs.send("YOUR_SERVICE_ID", "YOUR_TEMPLATE_ID", {
            visitor_id: Math.random().toString(36).substring(7),
            timestamp: visitorInfo.timestamp,
            device: visitorInfo.userAgent,
            duration: `${timeSpent}s`,
            location_ref: visitorInfo.referrer
        });
        */
    });

    console.log('[Analytics] Monitoring session engagement...');
}

/**
 * Contact Form Logic
 */
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const btn = contactForm.querySelector('button');
        const originalText = btn.innerHTML;
        
        btn.innerHTML = 'Dispatching...';
        btn.disabled = true;

        // Simulate dispatch
        setTimeout(() => {
            btn.innerHTML = 'Transmission Received.';
            contactForm.reset();
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 3000);
        }, 1500);
    });
}