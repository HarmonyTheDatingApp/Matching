import json
import os
import sqlite3
from typing import Dict, List
from Spotify import Spotify


class DatabaseManager:
  def __init__(self, config: Dict):
    self.config = config
    con = sqlite3.connect(config['db_name'])
    cur = con.cursor()
    
    try:
      cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.config['table']['name']}
        (
	        'name'	TEXT NOT NULL,
	        'popularity'	INTEGER NOT NULL,
	        'duration_ms'	REAL NOT NULL,
	        'id'	TEXT,
	        'preview_url'	TEXT,
	        'artists_name'	TEXT,
	        'artists_id'	TEXT
        );"""
                  )
      con.commit()
    except Exception as e:
      print(f"Something went wrong while creating table: {str(e)}")
    finally:
      con.close()
  
  def get_connection(self):
    return sqlite3.connect(self.config['db_name'])

def populate_playlist_tracks(playlist_ids: List[str]):
  client = Spotify()
  
  with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'db_config.json')) as f:
    db_config = json.load(f)
  db_client = DatabaseManager(config=db_config)
  
  for i, playlist_id in enumerate(playlist_ids):
    print(f"Fetching playlist: {i} -> {playlist_id}")
    tracks = client.get_playlist(playlist_id)
    
    print(f"Saving playlist: {i} -> {playlist_id}")
    save_to_database(db_client, db_config['table']['name'], tracks, playlist_id)

def save_to_database(db_client, table_name, tracks, playlist_id):
  insert_query = f"INSERT INTO {table_name}"
  data = []
  for i in range(len(tracks)):
    track = tracks[i]
    single_query = f"SELECT ? AS 'name', ? AS 'popularity', ?" \
                   f" AS 'duration_ms', ? AS 'id', ? AS 'preview_url'," \
                   f"? AS 'artists_name'," \
                   f"? AS 'artists_id'"
    data += [
      track['name'],
      track['popularity'],
      track['duration_ms'],
      track['id'],
      track['preview_url'],
      ':'.join(artist['name'] for artist in track['artists']),
      ':'.join(artist['id'] for artist in track['artists'])
    ]
    # single_query = f"SELECT '{track['name']}' AS 'name', {track['popularity']} AS 'popularity', {track['duration_ms']}" \
    #                f" AS 'duration_ms', '{track['id']}' AS 'id', '{track['preview_url']}' AS 'preview_url'," \
    #                f"'{':'.join(artist['name'] for artist in track['artists'])}' AS 'artists_name'," \
    #                f"'{':'.join(artist['id'] for artist in track['artists'])}' AS 'artists_id'"
    if i == 0:
      insert_query = f"{insert_query}\n{single_query}"
    else:
      insert_query = f"{insert_query}\nUNION ALL {single_query}"
  
  conn = db_client.get_connection()
  try:
    cur = conn.cursor()
    cur.execute(insert_query, tuple(data))
    conn.commit()
  except Exception as e:
    print(f"Something went wrong while saving playlist data in batch: {str(e)}")
    print(f"Saving extracted file: {playlist_id}.json...", end=' ')
    with open(f'{playlist_id}.json', 'w', encoding='utf-8') as f:
      json.dump(tracks, f)
    print("Done.")
  finally:
    conn.close()
