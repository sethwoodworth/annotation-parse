import bs4
from bs4 import BeautifulSoup
import json
import createhtml
import os
import FCUtil
import re
import sys
import math
from threading import Thread
from time import time, localtime, strftime
import difflib


class TextusAnnotation:
	pass


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
		self.id = annDic['id']
		self.section_id = annDic['section_id']
		self.start_index = annDic['start_index']
		self.end_index = annDic['end_index']
		self.deleted = annDic['deleted_on']
		tempQuote = BeautifulSoup(FCUtil.removeSpecChar(annDic['quote']).lstrip().lstrip('\''))
		self.quote = self.fixQuote(tempQuote.get_text())
		self.text = annDic['annotation']

	def __str__(self):
		try:
			return 'ID: '+str(self.id)+'\nSection ID: '+str(self.section_id)+'\nQuote: '+self.quote
		except:
			return 'ID: '+str(self.id)

	def fixQuote(self,string):
		return string.replace("&quot;",'"')

class annlocation:
	def __init__(self,xPath,charOffset):
		self.xPath= xPath
		self.charOffset = charOffset

	def __str__( self ):
		return str(self.xPath)+' '+str(self.charOffset)



class converter:
	def __init__(self,worker):
		self.id = 0
		self.noMatches = 0
		self.worker = worker

		annFile = open('annotations.json')
		self.annJSON = json.load(annFile)
		annFile.close()

		sec = open('sections.json')
		self.sectionsJson = json.load(sec)
		sec.close()

	def convert(self,id):
		self.id = id
		self.noMatches=0
		self.getAnnotation()
		#print "Quote: "+self.annotation.quote

		if "NULL" not in self.annotation.deleted:
			#print "deleted"
			return None

		htmlPath = self.getSectionHtmlPath()

		tagDic = {}
		self.tagList = []
		lenDic = {}
		self.textDic = {}
		wordCount = 0
		prevWordCount = 0
		try:
			file = open(htmlPath,'r')
		except:
			print 'Open Error: '+str(self.id)
		#print "htmlpath "+htmlPath
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
				self.tagList.append(name +'['+str(tagDic[name])+']')
				lenDic[name +'['+str(tagDic[name])+']'] = len(child.get_text())
				self.textDic[name +'['+str(tagDic[name])+']'] = child.get_text()
				wordCount += len(child.get_text().split())

				
				prevWordCount = wordCount
			
			
		self.startIndex = self.searchForStart(self.annotation.quote,self.textDic)
		#print 'Start Location: '+str(self.startIndex)
		#print self.textDic
		#print self.startIndex
		#print self.textDic[self.startIndex.xPath]
		#print 'Completely inside path:' +str(self.completelyInPath())
		if (self.completelyInPath):
			#print "inside one path"
			self.endIndex = [self.startIndex.xPath,self.startIndex.charOffset+len(self.annotation.quote)]
		else:
			print 'not inside one path'

		if self.startIndex.charOffset == -1:
			try:
				print str(self.annotation)
			except:
				print str(self.annotation.id)
		#print tagDic
		#print lenDic
		#results = annotationResult()
		results = ""
		return results


	def searchForStart(self, quote,textDic):
		finalDic = {}

		uWord = self.uniqueWord(quote,textDic)

		if uWord:
			#print "Unique Word"
			return uWord
			
		#print "Quote " + quote
		# for tag, text in textDic.items():
		# 	firstWordQuote = quote.split()[0]
		# 	firstWordQuote = self.escapePar(firstWordQuote)
		# 	startQuoteIndex = [m.start() for m in re.finditer(firstWordQuote, text)]

		# 	if len(startQuoteIndex) > 0:
		# 		finalDic[tag] = startQuoteIndex[0]
				
		# if len(finalDic) == 1:
		# 	print 'winner'
		# 	key,value = finalDic.popitem()
		# 	return annlocation(key,value)

		finalDic = {}
		for tag,text in textDic.items():
			quote = self.escapePar(quote)
			try:
				quoteIndex = [m.start() for m in re.finditer(quote, text,re.IGNORECASE)]
			except:
				print quote
			if quoteIndex:
				finalDic[tag] = quoteIndex

		if len(finalDic) >0 :
			#print 'winner better'
			matcheslist = []
			for key,values in finalDic.items():
				for v in values:
					matcheslist.append(annlocation(key,v))
			return self.closestToWordCount(matcheslist)

		finalDic = {}
		for tag,text in textDic.items():
			check = ''
			for i in quote.split():
				try:
					check +=i+' '
				except:
					#print type(check)
					#print type(i)
					check+=str(i).encode('ascii','ignore')+' '
				try:
					tempA = [m.start() for m in re.finditer(check, text,re.IGNORECASE)]
					#print check
					#print tempA
					if len(tempA) == 1:
						#print 'should delete'
						finalDic[tag] = [tempA[0],len(check)]
						
					#elif len(tempA) == 0:
						#finalDic[tag] = None
						
				except:
					pass
		#print finalDic
		#print 'not great'
		bestMatch =  self.bestMatch(finalDic)
		if bestMatch:
			return bestMatch
		else:
			#print 'no match'
			self.noMatches+=1
			return annlocation('p[1]',-1)

	def uniqueWord(self,quote,textDic):
		splitQutoe = quote.split()
		#print splitQutoe
		#print textDic
		tempDic = {}
		length = 0
		for word in splitQutoe:
			word = self.escapePar(word)
			for tag,text in textDic.items():
				wordIndex = [m.start() for m in re.finditer(word, text,re.IGNORECASE)]
				#print wordIndex
				if len(wordIndex) == 1:
					tempDic[tag]=wordIndex[0]-length
			if len(tempDic) == 1:
				key,value = tempDic.popitem()
				return annlocation(key,value)
			length+=len(word)+1
		return None


	def bestMatch(self,matchDic):
		if 	not matchDic:
			return None
		matchLength = -1
		matchPath = ''
		matchOffset = -1
		matches = []
		for tag,matchArray in matchDic.items():
			if matchArray[1] > matchLength:
				matchLength = matchArray[1]
				matchOffset = matchArray[0]
				matchPath = tag
		problems = 0
		for tag,matchArray in matchDic.items():
			if matchArray[1] == matchLength:
				matches.append(annlocation(tag,matchArray[0]))
		if len(matches) > 1:
			return self.closestToWordCount(matches)
		return annlocation(matchPath,matchOffset)

	def closestToWordCount(self,locList):
		wCount = self.annotation.start_index
		bestDelta = sys.maxint
		for loc in locList:
			if int(math.fabs(self.getWordCount(loc)-wCount)) < bestDelta:
				bestDelta = int(math.fabs(self.getWordCount(loc)-wCount))
				bestLoc = loc
		return bestLoc

	def getWordCount(self,location):
		count = 0
		for tag in self.tagList:
			if tag == location.xPath:
				return len(self.textDic[tag][0:location.charOffset].split())
			else:
				count += len(self.textDic[tag].split())


	def completelyInPath(self):
		#print self.startIndex
		if((len(self.annotation.quote)+self.startIndex.charOffset) <= len(self.textDic[self.startIndex.xPath])+5):
			return True
		else:
			#print 'Quote: '+self.annotation.quote
			#print len(self.annotation.quote)+self.startIndex.charOffset
			#print len(self.textDic[self.startIndex.xPath])
			return False




		


	def getAnnotation(self):
		
		for obj in self.annJSON:
			if obj['id'] == self.id:
				self.annotation = annotation(obj)
				return obj

	def getWorkId(self):
		

		for obj in self.sectionsJson:
			if self.annotation.section_id==obj['id']:
				return obj['work_id']

	def getSectionPath(self):
		return self.worker.getPathFromWorkID(self.getWorkId())

	def getSectionHtmlPath(self):
		folder = self.getSectionPath()
		dirList=os.listdir(folder)
		for fname in dirList:
			try:
				fSectionId = int(fname.rsplit('.',1)[-2].rsplit('_',1)[-1])
				if fSectionId == self.annotation.section_id:
					return folder+fname
			except:
				print 'failed'+fname
				pass
		print 'problem: '+str(self.annotation.section_id)

	

	def escapePar(self,string):
		string = string.replace('\(','(').replace('\)',')')
		return string.replace('(','\(').replace(')','\)')
			






