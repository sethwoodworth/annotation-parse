file = open('10.6.166.43.sql')
output = open('content.json', 'w')
import json
import re
import FCUtil

firstTime = True
output.write("[")
for row in file:
	if row[:20] == "INSERT INTO `content":
		if not firstTime:
			output.write (str(','))
		firstTime = False
	
		first = row.split("(", 1)[1].split(",", 2)
		dic = {}
		dic["id"] = int(first[0])
		dic["section_id"] = int(first[1])
		dic["content"] = FCUtil.cleanStr(str(str(first[2]).rsplit(");")[0]))
		output.write(json.dumps(dic))
		print json.dumps(dic, sort_keys=True, indent=4)
output.write("]")
output.close()