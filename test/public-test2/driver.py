#!/usr/bin/python3
#####################################################
#############  LEAVE CODE BELOW  ALONE  #############
# Include base directory into path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..')))

# Import tester
from tester import failtest, passtest, assertequals, runcmd, preparefile, runcmdsafe
#############    END UNTOUCHABLE CODE   #############
#####################################################

###################################
# Write your testing script below #
###################################
python_bin = sys.executable
preparefile('./test.py')
preparefile('./test.while')
b_stdout, b_stderr, b_exitcode = runcmdsafe(f'{python_bin} ./test.py')

if b_exitcode == 0:
	passtest('')
else:
	failtest(b_stdout.decode('utf-8'))