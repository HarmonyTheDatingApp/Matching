import json
import base64
import requests
import os
import logging
from typing import Dict, List


def get_config():
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')) as f:
    config = json.load(f)
  return config


class Spotify:
  BASE_URL = "https://api.spotify.com"
  logging.basicConfig(filename='Spotify.log')
  
  def __init__(self):
    self.config = get_config()
    self.access_token = Spotify.__get_access_token(**self.config)
  
  @staticmethod
  def __get_access_token(client_id: str, client_secret: str) -> str:
    client_credentials = base64.b64encode(f"{client_id}:{client_secret}".encode('ascii')).decode()
    res = requests.post(f"https://accounts.spotify.com/api/token",
                        headers={'Authorization': f"Basic {client_credentials}"},
                        data={'grant_type': 'client_credentials'})
    
    return res.json()['access_token']
  
  def make_api_call(self, method: str, url: str, headers: Dict = {}, data: Dict = {}, **kwargs):
    res = requests.request(method, url, headers=headers, data=data, **kwargs)
    
    if res.status_code == requests.codes.ok:
      return res.json()
    
    if res.status_code == requests.codes.unauthorized:
      self.access_token = Spotify.__get_access_token(**self.config)
      return self.make_api_call(method, url, headers, data, **kwargs)
    
    raise ValueError(res.json()['error']['message'])
  
  def get_raw_preview_for_track(self, id: str):
    res = self.make_api_call('get', f"{Spotify.BASE_URL}/v1/tracks/{id}",
                             headers={'Authorization': f"Bearer {self.access_token}"})
    
    preview_url = res['preview_url']
    
    # TODO: Do this separately
    preview_res = res.get(preview_url, stream=True)
    with open('id.mp3', 'wb') as f:
      f.write(preview_res.content)
  
  def get_playlist(self, pid: str) -> List:
    res = self.make_api_call('get', url=f"{Spotify.BASE_URL}/v1/playlists/{pid}/tracks?market=US",
                             headers={'Authorization': f'Bearer {self.access_token}',
                                      'Accept': 'application/json',
                                      'Content-Type': 'application/json'})
    
    data = Spotify.__extract_playlist_data(res, [])
    
    while res['next']:
      res = self.make_api_call('get', url=res['next'],
                               headers={'Authorization': f'Bearer {self.access_token}',
                                        'Accept': 'application/json',
                                        'Content-Type': 'application/json'})
      data = Spotify.__extract_playlist_data(res, data)
    
    return data
  
  def get_audio_features(self, track_ids: List[str], normalize: bool = False) -> List[Dict]:
    res = self.make_api_call('get', url=f"{Spotify.BASE_URL}/v1/audio-features",
                             headers={
                               'Authorization': f'Bearer {self.access_token}',
                               'Accept': 'application/json',
                               'Content-Type': 'application/json'
                             },
                             params={'ids': ','.join(track_ids)})
    
    features = Spotify.audio_features_list()
    data = []
    
    for i, item in enumerate(res['audio_features']):
      if item is None:
        logging.warning(f"{track_ids[i]} does not have audio features. Omitted.")
        continue
      track_features = {}
      for feature in features:
        track_features[feature] = item[feature]
      
      if normalize:
        """
        Normalizes loudness (assumed range: 0 - -60) and tempo (assumed range: 50 - 200).
        Hardmax/Hardmin if values out of range.
        """
        x = track_features['loudness']
        x = max(min(x, 0), -60) / (-60)
        track_features['loudness'] = round(x, 4)
        
        x = track_features['tempo']
        x = (max(min(x, 200), 50) - 50) / (200 - 50)
        track_features['tempo'] = round(x, 4)
      
      data.append(track_features)
    
    return data
  
  @staticmethod
  def __extract_playlist_data(res: Dict, data: List) -> List:
    for item in res['items']:
      item = item['track']
  
      artists = []
      for artist in item['artists']:
        artists.append({
          'name': artist['name'],
          'id': artist['id']
        })
  
      data.append({
        'name': item['name'],
        'popularity': item['popularity'],
        'duration_ms': item['duration_ms'],
        'id': item['id'],
        'preview_url': item['preview_url'],
        'artists': artists
      })
    
    return data

  @staticmethod
  def audio_features_list():
    return ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                  'instrumentalness', 'liveness', 'valence', 'tempo']
