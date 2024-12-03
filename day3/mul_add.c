////////////////////////////////////////////////////////////////////////////////////////////////////
// Solution for day 1 of advent of code 2024
// Task: Recognize the correct mul(<uint>,<uint>) commands on the input.
// Perform the multiplication of the two operands and summarize them.
// /////////////////////////////////////////////////////////////////////////////////////////////////
// Author: Andras Izso
////////////////////////////////////////////////////////////////////////////////////////////////////
// Edited with vim
////////////////////////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>


// Main program
// 	Read the input file line by line
// 	Perform multiplication
// 	Add to counter
int main(){
	// Define input operands and sum storage
	unsigned int num1, num2, sum = 0;
	// While input is available, multiply the operands and increment sum
	while(scanf("mul(%u,%u)\n", &num1, &num2) == 2){
		sum += num1 * num2;
	}

	// Display result
	printf("Result: %u\n", sum);

	// Exit program
	return 0;
}
