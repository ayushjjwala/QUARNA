import sys
import copy
import os
import itertools as it

args = sys.argv
folder = args[1]
store = {}	# To store the triplets in a dictionary against pdb files
rep_checker_li_sq = {}	# To keep a check on repitition of quartets
linear_quartets = {}	# To store the linear quartets
sq_quartets = {}	# To store the square quartets
# cyclic_trip = {}
rep_checker_cy_trip= {}	# To store the cyclic triplets and check for repitition
rep_checker_st_tri = {}	# To store the star and cyclic-3 quartets and check for repitition
# visited = {}
# cc_list = {}
# cur_cc = []
star_quartets = {}	# To store the star quartets
tri_quartets = {}	# To store the cyclic-3 quartets with one link
tri_quartets2 = {}	# To store the cyclic-3 quartets with two links
tri_quartets3 = {}	# To store the cyclic-3 quartets with three links


# quin_topology = {'11222':'T1','12234':'T10','11114':'T11','11224':'T12','22224':'T13','13334':'T14','33334':'T15','22244':'T16','23344':'T17','33444':'T18','11123':'T2','44444':'T19','12223':'T3/T7','12333':'T4','11233':'T5','22233':'T6','22222':'T8','22334':'T9'}


FOLDER = "bpfind/output/"+folder+"/"
# FOLDER  = '../DataSet/' + args[1].lower() + '/pdb_' + args[1].lower() + '/'
pdb_list = os.listdir(FOLDER)
pdb_list = [x for x in pdb_list if x.endswith('.out')]
# pdb_list = [folder]

#	Make the length of the numeric strings equal by adding leading zeros
def norm(num):
	if len(num)==1:
		return '000'+num
	elif len(num)==2:
		return '00'+num
	elif len(num)==3:
		return '0'+num
	else:
		return num

#	Creating graph of the PDB file
def create_dict(pdb):
	fo = open(FOLDER+pdb+'.out','r+')
	a = fo.readlines()
	a = [x for x in a if x!='\n']
	if(pdb not in store):
		store[pdb] = {}
	for line in a:
		ele_list = line.split()
		ele_list = map(str.strip,ele_list)
		if (len(ele_list)==11) and ('BP' in ele_list[9]): #If it is a base pair
			key1 = norm(ele_list[0])+norm(ele_list[1])+ele_list[2]+ele_list[3]
			key2 = norm(ele_list[4])+norm(ele_list[5])+ele_list[6]+ele_list[7]
			if key1 not in store[pdb]:
				store[pdb][key1] = {}
			if key2 not in store[pdb]:
				store[pdb][key2] = {}
			store[pdb][key1][key2] = {'edge':ele_list[8][0].upper()+ele_list[8][2].upper(),'ori':ele_list[8][3]}
			store[pdb][key2][key1] = {'edge':ele_list[8][2].upper()+ele_list[8][0].upper(),'ori':ele_list[8][3]}

		elif len(ele_list)==18 and ('BP' in ele_list[9]) and (('TP' in ele_list[16]) or ('BF' in ele_list[16])): #If it is a triplet
			key1 = norm(ele_list[0])+norm(ele_list[1])+ele_list[2]+ele_list[3]
			key2 = norm(ele_list[4])+norm(ele_list[5])+ele_list[6]+ele_list[7]
			key3 = norm(ele_list[11])+norm(ele_list[12])+ele_list[13]+ele_list[14]
			if key1 not in store[pdb]:
				store[pdb][key1] = {}
			if key2 not in store[pdb]:
				store[pdb][key2] = {}
			if key3 not in store[pdb]:
				store[pdb][key3] = {}
			store[pdb][key1][key2] = {'edge':ele_list[8][0].upper()+ele_list[8][2].upper(),'ori':ele_list[8][3]}
			store[pdb][key2][key1] = {'edge':ele_list[8][2].upper()+ele_list[8][0].upper(),'ori':ele_list[8][3]}
			store[pdb][key1][key3] = {'edge':ele_list[15][0].upper()+ele_list[15][2].upper(),'ori':ele_list[15][3]}
			store[pdb][key3][key1] = {'edge':ele_list[15][2].upper()+ele_list[15][0].upper(),'ori':ele_list[15][3]}

		elif len(ele_list)==25 and ('BP' in ele_list[9]) and (('TP' in ele_list) or ('BF' in ele_list)): #If it is a quartet
			key1 = norm(ele_list[0])+norm(ele_list[1])+ele_list[2]+ele_list[3]
			key2 = norm(ele_list[4])+norm(ele_list[5])+ele_list[6]+ele_list[7]
			key3 = norm(ele_list[11])+norm(ele_list[12])+ele_list[13]+ele_list[14]
			key4 = norm(ele_list[18])+norm(ele_list[19])+ele_list[20]+ele_list[21]
			if key1 not in store[pdb]:
				store[pdb][key1] = {}
			if key2 not in store[pdb]:
				store[pdb][key2] = {}
			if key3 not in store[pdb]:
				store[pdb][key3] = {}
			if key4 not in store[pdb]:
				store[pdb][key4] = {}
			store[pdb][key1][key2] = {'edge':ele_list[8][0].upper()+ele_list[8][2].upper(),'ori':ele_list[8][3]}
			store[pdb][key2][key1] = {'edge':ele_list[8][2].upper()+ele_list[8][0].upper(),'ori':ele_list[8][3]}
			store[pdb][key1][key3] = {'edge':ele_list[15][0].upper()+ele_list[15][2].upper(),'ori':ele_list[15][3]}
			store[pdb][key3][key1] = {'edge':ele_list[15][2].upper()+ele_list[15][0].upper(),'ori':ele_list[15][3]}
			store[pdb][key1][key4] = {'edge':ele_list[22][0].upper()+ele_list[22][2].upper(),'ori':ele_list[22][3]}
			store[pdb][key4][key1] = {'edge':ele_list[22][2].upper()+ele_list[22][0].upper(),'ori':ele_list[22][3]}

		elif len(ele_list)==32 and ('BP' in ele_list) and (('TP' in ele_list) or ('BF' in ele_list)): #If it is a quintate
			key1 = norm(ele_list[0])+norm(ele_list[1])+ele_list[2]+ele_list[3]
			key2 = norm(ele_list[4])+norm(ele_list[5])+ele_list[6]+ele_list[7]
			key3 = norm(ele_list[11])+norm(ele_list[12])+ele_list[13]+ele_list[14]
			key4 = norm(ele_list[18])+norm(ele_list[19])+ele_list[20]+ele_list[21]
			key5 = norm(ele_list[25])+norm(ele_list[26])+ele_list[27]+ele_list[28]
			if key1 not in store[pdb]:
				store[pdb][key1] = {}
			if key2 not in store[pdb]:
				store[pdb][key2] = {}
			if key3 not in store[pdb]:
				store[pdb][key3] = {}
			if key4 not in store[pdb]:
				store[pdb][key4] = {}
			if key5 not in store[pdb]:
				store[pdb][key5] = {}
			store[pdb][key1][key2] = {'edge':ele_list[8][0].upper()+ele_list[8][2].upper(),'ori':ele_list[8][3]}
			store[pdb][key2][key1] = {'edge':ele_list[8][2].upper()+ele_list[8][0].upper(),'ori':ele_list[8][3]}
			store[pdb][key1][key3] = {'edge':ele_list[15][0].upper()+ele_list[15][2].upper(),'ori':ele_list[15][3]}
			store[pdb][key3][key1] = {'edge':ele_list[15][2].upper()+ele_list[15][0].upper(),'ori':ele_list[15][3]}
			store[pdb][key1][key4] = {'edge':ele_list[22][0].upper()+ele_list[22][2].upper(),'ori':ele_list[22][3]}
			store[pdb][key4][key1] = {'edge':ele_list[22][2].upper()+ele_list[22][0].upper(),'ori':ele_list[22][3]}
			store[pdb][key1][key5] = {'edge':ele_list[29][0].upper()+ele_list[29][2].upper(),'ori':ele_list[29][3]}
			store[pdb][key5][key1] = {'edge':ele_list[29][2].upper()+ele_list[29][0].upper(),'ori':ele_list[29][3]}


