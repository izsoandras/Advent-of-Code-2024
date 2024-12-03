////////////////////////////////////////////////////////////////////////////////////////////////////
// Solution for day 1 of advent of code 2024
// Task: for each line check if numbers are only increasing or decreasing, with difference of max 3
// /////////////////////////////////////////////////////////////////////////////////////////////////
// Author: Andras Izso
////////////////////////////////////////////////////////////////////////////////////////////////////
// Edited with vim
////////////////////////////////////////////////////////////////////////////////////////////////////
#include <stdio.h>
#include <stdbool.h>
#include <ctype.h>

// States of input reader
typedef enum StateReading {
	InitRead = 0, 	// Begin new line=report
	InProgressRead,	// In the middle of report, but not number
	NumberRead,	// Currently reading number
	TillEndRead	// Bypassing to end, because error is detected
} StateReading;

// States of the input analyzer
typedef enum StateReport{
	InitReport = 0,	// Beginning of report, wait for new number
	IdleReport,	// One number already arrived, wait for second to determine increase or decrease
	IncreaseReport,	// Report is of increasing kind (judged by the first difference)
	DecreaseReport, // Report is of decreasing kind (judged by the first difference)
	ErrorReport	// Error detected in report
} StateReport;

// Different ways the level can change
typedef enum LevelChange{
	LevelIncrease = 0,	// Level increased
	LevelDecrease,		// Level decreased
	LevelChangeNOK		// Level changed in not safe way (change > 3 or 0)
} LevelChange;

// Convert character to integer.
// Character is not checked if it really is a number
// @param char c: character co convert
//
// @return: the number it represents
int ctoi(char c){
	return c - '0';
}

// Determine the type of the level change
// @param unsigned int prevLevel: value of previous level
// @param unsigned int currLevel: value of current level
LevelChange checkLevelChange(unsigned int prevLevel, unsigned int currLevel){
	// Calculate difference
	long int diff = (long int)currLevel - (long int)prevLevel;

	// If difference is 0 or greater than 3, the change is not safe
	if(diff == 0 || diff < -3 || diff > 3){
		return LevelChangeNOK;
	}else if(diff > 0){
		// If change is positive: increase
		return LevelIncrease;
	}else{
		// If change is negative: decrease
		return LevelDecrease;
	}
}

