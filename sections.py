file = open('10.6.166.43.sql')
output = open('sections.json', 'w')
import json
import re

output.write("[")
for row in file:
	if "INSERT INTO `sections" in row:
		print row
		first = row.split("(", 1)[1].split(",", 3)
		dic = {}
		dic["id"] = int(first[0])
		dic["work_id"] = int(first[1])
		dic["order"] = int(first[2])
		dic["name"] = str(first[3]).rsplit(");")[0].split("\'")[1]
		output.write(json.dumps(dic)+str(","))
		print json.dumps(dic, sort_keys=True, indent=4)
output.write("]")
output.close()