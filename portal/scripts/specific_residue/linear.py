import sys

args = sys.argv
res = args[1:5]
res.sort()

fo = open('dataset/linear/' + args[5],'r+')
a = fo.readlines()
a = [x for x in a if x!='\n']
store = {}

for i in xrange(len(a)):
	if '-----------' in a[i]:
		pdb = a[i].split('-----------')[1]
		store[pdb] = []
	# elif len(a[i])>71:
	# 	continue
	elif "Linear:" in a[i]:
	# else:
		checker = sorted(a[i][8:12])
		if checker == res[0:4]:
			store[pdb].append(a[i-1]+a[i])

for pdb in store:
	if store[pdb]!=[]:
		print '-----------'+pdb+'-----------'
		for mol in store[pdb]:
			print mol

