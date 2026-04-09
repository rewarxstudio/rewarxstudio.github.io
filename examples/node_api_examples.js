/**
 * Rewarx Batch API — Node.js Examples
 *
 * Covers the 3 most common production use cases:
 *  1. Background removal (Amazon-compliant)
 *  2. Ecommerce detail grid generation (8-panel)
 *  3. Commercial Ad Poster generation
 *
 * Docs: https://rewarxstudio.github.io/docs/api-quickstart
 * Sign Up: https://www.rewarx.com
 *
 * Install deps: npm install node-fetch form-data
 */

const FormData = require("form-data");
const fs = require("fs");
const fetch = require("node-fetch"); // npm install node-fetch@2

const API_KEY = "YOUR_API_KEY_HERE";
const MERCHANT_ID = "YOUR_MERCHANT_ID_HERE";
const BASE_URL = "https://api.rewarxstudio.com/api/v1/batch.php";

const defaultHeaders = {
  Authorization: `Bearer ${API_KEY}`,
  "X-Merchant-Id": MERCHANT_ID,
};

// ─────────────────────────────────────────────────────────────
// Helper: send request with form payload
// ─────────────────────────────────────────────────────────────
async function sendRequest(payload) {
  const form = new FormData();
  for (const [key, value] of Object.entries(payload)) {
    form.append(key, String(value));
  }

  const response = await fetch(BASE_URL, {
    method: "POST",
    headers: { ...defaultHeaders, ...form.getHeaders() },
    body: form,
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API Error ${response.status}: ${text}`);
  }
  return response.json();
}

// ─────────────────────────────────────────────────────────────
// 1. Background Removal — Upload local file
// ─────────────────────────────────────────────────────────────
async function removeBackgroundFromFile(imagePath, platform = "shopify") {
  const form = new FormData();
  form.append("action", "bg-remove");
  form.append("resolution", "2K");
  form.append("image_files[]", fs.createReadStream(imagePath));
  form.append("options[platform]", platform);
  form.append("options[optimize_repair]", "true");
  form.append("options[preserve_edges]", "true");

  const response = await fetch(BASE_URL, {
    method: "POST",
    headers: { ...defaultHeaders, ...form.getHeaders() },
    body: form,
  });

  if (!response.ok) throw new Error(`API Error: ${response.status}`);
  const result = await response.json();
  console.log("Background removed:", result);
  return result;
}

// ─────────────────────────────────────────────────────────────
// 2. Ecommerce Detail Grid — 8-panel product page content
// ─────────────────────────────────────────────────────────────
async function generateEcommerceGrid(imageUrl, options = {}) {
  const {
    country = "United States of America",
    platform = "Amazon",
    language = "en",
    themePrompt = "Clean minimalist product photography",
    webhookUrl,
  } = options;

  const payload = {
    action: "ecommerce-detail",
    resolution: "2K",
    "image_urls[]": imageUrl,
    "options[country]": country,
    "options[platform]": platform,
    "options[language]": language,
    "options[theme_prompt]": themePrompt,
    "options[additional_requirements]": "Bold modern typography, high-contrast backgrounds",
  };

  if (webhookUrl) payload["webhook_url"] = webhookUrl;

  const result = await sendRequest(payload);
  console.log("Ecommerce grid job:", result);
  return result;
}

// ─────────────────────────────────────────────────────────────
// 3. Commercial Ad Poster — Generate with URL + optional logo
// ─────────────────────────────────────────────────────────────
async function generateAdPoster(productImageUrl, adOptions = {}) {
  const {
    headline = "Premium Quality",
    subline = "Designed for those who demand more",
    cta = "Shop Now",
    visualPrompt = "Dark luxury background, cinematic depth of field",
    style = "Modern Minimalist",
    purpose = "New Launch",
    aspectRatio = "1:1",
    webhookUrl,
  } = adOptions;

  const payload = {
    action: "ad-poster",
    resolution: "2K",
    aspect_ratio: aspectRatio,
    "image_urls[]": productImageUrl,
    "options[headline]": headline,
    "options[subline]": subline,
    "options[cta]": cta,
    "options[visual_prompt]": visualPrompt,
    "options[style]": style,
    "options[purpose]": purpose,
  };

  if (webhookUrl) payload["webhook_url"] = webhookUrl;

  const result = await sendRequest(payload);
  console.log("Ad poster job:", result);
  return result;
}

// ─────────────────────────────────────────────────────────────
// Main — Run examples
// ─────────────────────────────────────────────────────────────
(async () => {
  try {
    // Example 1: Upload local file for bg removal
    // await removeBackgroundFromFile("./product.jpg", "amazon");

    // Example 2: Generate Amazon listing detail grid
    await generateEcommerceGrid(
      "https://yourstore.com/products/wireless-earbuds.jpg",
      {
        country: "United States of America",
        platform: "Amazon",
        language: "en",
        themePrompt: "Premium tech product on sleek dark surface",
      }
    );

    // Example 3: Generate an Instagram-ready ad creative
    await generateAdPoster(
      "https://yourstore.com/products/sneakers.jpg",
      {
        headline: "Step Up Your Game",
        subline: "Lightweight. Durable. Iconic.",
        cta: "Shop the Drop",
        visualPrompt: "Vibrant gradient background, dynamic energy, lifestyle athletics",
        style: "Bold & Dynamic",
        purpose: "Seasonal Sale",
        aspectRatio: "1:1",
      }
    );
  } catch (err) {
    console.error("Error:", err.message);
  }
})();
