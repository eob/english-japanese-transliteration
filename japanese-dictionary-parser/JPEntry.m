//
//  Entry.m
//  JapanExtract
//
//  Created by eob on 3/26/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "JPEntry.h"


@implementation JPEntry

@synthesize kana, kanji, english;

-(id) init {
	if (self = [super init]) {
		kana = [[NSMutableArray alloc] init];
		kanji = [[NSMutableArray alloc] init];
		english = [[NSMutableArray alloc] init];
	}
	return self;
}

-(BOOL)isDesirable {
	return (
			([self isKanaOnly]) && 
			([self isOnlyKatakana]) &&
			([self isOnlyAZ]) &&
			(! [self containsParens]) &&
			(! [self containsTooManyWords]) &&
			(! [self isOnomontopea]) &&
			(! [self isAcronym])
	);
}

-(BOOL)isKanaOnly {
	return (([kana count] > 0) && ([english count] > 0) && ([kanji count] == 0));
}

-(BOOL)containsParens {
	if ([english count] > 0) {
		BOOL containsParens = NO;
		NSString *word = [english objectAtIndex:0];
		for (int i=0; i<[word length]; i++) {
			unichar letter = [word characterAtIndex:i];
			if ((letter == 0x0028) || (letter == 0x0029)) {
				containsParens = YES;
			}
		}
		
		if (containsParens) {
			NSLog(@"%@ -- contains parens", word);
		}
		
		return containsParens;
	}
	return false;	
}

-(BOOL)isOnomontopea {
	if ([kana count] > 0) {
		NSString *kotoba = [kana objectAtIndex:0];
		int l = [kotoba length];
		if ((l% 2) == 0) {
			// is even length word
			NSString *firstHalf = [kotoba substringToIndex:(l/2)];
			NSString *secondHalf = [kotoba substringFromIndex:(l/2)];
			if ([firstHalf isEqual:secondHalf]) {
				NSLog(@"%@ -- is onomontopea", kotoba);
				return YES;
			}
		}
	}
	return NO;	
}


-(BOOL)containsTooManyWords {
	if ([english count] > 0) {
		int whitespaces = 0;

		NSString *word = [english objectAtIndex:0];
		for (int i=0; i<[word length]; i++) {
			unichar letter = [word characterAtIndex:i];
			if (letter == 0x0020) {
				whitespaces++;
			}
		}
		
		if (whitespaces > 2) {
			NSLog(@"%@ -- Too much whitespace", word);
		}
		return (whitespaces > 2);
	}
	return false;
}

-(BOOL)isAcronym {
	if ([english count] > 0) {
		BOOL foundLowercase = NO;
		NSString *word = [english objectAtIndex:0];
		for (int i=0; i<[word length]; i++) {
			unichar letter = [word characterAtIndex:i];
			if ((letter >= 0x0061) && (letter <= 0x007A)) {
				foundLowercase = YES;
			}
		}

		if (! foundLowercase) {
			NSLog(@"%@ -- is an acronym", word);
		}
		
		return (! foundLowercase);
	}
	return false;	
}

/*
 * Checks if the first letter starts with Katakana
 * Katakana is Unicode 30A0 to 30FF
 */
-(BOOL)isOnlyKatakana {
	if ([kana count] > 0) {
		NSString *kotoba = [kana objectAtIndex:0];
		for (int i=0; i<[kotoba length]; i++) {
			unichar stroke = [kotoba characterAtIndex:i];
			if (!((stroke >= 0x30A0) && (stroke <= 0x30FF))) {
				return false;
			}
		}
	}
	return true;
}


/*
 * Checks if the first letter starts with Katakana
 * Katakana is Unicode 30A0 to 30FF
 */
-(BOOL)isOnlyAZ {
	if ([english count] > 0) {
		NSString *word = [english objectAtIndex:0];
		for (int i=0; i<[word length]; i++) {
			unichar stroke = [word characterAtIndex:i];
			if (!(
				  ((stroke >= 0x0041) && (stroke <= 0x005A)) || // A-Z
				  ((stroke >= 0x0061) && (stroke <= 0x007A)) || // a-z
				  (stroke == 0x0020) // space
				)) {
				return false;
			}
		}
	}
	return true;
}

-(void) sendToData:(NSMutableData *)data {
	for (NSString *e in english) {
		for (NSString *k in kana) {
			NSString *line = [NSString stringWithFormat:@"%@,%@,%@\n", e, k, [k toRomanjiTokens]];
			[data appendData:[line dataUsingEncoding:NSUnicodeStringEncoding]];
			break ; // Only do the first
		}
		break ; // only do the first
	}
}

-(NSString *)description {
	return [NSString stringWithFormat:@"Entry<%@, %@>", [english objectAtIndex:0], [kana objectAtIndex:0]];
}

-(void) dealloc {
	[kana release];
	[kanji release];
	[english release];
}

@end
