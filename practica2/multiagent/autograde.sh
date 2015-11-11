#! /bin/sh -
while test $# -gt 0
do
	case "$1" in
		1) python autograder.py -q q1 --no-graphics 
			;;
		2) python autograder.py -q q2 --no-graphics 
			;;
		3) python autograder.py -q q3 --no-graphics 
			;;
		4) python autograder.py -q q4 --no-graphics 
			;;
		5) python autograder.py -q q5 --no-graphics 
			;;
		-hlep) echo "Usage: \n\t$ sh autograder.sh 2 3 - if you want to autograde questions 2 and 3"
			;;
		-all) python autograder.py
	esac
	shift
done

exit 0
