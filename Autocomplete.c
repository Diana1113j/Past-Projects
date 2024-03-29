#include "autocomplete.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int isDigit(char c) {
    return '0' <= c && c <= '9';
}

int toInt(char c) {
    return (int) c - '0';
}

int compare(const void* a, const void* b) {
    const struct term a_ = *((const struct term*) a), b_ = *((const struct term*) b);
    return strcmp(a_.term, b_.term);
}

int compareWeights(const void* a, const void* b) {
    const struct term a_ = *((const struct term*) a), b_ = *((const struct term*) b);
    return -((a_.weight) - (b_.weight));
}

void read_in_terms(struct term **terms, int *pnterms, char *filename)
{   
    

    FILE* fp = fopen(filename, "r");    

    if(fp == NULL) {   
        printf("Error");
    }

    char line[200];     
    fgets(line, 200, fp);   
                            
    *pnterms = atoi(line);  
    *terms = malloc(sizeof(struct term) * (*pnterms));

    for (int i = 0; i < *pnterms; i++) {
        fgets(line, 200, fp);
        int readingWeight = 0, readingTerm = 0; 
        double weight = 0;
        char term[200];
        memset(term, 0, sizeof(term));

        for (int c = 0; line[c] != '\n'; c++) {

            if (isDigit(line[c]) && c <= 14) {
                readingWeight = 1;  
                weight = (weight * 10) + toInt(line[c]);  
                                                            
            } else if (readingWeight == 1) {

                readingTerm = 1;
                readingWeight = 0;

                continue;
            }

            if (readingTerm >= 1) {
                term[readingTerm - 1] = line[c];
                readingTerm++; 
            }
        }

        (*terms)[i].weight = weight;
        strcpy((*terms)[i].term, term);
    }

    qsort(*terms, *pnterms, sizeof(struct term), compare);


    fclose(fp);
}

int lowest_match(term *terms, int nterms, char *substr)
{
    
    int start = 0, end = nterms - 1;
    while (start <= end) {
        int mid = (start + end) / 2;
        int strcomp = strncmp(substr, terms[mid].term, strlen(substr));
        if (strcomp > 0) start = mid + 1;
        else {
            end = mid - 1;  
        }
        
    }
    return start;
}

int highest_match(struct term *terms, int nterms, char *substr)
{
    
    int start = lowest_match(terms, nterms, substr); 
    int end = nterms - 1;
    while (start <= end) {
        int mid = (start + end) / 2;
        int strcomp = strncmp(substr, terms[mid].term, strlen(substr)); 
        
        if (strcomp < 0) end = mid - 1;
        else {
            start = mid + 1;
        }
      
    }
    return end;
}

void autocomplete(term **answer, int *n_answer, term *terms, int nterms, char *substr)  // idk if this works
{
    int lowest = lowest_match(terms, nterms, substr);
    int highest = highest_match(terms, nterms, substr);

    *n_answer = highest - lowest + 1;

    *answer = malloc(sizeof(struct term) * (*n_answer));
    for (int i = lowest; i < highest + 1; i++){
        strcpy((*answer)[i - lowest].term, terms[i].term);
        (*answer)[i - lowest].weight = terms[i].weight;
    }
    
    qsort(*answer, *n_answer, sizeof(struct term), compareWeights);

   
}

