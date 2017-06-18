import sys
store = {}

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

	store[key1]={}
	store[key1] = {key2:{'edge':q[6][0]+q[6][2],'ori':q[6][3]},key3:{'edge':q[10][0]+q[10][2],'ori':q[10][3]},key4:{'edge':q[14][0]+q[14][2],'ori':q[14][3]}}

	temp = [key1,key2,key3,key4]
	return temp

def nomenclature(quad):
	quad_list = quad.strip().split('\t')
	quad_list = filter(None,quad_list)
	q = create_graph(quad_list)

	res = []
	for i in xrange(1,4):
		p = q[0][4]+q[i][4]+store[q[0]][q[i]]['edge']+store[q[0]][q[i]]['ori']+q[0][0:4]+q[i][0:4]+q[0][5:]+q[i][5:]
		res.append(p)
	res.sort()

	var = q[0][0:4].lstrip('0')+q[0][4]+'('+q[0][5:]+')['+res[0][9:13].lstrip('0')+res[0][1]+'('+res[0][-1]+')&nbsp;&nbsp;'+res[1][9:13].lstrip('0')+res[1][1]+'('+res[1][-1]+')&nbsp;&nbsp;'+res[2][9:13].lstrip('0')+res[2][1]+'('+res[2][-1]+')]' 
	edge = res[0][2:5]+'/'+res[1][2:5]+'/'+res[2][2:5]

	return var + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + edge
