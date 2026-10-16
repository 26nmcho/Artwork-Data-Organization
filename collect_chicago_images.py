import json
import webbrowser
import time
import sys
import select
from pathlib import Path


FOLDER = Path("/Users/noahshomefolder/Code/Data Projects/Museum Data/art institute of chicago 5")

SKIPPED_FILE = Path("skipped_artworks_second_round.json")


def save_skipped_artworks(skipped_artworks):
    with open(
        SKIPPED_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            skipped_artworks,
            file,
            indent=4,
            ensure_ascii=False
        )


def wait_for_new_file(folder, old_files):
    print("Waiting for image...")
    print("Type 's' and press ENTER to skip this artwork.")

    while True:

        current_files = set(folder.iterdir())

        new_files = current_files - old_files

        new_files = [
            file for file in new_files
            if file.is_file()
            and not file.name.endswith(".crdownload")
            and not file.name.endswith(".download")
        ]

        if new_files:
            return new_files[0]

        ready, _, _ = select.select(
            [sys.stdin],
            [],
            [],
            0
        )

        if ready:
            command = sys.stdin.readline().strip().lower()

            if command == "s":
                return None

        time.sleep(0.5)


def create_file():

    with open(
        "skipped_artworks.json",
        "r",
        encoding="utf-8-sig"
    ) as file:
        data = json.load(file)

    FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    if SKIPPED_FILE.exists():

        with open(
            SKIPPED_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            skipped_artworks = json.load(file)

    else:
        skipped_artworks = []

    START_AT = 0

    for i, art in enumerate(data[START_AT:], start=START_AT):

        artwork_id = art["id"]
        image_id = art["image_id"]
        title = art["title"]

        existing_files = list(
            FOLDER.glob(f"{artwork_id}.*")
        )

        if existing_files:
            print(f"Already exists: {title}")
            continue

        print()
        print("=" * 60)

        print(
            f"Artwork {i + 1}/{len(data)}"
        )

        print(f"Title: {title}")
        print(f"Artwork ID: {artwork_id}")
        print(f"Image ID: {image_id}")

        old_files = set(
            FOLDER.iterdir()
        )

        image_url = (
            f"https://www.artic.edu/iiif/2/"
            f"{image_id}/full/200,/0/default.jpg"
        )

        webbrowser.open(
            image_url
        )

        new_file = wait_for_new_file(
            FOLDER,
            old_files
        )


        if new_file is None:

            print(
                f"Skipped: {title}"
            )

            skipped_artworks.append(
                art
            )

            save_skipped_artworks(
                skipped_artworks
            )

            continue

        extension = (
            new_file.suffix.lower()
        )

        if not extension:
            extension = ".jpg"

        final_path = (
            FOLDER /
            f"{artwork_id}{extension}"
        )

        new_file.rename(
            final_path
        )

        print(
            f"Saved as: {final_path.name}"
        )

        time.sleep(0.5)


if __name__ == "__main__":
    create_file()