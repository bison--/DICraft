import sys
import os
import subprocess

dirList = os.listdir(".")
for fname in dirList:
	if fname.endswith(".ui"):
		print "converting:", fname
		output = subprocess.check_output(["pyuic4", "-x", fname, "-o", fname.replace(".ui", ".py")])
		
print "conversion done"
#pyuic4 -x bodyDamage.ui -o bodyDamage.py
