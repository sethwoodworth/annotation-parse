import FCUtil
import json
import pprint
import re
import math

annFile = open('annotations.json')
AnnJSON = json.load(annFile)
annFile.close()
	
w = open('content.json')
ConJSON = json.load(w)
w.close()

secSpan = {}
secWorkId = {}
workSecId = {}

def getWorkIds(auth):
	w = open('works.json')
	j = json.load(w)
	w.close()
	ids = []
	for obj in j:
		if auth in obj['author']:
			ids.append(obj['id'])
	
	#print ids
	return ids
	w.close()
	#print(j)
	
def getSectionIdsByWorkId(id):
	sec = open('sections.json')
	s = json.load(sec)
	sec.close()
	
	
	
	sectionIds = []
	for obj in s:
		if obj['work_id'] == id:
			sectionIds.append(obj['id'])
			secWorkId[obj['id']] = id
			
	sSectionIds = sorted(sectionIds)
	workSecId[id] = sSectionIds
	for idx, k in enumerate(sSectionIds):
		secSpan[k] = idx
		#print str(k) +' '+str(idx)
	return sSectionIds

def getContentBySectionId(id):
	
	for obj in ConJSON:
		if int(obj['section_id']) == id:
			return obj['content']
			
def getStartOffsetFromAnnId(id):
	
	for obj in AnnJSON:
		if obj['id'] == id:
			wordIndex = obj['start_index']
			Oquote = obj['quote']
			content = getContentBySectionId(obj['section_id'])
			quote = FCUtil.strip_html(FCUtil.remove_html_tags(FCUtil.cleanStr(Oquote)))
			quote = re.sub('\s*(/)\s*',' ',quote).strip()
			endQuote = quote.split()[0]
			if	"'" in quote[:1]:
				quote = quote[1:]
			startQuote = quote.split()[0]
			
			#print "quote " + quote
			
			cw = FCUtil.strip_html(FCUtil.remove_html_tags(content))
			cnw = FCUtil.strip_html(content)
			c = cw.split()
			#print cnw
			#print len(c)
			#print 'startWordINdex: '+str(wordIndex)
			
			startQuoteIndex = [m.start() for m in re.finditer(startQuote.replace('[','\[').replace(']','\]'), cnw)] 
			quoteIndex = [m.start() for m in re.finditer(quote, cnw)]
			
			#print 'StartQuoteIndex for: '+startQuote
			#print startQuoteIndex
			
			
			if len( startQuoteIndex) == 1:
				#print 'via Start Quote'
				return [startQuoteIndex[0],1]
			elif len(quoteIndex) == 1:
				#print 'via entire Quote'
				return [quoteIndex[0],1]
			elif len(quoteIndex) == 0:
				sQuote = quote.split()
				print sQuote
				for i in sQuote:
					try:
						tempA = [m.start() for m in re.finditer(i, cnw)]
						if len(tempA) == 1:
							#print 'new way to town'
							return [tempA[0]-len(quote.split(i,1)[0]),1]
					except:
						pass
			else:
				sQuote = quote.split()
				check = ''
				for i in sQuote:
					check +=str(str(i)+' ')
					try:
						tempA = [m.start() for m in re.finditer(check, cnw)]
						if len(tempA) == 1:
							#print 'should delete'
							return [tempA[0],1]
					except:
						pass
						
			if len(quoteIndex) > 1:  #some how get word count to 
				print quoteIndex
			
			startLoc = []
			for idx, k in enumerate(c):
				if 	startQuote in k:
					startLoc.append(idx)
			#print startLoc
			
			place = 0
			m = 10000
			www = 0
			for idx,k in enumerate(startLoc):
				if(m > abs(k-wordIndex)):
					m = abs(k-wordIndex)
					place = idx
			#print "startIndex: "+str(place)
			#print "StartWordIndex: "+str(wordIndex)
			#print len(cnw.rsplit(startQuote,len(startLoc)-place)[0])
			if(len(startLoc) > 0):
				#return len(cnw.split(startQuote,len(startLoc)-place-1)[0])
				return [startQuoteIndex[place],len(startQuoteIndex),len(quote)]
			
			print 'START_ERROR'
			return None

