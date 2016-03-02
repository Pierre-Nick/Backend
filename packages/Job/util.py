def strip_headers(data_array):
	split_point = 0
	for x in range(len(data_array)):
		if data_array[x] is "":
			split_point = x
			break
	return data_array[x+1:]
