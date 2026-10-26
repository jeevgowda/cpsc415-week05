import os
import json
import sys
import urllib.request
import base64
from pathlib import Path

def parse_receipt_image(image_path, model_name):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: OPENROUTER_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    img_bytes = Path(image_path).read_bytes()
    b64_img = base64.b64encode(img_bytes).decode("utf-8")
    ext = Path(image_path).suffix.lower()
    mime = "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/png"

    prompt = (
        "Extract receipt details into a strict JSON object with keys: "
        "\"vendor\" (string), \"date\" (string), \"items\" "
        "(list of objects with \"name\", \"price\", \"quantity\"), "
        "\"tax\" (float), \"total\" (float). "
        "Return ONLY raw JSON with no markdown fences."
    )

    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64_img}"}}
                ]
            }
        ],
        "temperature": 0.0
    }

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            content = res_data["choices"][0]["message"]["content"].strip()
            if content.startswith("```json"): content = content[7:]
            if content.startswith("```"): content = content[3:]
            if content.endswith("```"): content = content[:-3]
            return json.loads(content.strip()), res_data.get("usage", {})
    except Exception as e:
        return {"error": str(e)}, {}
