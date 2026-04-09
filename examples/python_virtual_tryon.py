"""
Rewarx Batch API — Python Example
Action: ai-try-on (Virtual Garment Try-On)

Shows your garment on an AI-generated model in a
studio scene — no real model or photoshoot required.

Docs: https://rewarxstudio.github.io/docs/api-quickstart
Sign Up: https://www.rewarx.com
"""

import requests
import json

API_KEY = "YOUR_API_KEY_HERE"
MERCHANT_ID = "YOUR_MERCHANT_ID_HERE"
BASE_URL = "https://api.rewarxstudio.com/api/v1/batch.php"

# Available pose options
POSE_OPTIONS = [
    "standing-front", "standing-side", "back-view",
    "three-quarter", "walking", "running",
    "sitting", "crouching", "hands-on-hips", "leaning",
]

# Available background scene IDs
BACKGROUND_OPTIONS = [
    "studio-white", "minimal-gray", "urban-street", "luxury-interior",
    "modern-loft", "nature-park", "beach-sunset", "desert-dunes",
    "industrial-warehouse", "cyberpunk-city",
]

# Available lighting IDs
LIGHTING_OPTIONS = [
    "cinematic", "soft-studio", "natural-sunlight", "golden-hour",
    "dramatic", "high-key", "neon-glow", "moonlight", "ring-light",
]


def virtual_try_on(
    garment_url: str,
    model_description: str = "Elegant woman, mid-30s, natural makeup",
    pose: str = "standing-front",
    background: str = "luxury-interior",
    lighting: str = "soft-studio",
    style: str = "commercial fashion editorial",
    resolution: str = "2K",
    aspect_ratio: str = "3:4",
    webhook_url: str = None,
) -> dict:
    """
    Generate a virtual try-on image from a garment product photo.

    Args:
        garment_url:       Public URL of flat-lay or packaged garment image.
        model_description: Appearance prompt for the AI model.
        pose:              Model pose. See POSE_OPTIONS.
        background:        Scene background ID. See BACKGROUND_OPTIONS.
        lighting:          Lighting style ID. See LIGHTING_OPTIONS.
        style:             Overall visual style description.
        resolution:        Output resolution '1K' | '2K' | '4K'.
        aspect_ratio:      Output aspect ratio (3:4 recommended for fashion).
        webhook_url:       Optional HTTPS endpoint for async callback.

    Returns:
        API response JSON.
    """
    assert pose in POSE_OPTIONS, f"Invalid pose. Must be one of: {POSE_OPTIONS}"
    assert background in BACKGROUND_OPTIONS, f"Invalid background. Must be one of: {BACKGROUND_OPTIONS}"
    assert lighting in LIGHTING_OPTIONS, f"Invalid lighting. Must be one of: {LIGHTING_OPTIONS}"

    payload = {
        "action": "ai-try-on",
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "image_urls[]": garment_url,
        "options[pose]": pose,
        "options[model_description]": model_description,
        "options[background]": background,
        "options[lighting]": lighting,
        "options[style]": style,
        "options[generate_model]": "true",
        "options[keep_background]": "false",
        "options[keep_lighting]": "false",
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


if __name__ == "__main__":
    # -------------------------------------------------------
    # Example 1: Fashion editorial shot — luxury interior scene
    # -------------------------------------------------------
    result = virtual_try_on(
        garment_url="https://yourstore.com/products/silk-dress.jpg",
        model_description="Asian woman, early 20s, slim build, natural makeup",
        pose="standing-front",
        background="luxury-interior",
        lighting="soft-studio",
        style="High-end fashion editorial, Vogue magazine cover quality",
        resolution="2K",
        aspect_ratio="3:4",
    )
    print("Try-On Result (Luxury Interior):")
    print(json.dumps(result, indent=2))

    # -------------------------------------------------------
    # Example 2: Street lifestyle shot — urban background
    # -------------------------------------------------------
    result2 = virtual_try_on(
        garment_url="https://yourstore.com/products/denim-jacket.jpg",
        model_description="Young man, early 20s, athletic build, relaxed confidence",
        pose="three-quarter",
        background="urban-street",
        lighting="golden-hour",
        style="Urban streetwear, casual lifestyle photography",
        resolution="2K",
        aspect_ratio="3:4",
    )
    print("\nTry-On Result (Urban Street):")
    print(json.dumps(result2, indent=2))
