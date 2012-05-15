file = open('10.6.166.43.sql')
output = open('annotation_link_relationships.json', 'w')
import json
import re
import FCUtil


output.write("[")
firstTime = True
for row in file:
	if "INSERT INTO `annotation_link_relationships" in row:
		r = row.split("(", 1)[1].rsplit(");",1)[0].split(",")
		dic = {}
		if not firstTime:
			output.write (str(','))
		for item in r:
			dic["id"] = int(r[0])
			dic["title"] = FCUtil.cleanStr(r[1])
			print json.dumps(dic, sort_keys=True, indent=4)
		firstTime = False
		output.write(str(json.dumps(dic)))

output.write("]")
			
output.close()
