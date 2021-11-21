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

int main(int argc, char **argv)
{
    if(argc == 2) {
		NSVGimage* g_image = NULL;
        g_image = nsvgParseFromFile(argv[1], "px", 96.0f);
	    if (g_image == NULL) {
		    printf("Could not open SVG image.\n");
		    return -1;
	    }

		FILE* fp = fopen("coordinates.txt", "w+");

		NSVGshape* shape;
		NSVGpath* path;

		for (shape = g_image->shapes; shape != NULL; shape = shape->next) {
			printf("Name of the shape : %s\n", shape->id);
			fprintf(fp, "%s\n", shape->id);
			for (path = shape->paths; path != NULL; path = path->next) {
				printf("Number of points : %d\n", path->npts);
				fprintf(fp, "NEXT\n");
				for(int i=0; i<path->npts; i++) {
					printf("Coordinates : %.2f\n", path->pts[i]);
					fprintf(fp, "%.2f\n", path->pts[i]);
				}
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
