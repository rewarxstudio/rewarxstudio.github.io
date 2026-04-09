"""
Rewarx Batch API — Python Example
Action: model (AI Model Studio)

Generates professional model lifestyle photos from flat-lay
or product-held garment images. No studio, no model hiring required.

Docs: https://rewarxstudio.github.io/docs/api-quickstart
Sign Up: https://www.rewarx.com
"""

import requests
import json

API_KEY = "YOUR_API_KEY_HERE"
MERCHANT_ID = "YOUR_MERCHANT_ID_HERE"
BASE_URL = "https://api.rewarxstudio.com/api/v1/batch.php"


def generate_model_shot(
    garment_url: str,
    requirements: str = "Elegant woman, mid-30s, natural makeup",
    action: str = "Gently holding the product near chest, relaxed confident smile",
    background: str = "Modern sunlit apartment, minimalist white walls",
    visual_prompt: str = "Fashion editorial, high-end magazine",
    aesthetic: str = "Minimalist",
    atmosphere: str = None,
    resolution: str = "2K",
    aspect_ratio: str = "3:4",
    webhook_url: str = None,
) -> dict:
    """
    Generate an AI model studio photo from a garment image.

    The model is generated based on your description — no stock images used.
    Every generation is unique and custom to your product.

    Args:
        garment_url:   Public URL of flat-lay, product-only, or hanger image.
        requirements:  Model appearance description prompt.
        action:        What the model is doing in the scene.
        background:    Scene or location description.
        visual_prompt: Overall visual/editorial direction.
        aesthetic:     Style preset (Minimalist / Luxury / Pop Art / etc.)
        atmosphere:    Atmospheric effects (Foggy / Wet / Cinematic depth / etc.)
        resolution:    Output resolution '1K' | '2K' | '4K'.
        aspect_ratio:  Aspect ratio (3:4 recommended for fashion).
        webhook_url:   Optional HTTPS callback URL for async delivery.

    Returns:
        API response dict with job_id and output_url(s).
    """
    payload = {
        "action": "model",
        "resolution": resolution,
        "aspect_ratio": aspect_ratio,
        "image_urls[]": garment_url,
        "options[requirements]": requirements,
        "options[action]": action,
        "options[background]": background,
        "options[visual_prompt]": visual_prompt,
        "options[aesthetic]": aesthetic,
    }

    if atmosphere:
        payload["options[atmosphere]"] = atmosphere
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
    # Example 1: Women's fashion — luxury interior lifestyle
    # -------------------------------------------------------
    result_1 = generate_model_shot(
        garment_url="https://yourstore.com/products/womens-silk-blouse.jpg",
        requirements="Elegant woman, early 30s, high cheekbones, natural makeup, flowing dark hair",
        action="Lightly touching lapel, looking off-camera with quiet confidence",
        background="Airy Paris apartment, floor-to-ceiling windows with soft morning light",
        visual_prompt="High-end fashion editorial, Vogue cover",
        aesthetic="Luxury",
        atmosphere="Cinematic depth",
        resolution="2K",
        aspect_ratio="3:4",
    )
    print("Women's fashion result:")
    print(json.dumps(result_1, indent=2))

    print("-" * 60)

    # -------------------------------------------------------
    # Example 2: Men's streetwear — urban outdoor setting
    # -------------------------------------------------------
    result_2 = generate_model_shot(
        garment_url="https://yourstore.com/products/mens-hoodie.jpg",
        requirements="Young athletic man, mid-20s, fit build, modern grooming, relaxed energy",
        action="Walking forward, one hand in pocket, slight grin",
        background="Graffiti-lined urban alley, warm evening light",
        visual_prompt="Streetwear lookbook, youth culture magazine",
        aesthetic="Pop Art",
        atmosphere=None,
        resolution="2K",
        aspect_ratio="3:4",
    )
    print("Men's streetwear result:")
    print(json.dumps(result_2, indent=2))
