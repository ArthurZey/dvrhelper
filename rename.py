#!/usr/bin/env python

from tvdb_api import Tvdb
from config import config
from difflib import SequenceMatcher as SM
import argparse
import os.path
import re
import unicodedata

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
parser.add_argument("file", help="the file you wish to have automatically renamed according to Plex standards", type=str)
group.add_argument("-d", "--directory", help="the directory that contains the show directories (for name-matching)", type=str)
group.add_argument("-n", "--showname", help="manually specify show name", type=str)
parser.add_argument("--tvdbid", help="override show name matching and use thetvdb ID for show", type=int)
parser.add_argument("-s", "--season", help="override season extraction and use explicitly provided season number", type=int)
parser.add_argument("-e", "--episode", help="override episode number extraction and use explicitly provided episode number", type=int)
parser.add_argument("-v", "--verbose", help="turn on verbose output", action="store_true")
parser.add_argument("--dest", help="specify the destination directory for the file (renamed in place otherwise)", type=str)
args = parser.parse_args()

def sanitize_filename(filename):
  # first pass: get rid of accented characters
  filename = ''.join([c for c in unicodedata.normalize('NFD', filename) if unicodedata.category(c) != 'Mn'])
  
  # second pass: do specialized replacements
  replacements = {
    ": ": " - ",
    "–": "-",
    "—": "--",
    "{": "(",
    "}": ")",
    "[": "(",
    "]": ")",
    "<": "(",
    ">": ")",
    "|": " ",
    "`": "'",
    '"': "'",
    "/": "-",
    '\\': "-",
    }
  for (old, new) in replacements.items():
    filename = filename.replace(old, new)

  # third pass: go through, character by character, and strip remaining illegal characters (e.g., "?")
  valid_chars = "-_.,()!$&+='~ abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
  filename = ''.join([c for c in filename if c in valid_chars])
  
  return filename


if os.path.isfile(args.file):
  # extract data from the filename
  regex = re.compile(r'^(?P<show_filename>.*?)([sS])?(?P<season>\d{1,3})([eExX])(?P<episode>\d{1,3})')  

  match = regex.match(os.path.split(args.file)[1])
  show_raw = match.group("show_filename")
  season_raw = match.group("season")
  episode_raw = match.group("episode")
  
  # get proper show name
  if args.directory is not None and os.path.isdir(args.directory):
    directories = list()
    for item in os.listdir(args.directory):
      if os.path.isdir(os.path.join(args.directory, item)):
        directories.append(item)

    best_match = 0
    for tvshow in directories:
      match_ratio = SM(None, tvshow, show_raw).ratio()
      if match_ratio > best_match:
        best_match = match_ratio
        show_final = tvshow
  elif args.showname is not None:
    show_final = args.showname

  # set the season and episode variables
  season_int  = int(season_raw)  if args.season  is None else int(args.season)
  episode_int = int(episode_raw) if args.episode is None else int(args.episode)

  season_display  = str(season_int).zfill(len(season_raw) if len(season_raw) > 2 else 2)
  episode_display = str(episode_int).zfill(len(episode_raw) if len(episode_raw) > 2 else 2)

  # now look it up in thetvdb to get the episode name
  episode_name = ""
  tvdb = Tvdb(apikey=config["thetvdb_apikey"], language="en")
  episode_name = sanitize_filename(tvdb[show_final][season_int][episode_int]['episodename'])


  print(show_final + " - s" + season_display + "e" + episode_display + " - " + episode_name) 

else:
  "File does not exist."

# 

