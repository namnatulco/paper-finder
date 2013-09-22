import functools

# Known filters
TITLE=2
AUTHOR=3
YEAR=4
YEARRANGE=5


def titleFilter(expr, title, caseSensitive=False, moreExpr=[]):
  if caseSensitive:
    return expr in title and filter(lambda x: x in title, moreExpr)
  else:
    return expr.lower() in title.lower() and filter(lambda x: x.lower() in title.lower(), moreExpr)

def authorsFilter(expr, authors, partialMatching=False, moreExpr=[]):
  if partialMatching:
    return filter(lambda author: expr.lower() in author.lower() or filter(lambda x: x.lower() in author.lower(), moreExpr), authors)
  else:
    return expr.lower() in [author.lower() for author in authors] or filter(lambda x: x.lower() in [author.lower() for author in authors], moreExpr)

def yearFilter(expr, year, yearEnd=None):
  if yearEnd: #range filter
    return expr <= year and year <= yearEnd
  else:
    return expr==year

# return an arbitrary filter (i.e., a function), which takes exactly one 
# argument, and which will return True iff the argument matches the filter.
# Please note:
#   some filters require more inputs; these MUST be specified.
#   some filters have optional arguments, which may be (re)defined.
#    a filter with one argument of each type can be fully configured as:
#    >>>f=getFilter(type, expr, expr0=..)
#    >>>import functools
#    >>>myfilter=functools.parial(f(opt0=...))

def getFilter(type, expr, expr0=None, expr1=None):
  if type==TITLE:
    return functools.partial(titleFilter(expr))
  elif type==AUTHOR:
    return functools.partial(authorFilter(expr))
  elif type=YEAR:
    return functools.partial(yearFilter(expr))
  elif type=YEARRANGE:
    if expr0:
      if expr<expr0:
        return functools.partial(yearFilter(expr, yearEnd=expr0))
      else:
        return functools.partial(yearFilter(expr0, yearEnd=expr))
    else:
      return None
  else:
    return None
