from bs4 import BeautifulSoup
import roman_int
import os



def breakHTMLDocument(path):
	file = open(path,'r')
	soup = BeautifulSoup(file)
	breaks = soup.find_all('h2')
	#style = soup.find_all('style')
	style = ""
	file = open(path,'r')
	
	num = 0
	#length = len(brk)
	newFile = open('0'+'.html','w')
	for line in file:
		
		try:
			if any(s.get_text() in line for s in breaks):
				num+=1
				newFile.write(endHTML())
				newFile.close()
				newFile = open(str(num)+'.html','w')
				newFile.write(strartHTML(style))
		except:
			print line


		newFile.write(line + '\n')
			
	
	print num
	file.close()


def strartHTML(style):
	return '<html>\n<body>\n'

def endHTML():
	return '</body>\n</html>'

def correctFileName(max):
	for n in range(57,max+1):
		file = open(str(n)+'.html','r')
		soup = BeautifulSoup(file)
		soup =  BeautifulSoup(soup.find('h2').prettify())
		string = soup.find('h2').get_text()
		string = string.strip().title()
		stringList = string.rsplit(" ")
		print stringList
		pre = "Volume "+str(n)+", "
		string = pre+stringList[0]+" "+roman_int.roman_to_english(stringList[1])
		print string
		os.rename(str(n)+'.html',string+'.html')
		file.close()



if __name__ == '__main__':
	#print roman_int.roman_to_english('X')
	#correctFileName(57)
	#print htmlentitydefs(u'0xc3')
	breakHTMLDocument('Miscellaneous Essays.html')
	