# ✨ Rewarx Studio — AI Visual Content API & E-Commerce Tools

> **The world's most powerful browser-based AI-photography factory for e-commerce.**  
> We help Shopify, Amazon and enterprise merchants generate studio-quality product images in seconds — no DSLR, no model, no production crew required.

🌐 **Website**: [https://www.rewarx.com](https://www.rewarx.com)  
📘 **API Docs**: [→ Quickstart Guide](./docs/api-quickstart)  
🤝 **Partners**: [→ Affiliate Rewards Program](./reward-program-guide)

---

## 🏆 Why Rewarx?

| Traditional Photoshoot | ✅ Rewarx AI Studio |
|---|---|
| $800–$5,000 per SKU | From $0.10 per image |
| 2–4 weeks turnaround | Under 30 seconds |
| Requires agency coordination | Browser-based, instant |
| Re-shoot for every variant | Batch all variants at once |
| Limited to local models/styles | Any ethnicity, style, scene |

Rewarx is used by thousands of merchants on Shopify, Amazon, Etsy, TikTok Shop, and Temu to scale their visual catalog production without scaling their budget.

---

## 🚀 Available AI Tools (Free to Try)

### 👗 Apparel & Fashion
* **[AI Fashion Model Studio](https://www.rewarx.com/tools/model-studio.html)**  
  Drop your flat-lay apparel image → AI generates a photorealistic human model wearing it. Choose ethnicity, pose, background, and lighting — all in-browser.

* **[Virtual Try-On / Style Transfer](https://www.rewarx.com/tools/virtual-model-try-on.html)**  
  Combine a garment with a real model photo or a vibe reference image. The AI preserves the exact garment silhouette while cloning the aesthetic scene.

* **[Ghost Mannequin Generator](https://www.rewarx.com/tools/ghost-mannequin.html)**  
  Upload an item on a physical hanger or mannequin — our AI fills in the neck, shoulder, and body volume so it looks perfectly worn. Industry-standard for fashion catalogs.

### 📦 Product Photography
* **[AI Product Photography Studio](https://www.rewarx.com/tools/photography-studio.html)**  
  Transform raw product images into commercial lifestyle scenes. Choose from 20+ aesthetic presets – Minimalist, Luxury, Cyberpunk, Rustic. Add props, models, or atmospheric effects automatically.

* **[Group Shot Studio](https://www.rewarx.com/tools/group-shot-studio.html)**  
  Upload up to 8 product images → AI intelligently composes a styled group flatlay or lifestyle collage with custom backgrounds and lighting.

* **[AI Mockup Generator](https://www.rewarx.com/tools/mockup-generator.html)**  
  Apply flat pattern designs or logos to real physical items (mugs, apparel, packaging). Two modes: `text` (AI generates the object) or `image` (apply to your template image).

* **[AI Background Remover](https://www.rewarx.com/tools/ai-background-remover.html)**  
  Neural-precision background removal with automatic edge repair and shadow normalization. Supports platform presets: `amazon`, `shopify`, `etsy` for compliant white-background outputs.

### 📢 Marketing & Ads
* **[Commercial Ad Poster Generator](https://www.rewarx.com/tools/commercial-ad-poster.html)**  
  Feed it your product images + logo → AI generates on-brand advertising creatives with integrated headlines, subcopies, and CTAs. Supports multiple campaign styles and output dimensions.

---

## 💻 Batch API for Developers

We expose a production-grade **Batch Processing API** at:

```
POST https://api.rewarxstudio.com/api/v1/batch.php
Authorization: Bearer YOUR_API_KEY
X-Merchant-Id: YOUR_MERCHANT_ID
```

### ⚡ Supports 11 AI Actions via a Single Endpoint

| Action Name | Description |
|---|---|
| `photography` | Commercial product photo generation |
| `model` | AI model studio (full pipeline) |
| `ai-try-on` | Virtual garment try-on with pose control |
| `bg-remove` | Smart background removal/replacement |
| `mockup` | Pattern-to-3D mockup (text or image mode) |
| `ad-poster` | Advertising creative generation |
| `ghost-mannequin` | Hollow garment body-fill rendering |
| `lookalike` | Style transfer / scene vibe cloning |
| `ecommerce-detail` | 8-panel detail grid generator (multi-market) |
| `group-shot` | Multi-product scene composition |
| `studio-template` | Background scene cloning to your product |

### 🔧 Quick Python Example — Remove Background

```python
import requests

response = requests.post(
    "https://api.rewarxstudio.com/api/v1/batch.php",
    headers={
        "Authorization": "Bearer YOUR_API_KEY",
        "X-Merchant-Id": "YOUR_MERCHANT_ID"
    },
    data={
        "action": "bg-remove",
        "resolution": "2K",
        "image_urls[]": "https://yourstore.com/product.jpg",
        "options[bg_prompt]": "pure white background",
        "options[platform]": "amazon",
        "options[optimize_repair]": "true",
        "webhook_url": "https://yourstore.com/webhook/done"
    }
)

result = response.json()
print("Image URL:", result.get("output_url"))
```

➡️ **[See full API quickstart with all 11 action types →](./docs/api-quickstart)**

---

## 🔗 Platform Integrations

* **Shopify**: Install the official [Rewarx Shopify App](https://www.rewarx.com) for one-click catalog processing.
* **Amazon**: Use the `bg-remove` API action with `platform=amazon` for instant compliant PDP-ready images.
* **Headless / Custom**: Use the full Batch API to automate any workflow in your pipeline.

---

## 🤝 Partner with Us — Earn Recurring Commissions

Join the **Rewarx Partner Rewards Program** on **Impact.com** — the world's leading partnership management platform.

Whether you're a:
- 📊 E-commerce agency building client stores
- 📝 Content creator reviewing SaaS tools
- 👨‍💻 Developer integrating AI pipelines for clients
- 🛍️ Consultant advising brands on catalog operations

...you can earn **significant recurring commissions** for every merchant you introduce to Rewarx.

👉 **[Read the Complete Partner Rewards Guide](./reward-program-guide)**

---

## 📧 Contact & Support

| | |
|---|---|
| **Website** | [www.rewarx.com](https://www.rewarx.com) |
| **API Support** | studio@rewarx.com |
| **Partnership** | Via [Impact.com Partner Portal](https://www.rewarx.com) |

---

*Rewarx Studio is an AI company building the future of ecommerce visualisation for global merchants. All tools are available to try for free at [rewarx.com](https://www.rewarx.com).*
