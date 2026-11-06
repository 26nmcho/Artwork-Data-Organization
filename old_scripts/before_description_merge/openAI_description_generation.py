import base64
import json
import mimetypes
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).parent.parent / ".env")  # loads OPENAI_API_KEY

# classical only has 4, modern only has 3, contemporary has none
# abstract has 5, but only the Mondrian is fully abstract (the rest are near-abstract)

MODEL = "gpt-5-mini"
SAMPLES_DIR = Path(__file__).parent / "samples" / "cleveland"
OUTPUT_FILE = SAMPLES_DIR / "new_results.json"

# TODO: edit the prompt
PROMPT = (
    "Write an description of this picture"
    "make the description around 100-150 words long."
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
        "creation date early": 500,
        "era": "classical",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/138881.jpg"
    },
    {
        "id": 145925,
        "title": "Funerary Portrait of a Young Girl",
        "creation date early": 25,
        "era": "classical",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/145925.jpg"
    },
    {
        "id": 145923,
        "title": "Funerary Portrait of a Man",
        "creation date early": 138,
        "era": "classical",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/145923.jpg"
    },
    {
        "id": 145924,
        "title": "Funerary Portrait of a Woman",
        "creation date early": 138,
        "era": "classical",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/145924.jpg"
    },
    {
        "id": 133012,
        "title": "The White Path to the Western Paradise across Two Rivers (Niga Byakudō)",
        "creation date early": 1200,
        "era": "medieval",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/133012.jpg"
    },
    {
        "id": 125248,
        "title": "The Coronation of the Virgin with the Trinity",
        "creation date early": 1395,
        "era": "medieval",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/125248.jpg"
    },
    {
        "id": 156183,
        "title": "Summer Mountains (after Dong Yuan [active about ad 937-975])",
        "creation date early": 1290,
        "era": "medieval",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/156183.jpg"
    },
    {
        "id": 117658,
        "title": "Perfection of Wisdom in Eight Thousand Lines: Ashtasahasrika Prajnaparamita: Top Cover",
        "creation date early": 1119,
        "era": "medieval",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/117658.jpg"
    },
    {
        "id": 152250,
        "title": "Yujo Monogatari Emaki",
        "creation date early": 1336,
        "era": "medieval",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/152250.jpg"
    },
    {
        "id": 153736,
        "title": "Pine and Camellias",
        "creation date early": 1595,
        "era": "renaissance",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/153736.jpg"
    },
    {
        "id": 97179,
        "title": "Virgin and Child",
        "creation date early": 1437,
        "era": "renaissance",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/97179.jpg"
    },
    {
        "id": 159728,
        "title": "Washing the Feet (from the Dusty World)",
        "creation date early": 1570,
        "era": "renaissance",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/159728.jpg"
    },
    {
        "id": 146035,
        "title": "Clearing Autumn Mists in the Chu Mountains",
        "creation date early": 1600,
        "era": "renaissance",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/146035.jpg"
    },
    {
        "id": 86121,
        "title": "Moonlit Landscape (one of a pair)",
        "creation date early": 1575,
        "era": "renaissance",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/86121.jpg"
    },
    {
        "id": 111479,
        "title": "The Miracles of Saint James the Greater",
        "creation date early": 1726,
        "era": "early modernity",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/111479.jpg"
    },
    {
        "id": 130497,
        "title": "Fish and Rocks",
        "creation date early": 1650,
        "era": "early modernity",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/130497.jpg"
    },
    {
        "id": 146193,
        "title": "Girls Spraying Each Other at Holi",
        "creation date early": 1635,
        "era": "early modernity",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/146193.jpg"
    },
    {
        "id": 135483,
        "title": "Ruins in a Rocky Landscape",
        "creation date early": 1635,
        "era": "early modernity",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/135483.jpg"
    },
    {
        "id": 161785,
        "title": "Portrait of Sardar Singh (Son of Savant Singh, 1730–68)",
        "creation date early": 1755,
        "era": "early modernity",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/161785.jpg"
    },
    {
        "id": 314366,
        "title": "The Morning Toilette",
        "creation date early": 1805,
        "era": "19th century",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/314366.jpg"
    },
    {
        "id": 96328,
        "title": "Portrait of Benjamin West",
        "creation date early": 1818,
        "era": "19th century",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/96328.jpg"
    },
    {
        "id": 162195,
        "title": "Aurora and Cephalus",
        "creation date early": 1805,
        "era": "19th century",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/162195.jpg"
    },
    {
        "id": 96263,
        "title": "Portrait of Jean Terford David",
        "creation date early": 1813,
        "era": "19th century",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/96263.jpg"
    },
    {
        "id": 159270,
        "title": "The Slotskirken of Christiansborg, Copenhagen",
        "creation date early": 1850,
        "era": "19th century",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/159270.jpg"
    },
    {
        "id": 150017,
        "title": "Attributes of Music",
        "creation date early": 1863,
        "era": "impressionist period",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/150017.jpg"
    },
    {
        "id": 135480,
        "title": "The Apple Seller",
        "creation date early": 1885,
        "era": "impressionist period",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/135480.jpg"
    },
    {
        "id": 150079,
        "title": "Still Life with Asparagus",
        "creation date early": 1880,
        "era": "impressionist period",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/150079.jpg"
    },
    {
        "id": 157104,
        "title": "The Seine at Bas-Meudon",
        "creation date early": 1865,
        "era": "impressionist period",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/157104.jpg"
    },
    {
        "id": 144496,
        "title": "Still Life with Cantaloupe",
        "creation date early": 1875,
        "era": "impressionist period",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/144496.jpg"
    },
    {
        "id": 86399,
        "title": "Orchids and Rocks",
        "creation date early": 1897,
        "era": "post-impressionist",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/86399.jpg"
    },
    {
        "id": 125249,
        "title": "The Large Plane Trees (Road Menders at Saint-Rémy)",
        "creation date early": 1889,
        "era": "post-impressionist",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/125249.jpg"
    },
    {
        "id": 135299,
        "title": "Adeline Ravoux",
        "creation date early": 1890,
        "era": "post-impressionist",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/135299.jpg"
    },
    {
        "id": 125104,
        "title": "Frieze of Dancers",
        "creation date early": 1890,
        "era": "post-impressionist",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/125104.jpg"
    },
    {
        "id": 120286,
        "title": "Roses in a Vase",
        "creation date early": 1890,
        "era": "post-impressionist",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/120286.jpg"
    },
    {
        "id": 126769,
        "title": "Fight between a Tiger and a Buffalo",
        "creation date early": 1908,
        "era": "modern",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/126769.jpg"
    },
    {
        "id": 149587,
        "title": "Souvenir of an \"International Ball\" (Portrait of Miss Kathleen Bruce)",
        "creation date early": 1907,
        "era": "modern",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/149587.jpg"
    },
    {
        "id": 136510,
        "title": "Water Lilies (Agapanthus)",
        "creation date early": 1915,
        "era": "modern",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/136510.jpg"
    },
    {
        "id": 143278,
        "title": "Composition with Red, Yellow, and Blue",
        "creation date early": 1927,
        "era": "abstract",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/143278.jpg"
    },
    {
        "id": 167456,
        "title": "Rock at Sea",
        "creation date early": 1920,
        "era": "abstract",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/167456.jpg"
    },
    {
        "id": 164630,
        "title": "Night Café",
        "creation date early": 1918,
        "era": "abstract",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/164630.jpg"
    },
    {
        "id": 135420,
        "title": "Morning Glory with Black",
        "creation date early": 1926,
        "era": "abstract",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/135420.jpg"
    },
    {
        "id": 149112,
        "title": "Church Street El",
        "creation date early": 1920,
        "era": "abstract",
        "local_image": "/Users/noahshomefolder/Code/Data Projects/Museum Data/cleveland_images/149112.jpg"
    },
]


def saved_alt_text_ids():
    done = set()
    for path in SAMPLES_DIR.glob("*/less_restriction_alt_text_method.json"):
        # one file has a personal note above the json, so start reading at the first [
        text = path.read_text(encoding="utf-8")
        done |= {r["id"] for r in json.loads(text[text.index("["):]) if r["description_prompt"] == PROMPT}
    return done


def main():
    # Load earlier results so a rerun skips finished artworks (no double charges)
    if OUTPUT_FILE.exists():
        results = json.loads(OUTPUT_FILE.read_text())
    else:
        results = []
    done_ids = {r["id"] for r in results if r["description_prompt"] == PROMPT} | saved_alt_text_ids()

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

    print(f"Done: {len(results)} new results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