// Main function of program
// 	Read input file
//	Analyze the input, running the two state machines
//	Display results
int main(int argc, char* argv[]){
	// Create default input name
	char* fileName = "input";
	// Damping value for second part of the task
	unsigned int dampingLevel = 0;
	// If input arguments are given, use the first as input file name
	// If multiple are given, give warning
	if(argc > 1){
		fileName = argv[1];
		if(argc > 2){
			// If present: use 2nd argument as damping
			// NO ERROR HANDLING!
			damping = atoi(argv[2]);
			if(damping == 0)
				printf("Warning! 0 damping is in use (if that is intented, ignore this)\n");
			if(argc > 3)
				printf("Too many input arguments, considering only the first 2\n");
		}
	}else{
		printf("Using default input file\n");
	}

	// Open file for reading, signal if not found
	FILE* inputFile = fopen(fileName,"r");
	if(inputFile == NULL){
		printf("Input file not found: %s\n", fileName);
		return 0;
	}
	
	// State machine variables
	StateReading readerState, readerNextState = InitRead;
	StateReport analyzerState, analyzerNextState = InitReport;
	char inChar = ' ';
	unsigned int inNum, prevInNum = 0;
	// Signals between state machines
	bool newNumFlag, endReportFlag, reportErrorFlag  = false;
	// Additional variables to track
	LevelChange levelChangeStatus = LevelChangeNOK;
	unsigned int reportCounter, validCounter, badLevelCount = 0;

	// Iterate through the file character by character
	while((inChar = getc(inputFile)) != EOF){
		// Run reader state machine
		switch(readerState){
			case InitRead:
				// Reset variables and flages
				inNum = 0;
				newNumFlag = false;
				endReportFlag = false;
				reportErrorFlag = false;
				
				if(isdigit(inChar)){
					// If input is digit: start recording new number and move to
					// number read state
					inNum += ctoi(inChar);
					readerNextState = NumberRead;
				}else{
					// If something else: move to in progress state
					readerNextState = InProgressRead;
				}// Error is not handled, because if there is one, it is from the previous report
				break;
			case InProgressRead:
				// Reset number variables
				inNum = 0;
				newNumFlag = false;

				if(reportErrorFlag){
					// If error is detected: read the line
					readerNextState = TillEndRead;
				}else if(isdigit(inChar)){
					// if input is digit: move to number state
					inNum += ctoi(inChar);	// no multiplication, because this is the first digit
					readerNextState = NumberRead;
				}else{
					// If something els is read: stay here
					readerNextState = InProgressRead;
				}
				break;
			case NumberRead:
				if(reportErrorFlag){
					// If error is detected: skip the line
					readerNextState = TillEndRead;
				}else if(isdigit(inChar)){
					// If digit is read: add to the number and stay here
					inNum = inNum*10 + ctoi(inChar);
					readerNextState = NumberRead;
				}else{
					// If something else is read: move, and signal
					newNumFlag = true;
					readerNextState = InProgressRead;
				}
				break;
			case TillEndRead:
				// If error is detected, just pass the whole line
				readerNextState = TillEndRead;
				break;
			default: 
				readerNextState = InitRead;
				break;
		}
		// Regardless of state: if new line is read, we go back to init state, and signal end of report
		if(inChar == '\n'){
			readerNextState = InitRead;
			endReportFlag = true;
		}
		
		// Run analyzer state machine
		switch(analyzerState){
			case InitReport:
				// wait for number, and move to next state if arrives
				if(newNumFlag){
					analyzerNextState = IdleReport;
				}else{
					analyzerNextState = InitReport;
				}
				break;
			case IdleReport:
				// If second number comes in: go to appropriate reading state
				if(newNumFlag){
					levelChangeStatus = checkLevelChange(prevInNum, inNum);
					switch(levelChangeStatus){
						case LevelIncrease:
							analyzerNextState = IncreaseReport;
							break;
						case LevelDecrease:
							analyzerNextState = DecreaseReport;
							break;
						default:
							analyzerNextState = ErrorReport;
							reportErrorFlag = true;
							break;
					}
				}
				break;
			case IncreaseReport:
				if(newNumFlag){
					// If new number arrives: check level change
					levelChangeStatus = checkLevelChange(prevInNum, inNum);
					if(levelChangeStatus == LevelIncrease){
						// If increase is detected: only accept further increases
						analyzerNextState = IncreaseReport;
					}else{
						// If level not increased, or not OK: set error
						analyzerNextState = ErrorReport;
						reportErrorFlag = true;
					}
				}
				break;
			case DecreaseReport:
				if(newNumFlag){
					// If new number arrives: check level change
					levelChangeStatus = checkLevelChange(prevInNum, inNum);
					if(levelChangeStatus == LevelDecrease){
						// If increase is detected: only accept further decreases 
						analyzerNextState = DecreaseReport;
					}else{
						// If level not decreased, or not OK: set error
						analyzerNextState = ErrorReport;
						reportErrorFlag = true;
					}
				}
				break;
			case ErrorReport:
				// If in error state, stay there
				analyzerNextState = ErrorReport;
				break;
			default:
				analyzerNextState = InitReport;
				break;
		}
		// From all state: if new report -> go to init state
		if(endReportFlag)
			analyzerNextState = InitReport;
		
		// Logging
		//if(newNumFlag){
		//	printf("New number: %u\n", inNum);
		//}
		//if(endReportFlag)
		//	printf("End of report\n");
		//if(reportErrorFlag)
		//	printf("Report error!\n");
		
		// Reset number flag 
		if(newNumFlag){
			prevInNum = inNum;
			newNumFlag = false;
		}
		// If at the and of the report and no error is detected: increase counter and clear flag
		if(endReportFlag){
			if(!reportErrorFlag ){
				validCounter++;
			}
			reportCounter++;
			endReportFlag = false;
		}
		
		// Update states
		readerState = readerNextState;
		analyzerState = analyzerNextState;
	}
	
	// Display result
	printf("%u safe reports have been found out of %u reports\n", validCounter, reportCounter);
	fclose(inputFile);
	return 0;
}