# def create_dict(pdb):
# 	fo = open(FOLDER+pdb+'.out','r+')
# 	a = fo.readlines()
# 	a = [x for x in a if x!='\n']
# 	if(pdb not in store):
# 		store[pdb] = {}
# 	for line in a:
# 		if len(line)==46 and 'BP' in line:
# 			bp_list = line.split()
# 			bp_list = map(str.strip,bp_list)
# 			key1 = norm(bp_list[0])+norm(bp_list[1])+bp_list[2]+bp_list[3]
# 			key2 = norm(bp_list[4])+norm(bp_list[5])+bp_list[6]+bp_list[7]
# 			if key1 not in store[pdb]:
# 				store[pdb][key1] = {}
# 			if key2 not in store[pdb]:
# 				store[pdb][key2] = {}
# 			store[pdb][key1][key2] = {'edge':bp_list[8][0].upper()+bp_list[8][2].upper(),'ori':bp_list[8][3]}
# 			store[pdb][key2][key1] = {'edge':bp_list[8][2].upper()+bp_list[8][0].upper(),'ori':bp_list[8][3]}

# 		elif len(line)==75 and ('BP' in line) and (('TP' in line) or ('BF' in line)):
# 			tp_list = line.split()
# 			tp_list = map(str.strip,tp_list)
# 			key1 = norm(tp_list[0])+norm(tp_list[1])+tp_list[2]+tp_list[3]
# 			key2 = norm(tp_list[4])+norm(tp_list[5])+tp_list[6]+tp_list[7]
# 			key3 = norm(tp_list[11])+norm(tp_list[12])+tp_list[13]+tp_list[14]
# 			if key1 not in store[pdb]:
# 				store[pdb][key1] = {}
# 			if key2 not in store[pdb]:
# 				store[pdb][key2] = {}
# 			if key3 not in store[pdb]:
# 				store[pdb][key3] = {}
# 			store[pdb][key1][key2] = {'edge':tp_list[8][0].upper()+tp_list[8][2].upper(),'ori':tp_list[8][3]}
# 			store[pdb][key2][key1] = {'edge':tp_list[8][2].upper()+tp_list[8][0].upper(),'ori':tp_list[8][3]}
# 			store[pdb][key1][key3] = {'edge':tp_list[15][0].upper()+tp_list[15][2].upper(),'ori':tp_list[15][3]}
# 			store[pdb][key3][key1] = {'edge':tp_list[15][2].upper()+tp_list[15][0].upper(),'ori':tp_list[15][3]}

