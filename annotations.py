file = open('10.6.166.43.sql')
output = open('annotations.json', 'w')
import json
import re

firstTime = True
output.write("[")
for row in file:
	if row[:24] == "INSERT INTO `annotations":
		#ASSUMPTIONS: Table name does not include ")"
		#Quote does not include "', [0-9]"
		if not firstTime:
				output.write (str(','))
		firstTime = False

		print row
		first = row.split("(", 1)[1].split(",", 5)
		content = first[5].rsplit(",", 3)[0]
		print "content before " + str(content)
		c1 = re.split("', [-+]?\d+", content)[0]
		c2 = re.search("', [-+]?\d+", content).group().split(",")[1]
		#c2 = re.split("', [-+]?\d+", content)[1].split(",", 1)[0]
		c3 = re.split("', [-+]?\d+", content)[1].split(",", 1)[1]
		first = first[:5]
		for (index, item) in enumerate(first):
			first[index] = int(item)

		last = row.rsplit(");", 1)[0].rsplit(",", 3)[1:]
		for (index, item) in enumerate(last):
			if index == 0:
				last[0] = int(item.replace("'", ""))
			else:
				last[index] = item.replace("'", "")
		print "first " + str(first)
		print "content " + str(content)
		print "last " + str(last)
		dic = {}
		dic["id"] = first[0]
		dic["user_id"] = first[1]
		dic["section_id"] = first[2]
		dic["start_index"] = first[3]
		dic["end_index"] = first[4]
		dic["quote"] = c1
		dic["annotation"] = c3
		dic["rating"] = c2
		dic["published"] = last[0]
		dic["created_on"] = last[1]
		dic["deleted_on"] = last[2].lstrip().rstrip()
		output.write(str(json.dumps(dic)))
		print json.dumps(dic, sort_keys=True, indent=4)

output.write("]")
output.close()