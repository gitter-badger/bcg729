#!/usr/bin/python
# testCampaign.py
#
# Copyright (C) 2014
# Author : Vitold Sedyshev
#
# Copyright (C) 2011 Belledonne Communications, Grenoble, France
# Author : Johan Pascal
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# This script allow testing of g729 encoder/decoder functional blocs
# by default each bloc output is supposed to be identical to the pattern
# it can be configured to monitor and accept a (setable) difference between output
# and pattern(which can occur if a bloc or macros are modified).
# Tune the defaultMaxDiff associative array definition to modify
# the behavior of this script for any functional bloc under test

import os
import os.path
import sys
import subprocess
import difflib

binDirectory = "./src/"
patternDirectory = "./patterns"

def softDiff(self, filename1, filename2, maxDiff, percentMaxDiff, printStats):
        """ softDiff: compare two CSV files with a margin of acceptance between the values found
        arguments : file1, file2, maximumDiff tolerated(value), maximum percentage abs((val1-val2)/val1)*100 tolerated
        maximum condition ignored when set to 0 so it might be used:
        - with one maximum condition
        - with both maximum condition : trigger a warning if both maxima are exceded
        """
	# open the file1 and file2
	FP1 = open(filename1, "r")
	FP2 = open(filename2, "r")

	# remove path from filename2 as it might be used in error report
        filename2 = os.path.basename(filename2)

	# total values number count variables for stats
	nbr_values = 0
	total_diff = 0
	total_values = 0
	maxMaxDiff = 0
	maxPercentDiff = 0

	# boolean for return value: 0 no warning, 1 warning(s)
	warnings  = 0

	# loop over file1
        lineNb = 0
	while True:
                FP1_line = FP1.read()
                FP2_line = FP2.read()
                if not FP1_line:
                    break
                if not FP2_line:
                    break
		# get line number to display in potential message 
		lineNb += 1
		# get file1 and file2 CSV line into an array
		line1 = FP1_line.split (',')
		line2 = FP2_line.split (',')

		# check they have the same number of values
		line1length = len(line1)
		line2length = len(line2)
		if (line1length != line2length):
			raise Exception("at line {}, {} and $filename2 doesn't have the same number of values".format(lineNb, filename1, filename2))

		# loop on the values and compare them
		for i in xrange(0, line1length):
			v1 = int( line1[i].strip() )
			v2 = int( line2[i].strip() )
			diff = abs(v1 - v2)
			
			percentDiff = None
			if (abs(line1[i]) + abs(line2[i])) == 0:
				percentDiff = 0
			else:
				percentDiff = diff / (abs(line1[i])+abs(line2[i]))*200
			

			# Stats if needed 
			if printStats:
				# increment values counts
				nbr_values += 1
				total_diff += diff
				total_values += (abs(line1[i])+abs(line2[i])) / 2
				if diff > maxMaxDiff:
					maxMaxDiff = diff
					maxPercentDiff = percentDiff
			
			if (maxDiff > 0) or (percentMaxDiff> 0):
				if ((diff > maxDiff) or (percentDiff > percentMaxDiff)):
					warnings = 1
					print "WARNING : {}: line {} value {} ({} and {}) differ by {} ({} %)".format(filename2, lineNb, i, line1[i], line2[i], diff, percentDiff)
			else:
				# on a une ou zero condition */
				if (maxDiff > 0):
					# if we shall check the absolute value difference 
					if (diff > maxDiff):
						warnings = 1
						print "WARNING : {}: line {} value {} ({} and {}) differ by {}".format(filename2, lineNb, i, line1[i], line2[i], diff)
				if (percentMaxDiff > 0):
					# if we shall check the percentage of difference 
					if (percentDiff > percentMaxDiff):
						warnings = 1
						print "WARNING : {}: line {}. value {} ({} and {}) differ by {}%".format(filename2, lineNb, i, line1[i], line2[i], percentDiff)
	FP1.close()
	FP2.close()

	if printStats:
            print "Stats: Max Diff: %d(%f) mean diff: %0.3f mean percent diff : %0.2f" % (maxMaxDiff, maxPercentDiff, total_diff/nbr_values, total_diff*100/total_values)

	return warnings

def diff(name1, name2):
    FP1 = open(name1, "r")
    FP2 = open(name2, "r")
    FP1_lines = FP1.readlines()
    FP2_lines = FP2.readlines()
    FP1.close()
    FP2.close()

    differs = "\n".join( difflib.unified_diff(FP1_lines, FP2_lines) )
    print differs

    return differs

