file = open('10.6.166.43.sql')
output = open('users_files.json', 'w')
import json
import re
import FCUtil


output.write("[")
firstTime = True
for row in file:
	if "INSERT INTO `users_files`" in row:
		r = row.split("(", 1)[1].rsplit(");",1)[0].split(",")
		dic = {}
		if not firstTime:
			output.write (str(','))
		for item in r:
			dic["id"] = int(r[0])
			dic["user_id"] = int(r[1])
			dic["work_id"] = int(r[2])
			dic["name"] = str(FCUtil.cleanStr(r[3]))
			dic["description"] = str(FCUtil.cleanStr(r[4]))
			dic["file_location"] = str(FCUtil.cleanStr(r[5]))
			dic["created_on"] = str(FCUtil.cleanStr(r[6]))
			dic["deleted_on"] = str(FCUtil.cleanStr(r[7]))
			print json.dumps(dic, sort_keys=True, indent=4)
		firstTime = False
		print json.dumps(dic, sort_keys=True, indent=4)
		output.write(str(json.dumps(dic)))

output.write("]")
			
output.close()
