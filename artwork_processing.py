#!/usr/bin/env python3

import os
import json

files_scanned = 0
files_accepted = 0
files_rejected = 0
errors = 0

def main():
    cycle_through_files()

def cycle_through_files():
    folder_path = '/Users/noahshomefolder/Downloads/artic-api-data/json/artworks'


    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        global files_scanned
        files_scanned +=1
        get_data(file_path)


    global files_accepted
    global files_rejected
    global errors
    global no_id
    global no_title
    global no_description
    global no_short_description
    global not_painting
    print(f"Files accepted: {files_accepted}")
    print(f"Files rejected: {files_rejected}")
    print(f"Files scanned: {files_scanned}")
    print(f"Errors: {errors}")
    
def get_data(file):
    try:
        with open(file, mode = "r",encoding="utf-8-sig") as read_file:
            artwork_info = json.load(read_file)
    except UnicodeDecodeError as e :
        global files_rejected
        global errors
        files_rejected += 1
        errors += 1
        print(f"UnicodeDecodeError: {e} in file: {file}")
        return
    except json.decoder.JSONDecodeError as e:
        files_rejected += 1
        errors += 1
        print(f"JSONDecodeError: {e} in file: {file}")
        return
    except Exception as e:
        files_rejected += 1
        errors += 1
        print(f"Unexpected error: {e} in file: {file}")
        return


    if artwork_info.get("id") != None and artwork_info.get("title") != None and (artwork_info.get("description") != None or artwork_info.get("short_description") != None) and artwork_info.get("image_id") != None:
        if artwork_info.get("artwork_type_title") == None or "painting" in artwork_info.get("artwork_type_title").lower():
            global files_accepted
            artwork_info_load = {
                "filename" : remove_local_path(file),
                "id": artwork_info["id"],
                "title": artwork_info["title"],
                "image_id": artwork_info["image_id"]
            }

            if artwork_info.get("description") != None:
                new_long_description = format_description(artwork_info["description"])
                artwork_info_load["description"] = new_long_description

            if artwork_info.get("short_description") != None:
                new_short_description = format_description(artwork_info["short_description"])
                artwork_info_load["short_description"] = new_short_description

            if artwork_info.get("alt_text") != None:
                artwork_info_load["alt_text"] = artwork_info["alt_text"]

            if artwork_info.get("date_start") != None:
                artwork_info_load["date_start"] = artwork_info["date_start"]

            if artwork_info.get("date_end") != None:
                artwork_info_load["date_end"] = artwork_info["date_end"]

            if artwork_info.get("place_of_origin") != None:
                artwork_info_load["place_of_origin"] = artwork_info["place_of_origin"]

            if artwork_info.get("api_link") != None:
                artwork_info_load["api_link"] = artwork_info["api_link"]


            if files_accepted > 0:
                with open("harvested_data.json", mode="r",encoding="utf-8-sig") as read_file:
                    accepted_artwork_list = json.load(read_file)
            else:
                accepted_artwork_list = []

            accepted_artwork_list.append(artwork_info_load)
                
            with open("harvested_data.json", mode="w",encoding="utf-8-sig", errors="ignore") as write_file:
                json.dump(accepted_artwork_list, write_file, indent=0)

            files_accepted += 1
        else:
            files_rejected += 1
    else:
        files_rejected +=1

def remove_local_path(path):
    if path.startswith("/Users/noahshomefolder/Downloads/artic-api-data/json/artworks/"):
        return path.replace("/Users/noahshomefolder/Downloads/", "")
    else:
        return path


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


# add tracking for errors and conditions
# scrape images
# pandas: date_start, place_of_origine, word count
# matplotlib / seaborn
