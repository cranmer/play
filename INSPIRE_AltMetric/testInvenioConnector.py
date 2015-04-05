from invenio_connector import *

def testInvenioConnector():
	cds = InvenioConnector("http://cds.cern.ch")
	results = cds.search("ATLAS+Papers")
	print len(results)

	for record in results:
		for author in record["100__"]:
			print author
	"""
		#print record["245__a"][0]
		#print record["520__b"][0]
		#for author in record["100__"]:
	    # 	print author["a"][0], author["u"][0]
	"""


if __name__ == '__main__':
	testInvenioConnector()