import json
import requests


def print_openaccess_results():
    url = "https://openaccess-api.clevelandart.org/api/artworks"
    params = {
            'has_image': 1,
            'limit': 3,
            'type': 'Painting',
            'skip' : 0,
            'fields' : 'id,title,description,creation_date_earliest,creation_date_latest,creators,technique,type,images,url,share_license_status'
        }

    r = requests.get(url, params=params)

    data = r.json()



    for artwork in data['data']:
        artwork_id = artwork.get('id')
        artwork_title = artwork['title']
        artwork_desc = artwork['description']
        artwork_date_earliest = artwork['creation_date_earliest']
        artwork_date_latest = artwork['creation_date_latest']
        artwork_creators = artwork['creators']
        artwork_technique = artwork['technique']
        artwork_type = artwork['type']
        artwork_image = artwork['images']['web']['url']
        print(f"ID: {artwork_id}")
        print(f"Title: {artwork_title}")
        print(f"Description: {artwork_desc}")
        print(f"Earliest Creation Date: {artwork_date_earliest}")
        print(f"Latest Creatoin Date: {artwork_date_latest}")
        creator_index = 1
        for creator in artwork_creators:
            name = creator.get('description')
            print(f"Creator No. {creator_index}: {name}")
        print(f"Technique: {artwork_technique}")
        print(f"Type: {artwork_type}")
        print(f"Image Details: {artwork_image}")


if __name__ == '__main__':
    print_openaccess_results()