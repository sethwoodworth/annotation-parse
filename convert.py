import bs4
from bs4 import BeautifulSoup
import json
import create_html_by_sections
import os
import FCUtil
import re




class annotationResult:
	def __init__(self,startXpath,startOffset,endXpath,endOffset):
		self.startXpath = startXpath
		self.startOffset = startOffset
		self.endXpath = endOffset
		self.endOffset = endOffset

class annotation:
	def __init__(self,id,section_id,start_index,end_index,deleted,quote,text):
		self.id = id
		self.section_id = section_id
		self.start_index = start_index
		self.end_index = end_index
		self.deleted = deleted
		self.quote = quote
		self.text = text

	def __init__(self,annDic):
		self.dic = annDic
		self.section_id = annDic['section_id']
		self.start_index = annDic['start_index']
		self.end_index = annDic['end_index']
		self.deleted = annDic['deleted_on']
		tempQuote = BeautifulSoup(FCUtil.removeSpecChar(annDic['quote']).lstrip().lstrip('\''))
		self.quote = tempQuote.get_text()
		self.text = annDic['annotation']



class converter:
	def __init__(self):
		self.id = 0

	def convert(self,id):
		self.id = id
		self.getAnnotation()
		print self.annotation.dic

		if "NULL" not in self.annotation.deleted:
			print "deleted"
			return None

		htmlPath = self.getSectionHtmlPath()

		tagDic = {}
		lenDic = {}
		self.textDic = {}
		wordCount = 0
		prevWordCount = 0
		file = open(htmlPath,'r')
		soup = BeautifulSoup(file)
		#soup.body.h2.extract() #romve title that I added
		for child in soup.body.children:

			name = None
			if type(child) is bs4.element.Tag:
				name = child.name #get tag type can count how many if its in it !!!!!
			
			if name is not None:
				try:
					tagDic[name]+=1
				except:
					tagDic[name] = 1
				lenDic[name +'['+str(tagDic[name])+']'] = len(child.get_text())
				self.textDic[name +'['+str(tagDic[name])+']'] = child.get_text()
				wordCount += len(child.get_text().split())

				
				prevWordCount = wordCount
			
			
		self.startIndex = self.searchForStart(self.annotation.quote,self.textDic)

		print self.startIndex
		print self.textDic[self.startIndex[0]]
		print 'Completely inside path:' +str(self.completelyInPath())
		print tagDic
		print lenDic
		#results = annotationResult()
		results = ""
		return results

	def searchForStart(self, quote,textDic):
		finalDic = {}
		print "Quote " + quote
		for tag, text in textDic.items():
			firstWordQuote = quote.split()[0]
			startQuoteIndex = [m.start() for m in re.finditer(firstWordQuote, text)]
			

			if len(startQuoteIndex) == 1:
				finalDic[tag] = startQuoteIndex[0]
				

		if len(finalDic) == 1:
			print 'winner'
			key,value = finalDic.popitem()
			return [key,value]

		finalDic = {}
		for tag,text in textDic.items():
			quoteIndex = [m.start() for m in re.finditer(quote, text)]
			if len(quoteIndex) == 1:
				finalDic[tag] = quoteIndex[0]

		if len(finalDic) == 1:
			print 'winner better'
			key,value = finalDic.popitem()
			return [key,value]

		finalDic = {}
		for tag,text in textDic.items():
			check = ''
			for i in quote.split():
				check +=str(str(i)+' ')
				try:
					tempA = [m.start() for m in re.finditer(check, text)]
					#print check
					#print tempA
					if len(tempA) == 1:
						#print 'should delete'
						finalDic[tag] = [tempA[0],len(check)]
						
					#elif len(tempA) == 0:
						#finalDic[tag] = None
						
				except:
					pass
		print finalDic
		print 'not great'
		return self.bestMatch(finalDic)

	def bestMatch(self,matchDic):
		matchLength = 0
		matchPath = ''
		matchOffset = 0
		for tag,matchArray in matchDic.items():
			if matchArray[1] > matchLength:
				matchLength = matchArray[1]
				matchOffset = matchArray[0]
				matchPath = tag
		problems = 0
		for tag,matchArray in matchDic.items():
			if matchArray[1] == matchLength:
				problems += 1
		if problems > 1:
			print 'too many matches need to pick one'
		return [matchPath,matchOffset]

	def completelyInPath(self):
		print self.startIndex
		if((len(self.annotation.quote)+self.startIndex[1]) <= len(self.textDic[self.startIndex[0]])+5):
			return True
		else:
			print 'Quote: '+self.annotation.quote
			print ((len(self.annotation.quote)+self.startIndex[1]))
			print len(self.textDic[self.startIndex[0]])
			return False




		


	def getAnnotation(self):
		annFile = open('annotations.json')
		annJSON = json.load(annFile)
		annFile.close()
		for obj in annJSON:
			if obj['id'] == self.id:
				self.annotation = annotation(obj)
				return obj

	def getWorkId(self):
		sec = open('sections.json')
		sectionsJson = json.load(sec)
		sec.close()

		for obj in sectionsJson:
			if self.annotation.section_id==obj['id']:
				return obj['work_id']

	def getSectionPath(self):
		return create_html_by_sections.getPathFromWorkID(self.getWorkId())

	def getSectionHtmlPath(self):
		folder = self.getSectionPath()
		dirList=os.listdir(folder)
		for fname in dirList:
   			 fSectionId = int(fname.split('.')[0].split('_')[-1])
   			 if fSectionId == self.annotation.section_id:
   			 	return folder+fname






if __name__ == '__main__':
	conv = converter()
	list = [3381,3382,3383,3384,3385,3386,3387,3388,3389,3390,3391,3392,3393,3394]
	for num in list:
		conv.convert(num)


