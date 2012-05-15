file = open('10.6.166.43.sql')
output = open('section_parents.json', 'w')
import json
import re

firstTime = True
output.write("[")
for row in file:
	if "INSERT INTO `section_parents" in row:
		if not firstTime:
			output.write (str(','))
		firstTime = False
		print row
		first = row.split("(", 1)[1].split(",", 1)
		dic = {}
		dic["parent_id"] = int(first[0])
		dic["child_id"] = int(str(first[1]).rsplit(");")[0])
		#dic["order"] = int(first[2])
		#dic["name"] = str(first[3]).rsplit(");")[0].split("\'")[1]
		output.write(json.dumps(dic))
		print json.dumps(dic, sort_keys=True, indent=4)
output.write("]")
output.close()