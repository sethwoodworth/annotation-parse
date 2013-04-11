import json
import os
import bs4
from bs4 import BeautifulSoup
from bs4 import NavigableString
from difflib import SequenceMatcher



class creator:

	def __init__ (self):

		self.tags= ['br']
		self.check = 10709999
		self.special = [90,112,104,29,100,216,302,298,325,379]
		self.specialSec = [2448,2499,2500,2501,2502,2858,9296,9297,2457,2493,2494,2503,2504,2477,10356,10440,14229,14244,14262,14140]
		self.specialSec.append([14338,14360,16062,15959,15960,15961,18246,18219])
		w = open('content.json')
		self.ConJSON = json.load(w)
		w.close()

		sec = open('sections.json')
		self.sectionsJson = json.load(sec)
		sec.close()

		w = open('works.json')
		self.worksJSON = json.load(w)
		w.close()
		


		

		


	def getSectionIdsByWorkId(self,id):
		
		
		
		
		sectionIds = []
		for obj in self.sectionsJson:
			if obj['work_id'] == id:
				sectionIds.append(obj['id'])
				self.secWorkId[obj['id']] = id
				
		sSectionIds = sorted(sectionIds)
		self.workSecId[id] = sSectionIds
		for idx, k in enumerate(sSectionIds):
			self.secSpan[k] = idx
			#print str(k) +' '+str(idx)
		return sSectionIds

	def getNamefromWorkId(self,id):
		
		ids = []
		for obj in self.worksJSON:
			if id == obj['id']:
				return obj['title']

	def getSectionNamefromSecID(self,id):

		for obj in self.sectionsJson:
			if obj['id'] == id:
				return obj['name']

	def strartHTML(self,title):
		return '<html>\n<body title=\'%s\'>\n' %title.replace('\'','')

	def endHTML(self):
		return '\n</body>\n</html>'

	def createTitle(self,name):
		return '<H2> '+name+ '</H2>'

	def makehtml(self,id):
		self.secSpan = {}
		self.workSecId = {}
		self.secWorkId = {}
		ouputString= ''
		self.getSectionIdsByWorkId(id)
		for k,v in self.workSecId.items():
			for i in v:
				s = ""
				for obj in self.ConJSON:
					if obj['section_id'] == i:
						s = obj['content']
						s = s.replace('<br /></p>','</p>')

				if i == self.check:
					print s

				if s is not "":
					mypath = self.getPathFromWorkID(k)
					if not os.path.isdir(mypath):
	   					os.makedirs(mypath)
	   				name = self.getNamefromWorkId(k)+' '+self.getSectionNamefromSecID(i)
					output = open(mypath+name[0:220]+'_'+str(k)+'_'+str(i)+'.html', 'w')
					#output.write('<span id = '+str(i)+ >')
					outputString=self.strartHTML(name)
					#output.write(createTitle(getSectionNamefromSecID(i)))
					outputString+=self.replaceCharacters(s)
					outputString+=self.endHTML()

					if id in self.special or i in self.specialSec:
						output.write(outputString)
						output.close()
					else:
						#print outputString
						soup = BeautifulSoup(outputString)
						#print soup

						######Remove for TEXTUS#########
						soup = self.addptag(soup)
						soup = self.strip_tags(unicode(soup))
						
						if i == self.check:
							print soup
							pass

						soup = self.removeEmptyTags(soup,id)
						if i == self.check:
							print soup
							pass

						if soup.get_text() == "":
							print "Nothing in HTML: %d" %i

						try:
							x = soup.get_text()
							y = BeautifulSoup(outputString).get_text()
							s = SequenceMatcher(lambda x: x==' ',x,y)
							r = float(s.real_quick_ratio())
							dif = len(y)-len(x)
							if dif > 150 and r <.95:
								print 'Ratio %d: %.5f%%' %(i,(float(s.ratio())*100.0))
								print 'Length %d: %d' %(i,len(x)-len(y))

							output.write(soup.prettify(formatter="html"))
						except Exception as inst:
							print 'HTML write Error with: %d' %i
							print inst
							print s
							output.write(outputString)
						output.close()

				#output.write('</span>')

	def replaceCharacters(self,text):
		dict= {'--': '&mdash;'}
		for k,v in dict.iteritems():
			string = text.replace(k, v);
		return string

	def getAuthorFromWorkID(self,id):
		for obj in self.worksJSON:
			if id == obj['id']:
				return obj['author']

	def getPathFromWorkID(self,id):
		title = str(self.getNamefromWorkId(id))
		author = str(self.getAuthorFromWorkID(id))
		return author+'/'+title+'/'

	def addptag(self,soup):
		for child in soup.body.children:
			if type(child) is bs4.element.NavigableString:
				new_tag = soup.new_tag('span')
				new_tag.string = child
				child.replace_with(new_tag)
		return soup

	def strip_tags(self,html):
  		soup = BeautifulSoup(html)
  		for tag in soup.findAll():
   			if tag.name in self.tags:
      				s = ""
      				for c in tag.contents:
        				if not isinstance(c, bs4.element.NavigableString):
          					#c = self.strip_tags(c)
          					pass
        				s += unicode(c)
      				tag.replaceWith(s)
  		return soup

	def removeEmptyTags(self,soup,id):
		if id == 90:
			pass
		else:
			for tag in soup.find_all(lambda tag: tag.name == 'p' and tag.find(True) is None and (tag.string is None or tag.string.strip()=="")):
				#print tag.string
				tag.decompose()
		return soup 

	def sepecialFix(self,html,id):
		if id == 90:
			s = html.replace('<br /><br />','</p>\n<p>')
			return s
		elif id == 112:
			#return html
			pass



