from Scraper.PopulatePlaylists import populate_playlist_tracks, save_to_database, DatabaseManager
from Scraper.TransformAudio import map_previews_to_file

if __name__ == '__main__':
  map_previews_to_file(limit=1000, offset=3500)
  # playlist_ids = [
  #   "37i9dQZF1DXbYM3nMM0oPk",
  #   "37i9dQZF1DX0ieekvzt1Ic",
  #   "37i9dQZF1DX1dCsSMSXSsP",
  #   "37i9dQZF1DX5q67ZpWyRrZ",
  #   "37i9dQZF1DWUI804Xnly9d",
  #   "37i9dQZF1DX0XUfTFmNBRM",
  #   "37i9dQZF1DWXtlo6ENS92N",
  #   "37i9dQZF1DWSwxyU5zGZYe",
  #   "37i9dQZF1DXaXB8fQg7xif",
  #   "37i9dQZF1DX4dyzvuaRJ0n",
  #   "37i9dQZF1DWXRqgorJj26U",
  #   "37i9dQZF1DX3rxVfibe1L0",
  #   "37i9dQZF1DWX76Z8XDsZzF",
  #   "37i9dQZF1DXbITWG1ZJKYt",
  #   "37i9dQZF1DX1lVhptIYRda",
  #   "37i9dQZF1DXasneILDRM7B",
  #   "37i9dQZF1DX4WYpdgoIcn6",
  #   "37i9dQZF1DX5IDTimEWoTd",
  #   "37i9dQZF1DX2Y6ZOyTJZfp",
  #   "37i9dQZF1DWW0OFelDHUJP",
  #   "37i9dQZF1DWVTfbQdQ8l7H",
  #   "37i9dQZEVXbLiRSasKsNU9",
  #   "37i9dQZF1DX7yRWDZJQ3Yz",
  #   "37i9dQZF1DX1helbHcrYM1",
  #   "37i9dQZF1DWTcqUzwhNmKv",
  #   "37i9dQZF1DWTqYqGLu7kTX",
  #   "37i9dQZF1DX1ct2TQrAvRf",
  #   "37i9dQZF1DX9tPFwDMOaN1",
  #   "37i9dQZF1DX0018ciYu6bM",
  #   "37i9dQZF1DX14CbVHtvHRB",
  #   "37i9dQZF1DXaXB8fQg7xif",
  #   "37i9dQZF1DX4WgZiuR77Ef",
  #   "3DKzpfY3zkM5qBvMhBp1xF"]
  # playlist_ids = ['18mwBrB0moPrmoPshdWVNs', '37i9dQZF1DWSPMbB1kcXmo', '37i9dQZF1DWSG3ias7mSRY', '37i9dQZF1DWYBO1MoTDhZI', '37i9dQZF1DX319l60u7Jxg', '37i9dQZF1DX2pSTOxoPbx9', '37i9dQZF1DX50QitC6Oqtn', '37i9dQZF1DXaPCIWxzZwR1', '37i9dQZF1DX0BcQWzuB7ZO', '37i9dQZF1DX6VdMW310YC7', '37i9dQZF1DX2CqFedmO3RP', '37i9dQZF1DXa2huSXaKVkW', '37i9dQZF1DWZNJXX2UeBij', '37i9dQZF1DXbTxeAdrVG2l', '37i9dQZF1DX4o1oenSJRJd', '37i9dQZF1DX5Ejj0EkURtP', '37i9dQZF1DX4UtSsGT1Sbe', '37i9dQZF1DWTJ7xPn4vNaz', '37i9dQZF1DXaKIA8E7WcJj', '37i9dQZF1DWSV3Tk4GO2fq', '37i9dQZF1DX7e8TjkFNKWH', '37i9dQZF1DXdo6A3mWpdWx', '37i9dQZF1DX1rVvRgjX59F', '37i9dQZF1DX1spT6G94GFC', '37i9dQZF1DX6xnkAwJX7tn', '37i9dQZF1DWWwzidNQX6jx', '37i9dQZF1DWWzBc3TOlaAV', '37i9dQZF1DWTyiBJ6yEqeu', '37i9dQZF1DWXVJK4aT7pmk', '37i9dQZF1DX9wC1KY45plY', '3o4Sl1EoLmv43sbpkbI88d', '37i9dQZF1DX9qNs32fujYe', '37i9dQZF1DX3WvGXE8FqYX', '37i9dQZF1DXd0ZFXhY0CRF', '37i9dQZF1DX1i3hvzHpcQV']
  # populate_playlist_tracks(playlist_ids)

  # import json
  # with open("37i9dQZEVXbMWDif5SCBJq.json") as f:
  #   tracks = json.load(f)
  #
  # with open('db_config.json') as f:
  #   db_config = json.load(f)
  #
  # save_to_database(DatabaseManager(db_config), db_config['table']['name'], tracks, playlist_ids[0])
