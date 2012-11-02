Character Classes
------------------

VOWELS     := AIUEO           # These are pronounced as in the sentence "Ah, we soon get old"
Y-VOWELS   := äüö             # These are pronounced like "shIA, adIEU, kYOto"
VOWELS_SM  := aiueo 
VOWEL_LONG := ÂÎÛÊÔ           # Represents a continuation of the same prior vowel sound

CONSONANTS := KGSZTDNBHPMRW   # Note: W is the odd one out, behaving slightly differently than the others
Y_CONS     := Y               # This can only pair with A, U, and O
NASAL_N    := n               # Note: This is a syllable by itself, not combined with a vowel.
PAUSE      := .               # Called a "Chiisai tsu" (small tsu)

-----

The following combinations are allowed to exist in words:

VOWELS                        # A I U E O
CONSONANTS + VOWELS           # KA KI KU KE KO
Y_CONS + {A U O}              # YA YU YO
CONSONANTS + Y-VOWELS         # Kä Kü Kö
Any of the above four, followed by the appropriate VOWEL_LONG.

The PAUSE can only appear before one of the CONSONANTS and can not start a word
The NASAL_N can appear anywhere except the start of a word

-----

Let's forget about the VOWELS_SM right now. They are actually a modern invention used to try to mimic sounds not in the Japanese sound set.
This is actually a really hard problem. For example, "TU" in Japanese is actually pronounced "TSU". So TOOL (TUÛRU) is pronounced (TSU-RU). 
They use the VOWELS_SM set to add new sounds only in foreign languages.. so if you wrote TUÛRU instead as TOuÛRU then it would be pronounced
"TOO-RU" as we would hope (minus the +U at the end). The language is *really flexible* here because, after all, they're trying to import new
words.. so there are multiple correct ways to write down the sound.. which is why I think we should ignore any word that uses VOWELS_SM until
we have solved the problem for the other words first..

-----

Given the above representation.. I think we can:
	1) Represent the sounds of any Japanese word as well as Katakana can
	2) Split the word up into any size buckets and still be able to convert it back to katakana.
	    -> EG: フライドポテト,"fried potato" (French Fries),FURAIDOPOTETO
		-> ロシア,Russia,ROSIA
		-> ウーマン,Woman,UÛMAn
        -> ツール,tool,TUÛRU
		-> ツアー,tour,TUAÂ
		-> 

		