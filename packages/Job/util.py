from packages.Log import kwlog
import re

def value_from_header(data, attribute):
	kwlog.log("looking for "+ str(attribute))
	result = re.search(str(attribute)+"=[^&]*&", data[0])
	kwlog.log("found: " + str(result))
	if result is None:
		return "Error"
	else:
		return result.group(0).split("=")[1].split('&')[0]

def replace_commas_with_semicolons(data):
	data = str(data)
	
	in_string = False
	for i in range(len(data)):
		if data[i] == "\"":
			in_string =  not in_string
		elif data[i] == "," and in_string:
			data[i] = ";"
	return data
