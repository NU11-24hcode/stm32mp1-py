//
// Copyright (c) 2013 Mikko Mononen memon@inside.org
//
// This software is provided 'as-is', without any express or implied
// warranty.  In no event will the authors be held liable for any damages
// arising from the use of this software.
// Permission is granted to anyone to use this software for any purpose,
// including commercial applications, and to alter it and redistribute it
// freely, subject to the following restrictions:
// 1. The origin of this software must not be misrepresented; you must not
//    claim that you wrote the original software. If you use this software
//    in a product, an acknowledgment in the product documentation would be
//    appreciated but is not required.
// 2. Altered source versions must be plainly marked as such, and must not be
//    misrepresented as being the original software.
// 3. This notice may not be removed or altered from any source distribution.
//

/*
	This code was taken from https://github.com/memononen/nanosvg
	and adapted to our needs
*/

#include <stdio.h>
#include <string.h>
#include <float.h>

#define NANOSVG_IMPLEMENTATION
#include "nanosvg.h"

#include "../c/src/draw.h"

static float distPtSeg(float x, float y, float px, float py, float qx, float qy)
{
	float pqx, pqy, dx, dy, d, t;
	pqx = qx-px;
	pqy = qy-py;
	dx = x-px;
	dy = y-py;
	d = pqx*pqx + pqy*pqy;
	t = pqx*dx + pqy*dy;
	if (d > 0) t /= d;
	if (t < 0) t = 0;
	else if (t > 1) t = 1;
	dx = px + t*pqx - x;
	dy = py + t*pqy - y;
	return dx*dx + dy*dy;
}

static void cubicBez(float x1, float y1, float x2, float y2,
					 float x3, float y3, float x4, float y4,
					 float tol, int level, FILE* fp)
{
	float x12,y12,x23,y23,x34,y34,x123,y123,x234,y234,x1234,y1234;
	float d;
	
	if (level > 12) return;

	x12 = (x1+x2)*0.5f;
	y12 = (y1+y2)*0.5f;
	x23 = (x2+x3)*0.5f;
	y23 = (y2+y3)*0.5f;
	x34 = (x3+x4)*0.5f;
	y34 = (y3+y4)*0.5f;
	x123 = (x12+x23)*0.5f;
	y123 = (y12+y23)*0.5f;
	x234 = (x23+x34)*0.5f;
	y234 = (y23+y34)*0.5f;
	x1234 = (x123+x234)*0.5f;
	y1234 = (y123+y234)*0.5f;

	d = distPtSeg(x1234, y1234, x1,y1, x4,y4);
	if (d > tol*tol) {
		cubicBez(x1,y1, x12,y12, x123,y123, x1234,y1234, tol, level+1, fp); 
		cubicBez(x1234,y1234, x234,y234, x34,y34, x4,y4, tol, level+1, fp); 
	} else {
		printf("(%.2f,%.2f)\n",x4, y4);
		fprintf(fp, "%.2f,%.2f\n", x4, y4);
	}
}

void drawPath(float* pts, int npts, char closed, float tol, FILE* fp)
{
	int i;
	printf("(%.2f,%.2f)",pts[0], pts[1]);
	fprintf(fp, "NEXT\n%.2f,%.2f\n", pts[0], pts[1]);
	for (i = 0; i < npts-1; i += 3) {
		float* p = &pts[i*2];
		cubicBez(p[0],p[1], p[2],p[3], p[4],p[5], p[6],p[7], tol, 0, fp);
	}
	if (closed) {
		printf("(%.2f,%.2f)\n",pts[0], pts[1]);
		fprintf(fp, "%.2f,%.2f\n", pts[0], pts[1]);
	}
}

int main(int argc, char **argv)
{
    if(argc == 2) {
		NSVGimage* g_image = NULL;
        g_image = nsvgParseFromFile(argv[1], "mm", 96.0f);
	    if (g_image == NULL) {
		    printf("Could not open SVG image.\n");
		    return -1;
	    }

		FILE* fp = fopen("coordinates.txt", "w+");

		NSVGshape* shape;
		NSVGpath* path;

		for (shape = g_image->shapes; shape != NULL; shape = shape->next) {
			printf("Name of the shape : %s\n", shape->id);
			//fprintf(fp, "%s\n", shape->id);
			for (path = shape->paths; path != NULL; path = path->next) {
				printf("Number of points : %d\n", path->npts);
				//fprintf(fp, "NEXT\n");
				/*for(int i=0; i<path->npts; i++) {
					printf("Coordinates : %.2f\n", path->pts[i]);
					fprintf(fp, "%.2f\n", path->pts[i]);
				}*/
				drawPath(path->pts, path->npts, path->closed, 1.5f, fp);
			}
		}
		fclose(fp);

	    nsvgDelete(g_image);
    } else {
        printf("Error, no SVG file was passed as a parameter");
        return -1;
    }

	return 0;
}
