import requests
import os


class SpotifyClient:
    def __init__(self):
        self.user_id = os.getenv("SPOTIFY_USER_ID")
        self.auth_token = RefreshToken().get_token()
    
    def get_songs_in_playlist(self, playlist_id):
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.auth_token)})

        response_json = response.json()
        return response_json


# Spotify authorization tokens expire after 1hr, we need to request a refresh from Spotify
class RefreshToken:
    def __init__(self):
        self.refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')
        self.client_id_secret_b64 = os.getenv('SPOTIFY_CLIENT_ID_SECRET_B64')

    def get_token(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": self.refresh_token},
                                 headers={"Authorization": f"Basic {self.client_id_secret_b64}"})

        response = response.json()
        return response["access_token"]