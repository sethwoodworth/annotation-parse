import difflib
from bs4 import BeautifulSoup
import FCUtil
from diff_match_patch import diff_match_patch


class Annotation(object):
	"""docstring for textus_annotation"""
	def __init__(self):
		super(Annotation, self).__init__()


	def __init__(self,id,section_id,start_index,end_index,deleted,quote,text):
		self.id = id
		self.section_id = section_id
		self.start_index = start_index
		self.end_index = end_index
		self.deleted = deleted
		self.quote = quote
		self.text = text

	def __init__(self,annDic,uWorker):
		self.uWorker = uWorker
		self.dic = annDic
		self.id = annDic['id']
		self.date = annDic['created_on'].strip().replace(' ','T')+'Z'
		self.user_id = annDic['user_id']
		self.user = uWorker.getUserName(self.user_id)
		self.section_id = annDic['section_id']
		self.start_index = annDic['start_index']
		self.end_index = annDic['end_index']
		
		tempQuote = BeautifulSoup(FCUtil.removeSpecChar(annDic['quote']).lstrip().lstrip('\''))
		self.quote = self.fixQuote(tempQuote.get_text())
		tempText = BeautifulSoup(FCUtil.removeSpecChar(annDic['annotation']).strip().strip('\''))
		self.text = self.fixQuote(tempText.get_text())

		if "NULL" in annDic['deleted_on']:
			self.deleted = False
		else:
			self.deleted = True


	def fixQuote(self,string):
		return string.replace("&quot;",'"')
	
	def get_start(self,text):
		
		guess = FCUtil.wordcount_to_charcount(self.start_index,text)
		#matches = s.get_matching_blocks()
		#match = s.find_longest_match(0,len(self.quote),0,len(text))
		matcher = diff_match_patch()
		m = matcher.match_main(text,self.quote,guess)
		#print text
		#print self.quote
		s = difflib.SequenceMatcher(None,self.quote,text[m:m+len(self.quote)])
		r = s.ratio()
		if r < .9:
			print "Low Ratio %.2f %d " %(r,self.id)
			print "Quote: %s" %(self.quote)
			print "Text: %s" %(text[m:m+len(self.quote)])

		if m == -1:
			print "matching error for: %d" %self.id

		self.start = m
		self.end = m+len(self.quote)

	def toDictionary(self):
		payload = {'lang':'en','text':self.text}
		dic = {'start':self.start,'end':self.end,'type':'textus:comment','payload':payload,'user':self.user}
		dic['date'] = self.date
		return dic


