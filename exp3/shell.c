// shell.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
void foo() {
  char *name[3];
  name[0] = "/bin/cat";
  name[1] = "//etc/passwd";
  name[2] = NULL;
  execve(name[0], name, NULL);
}
int main(int argc, char *argv[]) {
  foo();
  return 0;
}