set -e # Exit on error

python autograder.py -q q1
python autograder.py -q q2
# python autograder.py -q q3 -> UCS that we didn't implement
python autograder.py -q q4
python autograder.py -q q5
python autograder.py -q q6
python autograder.py -q q7
