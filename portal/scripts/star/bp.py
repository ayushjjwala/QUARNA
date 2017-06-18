import sys

args = sys.argv
cb = args[1]
b1 = args[2]
res = [cb,b1]
orient = args[3]
dataset = args[4]

fo = open("dataset/star/"+dataset,"r+")
a = fo.readlines()
a = [x for x in a if x!='\n']
store = {}

for i in xrange(len(a)):
	if '-----------' in a[i]:
		pdb = a[i].split('-----------')[1]
		store[pdb] = []
	# elif len(a[i])==58:
	# 	continue
	elif "Star:" in a[i]:
	# else:
		checker_1 = [(a[i][6]+a[i][13]).upper(), (a[i][8]+a[i][14]).upper()]
		checker_2 = [(a[i][6]+a[i][17]).upper(), (a[i][9]+a[i][18]).upper()]
		checker_3 = [(a[i][6]+a[i][21]).upper(), (a[i][10]+a[i][22]).upper()]

		orient_checker_1 = a[i][15]
		orient_checker_2 = a[i][19]
		orient_checker_3 = a[i][23]
		if (checker_1 == res and orient_checker_1==orient) or (checker_2 == res and orient_checker_2 == orient) or (checker_3 == res and orient_checker_3 == orient):
			store[pdb].append(a[i-1] + a[i])

for pdb in store:
	if store[pdb]!=[]:
		print '-----------'+pdb+'-----------'
		for mol in store[pdb]:
			print mol