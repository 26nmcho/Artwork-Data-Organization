import json
import requests

# trackers
no_id = 0
no_title = 0
no_desc = 0
no_early_date = 0
no_late_date = 0 
no_creator = 0
no_technique = 0
no_image = 0



def data_collection(skip, limit):
    url = "https://openaccess-api.clevelandart.org/api/artworks"
    params = {
            'has_image': 1,
            'limit': limit,
            'type': 'Painting',
            'skip' : skip,
            'fields' : 'id,title,description,creation_date_earliest,creation_date_latest,creators,technique,type,images,url,share_license_status'
        }

    r = requests.get(url, params=params)

    data = r.json()

    accepted_artworks  = []

    for artwork in data['data']:
        artwork_id = artwork.get('id')
        artwork_title = artwork.get('title')
        artwork_desc = artwork.get('description')
        artwork_date_earliest = artwork.get('creation_date_earliest')
        artwork_date_latest = artwork.get('creation_date_latest')
        artwork_creators = artwork.get('creators')
        artwork_technique = artwork.get('technique')
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
            'image' : artwork_image
        }

        if data_validation(artwork):
            accepted_artworks.append(artwork)

    return accepted_artworks


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
    return return_boolean


if __name__ == '__main__':
    results = data_collection(0, 3)
    print(type(results))
    print(len(results))
    print(results[0])

    test_artwork = {
    "id": 1,
    "title": "Test",
    "description": "Test description",
    "creation date early": 1900,
    "creation date late": 1901,
    "creators": ["Test Artist"],
    "technique": "Oil on canvas",
    "image": "https://example.com/image.jpg"
    }

    print(data_validation(test_artwork))