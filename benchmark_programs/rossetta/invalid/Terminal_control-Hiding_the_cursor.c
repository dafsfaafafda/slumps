
/* Please note that curs_set is terminal dependent. */

#include<curses.h>
#include<stdio.h>

int
main ()
{
  printf
    ("At the end of this line you will see the cursor, process will sleep for 5 seconds.");
  napms (5000);
  curs_set (0);
  printf
    ("\nAt the end of this line you will NOT see the cursor, process will again sleep for 5 seconds.");
  napms (5000);
  printf ("\nGoodbye.");
  return 0;
}
/* <stdin>:4:9: fatal error: 'curses.h' file not found
#include<curses.h>
        ^~~~~~~~~~
1 error generated.
 */