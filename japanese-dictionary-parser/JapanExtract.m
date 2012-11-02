#import <Foundation/Foundation.h>
#import "JPEntry.h"
#import "JDictParser.h"
#import "NSString+Romanji.h"

int main (int argc, const char * argv[]) {
    NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
	
	JDictParser *parser = [[JDictParser alloc] initWithInput:@"/Users/eob/JMdict_e" 
													  output:@"/Users/eob/JAPAN_OUT.txt"];
	
	[parser parse];
	
	[pool drain];
    return 0;
}
