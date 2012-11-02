def ngram(arr, n):
	divider = '+'
	temp = ['^' for i in range(n)]
	out = []
	for item in arr:
		temp.pop(0)
		temp.append(item)
		out.append(divider.join(temp))
	for i in range(len(temp) - 1):
		temp.pop(0)
		temp.append('$')
		out.append(divider.join(temp))
	return out

def unngram(arr):
	divider = '+'
	out = []
	for item in arr:
		temp = item.split(divider)
		if ((temp[0] != '$') and (temp[0] != '^')):
			out.append(temp[0])
	return out