# 		elif len(line)==104 and ('BP' in line) and (('TP' in line) or ('BF' in line)):
# 			quad_list = line.split()
# 			quad_list = map(str.strip,quad_list)
# 			key1 = norm(quad_list[0])+norm(quad_list[1])+quad_list[2]+quad_list[3]
# 			key2 = norm(quad_list[4])+norm(quad_list[5])+quad_list[6]+quad_list[7]
# 			key3 = norm(quad_list[11])+norm(quad_list[12])+quad_list[13]+quad_list[14]
# 			key4 = norm(quad_list[18])+norm(quad_list[19])+quad_list[20]+quad_list[21]
# 			if key1 not in store[pdb]:
# 				store[pdb][key1] = {}
# 			if key2 not in store[pdb]:
# 				store[pdb][key2] = {}
# 			if key3 not in store[pdb]:
# 				store[pdb][key3] = {}
# 			if key4 not in store[pdb]:
# 				store[pdb][key4] = {}
# 			store[pdb][key1][key2] = {'edge':quad_list[8][0].upper()+quad_list[8][2].upper(),'ori':quad_list[8][3]}
# 			store[pdb][key2][key1] = {'edge':quad_list[8][2].upper()+quad_list[8][0].upper(),'ori':quad_list[8][3]}
# 			store[pdb][key1][key3] = {'edge':quad_list[15][0].upper()+quad_list[15][2].upper(),'ori':quad_list[15][3]}
# 			store[pdb][key3][key1] = {'edge':quad_list[15][2].upper()+quad_list[15][0].upper(),'ori':quad_list[15][3]}
# 			store[pdb][key1][key4] = {'edge':quad_list[22][0].upper()+quad_list[22][2].upper(),'ori':quad_list[22][3]}
# 			store[pdb][key4][key1] = {'edge':quad_list[22][2].upper()+quad_list[22][0].upper(),'ori':quad_list[22][3]}

# 		elif len(line)==133 and ('BP' in line) and (('TP' in line) or ('BF' in line)):
# 			pent_list = line.split()
# 			pent_list = map(str.strip,pent_list)
# 			key1 = norm(pent_list[0])+norm(pent_list[1])+pent_list[2]+pent_list[3]
# 			key2 = norm(pent_list[4])+norm(pent_list[5])+pent_list[6]+pent_list[7]
# 			key3 = norm(pent_list[11])+norm(pent_list[12])+pent_list[13]+pent_list[14]
# 			key4 = norm(pent_list[18])+norm(pent_list[19])+pent_list[20]+pent_list[21]
# 			key5 = norm(pent_list[25])+norm(pent_list[26])+pent_list[27]+pent_list[28]
# 			if key1 not in store[pdb]:
# 				store[pdb][key1] = {}
# 			if key2 not in store[pdb]:
# 				store[pdb][key2] = {}
# 			if key3 not in store[pdb]:
# 				store[pdb][key3] = {}
# 			if key4 not in store[pdb]:
# 				store[pdb][key4] = {}
# 			if key5 not in store[pdb]:
# 				store[pdb][key5] = {}
# 			store[pdb][key1][key2] = {'edge':pent_list[8][0].upper()+pent_list[8][2].upper(),'ori':pent_list[8][3]}
# 			store[pdb][key2][key1] = {'edge':pent_list[8][2].upper()+pent_list[8][0].upper(),'ori':pent_list[8][3]}
# 			store[pdb][key1][key3] = {'edge':pent_list[15][0].upper()+pent_list[15][2].upper(),'ori':pent_list[15][3]}
# 			store[pdb][key3][key1] = {'edge':pent_list[15][2].upper()+pent_list[15][0].upper(),'ori':pent_list[15][3]}
# 			store[pdb][key1][key4] = {'edge':pent_list[22][0].upper()+pent_list[22][2].upper(),'ori':pent_list[22][3]}
# 			store[pdb][key4][key1] = {'edge':pent_list[22][2].upper()+pent_list[22][0].upper(),'ori':pent_list[22][3]}
# 			store[pdb][key1][key5] = {'edge':pent_list[29][0].upper()+pent_list[29][2].upper(),'ori':pent_list[29][3]}
# 			store[pdb][key5][key1] = {'edge':pent_list[29][2].upper()+pent_list[29][0].upper(),'ori':pent_list[29][3]}

# #	Recursive program to find cyclic triplets
# def cyclic_trip_finder(pdb,quad,key,parent): 
# 	quad.append(key)
# 	if len(quad)==3:
# 		temp = copy.deepcopy(quad)
# 		temp2 = copy.deepcopy(quad)
# 		temp2.sort()
# 		stri = ''.join(temp2)
# 		if stri in rep_checker_cy_trip[pdb]:
# 			quad.pop()
# 			return
# 		fl=0
# 		for key1 in temp:
# 			if len(store[pdb][key1])==2:
# 				for key2 in store[pdb][key1]:
# 					if key2 not in temp:
# 						fl=1
# 						break
# 				if fl==1:
# 					break
# 			else:
# 				fl=1
# 				break
# 		rep_checker_cy_trip[pdb][stri]=1
# 		if fl==1:
# 			quad.pop()
# 			return
# 		else:
# 			cyclic_trip[pdb].append(temp)
# 	else:
# 		for key1 in store[pdb][key]:
# 			if(key1!=parent):
# 				cyclic_trip_finder(pdb,quad,key1,key)
# 	quad.pop()
# 	return

