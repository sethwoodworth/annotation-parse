file = open('10.6.166.43.sql')
output = open('users.json', 'w')
import json
import re

output.write("[")
for row in file:
	if "INSERT INTO `annotation_type_names`" in row:
		print row
		first = row.split("(", 1)[1].split(",")
		
		dic = {}
		dic["id"] = int(first[0])
		dic["type"] = str(first[1])
		dic["icon_path"] = str(first[2])
		dic["icon_alt"] = str(str(first[3]).rsplit(");")[0])
		output.write(json.dumps(dic)+str(","))
		print json.dumps(dic, sort_keys=True, indent=4)
output.write("]")
output.close()