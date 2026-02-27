// EvansMathibe Agency - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Navbar scroll effect
    const navbar = document.getElementById('navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
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
    $('.image-slider').slick({
        dots: false,
        infinite: true,
        speed: 800,
        slidesToShow: 1,
        slidesToScroll: 1,
        autoplay: true,
        autoplaySpeed: 5000,
        fade: true,
        cssEase: 'cubic-bezier(0.4, 0, 0.2, 1)',
        arrows: false,
        draggable: false,
        swipe: false,
        touchMove: false,
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

    // Form submission with AJAX
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
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
                    submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Sent Successfully!';
                    submitBtn.style.background = 'linear-gradient(135deg, #28a745, #20c997)';
                    this.reset();
                    
                    // Log to analytics
                    logFormSubmission('contact');
                    
                    setTimeout(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.style.background = '';
                        submitBtn.disabled = false;
                    }, 3000);
                } else {
                    throw new Error('Form submission failed');
                }
            } catch (error) {
                console.error('Error:', error);
                submitBtn.innerHTML = '<i class="fas fa-exclamation-triangle me-2"></i>Error - Try Again';
                submitBtn.style.background = 'linear-gradient(135deg, #dc3545, #c82333)';
                
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.style.background = '';
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    }

    // Session tracking
    const sessionId = generateSessionId();
    const sessionStart = Date.now();
    
    window.addEventListener('beforeunload', function() {
        const sessionDuration = Math.floor((Date.now() - sessionStart) / 1000);
        logSession(sessionId, sessionDuration);
    });

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
        timestamp: new Date().toISOString(),
        referrer: document.referrer,
        screenSize: `${window.screen.width}x${window.screen.height}`,
        userAgent: navigator.userAgent
    };
    
    // Store in localStorage for daily email summary
    let pageViews = JSON.parse(localStorage.getItem('evansmathibe_pageviews') || '[]');
    pageViews.push(data);
    
    // Keep only last 100 entries
    if (pageViews.length > 100) {
        pageViews = pageViews.slice(-100);
    }
    
    localStorage.setItem('evansmathibe_pageviews', JSON.stringify(pageViews));
    
    console.log('Page view logged:', data);
}

// Log form submission
function logFormSubmission(type) {
    const data = {
        type: type,
        timestamp: new Date().toISOString(),
        page: window.location.pathname
    };
    
    let submissions = JSON.parse(localStorage.getItem('evansmathibe_submissions') || '[]');
    submissions.push(data);
    localStorage.setItem('evansmathibe_submissions', JSON.stringify(submissions));
    
    console.log('Form submission logged:', data);
}

// Log session on exit
function logSession(sessionId, duration) {
    const data = {
        sessionId: sessionId,
        duration: duration,
        page: window.location.pathname,
        timestamp: new Date().toISOString()
    };
    
    let sessions = JSON.parse(localStorage.getItem('evansmathibe_sessions') || '[]');
    sessions.push(data);
    localStorage.setItem('evansmathibe_sessions', JSON.stringify(sessions));
    
    // Check if we should send daily email
    checkDailyEmail();
}

// Check if daily email should be sent
function checkDailyEmail() {
    const lastEmail = localStorage.getItem('evansmathibe_last_email');
    const now = new Date();
    
    // Send email once per day (at 6 PM)
    if (now.getHours() >= 18 && (!lastEmail || new Date(lastEmail).getDate() !== now.getDate())) {
        sendDailySummary();
    }
}

// Send daily summary via EmailJS (placeholder - configure with your EmailJS credentials)
function sendDailySummary() {
    const pageViews = JSON.parse(localStorage.getItem('evansmathibe_pageviews') || '[]');
    const submissions = JSON.parse(localStorage.getItem('evansmathibe_submissions') || '[]');
    const sessions = JSON.parse(localStorage.getItem('evansmathibe_sessions') || '[]');
    
    const summary = {
        date: new Date().toISOString().split('T')[0],
        pageViews: pageViews.length,
        formSubmissions: submissions.length,
        totalSessions: sessions.length,
        avgSessionDuration: sessions.length > 0 
            ? Math.round(sessions.reduce((a, b) => a + b.duration, 0) / sessions.length) 
            : 0,
        pages: [...new Set(pageViews.map(p => p.page))].length
    };
    
    console.log('Daily Summary:', summary);
    
    // Store for EmailJS integration
    localStorage.setItem('evansmathibe_daily_summary', JSON.stringify(summary));
    localStorage.setItem('evansmathibe_last_email', new Date().toISOString());
    
    // Clear daily data after sending
    localStorage.removeItem('evansmathibe_pageviews');
    localStorage.removeItem('evansmathibe_submissions');
    localStorage.removeItem('evansmathibe_sessions');
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
    .service-card:nth-child(5), .blog-card:nth-child(5) { animation-delay: 0.5s; }
    .service-card:nth-child(6), .blog-card:nth-child(6) { animation-delay: 0.6s; }
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
