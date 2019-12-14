import requests
import spotipy.util as util
import configparser

seed_artist = "Tame Impala"
BASE_URL = "https://api.spotify.com/v1/"


class SpotifyApi:
    def __init__(self, username, scope, client_id, client_secret, redirect_uri):
        token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
        self.__headers = {"Authorization": "Bearer {}".format(token)}

    def artist_search(self, artist):
        artist_query_string = "%20".join(artist.split(" "))
        full_query_string = "{}search?q={}&type=artist".format(BASE_URL, artist_query_string)
        return self.__get(full_query_string)

    def artist_related_artists(self, artist_id):
        query_string = "{}artists/{}/related-artists".format(BASE_URL, artist_id)
        res = self.__get(query_string)
        return parse_out_related_artists(res)

    def artist_name_from_artist_id(self, artist_id):
        query_string = "{}artists/{}".format(BASE_URL, artist_id)
        res = self.__get(query_string)
        return res['name']

    def artist_albums_from_artist_id(self, artist_id):
        query_string = "{}artists/{}/albums".format(BASE_URL, artist_id)
        res = self.__get(query_string)
        return parse_out_albums(res)

    def get_tracks_from_album_id(self, album_id):
        query_string = "{}albums/{}/tracks".format(BASE_URL, album_id)
        res = self.__get(query_string)
        return parse_out_tracks(res)

    def user_playlists_from_user_id(self, user_id):
        query_string = "{}users/{}/playlists".format(BASE_URL, user_id)
        res = self.__get(query_string)
        return parse_out_playlists(res)

    def get_current_user_id(self):
        query_string = "{}me".format(BASE_URL)
        res = self.__get(query_string)
        return res['id']

    def __get(self, url):
        return requests.get(url, headers=self.__headers).json()


# ---------- SpotifyApi Utilities --------------------


def parse_out_related_artists(related_artist_response):
    return __spotify_response_json_parser(related_artist_response, 'artists')


def parse_out_albums(artist_album_response):
    return __spotify_response_json_parser(artist_album_response, 'items')


def parse_out_tracks(artist_album_response):
    return __spotify_response_json_parser(artist_album_response, 'items')


def parse_out_playlists(artist_album_response):
    return __spotify_response_json_parser(artist_album_response, 'items')


def __spotify_response_json_parser(response, key):
    return [(item['id'], item['name']) for item in response[key]]


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
    api = SpotifyApi(username, "streaming", client_id, client_secret, redirect_url)


    uid = api.get_current_user_id()
    print(uid)

    playlists = api.user_playlists_from_user_id(uid)
    print(playlists)

    print("Starting a search with artist {}".format(seed_artist))
    artist_response = api.artist_search(seed_artist)
    artists = artist_response['artists']['items']
    first_artist_id = artists[0]["id"]
    print("Artist id: {}".format(first_artist_id))
    print("Querying for artist related artists")
    print("\nAnd here they are")
    print(api.artist_related_artists(first_artist_id))

    print("getting name from id")
    first_artist_name = api.artist_name_from_artist_id(first_artist_id)
    print(first_artist_name)

    first_artist_albums = api.artist_albums_from_artist_id(first_artist_id)
    album_id, album_name = first_artist_albums[0]

    print(api.get_tracks_from_album_id(album_id))


if __name__ == "__main__":
    main()
