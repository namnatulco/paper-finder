"""
This is the specific Parser implementation for the ACM Digital Library.

URI spec:

File spec:

Known bugs:
This parser is incomplete.

"""
#HTML Parsing:                 see http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup as BS
#simple HTTP library:             see http://docs.python-requests.org/en/latest/
import requests

import re

from paper import Paper
from parser import Parser

class ACM_Parser(Parser):
  def read(self):
    if self.uri:
      #use the flat layout to make sure the references are received
      if "preflayout=flat" not in self.uri:
        if "?" not in self.uri:
          self.uri +="?"
        elif not (self.uri.endswith("?") or self.uri.endswith("&")):
          self.uri += "&"
        self.uri +="preflayout=flat"
      resp = requests.get(self.uri)
      text=resp.text
    elif self.file:
      text=open(self.file)
    else:
      raise Exception("invalid state!")
  
  def process(self):
    if not self.text:
      raise Exception("Invalid state!")
    self.paper=ACM_References_Parser(self.text)
