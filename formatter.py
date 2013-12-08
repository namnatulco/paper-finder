def formatter_txt(authorList, title, year, publication, doi, url, referenceDict):
  res = "Paper \"%s\", written by %s, was published in %s in %s; it can be found under %s or %s. It has cited the following articles:\n"%(title, authorList, publication, year, doi, url)
  for pair in referenceDict:
    res+="%s, %s"%(pair, referenceDict[pair])
  return res
