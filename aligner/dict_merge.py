def main():
	import sys
	import os

	JAPANESE = "../data/japan_english_utf8.txt"
	ENGLISH = "../data/transcription.txt"
	OUT = "../data/dictionary.txt"
	
	try:
		os.remove(OUT)
	except:
		pass
	
	j = open(JAPANESE)
	e = open(ENGLISH)
	o = open(OUT, 'w')
	
	jl = j.readlines()
	el = e.readlines()
	
	for i in range(len(jl)):
		s = "%s,%s" % (jl[i].rstrip('\n'), el[i])
		o.write(s)
	
	j.close
	e.close
	o.close	


if __name__ == '__main__': main()