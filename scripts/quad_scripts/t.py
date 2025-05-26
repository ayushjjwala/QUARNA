#Script to run main.py on the .out files present in portal/scripts/bpfind/<pdb>/
import os

a = os.listdir("bpfind/output/")

for f in a:
	print f
	os.system("python quad_scripts/main.py "+f)