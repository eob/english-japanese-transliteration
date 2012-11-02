//
//  NSString+Romanji.m
//  JapanExtract
//
//  Created by eob on 4/17/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "NSString+Romanji.h"

@implementation NSString (Romanji)

+(NSDictionary *)getMappingDictionary {
	
	NSDictionary *dict = [[NSDictionary alloc] initWithObjectsAndKeys:
		KATAKANA_A, @"A",
		KATAKANA_I, @"I",
		KATAKANA_U, @"U",
		KATAKANA_E, @"E",
		KATAKANA_O, @"O",
	
		KATAKANA_A_SM, @"a",
		KATAKANA_I_SM,@"i",
		KATAKANA_U_SM,@"u",
		KATAKANA_E_SM,@"e",
		KATAKANA_O_SM,@"o",
		
		KATAKANA_KA,@"KA",
		KATAKANA_KI,@"KI",
		KATAKANA_KU,@"KU",
		KATAKANA_KE,@"KE",
		KATAKANA_KO,@"KO",
			
		KATAKANA_GA,@"GA",
		KATAKANA_GI,@"GI",
		KATAKANA_GU,@"GU",
		KATAKANA_GE,@"GE",
		KATAKANA_GO,@"GO",
	
		KATAKANA_SA,@"SA",
		KATAKANA_SI,@"SI",
		KATAKANA_SU,@"SU",
		KATAKANA_SE,@"SE",
		KATAKANA_SO,@"SO",

		KATAKANA_ZA,@"ZA",	
		KATAKANA_ZI,@"ZI",
		KATAKANA_ZU,@"ZU",
		KATAKANA_ZE,@"ZE",
		KATAKANA_ZO,@"ZO",

		KATAKANA_TA,@"TA",
		KATAKANA_TI,@"TI",
		KATAKANA_TU,@"TU",
		KATAKANA_TE,@"TE",
		KATAKANA_TO,@"TO",

		KATAKANA_TU_SM,@".",
		
		KATAKANA_DA,@"DA",
		KATAKANA_DI,@"DI",	
		KATAKANA_DU,@"DU",
		KATAKANA_DE,@"DE",
		KATAKANA_DO,@"DO",

		KATAKANA_NA,@"NA",
		KATAKANA_NI,@"NI",
		KATAKANA_NU,@"NU",
		KATAKANA_NE,@"NE",
		KATAKANA_NO,@"NO",

		KATAKANA_HA,@"HA",
		KATAKANA_HI,@"HI",
		KATAKANA_HU,@"HU",
		KATAKANA_HE,@"HE",
		KATAKANA_HO,@"HO",

		KATAKANA_BA,@"BA",
		KATAKANA_BI,@"BI",
		KATAKANA_BU,@"BU",
		KATAKANA_BE,@"BE",
		KATAKANA_BO,@"BO",

		KATAKANA_PA,@"PA",
		KATAKANA_PI,@"PI",
		KATAKANA_PU,@"PU",
		KATAKANA_PE,@"PE",
		KATAKANA_PO,@"PO",

		KATAKANA_MA,@"MA",
		KATAKANA_MI,@"MI",
		KATAKANA_MU,@"MU",
		KATAKANA_ME,@"ME",
		KATAKANA_MO,@"MO",

		KATAKANA_YA,@"YA",
		KATAKANA_YU,@"YU",
		KATAKANA_YO,@"YO",

		KATAKANA_YA_SM,@"ya",
		KATAKANA_YU_SM,@"yu",
		KATAKANA_YO_SM,@"yo",

		KATAKANA_RA,@"RA",
		KATAKANA_RI,@"RI",
		KATAKANA_RU,@"RU",
		KATAKANA_RE,@"RE",
		KATAKANA_RO,@"RO",
	
		KATAKANA_WA,@"WA",
		KATAKANA_WA_SM,@"wa",
		KATAKANA_WO,@"WO",
	
		KATAKANA_N,@"n",
	
		KATAKANA_KA_SM,@"ka",
		KATAKANA_KE_SM,@"ke",
	
		KATAKANA_VA,@"VA",
		KATAKANA_VU,@"VU",
		KATAKANA_DOT,@"*",
		KATAKANA_DASH,@"-",
		nil];
	return [dict autorelease];
}

