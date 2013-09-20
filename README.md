Here's a project. The goal is to parse references from web resources and 
figure out all the relevant references on a specific topic, eventually.
Current state is getting the data from ACM DL pages into something more sane.
This means parsing their flat HTML references tables, which are OCRd from the 
PDFs. As the formatting is quite inconsistent, this is the first goal to get 
working.

Dependencies:
* Developed on Python 2.7.3.
* PIP resources:
  * BeautifulSoup HTML parsing library.
  * requests HTTP library.


 Further steps include:
* finding associated DOIs.
* rate limiting (to avoid flooding the ACM servers with many requests)
* a useful visualization, probably in graph form.
* filtering of which papers are included
* duplicate resolution

Also useful may be:
* storage in a database
* other data sources (IEEE Xplore, SpringerLink)
* ability to handle PDFs directly (libpoppler may help here...)
* secondary data sources (DBLP, Mendeley, Zotero, scopus, ...)
* filter by availability
* filter by publication type (Workshop, Conference, Journal, ...)
* find related papers through authors or same publication platform
