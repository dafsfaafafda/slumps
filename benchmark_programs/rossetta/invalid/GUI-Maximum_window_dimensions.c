
#include<windows.h>
#include<stdio.h>

int main()
{
	printf("Dimensions of the screen are (w x h) : %d x %d pixels",GetSystemMetrics(SM_CXSCREEN),GetSystemMetrics(SM_CYSCREEN));
	return 0;
}
/* <stdin>:2:9: fatal error: 'windows.h' file not found
#include<windows.h>
        ^~~~~~~~~~~
1 error generated.
 */