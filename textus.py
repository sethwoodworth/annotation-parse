import bs4
from bs4 import BeautifulSoup
from bs4 import NavigableString
from bs4 import UnicodeDammit
import json
import os
import codecs
import jsonlib
import FCUtil
from textus_annotation import Annotation
import convert
from user_lookup import UserLookup
from optparse import OptionParser

class Tag(object):
    """ FIXME: write docstring """

    def __init__(self, name,start,end):
        # why are we supering here?
        super(Tag, self).__init__()
        self.name = name
        self.start = start
        self.end = end


    def __str__(self):
        return 'Tag %s \nstart: %d\nend: %d' %(self.name,self.start,self.end)

    def toDic(self):
        return {"start":self.start,"end":self.end,"css":self.name}


class Converter(object):
    """docstring for Converter"""

    def __init__(self):
        # Why a
        super(Converter, self).__init__()
        self.annJson = FCUtil.openJsonFile('annotations.json')
        self.uWorker = UserLookup()

    def convertHTMLtoJSON(self,HTMLFilePath):
        self.sec_id = int(HTMLFilePath.rsplit('.',1)[-2].rsplit('_',1)[-1])
        self.htmlFile = open(HTMLFilePath,'r')
        soup = BeautifulSoup(self.htmlFile)

        ######Take out all unneeded white spces#####

        for t in soup.findAll(text=True):
            if type(t) is bs4.element.NavigableString: # Ignores comments and CDATA
                if t.isspace():
                    t.replaceWith('')
                else:
                    t.replaceWith(t.replace('\n','').strip()+' ')


        jsonPath = HTMLFilePath.rsplit('.',1)[0]
        jsonFile = open(jsonPath+'.json','w')

        #print self.getText(soup)
        text = self.getText(soup)
        tags = self.getAllTags(soup)
        #tags = []
        annotations = self.convertAllAnnotations(text,self.sec_id)
        #annotations = []
        title = self.getTitle(HTMLFilePath)
        print title
        struct = [{'type':'textus:document','start':0,'depth':0,'description':'imported from old database','name':title}]

        self.createJSON(jsonFile,text,tags,annotations,struct)

        self.htmlFile.close()
        jsonFile.close()
        return len(annotations)

    def getText(self,soup):
        #print type(soup.get_text())
        return soup.get_text()

    def getTitle(self,htmlPath):
        return htmlPath.rsplit('.',1)[0].rsplit('/',1)[1].split('_',1)[0]


    def surrounded_by_strings(self,tag):
        return (isinstance(tag.next_element, NavigableString) and isinstance(tag.previous_element, NavigableString))

    def stringLengthOfTag(self,tag):
        count = 0
        for s in tag.find_all(text=True):
            count+=len(s)
        return count

    def getAllFromTag(self,tags,tag):
        for t in tag.children:
            if 'NavigableString' not in str(type(t)):
                l = self.stringLengthOfTag(t)
                s = self.getOffsetFromTag(t)
                tags.append({'start':s,'end':s+l,"css":t.name})
                self.getAllFromTag(tags,t)
        return tags

    def getOffsetFromTag(self,tag):
        p = tag.previous_element
        count = 0
        while( p is not None):
            if 'NavigableString' in str(type(p)):
                count += len(p)
            p = p.previous_element
        return count


    def getAllTags(self,soup):
        tags = []

        for item in soup.children:
            k = self.getAllFromTag(tags,item)

        #for item in tags:
            #print item

        return tags

    def updateDic(self,tagDic,tag,start,length):
        if tag not in tagDic:
            tagDic[tag]=Tag(tag.name,start,length)
        else:
            oldTag = tagDic[tag]
            tagDic[tag] = Tag(tag.name,min(start,oldTag.start),max(length,oldTag.end))
        return tagDic

    def createJSON(self,jsonFile,text,tags,annotations,struct):
        t = []
        t.append({"text":text,"sequence":0})
        dic = {'text':t,'offset':0,'typography':tags,'semantics':annotations,'structure':struct}
        jsonFile.write(json.dumps(dic,sort_keys=True))
        #json_ustr = jsonlib.write( dic, ascii_only=False )
        #json_bytes = json_ustr.encode('utf-8')
        #jsonFile.write(json_bytes)

    def getAllAnnotationsForSection(self,id):
        annList = []
        for obj in self.annJson:
            if obj['section_id'] == id:
                tempAnn = Annotation(obj,self.uWorker)
                if not tempAnn.deleted:
                    annList.append(tempAnn)
        return annList

    def convertAllAnnotations(self,text,id):
        annList = self.getAllAnnotationsForSection(id)
        print 'Total Annotations: %d'%len(annList)
        convertedList = []
        for ann in annList:
            start = ann.get_start(text)
            convertedList.append(ann.toDictionary())
        return convertedList

if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                  help="write report to FILE", metavar="FILE")

    (options, args) = parser.parse_args()

    conv = Converter()
    conv.convertHTMLtoJSON(options.filename)
    #conv.convertHTMLtoJSON('/Users/David/Documents/Finals Club/Miguel de Cervantes Saavedra/Don Quixote de la Mancha/Don Quixote de la Mancha About Cervantes and Don Quixote_112_2306.html')
    #print '\n2\n'
    #conv.convertHTMLtoJSON('2.html')
