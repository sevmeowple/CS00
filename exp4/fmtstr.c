// fmtstr.c
#include <stdio.h>
#include <stdlib.h>

void vul() {
  char user_input[1024];
  unsigned long int_input;
  // int A=0x3435,B=0x5657,C=0x7879;
  int A = 0x3435, B = 0x5657, C = 0x7879, D = 0x1234;

  // Original values of A, B and C.
  printf("&A=0x%x\t&B=0x%x\tC=0x%x.\n", &A, &B, &C);
  printf("A=0x%x\tB=0x%x\tC=0x%x.\n", A, B, C);

  // getting a string from user
  puts("Please enter a string:");
  scanf("%s", user_input);

  // Vulnerable place
  printf(user_input);
  puts("");

  // New values of A, B and C.
  printf("New values\tA=0x%x\tB=0x%x\tC=0x%x.\n", A, B, C);
}

void main(int argc, char *argv[]) { vul(); }
