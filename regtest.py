import re

dog = "'goober', 3, 'goober2', d"
print re.search("', [0-9]", dog).group().split(",")[1]