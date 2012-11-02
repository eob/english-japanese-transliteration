#!/usr/bin/env python
import sys
import math
import os

#How to use:

#python align.py "JAPANESE TRANSCRIPTION" "ENGLISH TRANSCRIPTION"
#(e.g., python align.py "A I SU" "AY S")
#outputs final japanese alignment (e.g., AI SU)


def init(japanese,english,verbose=True):
    global final_j_word #final output variable
    global anchor
    global prev_e_phone
    
    #first argument is the Japanese transcription
    #second argument is the English transcription
    #japanese = sys.argv[1]
    #english = sys.argv[2]
    #print japanese
    #print english
    
    
    #anchor letters (added J as an anchor)
    anchor = ["K", "G", "S", "Z", "T", "D", "N", "B", "H", "P", "M", "R","W", "L", "J"] #is L an anchor character

    #initialize lists
    j_word = []
    e_word = []
    word = ""

    #Take the string from the command line and put
    #it in a list format where each syllable/phoneme
    #is an element in the japanese/english lists
    for j_char in japanese:
        if(j_char == " "):
            j_word.append(word.strip())
            
            word=""
        word = word + j_char

    j_word.append(word.strip())

    #reinitialize variable for enlgish parsing
    word = ""

    #same structure/purpose as the japanese for loop above
    for e_char in english:
        if(e_char == " "):
            e_word.append(word.strip())
            
            word=""
        word = word + e_char

    e_word.append(word.strip())
    final_e_word = e_word
    #initialize variables
    final_j_word =[]
    prev_j_index = 0
    prev_e_phone = 0
    j_index = -1  # initialize to -1 1) because it is invald 2) bc the find_anchor 
    # will always start loking at j_index+1
    e_word_orig = e_word

    #go through each phoneme in the (remaining part) of the english word
    for e_phone in e_word:
        #find the anchor 
        try:
            if((e_phone[0] in anchor) or e_phone=="AXR"):

                #convert the AXR to R
                if(e_phone == "AXR"):
                    anchor_e = "R"

                    #conert L to R
                elif(e_phone[0] == "L"):
                    anchor_e = "R"+ e_phone[1:]

                else:
                    anchor_e = e_phone

                    #used to make sure it doesn't align an anchor
                    #with another anchor that was previously aligned
                    prev_j_index  = j_index

                    #find the anchor in the japanese word that corresponds
                    #to the english word
                    j_index = find_anchor(j_word, e_word, anchor_e, prev_j_index+1)

                    #make sure you don't duplicate the finding the same anchor 
                    # if(prev_j_index == 1 and j_index == 0 and e_phone[0]==prev_e_phone):
                    #    j_index = skip_first_find_anchor(j_word,e_word, anchor_e)

                    #if you do find an anchor that corresponds to the english anchor....
                    if(j_index != -1):

                        #get the prefix contained by the boundary anchors
                        prefix_e = e_word[0:e_word.index(e_phone)]
                        prefix_j = j_word[0:j_index]

                        #determine the remaining part of the english/japanese word
                        e_word = e_word[e_word.index(e_phone):]
                        j_word = j_word[j_index:]


                        #align the syllables/phonems properly!
                        if(align(prefix_j, prefix_e)==-1):
                            print "ERROR1"
                            return "ERR" 

                            #reinitialize status variable
                            skip_first_letter = 0

                            #find any japanese anchor if you cant find a matching english/japanese anchor
                        else:

                            j_index = find_non_matching_anchor(j_word, e_word, anchor_e, prev_j_index+1)

                            #alignment MUST ALWAYS start with the first japanese syllable
                            if(j_index > 0 and e_word_orig.index(e_phone)==0):
                                print "ERROR2"
                                return "ERR"


                                #get the prefix contained by the boundary anchors
                                prefix_e = e_word[0:e_word.index(e_phone)]
                                prefix_j = j_word[0:j_index]

                                #determine the remaining part of the english/japanese word
                                e_word = e_word[e_word.index(e_phone):]
                                j_word = j_word[j_index:]

                                print "prefix_e:%s"%prefix_e
                                print "prefix_j:%s"%prefix_j
                                #align the syllables/phonems properly!
                                if(align(prefix_j, prefix_e)==-1):
                                    print "ERROR3"
                                    return "ERR"

                                    #reinitialize status variable
                                    skip_first_letter = 0
                                    prev_e_phone = e_phone[0]
        except IndexError:
            print "INDEX ERROR"
            return "ERR"
            
    #align the remaning letters from the last anchor to the last remaining letter
    if(align(j_word, e_word)==-1):
        print "ERROR4"
        return "ERR"

        
    #ouput tuple format
    tuple_align=[]
    for i in range(len(final_j_word)):
		pair = (final_e_word[i],final_j_word[i])
		tuple_align.append(pair)
		

    #your final answer!
    #print final_j_word
    #print final_e_word
    #print tuple_align
    if(verbose):
    	print tuple_align

    return tuple_align
 
