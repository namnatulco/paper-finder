import parsers, time
res = parsers.parse(parsers.ACM)
print res
if not res:
  print "FAIL"
else:
  for (ref, paper) in res.iteritems():
    if paper.url:
      print "parsing: %s via %s"%(ref, paper.url)
      paper.references=parsers.parse(parsers.ACM, paper.url)
      time.sleep(5)
      break
