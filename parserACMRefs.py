"""
This is the specific Parser implementation for the ACM Digital Library.
Format last tested: ... (early September 2013?)

URI spec:
A direct link to an ACM DL page. The parser will convert the link to set the preferred
layout to 'flat', if not already set, while reading.

File spec:
The URI or File should point to or contain HTML page, containing the flat ACM DL layout.

Known bugs:

"""
#HTML Parsing:                 see http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup as BS
#simple HTTP library:             see http://docs.python-requests.org/en/latest/
import requests

import re

from paper import Paper
from parser import Parser

class ACMReferencesParser(Parser):
  def read(self, fileToMemory=False):
    if self.uri:
      #use the flat layout to make sure the references are received
      if "preflayout=flat" not in self.uri:
        if "?" not in self.uri:
          self.uri +="?"
        elif not (self.uri.endswith("?") or self.uri.endswith("&")):
          self.uri += "&"
        self.uri +="preflayout=flat"
      resp = requests.get(self.uri)
      self.text=resp.text
    elif self.myFile:
      if fileToMemory:
        self.text=""
        with open(self.myFile, 'r') as f:
          for line in f:
            self.text+=line
      else:
        self.text=open(self.myFile)
    else:
      raise Exception("invalid state!")
  
  def process(self):
    if not self.text:
      raise Exception("Invalid state!")
    #the following parses out a dict of references.
    # references are in a table; a row contains a div of class 'abstract' in the
    # first td, and the actual text description (possibly with linking to the 
    # paper pages, in a variety of formats) in the second td.
    # <tr><td><div class="abstract">number</div></td><td> citation </td>
    print self.text
    if self.text and self.debugmode:
      for x in self.text:
        print x
    soup = BS(self.text)
    
    trs = soup.find_all('tr')
    citations = {}
    for i in trs:
      divs = i.find_all('div')
      if not divs:
        continue
      try:
        if divs[0].has_attr('class') and (divs[0]['class'][0] == 'abstract'):
          #reference as outputted.
          ref_name = divs[1].get_text().strip()
          #grab the URL, if any.
          ref_url= divs[1].find('a')
          if ref_url:
            ref_url="http://dl.acm.org/" + divs[1].find('a')['href']
            #parse paper metadata. This assumes one of the formats used
            #on the page. It may be separated into a different function
            #later; this will make sense esp. when similar issues are 
            #encountered for other sources.
            #approximate description of the format:
            #author , author , author, title, pubname, [v.volume n.number, ][p.pages-pages, ][month [days], year, ][location]
            ref_remaining = ref_name
            ref_authors=[]
            ref_title=""
            ref_year=-1
            if ' , ' in ref_name:
              #parse all but the last author into a neat string list
              ref_authors = re.split(' , ', ref_name)
              ref_remaining = ref_authors[-1:][0]
              ref_authors = ref_authors[:-1]
              #the last author is followed by ', ', so it is still to be moved...
              ref_authors.append(ref_remaining[:ref_remaining.find(', ')])
              ref_remaining=ref_remaining[ref_remaining.find(', ')+2:]
              #now the title follows. unfortunately, it may contain commas. For now, we assume it doesn't, until I think of an elegant solution. Searching for the start of the publication name doesn't work ('IEEE' often appears in titles).
              ref_title = ref_remaining[:ref_remaining.find(', ')]
              ref_remaining=ref_remaining[ref_remaining.find(', ')+2:]
              #lastly, the year is somewhere at the end.
              tmp = ref_remaining.split(', ')
              for i in range(len(tmp)-1, 0, -1):
                if tmp[i].isdigit():
                  ref_year=int(tmp[i])
                  break
                elif tmp[i].strip()[-4:].isdigit():
                  ref_year=int(tmp[i].strip()[-4:])
                  break
            citations[ref_name]=Paper(ref_authors, ref_title, ref_year, ref_name, url=ref_url)
          else: #no URL parse-able, which implies a different format.
            continue #other formats to be implemented. However, this will be raw OCRd data, I'll need a function that resolves potential conflicts. This might, for example, work by checking google scholar and/or asking the user.
      except IndexError:
        print "Error parsing " +divs
    if self.uri:
      self.paper=Paper(None,None,None,None,url=self.uri,references=citations)
    else:
      self.paper=Paper(None,None,None,None,other_data="Parsed from "+self.myFile,references=citations)
    return self.paper

#def parse_ieee(url=...)
#def parse_springer(url=...)

