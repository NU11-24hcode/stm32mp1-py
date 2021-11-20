/* X11 draw simulator
 * Notes:
 * - the draw.c source code is included here to avoid code duplication and
 *   to be as close as possible to a "real" case.
 * - millimeters in "real" are equal to pixels in this simulator.
 */

#include "draw.c"

#include <X11/Xlib.h>

static int x11_initialized = 0;

static Display* display;
static Window win;			/* pointer to the newly created window.      */
static GC gc;				/* GC (graphics context) used for drawing    */

void xdraw_x11_init(void);
void xdraw_set_color(const char* color_name, int foreground);

/* Statistics */
static int   pen_is_up;
static float d_lines;
static int   nb_lines;
static float d_goto;
static int   nb_goto;

int wires_mm(float left, float right, float *wireL, float *wireR)
{
	struct kinematic next;

	*wireL = left;
	*wireR = right;

	/* Draw a x11 line by getting next x,y */
	xdraw_x11_init();

	next = current;
	next.left += left;
	next.right += right;
	lr2xy(&next);

	XDrawLine(display, win, gc, current.x, current.y, next.x, next.y);
	XFlush(display);
	XSync(display, False);

	/* Statistics */
	if (pen_is_up) {
		nb_goto++;
		d_goto += distance(next);
	} else {
		nb_lines++;
		d_lines += distance(next);
	}

	return 0;
}

void pen_up(void)
{
	xdraw_x11_init();

	xdraw_set_color("red", 1);

	/* Statistics */
	pen_is_up = 1;
	printf("Statistics: nb_lines %d nb_goto %d d_lines %.02f d_goto %.02f\n",
		   nb_lines, nb_goto, d_lines, d_goto);
}

void pen_down(void)
{
	xdraw_x11_init();

	xdraw_set_color("black", 1);

	/* Statistics */
	pen_is_up = 0;
}

void xdraw_set_color(const char* color_name, int foreground)
{
	Colormap screen_colormap;
	XColor col;
	Status s;

	screen_colormap = DefaultColormap(display, DefaultScreen(display));
	s = XAllocNamedColor(display, screen_colormap, color_name, &col, &col);
	if (s == BadColor) {
		fprintf(stderr, "bad color name %s, use black instead\n", color_name);
		s = XAllocNamedColor(display, screen_colormap, "black", &col, &col);
	}
	if (foreground)
		XSetForeground(display, gc, col.pixel);
	else
		XSetBackground(display, gc, col.pixel);
}

Window
create_simple_window(Display* display, int width, int height, int x, int y)
{
	int screen_num = DefaultScreen(display);
	int win_border_width = 2;
	Window win;

	/* create a simple window, as a direct child of the screen's */
	/* root window. Use the screen's black and white colors as   */
	/* the foreground and background colors of the window,       */
	/* respectively. Place the new window's top-left corner at   */
	/* the given 'x,y' coordinates.                              */
	win = XCreateSimpleWindow(display, RootWindow(display, screen_num),
							  x, y, width, height, win_border_width,
							  BlackPixel(display, screen_num),
							  WhitePixel(display, screen_num));

	/* make the window actually appear on the screen. */
	XMapWindow(display, win);

	/* flush all pending requests to the X server. */
	XFlush(display);
	long eventMask = StructureNotifyMask;
	XEvent evt;
	XSelectInput(display, win, eventMask);
	do {
		XNextEvent( display, &evt);
	} while (evt.type != MapNotify);

	return win;
}

GC
create_gc(Display* display, Window win, int reverse_video)
{
	GC gc;							/* handle of newly created GC.  */
	unsigned long valuemask = 0;	/* which values in 'values' to  */
									/* check when creating the GC.  */
	XGCValues values;				/* initial values for the GC.   */
	unsigned int line_width = 4;	/* line width for the GC.       */
	int line_style = LineSolid;		/* style for lines drawing and  */
	int cap_style  = CapButt;		/* style of the line's edje and */
	int join_style = JoinBevel;		/*  joined lines. */
	int screen_num = DefaultScreen(display);

	gc = XCreateGC(display, win, valuemask, &values);
	if (gc < 0) {
		fprintf(stderr, "XCreateGC error\n");
		exit(1);
	}

	/* allocate foreground and background colors for this GC. */
	if (reverse_video) {
		XSetForeground(display, gc, WhitePixel(display, screen_num));
		XSetBackground(display, gc, BlackPixel(display, screen_num));
	} else {
		XSetForeground(display, gc, BlackPixel(display, screen_num));
		XSetBackground(display, gc, WhitePixel(display, screen_num));
	}

	/* define the style of lines that will be drawn using this GC. */
	XSetLineAttributes(display, gc,
					   line_width, line_style, cap_style, join_style);

	/* define the fill style for the GC. to be 'solid filling'. */
	XSetFillStyle(display, gc, FillSolid);

	return gc;
}

void xdraw_x11_init(void)
{
	char *display_name;

	if (x11_initialized)
		return;

	display_name = getenv("DISPLAY");  /* address of the X display. */

	display = XOpenDisplay(display_name);
	if (display == NULL) {
		fprintf(stderr, "Cannot connect to X server %s\n", display_name);
		exit(1);
	}

	win = create_simple_window(display, current.width, current.height, 0, 0);
	gc = create_gc(display, win, 0);
	XSync(display, False);

	x11_initialized = 1;

	/* Display the drawing area */
	xdraw_set_color("gray", 1);
	XFillRectangle(display, win, gc, 0, 0, current.width, current.height);
	xdraw_set_color("white", 1);
	XFillRectangle(display, win, gc, current.da_x0, current.da_y0,
				   current.da_w, current.da_h);
	xdraw_set_color("green", 1);
	XDrawRectangle(display, win, gc, current.da_x0, current.da_y0,
				   current.da_w, current.da_h);
	XFlush(display);
	XSync(display, False);

	/* Statistics */
	pen_is_up = 0;
	d_lines = 0;
	nb_lines = 0;
	d_goto = 0;
	nb_goto = 0;
}
