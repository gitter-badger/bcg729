#!/bin/sh
# This script check if we have the tests patterns and download them if needed
# then run all available tests

# Do we have a patterns directory
if [ ! -d "patterns" ]; then
   # no pattern directory: download it from 
   # http://www.belledonne-communications.com/downloads/bcg729-patterns.zip
   wget http://www.belledonne-communications.com/downloads/bcg729-patterns.zip
   if [ -e bcg729-patterns.zip ]; then
	# check file
	if [[ `md5sum bcg729-patterns.zip | grep -c 75b4fb8b286485c375c9c326f8b9eb66` -ne 0 ]]; then
		# file ok, unzip it
		unzip bcg729-patterns.zip
	   	if [[ $? -ne 0 ]]; then
			echo "Error: unable to unzip correctly bcg729-patterns.zip, try to do it manually"
		else	
			rm bcg729-patterns.zip
		fi
	else
		echo "Error: bad checksum on bcg729-patterns.zip downloaded from http://www.belledonne-communications.com/downloads/.\nTry again"
		exit 1
	fi
   else
	echo "Error: Unable to download bcg729-patterns.zip pattern archive from http://www.belledonne-communications.com/downloads/"
	exit 1
   fi
fi

# run all the tests
./testCampaign all 
