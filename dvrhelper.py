
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