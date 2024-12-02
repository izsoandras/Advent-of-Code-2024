////////////////////////////////////////////////////////////////////////////////////////////////////
// Solution for day 1 of advent of code 2024
// Task: read in a file, containing two integers, separated by a space in each line
// Than compare numbers in the two columns: smallest with smallest, 2nd smallest /w 2nd smallest, etc
// Cummulate the absolute values of the differences of these pairs
// /////////////////////////////////////////////////////////////////////////////////////////////////
// Author: Andras Izso
////////////////////////////////////////////////////////////////////////////////////////////////////
// Edited with vim
////////////////////////////////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

// Linked list
typedef struct LinkedList{
	unsigned int data;	// Data to store
	struct LinkedList *nextElement;	// Pointer to next element
} LinkedList;

// Allocate a new element for the linked list
// @param unsigned int num: number to be stored
// @param LinkedList *nextElement: next element in linked list (if this will be the last: NULL)
//
// @return LinkedList*: pointer to the new element. Memory allocated dynamically, so don't forget to call free()!
LinkedList* allocLinkedListElement(unsigned int num, LinkedList *nextElement){
	LinkedList* newElement = (LinkedList*)malloc(sizeof(LinkedList));
	newElement->data = num;
	newElement->nextElement = nextElement;

	return newElement;
}

// Free the linked list
// @param LinkedList *list: list to be deallocated
void freeLinkedList(LinkedList *list){
	if(list->nextElement != NULL){
		freeLinkedList(list->nextElement);
	}

	free(list);
}

// Append new element to linked list
// @param LinkedList *list: pointer to a list element
// @param unsigned int num: number to insert
// 
// @return  the pointer to the new element for ease of chaining
LinkedList* appendToLinkedList(LinkedList *list, unsigned int num){
	// If this element is empty: create it
	// If not: go to next
	if(list->nextElement == NULL){
		list->nextElement = allocLinkedListElement(num, NULL);
		return list->nextElement;

	}else{
		return appendToLinkedList(list->nextElement, num);
	}
}

// Copy the given number of elements to the given destination
// @param LinkedList *list: list to be copied
// @param unsigned int dest: destination to copy to
// @param unsigned int length: number of elements to copy
void toArray(LinkedList *list, unsigned int *dest, unsigned int length){
	for(unsigned int i = 0; i<length; i++){
		dest[i] = list->data;
		list = list->nextElement;
	}
}

// Performs the partitioning of the quicksort algorithm.
// Pulled out to separate function to spare stack size.
// @param unsigned int *array: array to be sorted
// @param unsigned int startIdx: start index of partition to sort
// @param unsigned int endIdx: end index of partition to sort (inclusive)
// @paramOut unsigned int *lowerEndIdx: end of the partition, that is lower than the pivot value (inclusive). Signed, so underflow is visible, long to match all posititve int.
// @paramOut signed long int *greaterStartidx: start of the partition that is greater than the pivot value (inclusive). Signed, so overflow is visible, long to match all posititve int.
void qsortPivot(unsigned int *array, unsigned int startIdx, unsigned int endIdx, signed long int *lowerEndIdx, signed long int *greaterStartIdx){
	// Choose middle element as pivot
	unsigned int pivotVal = array[(startIdx+endIdx)/2];

	// Define working indicies, each indicating where the next value in each case should be placed
	unsigned int nextLowerIdx = startIdx;
	unsigned int nextEqualIdx = startIdx;
	unsigned int nextGreaterIdx = endIdx;

	// Temporary storage for swapping
	unsigned int tmp;
	// Perform pivot
	while(nextEqualIdx <= nextGreaterIdx){
		if(array[nextEqualIdx] < pivotVal){
			// If where equal is assumed, it is lower: swap with the lesser
			tmp = array[nextLowerIdx];
			array[nextLowerIdx] = array[nextEqualIdx];
			array[nextEqualIdx] = tmp;

			// Increment lower and equal indicies
			nextLowerIdx++;
			nextEqualIdx++;
		}else if(array[nextEqualIdx] > pivotVal){
			// If where equal is assumed, it is greater: swap with the lesser
			tmp = array[nextGreaterIdx];
			array[nextGreaterIdx] = array[nextEqualIdx];
			array[nextEqualIdx] = tmp;

			// Decremenet greater index
			nextGreaterIdx--;
		}else{// If equal actually equals: move on
		      nextEqualIdx++;
		}
	}
	*lowerEndIdx = (signed long int)nextLowerIdx-1;
	*greaterStartIdx = (signed long int)nextGreaterIdx+1;
}	

// Performs quick sort in place on (a segment of) an unsigned integer array.
// @param unsigned int *array: array to be sorted
// @param unsigned int startIdx: start index of array segment to be sorted (inclusive)
// @param unsigned int endIdx: end index of array segment to be sorted (inclusive)
void qsortUIntInplace(unsigned int *array, signed long int startIdx, signed long int endIdx){
	if(startIdx < endIdx){	// unsigned will underflow -> start becomes greater than (or equal to) end
		signed long int lowerPartEnd, greaterPartStart = 0;
		// Create partitions
		qsortPivot(array, startIdx, endIdx, &lowerPartEnd, &greaterPartStart);
		
		// Sort partitions
		qsortUIntInplace(array, startIdx, lowerPartEnd);
		qsortUIntInplace(array, greaterPartStart, endIdx);
	}	
}

