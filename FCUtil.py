import HTMLParser
import unicodedata
import re, htmlentitydefs
import json

sd = {
    '\\r\\n':' ',
    '\r\n':' ',
	'\\r':'',
	'\\n':'',
	'\'\'':'\'',
	'\'\'\'\'':'\"\'',
	'\\':' ',
	'\'\'':'\'',
    '--':'&mdash;'
}

def cleanLTQ(item):
	if str(item[1:2]).count("'")>0:
		item = str(item).split("'",1)[1]
	if str(item[len(item)-1:len(item)]).count("'")>0:
		item = str(item).rsplit("'",1)[0]
	return item


def removeSpecChar(s):
	for k, v in sd.iteritems():
		s=s.replace(k,v)
	return s

def unescapeHTML(s):
	return strip_html(s)

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)	

def strip_html(text):
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<":
            return "" # ignore tags
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        elif text[:1] == "&":
            import htmlentitydefs
            entity = htmlentitydefs.entitydefs.get(text[1:-1])
            if entity:
                if entity[:2] == "&#":
                    try:
                        return unichr(int(entity[2:-1]))
                    except ValueError:
                        pass
                else:
                    return unicode(entity, "iso-8859-1")
        return text # leave as is
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)	
	
def cleanStr(s):
	if s == ' \' \'':
		return None
	else:
		return removeSpecChar(removeSpecChar(cleanLTQ(s)))
	
def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub(' ', data)
    
def remove_html_tags_noWS(data):
	p = re.compile(r'<.*?>')
	return p.sub('', data)

def getAllAnnoationsforSec(id):
    annJson = openJsonFile('annotations.json')
    annList = []
    for obj in annJson:
        if obj['section_id'] == id:
            annList.append(obj['id'])
    return annList

def getAllAnnotationsforWork(id):
    annJson = openJsonFile('annotations.json')
    annList = []
    secList = getAllSectionsforWork(id)
    for obj in annJson:
        if obj['section_id'] in secList:
            annList.append(obj['id'])
    return annList

def getAllSectionsforWork(id):
    secJson = openJsonFile('sections.json')
    seclist = []
    for obj in secJson:
        if obj['work_id'] == id:
            seclist.append(obj['id'])
    return seclist

def getAllWorksExcluding(authors):
    workJson = openJsonFile('works.json')
    worklist= []
    for obj in workJson:
        if obj['author'] not in authors:
            worklist.append(obj['id'])
    return worklist

def openJsonFile(path):
    f = open(path)
    #print "test"
    JSON = json.load(f)
    f.close()
    return JSON

def wordcount_to_charcount(wordcount,text):
    count = 0
    for word in text.split()[0:wordcount-1]:
        count += (len(word)+1)
    if wordcount < 1:
        print 'Word Count less than 1'
    return count


	
