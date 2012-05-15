file = open('10.6.166.43.sql')
output = open('works_sponsored.json', 'w')
import json
import re
import FCUtil


output.write("[")
firstTime = True
for row in file:
	if "INSERT INTO `works_sponsored`" in row:
		r = row.split("(", 1)[1].rsplit(");",1)[0].split(",",1)
		dic = {}
		if not firstTime:
			output.write (str(','))
		for item in r:
			dic["work_id"] = int(r[0])
			dic["user_id"] = int(r[1])
			print json.dumps(dic, sort_keys=True, indent=4)
		firstTime = False
		output.write(str(json.dumps(dic)))

output.write("]")
			
output.close()
