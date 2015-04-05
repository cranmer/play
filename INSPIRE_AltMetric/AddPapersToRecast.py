# Author: Kyle Cranmer <kyle.cranmer@nyu.edu>
# Licence: BSD

"""
Using INSPIRE API to generate widgets for a given author
http://inspirehep.net/help/admin/search-engine-api
ot=24 for DOI
ot=35 for arXiv
ot=37 for arxiv etc.

ot=088 for arxiv
ot=856 for arxiv URL 
ot=245 for title
ot=520 for abstract
"""
print(__doc__)


import requests
from xml.etree import ElementTree
import json
from collections import OrderedDict


RECAST_USERNAME='cranmer'
def getTitleAndDOI(record):
	title,doi, abstract, arxivURL, lumi, energy = '','', '', '', '', ''
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
	for datafield in record.findall(".//{http://www.loc.gov/MARC21/slim}datafield[@tag='520']/."):
		for child in datafield:
			if child.attrib.has_key('code'):
				if child.attrib['code']=='a':
					#print child.tag, child.attrib, child.text
					abstract = child.text
					words = abstract.split()

					energyLoc = abstract.find('TeV')
					lumiLoc = abstract.find('fb')

					#this is fragile, could get mass of a particle
					if energyLoc>0:
						energy=abstract[energyLoc-2:energyLoc+3]

					#somewhat rediculous code for grabbing lumi string from different
					#conventions in the abstract
					if lumiLoc>0:
						temp=abstract[lumiLoc-10:lumiLoc+10]
						words = temp.split()
						for i, w in enumerate(words):
							if w.find('fb')==0: # eg: 4.8 fb$^{-1}$.
								lumi=words[i-1]+' '+w
								break
							if w.find('fb')>0: #eg: 4.8/fb
								lumi=w
								break
					if lumi[-1:]=='.': lumi=lumi[:-1]

	for datafield in record.findall(".//{http://www.loc.gov/MARC21/slim}datafield[@tag='856']/."):
		for child in datafield:
			if child.attrib.has_key('code'):
				if child.attrib['code']=='u':
					#print child.tag, child.attrib, child.text
					if child.text.find('arxiv.org')>0:
						arxivURL = child.text
	return {'title':title,'doi':doi, 'abstract':abstract, \
			'arxivURL':arxivURL, 'lumi':lumi, 'energy':energy}

def processRecords(collection ):
	return [getTitleAndDOI(record) for record in collection]


def getCollection():
	testing=True
	url = 'http://cds.cern.ch/search?&of=xm&ot=024,035,245,520,856&rg=200&cc=ATLAS+Papers&sc=1'
	tree = ElementTree.parse('atlasPapers.xml')
	root = tree.getroot()

	if not testing:
		response = requests.get(url)
		root = ElementTree.fromstring(response.content)
		f = open('atlasPapers.xml','w')
		f.write(response.content)
		f.close()
	return root

def printRecords(extractedContent):
	for i in extractedContent:
		print ''
		for r in i.iteritems():
			print r

def addRecord(rec):
	recast_url = "http://recast.perimeterinstitute.ca/dev/api/recast-analysis"
	payload=OrderedDict([ \
		('username',RECAST_USERNAME), \
		('title',rec['title']), \
		('collaboration','Atlas'), \
		('e_print',rec['arxivURL']), \
		('journal',''), \
		('doi',rec['doi']), \
		('inspire_url',rec['arxivURL']), \
		('description',rec['abstract']) \
		])
	print payload
	r = requests.post(recast_url, data=payload)
	print 'response said'
	print r
	print r.text
	uuid=r.text.split()[-1]
	print 'the uuid=',uuid

	#add the analysis & uuid to a recently added file
	f = open('recentlyAdded','a')
	alreadyAdded = f.write(uuid+' '+rec['title']+'\n')
	f.close()

	#add a run-condition to the analysis
	payload=OrderedDict([ 
		('username',RECAST_USERNAME),
		('name',rec['energy']),
		('description',rec['lumi']+' at '+rec['energy'])
		])
	recast_url = "http://recast.perimeterinstitute.ca/dev/api/recast-analysis/"+uuid+'/add-run-condition'
	print recast_url
	r = requests.post(recast_url, data=payload)
	print r

	return


def addRecords(extractedContent):
	f = open('alreadyAdded','r')
	alreadyAdded = f.readlines()
	f.close()
	for i in extractedContent:
		print i['title']

		if alreadyAdded.count(i['arxivURL']+'\n')>0:
			print 'paper already added, skipping'
			continue

		print 'add record (y/n)'
		answer=raw_input()
		if answer=='y':
			print 'ok'
			addRecord(i)




def testSubscription():
	recast_url = "http://recast.perimeterinstitute.ca/api/recast-subscription"
	payload=OrderedDict([ \
		('analysis-uuid','009bdb8a-90da-4bf4-4d52-48fcdeed68e2'), \
		('username',RECAST_USERNAME), \
		('subscription-type','observer'), \
		('requirements','none'), \
		('notifications','recast_requests') \
		])
	print payload
	r = requests.post(recast_url, data=payload)
	print 'response said'
	print r
	print r.text
	return

if __name__ == '__main__':
	testSubscription()
	addRecords(processRecords(getCollection()))
	#fun ones: M.Reece.1, N.Arkani.Hamed.1

