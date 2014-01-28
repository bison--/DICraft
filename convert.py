import sys
import os
import subprocess
import dicom

formats = {".png":"+on", ".pgm":"+opw", ".pnm":"+op"}

dcmFilePath = "./multiImageTest"
destPath = "./tmp"
destFormat = ".pnm"
dcmFiles = []
clearTemp = True
if len(sys.argv) > 1:
	dcmFilePath = sys.argv[1]

if len(sys.argv) > 2:
	destPath = sys.argv[2]
	
dcmFilesTmp = os.listdir(dcmFilePath)
dcmFilesTmp.sort()

if clearTemp:
	cntRemoved = 0
	for fil in os.listdir("tmp"):
		if not fil.endswith(".md"):
			#print os.path.join("tmp", fil)
			os.remove(os.path.join("tmp", fil))
	print "removed", cntRemoved, "files"


for i in range(len(dcmFilesTmp)):
	if dcmFilesTmp[i].lower().endswith(".dcm"):
		#dcm = dicom.load()
		dcmFiles.append( [os.path.join(dcmFilePath, dcmFilesTmp[i]), dcmFilesTmp[i]])

cntCurrentFile = 0
totalFiles = len(dcmFiles)
for fileInfo in dcmFiles:
	# TODO: if dcmj2pnm does not exist
	# OSError: [Errno 2] No such file or directory
	cntCurrentFile += 1
	print cntCurrentFile, "/", totalFiles
	output = subprocess.check_output(["dcmj2pnm", formats[destFormat], fileInfo[0], os.path.join(destPath, fileInfo[1] + destFormat)])

