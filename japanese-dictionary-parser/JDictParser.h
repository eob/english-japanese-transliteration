//
//  JDictParser.h
//  JapanExtract
//
//  Created by eob on 3/26/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>

@class JPEntry;

@interface JDictParser : NSObject {
	JPEntry *currentEntry;
	NSMutableString *currentValue;
	NSXMLParser *parser;
	NSString *inputFileName;
	NSString *outputFileName;
	NSMutableData* outputData;
}

-(id)initWithInput:(NSString *)input output:(NSString *)output;

- (void)parse;

@end