def main():
    ARGV = sys.argv[1:]
    ARGVlength = len(ARGV)
    if (ARGVlength < 1) or (ARGVlength > 2):
	print "##############################################################################"
	print "#                                                                            #"
	print "#  testCampaign [-s] <test name>                                             #"
	print "#     test name in the following list :                                      #"
	print "#       - decoder                                                            #"
	print "#       - decodeLSP                                                          #"
	print "#       - interpolateqLSPAndConvert2LP                                       #"
	print "#       - decodeAdaptativeCodeVector                                         #"
	print "#       - decodeFixedCodeVector                                              #"
	print "#       - decodeGains                                                        #"
	print "#       - LPSynthesisFilter                                                  #"
	print "#       - postFilter                                                         #"
	print "#       - postProcessing                                                     #"
	print "#                                                                            #"
	print "#       - encoder                                                            #"
	print "#       - preProcessing                                                      #"
	print "#       - computeLP                                                          #"
	print "#       - LP2LSPConversion                                                   #"
	print "#       - LSPQuantization                                                    #"
	print "#       - computeWeightedSpeech                                              #"
	print "#       - findOpenLoopPitchDelay                                             #"
	print "#       - adaptativeCodebookSearch                                           #"
	print "#       - computeAdaptativeCodebookGain                                      #"
	print "#       - fixedCodebookSearch                                                #"
	print "#       - gainQuantization                                                   #"
	print "#                                                                            #"
	print "#       - all : perform all tests                                            #"
	print "#     Options switch:                                                        #"
	print "#       -s : Display stats on each test (when running softDiff)              #"
	print "#                                                                            #"
	print "##############################################################################"
	return

    # check command validity
    # TODO

    printStats = 0

    # Get the test name
    command = ARGV[ARGVlength - 1]

    # is there a switch?
    if (ARGV[0] == "-s"):
	printStats= 1

    # define the default values to use for maxDiff and percentualMaxDiff for each test
    # "<testedBlocName> => [<absolut maximum difference>,<percentual maximum difference>]"
    # if both set to 0, the diff command will be used
    defaultMaxDiff = {	"preProcessing"                 : [0,0],
			"computeLP"                     : [0,0],
			"LP2LSPConversion"              : [0,0],
			"LSPQuantization"               : [0,0],
			"computeWeightedSpeech"         : [0,0],
			"findOpenLoopPitchDelay"        : [0,0],
			"adaptativeCodebookSearch"      : [0,0],
			"computeAdaptativeCodebookGain" : [0,0],
			"fixedCodebookSearch"           : [0,0],
			"gainQuantization"              : [0,0], 
			"encoder"                       : [0,0], 

			"decodeLSP"                     : [0,0],
			"interpolateqLSPAndConvert2LP"  : [0,0],
			"decodeAdaptativeCodeVector"    : [0,0],
			"decodeFixedCodeVector"         : [0,0],
			"decodeGains"                   : [0,0],
			"LPSynthesisFilter"             : [0,0],
			"postFilter"                    : [0,0],
			"postProcessing"                : [0,0],
			"decoder"                       : [0,0]
		}


    # check command: 
    if command == "all":
        # if run all tests, just get the defaultMaxDiff array as testsList as the test directory are retrieved from keys
	testsList = defaultMaxDiff
    else:
        # we run one test: create an associative array with one element having a key matching the test name
	testsList = { command: 0 } 

    #return value for autotools make check
    exitVal = 0

    for testDirectory in testsList.keys():
	# get the files
        files = []
        for fn in os.listdir("{}/{}".format(patternDirectory, testDirectory)):
            if fn.endswith(".in"):
                files.append(fn)
	testExec = os.path.abspath(os.path.join(binDirectory, testDirectory + "Test"))

	print "Test {} block".format(testDirectory)

	# for each *.in file found in the test directory
	for fn in files:
		# run the testExecutable
		filebase = os.path.basename(fn)
                print "    {} ... ".format(filebase)
		cmd = "{} {}/{}/{}".format(testExec, patternDirectory, testDirectory, fn)
                subprocess.check_output(cmd)

		# compare the output file with the pattern file
		filepattern = fn.replace(".in", ".pattern")
		fileout = fn.replace(".in", ".out")

		maxDiffTolerated = defaultMaxDiff[testDirectory][0];
		maxPercentualDiffTolerated = defaultMaxDiff[testDirectory][1]
		if ((maxDiffTolerated == 0) and (maxPercentualDiffTolerated == 0)):
			# no difference accepted, use the classic diff function
                        name1 = "{}/{}/{}".format(patternDirectory, testDirectory, filepattern)
                        name2 = "{}/{}/{}".format(patternDirectory, testDirectory, fileout)
                        differs = diff(name1, name2)
			if differs != "":
				print "RESULT: FAIL ... ";
				exitVal = 1
			else:
				print "RESULT: SUCCESS"
		else:
                # accept difference => use the softDiff function
			if softDiff(patternDirectory + "/" + testDirectory + "/" + filepattern, patternDirectory + "/" + testDirectory + "/" + fileout, maxDiffTolerated, maxPercentualDiffTolerated, printStats) == 0:
				print "  ... Pass"
			else:
				print "  {}  ... {}".format(filebase, "FAIL")
				exitVal = 1
    return exitVal


if __name__ == "__main__":
    sys.exit(main())
