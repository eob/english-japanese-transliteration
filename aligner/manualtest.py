from nltk import *
from nltk.tag.hmm import HiddenMarkovModelTagger as Hmm
import sys
from hmm import * 

"""
Manually construct the labeled squences, then use HiddenMarkovModelTagger to train them
token[0]: text
token[1]: state

"""
#sen1 = (('A','AA'),('A-','R'),('T','T'),('I','IX'),('Z','S'),('A','AE'),('N','N'))
sen1 = (('AA','A'),('R','A-'),('T','T'),('IX','I'),('S','Z'),('AE','A'),('N','N'))
#sen2 = (('AI','AY'),('AY','S'))
sen2 = (('AY','AI'),('S','AY'))
#sen3 = (('AI','AY'),('S','S'),('O','AX'),('TA','T'),('I','AY'),('P','P'),('U','AX'))
sen3 = (('AY','AI'),('S','S'),('AX','O'),('T','TA'),('AY','I'),('P','P'),('AX','U'))
#sen4 = (('AI','AY'),('T','T'),('E','AX'),('MU','M'))
sen4 = (('AY','AI'),('T','T'),('AX','E'),('M','MU'))
#sen5 = (('AI','AY'),('D','D'),('O','AX'),('RU','L'),('K','K'),('O','AO'),('SU','S'),('T','T'),('O','AX'))
sen5 = (('AY','AI'),('D','D'),('AX','O'),('L','RU'),('K','K'),('AO','O'),('S','SU'),('T','T'),('AX','O'))
#sen6 = (('AI','AY'),('RA','L'),('I','AY'),('N','N'))
sen6 = (('AY','AI'),('L','RA'),('AY','I'),('N','N'))
#sen7 = (('AI','AY'),('R','AXR'),('I','IH'),('SU','S'))
sen7 = (('AY','AI'),('AXR','R'),('IH','I'),('S','SU'))
#sen8 = (('AU','AW'),('TO','T'),('DO','D'),('A','OW'),('A-','R'),('GE','G'),('E-','EY'),('MU','M'))
#sen9 = (('A','AE'),('K','K'),('A','AX'),('D','D'),('E','EH'),('M','M'),('I','IX'),('S','S'),('I','IX'),('Z','Z'),('U','AX'),('MU','M'))
#sen10 = (('A','AX'),('KU','K'),('S','S'),('E','EH'),('PU','P'),('T','T'),('A','AX'),('N','N'),('SU','S'))
sen8 = (('AW','AU'),('T','TO'),('D','DO'),('OW','A'),('R','A-'),('G','GE'),('EY','E-'),('M','MU'))
sen9 = (('AE','A'),('K','K'),('AX','A'),('D','D'),('EH','E'),('M','M'),('IX','I'),('S','S'),('IX','I'),('Z','Z'),('AX','U'),('M','MU'))
sen10 = (('AX','A'),('K','KU'),('S','S'),('EH','E'),('P','PU'),('T','T'),('AX','A'),('N','N'),('S','SU'))
sen11 =(('AA','A'),('R','A-'),('B','B'),('AX','I'),('T','T'),('ER','A'))

#Truth:[('AA', 'A'), ('R', '-'), ('B', 'B'), ('AX', 'I'), ('T', 'T'), ('ER', 'A')]
#Guess:[('AA', 'A'), ('R', '-'), ('B', 'B'), ('AX', 'U'), ('T', 'TA'), ('ER', '-')]
#Truth:[('AY', 'AI'), ('S', 'S'), ('AX', 'O'), ('L', 'RE'), ('IH', '-'), ('T', 'T'), ('ER', 'A')]
#Guess:[('AY', 'AI'), ('S', 'S'), ('AX', 'U'), ('L', 'RA'), ('IH', 'I'), ('T', 'TA'), ('ER', '-')]

def build_manual():
	seqs = []
	seqs.insert(0,sen11)
	seqs.insert(0,sen10)
	seqs.insert(0,sen9)
	seqs.insert(0,sen8)
	seqs.insert(0,sen6)
	seqs.insert(0,sen5)
	seqs.insert(0,sen4)
	seqs.insert(0,sen3)
	seqs.insert(0,sen2)
	seqs.insert(0,sen1)
 	result = Hmm.train(seqs)
 	
 	return result

result = build_manual()


print "+++++++++"
print result._symbols
print result._outputs._pdists
print result._states
print result._transitions._pdists
print result._priors	
print "+++++++++"
#	serializeHMM(result)