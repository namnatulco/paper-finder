import time
from parserACMRefs import ACMReferencesParser

parser = ACMReferencesParser(myFile="test_acm.txt")
parser.read(fileToMemory=True)
res = parser.process()
resultList=[]

#res = parsers.parse(parsers.ACM)
if not res or not res.references:
  print "FAIL"
else:
  print res.references
  for (ref, paper) in res.references.iteritems():
    if paper.url:
      print "parsing: %s via %s"%(ref, paper.url)
      itemparser = ACMReferencesParser(uri=paper.url)
      try:
        itemparser.read()
      except:
        print "Error reading URL:",paper.url
        continue
      try:
        tehresult = itemparser.process()
        if tehresult:
          resultList.append(tehresult)
      except:
        print "failed, ignoring",ref
      time.sleep(1)
