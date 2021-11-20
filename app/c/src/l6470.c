#include <stdint.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <getopt.h>
#include <fcntl.h>
#include <time.h>
#include <sys/ioctl.h>
#include <linux/ioctl.h>
#include <sys/stat.h>
#include <linux/types.h>
#include <linux/spi/spidev.h>

#include "l6470.h"

#define ARRAY_SIZE(x) (sizeof(x) / sizeof((x)[0]))
#define BIT(n) (UINT32_C(1) << (n))

#define SPIDEV		"/dev/spidev0.0"

/* Registers & flags */
#define REG_MAX_SPEED		0x07
#define REG_MIN_SPEED		0x08
#define REG_OCD_TH			0x13
#define REG_STEP_MODE		0x16

#define REG_STATUS			0x19
#define STATUS_OCD			BIT(12)
#define STATUS_WRONG_CMD	BIT(8)
#define STATUS_NOTPERF_CMD	BIT(7)
#define STATUS_DIR			BIT(4)
#define STATUS_BUSY			BIT(1)
#define STATUS_HIZ			BIT(0)

/* Commands */
#define NOPE				0x00

#define SETPARAM			0x00
#define SETMAXSPEED			SETPARAM + REG_MAX_SPEED
#define SETMINSPEED			SETPARAM + REG_MIN_SPEED
#define SETSTEPS			SETPARAM + REG_STEP_MODE
#define SETOCDTH			SETPARAM + REG_OCD_TH

#define GETPARAM			0x20
#define GETSTEPS			GETPARAM + REG_STEP_MODE

#define GETSTATUS			0xD0

#define MOVE				0x40

#define SOFTSTOP			0xB0
#define RESETDEVICE			0xC0
#define SOFTHIZ				0xA0

#define MAX_LENGTH			4
#define DAISYCHAIN			2
#define MSG_SIZE			(MAX_LENGTH * DAISYCHAIN)
#define MAX_STEP			0x3FFFFF
#define STEP				0.2

#define DEFAULT_OCD_TH		0x08 /* 0..15 steps, 375mA each step */

static int fd = - 1;

static uint32_t _get_status(void)
{
	int ret;
	int i;
	uint32_t status;
	char tx[MSG_SIZE];
	char rx[MSG_SIZE];

	memset(tx, NOPE, sizeof(tx));
	memset(rx, NOPE, sizeof(rx));
	memset(tx, GETSTATUS, DAISYCHAIN);

	for (i = 0; i < MAX_LENGTH; i++) {
		struct spi_ioc_transfer msg[1] = {
			{
				.tx_buf = (unsigned long)tx + (i * DAISYCHAIN),
				.rx_buf = (unsigned long)rx + (i * DAISYCHAIN),
				.len    = DAISYCHAIN,
			}
		};

		ret = ioctl(fd, SPI_IOC_MESSAGE(1), &msg);
		if (ret < 1)
			printf("Can't send spi message\n");
	}

	status = (rx[2] << 24) + (rx[4] << 16) + (rx[3] << 8) + rx[5];

	if ((status & STATUS_WRONG_CMD) || (status & (STATUS_WRONG_CMD << 16)))
		printf("Status: wrong command status 0x%x\n", status);

	if ((status & STATUS_NOTPERF_CMD) || (status & (STATUS_NOTPERF_CMD << 16)))
		printf("Status: not performed command status 0x%x\n", status);

	if (!(status & STATUS_OCD) || !(status & (STATUS_OCD << 16))) {
		printf("Status: overcurrent detected 0x%x\n", status);
		printf("APPLICATION STOPPED - Please check the mechanical setup and your software :-)\n");
		exit(1);
	}

	return status;
}

static int _is_highZ(void)
{
	uint32_t status = _get_status();

	return (status & STATUS_HIZ) && (status & (STATUS_HIZ << 16));
}

static int _is_busy(void)
{
	uint32_t status = _get_status();

	return !(status & STATUS_BUSY) || !(status & (STATUS_BUSY << 16));
}

static void _stophiz(void)
{
	int ret;
	int i;
	char tx[MSG_SIZE];
	char rx[MSG_SIZE];

	memset(tx, NOPE, sizeof(tx));
	memset(rx, NOPE, sizeof(rx));
	memset(tx, SOFTHIZ, DAISYCHAIN);

	while(_is_busy());

	for (i = 0; i < MAX_LENGTH; i++) {
		struct spi_ioc_transfer msg[1] = {
			{
				.tx_buf = (unsigned long)tx + (i * DAISYCHAIN),
				.rx_buf = (unsigned long)rx + (i * DAISYCHAIN),
				.len    = DAISYCHAIN,
			}
		};

		ret = ioctl(fd, SPI_IOC_MESSAGE(1), &msg);
		if (ret < 1)
			printf("Can't send spi message\n");
	}
}

/* set steps divisor
 * 0 is full step
 * 7 is 1/128 micro steps */
static void _set_steps(int step)
{
	int ret;
	int i;
	char tx[MSG_SIZE];
	char rx[MSG_SIZE];
	//printf("step 1 / %d\n", 1 << step);

	if (fd < 0)
		return;

	memset(tx, NOPE, sizeof(tx));
	memset(rx, NOPE, sizeof(rx));

	_stophiz();
	while(_is_busy() || !_is_highZ());

	tx[0] = SETSTEPS;
	tx[1] = SETSTEPS;
	tx[2] = step & 0x07;
	tx[3] = step & 0x07;

	for (i = 0; i < 2; i++) {
		struct spi_ioc_transfer msg[1] = {
			{
				.tx_buf = (unsigned long)tx + (i * DAISYCHAIN),
				.rx_buf = (unsigned long)rx + (i * DAISYCHAIN),
				.len    = DAISYCHAIN,
			}
		};

		ret = ioctl(fd, SPI_IOC_MESSAGE(1), &msg);
		if (ret < 1)
			printf("Can't send spi message\n");
	}
}


