#!/usr/bin/env python
import sys
import math
import os
import ngramer
import string

#How to use:

#-------
# ANCHOR ALIGNMENT
#

# English Phoneme Start -> Japanese Phoneme
FULL_ANCHORS = {
    "AXR":["R"],
    "JH":["Z","D","G"],
    "CH":["T"]
}

CONS_ANCHORS = {
    "B":["B"],
    "D":["D"],
    "F":["H"],
    "G":["G"],
    "H":["H"],
    "J":["S"],
    "K":["K"],
    "L":["R"],
    "M":["M"],
    "N":["N","n"],
    "P":["P"],
    "Q":["K"],
    "R":["R"],
    "S":["S"],
    "T":["T"],
    "V":["B"],
    "W":["W"],
    "Z":["Z"]
}

ALL_J_ANCHORS = [x for x in [v for v in CONS_ANCHORS.values()]]

# Returns (e,j) or False
def get_anchor(english):
    global FULL_ANCHORS
    global CONS_ANCHORS
    
    if (FULL_ANCHORS.has_key(english)):
        return (english, FULL_ANCHORS[english])
    if (CONS_ANCHORS.has_key(english[0])):
        return (english[0], CONS_ANCHORS[english[0]])
    return False

# self explanatory
# anchors is the (e,j) anchor pair returned from get_anchor
def find_anchor(j_word, anchors, from_index=0):
    for i in range(from_index,len(j_word)):
        if(j_word[i][0] in anchors[1]):
            return i
    return -1

#python align.py "JAPANESE TRANSCRIPTION" "ENGLISH TRANSCRIPTION"
#(e.g., python align.py "A I SU" "AY S")
#outputs final japanese alignment (e.g., AI SU)

def anchor(japanese,english,verbose=False):
    try:
        # Turn them into arrays
        eng = english.split(" ")
        jap = japanese.split(" ")

        eng_out = []
        jap_out = []
    
        j_past = -1
        e_past = -1
        j_present = -1
        e_present = -1
        # main loop to look for 
        for i in range(len(eng)):
            anchors = get_anchor(eng[i])
    #        print "Anchor at %i: %s" % (i, str(anchors))
            if(anchors):
                e_present = i
                j_present = find_anchor(jap, anchors, j_past+1)
                if j_present == -1:
                    continue # couldn't find one. skip to next english anchor

     #           print "EPast: %i EPresent %i JPast %i JPresent %i " % (e_past, e_present, j_past, j_present)
            
                # Append from past to present
                e_from = e_past
                j_from = j_past
                if e_from < 0:
                    e_from = 0
                if j_from < 0:
                    j_from = 0
                
                e_chunk = eng[e_from:e_present]
                j_chunk = jap[j_from:j_present]
            
    #            print "EChunk %s JChunk %s" % (e_chunk, j_chunk)
            
                if (not ((e_chunk == []) and (j_chunk == []))):
                    eng_out.append(e_chunk)
                    jap_out.append(j_chunk)
            
                e_past = e_present
                j_past = j_present
    
        eng_out.append(eng[e_past:])
        jap_out.append(jap[j_past:])
    
        # Test the results
        enout = ''
        for chunk in eng_out:
            enout = enout + ' ' + ' '.join(chunk)
        enout = enout.lstrip(' ')
        if (enout != english):
            return False
    except:
        return False
        
    return jap_out, eng_out
            
def align_words(japanese,english,verbose=False):
    anchored = anchor(japanese, english)
    if (anchored == False):
        return "ERR"
    
    anchored_japanese = anchored[0]
    anchored_english = anchored[1]
    japanese_out = []
    english_out = english.split(' ')
    
    for i in range(len(anchored_japanese)):

        j_chunk = anchored_japanese[i]
        e_chunk = anchored_english[i]
                
        aligned = align(j_chunk, e_chunk)
        if (aligned == False):
            return "ERR"
        japanese_out.extend(aligned[0])    
    return japanese_out, english_out

def align(prefix_j, prefix_e):
    counter = 0
    #keep trying to align the phonemes/syllables until their lengths are equal
    while (len(prefix_j) != len(prefix_e)):
        while(len(prefix_j) < len(prefix_e)):
            
            if(counter > 100):
                return False
            prefix_j = split_one(prefix_j)
            counter = counter + 1
                        
        while(len(prefix_j) > len(prefix_e)):
            
            if(counter > 100):
                return -1
            prefix_j = merge_one(prefix_j)
            if (prefix_j == -1):
                return False
            counter = counter + 1
        
    return prefix_j, prefix_e

#split the first splittable syllable (exclude three letter syllabes like tsu)
def split_one(prefix_j):
    for j_phone in prefix_j:
        if(len(j_phone) == 2):
            temp1 = j_phone[0]
            temp2 = j_phone[1]

            idx = prefix_j.index(j_phone)
            toreturn = prefix_j[0:idx] + [temp1, temp2] + prefix_j[idx+1:]
            return toreturn
    return prefix_j


#merges two japanese syllables
def merge_one(prefix_j, verbose=False):

    #initialize variables
    lowest_cost = 999
    lowest_cost_index = 0
    
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
        if verbose:
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
    japanese = "A HU RI KA - n SU"
    english = "AE F R IX K AA N Z"   
    
    print "E,J = %s,%s" % (english, japanese)
    
    # print "Anchored:"
    # print anchor(japanese, english)

    aligned = align_words(japanese,english,True)
    print aligned

if __name__ == '__main__':
     main()
