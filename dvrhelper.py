
from tvdb_api import Tvdb
from config import config
from difflib import SequenceMatcher as SM
import os.path
import re
import unicodedata

# Look at https://github.com/midgetspy/Sick-Beard/blob/development/sickbeard/name_parser/parser.py

class DVRFile:
  def __init__(self, path):
    self.path            = dict()
    self.show_name       = dict()
    self.season          = dict()
    self.season["num"]   = dict()
    self.episode         = dict()
    self.episode["num"]  = dict()
    self.episode["name"] = dict()

    self.tvdb = Tvdb(apikey=config["thetvdb_apikey"], language="en")

    self.path["given"] = path

    if os.path.isfile(path):
      self.path["dir"], self.path["filename"] = os.path.split(os.path.abspath(path))
    else:
      self.path["dir"] = None
      self.path["filename"] = os.path.split(path)[1]

    self.path["ext"] = os.path.splitext(self.path["filename"])[1]

    self.show_name["raw"], self.season["num"]["raw"], self.episode["num"]["raw"] = self.__filename_regex_extract(self.path["filename"])

    self.season["num"]["int"]  = int(self.season["num"]["raw"])
    self.episode["num"]["int"] = int(self.episode["num"]["raw"])

    self.season["num"]["disp"]  = str(self.season["num"]["int"]).zfill(len(self.season["num"]["raw"]) if len(self.season["num"]["raw"]) > 2 else 2)
    self.episode["num"]["disp"] = str(self.episode["num"]["int"]).zfill(len(self.episode["num"]["raw"]) if len(self.episode["num"]["raw"]) > 2 else 2)

  def __filename_regex_extract(self, filename):
    regex = re.compile(r'^(?P<show_name>.*?)([sS])?(?P<season>\d{1,3})([eExX])(?P<episode>\d{1,3})')  

    match = regex.match(filename)

    return [match.group("show_name"), match.group("season"), match.group("episode")]

  def set_show_name(self, method="tvdb_search", lookup_data=None):
    # sets self.show_name["disp"] based on self.show_name["raw"] and some transformation

    if method == "tvdb_id":
      # expected lookup_data is the int for the show's tvdb show ID
      self.show_name["disp"] = self.tvdb[lookup_data].data["seriesname"]
    elif method == "dir_search" and os.path.isdir(lookup_data):
      # expected lookup_data is a string for the path to a directory containing directories for each TV show

      # get the list of directories to match against
      directories = list()
      for item in os.listdir(lookup_data):
        if os.path.isdir(os.path.join(lookup_data, item)):
          directories.append(item)

      best_match = 0
      for tvshow in directories:
        match_ratio = SM(None, tvshow, self.show_name["raw"]).ratio()
        if match_ratio > best_match:
          best_match = match_ratio
          self.show_name["disp"] = tvshow

    elif method == "explicit":
      self.show_name["disp"] = lookup_data
    else:
      # assume "tvdb_search"; no expected lookup_data
      # need to pass the show formatted more correctly to get a match:
      self.show_name["disp"] = self.tvdb["".join([c if c not in (".", "_") else " " for c in self.show_name["raw"]])].data["seriesname"]

  def set_episode_name(self):
    # expects self.show_name["disp"] to be set, uses thetvdb to get the name
    self.episode["name"]["official"] = self.tvdb[self.show_name["disp"]][self.season["num"]["int"]][self.episode["num"]["int"]]['episodename']
    self.episode["name"]["file"]     = self.sanitize_filename(self.episode["name"]["official"])


