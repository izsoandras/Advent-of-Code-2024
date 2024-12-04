////////////////////////////////////////////////////////////////////////////////////////////////////
// Solution for day 4 of advent of code 2024
// Find XMAS in all orientation
// /////////////////////////////////////////////////////////////////////////////////////////////////
// Author: Andras Izso
////////////////////////////////////////////////////////////////////////////////////////////////////
// Edited with vim
////////////////////////////////////////////////////////////////////////////////////////////////////
#include <stdio.h>
#include <stdlib.h>

typedef struct BlockArray{
	unsigned int blockSize;		// size of a block (they are squre)
	unsigned int heightInBlock;	// how many rows of blocks there is
	unsigned int widthInBlock;	// how many columns of blocks there is
	unsigned int numInBlock;	// how many entries are in a block (store for caching reasons)
	unsigned int numInBlockRow;	// how many entries are in a row of blocks (store for caching reasons)
	char *array;			// pointer to memory block
} BlockArray;

BlockArray createBlockArray(unsigned int widthInBlock, unsigned int heightInBlock, unsigned int blockSize){
	BlockArray ret;
	ret.blockSize = blockSize;
	ret.widthInBlock = widthInBlock;
	ret.heightInBlock = heightInBlock;
	ret.numInBlock = blockSize * blockSize;
	ret.numInBlockRow = ret.numInBlock * widthInBlock;

	ret.array = (char*)malloc(heightInBlock * ret.numInBlockRow * sizeof(char));

	return ret;
}

unsigned int getLinearIndex(BlockArray array, unsigned int row, unsigned int col){
	unsigned int blockRow = row/array.blockSize;
	unsigned int blockCol = col/array.blockSize;

	unsigned int subRow = row % array.blockSize;
	unsigned int subCol = col % array.blockSize;

	return blockRow * array.numInBlockRow + blockCol * array.numInBlock + subRow * array.blockSize + blockCol;
}

char getFromBlockArray(BlockArray ba, unsigned int row, unsigned int col){
	return ba.array[getLinearIndex(ba, row, col)];
}

void setInBlockArray(char c, BlockArray ba, unsigned int row, unsigned int col){
	ba.array[getLinearIndex(ba, row, col)] = c;
}

// Main program
// 	Reads the input file name from argument
//	Reads the input file into two linked lists
//	Reads sorts the linked lists
//      Calculate and Prints the result
int main(int argc, char* argv[]){
	// Create default input name
	char* fileName = "input";
	// If input arguments are given, use the first as input file name
	// If multiple are given, give warning
	if(argc > 1){
		fileName = argv[1];
		if(argc > 2){
			printf("Too many input arguments, considering 1st as input name\n");
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
}