/*! Returns a tokenized version of the string */
- (NSString *)toRomanjiTokens {
	return [self toRomanjiTokens:@" " romanjiSpecification:EOB_ROMANJI_NLP];
}

/*! Returns a tokenized version of the string */
- (NSString *)toRomanjiTokens:(NSString *)tokenDivider romanjiSpecification:(EOBRomanjiSpecification)romanjiSpecification {
	NSMutableString *outputString = [[NSMutableString alloc] initWithCapacity:[self length]];
	
	for (int i=0; i<[self length]; i++) {
		// Insert the token divider if we're in the middle of the string (but not starting)
		if (i != 0) {
			[outputString appendString:tokenDivider];
		}
		NSString *nextPart = [self nextTokenAtIndex:i romanjiSpecification:romanjiSpecification];

		// Now we have to decide how to handle this next part. append? or alter an existing character?
//		if ([nextPart isEqual:@"ya"]) {
//			[outputString appendString:[outputString chiisaiYaLastVowel]];	
//		}
//		else if ([nextPart isEqual:@"yu"]) {
//			[outputString appendString:[outputString chiisaiYuLastVowel]];	
//		}
//		else if ([nextPart isEqual:@"yo"]) {
//			[outputString appendString:[outputString chiisaiYoLastVowel]];
//		}
//		else if ([nextPart isEqual:@"-"]) {
//			[outputString appendString:[outputString extendLastVowel]];
//		}
//		else {
			// Just append it.
			[outputString appendString:nextPart];
//		}
	}
	
	// Make an imutable copy of the string in progress, free memory, and return 
	NSString *retString = [NSString stringWithString:outputString];
	[outputString release];
	return retString;
}

//- (NSString *)extendLastVowel {
//	return nil;
//}
//
//- (NSString *)chiisaiYoLastVowel {
//	return nil;
//}
//
//- (NSString *)chiisaiYuLastVowel {
//	return nil;
//}
//
//- (NSString *)chiisaiYaLastVowel {
//	return nil;
//}

