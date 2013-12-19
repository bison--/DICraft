import sys
import os
import subprocess

formats = {".png":"+on", ".pgm":"+opw"}

dcmFilePath = "./multiImageTest"
destPath = "./tmp"
destFormat = ".pgm"
dcmFiles = []
clearTemp = True
if len(sys.argv) > 1:
	dcmFilePath = sys.argv[1]
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
			dcmFiles.append( [os.path.join(dcmFilePath, dcmFilesTmp[i]), dcmFilesTmp[i]])
	
	cntCurrentFile = 0
	totalFiles = len(dcmFiles)
	for fileInfo in dcmFiles:
		# TODO: if dcmj2pnm does not exist
		# OSError: [Errno 2] No such file or directory
		cntCurrentFile += 1
		print cntCurrentFile, "/", totalFiles
		output = subprocess.check_output(["dcmj2pnm", formats[destFormat], fileInfo[0], os.path.join(destPath, fileInfo[1] + destFormat)])

