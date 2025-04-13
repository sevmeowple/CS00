// gcc -o asm_shell ../shell_asm.c
void foo() {
  __asm__("xor    %edx,%edx ;"

          "push   %edx ;"
          "push   $0x64777373 ;" /* "sswd" */
          "push   $0x61702f2f ;" /* "//pa" */
          "push   $0x6374652f ;" /* "/etc" */
          "mov    %esp,%esi ;"   /* 保存 "//etc/passwd" 的地址到 esi */

          "push   %edx ;"        /* NULL 终止符 */
          "push   $0x7461632f ;" /* "/cat" */
          "push   $0x6e69622f ;" /* "/bin" */
          "mov    %esp,%ebx ;"   /* ebx = 程序路径 "/bin/cat" */

          "push   %edx ;"
          "push   %esi ;" 
          "push   %ebx ;"
          "mov    %esp,%ecx ;"
          "lea    0xb(%edx),%eax ;"
          "int    $0x80;" //"sysenter ;"
  );
}

int main(int argc, char *argv[]) {
  foo();
  return 0;
}
