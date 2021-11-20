#include <stdlib.h>
#include <stdio.h>

#include "l6470.h"
#include "wires.h"

#define STEP		(float)(0.2 / (1 << MICRO_STEPS))
#define MAX_SPEED	(float)10

int wires_mm(float left, float right, float *wireL, float *wireR)
{
	int32_t stepL, stepR;
	uint32_t speedL, speedR;

	/*
	 * adapt motors speed given the number of steps
	 * they have to do to let them finish at the same time
	 */
	if (abs(left) > abs(right)) {
		speedL = MAX_SPEED;
		speedR = abs(right * MAX_SPEED / left);
	} else {
		speedR = MAX_SPEED;
		speedL = abs(left * MAX_SPEED / right);
	}
	l6740_set_maxspeed(speedL, speedR);

	/* convert mm in steps */
	stepL = left / STEP;
	stepR = right / STEP;

	*wireL = stepL * STEP;
	*wireR = stepR * STEP;

	return l6470_do_steps(stepL, stepR);
}
