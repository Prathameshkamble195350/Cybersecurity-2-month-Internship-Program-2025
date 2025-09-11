#include <stdio.h>
#include <string.h>

// Vulnerable function with buffer overflow
void vulnerable() {
    char buf[64];
    printf("Enter some input: ");
    gets(buf);   // ⚠️ Insecure function, allows buffer overflow
}

int main() {
    printf("Toy binary for ROPSmith testing.\n");
    vulnerable();
    return 0;
}