#	Recursive program to find linear and square quartets
def linear_sq_quartet_finder(pdb,quad,key,parent): 
	if len(quad) > 0 and key == quad[0]:
		return
	quad.append(key)
	if len(quad)==4:
		temp = copy.deepcopy(quad)
		temp2 = copy.deepcopy(quad)
		temp2.sort()
		stri = ''.join(temp2)
		if stri in rep_checker_li_sq[pdb]:
			quad.pop()
			return
		fl = 0
		for key1 in store[pdb][key]:
			if key1 == quad[0]:
				fl = 1
		rep_checker_li_sq[pdb][stri] = 1
		if fl:
			sq_quartets[pdb].append(temp)
		else:
			linear_quartets[pdb].append(temp)
	else:
		for key1 in store[pdb][key]:
			if(key1!=parent):
				linear_sq_quartet_finder(pdb,quad,key1,key)
	quad.pop()
	return

#	Recursive program to find star and triangular quartets
def star_tri_quartet_finder(pdb):
	for center in store[pdb]:
		if len(store[pdb][center])>=3:
			node_list = []
			for node in store[pdb][center]:
				node_list.append(node) 
			for s in it.combinations(node_list,3):
				flag=0
				tri_quad = []
				checker = {}
				for node in s:
					for key in store[pdb][node]:
						if key in store[pdb][center]:
							check = ''.join(sorted([node,key]))
							if check not in checker:
								tri_quad.append([node,key])
								flag+=1
							checker[check]=1

				quad = [center,s[0],s[1],s[2]]
				stri = ''.join(sorted(quad))
				if stri not in rep_checker_st_tri[pdb]:
					if flag==0:
						star_quartets[pdb].append(quad)
					elif flag==1:
						for node in tri_quad[0]:
							quad.remove(node)
						tri_quartets[pdb].append(quad+tri_quad[0])
					elif flag==2:
						tri_quartets2[pdb].append(quad+tri_quad)
					elif flag==2:
						tri_quartets3[pdb].append(quad+tri_quad)		
				rep_checker_st_tri[pdb][stri] = 1

# #	Recursive program to find connected components in the graph
# def dfs(pdb,key):
# 	if(visited[pdb][key]==1):
# 		return
# 	cur_cc.append(key)
# 	visited[pdb][key]=1
# 	for node in store[pdb][key]:
# 		dfs(pdb,node)
# 	return

#	Assign nomenclature to the linear quartet
def linear_nomenclature(pdb,q): 
	p1 = q[0][8]+q[1][8]+store[pdb][q[0]][q[1]]['edge']+store[pdb][q[0]][q[1]]['ori']+q[0][4:8]+q[1][4:8]+q[0][9:]+q[1][9:]+q[0][0:4]+q[1][0:4]
	p2 = q[3][8]+q[2][8]+store[pdb][q[3]][q[2]]['edge']+store[pdb][q[3]][q[2]]['ori']+q[3][4:8]+q[2][4:8]+q[3][9:]+q[2][9:]+q[3][0:4]+q[2][0:4]
	if p1>p2:
		q = list(reversed(q))
	triplet = q[1][4:8].lstrip("0")+'\t'+q[1][8]+'\t'+q[1][9:]+'\t'+q[0][4:8].lstrip("0")+'\t'+q[0][8]+'\t'+q[0][9:]+'\t'+store[pdb][q[1]][q[0]]['edge'][0]+':'+store[pdb][q[1]][q[0]]['edge'][1]+store[pdb][q[1]][q[0]]['ori']+'\t'+q[2][4:8].lstrip("0")+'\t'+q[2][8]+'\t'+q[2][9:]+'\t'+store[pdb][q[1]][q[2]]['edge'][0]+':'+store[pdb][q[1]][q[2]]['edge'][1]+store[pdb][q[1]][q[2]]['ori']
	bp = q[2][4:8].lstrip("0")+'\t'+q[2][8]+'\t'+q[2][9:]+'\t'+q[3][4:8].lstrip("0")+'\t'+q[3][8]+'\t'+q[3][9:]+'\t'+store[pdb][q[2]][q[3]]['edge'][0]+':'+store[pdb][q[2]][q[3]]['edge'][1]+store[pdb][q[2]][q[3]]['ori']
	quartet = triplet +'\t\t\t' + bp
	var = q[0][8]+q[1][8]+q[2][8]+q[3][8]
	edge = store[pdb][q[0]][q[1]]['edge']+store[pdb][q[0]][q[1]]['ori']+'-'+store[pdb][q[1]][q[2]]['edge']+store[pdb][q[1]][q[2]]['ori']+'-'+store[pdb][q[2]][q[3]]['edge']+store[pdb][q[2]][q[3]]['ori']
	return [q,quartet,var,edge]

