"""
A Parser processes a single input into a Paper instances (possibly incomplete)

In general, a parser parses a references' page and the references as displayed
on its page (in whichever format the parser expects).
The references are written to a dictionary (see Paper documentation).

A parser should always accept both file and url input; file input is default.
Partial parsers may accept text input (usually an iterable, such as a file object).
Order: text > file > uri

A parser may use sub-parser(s) to modularize certain steps that repeat, or to
process different outputs from the same source (e.g., a DOI resolver could be 
implemented this way).

Workflow for parsers:
create instance -> read -> process -> read Parser.paper
"""

from paper import Paper

class Parser():
  debugmode=False
  uri=None
  file=None
  text=None
  paper=None
  
  def __init__(self, file=None, uri=None, text=None):
    if not file and not uri and not text:
      raise Exception("Must provide file, text or uri")
    elif text:
      self.text=text
    elif file:
      self.file=file
    elif uri:
      self.uri=uri
  
  def read(self):
    if file:
      pass
    elif uri:
      pass
    else:
      raise Exception("Invalid state!")
  
  def process(self):
    pass
