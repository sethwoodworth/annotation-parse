file = open('10.6.166.43.sql')
output = open('annotations.json', 'w')
import json
import re

for row in file:
	if "INSERT INTO `annotation_links" in row:
		#ASSUMPTIONS: Table name does not include ")"
		#Quote does not include "', [0-9]"

		print row
		