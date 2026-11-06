import base64
import json
import mimetypes
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parent.parent / ".env")  # loads OPENAI_API_KEY

# python3 descriptions/generate_descriptions.py            -> generates whatever is missing
# python3 descriptions/generate_descriptions.py --dry-run  -> shows what's missing without calling the API

MODEL = "gpt-5-mini"
DESCRIPTIONS_FILE = Path(__file__).parent / "descriptions.json"

# to try a new prompt, add it here with a new name. rewording one under an old name won't regenerate it
PROMPTS = {
    "high_restrictions_context_for_project": (
        "You are a museum curator tasked with writing a description of the artwork provided. "
        "Describe the painting in a clear, detailed, and engaging manner, considering its visual "
        "elements, artistic style, possible meanings, and overall impression. Write approximately "
        "100–150 words in a natural, museum-style tone."
    ),
    "less_restriction_alt_text_method": (
        "Write an alternative text, annotation of the provided image supposedly for a blind/low vision group"
        "make the description around 100-150 words long."
    ),
    "plain_description": (
        "Write an description of this picture"
        "make the description around 100-150 words long."
    ),
}

ARTWORK_FIELDS = ("museum", "id", "title", "creation date early", "era", "abstract", "local_image")

client = OpenAI()  # reads OPENAI_API_KEY from your environment


def describe_artwork(image_path, prompt):
    image_path = Path(image_path)

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"

    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": prompt},
                    {
                        "type": "input_image",
                        "image_url": f"data:{mime_type};base64,{encoded_image}",
                        "detail": "high",
                    },
                ],
            }
        ],
    )

    return response.output_text


def find_missing(results):
    done = {(r["museum"], r["id"], r["prompt_name"]) for r in results}

    artworks = {}
    for r in results:
        artworks.setdefault((r["museum"], r["id"]), {field: r[field] for field in ARTWORK_FIELDS})

    missing = []
    for prompt_name in PROMPTS:
        for artwork in artworks.values():
            if (artwork["museum"], artwork["id"], prompt_name) not in done:
                missing.append((artwork, prompt_name))
    return missing


def main():
    results = json.loads(DESCRIPTIONS_FILE.read_text(encoding="utf-8"))
    missing = find_missing(results)
    print(f"{len(missing)} descriptions to generate")

    if "--dry-run" in sys.argv:
        for artwork, prompt_name in missing:
            print(f"  {artwork['museum']:<10} {artwork['id']:<8} {prompt_name}  {artwork['title']}")
        return

    for artwork, prompt_name in missing:
        print(f"Describing {artwork['museum']} {artwork['id']} with {prompt_name}: {artwork['title']}")
        try:
            description = describe_artwork(artwork["local_image"], PROMPTS[prompt_name])
        except Exception as e:
            print(f"  failed: {e}")
            continue

        results.append({
            **artwork,
            "prompt_name": prompt_name,
            "generated_description": description,
            "description_model": MODEL,
            "description_prompt": PROMPTS[prompt_name],
        })
        # Save after every artwork so a crash doesn't lose finished ones
        DESCRIPTIONS_FILE.write_text(json.dumps(results, indent=4, ensure_ascii=False), encoding="utf-8")

    print(f"Done: {len(results)} descriptions saved to {DESCRIPTIONS_FILE}")


if __name__ == "__main__":
    main()
