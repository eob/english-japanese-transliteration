from nltk import *
from nltk.tag.hmm import HiddenMarkovModelTagger as Hmm
import sys
import ngramer 

# Enumeration of Test types
class Enumerate(object):
	def __init__(self, names):
		for number, name in enumerate(names.split()):
			setattr(self, name, number)

test_types = Enumerate("CROSS_VALIDATE LOOCV")

# STEP 1
#
#
def read_dictionary(dictionary_file):
	"""
	INPUT:
		dictionary_file - the path to a dictionary file of format
		  ENGLISH, KATAKANA, JAPANESE PHONEMES, ENGLISH PHONEMES
	
	OUTPUT:
		japanese_phoneme_set, english_phoneme_set
		Two parallel arrays containing the English and Japanese phonemes.
	"""
	print "[Start] Reading dictionary"
	dictionary = open(dictionary_file)
	lines = dictionary.readlines()
	
	japanese_phoneme_set = []
	english_phoneme_set = []	

	for i in range(len(lines)):
 		try:
			arr = lines[i].strip().split(',')
			japanese_phonemes = arr[2]
			english_phonemes  = arr[3]
 			japanese_phoneme_set.append(japanese_phonemes)
 			english_phoneme_set.append(english_phonemes)
		except:
			print "err"
	
	dictionary.close()
	print "[ End ] Reading dictionary"	
	return japanese_phoneme_set, english_phoneme_set

# STEP 2
#
#	
def align_phoneme_sets(japanese,english,verbose=False):
	"""
	INPUT:
		japanese - an array of japanese phoneme sequences. each item is a string
		english  - an array of english phoneme sequences. each item is a string
	
	OUTPUT: 
		j_aligned - an array of japanese phoneme sequences. each item is an ARRAY
		e_aligned - an array of english phoneme sequences. each item is an ARRAY
	"""
	import align_ted as aligner
	print "[Start] Aligning Phoneme Sequences"
	print "[.....] Starting with %i sequences" % len(japanese)	
	
	aligned_japanese = []
	aligned_english = []
	errors = 0 
	err_align = open("error_align.txt",'w')

	for i in range(len(japanese)):
		try:
			jap_phones = japanese[i] 
			eng_phones = english[i]
			aligned = aligner.align_words(jap_phones,eng_phones,False)
			if (aligned == "ERR"):
				err_align.write("line No:%d"%i+"\n")
				err_align.write("Eng:%s"%jap_phones[i])
				err_align.write("Jap:%s"%eng_phones[i]+"\n")
				errors = errors + 1
			else:
				aligned_japanese.append(aligned[0])
				aligned_english.append(aligned[1])
 		except:
 			if verbose:
				print "Unexpected error line %i: %s" % (i, sys.exc_info()[0]) 
			errors = errors + 1

	err_align.close()
	print "[.....] Success: %i, Error: %i, Error Rate: %f" % (len(aligned_japanese), errors, float(errors)/len(aligned_japanese))
	print "[ End ] Aligning Phoneme Sequences"
	return aligned_japanese, aligned_english
	
# STEP 3
#
#	
def construct_hmm(japanese,english):
	"""
	INPUT:
		*Aligned* parallel arrays
	OUTPUT: 
		An HMM
	"""
	print "[Start] Training HMM"
	# Coming in, we have two parallel arrays of arrays.
	# [ ['j1', 'j2'], ['j1', 'j2'] ] + [ ['e1', 'e2'], ['e1', 'e2'] ]
	# What we need is an array of combined tuples
	# [ [ [j1,e1],[j2,e2] ], [ [j1,e1],[j2,e2] ] ]
	training_data = []
	for i in range(len(japanese)):
		sequence = []
		j_word = japanese[i]
		e_word = english[i]
		for j in range(len(j_word)):
			sequence.append((e_word[j],j_word[j]))
		training_data.append(sequence)
	model = Hmm.train(training_data)
	print "[ End ] Training HMM"
	return model


def serializeHMM(result):
	import pickle as pickle
	SYMBOLS = open("_symbols.hmm","w")
	TRANSITIONS = open("_transitions.hmm","w")
	STATES = open("_states.hmm","w")
	OUTPUTS = open("_outputs.hmm","w")
	PRIORS = open("_priors.hmm","w")
	
	pickle.dump(result._symbols,SYMBOLS)
	pickle.dump(result._transitions,TRANSITIONS)
	pickle.dump(result._states,STATES)
	pickle.dump(result._outputs,OUTPUTS)
	pickle.dump(result._priors,PRIORS)
	
	SYMBOLS.close()
	TRANSITIONS.close()
	STATES.close()
	OUTPUTS.close()
	PRIORS.close()
		
def generate_idx(k,total):
	import random
	indexes = []
	cards = range(total)
	for i in range(k):
		random.shuffle(cards)
		test = cards[:total/k]
		train = cards[total/k:]
		single=[train,test]
		indexes.append(single)	
	
	return indexes 	
	
