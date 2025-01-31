/** @file route_manager.c
 *  @brief A small program to analyze airline routes data.
 *  @author Mike Z.
 *  @author Felipe R.
 *  @author Hausi M.
 *  @author Jose O.
 *  @author Saasha J.
 *  @author Victoria L.
 *  @author STUDENT_NAME
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "list.h"
#include <ctype.h>

#define MAX_LINE_LENGTH 1024
#define MAX_FIELD_LENGTH 128
#define MAX_FIELDS 14
#define CHUNK_SIZE 13

typedef struct {
    char airline_name[100];
    char airline_icao_unique_code[100];
    char airline_country[100];
    char from_airport_name[100];
    char from_airport_city[100];
    char from_airport_country[100];
    char from_airport_icao_unique_code[100];
    double from_airport_altitude[100];
    char to_airport_name[100];
    char to_airport_city[100];
    char to_airport_country[100];
    char to_airport_icao_unique_code[100];
    double to_airport_altitude[100];
} Route;

// TODO: Make sure to adjust this based on the input files given
#define MAX_LINE_LEN 80

/**
 * @brief Serves as an incremental counter for navigating the list.
 *
 * @param p The pointer of the node to print.
 * @param arg The pointer of the index.
 *
 */
void inccounter(node_t *p, void *arg)
{
    int *ip = (int *)arg;
    (*ip)++;
}

/**
 * @brief Allows to print out the content of a node.
 *
 * @param p The pointer of the node to print.
 * @param arg The format of the string.
 *
 */
void print_node(node_t *p, void *arg)
{
    //char *fmt = (char *)arg;

    printf("%s (%s),%d\n",p->subject,p->icaocode,p->statistic);
}

/**
 * @brief Allows to print each node in the list.
 *
 * @param l The first node in the list
 *
 */
void analysis(node_t *l)
{
    int len = 0;

    apply(l, inccounter, &len);
    printf("Number of subject: %d\n", len);

    apply(l, print_node, "%s\n");
}

void strip_whitespace(char* str) {
    int i, j;
    int len = strlen(str);

    // Find the first non-whitespace character
    for (i = 0; i < len && (str[i] == ' ' || str[i] == '\t'); i++);

    // Shift the string left by i positions
    if (i > 0) {
        for (j = 0; j < len - i; j++) {
            str[j] = str[j + i];
        }
        str[j] = '\0';
    }
}


struct node_t* findNode(node_t* head, char* subject) {

    node_t* curr_node = head;

    while (curr_node != NULL) {

        if (strcmp(curr_node->subject, subject) == 0) {
            return curr_node;
        }

        curr_node = curr_node->next;
    }

    return NULL;
}

void read_routes_data() {

    FILE *fp;
    char line[100];
    fp = fopen("routes-airlines-airports.yaml","r");

    if (fp == NULL){

        printf("Error opening file.");
        exit(1);
    }

    node_t * resultlist = NULL;

    int counter = 0;
    fgets(line,1000,fp);

    while (fgets(line,1000, fp)!= NULL){

        Route current_route;

        counter++;

        char *token = strtok(line, ":");
        token = strtok(NULL, ":");
        token = strtok(token, "\n");

        switch (counter % 13) {

            case 1:
                strip_whitespace(token);
                strncpy(current_route.airline_name,token, 99);
                current_route.airline_name[99] = '\0';
                break;
            case 2:
                strip_whitespace(token);
                strncpy(current_route.airline_icao_unique_code, token, 99);
                current_route.airline_icao_unique_code[99] = '\0';
                break;
            case 3:
                strncpy(current_route.airline_country, token, 99);
                current_route.airline_country[99] = '\0';
                break;
            case 4:
                strncpy(current_route.from_airport_name, token, 99);
                current_route.from_airport_name[99] = '\0';
                break;
            case 5:
                strncpy(current_route.from_airport_city, token, 99);
                current_route.from_airport_city[99] = '\0';
                break;
            case 6:
                strncpy(current_route.from_airport_country, token, 99);
                current_route.from_airport_country[99] = '\0';
                break;
            case 7:
                strncpy(current_route.from_airport_icao_unique_code, token, 99);
                current_route.from_airport_icao_unique_code[99] = '\0';
                break;
            case 8:
                current_route.from_airport_altitude[0] = atof(token);
                current_route.from_airport_altitude[99] = '\0';
                break;
            case 9:
                strncpy(current_route.to_airport_name, token, 99);
                current_route.to_airport_name[99] = '\0';
                break;
            case 10:
                strncpy(current_route.to_airport_city, token, 99);
                current_route.to_airport_city[99] = '\0';
                break;
            case 11:
                strncpy(current_route.to_airport_country, token, 99);
                current_route.to_airport_country[99] = '\0';
                break;
            case 12:
                strncpy(current_route.to_airport_icao_unique_code, token, 99);
                current_route.to_airport_icao_unique_code[99] = '\0';
                break;
            case 0:
                current_route.to_airport_altitude[0] = atof(token);
                current_route.to_airport_altitude[99] = '\0';


            if (strcmp(current_route.to_airport_country," Canada")==0){

                node_t * found_node = findNode(resultlist,current_route.airline_name);

                if (found_node == NULL) {

                    resultlist = add_inorder(resultlist,new_node(current_route.airline_name,1,current_route.airline_icao_unique_code));
                }else{
                    found_node->statistic++;
                }
            }
        }

    }

    fclose(fp);

    //add from resultlist to an in order final list
    node_t * final = NULL;
    node_t * curr = resultlist;
    while (curr!=NULL){
        final = add_inorder(final,new_node(curr->subject,curr->statistic,curr->icaocode));
        curr = curr->next;
    }

    analysis(final);


}


/**
 * @brief The main function and entry point of the program.
 *
 * @param argc The number of arguments passed to the program.
 * @param argv The list of arguments passed to the program.
 * @return int 0: No errors; 1: Errors produced.
 *
 */

int main(int argc, char *argv[]) {
    /*
    // Initial dummy code
    char *line = NULL;
    char *t;
    int num = 0;
    node_t *list = NULL;
    line = (char *)malloc(sizeof(char) * MAX_LINE_LEN);
    strcpy(line, "this is the starting point for A3.");

    // Creating the nodes for the ordered list
    t = strtok(line, " ");
    while (t)
    {
        num++;
        list = add_inorder(list, new_node(t));
        t = strtok(NULL, " ");
    }

    // Printing out the content of the sorted list
    analysis(list);
    

    // Releasing the space allocated for the list and other emalloc'ed elements
    node_t *temp_n = NULL;
    for (; list != NULL; list = temp_n)
    {
        temp_n = list->next;
        free(list->word);
        free(list);
    }
    free(line);

    exit(0);
    */

    char question_param[100]; // Allocate enough space for the string
    strcpy(question_param, argv[2]); // Copy the string into the array

    char requested_elements[100]; // Allocate enough space for the string
    strcpy(requested_elements, argv[3]); // Copy the string into the array


    if (strcmp(question_param,"--QUESTION=1")==0){
        printf("entering question1");
        read_routes_data();


    }else if (strcmp(question_param,"--QUESTION=2")==0){
        printf("entering question2");

    }else if (strcmp(question_param,"--QUESTION=3")==0){
        printf("entering question3");

    }else{
        printf("Error, question not found.");

    }




   return 0;


}
