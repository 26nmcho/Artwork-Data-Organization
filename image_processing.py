# !#/usr/bin/env python3

import json
import requests
from PIL import Image
from io import BytesIO
import time

file = "harvested_data.json"

def main():
    read_harvested_data()

def read_harvested_data():
    give_me_one = 0
    try:
        with open(file, mode = "r",encoding="utf-8-sig") as read_file:
            image_info = json.load(read_file)
    except Exception as e:
        files_rejected += 1
        errors += 1
        print(f"Unexpected error: {e} in file: {file}")
        return

    for art in image_info:
        create_image(art)

def create_image(art):
    image_id = art.get("image_id")
    id = art.get("id")
    r = requests.get(f"https://www.artic.edu/iiif/2/{image_id}/full/843,/0/default.jpg")
    i = Image.open(BytesIO(r.content))
    i.save(f"images/{id}.jpg")
    time.sleep(1)


if __name__ == "__main__":
    main()
          