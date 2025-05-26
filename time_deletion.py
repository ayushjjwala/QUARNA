import time
import os

def check_time(folder):
	make_time = os.stat(folder).st_mtime
	current_time = time.time()
	return current_time - make_time

while 1:
	folder = 'scripts/bpfind/output/'
	for somefile in os.listdir(folder):
		if check_time(folder+somefile) > 1800:
			try:
				print('remove %s'%folder+somefile)
				os.system('rm -r ' + folder + somefile)
				print('remove media/output/%s'%somefile + '.zip')
				os.system('rm media/output/'+somefile+'.zip')
				print('remove media/input/%s'%somefile + '.pdb')
				os.system('rm media/input/%s'%somefile + '.pdb')
			except:
				pass
	
	folders = ['media/output/cyclic/','media/output/linear/','media/output/star/','media/output/semi_cyclic/','media/output/specific_residue/']
	for folder in folders:
		for somefile in os.listdir(folder):
			if check_time(folder+somefile) > 5:
				try:
					print('remove %s'%folder+somefile)
					os.system('rm ' + folder + somefile)
				except:
					pass



