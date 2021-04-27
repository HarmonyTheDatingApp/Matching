from Scraper.Spotify import Spotify
import numpy as np
from sklearn.cluster import KMeans
from typing import List, Dict

def compute_clusters_in_tracks(audio_features: List[Dict], features_list: List[str], n_clusters: int) -> np.ndarray:
  """
  Computes clusters in audio tracks in 11 dimensional space to identify several musical tastes.
  :param audio_features: Assume normalized (not standardized)
  :param features_list: List of audio features
  :param n_clusters: number of clusters (vectors) to return. Represents musical tastes.
  :return: n vectors
  """
  
  vectors = [[track[feature] for feature in features_list] for track in audio_features]
  arr = np.array(vectors)
  kmeans = KMeans(n_clusters=n_clusters, random_state=42)
  kmeans.fit(arr)
  
  return kmeans.cluster_centers_
