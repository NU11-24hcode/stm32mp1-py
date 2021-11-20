#include <stdint.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "draw.h"
#include "wires.h"
#include "pen.h"

/* Default paperboard sizes (width is the distance between the 2 motors */
#define PAPERBOARD_WIDTH_MM   675.0
#define PAPERBOARD_HEIGHT_MM  880.0

/* Default scale factor between the paperboard surface and the drawing area.
 * It helps to define the drawing area where drawing are "perfect" vs.
 * areas where the drawing could be distorted... */
#define DRAWING_AREA_SCALING_FACTOR (float)0.6

/* Default line step size */
#define MAX_LENGTH_MM (float)2.0

#define PI 3.14159265

/* struct kinematic
 * @width,height: width,height of drawing surface
 * @x,y: x,y coordonate
 * @left,right: wires length
 * @da_x0,da_y0,da_w,da_h: drawing area inside the drawing surface
 */
struct kinematic {
	float width, height;
	float x, y;
	float left, right;
	float da_x0, da_y0, da_w, da_h;
};

static struct kinematic current;

static void kinematic_dump(struct kinematic k)
{
	printf("(w,h) %.2f,%.2f (x,y) %.2f,%.2f (left,right) %.2f,%.2f\n",
		   k.width, k.height, k.x, k.y, k.left, k.right);
}

/* inverse kinematics: (x,y) to (l,r) length */
static void xy2lr(struct kinematic *k)
{
	float x = k->x;
	float y = k->y;

	k->left = sqrt((x*x) + (y*y));

	x = k->width - k->x;
	k->right = sqrt((x*x) + (y*y));
}

/* forward kinematics: (l,r) to (x,y) */
static void lr2xy(struct kinematic *k)
{
	float theta = acos(((k->left * k->left) + (k->width * k->width) - (k->right * k->right)) / (2 * k->left * k->width));
	float alpha = PI / 2 - theta;

	k->x = sin(alpha) * k->left;
	k->y = cos(alpha) * k->left;
}

int draw_set_drawing_area(float x0, float y0, float width, float height)
{
	/* Quick checks of the given drawing area */
	/* TODO be more restrictive, by adding a mechanical secure area? */
	if (x0 < 0.0 || x0 > current.width ||
		y0 < 0.0 || y0 > current.height ||
		width < 0.0 || width > current.width ||
		height < 0.0 || height > current.height) {

		printf("bad drawing area\n");
		return -1;
	}

	current.da_x0 = x0;
	current.da_y0 = y0;
	current.da_w = width;
	current.da_h = height;

	/* printf("drawing area: (%.2f,%.2f) %.2f x %.2f\n",
		   current.da_x0, current.da_y0, current.da_w, current.da_h);*/

	return 0;
}

int draw_get_drawing_area(float* x0, float* y0, float* width, float* height)
{
	/* TODO check if draw_set_drawing_area() has been called at least once */

	*x0 = current.da_x0;
	*y0 = current.da_y0;
	*width = current.da_w;
	*height = current.da_h;

	return 0;
}

int draw_init(void)
{
	float x0, y0, w, h;
	float width, height;

	width = PAPERBOARD_WIDTH_MM;
	height = PAPERBOARD_HEIGHT_MM;

	current.width = width;
	current.height = height;
	current.x = width / 2;
	current.y = height / 2;
	xy2lr(&current);

	/* By default the drawing area inside the drawing surface is downscaled */
	/* Note: you can call draw_set_drawing_area() to adjust this area */
	w = width * DRAWING_AREA_SCALING_FACTOR;
	h = height * DRAWING_AREA_SCALING_FACTOR;
	x0 = (width - w) / 2.0;
	y0 = (height - h) / 2.0;

	draw_set_drawing_area(x0, y0, w, h);

	printf("Before continuing, please adjust left wire length to %.0fmm & right wire length to %.0fmm\n",
			current.left, current.right);
	kinematic_dump(current);

	return 0;
}

int draw_close()
{
	return 0;
}

/* Move from current to next position */
static void draw_move(struct kinematic next)
{
	float l, r;

	kinematic_dump(next);
	wires_mm(next.left - current.left, next.right - current.right, &l, &r);

	/* We may haven't move exactly we are suppose to so adjust
	 * our position
	 */
	current.left += l;
	current.right += r;
	lr2xy(&current);
}

/* draw_goto - go to X,Y without drawing */
int draw_goto(float x, float y)
{
	struct kinematic next;

	x += current.da_x0;
	y += current.da_y0;

	next.width = current.width;
	next.height = current.height;
	next.x = x;
	next.y = y;
	xy2lr(&next);

	pen_up();
	draw_move(next);

	return 0;
}

static __attribute__ ((unused)) float distance(struct kinematic to)
{
	return sqrt((to.x - current.x)*(to.x - current.x) +
				(to.y - current.y)*(to.y - current.y));
}

/* draw_line - draw a line from the current position to X,Y */
int draw_line(float x, float y)
{
	struct kinematic to;

	x += current.da_x0;
	y += current.da_y0;

	to.width = current.width;
	to.height = current.height;
	to.x = x;
	to.y = y;
	xy2lr(&to);

	draw_move(to);

	return 0;
}

int draw_home(void)
{
	/* Move to the drawing area top-left corner (mechanically "secure" home) */
	return draw_goto(0, 0);
}
