file = open('10.6.166.43.sql')
output = open('annotation_links.json', 'w')
import json
import re
import FCUtil


output.write("[")
firstTime = True
for row in file:
	if "INSERT INTO `annotation_links`" in row:
		r = row.split("(", 1)[1].rsplit(");",1)[0].split(",",4)
		dic = {}
		if not firstTime:
			output.write (str(','))
		for item in r:
			dic["id"] = int(r[0])
			dic["annotation_linker_id"] = int(r[1])
			dic["linkee_type"] = FCUtil.cleanStr(r[2])
			dic["linkee_id"] = int(r[3])
			dic["reason"]= FCUtil.cleanStr(r[4].rsplit(',',1)[0])
			dic["relationship"] = int(r[4].rsplit(',',1)[1])
			print json.dumps(dic, sort_keys=True, indent=4)
		firstTime = False
		output.write(str(json.dumps(dic)))

output.write("]")
			
output.close()
