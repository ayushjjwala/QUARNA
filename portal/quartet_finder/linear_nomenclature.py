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

def create_graph(q):
	key1 = norm(q[0])+q[1]+q[2]
	key2 = norm(q[3])+q[4]+q[5]
	key3 = norm(q[7])+q[8]+q[9]
	key4 = norm(q[11])+q[12]+q[13]
	key5 = norm(q[14])+q[15]+q[16]

	store[key1]={}
	store[key2]={}
	store[key3]={}
	store[key4]={}
	store[key5]={}
	store[key1] = {key2:{'edge':q[6][0]+q[6][2],'ori':q[6][3]},key3:{'edge':q[10][0]+q[10][2],'ori':q[10][3]}}
	store[key2] = {key1:{'edge':q[6][2]+q[6][0],'ori':q[6][3]}}
	store[key3] = {key1:{'edge':q[10][2]+q[10][0],'ori':q[10][3]}}
	store[key4][key5] = {'edge':q[17][0]+q[17][2],'ori':q[17][3]}
	store[key5][key4] = {'edge':q[17][2]+q[17][0],'ori':q[17][3]}

	temp = [key2,key1,key3]
	if key4==temp[0]:
		temp = [key5] + temp
	elif key4==temp[2]:
		temp.append(key5)
	if key5==temp[0]:
		temp = [key4] + temp
	elif key5==temp[2]:
		temp.append(key4)
	
	return temp

def nomenclature(quad): 
	quad_list = quad.strip().split('\t')
	quad_list = filter(None,quad_list)
	q = create_graph(quad_list)

	p1 = q[0][4]+q[1][4]+store[q[0]][q[1]]['edge']+store[q[0]][q[1]]['ori']+q[0][0:4]+q[1][0:4]+q[0][5:]+q[1][5:]
	p2 = q[3][4]+q[2][4]+store[q[3]][q[2]]['edge']+store[q[3]][q[2]]['ori']+q[3][0:4]+q[2][0:4]+q[3][5:]+q[2][5:]

	if p1>p2:
		q = list(reversed(q))

	var = q[0][0:4].lstrip('0')+q[0][4]+'('+q[0][5]+')-'+q[1][0:4].lstrip('0')+q[1][4]+'('+q[1][5]+')-'+q[2][0:4].lstrip('0')+q[2][4]+'('+q[2][5]+')-'+q[3][0:4].lstrip('0')+q[3][4]+'('+q[3][5]+')'
	edge = store[q[0]][q[1]]['edge']+store[q[0]][q[1]]['ori']+'-'+store[q[1]][q[2]]['edge']+store[q[1]][q[2]]['ori']+'-'+store[q[2]][q[3]]['edge']+store[q[2]][q[3]]['ori']

	return var + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + edge
