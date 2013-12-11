import time
from parser import Parser
from parser_acm_refs import ACM_References_Parser

parser = Parser(file="test_acm.txt")
parser.debugmode=True
print parser.debugmode
parser.read()
res = parser.process()

#res = parsers.parse(parsers.ACM)
if not res or not res.references:
  print "FAIL"
else:
  print res.references
  for (ref, paper) in res.references.iteritems():
    if paper.url:
      print "parsing: %s via %s"%(ref, paper.url)
      paper.references=parsers.parse(parsers.ACM, paper.url)
      time.sleep(5)
      break
