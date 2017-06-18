import sys

args = sys.argv
b1 = args[1]
# e1 = args[2]
b2 = args[2]
# e2 = args[4]
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
		checker = [(a[i][9]+a[i][17]).upper(), (a[i][10]+a[i][18]).upper()]
		checker.sort()
		orient_checker = a[i][19]
		if checker == res and orient_checker==orient:
			store[pdb].append(a[i-1] + a[i])

for pdb in store:
	if store[pdb]!=[]:
		print '-----------'+pdb+'-----------'
		for mol in store[pdb]:
			print mol