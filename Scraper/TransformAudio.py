from pydub import AudioSegment
import numpy as np
from scipy import signal
import random
import json
from multiprocessing import Pool
from itertools import repeat
from Scraper.Spotify import Spotify
from Scraper.PopulatePlaylists import DatabaseManager
from typing import List, Tuple
import logging

def transform_audio(audio: AudioSegment, audio_len: int = 5) -> List:
  millis_per_sec = 1000
  preview_len = 30
  
  audio = audio.set_channels(1)[:millis_per_sec * preview_len]
  random_idx = random.randint(0, len(audio) - millis_per_sec * audio_len - 1)
  array = np.array(audio[random_idx:random_idx + millis_per_sec * audio_len].get_array_of_samples())
  
  freqs, times, spec = signal.spectrogram(
    array,
    fs=audio.frame_rate,
    window='hanning',
    nperseg=512,
    noverlap=0,
    detrend=False,
    scaling='spectrum'
  )
  
  return spec.flatten().tolist()


def save_preview(args: Tuple, table_name: str):
  global con, client
  track_id, preview_url = args
  
  client.download_preview(track_id, preview_url, verbose=True)
  audio = AudioSegment.from_mp3(f'previews/{track_id}.mp3')
  spec = transform_audio(audio)
  cur = con.cursor()
  
  query = "INSERT INTO {} (track_id, spec) VALUES (?, ?)".format(table_name.replace('"', '""'))
  try:
    cur.execute(query, (track_id, str(spec)))
    con.commit()
  except Exception as e:
    logging.warning(f"{track_id} preview was not saved: {str(e)}")
    return False
  
  return True

def initialize_worker():
  global con, client
  with open('db_config.json') as f:
    db_config = json.load(f)
  
  db_client = DatabaseManager(db_config)
  con = db_client.get_connection()
  client = Spotify()

def map_previews_to_file(limit: int = None, offset: int = None):
  logging.basicConfig(filename='TransformAudio.log', level=logging.DEBUG)
  
  with open('db_config.json') as f:
    db_config = json.load(f)

  if not db_config['spec']:
    raise ValueError("Set 'spec' value to true in 'db_config.json'.")

  db_client = DatabaseManager(db_config)
  con = db_client.get_connection()
  cur = con.cursor()
  
  query = 'SELECT DISTINCT id, preview_url FROM "{}" WHERE preview_url IS NOT NULL'.format(db_config['table']['name'].
                                                                                           replace('"', '"""'))
  if limit:
    query += f" LIMIT {limit}"
  if limit and offset:
    query += f" OFFSET {offset}"
  
  data = []
  for row in cur.execute(query):
    data.append(row)
  
  cur = con.cursor()
  
  try:
    cur.execute("""CREATE TABLE IF NOT EXISTS spec ('track_id' TEXT NOT NULL, 'spec' TEXT NOT NULL);""")
    con.commit()
  except Exception as e:
    print(f"Something went wrong while creating 'spec' table: {str(e)}")
  finally:
    con.close()

  with Pool(processes=4, initializer=initialize_worker) as pool:
    res = pool.starmap(save_preview, zip(data, repeat('spec')))
  
  con.close()
  
  if len(res) != sum(res):
    logging.warning(f"{len(res) - sum(res)} previews not saved.")
