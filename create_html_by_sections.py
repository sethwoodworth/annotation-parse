import json
import os


w = open('content.json')
ConJSON = json.load(w)
w.close()

sec = open('sections.json')
sectionsJson = json.load(sec)
sec.close()

w = open('works.json')
worksJSON = json.load(w)
w.close()

secSpan = {}
workSecId = {}
secWorkId = {}


def getSectionIdsByWorkId(id):
	
	
	
	
	sectionIds = []
	for obj in sectionsJson:
		if obj['work_id'] == id:
			sectionIds.append(obj['id'])
			secWorkId[obj['id']] = id
			
	sSectionIds = sorted(sectionIds)
	workSecId[id] = sSectionIds
	for idx, k in enumerate(sSectionIds):
		secSpan[k] = idx
		#print str(k) +' '+str(idx)
	return sSectionIds

def getNamefromWorkId(id):
	
	ids = []
	for obj in worksJSON:
		if id == obj['id']:
			return obj['title']

def getSectionNamefromSecID(id):

	for obj in sectionsJson:
		if obj['id'] == id:
			return obj['name']

def strartHTML():
	return '<html>\n<body>\n'

def endHTML():
	return '</body>\n</html>'

def createTitle(name):
	return '<H2> '+name+ '</H2>'

def createHtml():
	for k,v in workSecId.items():
		for i in v:
			s = ""
			for obj in ConJSON:
				if obj['section_id'] == i:
					s = obj['content']

			if s is not "":
				mypath = getPathFromWorkID(k)
				if not os.path.isdir(mypath):
   					os.makedirs(mypath)
				output = open(mypath+getNamefromWorkId(k)+' '+getSectionNamefromSecID(i)+'_'+str(k)+'_'+str(i)+'.html', 'w')
				#output.write('<span id = '+str(i)+' >')
				output.write(strartHTML())
				#output.write(createTitle(getSectionNamefromSecID(i)))
				output.write(replaceCharacters(s))
				output.write(endHTML())
				output.close()

			#output.write('</span>')

def replaceCharacters(text):
	dict= {'--': '&mdash;'}
	for k,v in dict.iteritems():
		string = text.replace(k, v);
	return string

def getAuthorFromWorkID(id):
	for obj in worksJSON:
		if id == obj['id']:
			return obj['author']

def getPathFromWorkID(id):
	title = str(getNamefromWorkId(id))
	author = str(getAuthorFromWorkID(id))
	return author+'/'+title+'/'


			


if __name__ == '__main__':
	getSectionIdsByWorkId(10)
	createHtml()
	print getAuthorFromWorkID(10)


