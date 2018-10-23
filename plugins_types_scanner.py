import re
import os

def remove_space_pattern(string):
    s = ''
    for i in range(len(string)):
        if (i+1)%2!=0:
            s += string[i]
        else:
            s += ''
    return s
filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "plugins.types")

with open(filepath, 'rb') as file:
	data = file.read()
	data = data.decode('utf-8', 'ignore')
	data = remove_space_pattern(data)# weird pattern where every 2nd character is space(extra)
	
	print("Analyzing plugin types")
	re_pattern = r'exports: \[(\".*\")]'
	r = re.findall(re_pattern, data)
	print("Exports found: %s" % r)
