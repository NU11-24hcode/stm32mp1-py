#ifndef L6470_H
#define L6470_H

#include <stdint.h>

#define MICRO_STEPS		7

/* l6740_set_maxspeed - set the max speed on each motor */
void l6740_set_maxspeed(uint32_t left, uint32_t right);

/* l6470_do_steps - perform L,R steps on left and right motors */
int l6470_do_steps(int left, int right);

#endif
