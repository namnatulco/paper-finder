import parsers
res = parsers.parse_acm(None)
print res
if not res:
  print "FAIL"
else:
  for text in res.keys():
    print text
  for link in res.values():
    print link
