#include <stdio.h>
#include <string.h>

// Safe input (no implicit gets)
void vulnerable() {
    char buf[64];
    printf("Enter some input: ");
    fflush(stdout);
    if (fgets(buf, sizeof(buf), stdin) != NULL) {
        // remove newline if present
        buf[strcspn(buf, "\n")] = '\0';
    }
}

int main() {
    printf("Toy binary for ROPSmith testing.\n");
    vulnerable();
    return 0;
}
