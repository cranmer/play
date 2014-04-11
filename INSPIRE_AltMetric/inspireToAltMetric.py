# Author: Kyle Cranmer <kyle.cranmer@nyu.edu>
# Licence: BSD

"""
Using INSPIRE API to generate widgets for a given author
http://inspirehep.net/help/admin/search-engine-api
ot=24 for DOI
ot=35 for arXiv
ot=37 for arxiv etc.
ot=245 for title
"""
print(__doc__)


import requests
from xml.etree import ElementTree


def getTitleAndDOI(record):
	title,doi = '',''
	for datafield in record.findall(".//{http://www.loc.gov/MARC21/slim}subfield[@code='2']/.."):
		for child in datafield:
			if child.attrib.has_key('code'):
				if child.attrib['code']=='a':
					#print child.tag, child.attrib, child.text
					doi = child.text
	for datafield in record.findall(".//{http://www.loc.gov/MARC21/slim}datafield[@tag='245']/."):
		for child in datafield:
			if child.attrib.has_key('code'):
				if child.attrib['code']=='a':
					#print child.tag, child.attrib, child.text
					title = child.text
	return [title,doi]

def processRecords(collection ):
	return [getTitleAndDOI(record) for record in collection]


def getCollection(authorID='K.S.Cranmer.1'):
	testing=False
	url = 'http://inspirehep.net/search?p=author:%s&of=xm&ot=024,035,245&rg=200' %(authorID)
	tree = ElementTree.parse('example2.xml')
	root = tree.getroot()

	if not testing:
		response = requests.get(url)
		root = ElementTree.fromstring(response.content)
		f = open('example2.xml','w')
		f.write(response.content)
		f.close()
	return root


def makeWidgets(titlesAndDOIs):
	f = open('converted.html','w')
	for title,doi in titlesAndDOIs:
		if doi=='':
			continue
		entry = """
<div class="row">
	<div  class="col-md-4">
		%s
	</div>
	<div  class='col-md-8'> 
		<div class='altmetric-embed' data-badge-type='medium-donut' 
		data-badge-details='right' data-doi='%s'></div>
	</div>
</div>""" %(title,doi)
		f.write(entry.encode('utf-8'))
	f.close()


if __name__ == '__main__':
	makeWidgets(processRecords(getCollection()))
	#fun ones: M.Reece.1, N.Arkani.Hamed.1

