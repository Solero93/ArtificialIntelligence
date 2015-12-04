#! /bin/sh -
while test $# -gt 0
do
	case "$1" in
		1) python autograder.py -q q1 
			;;
		2) python autograder.py -q q2 
			;;
		3) python autograder.py -q q3 
			;;
		4) python autograder.py -q q4 
			;;
		-hlep) echo "Usage: \n\t$ sh autograder.sh 2 3 - if you want to autograde questions 2 and 3"
			;;
		-all) python autograder.py
	esac
	shift
done

exit 0
