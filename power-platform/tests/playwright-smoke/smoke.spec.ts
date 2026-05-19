import { test, expect } from "@playwright/test";

const appUrl = process.env.MCHS_POWER_APP_URL;

test.describe("MCHS Power Platform runtime smoke", () => {
  test.skip(!appUrl, "MCHS_POWER_APP_URL is required for live NSW smoke tests");

  test("authorized user can open orchestration app", async ({ page }) => {
    await page.goto(appUrl!);
    await expect(page).toHaveTitle(/Power Apps|MCHS|Microcosting/i);
  });
});