#	Assign nomenclature to the square quartet
def sq_nomenclature(pdb,q): 
	# print q
	p1 = q[0][8]+'.'+q[1][8]+'.'+store[pdb][q[0]][q[1]]['edge']+store[pdb][q[0]][q[1]]['ori']+'.'+q[0][4:8]+'.'+q[1][4:8]+'.'+q[0][9:]+'.'+q[1][9:]+'.'+q[0][0:4]+'.'+q[1][0:4]
	p2 = q[1][8]+'.'+q[2][8]+'.'+store[pdb][q[1]][q[2]]['edge']+store[pdb][q[1]][q[2]]['ori']+'.'+q[1][4:8]+'.'+q[2][4:8]+'.'+q[1][9:]+'.'+q[2][9:]+'.'+q[1][0:4]+'.'+q[2][0:4]
	p3 = q[2][8]+'.'+q[3][8]+'.'+store[pdb][q[2]][q[3]]['edge']+store[pdb][q[2]][q[3]]['ori']+'.'+q[2][4:8]+'.'+q[3][4:8]+'.'+q[2][9:]+'.'+q[3][9:]+'.'+q[2][0:4]+'.'+q[3][0:4]
	p4 = q[3][8]+'.'+q[0][8]+'.'+store[pdb][q[3]][q[0]]['edge']+store[pdb][q[3]][q[0]]['ori']+'.'+q[3][4:8]+'.'+q[0][4:8]+'.'+q[3][9:]+'.'+q[0][9:]+'.'+q[3][0:4]+'.'+q[0][0:4]
	p5 = q[0][8]+'.'+q[3][8]+'.'+store[pdb][q[0]][q[3]]['edge']+store[pdb][q[0]][q[3]]['ori']+'.'+q[0][4:8]+'.'+q[3][4:8]+'.'+q[0][9:]+'.'+q[3][9:]+'.'+q[0][0:4]+'.'+q[3][0:4]
	p6 = q[3][8]+'.'+q[2][8]+'.'+store[pdb][q[3]][q[2]]['edge']+store[pdb][q[3]][q[2]]['ori']+'.'+q[3][4:8]+'.'+q[2][4:8]+'.'+q[3][9:]+'.'+q[2][9:]+'.'+q[3][0:4]+'.'+q[2][0:4]
	p7 = q[2][8]+'.'+q[1][8]+'.'+store[pdb][q[2]][q[1]]['edge']+store[pdb][q[2]][q[1]]['ori']+'.'+q[2][4:8]+'.'+q[1][4:8]+'.'+q[2][9:]+'.'+q[1][9:]+'.'+q[2][0:4]+'.'+q[1][0:4]
	p8 = q[1][8]+'.'+q[0][8]+'.'+store[pdb][q[1]][q[0]]['edge']+store[pdb][q[1]][q[0]]['ori']+'.'+q[1][4:8]+'.'+q[0][4:8]+'.'+q[1][9:]+'.'+q[0][9:]+'.'+q[1][0:4]+'.'+q[0][0:4]
	# p2 = q[1][8]+q[2][8]+store[pdb][q[1]][q[2]]['edge']+store[pdb][q[1]][q[2]]['ori']+q[1][4:8]+q[2][4:8]+q[1][9:]+q[2][9:]+q[1][0:4]+q[2][0:4]
	# p3 = q[2][8]+q[3][8]+store[pdb][q[2]][q[3]]['edge']+store[pdb][q[2]][q[3]]['ori']+q[2][4:8]+q[3][4:8]+q[2][9:]+q[3][9:]+q[2][0:4]+q[3][0:4]
	# p4 = q[3][8]+q[0][8]+store[pdb][q[3]][q[0]]['edge']+store[pdb][q[3]][q[0]]['ori']+q[3][4:8]+q[0][4:8]+q[3][9:]+q[0][9:]+q[3][0:4]+q[0][0:4]
	# p5 = q[0][8]+q[3][8]+store[pdb][q[0]][q[3]]['edge']+store[pdb][q[0]][q[3]]['ori']+q[0][4:8]+q[3][4:8]+q[0][9:]+q[3][9:]+q[0][0:4]+q[3][0:4]
	# p6 = q[3][8]+q[2][8]+store[pdb][q[3]][q[2]]['edge']+store[pdb][q[3]][q[2]]['ori']+q[3][4:8]+q[2][4:8]+q[3][9:]+q[2][9:]+q[3][0:4]+q[2][0:4]
	# p7 = q[2][8]+q[1][8]+store[pdb][q[2]][q[1]]['edge']+store[pdb][q[2]][q[1]]['ori']+q[2][4:8]+q[1][4:8]+q[2][9:]+q[1][9:]+q[2][0:4]+q[1][0:4]
	# p8 = q[1][8]+q[0][8]+store[pdb][q[1]][q[0]]['edge']+store[pdb][q[1]][q[0]]['ori']+q[1][4:8]+q[0][4:8]+q[1][9:]+q[0][9:]+q[1][0:4]+q[0][0:4]
	seq_list = [p1,p2,p3,p4,p5,p6,p7,p8]
	seq = min(seq_list)
	seq = seq.split('.')
	# print seq
	res1 = seq[7]+seq[3]+seq[0]+seq[5]
	res2 = seq[8]+seq[4]+seq[1]+seq[6]
	# res1 = seq[15:19]+seq[5:9]+seq[0]+seq[13]
	# res2 = seq[19:23]+seq[9:13]+seq[1]+seq[14]
	index_res1 = q.index(res1)
	index_res2 = q.index(res2)
	
	if(index_res1==3 and index_res2==0):
		q = q[index_res1:] + q[:index_res1]
	elif(index_res1==0 and index_res2==3):
		q = list(reversed(q))
		q = q[3:]+q[:3]
	elif(index_res1 < index_res2):
		q = q[index_res1:] + q[:index_res1]
	elif(index_res1 > index_res2):
		q = list(reversed(q))
		index_res1 = q.index(res1)
		q = q[index_res1:] + q[:index_res1]

	triplet1 = q[1][4:8].lstrip("0")+'\t'+q[1][8]+'\t'+q[1][9:]+'\t'+q[0][4:8].lstrip("0")+'\t'+q[0][8]+'\t'+q[0][9:]+'\t'+store[pdb][q[1]][q[0]]['edge'][0]+':'+store[pdb][q[1]][q[0]]['edge'][1]+store[pdb][q[1]][q[0]]['ori']+'\t'+q[2][4:8].lstrip("0")+'\t'+q[2][8]+'\t'+q[2][9:]+'\t'+store[pdb][q[1]][q[2]]['edge'][0]+':'+store[pdb][q[1]][q[2]]['edge'][1]+store[pdb][q[1]][q[2]]['ori']
	triplet2 = q[3][4:8].lstrip("0")+'\t'+q[3][8]+'\t'+q[3][9:]+'\t'+q[0][4:8].lstrip("0")+'\t'+q[0][8]+'\t'+q[0][9:]+'\t'+store[pdb][q[3]][q[0]]['edge'][0]+':'+store[pdb][q[3]][q[0]]['edge'][1]+store[pdb][q[3]][q[0]]['ori']+'\t'+q[2][4:8].lstrip("0")+'\t'+q[2][8]+'\t'+q[2][9:]+'\t'+store[pdb][q[3]][q[2]]['edge'][0]+':'+store[pdb][q[3]][q[2]]['edge'][1]+store[pdb][q[3]][q[2]]['ori']
	var = q[0][8]+q[1][8]+q[2][8]+q[3][8]
	edge = store[pdb][q[0]][q[1]]['edge']+store[pdb][q[0]][q[1]]['ori']+'-'+store[pdb][q[1]][q[2]]['edge']+store[pdb][q[1]][q[2]]['ori']+'-'+store[pdb][q[2]][q[3]]['edge']+store[pdb][q[2]][q[3]]['ori']+'-'+store[pdb][q[3]][q[0]]['edge']+store[pdb][q[3]][q[0]]['ori']+'->'
	return [q,triplet1,triplet2,var,edge]

