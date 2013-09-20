################################################################################
# This file contains simple parsers based on the BeautifulSoup library.        #
# These parse the references as defined by their web page, and return them in  #
# the following format in a dictionary:                                        #
# citation : Paper instance                                                    #
# Where Paper instance may be None. Note that citations are string             #
# representations, which means that they are not unique. Paper instances are   #
# unique, but parsing may fail (leading to the value of None).                 #
#                                                                              #
# This set of functions should be silent; for debugging, set parsers.debugmode #
#                                                                              #
# adding parsers:                                                              #
# each parser should accept file and url input; file input is default and      #
# should be used for testing. A parser shall return a correctly formatted dict #
# and may include URLs (https?://...) or DOIs (doi://...).                     #
#                                                                              #
################################################################################

#HTML Parsing:                 see http://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup as BS
#simple HTTP library:             see http://docs.python-requests.org/en/latest/
import requests

import re

from paper import Paper

debugmode=False

def parse(url, type=None):
  if(type==None):
    print "Type not defined, type guessing not supported (yet?)"
  if(type=="ACM"):
    return parse_acm(url)

def parse_acm(url, file="test_acm.txt"):
  #download the text, or use file for testing.
  txt = None
  if url:
    #use the flat layout to make sure the references are received
    if "preflayout=flat" not in url:
      if "?" not in url:
        url +="?"
      elif not (url.endswith("?") or url.endswith("&")):
        url += "&"
      url+="preflayout=flat"
    resp = requests.get(url)
    txt=resp.text()
  else:
    txt=open(file)
  
  
  #the following parses out a dict of references.
  # references are in a table; a row contains a div of class 'abstract' in the
  # first td, and the actual text description (possibly with linking to the 
  # paper pages, in a variety of formats) in the second td.
  # <tr><td><div class="abstract">number</div></td><td> citation </td>
  soup = BS(txt)

  trs = soup.find_all('tr')
  citations = {}
  for i in trs:
    divs = i.find_all('div')
    if not divs:
      continue
    try:
      if divs[0].has_attr('class') and (divs[0]['class'][0] == 'abstract'):
        ref_url= divs[1].find('a')
        if ref_url:
          ref_url="http://dl.acm.org/" + divs[1].find('a')['href']
        #parse paper metadata. This assumes one of the formats used
        #on the page. It may be separated into a different function
        #later; this will make sense esp. when similar issues are 
        #encountered for other sources.
        #approximate description of the format:
        #name , name , name, title, pubname, [v.volume n.number, ][p.pages-pages, ][month [days], year, ][location]
        ref_name = divs[1].get_text().strip()
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
          citations[ref_name]=Paper(ref_authors, ref_title, ref_year, ref_name)
    except IndexError:
      print "Error parsing " +divs
  return citations

#def parse_ieee(url=...)
#def parse_springer(url=...)

