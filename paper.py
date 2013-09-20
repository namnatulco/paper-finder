class Paper():
  authors=[]
  title=""
  year=-1
  journal=""
  proceeding=""
  doi=""
  url=""
  references={}
  other_data=""
  string_rep=""
  
  def __init__(self, authors, title, year, string_rep, journal=None, proceeding=None, doi=None, url=None, references={}, other_data=""):
    self.authors = authors
    self.title = title
    self.year = year
    self.journal = journal
    self.proceeding = proceeding
    self.doi = doi
    self.url = url
    self.references = references
    self.other_data = other_data
    self.string_rep=string_rep
  
  def __str__(self):
    return "Paper with title \"%s\", written by %s in %d. The paper was cited as:\n%s"%(self.title, self.authors, self.year, self.string_rep)
    
  def get_publication_title(self):
    if self.journal:
      return self.journal
    else:
      return self.proceeding
