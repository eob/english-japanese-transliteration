//
//  JDictParser.m
//  JapanExtract
//
//  Created by eob on 3/26/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "JDictParser.h"
#import "JPEntry.h"

@implementation JDictParser

-(id)initWithInput:(NSString *)input output:(NSString *)output {
	if (self = [super init]) {
		inputFileName = [input retain];
		outputFileName = [output retain];
		outputData = [[NSMutableData alloc] init];
	}
	return self;
}

- (void)parse {
    BOOL success;
    NSURL *xmlURL = [NSURL fileURLWithPath:inputFileName];
	
	NSLog(@"URL: %@", xmlURL);
	
    if (parser) // addressParser is an NSXMLParser instance variable
        [parser release];
	
    parser = [[NSXMLParser alloc] initWithContentsOfURL:xmlURL];
    [parser setDelegate:self];
    [parser setShouldResolveExternalEntities:YES];
    success = [parser parse]; // return value not used
	
	if (!success) {
		NSLog(@"Error!");
	}
	
	// if not successful, delegate is informed of error
}


- (void)parser:(NSXMLParser *)parser didStartElement:(NSString *)elementName namespaceURI:(NSString *)namespaceURI qualifiedName:(NSString *)qName attributes:(NSDictionary *)attributeDict {
    if ( [elementName isEqualToString:@"entry"]) {
		// We began a new entry
        if (currentEntry)
			[currentEntry release];
		currentEntry = [[JPEntry alloc] init];
	}
	else if ( [elementName isEqualToString:@"reb"] ) {
		if (currentValue) 
			[currentValue release];
		currentValue = [[NSMutableString alloc] init];
	}
	else if ( [elementName isEqualToString:@"gloss"] ) {
		if (currentValue) 
			[currentValue release];
		currentValue = [[NSMutableString alloc] init];		
	}
	else if ( [elementName isEqualToString:@"keb"] ) {
		if (currentValue) 
			[currentValue release];
		currentValue = [[NSMutableString alloc] init];		
	}	
}

- (void)parser:(NSXMLParser *)parser foundCharacters:(NSString *)string {
    if (currentValue) {
		[currentValue appendString:string];
    }	
}

- (void)parser:(NSXMLParser *)parser didEndElement:(NSString *)elementName namespaceURI:(NSString *)namespaceURI qualifiedName:(NSString *)qName {
    if ( [elementName isEqualToString:@"entry"]) {
		if ([currentEntry isDesirable]) {
			[currentEntry sendToData:outputData];
			[currentEntry release];
			currentEntry = nil;
		}
	}
	else if ( [elementName isEqualToString:@"reb"] ) {
		[currentEntry.kana addObject:currentValue];
		[currentValue release];
		currentValue = nil;
	}
	else if ( [elementName isEqualToString:@"gloss"] ) {
		[currentEntry.english addObject:currentValue];
		[currentValue release];
		currentValue = nil;
	}
	else if ( [elementName isEqualToString:@"keb"] ) {
		[currentEntry.kanji addObject:currentValue];
		[currentValue release];
		currentValue = nil;
	}
}

- (void)parserDidEndDocument:(NSXMLParser *)parser {
	[outputData writeToFile:outputFileName atomically:YES];
}

- (void)parser:(NSXMLParser *)parser parseErrorOccurred:(NSError *)parseError {
	
    NSLog(@"Error %i, Description: %@, Line: %i, Column: %i", [parseError code],
									 [[parser parserError] localizedDescription], [parser lineNumber],
									 [parser columnNumber]);	
}

-(void) dealloc {
	[inputFileName release];
	[outputFileName release];
	[outputData release];
	[super dealloc];
}


@end