def cross_validate(j_lines,e_lines,index,ngram_order=1,verbose=False):
	print "[Start] Cross Validating Data"
	
	rightfile = open("out_right.txt" % index, "w")
	wrongfile = open("out_wrong.txt" % index, "w")
	
	get_right = 0
 	total_score = 0.0
	buckets = [0,0,0,0,0,0,0,0,0,0]
	
	print "[.....] Creating training and testing data sets"
	train_j,train_e,test_j,test_e = split_data(j_lines,e_lines,index)
 	total_test = len(test_e)

	print "[Start] Converting training set to %i-Grams" % ngram_order
	n_gramed_japanese = [ngramer.ngram(x, ngram_order) for x in train_j]
	n_gramed_english = [ngramer.ngram(x, ngram_order) for x in train_e]
	print "[ End ] Converting training set to %i-Grams" % ngram_order

	model = construct_hmm(n_gramed_japanese,n_gramed_english)
	
	# NOW STAT THE TESTING PHASE
	# need to first also build the truth into dictionary
	
	print "[.....] Preparing test set"
	ground_truth = {}
	for i in range(len(test_e)):
		e = ' '.join(test_e[i])
		j = ' '.join(test_j[i])
		ground_truth[e] = j
	
	print "[.....] Testing"
	for eng in test_e:
		e = ' '.join(eng)
 		score,correct,guess = test_one(model,e,ground_truth[e],ngram_order=ngram_order,verbose=verbose)
 		if correct:
 			get_right +=1
			rightfile.write("%s,%s\n" % (e, ground_truth[e]))
		else:
			wrongfile.write("%s,%s,%s\n" % (e, ground_truth[e],guess))
 		total_score += score
		bucket = int(score*10)
		if bucket > 9:
			bucket = 9
		buckets[bucket] = buckets[bucket] + 1
	
 	avg_score = total_score/total_test
 	precision_word_wise = float(get_right)/float(total_test)
	print "[.....] Average Score: %f" % avg_score
	print "[.....] Wordwise Precision: %f" % precision_word_wise
	print "[.....] Buckets:" 
	for i in range(10):
		print "[.....] %i to %i Percent: %i" % ((i*10), ((i+1)*10), buckets[i])
		
 	print "[ End ] Cross Validating Data"
	rightfile.close()
	wrongfile.close()
 	return avg_score,precision_word_wise
 	
		

def split_data(japanese,english,index):
# input are parallel corpus of japanese and English corpus, plus the [[train],[test]] index 
 	part = Enumerate("TRAIN TEST")
 	japanese_train = []
 	english_train = []
 	japanese_test = []
 	english_test = []

 	for idx in index[part.TRAIN]:
 		japanese_train.append(japanese[idx])
 		english_train.append(english[idx])
 	
 	for idx2 in index[part.TEST]:
 		japanese_test.append(japanese[idx2])
 		english_test.append(english[idx2])
 
 	return japanese_train, english_train, japanese_test, english_test
 	
def guess(model,teststring,ngram_order=1,verbose=False):
	# lable a single test string and return it's score
	# change "AA R B AX T ER" into ['AA','R','B', 'AX', 'T','ER']
	unlabeled = teststring.split()
	unlabeled_ngram = ngramer.ngram(unlabeled, ngram_order)
	if verbose:
		print "Converted to %i-Gram: %s " % (ngram_order, unlabeled_ngram)
		
	result = model.tag(unlabeled_ngram)	
		
 	# Fetch the (possibly N-Gramed) result
	result_ngram = []
	for align in result:
		result_ngram.append(align[1])
		
	if verbose:
		print "Recovered: %s " % (result_ngram)
 	
 	# Un-NGram the result
 	result_recovered = ngramer.unngram(result_ngram)

	if verbose:
		print "Fixed to: %s " % (result_recovered)

 	# Construct the guess from this array
	kata_guess = "".join(result_recovered)
	return kata_guess
	

def test_one(model,teststring,correctseq,ngram_order=1,verbose=False):
	"""
	INPUT:
		model       - a trained HMM
		teststring  - the string of english phonemes ("AA R B AX T ER")
		correctseq  - the string representing the correct sequence of japanese
	OUTPUT: 
		score,correct,guess
	"""
	
	if verbose:
		print "Testing: %s (should be: %s)" % (teststring, correctseq)

	correct = False
 	
	kata_guess = guess(model,teststring,ngram_order,verbose)

	# !! NOW WE REMOVE ALL SPACES FROM kata_guess AND correctseq
	kata_guess = kata_guess.replace(" ", "")
	correctseq = correctseq.replace(" ", "")
 
	if verbose:
		print "Truth:%s"%correctseq
		print "Guess:%s"% result
		print "GuessString:%s"%kata_guess
	
	dist,length = LevenshteinDistance(correctseq,kata_guess)
	if verbose:
		print "dist:%d, length:%d "%(dist,length)
	score = (float(length-dist)/float(length))
	if verbose:
		print "score:%f"%score
	
	if score == 1.0:
		correct = True
 
	return score,correct,kata_guess
	

