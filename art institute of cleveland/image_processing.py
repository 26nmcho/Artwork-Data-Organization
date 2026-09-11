import requests
from pathlib import Path
import json

images_saved = 1

def retrieve_images():
    with open("cleveland_harvested_data.json", mode="r",encoding="utf-8-sig") as read_file:
        collected_data = json.load(read_file)

    for artwork in collected_data:
        image_save(artwork['id'], artwork['image'])
        global images_saved
        images_saved += 1
        


def image_save(name, url):
    image_folder = Path("/Users/noahshomefolder/Desktop/Cleveland Musuem Images")

    file_path = image_folder/f"{name}.jpg"

    response = requests.get(url)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            file.write(response.content)

        print(f"Saved: {file_path}")
        print(f"Total Images Saved:  {images_saved}")


if __name__ == "__main__":
    retrieve_images()