#	Assign nomenclature to the star quartet
def star_nomenclature(pdb,q):
	res = []
	for i in xrange(1,4):
		p = q[0][8]+'.'+q[i][8]+'.'+store[pdb][q[0]][q[i]]['edge']+store[pdb][q[0]][q[i]]['ori']+'.'+q[0][4:8]+'.'+q[i][4:8]+'.'+q[0][9:]+'.'+q[i][9:]+'.'+q[0][0:4]+'.'+q[i][0:4]
		# p = q[0][8]+q[i][8]+store[pdb][q[0]][q[i]]['edge']+store[pdb][q[0]][q[i]]['ori']+q[0][4:8]+q[i][4:8]+q[0][9:]+q[i][9:]+q[0][0:4]+q[i][0:4]
		res.append(p)
	res.sort()
	quartet = q[0][4:8].lstrip("0")+'\t'+q[0][8]+'\t'+q[0][9:]
	var = q[0][8]+'['
	edge = ''
	for i in xrange(3):
		res[i] = res[i].split('.')
		quartet = quartet+'\t'+res[i][4].lstrip("0")+'\t'+res[i][1]+'\t'+res[i][6]+'\t'+res[i][2][0]+':'+res[i][2][1:]
		# quartet = quartet+'\t'+res[i][9:13].lstrip("0")+'\t'+res[i][1]+'\t'+res[i][14]+'\t'+res[i][2]+':'+res[i][3:5]
		var = var + res[i][1]
		edge = edge + res[i][2] +'/'
	var = var + ']'
	edge = edge[:-1]
	return [quartet,var,edge]
	

