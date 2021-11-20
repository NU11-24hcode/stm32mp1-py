#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

#include "pwm.h"

#define EXPORT "/sys/class/pwm/pwmchip0/export"
#define ENABLE "/sys/class/pwm/pwmchip0/pwm0/enable"
#define PERIODE "/sys/class/pwm/pwmchip0/pwm0/period"
#define DUTY "/sys/class/pwm/pwmchip0/pwm0/duty_cycle"

static int export_done = 0;

static int _pwm_write(char *file, int val)
{
	FILE *f;

	f = fopen(file, "w");
	if (f == NULL) {
		//g_print("Fail to open %s\n", file);
		return 1;
	}

	fprintf(f, "%d\n", val);
	fclose(f);

	return 0;
}

static int _pwm_enable(int enable)
{
	return _pwm_write(ENABLE, enable);
}

static int _pwm_period(int period)
{
	return _pwm_write(PERIODE, period);
}

static int _pwm_duty_cycle(int duty)
{
	return _pwm_write(DUTY, duty);
}

static int _pwm_export(int channel)
{
	return _pwm_write(EXPORT, channel);
}

void pwm_set(int duty, int period)
{
	if (!export_done) {
		export_done = !_pwm_export(0);
	}

	_pwm_enable(0);
	_pwm_period(period);
	_pwm_duty_cycle(duty);
	_pwm_enable(1);
}
