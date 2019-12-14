import requests
import spotipy.util as util
import configparser

seed_artist = "Tame Impala"

BASE_URL = "https://api.spotify.com/v1"

artist_search_query = "/search?q={}&type=artist"
related_artist_query = "/artists/{}/related-artists"
artist_name_from_id_query = "/artists/{}"
albums_from_artist_id_query = "/artists/{}/albums"
tracks_from_album_id_query = "/albums/{}/tracks"
playlists_for_user_id_query = "/users/{}/playlists"
current_user_query = "/me"

class SpotifyApi:
    def __init__(self, username, scope, client_id, client_secret, redirect_uri):
        token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
        self.__headers = {"Authorization": "Bearer {}".format(token)}

    def artist_search(self, artist):
        artist_search_text = "%20".join(artist.split(" "))
        query = build_query(artist_search_query, artist_search_text)
        artist_response = self.__get(query)
        return parse_out_first_artist_id(artist_response)

    def artist_related_artists(self, artist_id):
        query = build_query(related_artist_query, artist_id)
        res = self.__get(query)
        return parse_out_related_artists(res)

    def artist_name_from_artist_id(self, artist_id):
        query = build_query(artist_name_from_id_query, artist_id)
        res = self.__get(query)
        return res['name']

    def artist_albums_from_artist_id(self, artist_id):
        query = build_query(albums_from_artist_id_query, artist_id)
        res = self.__get(query)
        return parse_out_albums(res)

    def get_tracks_from_album_id(self, album_id):
        query = build_query(tracks_from_album_id_query, album_id)
        res = self.__get(query)
        return parse_out_tracks(res)

    def user_playlists_from_user_id(self, user_id):
        query = build_query(playlists_for_user_id_query, user_id)
        res = self.__get(query)
        return parse_out_playlists(res)

    def get_current_user_id(self):
        res = self.__get(build_query(current_user_query))
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


def parse_out_first_artist_id(artist_response):
    artists = artist_response['artists']['items']
    return artists[0]["id"]


def build_query(query_extension, query_parameters=None):
    return BASE_URL + (query_extension.format(query_parameters) if query_parameters else query_extension)


def read_config():
    config = configparser.ConfigParser()
    config.read(".config")
    username = config.get("DEFAULT", "username")
    client_id = config.get("DEFAULT", "client_id")
    client_secret = config.get("DEFAULT", "client_secret")
    redirect_url = config.get("DEFAULT", "redirect_url")

    return username, client_id, client_secret, redirect_url

# ---------- Demos --------------------


def demo_everything():
    username, client_id, client_secret, redirect_url = read_config()
    api = SpotifyApi(username, "streaming", client_id, client_secret, redirect_url)

    uid = api.get_current_user_id()
    display_demo("Getting current user id", uid)

    playlists = api.user_playlists_from_user_id(uid)
    display_demo("Playlists for the current user", playlists)

    artist_id = api.artist_search(seed_artist)
    display_demo("Searching for an artist ID with the query: {}".format(seed_artist), artist_id)

    name = api.artist_name_from_artist_id(artist_id)
    display_demo("Getting artist name from the id: {}".format(artist_id), name)

    artist_albums = api.artist_albums_from_artist_id(artist_id)
    display_demo("Getting albums for {}".format(artist_id), artist_albums)

    album_id, album_name = artist_albums[0]
    tracks = api.get_tracks_from_album_id(album_id)
    display_demo("Getting all the tracks for an album of {}".format(artist_id), tracks)


def display_demo(description, demo_block_result):
    print("--------------------------------\n")
    print(description + ":")
    print("{}\n".format(demo_block_result))

    return demo_block_result


def main():
    demo_everything()


if __name__ == "__main__":
    main()