#	Assign nomenclature to the triangular quartet
def tri_nomenclature(pdb,q):
	p1 = q[0][8]+q[2][8]+store[pdb][q[0]][q[2]]['edge']+store[pdb][q[0]][q[2]]['ori']+q[0][4:8]+q[2][4:8]+q[0][9:]+q[2][9:]+q[0][0:4]+q[2][0:4]
	p2 = q[0][8]+q[3][8]+store[pdb][q[0]][q[3]]['edge']+store[pdb][q[0]][q[3]]['ori']+q[0][4:8]+q[3][4:8]+q[0][9:]+q[3][9:]+q[0][0:4]+q[3][0:4]
	if(p1>p2):
		q[2],q[3] = q[3],q[2]
		p1,p2 = p2,p1

	var = q[0][8]+'[<'+q[2][8]+q[3][8]+'>'+q[1][8]+']'
	edge = store[pdb][q[0]][q[2]]['edge']+store[pdb][q[0]][q[2]]['ori']+'/'+store[pdb][q[0]][q[3]]['edge']+store[pdb][q[0]][q[3]]['ori']+'/'+store[pdb][q[0]][q[1]]['edge']+store[pdb][q[0]][q[1]]['ori']+','+store[pdb][q[2]][q[3]]['edge']+store[pdb][q[2]][q[3]]['ori']
	quad = q[0][4:8].lstrip("0")+'\t'+q[0][8]+'\t'+q[0][9:]

	for i in xrange(1,4):
		quad = quad + '\t' + q[i][4:8].lstrip("0")+'\t'+q[i][8]+'\t'+q[i][9:]+'\t'+store[pdb][q[0]][q[i]]['edge'][0]+':'+store[pdb][q[0]][q[i]]['edge'][1]+store[pdb][q[0]][q[i]]['ori']

	q[0],q[2] = q[2],q[0]
	trip = q[0][4:8].lstrip("0")+'\t'+q[0][8]+'\t'+q[0][9:]
	for i in xrange(2,4):
		trip = trip + '\t' + q[i][4:8].lstrip("0")+'\t'+q[i][8]+'\t'+q[i][9:]+'\t'+store[pdb][q[0]][q[i]]['edge'][0]+':'+store[pdb][q[0]][q[i]]['edge'][1]+store[pdb][q[0]][q[i]]['ori']

	q[0],q[2] = q[2],q[0]
	return [quad,trip,var,edge]

#	Loop to create graph
for pdb in pdb_list:
	pdb_name = pdb.split('.')[0]
	create_dict(pdb_name)

#	Loop to get cyclic triplets, linear quartets and square quartets 
print "Extracting linear and cyclic-4 quartets"
parent = ''
for pdb in store:
	linear_quartets[pdb] = []
	sq_quartets[pdb] = []
	# cyclic_trip[pdb] = []
	rep_checker_li_sq[pdb] = {}
	rep_checker_cy_trip[pdb] = {}
	for key in store[pdb]:
		# cyclic_trip_finder(pdb,[],key,parent)
		linear_sq_quartet_finder(pdb,[],key,parent)

#	Loop to get star quartets and triangular quartets 
print "Extracting star and cyclic-3 quartets"
for pdb in store:
	star_quartets[pdb] = []
	tri_quartets[pdb] = []
	tri_quartets2[pdb] = []
	tri_quartets3[pdb] = []
	rep_checker_st_tri[pdb] = {}
	star_tri_quartet_finder(pdb)

# #	Loop to get connected components in the graph
# for pdb in store:
# 	cc_list[pdb] = []
# 	visited[pdb] = {}
# 	for node in store[pdb]:
# 		visited[pdb][node] = 0
# 	for node in store[pdb]:
# 		if(visited[pdb][node] == 0):
# 			cur_cc = []
# 			dfs(pdb,node)
# 			cc_list[pdb].append(cur_cc)

# #	Print the Cyclic Triplets
# with open("output/test/"+ args[1].lower()+"/cyclic_trip","w") as fo:
# 	count=0
# 	for pdb in store:
# 		if cyclic_trip[pdb]!=[]:
# 			fo.write('-----------'+pdb+'-----------\n')
# 			for t in cyclic_trip[pdb]:
# 				trip=t[0][4:8].lstrip('0')+'\t'+t[0][8]+'\t'+t[0][9:]+'\t'+t[1][4:8].lstrip('0')+'\t'+t[1][8]+'\t'+t[1][9:]+'\t'+store[pdb][t[0]][t[1]]['edge'][0]+':'+store[pdb][t[0]][t[1]]['edge'][1]+store[pdb][t[0]][t[1]]['ori']+'\t'+t[2][4:8].lstrip('0')+'\t'+t[2][8]+'\t'+t[2][9:]+'\t'+store[pdb][t[0]][t[2]]['edge'][0]+':'+store[pdb][t[0]][t[2]]['edge'][0]+store[pdb][t[0]][t[2]]['ori']
# 				fo.write(trip+'\n')
# 				fo.write('\n')
# 				count+=1
# 	fo.write(str(count))

#	Print the Linear Quartets
print "Printing linear quartets"
with open("bpfind/output/"+folder+"/linear.txt","w") as fo:
# with open("output/test/"+ args[1].lower()+"/type_1","w") as fo:
	count=0
	for pdb in linear_quartets:
		if(linear_quartets[pdb]!=[]):
			# with open("bpfind/output/"+folder+"/linear.txt","w") as fo:
			fo.write('-----------'+pdb+'-----------\n')
			for q in linear_quartets[pdb]:
				nm = linear_nomenclature(pdb,q)
				fo.write(nm[1]+'\n')
				fo.write("Linear:\t"+nm[2]+'\t'+nm[3]+'\n')
				fo.write('\n')
				count+=1
	fo.write(str(count))

#	Print the Star Quartets
print "Printing star quartets"
with open("bpfind/output/"+folder+"/star.txt","w") as fo:
# with open("output/test/"+ args[1].lower()+"/type_2",'w') as fo:
	count=0
	for pdb in pdb_list:
		pdb = pdb.split('.')[0]
		if(star_quartets[pdb]!=[]):
			fo.write('-----------'+pdb+'-----------\n')
			for q in star_quartets[pdb]:	
				nm = star_nomenclature(pdb,q)
				fo.write(nm[0]+'\n')
				fo.write("Star:\t"+nm[1]+'\t'+nm[2]+'\n')
				fo.write("\n")
				count+=1
	fo.write(str(count))