def LevenshteinDistance(truth, guess):
	# truth : "A I SO RE - TA"
	# guess : "AI S U RA I TA -"
	DEL_COST = 1.0
	INS_COST = 1.0
	SUB_COST = 1.0
	
	t =  collapse(truth)
	g  =  collapse(guess) # makes "A I SO RE - TA" becomes "AISORE-TA"
	
	_truth = list(t) # turn the string into list
	_guess = list(g) # turn into list
	
	matrix = init_matrix(len(_truth),len(_guess))

	for i in range(len(_truth)):
		matrix[i][0] = i
	for j in range(len(_guess)):
		matrix[0][j] = j
	

	for i in range(1,len(_truth)):
		for j in range(1,len(_guess)):
			if(_truth[i]==_guess[j]):
				cost = 0
			else:
				cost = SUB_COST
			
			matrix[i][j] = min(matrix[i-1][j] + INS_COST,
								matrix[i][j-1] + DEL_COST,
								matrix[i-1][j-1] + cost
								)
	# get the final score from 							
 	score = matrix[len(_truth)-1][len(_guess)-1]

 	return score,len(t)
 	
def collapse(s):
	result = ""
	for tmp in s.split():
		result = result+tmp
	return result

def init_matrix(x,y):
	d = []
	for i in range(x):
		d.append([])
		for j in range(y):
			d[i].append(0)
	return d


#######-------------------------------------------------------------------
#
# MAIN ROUTINES
#
def systemtest(dictionary_file, type, ngram_order=1, verbose=False):
	japanese, english = read_dictionary(dictionary_file)
	aligned_japanese, aligned_english = align_phoneme_sets(japanese, english)	
	K_FOLD = 20
	indexes = generate_idx(K_FOLD,len(aligned_japanese))
	score = []
	for i in range(K_FOLD):
		_score,precision = cross_validate(aligned_japanese,aligned_english,indexes[i],ngram_order=ngram_order,verbose=verbose)
		score.append([_score,precision])
	return score
	
def smalltest(dictionary_file, ngram_order=1, verbose=False):
	import ngramer
	
	japanese, english = read_dictionary(dictionary_file)
	aligned_japanese, aligned_english = align_phoneme_sets(japanese, english)
	
	print "[Start] Converting dictionary to %i-Grams" % ngram_order
	n_gramed_japanese = [ngramer.ngram(x, ngram_order) for x in aligned_japanese]
	n_gramed_english = [ngramer.ngram(x, ngram_order) for x in aligned_english]
	print "[ End ] Converting dictionary to %i-Grams" % ngram_order
 	
	model = construct_hmm(n_gramed_japanese,n_gramed_english)

  	true_japanese = "A - BA n"
	english = "ER B AX N"

	test_one(model,"AA M AX N D AX","A - MO n DO",ngram_order,verbose)
 
def newwordtest(dictionary_file, wordfile, ngram_order=1, verbose=False):
	import ngramer
	
	japanese, english = read_dictionary(dictionary_file)
	aligned_japanese, aligned_english = align_phoneme_sets(japanese, english)
	
	print "[Start] Converting dictionary to %i-Grams" % ngram_order
	n_gramed_japanese = [ngramer.ngram(x, ngram_order) for x in aligned_japanese]
	n_gramed_english = [ngramer.ngram(x, ngram_order) for x in aligned_english]
	print "[ End ] Converting dictionary to %i-Grams" % ngram_order
 	
	model = construct_hmm(n_gramed_japanese,n_gramed_english)
	
	testfile = open(wordfile)
	testlines = testfile.readlines()
	
	for i in range(len(testlines)):
		line = testlines[i]
		tup  = line.split(",")
		english = tup[0]
		sound   = tup[1]
		kguess = guess(model,sound,ngram_order,verbose)
		print "%s -> %s -> %s" % (english, sound, kguess)
	
def main():
	"""
	Note: 
		DICTIONARY INPUT
		-----------------
		The new dictionary is ../data/dictionary.txt. This is a 4-tuple where
		the english phoneme sequence has been added on the end. It is generated
		from the japan_english_utf8.txt and transcription.txt files using the
		dict_merge.py script found in this directory
	"""
	import hmm
	import sys
	from hmm import Enumerate as Enum
	
	# Pick the NGRAM Order
	if (len(sys.argv) > 1):
		ngram_order = int(sys.argv[1])
	else:
		ngram_order = 3
		
	ngram_order = 1# Hard code to 2
	print "Using N-Gram Order %i" % ngram_order

	# Dictionary Files
	DICT = "../data/dictionary.txt" 
	REALTEST = "../data/word_test.txt"
	# hmm.smalltest(DICT,ngram_order=ngram_order,verbose=True)
	#hmm.systemtest(DICT,test_types.CROSS_VALIDATE, ngram_order=ngram_order,verbose=False)
	hmm.newwordtest(DICT,REALTEST,ngram_order=ngram_order,verbose=False)


if __name__ == '__main__': main()


