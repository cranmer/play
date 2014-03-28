"""
Using INSPIRE API
http://inspirehep.net/help/admin/search-engine-api
ot=24 for DOI
ot=35 for arXiv
ot=37 for arxiv etc.
ot=245 for title
"""

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
	testing=True
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
	#makeWidgets(getListOfDOIs())
	makeWidgets(processRecords(getCollection()))


"""
http://inspirehep.net/search?p=author:K.S.Cranmer.1&of=xm&ot=024,035&rg=200

<record>
<controlfield tag="001">1285866</controlfield>
<datafield tag="024" ind1="7" ind2=" ">
<subfield code="2">DOI</subfield>
<subfield code="a">10.1088/1742-6596/490/1/012229</subfield>
</datafield>
<datafield tag="035" ind1=" " ind2=" ">
<subfield code="9">INSPIRETeX</subfield>
<subfield code="a">Gumpert:2014kea</subfield>
</datafield>
</record>
<record>
<controlfield tag="001">1286622</controlfield>
<datafield tag="035" ind1=" " ind2=" ">
<subfield code="9">INSPIRETeX</subfield>
<subfield code="a">Aad:2014mha</subfield>
</datafield>
<datafield tag="035" ind1=" " ind2=" ">
<subfield code="9">arXiv</subfield>
<subfield code="a">oai:arXiv.org:1403.5222</subfield>
</datafield>
</record>
"""