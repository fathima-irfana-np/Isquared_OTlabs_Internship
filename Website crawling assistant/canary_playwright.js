const { chromium } = require('playwright');

(async () => {
    console.log("Starting canary test...");
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    try {
        console.log("Navigating to calculator.net...");
        await page.goto('https://www.calculator.net/scientific-calculator.html', { timeout: 30000 });
        const title = await page.title();
        console.log(`Page title: ${title}`);
        if (title.includes('Scientific Calculator')) {
            console.log("CANARY_SUCCESS");
        } else {
            console.log("CANARY_FAILURE: title mismatch");
        }
    } catch (e) {
        console.error(`CANARY_ERROR: ${e.message}`);
    } finally {
        await browser.close();
        console.log("Browser closed.");
    }
})();