#self explanatory
def find_anchor(j_word, e_word, anchor_e, from_index=0):
    for j_phone in j_word:
        if (j_word.index(j_phone) >= from_index):
            if(anchor_e[0] == j_phone[0]):
                return j_word.index(j_phone)

    return -1


def find_non_matching_anchor(j_word, e_word, anchor_e,from_index=0):
    global anchor
    global prev_e_phone
    
    for j_phone in j_word:
        
        if((j_phone[0] in anchor) and j_word.index(j_phone)>=from_index):
            return j_word.index(j_phone)

    return -1


#same as find_anchor but it skips the first letter
#because it determine in the main loop that
#the first letter would be a duplicate anchor
def skip_first_find_anchor(j_word, e_word, anchor_e):
    skip_first_j_word = j_word[1:]
    
    for j_phone in skip_first_j_word:
        if(anchor_e[0] == j_phone[0]):
            return (skip_first_j_word.index(j_phone)+1)

    return -1

def align(prefix_j, prefix_e):
    global final_j_word
    counter = 0
    #keep trying to align the phonemes/syllables until their lengths are equal
    while (len(prefix_j) != len(prefix_e)):

        while(len(prefix_j) < len(prefix_e)):
            
            if(counter > 100):
                return -1
            prefix_j = split_one(prefix_j)
            counter = counter + 1
                        
        while(len(prefix_j) > len(prefix_e)):
            
            if(counter > 100):
                return -1
            prefix_j = merge_one(prefix_j)
            if (prefix_j == -1):
                return -1
            counter = counter + 1
        
            
    counter = 0
    final_j_word.extend(prefix_j)

    return 0

#split the first splittable syllable (exclude three letter syllabes like tsu)
def split_one(prefix_j):
    for j_phone in prefix_j:
        if(len(j_phone) == 2):
            temp1 = j_phone[0]
            temp2 = j_phone[1]

            #make sure the split is within array bounds
            #and attach the split to the first part of the prefix...
            if(prefix_j.index(j_phone) > 0):
                temp_pre = prefix_j[0:(prefix_j.index(j_phone)-1)] + [temp1]+[temp2]
            else:
                temp_pre = [temp1]+[temp2]

            #...then attach the first part w/ new split with the second part of the prefix
            prefix_j = temp_pre + prefix_j[(prefix_j.index(j_phone)+1):]
            return prefix_j
    return prefix_j


