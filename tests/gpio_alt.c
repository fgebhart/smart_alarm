    /*
    Utility to switch Raspberry-Pi GPIO pin functions
    Tim Giles 01/04/2013

    Usage:
    $ gpio_alt -p PIN_NUMBER -f ALT_NUMBER

    Based on RPi code from Dom and Gert, 15-Feb-2013, <http://elinux.org/RPi_Low-level_peripherals#C_2>
    and Gnu getopt() example <http://www.gnu.org/software/libc/manual/html_node/Example-of-Getopt.html#Example-of-Getopt>
    */

    #include <ctype.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <unistd.h>
    #include <fcntl.h>
    #include <sys/mman.h>

    #define BCM2708_PERI_BASE        0x20000000
    #define GPIO_BASE                (BCM2708_PERI_BASE + 0x200000) /* GPIO controller */
    #define PAGE_SIZE (4*1024)
    #define BLOCK_SIZE (4*1024)

    int  mem_fd;
    void *gpio_map;
    volatile unsigned *gpio;
    void setup_io();

    // GPIO setup macros. Always use INP_GPIO(x) before using OUT_GPIO(x) or SET_GPIO_ALT(x,y)
    #define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
    #define OUT_GPIO(g) *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))
    #define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))

    #define GPIO_SET *(gpio+7)  // sets   bits which are 1 ignores bits which are 0
    #define GPIO_CLR *(gpio+10) // clears bits which are 1 ignores bits which are 0



    int main (int argc, char **argv) {
      int opt, flag, n_pin, n_alt;
      flag=0;

      while ((opt = getopt (argc, argv, "hp:f:")) != -1) {
        switch (opt) {
        case 'h':
          break;
        case 'p':
          n_pin = atoi(optarg); flag |= 0b0001; break;
        case 'f':
          n_alt = atoi(optarg); flag |= 0b0010; break;
        case '?':
          // getopt() prints error messages, so don't need to repeat them here
          return 1;
        default:
          abort ();
        }
      }
     
      if (flag != 0b0011) {
        fprintf (stderr, "Usage:\n$ gpio_alt -p PIN_NUM -f FUNC_NUM\n");
        return 1;
      }
     
      setup_io(); // Set up gpi pointer for direct register access
      INP_GPIO(n_pin);  // Always use INP_GPIO(x) before using SET_GPIO_ALT(x,y)
      SET_GPIO_ALT(n_pin, n_alt);
     
      printf("Set pin %i to alternative-function %i\n", n_pin, n_alt);
     
      return 0;
    }



    void setup_io() {
       /* open /dev/mem */
       if ((mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) {
          printf("can't open /dev/mem \n");
          exit(-1);
       }

       /* mmap GPIO */
       gpio_map = mmap(
          NULL,             //Any adddress in our space will do
          BLOCK_SIZE,       //Map length
          PROT_READ|PROT_WRITE,// Enable reading & writting to mapped memory
          MAP_SHARED,       //Shared with other processes
          mem_fd,           //File to map
          GPIO_BASE         //Offset to GPIO peripheral
       );

       close(mem_fd); //No need to keep mem_fd open after mmap

       if (gpio_map == MAP_FAILED) {
          printf("mmap error %d\n", (int)gpio_map);//errno also set!
          exit(-1);
       }

       // Always use volatile pointer!
       gpio = (volatile unsigned *)gpio_map;
    }
