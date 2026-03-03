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
            dots: false, // Removed dots as per instruction
            infinite: true,
            speed: 1000, // Smooth transition speed
            slidesToShow: 1,
            slidesToScroll: 1,
            adaptiveHeight: true,
            autoplay: true,
            autoplaySpeed: 3000, // 3 seconds interval
            fade: true,
            cssEase: 'linear',
            arrows: false,
            pauseOnHover: false,
            pauseOnFocus: false
        });
    }

    // Form Real-time Validation
    const contactForm = document.getElementById('contactForm');
    const inputs = contactForm.querySelectorAll('.form-control[required]');

    if (inputs.length) {
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                validateField(this);
            });
            
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    }

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
                
                const result = await response.json();
                
                if (response.ok && (result.success === "true" || result.success === true)) {
                    submitBtn.innerHTML = '<i class="fas fa-check me-2"></i>Message Sent!';
                    submitBtn.style.background = 'var(--success)';
                    this.reset();
                    
                    setTimeout(() => {
                        submitBtn.innerHTML = originalText;
                        submitBtn.style.background = '';
                        submitBtn.disabled = false;
                    }, 5000);
                } else {
                    throw new Error(result.message || 'Form submission failed');
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
