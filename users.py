file = open('10.6.166.43.sql')
output = open('users.json', 'w')
import json
import re

output.write("[")
for row in file:
	if "INSERT INTO `users`" in row:
		#print row
		first = row.split("(", 1)[1].split(",")
		#second = first[len(first)-1].split(",")
		second = []
		print first
		print len(first)
		holdString = ""
		open = False
	
		for item in first:
			
			#print str(item[1:2])+" "+str(item[len(item)-1:len(item)])
			
			
			if str(item[1:2]).count("'")==1 and str(item[len(item)-1:len(item)]).count("'") != 1:
				open = True
				holdString += str(item)+","
			elif str(item[1:2]).count("'")!=1 and str(item[len(item)-1:len(item)]).count("'") == 1:
				open = False
				holdString += str(item)
			elif open:
				holdString += str(item) +","
			elif str(item[1:2]).count("'")==1 and str(item[len(item)-1:len(item)]).count("'") == 1:
				open = False
				holdString = item
			elif item.count("'")==0:
				open = False
				holdString = item
				
			if not open:
				second.append(holdString)
				holdString = ""
		
		#print second
		
		dic = {}
		dic["id"] = int(second[0])
		dic["hash_id"] = str(second[1])
		dic["email_identifier"] = str(second[2])
		dic["name"] = str(second[3])
		dic["second_name"] = str(second[4])
		dic["middle_name"] = str(second[5])
		dic["last_name"] = str(second[6])
		dic["username"] = str(second[7])
		dic["email"] = str(second[8])
		dic["password"] = str(second[9])
		dic["affiliation"] = str(second[10])
		dic["favorite_books"] = str(second[11])
		dic["education_level"] = str(second[12])
		dic["philosophy"] = str(second[13])
		dic["academic_influences"] = str(second[14])
		dic["gender"] = str(second[15])
		dic["year_of_birth"] = str(second[16])
		dic["country"] = int(second[17])
		dic["city"] = str(second[18])
		dic["library_public"] = str(second[19])
		dic["num_logins"] = str(second[20])
		dic["is_logged_in"] = str(second[21])
		dic["last_activity"] = str(second[22])
		dic["last_login"] = str(second[23])
		dic["created_on"] = str(second[24])
		dic["activated_on"] = str(second[25])
		dic["deleted_on"] = str(second[26])
		dic["networkid"] = str(second[27])
		dic["activated_on"] = str(second[28])
		dic["photo_path"] = str(second[29])
		dic["website"] = str(second[30])
		dic["standing"] = str(second[31].rsplit(");")[0])
		#dic["child_id"] = int(str(second[1]).rsplit(");")[0])
		#dic["order"] = int(second[2])
		#dic["name"] = str(second[3]).rsplit(");")[0].split("\'")[1]
		output.write(json.dumps(dic)+str(","))
		print json.dumps(dic, sort_keys=True, indent=4)
output.write("]")
output.close()