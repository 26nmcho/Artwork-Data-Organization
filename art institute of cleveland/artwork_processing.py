import json
import requests


def print_openaccess_results():
    url = "https://openaccess-api.clevelandart.org/api/artworks"
    params = {
            'has_image': 1,
            'limit': 25,
            'type': 'painting',
            'skip' : 0,
            'fields' : 'id,title,description,creation_date_earliest,creation_date_latest,creators,technique,type,images,url,share_license_status'
        }

    r = requests.get(url, params=params)

    data = r.json()

    for artwork in data['data']:
        artwork_metadata = artwork['id']['title']['description']['creation_date_earliest']['creation_date_latest']['creators']['technique']['type']
        artwork_image = artwork['images']['web']['url']

        print(f"{artwork_metadata}\n{artwork_image}\n---")

if __name__ == '__main__':
    print_openaccess_results()