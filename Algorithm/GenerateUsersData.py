import json
import sqlite3
import random
from itertools import repeat
from tqdm import tqdm
from typing import List
from Algorithm.Clusters import compute_clusters_in_tracks
from Scraper.Spotify import Spotify

def table_exists(dbcon, tablename):
  dbcur = dbcon.cursor()
  dbcur.execute("""
    SELECT COUNT(*)
    FROM sqlite_master
    WHERE type='table'
    AND name = '{0}'
    """.format(tablename.replace('\'', '\'\'')))
  if dbcur.fetchone()[0] == 1:
    dbcur.close()
    return True
  
  dbcur.close()
  return False

def generate_users(n: int):
  con = sqlite3.connect("Users.db")
  cur = con.cursor()
  table_name = 'Users'
  
  if table_exists(con, table_name):
    ans = input("'Users' table already exists in 'Users.db'. Want to drop it and refill? y/n")
    if ans.lower() == 'y' or ans.lower() == 'yes':
      cur.execute('DROP TABLE "Users";')
      con.commit()
    else:
      table_name = input("Give new table name: ")
      if table_exists(con, table_name):
        print(f"{table_name} already exists.")
        con.close()
        exit(-1)
  
  table_name = table_name.replace('"', '""')
  
  cur.execute(f'''CREATE TABLE IF NOT EXISTS "{table_name}" (
    "user_id" INTEGER PRIMARY KEY,
	  "v1" TEXT,
	  "v2" TEXT,
	  "v3" TEXT,
	  "v4" TEXT
  );''')
  con.commit()
  
  user_ids = list(range(1, n+1))
  cur.executemany(f"INSERT INTO {table_name} VALUES (?, NULL, NULL, NULL, NULL)",
                  [(user_id,) for user_id in user_ids])
  con.commit()
  
  cur.execute(f'''CREATE TABLE IF NOT EXISTS Tracks (
    "user_id" INTEGER,
    "track" TEXT,
    FOREIGN KEY(user_id) REFERENCES {table_name}(user_id)
  )''')
  
  with open('Scraper/db_config.json') as f:
    db_config = json.load(f)
  con_playlist = sqlite3.connect(f"Scraper/{db_config['db_name']}")
  cur_playlist = con_playlist.cursor()
  
  songs_table = db_config['table']['name']
  cur_playlist.execute(f"SELECT COUNT(*) FROM {songs_table};")
  
  tracks_per_user = 50
  tracks = [row[0] for row in cur_playlist.execute(f"SELECT DISTINCT id FROM {songs_table};")]
  con_playlist.close()
  
  for user_id in user_ids:
    curr_user_tracks = random.choices(tracks, k=tracks_per_user)
    cur.executemany("INSERT INTO Tracks VALUES (?, ?)", zip(repeat(user_id), curr_user_tracks))
    print(f"Generated user: {user_id}")
    
  con.commit()
  print(f"All data saved. Stats:\n'Users' table contains {n} users.\n'Tracks' table contains {n*50} tracks.")


def compute_clusters_per_users(user_ids: List[int], db_name: str, users_table: str = 'Users',
                               tracks_table: str = 'Tracks', n_clusters: int = 4):
  con = sqlite3.connect(db_name)
  cur = con.cursor()
  client = Spotify()
  
  for i, user_id in enumerate(tqdm(user_ids)):
    tracks = [row[0] for row in cur.execute(f"SELECT track FROM {tracks_table} WHERE user_id={user_id};")]
    
    audio_features = client.get_audio_features(tracks, normalize=True)
    vectors = compute_clusters_in_tracks(audio_features, Spotify.audio_features_list(), n_clusters)
    
    cur.execute(f'''UPDATE {users_table} SET v1=?, v2=?, v3=?, v4=? WHERE user_id=?;''', (
      str(vectors[0].tolist()),
      str(vectors[1].tolist()),
      str(vectors[2].tolist()),
      str(vectors[3].tolist()),
      user_id
    ))
    con.commit()

  con.close()
