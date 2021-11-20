#ifndef DRAW_H
#define DRAW_H

int draw_init(void);
int draw_set_drawing_area(float x0, float y0, float width, float height);
int draw_get_drawing_area(float* x0, float* y0, float* width, float* height);
int draw_goto(float x_in_drawing_area, float y_in_drawing_area);
int draw_line(float x_in_drawing_area, float y_in_drawing_area);
int draw_home(void);
int draw_close(void);
#endif
