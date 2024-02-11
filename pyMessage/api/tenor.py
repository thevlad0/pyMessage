import requests
import json

API_KEY = 'AIzaSyAVuwnMyrhdo3DAdWRSAR8PHO7AxWaczwQ'
C_KEY = 'pyMessage'

def search(to_search):
    lmt = 8

    r = requests.get(
        "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (to_search, API_KEY, C_KEY, 8))

    if r.status_code == 200:
        top_8gifs = json.loads(r.content)
        print(top_8gifs)
    else:
        top_8gifs = None

def advanced_search(to_search):   
    # get the top 10 featured GIFs - using the default locale of en_US
    r = requests.get(
        "https://tenor.googleapis.com/v2/featured?key=%s&client_key=%s&limit=%s" 
        % (API_KEY, C_KEY, 10))

    if r.status_code == 200:
        featured_gifs = json.loads(r.content)
    else:
        featured_gifs = None

    r = requests.get(
        "https://tenor.googleapis.com/v2/categories?key=%s&client_key=%s" % (API_KEY, C_KEY))

    if r.status_code == 200:
        categories = json.loads(r.content)
    else:
        categories = None

    print (featured_gifs)
    print (categories)