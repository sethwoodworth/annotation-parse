import json

def createIntroEssays(auth):
	file = open('works.json')
	j = json.load(file)
	file.close()
	ids = []
	for obj in j:
		if auth in obj['author']:
			ids.append(obj['id'])
			if obj['intro_essay']:
				output = open(str(obj['title'])+'_intro_essay_'+str(obj['id'])+'.html', 'w')
				print obj['id']
				output.write(obj['intro_essay'])
				output.close()

createIntroEssays('William Shakespeare')