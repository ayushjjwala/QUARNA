import sys
store = {} # Graph of the linear quartet

def norm(num):
	if len(num)==1:
		return '000'+num
	elif len(num)==2:
		return '00'+num
	elif len(num)==3:
		return '0'+num
	else:
		return num

def create_graph(q1,q2):
	key1 = norm(q1[0])+q1[1]+q1[2]
	key2 = norm(q1[3])+q1[4]+q1[5]
	key3 = norm(q1[7])+q1[8]+q1[9]
	key4 = norm(q2[0])+q2[1]+q2[2]
	key5 = norm(q2[3])+q2[4]+q2[5]
	key6 = norm(q2[7])+q2[8]+q2[9]

	store[key1]={}
	store[key2]={}
	store[key3]={}
	store[key4]={}

	store[key1] = {key2:{'edge':q1[6][0]+q1[6][2],'ori':q1[6][3]}, key3:{'edge':q1[10][0]+q1[10][2],'ori':q1[10][3]}}
	store[key4] = {key5:{'edge':q2[6][0]+q2[6][2],'ori':q2[6][3]}, key6:{'edge':q2[10][0]+q2[10][2],'ori':q2[10][3]}}
	store[key2][key1] = {'edge':store[key1][key2]['edge'][::-1],'ori':store[key1][key2]['ori']}
	store[key2][key4] = {'edge':store[key4][key2]['edge'][::-1],'ori':store[key4][key2]['ori']}
	store[key3][key1] = {'edge':store[key1][key3]['edge'][::-1],'ori':store[key1][key3]['ori']}
	store[key3][key4] = {'edge':store[key1][key3]['edge'][::-1],'ori':store[key4][key3]['ori']}

	temp = [key1,key2,key4,key3]
	return temp

def nomenclature(quad):
	quad_list1 = quad[0].strip().split('\t')
	quad_list1 = filter(None,quad_list1)
	quad_list2 = quad[1].strip().split('\t')
	quad_list2 = filter(None,quad_list2)

	q = create_graph(quad_list1,quad_list2)

	p1 = q[0][4]+q[1][4]+store[q[0]][q[1]]['edge']+store[q[0]][q[1]]['ori']+q[0][0:4]+q[1][0:4]+q[0][5:]+q[1][5:]
	p2 = q[1][4]+q[2][4]+store[q[1]][q[2]]['edge']+store[q[1]][q[2]]['ori']+q[1][0:4]+q[2][0:4]+q[1][5:]+q[2][5:]
	p3 = q[2][4]+q[3][4]+store[q[2]][q[3]]['edge']+store[q[2]][q[3]]['ori']+q[2][0:4]+q[3][0:4]+q[2][5:]+q[3][5:]
	p4 = q[3][4]+q[0][4]+store[q[3]][q[0]]['edge']+store[q[3]][q[0]]['ori']+q[3][0:4]+q[0][0:4]+q[3][5:]+q[0][5:]
	p5 = q[0][4]+q[3][4]+store[q[0]][q[3]]['edge']+store[q[0]][q[3]]['ori']+q[0][0:4]+q[3][0:4]+q[0][5:]+q[3][5:]
	p6 = q[3][4]+q[2][4]+store[q[3]][q[2]]['edge']+store[q[3]][q[2]]['ori']+q[3][0:4]+q[2][0:4]+q[3][5:]+q[2][5:]
	p7 = q[2][4]+q[1][4]+store[q[2]][q[1]]['edge']+store[q[2]][q[1]]['ori']+q[2][0:4]+q[1][0:4]+q[2][5:]+q[1][5:]
	p8 = q[1][4]+q[0][4]+store[q[1]][q[0]]['edge']+store[q[1]][q[0]]['ori']+q[1][0:4]+q[0][0:4]+q[1][5:]+q[0][5:]
	
	seq_list = [p1,p2,p3,p4,p5,p6,p7,p8]
	seq = min(seq_list)
	res1 = seq[5:9]+seq[0]+seq[13]
	res2 = seq[9:13]+seq[1]+seq[14]
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

	var = q[0][0:4].lstrip('0')+q[0][4]+'('+q[0][5]+')-'+q[1][0:4].lstrip('0')+q[1][4]+'('+q[1][5]+')-'+q[2][0:4].lstrip('0')+q[2][4]+'('+q[2][5]+')-'+q[3][0:4].lstrip('0')+q[3][4]+'('+q[3][5]+')'
	edge = store[q[0]][q[1]]['edge']+store[q[0]][q[1]]['ori']+'-'+store[q[1]][q[2]]['edge']+store[q[1]][q[2]]['ori']+'-'+store[q[2]][q[3]]['edge']+store[q[2]][q[3]]['ori']+'-'+store[q[3]][q[0]]['edge']+store[q[3]][q[0]]['ori']+'->'

	return var + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + edge
