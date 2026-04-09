"""
Rewarx Batch API — Python Example
Action: bg-remove (Background Removal)

Removes the background from product images and returns
a clean, marketplace-compliant output.

Docs: https://rewarxstudio.github.io/docs/api-quickstart
Sign Up: https://www.rewarx.com
"""

import requests
import json
import time

API_KEY = "YOUR_API_KEY_HERE"
MERCHANT_ID = "YOUR_MERCHANT_ID_HERE"
BASE_URL = "https://api.rewarxstudio.com/api/v1/batch.php"


def remove_background(
    image_url: str,
    platform: str = "amazon",  # amazon | shopify | etsy | none
    resolution: str = "2K",
    webhook_url: str = None,
) -> dict:
    """
    Remove the background from a product image.

    Args:
        image_url: Public URL of the source product image.
        platform:  Target marketplace preset. Automatically adjusts
                   background color, aspect ratio, and resolution to
                   meet platform compliance specs.
        resolution: Output resolution. '1K' | '2K' | '4K'.
        webhook_url: Optional HTTPS endpoint to receive async callback.

    Returns:
        API response JSON with job_id and output_url(s).
    """
    payload = {
        "action": "bg-remove",
        "resolution": resolution,
        "image_urls[]": image_url,
        "options[platform]": platform,
        "options[optimize_repair]": "true",
        "options[preserve_edges]": "true",
        "options[optimize_lighting]": "true",
    }

    if webhook_url:
        payload["webhook_url"] = webhook_url

    response = requests.post(
        BASE_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "X-Merchant-Id": MERCHANT_ID,
        },
        data=payload,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def batch_remove_backgrounds(image_urls: list[str], platform: str = "amazon") -> list:
    """
    Process a list of product images through bg-remove sequentially.
    For production, consider using asyncio or a queue for parallelism.

    Args:
        image_urls: List of public image URLs to process.
        platform:   Target marketplace preset.

    Returns:
        List of API response payloads.
    """
    results = []
    for i, url in enumerate(image_urls):
        print(f"[{i + 1}/{len(image_urls)}] Processing: {url}")
        try:
            result = remove_background(url, platform=platform)
            results.append(result)
            print(f"  ✓ Job ID: {result.get('job_id')}")
        except requests.exceptions.RequestException as e:
            print(f"  ✗ Failed: {e}")
            results.append({"error": str(e), "source_url": url})

        if i < len(image_urls) - 1:
            time.sleep(0.5)  # Respect rate limits

    return results


if __name__ == "__main__":
    # ------------------------------------------------------------------
    # Single image example
    # ------------------------------------------------------------------
    result = remove_background(
        image_url="https://yourstore.com/products/shirt.jpg",
        platform="amazon",
        resolution="2K",
    )
    print("Single image result:")
    print(json.dumps(result, indent=2))

    # ------------------------------------------------------------------
    # Batch example (multiple SKUs)
    # ------------------------------------------------------------------
    product_catalog = [
        "https://yourstore.com/products/blue-shirt.jpg",
        "https://yourstore.com/products/red-dress.jpg",
        "https://yourstore.com/products/black-jacket.jpg",
    ]

    results = batch_remove_backgrounds(product_catalog, platform="shopify")
    print("\nBatch results:")
    for r in results:
        print(f"  Output: {r.get('output_url', r.get('error', 'Unknown'))}")
