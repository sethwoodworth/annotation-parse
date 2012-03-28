file = open('10.6.166.43.sql')
output = open('section_parents.json', 'w')
import json
import re

output.write("[")
for row in file:
	if "INSERT INTO `sections" in row:
		print row
		#first = row.split("(", 1)[1].split(",", 2)
		dic = {}
		#dic["id"] = int(first[0])
		#dic["section_id"] = int(first[1])
		#dic["content"] = str(first[2]).rsplit(");")[0]
		#output.write(json.dumps(dic)+str(","))
		#print json.dumps(dic, sort_keys=True, indent=4)
#output.write("]")
#output.close()