- (NSString *)nextTokenAtIndex:(int)i romanjiSpecification:(EOBRomanjiSpecification)romanjiSpecification {
	unichar curChar = [self characterAtIndex:i];

	switch(curChar) {
		case KATAKANA_A:
			return @"A";
			break;
		case KATAKANA_I:
			return @"I";
			break;
		case KATAKANA_U:
			return @"U";
			break;
		case KATAKANA_E:
			return @"E";
			break;
		case KATAKANA_O:
			return @"O";
			break;
			
		case KATAKANA_A_SM:
			return @"a";
			break;
		case KATAKANA_I_SM:
			return @"i";
			break;
		case KATAKANA_U_SM:
			return @"u";
			break;
		case KATAKANA_E_SM:
			return @"e";
			break;
		case KATAKANA_O_SM:
			return @"o";
			break;			
			
		case KATAKANA_KA:
			return @"K A";
			break;
		case KATAKANA_KI:
			return @"K I";
			break;
		case KATAKANA_KU:
			return @"K U";
			break;
		case KATAKANA_KE:
			return @"K E";
			break;
		case KATAKANA_KO:
			return @"K O";
			break;
			
		case KATAKANA_GA:
			return @"G A";
			break;
		case KATAKANA_GI:
			return @"G I";
			break;
		case KATAKANA_GU:
			return @"G U";
			break;
		case KATAKANA_GE:
			return @"G E";
			break;
		case KATAKANA_GO:
			return @"G O";
			break;

		case KATAKANA_SA:
			return @"S A";
			break;
		case KATAKANA_SI:
			return @"S I";
			break;
		case KATAKANA_SU:
			return @"S U";
			break;
		case KATAKANA_SE:
			return @"S E";
			break;
		case KATAKANA_SO:
			return @"S O";
			break;

		case KATAKANA_ZA:
			return @"Z A";
			break;
		case KATAKANA_ZI:
			return @"Z I";
			break;
		case KATAKANA_ZU:
			return @"Z U";
			break;
		case KATAKANA_ZE:
			return @"Z E";
			break;
		case KATAKANA_ZO:
			return @"Z O";
			break;
			
		case KATAKANA_TA:
			return @"T A";
			break;
		case KATAKANA_TI:
			return @"T I";
			break;
		case KATAKANA_TU:
			return @"T U";
			break;
		case KATAKANA_TE:
			return @"T E";
			break;
		case KATAKANA_TO:
			return @"T O";
			break;
			
		case KATAKANA_TU_SM:
			return @".";
			break;
		
		case KATAKANA_DA:
			return @"D A";
			break;
		case KATAKANA_DI:
			return @"D I";
			break;
		case KATAKANA_DU:
			return @"D U";
			break;
		case KATAKANA_DE:
			return @"D E";
			break;
		case KATAKANA_DO:
			return @"D O";
			break;

		case KATAKANA_NA:
			return @"N A";
			break;
		case KATAKANA_NI:
			return @"N I";
			break;
		case KATAKANA_NU:
			return @"N U";
			break;
		case KATAKANA_NE:
			return @"N E";
			break;
		case KATAKANA_NO:
			return @"N O";
			break;
			
		case KATAKANA_HA:
			return @"H A";
			break;
		case KATAKANA_HI:
			return @"H I";
			break;
		case KATAKANA_HU:
			return @"H U";
			break;
		case KATAKANA_HE:
			return @"H E";
			break;
		case KATAKANA_HO:
			return @"H O";
			break;
			
		case KATAKANA_BA:
			return @"B A";
			break;
		case KATAKANA_BI:
			return @"B I";
			break;
		case KATAKANA_BU:
			return @"B U";
			break;
		case KATAKANA_BE:
			return @"B E";
			break;
		case KATAKANA_BO:
			return @"B O";
			break;
			
		case KATAKANA_PA:
			return @"P A";
			break;
		case KATAKANA_PI:
			return @"P I";
			break;
		case KATAKANA_PU:
			return @"P U";
			break;
		case KATAKANA_PE:
			return @"P E";
			break;
		case KATAKANA_PO:
			return @"P O";
			break;

		case KATAKANA_MA:
			return @"M A";
			break;
		case KATAKANA_MI:
			return @"M I";
			break;
		case KATAKANA_MU:
			return @"M U";
			break;
		case KATAKANA_ME:
			return @"M E";
			break;
		case KATAKANA_MO:
			return @"M O";
			break;
			
		case KATAKANA_YA:
			return @"Y A";
			break;
		case KATAKANA_YU:
			return @"Y U";
			break;
		case KATAKANA_YO:
			return @"Y O";
			break;
			
		case KATAKANA_YA_SM:
			return @"ya";
			break;
		case KATAKANA_YU_SM:
			return @"yu";
			break;
		case KATAKANA_YO_SM:
			return @"yo";
			break;
			
		case KATAKANA_RA:
			return @"R A";
			break;
		case KATAKANA_RI:
			return @"R I";
			break;
		case KATAKANA_RU:
			return @"R U";
			break;
		case KATAKANA_RE:
			return @"R E";
			break;
		case KATAKANA_RO:
			return @"R O";
			break;

		case KATAKANA_WA:
			return @"W A";
			break;
		case KATAKANA_WA_SM:
			return @"w a";
			break;
		case KATAKANA_WO:
			return @"W O";
			break;
			
		case KATAKANA_N:
			return @"n";
			break;
			
		case KATAKANA_KA_SM:
			return @"k a";
			break;
		case KATAKANA_KE_SM:
			return @"k e";
			break;
		
		case KATAKANA_VA:
			return @"V A";
			break;
		case KATAKANA_VU:
			return @"V U";
			break;
			
		case KATAKANA_DOT:
			return @"*";
			break;
		case KATAKANA_DASH:
			return @"-";
			break;
			
		default:
			return @"?";
			break;
	}
}



@end