/* set Over Current Detection Threshold
 * 0..15 steps, 375mA each step */
static void _set_ocd_threshold(int threshold)
{
	int ret;
	int i;
	char tx[MSG_SIZE];
	char rx[MSG_SIZE];

	if (fd < 0)
		return;

	memset(tx, NOPE, sizeof(tx));
	memset(rx, NOPE, sizeof(rx));

	_stophiz();
	while(_is_busy() || !_is_highZ());

	tx[0] = SETOCDTH;
	tx[1] = SETOCDTH;
	tx[2] = threshold & 0x0F;
	tx[3] = threshold & 0x0F;

	for (i = 0; i < 2; i++) {
		struct spi_ioc_transfer msg[1] = {
			{
				.tx_buf = (unsigned long)tx + (i * DAISYCHAIN),
				.rx_buf = (unsigned long)rx + (i * DAISYCHAIN),
				.len    = DAISYCHAIN,
			}
		};

		ret = ioctl(fd, SPI_IOC_MESSAGE(1), &msg);
		if (ret < 1)
			printf("Can't send spi message\n");
	}
}

void _reset_device(void)
{
	int ret;
	int i;
	char tx[MSG_SIZE];
	char rx[MSG_SIZE];

	memset(tx, NOPE, sizeof(tx));
	memset(rx, NOPE, sizeof(rx));
	memset(tx, RESETDEVICE, DAISYCHAIN);

	for (i = 0; i < MAX_LENGTH; i++) {
		struct spi_ioc_transfer msg[1] = {
			{
				.tx_buf = (unsigned long)tx + (i * DAISYCHAIN),
				.rx_buf = (unsigned long)rx + (i * DAISYCHAIN),
				.len    = DAISYCHAIN,
			}
		};

		ret = ioctl(fd, SPI_IOC_MESSAGE(1), &msg);
		if (ret < 1)
			printf("Can't send spi message\n");
	}
}

static int _init(void)
{
	int ret;
	uint32_t mode = SPI_CPHA | SPI_CPOL;
	uint32_t bits = 0; /* 8 bits per word */

	if (fd > 0)
		return 0;

	fd = open(SPIDEV, O_RDWR);
	if (fd < 0) {
		printf("Can't open %s\n", SPIDEV);
		return fd;
	}

	ret = ioctl(fd, SPI_IOC_WR_MODE32, &mode);
	if (ret == -1) {
		printf("can't set spi mode");
		return ret;
	}

	ret = ioctl(fd, SPI_IOC_WR_BITS_PER_WORD, &bits);
	if (ret == -1) {
		printf("can't set bits per word");
		return ret;
	}

	_reset_device();

	_set_steps(MICRO_STEPS);

	_set_ocd_threshold(DEFAULT_OCD_TH);

	return 0;
}

/* move of given number of steps */
int l6470_do_steps(int32_t left, int32_t right)
{
	int ret, i;
	char tx[MSG_SIZE];
	char rx[MSG_SIZE];

	if (!left && !right)
		return 0;

	_init();

	//printf("l6470_move %d %d\n", left, right);

	if (fd < 0) {
		return 0;
	}

	memset(tx, NOPE, sizeof(tx));
	memset(rx, NOPE, sizeof(rx));

	while(_is_busy());

	tx[0] = MOVE;
	tx[0] |= left < 0 ? 0 : 1;
	tx[2] = (abs(left) >> 16) & 0x3F;
	tx[4] = (abs(left) >> 8) & 0xFF;
	tx[6] = abs(left) & 0xFF;

	tx[1] = MOVE;
	tx[1] |= right > 0 ? 0 : 1;
	tx[3] = (abs(right) >> 16) & 0x3F;
	tx[5] = (abs(right) >> 8) & 0xFF;
	tx[7] = abs(right) & 0xFF;

	for (i = 0; i < MAX_LENGTH; i++) {
		struct spi_ioc_transfer msg[1] = {
			{
				.tx_buf = (unsigned long)tx + (i * DAISYCHAIN),
				.rx_buf = (unsigned long)rx + (i * DAISYCHAIN),
				.len    = DAISYCHAIN,
			}
		};

		ret = ioctl(fd, SPI_IOC_MESSAGE(1), &msg);
		if (ret < 1) {
			printf("Can't send spi message\n");
			return ret;
		}
	}

	while(_is_busy());

	return 0;
}

/* Set max speed */
void l6740_set_maxspeed(uint32_t left, uint32_t right)
{
	int ret;
	int i;
	char tx[MSG_SIZE];
	char rx[MSG_SIZE];

	_init();

	if (fd < 0)
		return;

	memset(tx, NOPE, sizeof(tx));
	memset(rx, NOPE, sizeof(rx));

	while(_is_busy());

	tx[0] = SETMAXSPEED;
	tx[1] = SETMAXSPEED;
	tx[2] = (left >> 8) & 0x3;
	tx[3] = (right >> 8) & 0x3;
	tx[4] = left & 0xFF;
	tx[5] = right & 0xFF;

	for (i = 0; i < 3; i++) {
		struct spi_ioc_transfer msg[1] = {
			{
				.tx_buf = (unsigned long)tx + (i * DAISYCHAIN),
				.rx_buf = (unsigned long)rx + (i * DAISYCHAIN),
				.len    = DAISYCHAIN,
			}
		};

		ret = ioctl(fd, SPI_IOC_MESSAGE(1), &msg);
		if (ret < 1)
			printf("Can't send spi message\n");
	}
}
