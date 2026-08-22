#!/usr/bin/env python3

import os
import json

files_scanned = 0
files_accepted = 0
files_rejected = 0

def main():
    cycle_through_files()

def cycle_through_files():
    folder_path = '/Users/noahshomefolder/Downloads/New Folder With Items'

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        global files_scanned
        files_scanned +=1
        get_data(file_path)

def get_data(file):
    with open(file, mode = "r",encoding="utf-8") as read_file:
        artwork_info = json.load(read_file)

    if artwork_info.get("id") != None and artwork_info.get("title") != None and artwork_info.get("description") != None and artwork_info.get("image_id") != None:
        new_description = format_description(artwork_info["description"])
        artwork_info_load = {
            "filename" : file,
            "id": artwork_info["id"],
            "title": artwork_info["title"],
            "description": new_description,
            "image_id": artwork_info["image_id"]
        }

        if files_accepted > 0:
            with open("harvested_data.json", mode="r",encoding="utf-8") as read_file:
                accepted_artwork_list = json.load(read_file)
        else:
            accepted_artwork_list = []

        accepted_artwork_list.append(artwork_info_load)
        
        with open("harvested_data.json", mode="w",encoding="utf-8") as write_file:
            json.dump(accepted_artwork_list, write_file, indent=0)


def format_description(description):
    count = 0
    start_count = 0
    end_count = 0

    while count < len(description):
        char = description[count]
        if char == "<":
            start_count = count
        elif char == ">":
            end_count = count
            description = (
                description[:start_count]
                + description[end_count + 1:]
            )
            count = start_count - 1
        count += 1
    return description

if __name__ == "__main__":
    main()