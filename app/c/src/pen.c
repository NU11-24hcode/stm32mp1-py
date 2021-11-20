#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include "pwm.h"

#define PERIOD	20000000 /* 20 ms */
#define DOWN	 1000000 /* 1.0 ms */
#define UP		 1400000 /* 1.4 ms */

void pen_up(void)
{
	pwm_set(UP, PERIOD);
}

void pen_down(void)
{
	pwm_set(DOWN, PERIOD);
}
