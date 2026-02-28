// EvansMathibe Agency - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    const backToTop = document.getElementById('backToTop');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        // Back to top visibility
        if (window.scrollY > 300) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '#') return;
            
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Initialize Image Slider
    if ($('.image-slider').length) {
        $('.image-slider').slick({
            dots: true,
            infinite: true,
            speed: 800,
            slidesToShow: 1,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 5000,
            fade: true,
            cssEase: 'cubic-bezier(0.4, 0, 0.2, 1)',
            arrows: false,
            dotsClass: 'slick-dots custom-dots',
            responsive: [
                {
                    breakpoint: 768,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1
                    }
                }
            ]
        });
    }

    // Custom slick dots styling
    const style = document.createElement('style');
    style.textContent = `
        .custom-dots {
            bottom: 20px !important;
        }
        .custom-dots li {
            margin: 0 5px !important;
        }
        .custom-dots li button {
            width: 12px !important;
            height: 12px !important;
            padding: 0 !important;
            border-radius: 50% !important;
            background: rgba(255, 182, 180, 0.5) !important;
            border: 2px solid var(--accent-pink) !important;
        }
        .custom-dots li.slick-active button {
            background: var(--accent-pink) !important;
            transform: scale(1.2);
        }
    `;
    document.head.appendChild(style);

    // Form Real-time Validation
    const contactForm = document.getElementById('contactForm');
    const inputs = contactForm.querySelectorAll('.form-control[required]');

    inputs.forEach(input => {
        input.addEventListener('input', function() {
            validateField(this);
        });
        
        input.addEventListener('blur', function() {
            validateField(this);
        });
    });

    function validateField(field) {
        const errorMsg = field.parentElement.querySelector('.error-message');
        let isValid = true;

        if (field.type === 'email') {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            isValid = emailRegex.test(field.value);
        } else {
            isValid = field.value.trim() !== '';
        }

        if (isValid) {
            field.classList.remove('invalid');
            if (errorMsg) errorMsg.style.display = 'none';
        } else {
            field.classList.add('invalid');
            if (errorMsg) errorMsg.style.display = 'block';
        }
        return isValid;
    }
    
    // Form submission with AJAX
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Final validation check
            let formIsValid = true;
            inputs.forEach(input => {
                if (!validateField(input)) formIsValid = false;
            });

            if (!formIsValid) return;
            
            const submitBtn = this.querySelector('.submit-btn');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Sending...';
            submitBtn.disabled = true;
            
            try {
                const formData = new FormData(this);
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Accept': 'application/json'
                    }
                });
                
                if (response.ok) {
                    submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Message Sent!';
                    submitBtn.style.background = 'var(--success)';
                    this.reset();
                    
                    // Log to analytics
                    logFormSubmission('contact');
                    
                    setTimeout(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.style.background = '';
                        submitBtn.disabled = false;
                    }, 5000);
                } else {
                    throw new Error('Form submission failed');
                }
            } catch (error) {
                console.error('Error:', error);
                submitBtn.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Error - Try Again';
                submitBtn.style.background = '#dc3545';
                
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    }

    // Session tracking (simplified)
    const sessionId = generateSessionId();
    
    // Track page views
    logPageView();

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.service-card, .blog-card, .stat-item').forEach(el => {
        observer.observe(el);
    });
});

// Generate unique session ID
function generateSessionId() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// Log page view
function logPageView() {
    const data = {
        page: window.location.pathname,
        title: document.title,
        timestamp: new Date().toISOString()
    };
    
    let pageViews = JSON.parse(localStorage.getItem('evansmathibe_pageviews') || '[]');
    pageViews.push(data);
    if (pageViews.length > 100) pageViews = pageViews.slice(-100);
    localStorage.setItem('evansmathibe_pageviews', JSON.stringify(pageViews));
}

// Log form submission
function logFormSubmission(type) {
    const data = {
        type: type,
        timestamp: new Date().toISOString()
    };
    
    let submissions = JSON.parse(localStorage.getItem('evansmathibe_submissions') || '[]');
    submissions.push(data);
    localStorage.setItem('evansmathibe_submissions', JSON.stringify(submissions));
}

// Add animation class
const animationStyle = document.createElement('style');
animationStyle.textContent = `
    .animate-in {
        animation: fadeInUp 0.6s ease forwards;
    }
    
    .service-card, .blog-card, .stat-item {
        opacity: 0;
        transform: translateY(30px);
    }
    
    .service-card:nth-child(1), .blog-card:nth-child(1), .stat-item:nth-child(1) { animation-delay: 0.1s; }
    .service-card:nth-child(2), .blog-card:nth-child(2), .stat-item:nth-child(2) { animation-delay: 0.2s; }
    .service-card:nth-child(3), .blog-card:nth-child(3), .stat-item:nth-child(3) { animation-delay: 0.3s; }
    .service-card:nth-child(4), .blog-card:nth-child(4), .stat-item:nth-child(4) { animation-delay: 0.4s; }
    .service-card:nth-child(5) { animation-delay: 0.5s; }
    .service-card:nth-child(6) { animation-delay: 0.6s; }
    .service-card:nth-child(7) { animation-delay: 0.7s; }
    .service-card:nth-child(8) { animation-delay: 0.8s; }
    
    @keyframes fadeInUp {
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(animationStyle);
