# !#/usr/bin/env python3

import json

file = "harvested_data.json"

def main():
    read_harvested_data()

def read_harvested_data():
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
    print(art.get("image_id"))

if __name__ == "__main__":
    main()
          