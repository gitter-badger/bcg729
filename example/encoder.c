/*
 encoderTest.c

 Copyright (C) 2011 Belledonne Communications, Grenoble, France
 Author : Johan Pascal
 
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 as published by the Free Software Foundation; either version 2
 of the License, or (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
 */
/*****************************************************************************/
/*                                                                           */
/* Test Program for encoder                                                  */
/*    Input: the reconstructed signal : each frame (80 16 bits PCM values)   */
/*           on a row of a text CSV file                                     */
/*    Output: 15 parameters on each row of a text CSV file.                  */
/*                                                                           */
/*****************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <time.h>


#include "typedef.h"
#include "codecParameters.h"
#include "utils.h"

#include "bcg729/encoder.h"


int main(int argc, char *argv[] )
{
	/*** input and output file pointers ***/
	FILE *fpBinInput;
	FILE *fpBinOutput;

	/*** input and output buffers ***/
	int16_t inputBuffer[L_FRAME]; /* output buffer: the signal */ 
	uint8_t bitStream[10]; /* binary output of the encoder */

	char *inputFile = malloc(512);
	char *outputFile = malloc(512);

	/*** inits ***/

	/* open the input file */
        sprintf(inputFile, "%s", argv[1]);
	if ((fpBinInput = fopen(inputFile, "rb")) == NULL) {
		printf("%s - Error: can't open file  %s\n", argv[0], argv[1]);
		exit(-1);
	}

	/* create the output file(filename is the same than input file with the .out extension) */
	sprintf(outputFile, "%s.out", argv[1]);
	if ( (fpBinOutput = fopen(outputFile, "wb")) == NULL) {
		printf("%s - Error: can't create file  %s\n", argv[0], outputFile);
		exit(-1);
	}
	
	/*** init of the tested bloc ***/
	bcg729EncoderChannelContextStruct *encoderChannelContext = initBcg729EncoderChannel();

	/*** initialisation complete ***/
	/* perf measurement */
	clock_t start, end;
	double cpu_time_used=0.0;
	int framesNbr =0;

	/*** loop over input file ***/
	while(1)
	{
		if (fread(inputBuffer, sizeof(int16_t), L_FRAME, fpBinInput) != L_FRAME) {
			break;
		}

		framesNbr++;

		start = clock();
		bcg729Encoder(encoderChannelContext, inputBuffer, bitStream);
		end = clock();

		cpu_time_used += ((double) (end - start));

		fwrite(bitStream, sizeof(uint8_t), 10, fpBinOutput);
	}
	closeBcg729EncoderChannel(encoderChannelContext);

	/* Perf measurement: uncomment next line to print cpu usage */
	printf("Encode %d frames in %f seconds : %f us/frame\n", framesNbr, cpu_time_used/CLOCKS_PER_SEC, cpu_time_used*1000000/((double)framesNbr*CLOCKS_PER_SEC));

	/* perf measurement */
	exit (0);
}

