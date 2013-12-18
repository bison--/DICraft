import sys
import os
import subprocess

dcmFilePath = "./multiImageTest"
destPath = "./tmp"
destFormat = ".png"
dcmFiles = []
if len(sys.argv) > 1:
	dcmFilePath = sys.argv[1]
	dcmFilesTmp = os.listdir(dcmFilePath)
	dcmFilesTmp.sort()
	
	for i in range(len(dcmFilesTmp)):
		if dcmFilesTmp[i].lower().endswith(".dcm"):
			dcmFiles.append( [os.path.join(dcmFilePath, dcmFilesTmp[i]), dcmFilesTmp[i]])
	
	cnt = 0
	totalFiles = len(dcmFiles)
	for fileInfo in dcmFiles:
		# TODO: if dcmj2pnm does not exist
		# OSError: [Errno 2] No such file or directory
		cnt += 1
		print cnt, "/", totalFiles
		output = subprocess.check_output(["dcmj2pnm", "+on", fileInfo[0], os.path.join(destPath, fileInfo[1] + destFormat)])

