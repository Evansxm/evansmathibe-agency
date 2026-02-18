(function() {
  'use strict';

  const CONFIG = {
    endpoint: null, // Set to your analytics server URL or leave null for local storage only
    batchSize: 50,
    flushInterval: 30000,
    storageKey: 'evansAnalyticsQueue',
    sessionIdKey: 'evansAnalyticsSession',
    siteName: 'EvansMathibe Agency',
    debug: false
  };

  const state = {
    sessionId: null,
    pageLoadTime: Date.now(),
    lastFlushTime: Date.now(),
    sectionTimers: {},
    currentSection: null,
    sectionEnterTime: null,
    maxScrollDepth: 0,
    isInitialized: false,
    pendingEvents: []
  };

  function generateSessionId() {
    return 'sess_' + Date.now() + '_' + Math.random().toString(36).substring(2, 15);
  }

  function getSessionId() {
    let sessionId = sessionStorage.getItem(CONFIG.sessionIdKey);
    if (!sessionId) {
      sessionId = generateSessionId();
      sessionStorage.setItem(CONFIG.sessionIdKey, sessionId);
    }
    return sessionId;
  }

  function getDeviceType() {
    const ua = navigator.userAgent.toLowerCase();
    if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
      return 'tablet';
    }
    if (/mobile|iphone|ipod|android|blackberry|opera mini|iemobile/i.test(ua)) {
      return 'mobile';
    }
    return 'desktop';
  }

  function parseUserAgent() {
    const ua = navigator.userAgent;
    const deviceInfo = {
      userAgent: ua,
      browser: 'Unknown',
      browserVersion: 'Unknown',
      os: 'Unknown',
      osVersion: 'Unknown',
      deviceMake: 'Unknown',
      deviceModel: 'Unknown'
    };

    const browserPatterns = [
      { name: 'Edge', pattern: /Edge\/(\d+\.?\d*)/i },
      { name: 'Edg', pattern: /Edg\/(\d+\.?\d*)/i },
      { name: 'Chrome', pattern: /Chrome\/(\d+\.?\d*)/i },
      { name: 'Firefox', pattern: /Firefox\/(\d+\.?\d*)/i },
      { name: 'Safari', pattern: /Version\/(\d+\.?\d*).*Safari/i },
      { name: 'Opera', pattern: /OPR\/(\d+\.?\d*)/i },
      { name: 'IE', pattern: /MSIE\s(\d+\.?\d*)/i },
      { name: 'IE', pattern: /Trident.*rv:(\d+\.?\d*)/i }
    ];

    for (const bp of browserPatterns) {
      const match = ua.match(bp.pattern);
      if (match) {
        deviceInfo.browser = bp.name;
        deviceInfo.browserVersion = match[1];
        break;
      }
    }

    const osPatterns = [
      { name: 'Windows', pattern: /Windows NT\s?(\d+\.?\d*)/i },
      { name: 'macOS', pattern: /Mac OS X\s?(\d+[._]\d+[._]?\d*)/i },
      { name: 'iOS', pattern: /iPhone OS\s?(\d+[._]\d+)/i },
      { name: 'iOS', pattern: /iPad.*OS\s?(\d+[._]\d+)/i },
      { name: 'Android', pattern: /Android\s?(\d+\.?\d*)/i },
      { name: 'Linux', pattern: /Linux/i },
      { name: 'Chrome OS', pattern: /CrOS/i }
    ];

    for (const op of osPatterns) {
      const match = ua.match(op.pattern);
      if (match) {
        deviceInfo.os = op.name;
        if (match[1]) {
          deviceInfo.osVersion = match[1].replace(/_/g, '.');
        }
        break;
      }
    }

    const devicePatterns = [
      { make: 'Apple', model: 'iPhone', pattern: /iPhone/i },
      { make: 'Apple', model: 'iPad', pattern: /iPad/i },
      { make: 'Apple', model: 'Mac', pattern: /Macintosh/i },
      { make: 'Samsung', pattern: /Samsung\/([a-zA-Z0-9-]+)/i },
      { make: 'Samsung', pattern: /SM-([a-zA-Z0-9]+)/i },
      { make: 'Google', pattern: /Pixel/i },
      { make: 'Huawei', pattern: /Huawei/i },
      { make: 'OnePlus', pattern: /OnePlus/i },
      { make: 'Xiaomi', pattern: /Xiaomi|Redmi|MI/i },
      { make: 'LG', pattern: /LG/i },
      { make: 'Motorola', pattern: /Moto/i },
      { make: 'Nokia', pattern: /Nokia/i },
      { make: 'HTC', pattern: /HTC/i },
      { make: 'Sony', pattern: /Xperia/i }
    ];

    for (const dp of devicePatterns) {
      const match = ua.match(dp.pattern);
      if (match) {
        deviceInfo.deviceMake = dp.make;
        deviceInfo.deviceModel = dp.model || (match[1] ? match[1] : 'Unknown');
        break;
      }
    }

    if (deviceInfo.deviceMake === 'Unknown') {
      if (deviceInfo.os === 'macOS' || deviceInfo.os === 'iOS') {
        deviceInfo.deviceMake = 'Apple';
      } else if (deviceInfo.os === 'Android') {
        deviceInfo.deviceMake = 'Android Device';
      }
    }

    return deviceInfo;
  }

  function getScreenInfo() {
    return {
      screenWidth: screen.width,
      screenHeight: screen.height,
      viewportWidth: window.innerWidth,
      viewportHeight: window.innerHeight,
      pixelRatio: window.devicePixelRatio || 1,
      colorDepth: screen.colorDepth,
      orientation: screen.orientation ? screen.orientation.type : 'unknown'
    };
  }

  function getReferrer() {
    const referrer = document.referrer;
    if (!referrer) return { referrer: null, source: 'direct' };

    try {
      const url = new URL(referrer);
      const hostname = url.hostname;
      
      const searchEngines = ['google', 'bing', 'yahoo', 'duckduckgo', 'baidu', 'yandex'];
      const socialMedia = ['facebook', 'twitter', 'linkedin', 'instagram', 'youtube', 'tiktok', 'pinterest', 'reddit'];
      
      let source = 'other';
      if (searchEngines.some(se => hostname.includes(se))) {
        source = 'search';
      } else if (socialMedia.some(sm => hostname.includes(sm))) {
        source = 'social';
      } else if (hostname === window.location.hostname) {
        source = 'internal';
      }

      return {
        referrer: referrer,
        referrerDomain: hostname,
        source: source
      };
    } catch (e) {
      return { referrer: referrer, source: 'unknown' };
    }
  }

  async function getGeoLocation() {
    try {
      const response = await fetch('https://ipapi.co/json/', {
        method: 'GET',
        headers: { 'Accept': 'application/json' }
      });
      if (response.ok) {
        const data = await response.json();
        return {
          ip: data.ip || null,
          city: data.city || null,
          region: data.region || null,
          country: data.country_name || null,
          countryCode: data.country_code || null,
          latitude: data.latitude || null,
          longitude: data.longitude || null,
          timezone: data.timezone || null,
          isp: data.org || null
        };
      }
    } catch (e) {
      console.warn('Analytics: Geo location fetch failed');
    }
    return null;
  }

  function getScrollDepth() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrollPercent = scrollHeight > 0 ? Math.round((scrollTop / scrollHeight) * 100) : 0;
    return Math.min(100, Math.max(0, scrollPercent));
  }

  function trackEvent(eventType, data = {}) {
    const event = {
      id: 'evt_' + Date.now() + '_' + Math.random().toString(36).substring(2, 9),
      sessionId: state.sessionId,
      eventType: eventType,
      timestamp: Date.now(),
      pageUrl: window.location.href,
      pagePath: window.location.pathname,
      ...data
    };

    state.pendingEvents.push(event);
    saveToLocalStorage();

    if (state.pendingEvents.length >= CONFIG.batchSize) {
      flushEvents();
    }
  }

  function saveToLocalStorage() {
    try {
      localStorage.setItem(CONFIG.storageKey, JSON.stringify(state.pendingEvents));
    } catch (e) {
      console.warn('Analytics: Local storage save failed');
    }
  }

  function loadFromLocalStorage() {
    try {
      const stored = localStorage.getItem(CONFIG.storageKey);
      if (stored) {
        state.pendingEvents = JSON.parse(stored);
      }
    } catch (e) {
      state.pendingEvents = [];
    }
  }

  async function flushEvents() {
    if (state.pendingEvents.length === 0) return;

    const eventsToSend = [...state.pendingEvents];
    state.pendingEvents = [];
    state.lastFlushTime = Date.now();

    try {
      const response = await fetch(CONFIG.endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          events: eventsToSend,
          meta: {
            sentAt: Date.now(),
            userAgent: navigator.userAgent,
            url: window.location.href
          }
        }),
        keepalive: true
      });

      if (!response.ok) {
        state.pendingEvents = [...eventsToSend, ...state.pendingEvents];
        saveToLocalStorage();
      } else {
        localStorage.removeItem(CONFIG.storageKey);
      }
    } catch (e) {
      state.pendingEvents = [...eventsToSend, ...state.pendingEvents];
      saveToLocalStorage();
    }
  }

  function setupClickListener() {
    document.addEventListener('click', function(e) {
      const target = e.target;
      const clickData = {
        tagName: target.tagName.toLowerCase(),
        className: target.className || '',
        id: target.id || '',
        text: target.innerText ? target.innerText.substring(0, 100) : '',
        href: target.href || target.closest('a')?.href || '',
        x: e.clientX,
        y: e.clientY,
        path: getElementPath(target)
      };

      trackEvent('click', clickData);
    }, { passive: true });
  }

  function getElementPath(element) {
    const path = [];
    let current = element;
    
    while (current && current !== document.body) {
      let selector = current.tagName.toLowerCase();
      if (current.id) {
        selector += '#' + current.id;
      } else if (current.className && typeof current.className === 'string') {
        selector += '.' + current.className.split(' ').filter(c => c).join('.');
      }
      path.unshift(selector);
      current = current.parentElement;
    }
    
    return path.join(' > ');
  }

  function setupScrollTracking() {
    let scrollTimeout;
    
    window.addEventListener('scroll', function() {
      if (scrollTimeout) return;
      
      scrollTimeout = setTimeout(function() {
        scrollTimeout = null;
        const currentDepth = getScrollDepth();
        
        if (currentDepth > state.maxScrollDepth) {
          state.maxScrollDepth = currentDepth;
          
          const milestones = [25, 50, 75, 90, 100];
          for (const milestone of milestones) {
            if (currentDepth >= milestone) {
              trackEvent('scroll_depth', { depth: milestone, actualDepth: currentDepth });
            }
          }
        }
      }, 100);
    }, { passive: true });
  }

  function setupSectionTracking() {
    const sections = document.querySelectorAll('section, [data-section], [data-track-section], main, article, .section, #about, #services, #contact, #portfolio, #team');
    
    if (sections.length === 0) return;

    const observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        const sectionId = entry.target.id || 
                         entry.target.getAttribute('data-section') || 
                         entry.target.className || 
                         entry.target.tagName.toLowerCase();
        
        if (entry.isIntersecting) {
          state.sectionEnterTime = Date.now();
          state.currentSection = sectionId;
          trackEvent('section_enter', { section: sectionId });
        } else if (state.currentSection === sectionId && state.sectionEnterTime) {
          const timeSpent = Date.now() - state.sectionEnterTime;
          trackEvent('section_exit', { 
            section: sectionId, 
            timeSpentMs: timeSpent 
          });
          
          if (!state.sectionTimers[sectionId]) {
            state.sectionTimers[sectionId] = 0;
          }
          state.sectionTimers[sectionId] += timeSpent;
          
          state.currentSection = null;
          state.sectionEnterTime = null;
        }
      });
    }, {
      threshold: 0.3,
      rootMargin: '0px'
    });

    sections.forEach(function(section) {
      observer.observe(section);
    });
  }

  function setupUnloadTracking() {
    window.addEventListener('beforeunload', function() {
      if (state.currentSection && state.sectionEnterTime) {
        const timeSpent = Date.now() - state.sectionEnterTime;
        if (!state.sectionTimers[state.currentSection]) {
          state.sectionTimers[state.currentSection] = 0;
        }
        state.sectionTimers[state.currentSection] += timeSpent;
      }

      trackEvent('page_exit', {
        totalTimeOnPageMs: Date.now() - state.pageLoadTime,
        maxScrollDepth: state.maxScrollDepth,
        sectionsVisited: Object.keys(state.sectionTimers),
        sectionTimes: state.sectionTimers
      });

      flushEvents();
    });
  }

  function setupVisibilityTracking() {
    document.addEventListener('visibilitychange', function() {
      if (document.hidden) {
        trackEvent('page_hidden', {
          timeOnPageMs: Date.now() - state.pageLoadTime
        });
      } else {
        trackEvent('page_visible');
      }
    });
  }

  async function initialize() {
    if (state.isInitialized) return;
    state.isInitialized = true;

    state.sessionId = getSessionId();
    loadFromLocalStorage();

    const deviceInfo = parseUserAgent();
    const screenInfo = getScreenInfo();
    const referrerInfo = getReferrer();
    const geoInfo = await getGeoLocation();

    const sessionStartEvent = {
      eventType: 'session_start',
      sessionId: state.sessionId,
      timestamp: state.pageLoadTime,
      pageUrl: window.location.href,
      pagePath: window.location.pathname,
      pageTitle: document.title,
      deviceType: getDeviceType(),
      device: deviceInfo,
      screen: screenInfo,
      referrer: referrerInfo,
      geo: geoInfo,
      language: navigator.language,
      cookiesEnabled: navigator.cookieEnabled,
      doNotTrack: navigator.doNotTrack
    };

    state.pendingEvents.push(sessionStartEvent);

    setupClickListener();
    setupScrollTracking();
    setupSectionTracking();
    setupUnloadTracking();
    setupVisibilityTracking();

    setInterval(flushEvents, CONFIG.flushInterval);

    setTimeout(function() {
      setupSectionTracking();
    }, 1000);
  }

  function waitForDOMContentLoaded() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initialize);
    } else {
      initialize();
    }
  }

  waitForDOMContentLoaded();

  window.EvansMathibeAnalytics = {
    trackEvent: trackEvent,
    flushEvents: flushEvents,
    getSessionId: function() { return state.sessionId; },
    getConfig: function() { return { ...CONFIG }; },
    setEndpoint: function(url) { CONFIG.endpoint = url; }
  };

})();
