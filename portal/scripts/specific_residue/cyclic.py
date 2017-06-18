import sys

args = sys.argv
res = args[1:5]
res.sort()

fo = open('dataset/cyclic/' + args[5],'r+')
a = fo.readlines()
a = [x for x in a if x!='\n']
store = {}

for i in xrange(len(a)):
	if '-----------' in a[i]:
		pdb = a[i].split('-----------')[1]
		store[pdb] = []
	# elif len(a[i])==43:
	# 	continue
	elif "Cyclic-4:" in a[i]:
	# else:
		checker = sorted(a[i][10:14])
		if checker == res[0:4]:
			store[pdb].append(a[i-2]+a[i-1]+a[i])

for pdb in store:
	if store[pdb]!=[]:
		print '-----------'+pdb+'-----------'
		for mol in store[pdb]:
			print mol