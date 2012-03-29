file = open('10.6.166.43.sql')
output = open('works.json', 'w')
import json
import re

output.write("[")
for row in file:
	if "INSERT INTO `works`" in row:
		print row
		r = row.split("(", 1)[1].rsplit(");",1)[0].split(",")
		print "array" + r[len(r)-1]
		print len(r)
		first = []
		holdString=""
		open=False
		for item in r:
			
			#print str(item[1:2])+" "+str(item[len(item)-1:len(item)])
			
			if str(item[1:2]).count("'")==1 and str(item[len(item)-1:len(item)]).count("'") != 1:
				open = True
				holdString += str(item)+","
			elif str(item[1:2]).count("'")!=1 and str(item[len(item)-1:len(item)]).count("'") == 1:
				open = False
				holdString += str(item)
			elif open:
				holdString += str(item) +","
			elif str(item[1:2]).count("'")==1 and str(item[len(item)-1:len(item)]).count("'") == 1:
				open = False
				holdString = item
			elif item.count("'")==0:
				open = False
				holdString = item
				
			if not open:
				first.append(holdString)
				holdString = ""
		
		print len(first)
		#print first
		
		
		dic = {}
		dic["id"] = int(first[0])
		dic["title"] = str(first[1])
		dic["author"] = str(first[2])
		dic["summary"] = str(first[3])
		dic["year"] = int(first[4])
		dic["page_views"] = int(first[5])
		dic["wordpress_url"] = str(first[6])
		dic["intro_essay"] = str(first[7])
		dic["created_on"] = str(str(first[8]).rsplit(");")[0])
		output.write(json.dumps(dic)+str(","))
		print json.dumps(dic, sort_keys=True, indent=4)
output.write("]")
output.close()