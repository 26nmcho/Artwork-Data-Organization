import base64
import json
import mimetypes
from pathlib import Path
from openai import OpenAI

# classical only has 4, modern only has 3, contemporary has none

MODEL = "gpt-5-mini"
OUTPUT_FILE = Path(__file__).parent / "chosen_artworks_with_descriptions.json"

# TODO: edit the prompt
PROMPT = (
    "You are a museum curator tasked with writing a description of the "
    "artwork provided. Describe the painting in a clear, detailed, and "
    "engaging manner, considering its visual elements, artistic style, "
    "possible meanings, and overall impression. Write approximately "
    "100–150 words in a natural, museum-style tone."
)

client = OpenAI()  # reads OPENAI_API_KEY from your environment


def describe_artwork(image_path):
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
                    {"type": "input_text", "text": PROMPT},
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


artworks = [
    {
        "id": 138881,
        "title": "Mural Fragment with Elite Male and Maguey Cactus Leaves",
        "era": "classical",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/138881.jpg"
    },
    {
        "id": 145925,
        "title": "Funerary Portrait of a Young Girl",
        "era": "classical",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/145925.jpg"
    },
    {
        "id": 145923,
        "title": "Funerary Portrait of a Man",
        "era": "classical",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/145923.jpg"
    },
    {
        "id": 145924,
        "title": "Funerary Portrait of a Woman",
        "era": "classical",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/145924.jpg"
    },
    {
        "id": 133012,
        "title": "The White Path to the Western Paradise across Two Rivers (Niga Byakudō)",
        "era": "medieval",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/133012.jpg"
    },
    {
        "id": 125248,
        "title": "The Coronation of the Virgin with the Trinity",
        "era": "medieval",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/125248.jpg"
    },
    {
        "id": 156183,
        "title": "Summer Mountains (after Dong Yuan [active about ad 937-975])",
        "era": "medieval",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/156183.jpg"
    },
    {
        "id": 117658,
        "title": "Perfection of Wisdom in Eight Thousand Lines: Ashtasahasrika Prajnaparamita: Top Cover",
        "era": "medieval",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/117658.jpg"
    },
    {
        "id": 152250,
        "title": "Yujo Monogatari Emaki",
        "era": "medieval",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/152250.jpg"
    },
    {
        "id": 153736,
        "title": "Pine and Camellias",
        "era": "renaissance",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/153736.jpg"
    },
    {
        "id": 97179,
        "title": "Virgin and Child",
        "era": "renaissance",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/97179.jpg"
    },
    {
        "id": 159728,
        "title": "Washing the Feet (from the Dusty World)",
        "era": "renaissance",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/159728.jpg"
    },
    {
        "id": 146035,
        "title": "Clearing Autumn Mists in the Chu Mountains",
        "era": "renaissance",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/146035.jpg"
    },
    {
        "id": 86121,
        "title": "Moonlit Landscape (one of a pair)",
        "era": "renaissance",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/86121.jpg"
    },
    {
        "id": 111479,
        "title": "The Miracles of Saint James the Greater",
        "era": "early modernity",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/111479.jpg"
    },
    {
        "id": 130497,
        "title": "Fish and Rocks",
        "era": "early modernity",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/130497.jpg"
    },
    {
        "id": 146193,
        "title": "Girls Spraying Each Other at Holi",
        "era": "early modernity",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/146193.jpg"
    },
    {
        "id": 135483,
        "title": "Ruins in a Rocky Landscape",
        "era": "early modernity",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/135483.jpg"
    },
    {
        "id": 161785,
        "title": "Portrait of Sardar Singh (Son of Savant Singh, 1730–68)",
        "era": "early modernity",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/161785.jpg"
    },
    {
        "id": 314366,
        "title": "The Morning Toilette",
        "era": "19th century",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/314366.jpg"
    },
    {
        "id": 96328,
        "title": "Portrait of Benjamin West",
        "era": "19th century",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/96328.jpg"
    },
    {
        "id": 162195,
        "title": "Aurora and Cephalus",
        "era": "19th century",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/162195.jpg"
    },
    {
        "id": 96263,
        "title": "Portrait of Jean Terford David",
        "era": "19th century",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/96263.jpg"
    },
    {
        "id": 159270,
        "title": "The Slotskirken of Christiansborg, Copenhagen",
        "era": "19th century",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/159270.jpg"
    },
    {
        "id": 150017,
        "title": "Attributes of Music",
        "era": "impressionist period",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/150017.jpg"
    },
    {
        "id": 135480,
        "title": "The Apple Seller",
        "era": "impressionist period",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/135480.jpg"
    },
    {
        "id": 150079,
        "title": "Still Life with Asparagus",
        "era": "impressionist period",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/150079.jpg"
    },
    {
        "id": 157104,
        "title": "The Seine at Bas-Meudon",
        "era": "impressionist period",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/157104.jpg"
    },
    {
        "id": 144496,
        "title": "Still Life with Cantaloupe",
        "era": "impressionist period",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/144496.jpg"
    },
    {
        "id": 86399,
        "title": "Orchids and Rocks",
        "era": "post-impressionist",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/86399.jpg"
    },
    {
        "id": 125249,
        "title": "The Large Plane Trees (Road Menders at Saint-Rémy)",
        "era": "post-impressionist",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/125249.jpg"
    },
    {
        "id": 135299,
        "title": "Adeline Ravoux",
        "era": "post-impressionist",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/135299.jpg"
    },
    {
        "id": 125104,
        "title": "Frieze of Dancers",
        "era": "post-impressionist",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/125104.jpg"
    },
    {
        "id": 120286,
        "title": "Roses in a Vase",
        "era": "post-impressionist",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/120286.jpg"
    },
    {
        "id": 126769,
        "title": "Fight between a Tiger and a Buffalo",
        "era": "modern",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/126769.jpg"
    },
    {
        "id": 149587,
        "title": "Souvenir of an \"International Ball\" (Portrait of Miss Kathleen Bruce)",
        "era": "modern",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/149587.jpg"
    },
    {
        "id": 136510,
        "title": "Water Lilies (Agapanthus)",
        "era": "modern",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/Cleveland Musuem Images/136510.jpg"
    },
]


def main():
    # Load earlier results so a rerun skips finished artworks (no double charges)
    if OUTPUT_FILE.exists():
        results = json.loads(OUTPUT_FILE.read_text())
    else:
        results = []
    done_ids = {r["id"] for r in results}

    for artwork in artworks:
        if artwork["id"] in done_ids:
            continue
        print(f"Describing {artwork['id']}: {artwork['title']}")
        try:
            description = describe_artwork(artwork["local_image"])
        except Exception as e:
            print(f"  failed: {e}")
            continue

        results.append({
            **artwork,
            "generated_description": description,
            "description_model": MODEL,
            "description_prompt": PROMPT,
        })
        # Save after every artwork so a crash doesn't lose finished ones
        OUTPUT_FILE.write_text(json.dumps(results, indent=4, ensure_ascii=False))

    print(f"Done: {len(results)}/{len(artworks)} saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
