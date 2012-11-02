import align as aligner1
import align_ted as aligner2
import hmm

japanese,english = hmm.read_dictionary("../data/dictionary.txt")

def test_anchor(japanese, english):
    total = 0
    false = 0
    for i in range(len(english)):
        res = aligner2.anchor(japanese[i],english[i])
        total = total + 1
        if res == False:
            false = false + 1
    print "Total: %i, False: %i" % (total, false)

def test_aligners(japanese, english):    
    for i in range(len(english)):
        out1 = aligner1.align_words(japanese[i],english[i])
        out2 = aligner2.align_words(japanese[i],english[i], False)
        if (out1 != out2):
            if (out2 == "ERR"):
                print "Basic: " + str(out1)
                print "Ted  : " + str(out2)
                print "-"
        
test_aligners(japanese, english)