#merges two japanese syllables
def merge_one(prefix_j):

    #initialize variables
    lowest_cost = 999
    lowest_cost_index = 0

    #reverse japanese prefix list
    #prefix_j.reverse()

    #reversed list#!/usr/bin/env python
    import sys
    import math
    import os

    #How to use:

    #python align.py "JAPANESE TRANSCRIPTION" "ENGLISH TRANSCRIPTION"
    #(e.g., python align.py "A I SU" "AY S")
    #outputs final japanese alignment (e.g., AI SU)


    def init(japanese,english,verbose=True):
        global final_j_word #final output variable
        global anchor
        global prev_e_phone

        #first argument is the Japanese transcription
        #second argument is the English transcription
        #japanese = sys.argv[1]
        #english = sys.argv[2]
        #print japanese
        #print english


        #anchor letters (added J as an anchor)
        anchor = ["K", "G", "S", "Z", "T", "D", "N", "B", "H", "P", "M", "R","W", "L", "J"] #is L an anchor character

        #initialize lists
        j_word = []
        e_word = []
        word = ""

        #Take the string from the command line and put
        #it in a list format where each syllable/phoneme
        #is an element in the japanese/english lists
        for j_char in japanese:
            if(j_char == " "):
                j_word.append(word.strip())

                word=""
            word = word + j_char

        j_word.append(word.strip())

        #reinitialize variable for enlgish parsing
        word = ""

        #same structure/purpose as the japanese for loop above
        for e_char in english:
            if(e_char == " "):
                e_word.append(word.strip())

                word=""
            word = word + e_char

        e_word.append(word.strip())
        final_e_word = e_word
        #initialize variables
        final_j_word =[]
        prev_j_index = 0
        prev_e_phone = 0
        j_index = -1  # initialize to -1 1) because it is invald 2) bc the find_anchor 
        # will always start loking at j_index+1
        e_word_orig = e_word

        #go through each phoneme in the (remaining part) of the english word
        for e_phone in e_word:
            #find the anchor 
            try:
                if (e_phone[0] == "5"):
                    print "NO!"
            except:
                print e_phone

            if((e_phone[0] in anchor) or e_phone=="AXR"):

                #convert the AXR to R
                if(e_phone == "AXR"):
                    anchor_e = "R"

                #conert L to R
                elif(e_phone[0] == "L"):
                    anchor_e = "R"+ e_phone[1:]

                else:
                    anchor_e = e_phone

                #used to make sure it doesn't align an anchor
                #with another anchor that was previously aligned
                prev_j_index  = j_index

                #find the anchor in the japanese word that corresponds
                #to the english word
                j_index = find_anchor(j_word, e_word, anchor_e, prev_j_index+1)

                #make sure you don't duplicate the finding the same anchor 
                # if(prev_j_index == 1 and j_index == 0 and e_phone[0]==prev_e_phone):
                #    j_index = skip_first_find_anchor(j_word,e_word, anchor_e)

                #if you do find an anchor that corresponds to the english anchor....
                if(j_index != -1):

                    #get the prefix contained by the boundary anchors
                    prefix_e = e_word[0:e_word.index(e_phone)]
                    prefix_j = j_word[0:j_index]

                    #determine the remaining part of the english/japanese word
                    e_word = e_word[e_word.index(e_phone):]
                    j_word = j_word[j_index:]


                    #align the syllables/phonems properly!
                    if(align(prefix_j, prefix_e)==-1):
                        print "ERROR1"
                        return "ERR" 

                    #reinitialize status variable
                    skip_first_letter = 0

                #find any japanese anchor if you cant find a matching english/japanese anchor
                else:

                    j_index = find_non_matching_anchor(j_word, e_word, anchor_e, prev_j_index+1)

                    #alignment MUST ALWAYS start with the first japanese syllable
                    if(j_index > 0 and e_word_orig.index(e_phone)==0):
                        print "ERROR2"
                        return "ERR"


                    #get the prefix contained by the boundary anchors
                    prefix_e = e_word[0:e_word.index(e_phone)]
                    prefix_j = j_word[0:j_index]

                    #determine the remaining part of the english/japanese word
                    e_word = e_word[e_word.index(e_phone):]
                    j_word = j_word[j_index:]

                    #print "prefix_e:%s"%prefix_e
                    #print "prefix_j:%s"%prefix_j
                    #align the syllables/phonems properly!
                    if(align(prefix_j, prefix_e)==-1):
                        print "ERROR3"
                        return "ERR"

                    #reinitialize status variable
                    skip_first_letter = 0
                prev_e_phone = e_phone[0]
        #align the remaning letters from the last anchor to the last remaining letter
        if(align(j_word, e_word)==-1):
            print "ERROR4"
            return "ERR"


        #ouput tuple format
        tuple_align=[]
        for i in range(len(final_j_word)):
    		pair = (final_e_word[i],final_j_word[i])
    		tuple_align.append(pair)


        #your final answer!
        #print final_j_word
        #print final_e_word
        #print tuple_align
        if(verbose):
        	print tuple_align

        return tuple_align

    #self explanatory
    def find_anchor(j_word, e_word, anchor_e, from_index=0):
        for j_phone in j_word:
            if (j_word.index(j_phone) >= from_index):
                if(anchor_e[0] == str.upper(j_phone[0])):
                    return j_word.index(j_phone)

        return -1


    def find_non_matching_anchor(j_word, e_word, anchor_e,from_index=0):
        global anchor
        global prev_e_phone

        for j_phone in j_word:

            if((str.upper(j_phone[0]) in anchor) and j_word.index(j_phone)>=from_index):
                return j_word.index(j_phone)

        return -1


    #same as find_anchor but it skips the first letter
    #because it determine in the main loop that
    #the first letter would be a duplicate anchor
    def skip_first_find_anchor(j_word, e_word, anchor_e):
        skip_first_j_word = j_word[1:]

        for j_phone in skip_first_j_word:
            if(anchor_e[0] == j_phone[0]):
                return (skip_first_j_word.index(j_phone)+1)

        return -1

    def align(prefix_j, prefix_e):
        global final_j_word
        counter = 0
        #keep trying to align the phonemes/syllables until their lengths are equal
        while (len(prefix_j) != len(prefix_e)):

            while(len(prefix_j) < len(prefix_e)):

                if(counter > 100):
                    return -1
                prefix_j = split_one(prefix_j)
                counter = counter + 1

            while(len(prefix_j) > len(prefix_e)):

                if(counter > 100):
                    return -1
                prefix_j = merge_one(prefix_j)
                if (prefix_j == -1):
                    return -1
                counter = counter + 1


        counter = 0
        final_j_word.extend(prefix_j)

        return 0

    #split the first splittable syllable (exclude three letter syllabes like tsu)
    def split_one(prefix_j):
        for j_phone in prefix_j:
            if(len(j_phone) == 2):
                temp1 = j_phone[0]
                temp2 = j_phone[1]

                #make sure the split is within array bounds
                #and attach the split to the first part of the prefix...
                if(prefix_j.index(j_phone) > 0):
                    temp_pre = prefix_j[0:(prefix_j.index(j_phone)-1)] + [temp1]+[temp2]
                else:
                    temp_pre = [temp1]+[temp2]

                #...then attach the first part w/ new split with the second part of the prefix
                prefix_j = temp_pre + prefix_j[(prefix_j.index(j_phone)+1):]
                return prefix_j
        return prefix_j


    #merges two japanese syllables
    def merge_one(prefix_j):

        #initialize variables
        lowest_cost = 999
        lowest_cost_index = 0

        #reverse japanese prefix list
        #prefix_j.reverse()

        #reversed list
        #find the earliest syllable that is the smallest to merge with
        for j_phone in prefix_j:
            if(prefix_j.index(j_phone) > 0):
                cost = merge_cost(j_phone, prefix_j[(prefix_j.index(j_phone)-1)])
                if(cost < lowest_cost):
                    lowest_cost = cost
                    lowest_cost_index = (prefix_j.index(j_phone)-1)

        #reverse the prefix list back to its original form
        #prefix_j.reverse()

        #merge syllables
        try:
            combined = str(prefix_j[lowest_cost_index])+str(prefix_j[lowest_cost_index+1])
        except IndexError:
            print "ERROR"
            return -1

        #add the merged syllable back to the first part of the list
        temp =prefix_j[0:lowest_cost_index]+[combined]

        #add the first part of the list w/ newly merged syllable to the second part of the list
        prefix_j = temp + prefix_j[lowest_cost_index+2:]

        return prefix_j


    def merge_cost(a,b):
        return len(a)+len(b)


    def main():
            #first argument is the Japanese transcription
        #second argument is the English transcription
        japanese = sys.argv[1]
        english = sys.argv[2]
        init(japanese,english)

    if __name__ == '__main__':
         main()
    
    #find the earliest syllable that is the smallest to merge with
    for j_phone in prefix_j:
        if(prefix_j.index(j_phone) > 0):
            cost = merge_cost(j_phone, prefix_j[(prefix_j.index(j_phone)-1)])
            if(cost < lowest_cost):
                lowest_cost = cost
                lowest_cost_index = (prefix_j.index(j_phone)-1)

    #reverse the prefix list back to its original form
    #prefix_j.reverse()

    #merge syllables
    try:
        combined = str(prefix_j[lowest_cost_index])+str(prefix_j[lowest_cost_index+1])
    except IndexError:
        print "ERROR"
        return -1

    #add the merged syllable back to the first part of the list
    temp =prefix_j[0:lowest_cost_index]+[combined]

    #add the first part of the list w/ newly merged syllable to the second part of the list
    prefix_j = temp + prefix_j[lowest_cost_index+2:]
    
    return prefix_j


def merge_cost(a,b):
    return len(a)+len(b)
 
	
def main():
        #first argument is the Japanese transcription
    #second argument is the English transcription
    japanese = sys.argv[1]
    english = sys.argv[2]
    init(japanese,english)

if __name__ == '__main__':
     main()
