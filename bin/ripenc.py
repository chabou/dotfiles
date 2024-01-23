#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#######################
# ripenc.py
#######################
# - Rip d'un CD Audio
# - Récupération Titre/Artiste
# - Encodage AAC, MP3, FLAC
# - Génération de la playlist
# - Ménage
#######################
# Compatibilité :
# - MacOS
# - Linux
#######################

import subprocess # commandes externes
import urllib.request # requête http
import configparser # lecture .ini
import re # regexp
import os # renommage fichiers
import glob # recherche de fichiers

# Dépendances binaires externes devant se trouver dans le path
DEPENDENCIES = [
  'cdparanoia',
  'cd-discid',
  'ffmpeg'
]

# Ripper le CD Audio ?
CD_RIP = True

# Chemin du lecteur de CD (à adapter)
CD_PATH = "/dev/disk4"

# Récupérer les titres sur gnudb et renommer les fichiers extraits
# Le CD Audio doit toujours être dans le lecteur
GNUDB_REQUEST = True

# type d'encodage à effectuer : aac|flac|mp3|False
ENCODE_FORMAT = 'mp3'

# effacer le .wav d'origine à la fin de l'encodage ?
CLEAN_WAV = True

# générer la liste de lecture
PLAYLIST_CREATE = True

# nom de la liste de lecture
PLAYLIST_NAME = "playlist.m3u"

def check_dependencies():
  print("- Vérification des dépendances")
  for cmd in DEPENDENCIES:
    subprocess.run(['command', '-v', cmd], check=True, universal_newlines=True)
  print("OK")

def cd_rip():
  print("- RIP du CD audio")
  subprocess.run(['cdparanoia', '-XB'], check=True, universal_newlines=True)

def get_discid():
  print("- Récupération du discid")
  cp = subprocess.run(['cd-discid', CD_PATH], check=True, universal_newlines=True, stdout=subprocess.PIPE)
  # ex: 6a09de08 8 150 49017 76397 94357 112290 137397 154280 164597 2528
  ret = cp.stdout.split()
  return ret[0]

def get_gnudb(discid):
  print('- Récupération des metadonnées sur gnudb.org')
  url = 'https://gnudb.org/gnudb/' + discid
  str = urllib.request.urlopen(url).read().decode("utf-8")
  cfg = configparser.ConfigParser()
  cfg.read_string('[root]\n' + str) # section root factice
  dict = {}
  for option in cfg.options('root'):
    dict[option] = cfg.get('root', option) # les options ont été lowercasées
  return dict

def rename_tracks(dict):
  print('- Renommage des fichiers')
  for key in dict:
    m = re.search('ttitle([0-9]{1,2})', key)
    if m:
      track_number = format(int(m.group(1)) + 1, '02d')
      orig_file = 'track' + track_number + '.cdda.wav'
      dest_file = track_number + ' - ' + dict[key] + '.wav'
      print('key: ' + key + ' value= ' + dict[key] + ' track_number = ', track_number)
      print('rename ' + orig_file + ' -> ' + dest_file)
      if os.path.isfile(orig_file):
        os.rename(orig_file, dest_file)
        print('OK')
      else:
        print('fichier ' + orig_file + ' non trouvé')

def encode_wavs():
  files = glob.glob('*.wav')
  files.sort() # glob ne fait aucun tri
  for file in files:
    print('- Traitement ' + file)

    if ENCODE_FORMAT == 'aac':
      encode_aac(file)
    elif ENCODE_FORMAT == 'flac':
      encode_flac(file)
    elif ENCODE_FORMAT == 'mp3':
      encode_mp3(file)

    if CLEAN_WAV:
      clean_wav(file)

def clean_wav(file):
  print("- Suppression " + file)
  os.remove(file)

def encode_aac(input):
  output = input.replace('.cdda.wav', '').replace('.wav', '') + '.m4a'
  print('- Encodage AAC : ' + input + ' -> ' + output)
  subprocess.run(['ffmpeg', '-y', '-hide_banner', '-i', input, '-c:a', 'aac', '-b:a', '160k', output], check=True, universal_newlines=True)
  if PLAYLIST_CREATE:
    playlist_append(output)

def encode_flac(input):
  output = input.replace('.cdda.wav', '').replace('.wav', '') + '.flac'
  print('- Encodage FLAC : ' + input + ' -> ' + output)
  subprocess.run(['ffmpeg', '-y', '-hide_banner', '-i', input, '-c:a', 'flac', output], check=True, universal_newlines=True)
  if PLAYLIST_CREATE:
    playlist_append(output)

def encode_mp3(input):
  output = input.replace('.cdda.wav', '').replace('.wav', '') + '.mp3'
  print('- Encodage MP3 : ' + input + ' -> ' + output)
  subprocess.run(['ffmpeg', '-y', '-hide_banner', '-i', input, '-c:a', 'libmp3lame', '-b:a', '320k', output], check=True, universal_newlines=True)
  if PLAYLIST_CREATE:
    playlist_append(output)

def playlist_append(file):
  print('- Ajout ' + file + ' à la liste de lecture')
  f = open(PLAYLIST_NAME, 'a')
  f.write(file + "\n")
  f.close()

if __name__ == '__main__':
  check_dependencies()
  if CD_RIP:
    cd_rip()
  if GNUDB_REQUEST:
    discid = get_discid()
    print('discid: ' + discid)

    info = get_gnudb(discid)
    if info:
      rename_tracks(info)

  encode_wavs()
