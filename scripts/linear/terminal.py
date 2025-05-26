import sys

args = sys.argv
b1 = args[1]
b2 = args[2]
res = [b1,b2]
res.sort()
orient = args[3]
dataset = args[4]

fo = open("dataset/linear/"+dataset,"r+")
a = fo.readlines()
a = [x for x in a if x!='\n']
store = {}

for i in xrange(len(a)):
	if '-----------' in a[i]:
		pdb = a[i].split('-----------')[1]
		store[pdb] = []
	# elif len(a[i])==72:
	# 	continue
	elif "Linear:" in a[i]:
	# else:
		checker_1 = [(a[i][8]+a[i][13]).upper(), (a[i][9]+a[i][14]).upper()]
		checker_2 = [(a[i][10]+a[i][21]).upper(), (a[i][11]+a[i][22]).upper()]
		checker_1.sort()
		checker_2.sort()
		orient_checker_1 = a[i][15]
		orient_checker_2 = a[i][23]
		if (checker_1 == res and orient_checker_1==orient) or (checker_2 == res and orient_checker_2 == orient):
			store[pdb].append(a[i-1] + a[i])

for pdb in store:
	if store[pdb]!=[]:
		print '-----------'+pdb+'-----------'
		for mol in store[pdb]:
			print mol