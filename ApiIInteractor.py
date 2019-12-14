import requests
import spotipy.util as util
import configparser

seed_artist = "Tame Impala"
BASE_URL = "https://api.spotify.com/v1/"


class ApiInteractor:
    def __init__(self, username, scope, client_id, client_secret, redirect_uri):
        token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
        self.__headers = {"Authorization": "Bearer {}".format(token)}

    def artist_search(self, artist):
        artist_query_string = "%20".join(artist.split(" "))
        full_query_string = "{}search?q={}&type=artist".format(BASE_URL, artist_query_string)
        return self.__get(full_query_string)

    def artist_related_artists(self, artist_id):
        full_query_string = "{}artists/{}/related-artists".format(BASE_URL, artist_id)
        res = self.__get(full_query_string)
        return parse_out_related_artist_ids(res)

    def __get(self, url):
        return requests.get(url, headers=self.__headers).json()


# ---------- ApiInteractor Utilities --------------------


def parse_out_related_artist_ids(related_artist_response):
    artist_lst = related_artist_response['artists']
    return [artist['id'] for artist in artist_lst]


def read_config():
    config = configparser.ConfigParser()
    config.read(".config")
    username = config.get("DEFAULT", "username")
    client_id = config.get("DEFAULT", "client_id")
    client_secret = config.get("DEFAULT", "client_secret")
    redirect_url = config.get("DEFAULT", "redirect_url")

    return username, client_id, client_secret, redirect_url


def main():
    username, client_id, client_secret, redirect_url = read_config()
    api = ApiInteractor(username, "streaming", client_id, client_secret, redirect_url)

    print("Starting a search with artist {}".format(seed_artist))
    artist_response = api.artist_search(seed_artist)
    artists = artist_response['artists']['items']
    first_artist_id = artists[0]["id"]
    print("Artist id: {}".format(first_artist_id))
    print("Querying for artist related artists")
    print("\nAnd here they are")
    print(api.artist_related_artists(first_artist_id))



if __name__ == "__main__":
    main()