#	Print the Cylcic-4 Quartets
print "Printing cyclic-4 quartets"
with open("bpfind/output/"+folder+"/cyclic-4.txt","w") as fo:
# with open("output/test/"+ args[1].lower()+"/type_3","w") as fo:
	count=0
	for pdb in sq_quartets:
		if(sq_quartets[pdb]!=[]):
		# with open("bpfind/output/"+folder+"/cyclic-4.txt","w") as fo:
			fo.write('-----------'+pdb+'-----------\n')
			for q in sq_quartets[pdb]:
				nm = sq_nomenclature(pdb,q)
				fo.write(nm[1]+'\n')
				fo.write(nm[2]+'\n')
				fo.write("Cyclic-4:\t"+nm[3]+"\t"+nm[4]+'\n')
				fo.write('\n')
				count+=1
	fo.write(str(count))

#	Print the Cyclic-3 Quartets
print "Printing cyclic-3 quartets"
with open("bpfind/output/"+folder+"/cyclic-3.txt","w") as fo:
# with open("output/test/"+ args[1].lower()+"/type_4",'w') as fo:
	count=0
	for pdb in pdb_list:
		pdb = pdb.split('.')[0]
		if(tri_quartets[pdb]!=[]):
			fo.write('-----------'+pdb+'-----------\n')
			for q in tri_quartets[pdb]:
				nm = tri_nomenclature(pdb,q)
				fo.write("quad:\t"+nm[0]+'\n')
				fo.write("triplet:\t"+nm[1]+'\n')
				fo.write("Cyclic-3:\t"+nm[2]+'\t'+nm[3]+'\n')
				fo.write('\n')
				count+=1
	fo.write(str(count))

# #	Print the connected components in the graph
# with open("output/test/"+ args[1].lower()+"/cc",'w') as fo:
# 	for pdb in store:
# 		if cc_list[pdb]!=[]:
# 			# fo.write('-----------'+pdb+'-----------\n')
# 			for cc in cc_list[pdb]:
# 				final=[]
# 				for comp in cc:
# 					temp = [comp,len(store[pdb][comp])]
# 					final.append(temp)
# 				if len(cc)==5:
# 					key = ''
# 					for comp in cc:
# 						key += str(len(store[pdb][comp]))
# 					key = ''.join(sorted(key))
# 					if key in quin_topology:
# 						topo = quin_topology[key]
# 					else:
# 						topo = "NOT AVAILABLE"
# 					fo.write(pdb+'\t'+str(final)+'\t'+topo)
# 					fo.write('\n')
# 				if len(cc)>3 and len(cc)!=5:
# 					fo.write(pdb+'\t'+str(final))
# 					# fo.write(str(cc) + '\t' + pdb)
# 					fo.write('\n')



# #	Print Tab Seperated Outputs
# with open("output/test/tab_sep_output/" + args[1].lower() + "/type_1","w") as fo:
# 	count=0
# 	for pdb in linear_quartets:
# 		if(linear_quartets[pdb]!=[]):
# 			for q in linear_quartets[pdb]:
# 				nm = linear_nomenclature(pdb,q)
# 				fo.write(nm[1]+'\t'+nm[2]+'\t'+nm[3]+'\t'+pdb+'\n')
# 				fo.write('\n')
# 				count+=1
# 	fo.write(str(count))

# with open('output/test/tab_sep_output/'+ args[1].lower()+'/type_2','w') as fo:
# 	count=0
# 	for pdb in pdb_list:
# 		pdb = pdb.split('.')[0]
# 		if(star_quartets[pdb]!=[]):
# 			for q in star_quartets[pdb]:	
# 				nm = star_nomenclature(pdb,q)
# 				fo.write(nm[0]+'\t'+nm[1]+'\t'+nm[2]+'\t'+pdb+'\n')
# 				fo.write("\n")
# 				count+=1
# 	fo.write(str(count))

# with open("output/test/tab_sep_output/"+ args[1].lower() +"/type_3","w") as fo:
# 	count=0
# 	for pdb in sq_quartets:
# 		if(sq_quartets[pdb]!=[]):
# 			for q in sq_quartets[pdb]:
# 				nm = sq_nomenclature(pdb,q)
# 				fo.write(nm[1]+'\t'+nm[2]+'\t'+nm[3]+'\t'+nm[4]+'\t'+pdb)
# 				fo.write('\n')
# 				count+=1
# 	fo.write(str(count))


# with open('output/test/tab_sep_output/'+ args[1].lower()+'/type_4','w') as fo:
# 	count=0
# 	for pdb in pdb_list:
# 		pdb = pdb.split('.')[0]
# 		if(tri_quartets[pdb]!=[]):
# 			for q in tri_quartets[pdb]:
# 				nm = tri_nomenclature(pdb,q)
# 				fo.write(nm[0]+'\t\t'+nm[1]+'\t'+nm[2]+'\t'+nm[3]+'\t'+pdb+'\n')
# 				fo.write('\n')
# 				count+=1
# 	fo.write(str(count))