if __name__ == '__main__':
	
	#	annotationsbyworkid[wid]=FCUtil.getAllAnnotationsforWork(wid)


	#print annotationsbyworkid
	#works = FCUtil.getAllWorksExcluding(['William Shakespeare'])
	#112 1 problem do it by hand

	complete = [10,12,8,9,11,195,15,17,23,25,26,40,29,30,31,32,33,86,36,37,317,41,42,43,44,46,47,48,49,50,51,]
	complete.extend(range(52,58))
	complete.extend(range(61,66))
	complete.extend(range(71,81))
	complete.extend([199,82,83,90,59,67,84,85,87,88,91,92,93,94,95,97,99,100,103,104,105,106])
	complete.extend([108,112,113])
	#for i in complete:
	#	works.remove(i)

	#print works

	def crunch(worker,conv,workId):
		
		
		list = FCUtil.getAllAnnotationsforWork(workId)
		total = 0;
		badMatches = 0
		#print 'this is the list '+str(list)
		#print "Total: %d"%len(list)
		
		et = time()
		st = time()
		for num in list:
			
			
			print "Annotation on: %d %0.2f%% Last one took: %.1f "%(num,(float((total+1))/float(len(list))*100.0),et-st)
			st = time()
			#conv.convert(num)
			total += 1
			et = time()
		badMatches += conv.noMatches

		if badMatches != 0 and total !=0:
			p = (float(badMatches)/float(total))*100.0
			print "No matches for %d : %4.2f" %(workId, p)
		print "No Matches for "+str(workId)+' : '+str(badMatches)
		print "Total for "+str(workId)+' : '+str(total)


	#workNumber = 112
	#print "Work: %d\n" %workNumber
	#crunch(workNumber)

	#annNumber = 1762
	#print 'Annotation: %d\n'%annNumber
	#conv = converter()
	#conv.convert(annNumber)

	works = FCUtil.getAllWorksExcluding(['William Shakespeare'])
	#works = [61]
	totalWorks = len(works)
	annotationsbyworkid = {}
	count = 0
	
	worker = createhtml.creator()
	conv= converter(worker)
	for wid in works:
		try:
			print '\nCurrently on Work %d %00.2f%%' %(wid,((float(count)/float(totalWorks)))*100.0)
		except:
			print '\nCurrently on Work %d' &wid
		worker.makehtml(wid)
		#crunch(worker,conv,wid)
		count+=1



	#for workId in works:
		#crunch(workId)
		#pass

		
	



