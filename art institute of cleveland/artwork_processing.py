import json
import pandas as pd
import requests
from pathlib import Path
import matplotlib.pyplot as plt
import image_processing

accepted_tracker = 0
total_tracker = 0

# trackers
no_id = 0
no_title = 0
no_desc = 0
no_early_date = 0
no_late_date = 0 
no_creator = 0
no_technique = 0
no_image = 0
no_culture = 0


pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 20)

def data_collection(step):
    global accepted_tracker
    global total_tracker
    url = "https://openaccess-api.clevelandart.org/api/artworks"
    params = {
            'has_image': 1,
            'limit': step,
            'type': 'Painting',
            'skip' : total_tracker,
            'fields' : 'id,title,description,creation_date_earliest,creation_date_latest,creators,technique,culture,type,images,url,share_license_status'
        }

    r = requests.get(url, params=params)

    data = r.json()
    total_tracker += len(data['data'])

    accepted_artworks = []

    for artwork in data['data']:
        artwork_id = artwork.get('id')
        artwork_title = artwork.get('title')
        artwork_desc = artwork.get('description')
        artwork_date_earliest = artwork.get('creation_date_earliest')
        artwork_date_latest = artwork.get('creation_date_latest')
        artwork_creators = artwork.get('creators')
        artwork_technique = artwork.get('technique')
        artwork_culture = artwork.get('culture')
        try:
            artwork_image = artwork['images']['web']['url']
        except KeyError:
            artwork_image = None
        creator_list = []
        if artwork_creators != None:
            for creator in artwork_creators:
                name = creator.get('description')
                creator_list.append(name)
        artwork = {
            'id' : artwork_id,
            'title' : artwork_title,
            'description' : artwork_desc,
            'creation date early' : artwork_date_earliest,
            'creation date late' : artwork_date_latest,
            'creators' : creator_list,
            'technique' : artwork_technique,
            'image' : artwork_image,
            'culture' : artwork_culture
        }

        if data_validation(artwork):
            accepted_artworks.append(artwork)
            accepted_tracker += 1
            print(f"Artwork Collected: {accepted_tracker}")

    write_artwork(accepted_artworks)
    return accepted_artworks

def historical_data_processing():
    with open("cleveland_historical_api.json", "r", encoding="utf-8-sig") as file:
            data = json.load(file)
    
    df = pd.DataFrame(data)
    print(df.head(5))

    df = df[(df['type'] == 'Painting') & ((df['digital_description'].notna()) | (df['wall_description'].notna())) & (df["images"].notna())]
    print(df.shape)

    df = df.filter(["id","title","creation_date", "creation_date_earliest","creation_date_latest","creators","culture",'technique',"type","inscriptions","wall_description","digital_description"])
    print(df.shape)
    print(df.head(8))

    walldesc_size = df["wall_description"].count()
    digitaldesc_size = df["digital_description"].count()

    print(f"How many paintings have the wall description: {walldesc_size}")
    print(f"How many paintings have the digital description: {digitaldesc_size}")

    print(df.describe())

    bar_chart_labels = list(df.columns)
    values = [(df[column].isna() | df[column].map(lambda x: isinstance(x, list) and len(x) == 0)).sum()
              for column in bar_chart_labels]
    total = len(df)
    pairs = sorted(zip(bar_chart_labels, values), key=lambda pair: pair[1])
    bar_chart_labels = [pair[0] for pair in pairs]
    values = [pair[1] for pair in pairs]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(bar_chart_labels, values, color="#2a78d6")
    for bar, value in zip(bars, values):
        ax.text(bar.get_width() + 15, bar.get_y() + bar.get_height() / 2,
                f"{value} ({value / total:.1%})", va="center", fontsize=9, color="#52514e")
    ax.set_xlim(0, total)
    ax.set_xlabel(f"Paintings missing a value (out of {total})")
    ax.set_title("Missing Values per Column", loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.show()
    


def data_validation(artwork):
    return_boolean = True
    if artwork['id'] == None:
        return_boolean = False
        global no_id
        no_id += 1
    if artwork['title'] == None:
        return_boolean = False
        global no_title
        no_title += 1
    if artwork['description'] == None:
        return_boolean = False
        global no_desc
        no_desc += 1
    if artwork['creation date early'] == None:
        return_boolean = False
        global no_early_date
        no_early_date += 1
    if artwork['creation date late'] == None:
        return_boolean = False
        global no_late_date
        no_late_date += 1
    if artwork['creators'] == None:
        return_boolean = False
        global no_creator
        no_creator += 1
    if artwork['technique'] == None:
        return_boolean = False
        global no_technique
        no_technique += 1
    if artwork['image'] == None:
        return_boolean = False
        global no_image
        no_image += 1
    if artwork['culture'] == None:
        return_boolean = False
        global no_culture
        no_culture += 1
    return return_boolean

def write_artwork(accepted_artworks):
    global accepted_tracker

    if accepted_tracker > len(accepted_artworks):
        with open("cleveland_harvested_data.json", mode="r",encoding="utf-8-sig") as read_file:
            collected_data = json.load(read_file)
    else:
        collected_data = []
            
    collected_data.extend(accepted_artworks)
                            
    with open("cleveland_harvested_data.json", mode = "w", encoding="utf-8") as write_file:
        json.dump(collected_data, write_file, indent=4)

def image_metadata_check():

    try:
        with open("cleveland_harvested_data.json", mode = "r", encoding = "utf-8-sig") as file:
            metadata = json.load(file)
    except FileNotFoundError:
        print("error: file unavailable")
        return 
    except Exception as e:
        print(e)
        return

    data_size = len(metadata)

    image_extensions = {".jpg"}

    folder = Path('/Users/noahshomefolder/Desktop/Cleveland Musuem Images')

    image_id = [file.stem for file in folder.iterdir() if file.suffix.lower() in image_extensions]

    data_no_image = []
    artwork_num = 0

    for artwork in metadata: 

        has_image = False
        for id in image_id:
            if id == str(artwork["id"]):
                has_image = True

        if has_image == False:
            data_no_image.append(artwork)

        # percentage done
        artwork_num += 1

        progress = artwork_num / data_size

        print(f"Percentage Checked: {progress:.2f}", end = "\r", flush=True)



    print()

    for x in data_no_image:
        print(x["id"])

    return data_no_image


# save the missing images found by the image metadata check method
def fill_images(data_no_image):
    for artwork in data_no_image:
        image_processing.image_save(artwork['id'], artwork['image'])
        print(f"Image Retreived: {artwork["id"]}")

if __name__ == '__main__':
    '''while True:
        previous_total = total_tracker
        data_collection(25)
        if total_tracker == previous_total:
            break

    print("No ID:", no_id)
    print("No Title:", no_title)
    print("No Description:", no_desc)
    print("No Early Date:", no_early_date)
    print("No Late Date:", no_late_date)
    print("No Creator:", no_creator)
    print("No Technique:", no_technique)
    print("No Image:", no_image)
    print("No Culture:", no_culture)

    test_artwork = {
    "id": 1,
    "title": "Test",
    "description": "Test description",
    "creation date early": 1900,
    "creation date late": 1901,
    "creators": ["Test Artist"],
    "technique": "Oil on canvas",
    "image": "https://example.com/image.jpg"
    }'''
    historical_data_processing()

   ## image_metadata_check()




# share git and drop box all data and code
# check historical cleveland api
# docuemntation
# keep trying to harvest images for chicago
# pick the right model figure out hte pipeline for prmopt engineering - exploratory
