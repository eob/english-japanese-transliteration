//
//  Entry.h
//  JapanExtract
//
//  Created by eob on 3/26/09.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface JPEntry : NSObject {
	NSMutableArray *kana;
	NSMutableArray *kanji;
	NSMutableArray *english;
}

@property (nonatomic, retain) NSMutableArray *kana;
@property (nonatomic, retain) NSMutableArray *kanji;
@property (nonatomic, retain) NSMutableArray *english;

-(BOOL) isDesirable;
-(void) sendToData:(NSMutableData *)data;

@end
