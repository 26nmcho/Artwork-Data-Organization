import base64
import json
import mimetypes
import random
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parent.parent / ".env")  # loads OPENAI_API_KEY

# same model, settings, and two prompts as the Cleveland run
MODEL = "gpt-5-mini"
SEED = 42
PER_ERA = 5

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
}

METADATA_FILE = Path(__file__).parent.parent / "data" / "chicago_harvested_data.json"
IMAGES_FOLDER = Path("/Users/noahshomefolder/Code/Data Projects/Museum Data/chicago_images")
OUTPUT_DIR = Path(__file__).parent / "samples" / "chicago"

# same eras as the Cleveland run (contemporary left out, Cleveland had none)
ERA_ORDER = [
    "classical",
    "medieval",
    "renaissance",
    "early modernity",
    "19th century",
    "impressionist period",
    "post-impressionist",
    "modern",
]

# fully abstract candidates picked by hand from the description keyword search
FULLY_ABSTRACT_IDS = [
    109819, 65821, 64962, 242223, 186682, 65871,
    73417, 83642, 15569, 89232, 146988, 261313,
]

client = OpenAI()  # reads OPENAI_API_KEY from your environment


def return_era(year):
    if year <= 500.0:
        return "classical"
    elif 500 < year <= 1400.0:
        return "medieval"
    elif 1400.0 < year <= 1600.0:
        return "renaissance"
    elif 1600.0 < year <= 1800.0:
        return "early modernity"
    elif 1800.0 < year <= 1860.0:
        return "19th century"
    elif 1860.0 < year <= 1886.0:
        return "impressionist period"
    elif 1886.0 < year <= 1905.0:
        return "post-impressionist"
    elif 1905.0 < year <= 1970.0:
        return "modern"
    elif 1970.0 < year:
        return "contemporary"


def find_local_images():
    return {image.stem: image for image in IMAGES_FOLDER.glob("*.jpg")}


def choose_artworks():
    with open(METADATA_FILE, "r", encoding="utf-8-sig") as file:
        metadata = json.load(file)

    images = find_local_images()
    pool = [
        artwork for artwork in metadata
        if str(artwork["id"]) in images and artwork.get("date_start") is not None
    ]

    def entry(artwork, era):
        return {
            "id": artwork["id"],
            "title": artwork["title"],
            "creation date early": artwork["date_start"],
            "era": era,
            "local_image": str(images[str(artwork["id"])]),
        }

    rng = random.Random(SEED)

    # abstract picks are their own group, so keep them out of the era pools
    by_id = {artwork["id"]: artwork for artwork in pool}
    abstract_ids = rng.sample(FULLY_ABSTRACT_IDS, PER_ERA)
    abstract = [entry(by_id[i], "abstract") for i in abstract_ids]

    no_abstract = []
    for era in ERA_ORDER:
        era_pool = sorted(
            (a for a in pool if return_era(a["date_start"]) == era and a["id"] not in FULLY_ABSTRACT_IDS),
            key=lambda a: a["id"],
        )
        chosen = rng.sample(era_pool, min(PER_ERA, len(era_pool)))
        no_abstract += [entry(artwork, era) for artwork in chosen]

    return {"no abstract": no_abstract, "abstract": abstract}


# reuse the saved picks, resampling would swap artworks now that the image folder changed
def saved_artworks():
    groups = {}
    for group in ("no abstract", "abstract"):
        path = OUTPUT_DIR / group / "less_restriction_alt_text_method.json"
        if not path.exists():
            return None
        groups[group] = [
            {key: artwork[key] for key in ("id", "title", "creation date early", "era", "local_image")}
            for artwork in json.loads(path.read_text())
        ]
    return groups


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


def run(artworks, prompt, output_file):
    # Load earlier results so a rerun skips finished artworks (no double charges)
    if output_file.exists():
        results = json.loads(output_file.read_text())
    else:
        results = []
    done_ids = {r["id"] for r in results}

    for artwork in artworks:
        if artwork["id"] in done_ids:
            continue
        print(f"Describing {artwork['id']}: {artwork['title']}")
        try:
            description = describe_artwork(artwork["local_image"], prompt)
        except Exception as e:
            print(f"  failed: {e}")
            continue

        results.append({
            **artwork,
            "generated_description": description,
            "description_model": MODEL,
            "description_prompt": prompt,
        })
        # Save after every artwork so a crash doesn't lose finished ones
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(json.dumps(results, indent=4, ensure_ascii=False))

    print(f"Done: {len(results)}/{len(artworks)} saved to {output_file}")


def main():
    groups = saved_artworks() or choose_artworks()

    # --dry-run prints the chosen artworks without calling the API
    if "--dry-run" in sys.argv:
        for group, artworks in groups.items():
            print(f"\n{group}: {len(artworks)}")
            for artwork in artworks:
                print(f"  {artwork['era']:<22} {artwork['id']:<8} {artwork['title']}")
        return

    for group, artworks in groups.items():
        for prompt_name, prompt in PROMPTS.items():
            run(artworks, prompt, OUTPUT_DIR / group / f"{prompt_name}.json")


if __name__ == "__main__":
    main()
