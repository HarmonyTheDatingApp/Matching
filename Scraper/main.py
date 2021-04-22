from PopulatePlaylists import populate_playlist_tracks, save_to_database, DatabaseManager

if __name__ == '__main__':
  playlist_ids = [
    "37i9dQZF1DXbYM3nMM0oPk",
    "37i9dQZF1DX0ieekvzt1Ic",
    "37i9dQZF1DX1dCsSMSXSsP",
    "37i9dQZF1DX5q67ZpWyRrZ",
    "37i9dQZF1DWUI804Xnly9d",
    "37i9dQZF1DX0XUfTFmNBRM",
    "37i9dQZF1DWXtlo6ENS92N",
    "37i9dQZF1DWSwxyU5zGZYe",
    "37i9dQZF1DXaXB8fQg7xif",
    "37i9dQZF1DX4dyzvuaRJ0n",
    "37i9dQZF1DWXRqgorJj26U",
    "37i9dQZF1DX3rxVfibe1L0",
    "37i9dQZF1DWX76Z8XDsZzF",
    "37i9dQZF1DXbITWG1ZJKYt",
    "37i9dQZF1DX1lVhptIYRda",
    "37i9dQZF1DXasneILDRM7B"
  ]
  populate_playlist_tracks(playlist_ids)

  # import json
  # with open("37i9dQZEVXbMWDif5SCBJq.json") as f:
  #   tracks = json.load(f)
  #
  # with open('db_config.json') as f:
  #   db_config = json.load(f)
  #
  # save_to_database(DatabaseManager(db_config), db_config['table']['name'], tracks, playlist_ids[0])
