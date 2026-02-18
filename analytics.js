/**
 * EvansMathibe Website Analytics Tracker
 * Client-side analytics for GitHub Pages
 */

(function() {
    'use strict';
    
    const Analytics = {
        // Configuration
        storageKey: 'evans_analytics',
        sessionKey: 'evans_session',
        
        // Initialize
        init: function() {
            this.startSession();
            this.trackPageView();
            this.trackScrollDepth();
            this.trackClicks();
            this.trackTimeOnPage();
            this.setupBeforeUnload();
        },
        
        // Session management
        startSession: function() {
            let session = this.getStorage(this.sessionKey);
            if (!session) {
                session = {
                    id: this.generateId(),
                    start: Date.now(),
                    pages: []
                };
                this.setStorage(this.sessionKey, session);
            }
            return session;
        },
        
        getSession: function() {
            return this.getStorage(this.sessionKey) || this.startSession();
        },
        
        // Storage helpers
        getStorage: function(key) {
            try {
                const data = localStorage.getItem(key);
                return data ? JSON.parse(data) : null;
            } catch (e) {
                return null;
            }
        },
        
        setStorage: function(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
            } catch (e) {
                console.warn('Storage full or unavailable');
            }
        },
        
        // Generate unique ID
        generateId: function() {
            return 'evans_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        },
        
        // Device detection
        getDevice: function() {
            const ua = navigator.userAgent;
            if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
                return 'Tablet';
            }
            if (/Mobile|Android|iP(hone|od)|IEMobile|BlackBerry|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(ua)) {
                return 'Mobile';
            }
            return 'Desktop';
        },
        
        // Browser detection
        getBrowser: function() {
            const ua = navigator.userAgent;
            if (ua.indexOf('Firefox') > -1) return 'Firefox';
            if (ua.indexOf('Chrome') > -1) return 'Chrome';
            if (ua.indexOf('Safari') > -1) return 'Safari';
            if (ua.indexOf('MSIE') > -1 || ua.indexOf('Trident/') > -1) return 'IE';
            return 'Other';
        },
        
        // Get current page info
        getPageInfo: function() {
            return {
                url: window.location.href,
                path: window.location.pathname,
                title: document.title,
                referrer: document.referrer || 'direct'
            };
        },
        
        // Track page view
        trackPageView: function() {
            const session = this.getSession();
            const pageInfo = this.getPageInfo();
            
            const pageView = {
                url: pageInfo.path,
                title: pageInfo.title,
                timestamp: Date.now(),
                device: this.getDevice(),
                browser: this.getBrowser(),
                screenWidth: window.screen.width,
                language: navigator.language
            };
            
            session.pages.push(pageView);
            this.setStorage(this.sessionKey, session);
            
            // Send to local analytics storage
            this.saveToAnalytics(pageView);
        },
        
        // Track scroll depth
        trackScrollDepth: function() {
            let maxScroll = 0;
            const thresholds = [25, 50, 75, 100];
            const tracked = new Set();
            
            window.addEventListener('scroll', () => {
                const scrollPercent = Math.round(
                    (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100
                );
                
                thresholds.forEach(threshold => {
                    if (scrollPercent >= threshold && !tracked.has(threshold)) {
                        tracked.add(threshold);
                        this.trackEvent('scroll_depth', { depth: threshold });
                    }
                });
                
                maxScroll = Math.max(maxScroll, scrollPercent);
            });
        },
        
        // Track clicks
        trackClicks: function() {
            document.addEventListener('click', (e) => {
                const target = e.target.closest('a, button');
                if (target) {
                    this.trackEvent('click', {
                        type: target.tagName.toLowerCase(),
                        text: target.textContent?.trim().substring(0, 50),
                        href: target.href || null
                    });
                }
            });
        },
        
        // Track time on page
        trackTimeOnPage: function() {
            const startTime = Date.now();
            
            window.addEventListener('beforeunload', () => {
                const duration = Math.round((Date.now() - startTime) / 1000);
                this.trackEvent('time_on_page', { duration: duration });
            });
        },
        
        // Setup before unload
        setupBeforeUnload: function() {
            window.addEventListener('beforeunload', () => {
                this.finalizeSession();
            });
        },
        
        // Track custom event
        trackEvent: function(eventType, data = {}) {
            const event = {
                type: eventType,
                data: data,
                timestamp: Date.now(),
                url: window.location.pathname
            };
            
            // Save to analytics
            const analytics = this.getStorage(this.storageKey) || { events: [] };
            analytics.events = analytics.events || [];
            analytics.events.push(event);
            
            // Keep only last 100 events
            if (analytics.events.length > 100) {
                analytics.events = analytics.events.slice(-100);
            }
            
            this.setStorage(this.storageKey, analytics);
        },
        
        // Save to analytics storage
        saveToAnalytics: function(pageView) {
            const analytics = this.getStorage(this.storageKey) || { visits: [] };
            analytics.visits = analytics.visits || [];
            
            // Add page view
            analytics.visits.push({
                ...pageView,
                session: this.getSession().id
            });
            
            // Keep last 200 visits
            if (analytics.visits.length > 200) {
                analytics.visits = analytics.visits.slice(-200);
            }
            
            this.setStorage(this.storageKey, analytics);
        },
        
        // Finalize session
        finalizeSession: function() {
            const session = this.getSession();
            if (session) {
                session.end = Date.now();
                session.duration = session.end - session.start;
                
                // Get stored analytics and update
                const analytics = this.getStorage(this.storageKey) || {};
                analytics.sessions = analytics.sessions || [];
                analytics.sessions.push(session);
                
                // Keep last 50 sessions
                if (analytics.sessions.length > 50) {
                    analytics.sessions = analytics.sessions.slice(-50);
                }
                
                this.setStorage(this.storageKey, analytics);
            }
        },
        
        // Get analytics data (for export)
        getData: function() {
            return this.getStorage(this.storageKey);
        },
        
        // Export data as JSON
        exportData: function() {
            const data = this.getData();
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'evans_analytics_' + new Date().toISOString().split('T')[0] + '.json';
            a.click();
            URL.revokeObjectURL(url);
        },
        
        // Send data to owner via email
        sendReport: function() {
            const data = this.getData();
            const sessions = data?.sessions || [];
            const visits = data?.visits || [];
            
            // Calculate stats
            const totalVisits = visits.length;
            const uniqueSessions = new Set(sessions.map(s => s.id)).size;
            const totalDuration = sessions.reduce((sum, s) => sum + (s.duration || 0), 0);
            const avgDuration = totalDuration / sessions.length || 0;
            
            // Top pages
            const pageCounts = {};
            visits.forEach(v => {
                pageCounts[v.url] = (pageCounts[v.url] || 0) + 1;
            });
            
            // Devices
            const deviceCounts = {};
            visits.forEach(v => {
                deviceCounts[v.device] = (deviceCounts[v.device] || 0) + 1;
            });
            
            // Generate email
            const subject = encodeURIComponent('📊 Website Analytics Report - ' + new Date().toLocaleDateString());
            const body = encodeURIComponent(
                `📊 Website Analytics Report
=========================

📈 Summary:
- Total Page Views: ${totalVisits}
- Unique Visitors: ${uniqueSessions}
- Avg. Time on Site: ${Math.round(avgDuration)} seconds

📍 Top Pages:
${Object.entries(pageCounts).map(([page, count]) => `- ${page}: ${count}`).join('\n')}

📱 Devices:
${Object.entries(deviceCounts).map(([device, count]) => `- ${device}: ${count}`).join('\n')}

🌐 View full data attached.

---
EvansMathibe Analytics`
            );
            
            window.location.href = `mailto:evans.mathibe@mail.com?subject=${subject}&body=${body}`;
        },
        
        // Check if notification due (every 3 days)
        checkNotificationDue: function() {
            const lastNotification = localStorage.getItem('evans_last_notification');
            if (!lastNotification) return true;
            
            const daysSince = (Date.now() - parseInt(lastNotification)) / (1000 * 60 * 60 * 24);
            return daysSince >= 3;
        },
        
        // Request notification permission
        requestNotificationPermission: function() {
            if ('Notification' in window && Notification.permission === 'default') {
                Notification.requestPermission();
            }
        }
    };
    
    // Initialize on load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => Analytics.init());
    } else {
        Analytics.init();
    }
    
    // Expose to window
    window.EvansAnalytics = Analytics;
    
})();
