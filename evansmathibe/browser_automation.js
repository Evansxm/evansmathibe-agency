const { chromium } = require('playwright');

async function updateBusinessProfile() {
    console.log('🔧 Starting browser...');
    
    // Use existing Chromium from ms-playwright cache
    const browserPath = '/home/ev/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome';
    
    const browser = await chromium.launch({
        executablePath: browserPath,
        headless: false,
        args: ['--no-sandbox', '--disable-dev-shm-usage']
    });
    
    console.log('✅ Browser launched!');
    
    const context = await browser.newContext({
        viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    
    try {
        // Go to Google Business Profile
        console.log('📍 Going to Google Business Profile...');
        await page.goto('https://business.google.com/manage/', { timeout: 30000 });
        await page.waitForLoadState('networkidle', { timeout: 15000 });
        
        console.log(`URL: ${page.url()}`);
        console.log(`Title: ${page.title()}`);
        
        // Wait for user to complete manually if needed
        console.log('\n⏳ Keeping browser open for manual completion...');
        console.log('Please:');
        console.log('1. Click on your business');
        console.log('2. Click Edit profile');
        console.log('3. Update name to: Evans Mathibe | Mone | TYC');
        console.log('\nPress Ctrl+C when done, or wait 60 seconds...');
        
        await page.waitForTimeout(60000);
        
    } catch (error) {
        console.error('❌ Error:', error.message);
    } finally {
        await browser.close();
        console.log('✅ Browser closed');
    }
}

updateBusinessProfile();
