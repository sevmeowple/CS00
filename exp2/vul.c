/*  vul.c : code for buffer overflow experiment 01.
*   By Dr. Fanping Zeng on March 28, 2025.
*   gcc -DBUF_SIZE=16 -fno-stack-protector -z execstack -o vul ../vul.c 
*/

#include <stdio.h>
#include <string.h>

#ifndef BUF_SIZE
#define BUF_SIZE 25
#endif

void welcome(char * name)
{
    char buffer[BUF_SIZE];
    strcpy (buffer, name);
    printf ("Welcome! Dear %s.\n", buffer);
    // getchar(); /* for debug */
}

int main (int argc, char *argv[])
{
    if(argc < 2){
        puts("usage: On the command line, please enter your name.");
        return 1;
    }

    welcome(argv[1]);
    
    return 0;
}
