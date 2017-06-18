import sys

args = sys.argv
cb = args[1]
b1 = args[2]
res = [cb,b1]
orient = args[3]
dataset = args[4]

fo = open("dataset/semi_cyclic/"+dataset,"r+")
a = fo.readlines()
a = [x for x in a if x!='\n']
store = {}

for i in xrange(len(a)):
	if '-----------' in a[i]:
		pdb = a[i].split('-----------')[1]
		store[pdb] = []
	# elif len(a[i])==64 or len(a[i])==51:
	# 	continue
	elif "Cyclic-3:" in a[i]:
	# else:
		checker_1 = [(a[i][10]+a[i][19]).upper(), (a[i][13]+a[i][20]).upper()]
		checker_2 = [(a[i][10]+a[i][23]).upper(), (a[i][14]+a[i][24]).upper()]
		checker_3 = [(a[i][10]+a[i][27]).upper(), (a[i][16]+a[i][28]).upper()]
		checker_4 = [(a[i][13]+a[i][31]).upper(), (a[i][14]+a[i][32]).upper()]

		orient_checker_1 = a[i][21]
		orient_checker_2 = a[i][25]
		orient_checker_3 = a[i][29]
		orient_checker_4 = a[i][33]
		if (checker_1 == res and orient_checker_1==orient) or (checker_2 == res and orient_checker_2 == orient) or (checker_3 == res and orient_checker_3 == orient) or (checker_4 == res and orient_checker_4 == orient):
			store[pdb].append(a[i-2] + a[i-1] + a[i])

for pdb in store:
	if store[pdb]!=[]:
		print '-----------'+pdb+'-----------'
		for mol in store[pdb]:
			print mol