def getEndOffsetFromAnnId(id):
	
	for obj in AnnJSON:
		if obj['id'] == id:
			wordIndex = obj['end_index']
			Oquote = obj['quote']
			quote = FCUtil.strip_html(FCUtil.remove_html_tags(FCUtil.cleanStr(Oquote)))
			quote = re.sub('\s*(/)\s*','',quote).strip()
			endQuote = quote.rsplit()[-1]
			if	"'" in quote[:1]:
				quote = quote[1:]
				
			#print "quote " + quote
			
		
			content = getContentBySectionId(obj['section_id'])
			cw = FCUtil.strip_html(FCUtil.remove_html_tags(content))
			#possible use of beautifulsoup
			cnw = FCUtil.strip_html(content)
			c = cw.split()
			#print c
			endQuoteIndex = [m.start() for m in re.finditer(endQuote.replace('[','\[').replace(']','\]'), cnw)] 
			quoteIndex = [m.start() for m in re.finditer(quote, cnw)]
			
			#print 'Quote: '+quote
			#print 'Content: '+cnw
			#print 'EndQuoteIndex for: '+endQuote
			#print endQuoteIndex
			
			if len( endQuoteIndex) == 1:
				return [endQuoteIndex[0]+len(endQuote),1,len(quote)]
			elif len(quoteIndex) == 1:
				return [len(quote)+quoteIndex[0],1,len(quote)]
			elif len(quoteIndex) == 0:
				sQuote = quote.split()
				for i in sQuote:
					try:
						tempA = [m.start() for m in re.finditer(i, cnw)]
						if len(tempA) == 1:
							#print 'new way to town'
							return [tempA[0]+len(quote.split(i,1)[1]),1,len(quote)]
					except:
						pass
			else:
				sQuote = quote.split()
				check = ''
				for i in sQuote:
					check +=str(str(i)+' ')
					try:
						tempA = [m.start() for m in re.finditer(check, cnw)]
						if len(tempA) == 1:
							return [len(quote)+tempA[0],1,len(quote)]
					except:
						pass
			
			endLoc = []
			for idx, k in enumerate(c):
				if 	endQuote in k:
					endLoc.append(idx)
			#print endLoc
			
			place = 0
			m = 10000
			for idx,k in enumerate(endLoc):
				if(m > abs(k-wordIndex)):
					m = abs(k-wordIndex)
					place = idx
			#print "index "+str(place)
			#print len(cnw.rsplit(endQuote,len(endLoc)-place)[0])+len(endQuote)
			#print "EndWordIndex: "+str(wordIndex)
			#print "EndIndex: "+str(place)
			if len(endLoc) >0:
				#return len(cnw.rsplit(endQuote,len(endLoc)-place)[0])+len(endQuote)
				return [endQuoteIndex[place]+len(endQuote),len(endQuoteIndex),len(quote)]
			
			print 'END_ERROR'
			return None

def getNamefromWorkId(id):
	w = open('works.json')
	j = json.load(w)
	w.close()
	ids = []
	for obj in j:
		if id == obj['id']:
			return obj['title']

def createHtml():
	workSecId
	
	for k,v in workSecId.items():
		output = open(getNamefromWorkId(k)+' '+str(k)+'.html', 'w')
		print v
		for i in v:
			output.write('<span id = '+str(i)+' >')
			for obj in ConJSON:
				if obj['section_id'] == i:
					output.write(obj['content'])
			output.write('</span>')
		output.close()
	
def formatDate(date):
	date = date.split()
	return date[0]+'T'+date[1]
	
def translateCertainAuthor(author):
	output = open(str(author)+'.json', 'w')
	
	sections = set()
	workIds = getWorkIds(author)
	print len(workIds)
	for wo in workIds:
		tempWo = getSectionIdsByWorkId(wo)
		for sect in  tempWo:
			sections.add(sect)
			

	#print sections
	firstTime = True
	output.write("[")
	counter =0
	for obj in AnnJSON:
		if 'NULL' in obj['deleted_on'] and obj['section_id'] in sections:
			if not firstTime:
				output.write (str(','))
			firstTime = False
			dic = {}
			id = obj['id']
			#print id
			
			so = getStartOffsetFromAnnId(id)
			try:
				eo = getEndOffsetFromAnnId(id)
			except:
				print "HELP"
			
			diff = int(eo[0])-int( so[0])
			if diff > len(obj['quote']) or diff<0:
				#print 'Length Error'
				#print str(so[0] ) + ' - '+str(eo[0] ) +' = '+str(diff)
				#print 'actual: '+str(len(obj['quote']))
				if eo[1] < so[1]:
					#print 'End Wins'
					so[0] = eo[0]-eo[2]
				else :
					#print 'Start Wins'
					eo[0] = so[0]+eo[2]
				#print 'new: ' +str(so[0] ) + ' - '+str(eo[0] ) +' = '+str(int(eo[0])-int( so[0]))
				#print obj['quote']
			span = secSpan[obj['section_id']]
			workId = secWorkId[obj['section_id']]
			dic['id'] = obj['id']
			dic['annotator_schema_version'] = 'v1.0'
			dic['created'] = formatDate(obj['created_on'])
			dic['updated'] = None
			dic['text'] = obj['annotation']
			dic['quote'] = obj['quote']
			dic['uri'] = str(getNamefromWorkId(workId)+' '+str(workId)+'.html')
			dic['ranges'] = {'start': '/span['+str(span+1)+']', 'end': '/span['+str(span+2)+']', 'startOffset': so[0]  ,'endOffset': eo[0] }
			dic['user'] = obj['user_id']
			dic['consumer'] = None
			dic['tags'] = None
			dic['permissions'] = {'read': None,'admin':None,'update':None,'delete':None}
			counter +=1
			output.write(str(json.dumps(dic)))
			print json.dumps(dic, sort_keys=True, indent=4)
		
	output.write("]")
	output.close()
	print counter
	
workIds = getWorkIds('William Shakespeare')

sec = getSectionIdsByWorkId(4)
#print sec
#for s in sec:
	#content = getContentBySectionId(s)
	#content = FCUtil.c
	#print FCUtil.strip_html(content)
#content = getContentBySectionId(75)
#print content
#print FCUtil.strip_html(FCUtil.remove_html_tags(content))

#print getEndOffsetFromAnnId(11)
translateCertainAuthor('Henry James')
print secSpan
print ''
print secWorkId
print ''
print 'creating HTML...'
createHtml()
#print FCUtil.remove_html_tags(content)
