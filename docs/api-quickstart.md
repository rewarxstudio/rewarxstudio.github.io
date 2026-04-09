# Rewarx Batch API — Developer Quickstart Guide

> **Base URL**: `POST https://api.rewarxstudio.com/api/v1/batch.php`  
> **Auth**: `Authorization: Bearer <your_api_key>` + `X-Merchant-Id: <merchant_id>`

The Rewarx Batch API is designed for high-throughput e-commerce image production. A single endpoint handles all 11 AI generation types. Send a request, receive a webhook callback (or poll the job ID), and download your generated assets.

---

## Authentication

All requests must include two headers:

```http
Authorization: Bearer sk_live_xxxxxxxxxxxxxxxxxxxxxx
X-Merchant-Id: merchant_123456
```

Get your API key from the [Rewarx Dashboard](https://www.rewarx.com) after subscribing to a Business or Enterprise plan.

---

## Common Request Parameters

| Field | Type | Notes |
|---|---|---|
| `action` | string | **Required**. See supported actions below |
| `resolution` | string | `1K` / `2K` / `4K`. Default `1K` |
| `aspect_ratio` | string | `1:1` `3:4` `4:3` `9:16` `16:9`. Default `1:1` |
| `image_urls[]` | array | Public image URLs (use this OR `image_files[]`) |
| `image_files[]` | binary | Upload via multipart/form-data |
| `options[*]` | object | Action-specific parameters (see each action) |
| `webhook_url` | string | Optional HTTPS endpoint to receive completion callback |

---

## Quickstart: 5 Most Common Actions

### 1. Background Removal (`bg-remove`)
Best for: Amazon, Shopify, Etsy listing compliance.

```python
import requests

resp = requests.post(
    "https://api.rewarxstudio.com/api/v1/batch.php",
    headers={
        "Authorization": "Bearer YOUR_KEY",
        "X-Merchant-Id": "YOUR_MERCHANT_ID",
    },
    data={
        "action": "bg-remove",
        "resolution": "2K",
        "image_urls[]": "https://yourcdn.com/product.jpg",
        # Marketplace preset auto-configures aspect_ratio + bg
        "options[platform]": "amazon",  # or: shopify, etsy, none
        "options[optimize_repair]": "true",
        "options[preserve_edges]": "true",
        "webhook_url": "https://yoursite.com/api/webhook",
    }
)
print(resp.json())
```

---

### 2. AI Model Studio (`model`)
Best for: Apparel brands needing model lifestyle shots without a photoshoot.

```python
import requests

resp = requests.post(
    "https://api.rewarxstudio.com/api/v1/batch.php",
    headers={
        "Authorization": "Bearer YOUR_KEY",
        "X-Merchant-Id": "YOUR_MERCHANT_ID",
    },
    data={
        "action": "model",
        "resolution": "2K",
        "aspect_ratio": "3:4",
        "image_urls[]": "https://yourcdn.com/shirt_flatlay.jpg",
        "options[requirements]": "Elegant woman, early 30s, natural makeup",
        "options[action]": "holding product near chest, relaxed smile",
        "options[background]": "Modern sunlit apartment, minimalist white walls",
        "options[visual_prompt]": "High-end fashion editorial, Vogue cover quality",
        "options[aesthetic]": "Minimalist",
        "webhook_url": "https://yoursite.com/api/webhook",
    }
)
print(resp.json())
```

---

### 3. Virtual Try-On (`ai-try-on`)
Best for: Garment retailers wanting to show items on diverse models without model hiring.

```python
import requests

resp = requests.post(
    "https://api.rewarxstudio.com/api/v1/batch.php",
    headers={
        "Authorization": "Bearer YOUR_KEY",
        "X-Merchant-Id": "YOUR_MERCHANT_ID",
    },
    data={
        "action": "ai-try-on",
        "resolution": "2K",
        "aspect_ratio": "3:4",
        "image_urls[]": "https://yourcdn.com/dress_product.jpg",
        "options[pose]": "standing-front",  # See POSE_OPTIONS below
        "options[model_description]": "Asian woman, mid-20s, slim build, natural makeup",
        "options[background]": "luxury-interior",  # See BG_OPTIONS below
        "options[lighting]": "soft-studio",
        "options[style]": "commercial fashion editorial",
        "options[generate_model]": "true",
        "webhook_url": "https://yoursite.com/api/webhook",
    }
)
print(resp.json())
```

**Available Poses**: `standing-front` `standing-side` `back-view` `three-quarter` `walking` `running` `sitting` `crouching` `hands-on-hips` `leaning`

**Available Backgrounds**: `studio-white` `minimal-gray` `urban-street` `luxury-interior` `modern-loft` `nature-park` `beach-sunset` `desert-dunes` `industrial-warehouse` `cyberpunk-city`

---

### 4. Ghost Mannequin (`ghost-mannequin`)
Best for: Sweaters, jackets, structured apparel where the wear shape must be shown cleanly.

```python
import requests

resp = requests.post(
    "https://api.rewarxstudio.com/api/v1/batch.php",
    headers={
        "Authorization": "Bearer YOUR_KEY",
        "X-Merchant-Id": "YOUR_MERCHANT_ID",
    },
    data={
        "action": "ghost-mannequin",
        "resolution": "2K",
        "aspect_ratio": "3:4",
        "image_urls[]": "https://yourcdn.com/jacket_on_mannequin.jpg",
        "options[angle]": "front",
        "options[auto_bg]": "true",  # AI generates commercial background
        "options[extra_requirements]": "preserve collar stitching and zipper detail",
        "webhook_url": "https://yoursite.com/api/webhook",
    }
)
print(resp.json())
```

---

### 5. Commercial Ad Poster (`ad-poster`)
Best for: Creating platform-ready social creatives from product images in bulk.

```python
import requests

resp = requests.post(
    "https://api.rewarxstudio.com/api/v1/batch.php",
    headers={
        "Authorization": "Bearer YOUR_KEY",
        "X-Merchant-Id": "YOUR_MERCHANT_ID",
    },
    data={
        "action": "ad-poster",
        "resolution": "2K",
        "aspect_ratio": "1:1",
        "image_urls[]": "https://yourcdn.com/product.jpg",
        "options[headline]": "Next-Gen Performance",
        "options[subline]": "Engineered for the modern athlete",
        "options[cta]": "Shop the Collection",
        "options[visual_prompt]": "dark luxury background, editorial lighting, cinematic depth",
        "options[style]": "Tech Sleek",
        "options[purpose]": "New Launch",
        "webhook_url": "https://yoursite.com/api/webhook",
    }
)
print(resp.json())
```

---

## Node.js Example — Batch Background Removal

```javascript
const FormData = require('form-data');
const fs = require('fs');
const fetch = require('node-fetch');

async function removeBackground(imagePath) {
  const form = new FormData();
  form.append('action', 'bg-remove');
  form.append('resolution', '2K');
  form.append('image_files[]', fs.createReadStream(imagePath));
  form.append('options[platform]', 'amazon');
  form.append('options[optimize_repair]', 'true');
  form.append('webhook_url', 'https://yoursite.com/api/webhook');

  const response = await fetch('https://api.rewarxstudio.com/api/v1/batch.php', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'X-Merchant-Id': 'YOUR_MERCHANT_ID',
      ...form.getHeaders(),
    },
    body: form,
  });

  const result = await response.json();
  console.log('Job submitted:', result.job_id);
  return result;
}

removeBackground('./my-product.jpg');
```

---

## Webhook Callback Format

When `webhook_url` is provided, on completion Rewarx will POST to your endpoint:

```json
{
  "job_id": "job_abc123",
  "status": "completed",
  "action": "bg-remove",
  "output_urls": [
    "https://cdn.rewarxstudio.com/output/result_001.jpg",
    "https://cdn.rewarxstudio.com/output/result_002.jpg"
  ],
  "metadata": {
    "resolution": "2K",
    "aspect_ratio": "1:1",
    "processing_time_ms": 8740
  }
}
```

---

## All 11 Supported Actions (Quick Reference)

| Action | Use Case |
|---|---|
| `photography` | Commercial product photo with scene/model |
| `model` | Full AI model studio pipeline |
| `ai-try-on` | Virtual garment try-on with pose & scene |
| `bg-remove` | Background removal & marketplace normalization |
| `mockup` | Logo/pattern to 3D physical object |
| `ad-poster` | Ad creative generation with typography |
| `ghost-mannequin` | Hollow garment worn-look rendering |
| `lookalike` | Vibe/style transfer from reference image |
| `ecommerce-detail` | 8-panel detail image grid for product pages |
| `group-shot` | Multi-product composition studio |
| `studio-template` | Clone a reference scene onto your product |

---

## Get Started

1. Sign up at [www.rewarx.com](https://www.rewarx.com)
2. Upgrade to a **Business plan** to access the Batch API
3. Copy your API key from the dashboard
4. Clone our [code examples](./examples) and start processing in minutes

📧 API support: studio@rewarx.com
