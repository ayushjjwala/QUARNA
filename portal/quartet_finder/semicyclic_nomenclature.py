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

def create_graph(q,t):
	key1 = norm(q[0])+q[1]+q[2]
	key2 = norm(q[3])+q[4]+q[5]
	key3 = norm(q[7])+q[8]+q[9]
	key4 = norm(q[11])+q[12]+q[13]
	key5 = norm(t[0])+t[1]+t[2]
	key6 = norm(t[3])+t[4]+t[5]
	key7 = norm(t[7])+t[8]+t[9]

	store[key1]={}
	store[key5]={}
	store[key1] = {key2:{'edge':q[6][0]+q[6][2],'ori':q[6][3]},key3:{'edge':q[10][0]+q[10][2],'ori':q[10][3]},key4:{'edge':q[14][0]+q[14][2],'ori':q[14][3]}}
	
	if(key6!=key1):
		store[key6]={}
		store[key5][key6] = {'edge':t[6][0]+t[6][2],'ori':t[6][3]}
		store[key6][key5] = {'edge':t[6][2]+t[6][0],'ori':t[6][3]}
		link = [key5,key6]
	elif(key7!=key1):
		store[key7]={}
		store[key5][key7] = {'edge':t[10][0]+t[10][2],'ori':t[10][3]}
		store[key7][key5] = {'edge':t[10][2]+t[10][0],'ori':t[10][3]}
		link = [key5,key7]

	quad = [key1,key2,key3,key4]
	for l in link:
		quad.remove(l)
	quad = quad + link

	return quad



def nomenclature(quad,trip):
	quad_list = quad.strip().split('\t')
	quad_list = filter(None,quad_list)
	trip_list = trip.strip().split('\t')
	trip_list = filter(None,trip_list)
	# print "here"
	# print trip
	# print trip_list
	q = create_graph(quad_list,trip_list)
	p1 = q[0][4]+q[2][4]+store[q[0]][q[2]]['edge']+store[q[0]][q[2]]['ori']+q[0][0:4]+q[2][0:4]+q[0][5:]+q[2][5:]
	p2 = q[0][4]+q[3][4]+store[q[0]][q[3]]['edge']+store[q[0]][q[3]]['ori']+q[0][0:4]+q[3][0:4]+q[0][5:]+q[3][5:]
	if(p1>p2):
		q[2],q[3] = q[3],q[2]
		p1,p2 = p2,p1

	var = q[0][0:4].lstrip('0')+q[0][4]+'('+q[0][5]+')[<'+q[2][0:4].lstrip('0')+q[2][4]+'('+q[2][5]+')&nbsp;&nbsp;'+q[3][0:4].lstrip('0')+q[3][4]+'('+q[3][5]+')>'+q[1][0:4].lstrip('0')+q[1][4]+'('+q[1][5]+')]'
	edge = store[q[0]][q[2]]['edge']+store[q[0]][q[2]]['ori']+'/'+store[q[0]][q[3]]['edge']+store[q[0]][q[3]]['ori']+'/'+store[q[0]][q[1]]['edge']+store[q[0]][q[1]]['ori']+','+store[q[2]][q[3]]['edge']+store[q[2]][q[3]]['ori']
	return var + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + edge