// Find first appearance of a target number in an ordered array, utilizing interval halving search
// @param unsigned int *array: the ordered array
// @param unsigned int length: length of the array
// @param unsigned int target: the number we are looking for
//
// @return: the index of the first appearance of the number, or -1 if not present
long int findFirstInOrdered(unsigned int *array, unsigned int length, unsigned int target){
	// If the target cannot be in the array, signal it
	if(target < array[0] || target > array[length-1])
		return -1;

	// Initialize bounding and middle indicies
	unsigned int lowerBoundIdx = 0;
	unsigned int upperBoundIdx = length-1;
	unsigned int midIdx;
	
	// Perform search
	while(upperBoundIdx > lowerBoundIdx){
		// Value at the middle of interval
		midIdx = (lowerBoundIdx + upperBoundIdx)/2;

		if(array[midIdx] < target){
			// If middle is less than target: increase lower bound
			lowerBoundIdx = midIdx+1;
		}else{
			// If middle is greater than or equal to the target: reduce upper bound
			upperBoundIdx = midIdx;
		}
	}
	
	// If the number is not present in the array, the lower bound will indicate the first element
	// that is greater than the target
	if(array[upperBoundIdx] == target)
		return upperBoundIdx;
	else
		return -1;
}

// Find last appearance of a target number in an ordered array, utilizing interval halving search
// @param unsigned int *array: the ordered array
// @param unsigned int length: length of the array
// @param unsigned int target: the number we are looking for
//
// @return: the index of the last appearance of the number, or -1 if not present
long int findLastInOrdered(unsigned int *array, unsigned int length, unsigned int target){
	// If the target cannot be in the array, signal it
	if(target < array[0] || target > array[length-1])
		return -1;

	// Initialize bounding and middle indicies
	unsigned int lowerBoundIdx = 0;
	unsigned int upperBoundIdx = length-1;
	unsigned int midIdx;
	
	// Perform search
	while(upperBoundIdx > lowerBoundIdx){
		midIdx = (lowerBoundIdx + upperBoundIdx + 1)/2;

		if(array[midIdx] > target){
			// If middle is greater than the target: reduce upper bound
			upperBoundIdx = midIdx-1;
		}else{
			// If middle is less than or equal to target: increase lower bound
			lowerBoundIdx = midIdx;
		}
	}

	// If the number is not present in the array, the upper bound will indicate the first element
	// that is less than the target
	if(array[lowerBoundIdx] == target)
		return lowerBoundIdx;
	else
		return -1;
}

// Calculate the number of appaerance of a target number in the given ordered array
// @param unsigned int *array: array to be searched
// @param unsigned int length: length of array
// @param unsigned int target: number to be searched
//
// @return: the number of occurance
unsigned int numberOfAppearenceInOrdered(unsigned int *array, unsigned int length, unsigned int target){
	long int firstIdx = findFirstInOrdered(array, length, target);

	if(firstIdx == -1)
		return 0;

	long int lastIdx = findLastInOrdered(array, length, target);

	return (unsigned int)(lastIdx - firstIdx + 1);
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
	
	// Allocate variables
	unsigned int inNum1, inNum2, inLength = 0;	// Read input destination
	LinkedList *list1, *lastElement1, *list2, *lastElement2 = NULL;	// Lists to store data, and their last elements
	
	// Read first line to initialize lists
	if(fscanf(inputFile, "%d %d\n", &inNum1, &inNum2) == 2){
		inLength++;
		list1 = allocLinkedListElement(inNum1, NULL);
		list2 = allocLinkedListElement(inNum2, NULL);
		
		// Store last elements to more efficient insertion, and sorting
		lastElement1 = list1;
		lastElement2 = list2;

		// Read rest of the file
		while(fscanf(inputFile, "%u %u\n", &inNum1, &inNum2) == 2){
			inLength++;
			lastElement1 = appendToLinkedList(lastElement1, inNum1);
			lastElement2 = appendToLinkedList(lastElement2, inNum2);
		}
	}

	// Output basic statistics, to check if read is successful
	printf("%u elements have been read\n", inLength);
	printf("Last elements are %u and %u\n", lastElement1->data, lastElement2->data);
	
	// Convert to standard array for ease of sorting
	unsigned int array1[inLength], array2[inLength];
	toArray(list1, array1, inLength);
	toArray(list2, array2, inLength);

	freeLinkedList(list1);
	freeLinkedList(list2);

	// Sort linked lists
	qsortUIntInplace(array1, 0, inLength-1);
	qsortUIntInplace(array2, 0, inLength-1);

	// Calculate difference between ordered elements and similarity index 
	unsigned long int sumAbsDiff, similarityIdx = 0;
	unsigned int increment, noOfAppear = 0, prev1 = 0;
	
	for(unsigned int i = 0; i<inLength; i++){
		// Total absolute difference
		if(array1[i] > array2[i])
			increment = array1[i]-array2[i];
		else
			increment = array2[i]-array1[i];

		sumAbsDiff += increment;

		// Similarity index: array1 element * number of appearence in array2
		if(prev1 != array1[i]){
			noOfAppear = numberOfAppearenceInOrdered(array2, inLength, array1[i]);
			similarityIdx += array1[i] * noOfAppear;
			prev1 = array1[i];
		}
	}

	// Print result
	printf("====RESULTS====\n");
	printf("Total absolute difference of locations: %lu\n", sumAbsDiff);
	printf("Similarity index: %lu\n", similarityIdx);

	// Close file
	fclose(inputFile);

	// Exit program
	return 0;
}
