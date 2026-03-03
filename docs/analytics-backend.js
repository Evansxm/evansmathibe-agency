// Backend Data Archive System for EvansMathibe Agency
// Collects visitor data and archives it via email and GitHub

(function() {
    'use strict';
    
    // Configuration
    const CONFIG = {
        emailEndpoint: 'https://formsubmit.co/evans.mathibe@mail.com',
        githubRepo: 'Evansxm/evansmathibe-agency',
        archiveInterval: 5 * 60 * 1000, // 5 minutes
        batchSize: 10
    };
    
    // Data Archive System
    const DataArchive = {
        init: function() {
            this.sessionId = this.generateSessionId();
            this.visitorData = this.collectVisitorInfo();
            this.activityLog = [];
            
            this.startArchiving();
            
            window.addEventListener('beforeunload', () => {
                this.finalizeSession();
            });
            
            console.log('[EvansMathibe Analytics] Archive system initialized');
        },
        
        generateSessionId: function() {
            return 'evans_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        },
        
        collectVisitorInfo: function() {
            const ua = navigator.userAgent;
            const width = window.innerWidth;
            const height = window.innerHeight;
            
            let deviceType = 'Desktop';
            if (/Mobile|Android|iPhone/i.test(ua)) {
                deviceType = 'Mobile';
            } else if (/iPad|Tablet/i.test(ua) || (width > 768 && width < 1024)) {
                deviceType = 'Tablet';
            }
            
            let browser = 'Unknown';
            if (ua.includes('Chrome')) browser = 'Chrome';
            else if (ua.includes('Safari')) browser = 'Safari';
            else if (ua.includes('Firefox')) browser = 'Firefox';
            else if (ua.includes('Edge')) browser = 'Edge';
            
            let os = 'Unknown';
            if (ua.includes('Windows')) os = 'Windows';
            else if (ua.includes('Mac')) os = 'MacOS';
            else if (ua.includes('Linux')) os = 'Linux';
            else if (ua.includes('Android')) os = 'Android';
            else if (ua.includes('iOS')) os = 'iOS';
            
            return {
                sessionId: this.sessionId,
                timestamp: new Date().toISOString(),
                date: new Date().toLocaleDateString(),
                time: new Date().toLocaleTimeString(),
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                url: window.location.href,
                referrer: document.referrer || 'Direct',
                deviceType: deviceType,
                browser: browser,
                os: os,
                screenResolution: screen.width + 'x' + screen.height,
                viewport: width + 'x' + height,
                language: navigator.language,
                platform: navigator.platform,
                userAgent: ua.substring(0, 100),
                cookiesEnabled: navigator.cookieEnabled,
                online: navigator.onLine
            };
        },
        
        logActivity: function(type, details) {
            this.activityLog.push({
                timestamp: new Date().toISOString(),
                type: type,
                details: details,
                section: this.getCurrentSection()
            });
            
            this.storeTempData();
        },
        
        getCurrentSection: function() {
            const sections = ['home', 'services', 'about', 'projects', 'gallery', 'blog', 'contact'];
            for (const section of sections) {
                const el = document.getElementById(section);
                if (el) {
                    const rect = el.getBoundingClientRect();
                    if (rect.top >= 0 && rect.top <= window.innerHeight / 2) {
                        return section;
                    }
                }
            }
            return 'unknown';
        },
        
        storeTempData: function() {
            const data = {
                visitor: this.visitorData,
                activities: this.activityLog,
                lastUpdate: new Date().toISOString()
            };
            localStorage.setItem('evans_archive_temp', JSON.stringify(data));
        },
        
        archiveViaEmail: function(data) {
            const emailData = new FormData();
            emailData.append('_subject', `EVANSMATHIBE ANALYTICS: ${data.visitor.date} ${data.visitor.time}`);
            emailData.append('_captcha', 'false');
            emailData.append('_template', 'table');
            
            emailData.append('Session ID', data.visitor.sessionId);
            emailData.append('Date', data.visitor.date);
            emailData.append('Time', data.visitor.time);
            emailData.append('Timezone', data.visitor.timezone);
            emailData.append('Device Type', data.visitor.deviceType);
            emailData.append('Browser', data.visitor.browser);
            emailData.append('OS', data.visitor.os);
            emailData.append('Screen', data.visitor.screenResolution);
            emailData.append('Viewport', data.visitor.viewport);
            emailData.append('Language', data.visitor.language);
            emailData.append('Referrer', data.visitor.referrer);
            emailData.append('Online', data.visitor.online ? 'Yes' : 'No');
            
            const pageViews = data.activities.filter(a => a.type === 'page_view').length;
            const clicks = data.activities.filter(a => a.type === 'click').length;
            const formInteractions = data.activities.filter(a => a.type === 'form').length;
            
            emailData.append('Pages Viewed', pageViews);
            emailData.append('Total Clicks', clicks);
            emailData.append('Form Interactions', formInteractions);
            emailData.append('Time on Site', this.calculateTimeOnSite());
            emailData.append('Activity Log (JSON)', JSON.stringify(data.activities.slice(-20)));
            
            fetch(CONFIG.emailEndpoint, {
                method: 'POST',
                body: emailData
            }).then(response => {
                console.log('[EvansMathibe Analytics] Data archived to email');
            }).catch(error => {
                console.error('[EvansMathibe Analytics] Email archive failed:', error);
            });
        },
        
        calculateTimeOnSite: function() {
            const start = new Date(this.visitorData.timestamp);
            const now = new Date();
            const diff = Math.floor((now - start) / 1000);
            const minutes = Math.floor(diff / 60);
            const seconds = diff % 60;
            return `${minutes}m ${seconds}s`;
        },
        
        startArchiving: function() {
            setInterval(() => {
                const data = {
                    visitor: this.visitorData,
                    activities: this.activityLog
                };
                
                if (this.activityLog.length > 0) {
                    this.archiveViaEmail(data);
                    console.log('[EvansMathibe Analytics] Data archived');
                }
            }, CONFIG.archiveInterval);
            
            this.setupEventTracking();
        },
        
        setupEventTracking: function() {
            document.addEventListener('click', (e) => {
                const target = e.target.closest('a, button, .btn');
                if (target) {
                    this.logActivity('click', {
                        element: target.tagName,
                        text: target.textContent?.substring(0, 50),
                        href: target.href || ''
                    });
                }
            });
            
            document.querySelectorAll('form').forEach(form => {
                form.addEventListener('submit', () => {
                    this.logActivity('form', {
                        formType: form.querySelector('[name="_subject"]')?.value || 'Unknown'
                    });
                });
            });
            
            const sections = document.querySelectorAll('section[id]');
            const sectionObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting && entry.intersectionRatio > 0.5) {
                        this.logActivity('page_view', {
                            section: entry.target.id
                        });
                    }
                });
            }, { threshold: 0.5 });
            
            sections.forEach(section => sectionObserver.observe(section));
        },
        
        finalizeSession: function() {
            const data = {
                visitor: this.visitorData,
                activities: this.activityLog,
                finalTimestamp: new Date().toISOString()
            };
            
            const emailData = new FormData();
            emailData.append('_subject', `EVANSMATHIBE SESSION END: ${data.visitor.sessionId}`);
            emailData.append('_captcha', 'false');
            emailData.append('Session ID', data.visitor.sessionId);
            emailData.append('Duration', this.calculateTimeOnSite());
            emailData.append('Total Activities', data.activities.length);
            emailData.append('Full Data', JSON.stringify(data));
            
            if (navigator.sendBeacon) {
                navigator.sendBeacon(CONFIG.emailEndpoint, emailData);
            }
        }
    };
    
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => DataArchive.init());
    } else {
        DataArchive.init();
    }
    
    window.EvansAnalytics = DataArchive;
})();
