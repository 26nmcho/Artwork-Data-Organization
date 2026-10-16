import json
import os
import hashlib


IMAGES_FOLDER_PATH = "/Users/noahshomefolder/Code/Data Projects/Museum Data/art institute of chicago 6"
IMAGE_FAILURE_FOLDER_PATH = "skipped_artworks_second_round.json"
METADATA_FILE_PATH = "chicago_harvested_data.json"

#load chicago meta data
def load_chicago_metadata():
    with open(METADATA_FILE_PATH, 'r', encoding='utf-8-sig') as f:
        metadata = json.load(f)
    return metadata

#load retry data file
def load_retry_data():
    try:
        with open(IMAGE_FAILURE_FOLDER_PATH, 'r') as f:
            retry_data = json.load(f)
    except FileNotFoundError:
        retry_data = []
    return retry_data

#delete the second round skipped artworks from the chicago dataset
def delete_skipped():
    metadata = load_chicago_metadata()
    skipped = load_retry_data()

    skipped_ids = {artwork["id"] for artwork in skipped}
    cleaned = [artwork for artwork in metadata if artwork["id"] not in skipped_ids]

    with open(METADATA_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)

    print(f"Deleted {len(metadata) - len(cleaned)} datapoints")
    return cleaned

#load the chicago images
def load_chicago_images():
    image_names = []
    for file_name in os.listdir(IMAGES_FOLDER_PATH):
        if file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            image_names.append(file_name)
    return image_names

#find images that are exact copies of each other and delete the extra copies
def delete_duplicate_images():
    image_names = load_chicago_images()
    seen_images = {}
    count_deleted_duplicates = 0
    for name in sorted(image_names):
        image_path = os.path.join(IMAGES_FOLDER_PATH, name)
        with open(image_path, 'rb') as f:
            image_hash = hashlib.md5(f.read()).hexdigest()

        if image_hash not in seen_images:
            seen_images[image_hash] = name
        else:
            os.remove(image_path)
            print(f"Deleted {name} (duplicate of {seen_images[image_hash]})")
            count_deleted_duplicates += 1

    print(f"Deleted {count_deleted_duplicates} duplicate images")
    return count_deleted_duplicates


def main():
    print(len(load_chicago_images()))
    print()
    delete_skipped()
    delete_duplicate_images()

if __name__ == "__main__":
    main()

