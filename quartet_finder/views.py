from django.shortcuts import render, HttpResponseRedirect, redirect
import os
from urllib import request as urllib2
from . import linear_nomenclature
from . import star_nomenclature
from . import cyclic_nomenclature
from . import semicyclic_nomenclature
# import linear_test
# import star_test
# import cyclic_test
# import semicyclic_test

def index(request, *args, **kwargs):
	return render(request,'quartet_finder/index.html')

def help(request):
	return render(request,'quartet_finder/help.html')


def tnd(request):
	return render(request,'quartet_finder/tnd.html')

def contact(request):
	return render(request,'quartet_finder/contact.html')

# Check whether PDB is uploaded or just PDB is mentioned and then use other functions to process the PDB
def pdb_upload(request):
    if request.method=='POST':
        pdb_name = request.POST['pdb_name']
        pdb_files = request.FILES.get("uploaded_pdb", None)
        download_path = None
        if(pdb_files==None) and (pdb_name==''):
            alert_msg1 = "Write a PDB file name or Upload a PDB file"
            print(alert_msg1)
            return render(request,'quartet_finder/index.html',{'alert_msg1':alert_msg1})

        elif (pdb_files!=None):
            name = str(pdb_files).split('.')
            if len(name)==2 and name[1]=='pdb':
                handle_upload(pdb_files)    
                run_bpfind(str(pdb_files))
                pdb_name = str(pdb_files).split('.')[0]
                download_path = 'media/output/'+pdb_name + '.zip'
                file_name = pdb_name + '.zip'
            else:
                alert_msg2 = "Upload a '.pdb' file"
                print(alert_msg2)
                return render(request,'quartet_finder/index.html',{'alert_msg2':alert_msg2})
        elif (pdb_files==None) and (pdb_name!=''):
            val = download_pdb(pdb_name)
            if val==1: #download was not successfull
                print(f"PDB File: {pdb_name} download was not successful")
                return HttpResponseRedirect('/')
            run_bpfind(pdb_name+".pdb") 
            download_path = 'media/output/'+pdb_name+'.zip'
            # print("download_path:", download_path)
            file_name = pdb_name + '.zip'
        return render(request,'quartet_finder/index.html',{'download_path':download_path,'file_name':file_name,'pdb_name':pdb_name})

    else:
        return HttpResponseRedirect('/')

# Download the PDB mentioned by the user
def download_pdb(name):
    try:
        print(f"downloading PDB File from web: {name}")
        proxy = urllib2.ProxyHandler({'http':'proxy.iiit.ac.in:8080'})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        u = urllib2.urlopen('http://www.rcsb.org/pdb/download/downloadFile.do?fileFormat=pdb&compression=NO&structureId='+str(name))
        with open('media/input/' + name + '.pdb','wb+') as destination:
            destination.write(u.read())
        destination.close()
        return 0
    except:
        return 1

# Download the uploaded PDB
def handle_upload(f):
    print(f"Downloading the PDB File uploaded: {str(f)}")
    with open('media/input/'+str(f),'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    destination.close()

# Run BPFIND on the PDB
def run_bpfind(pdb):
    print(f"Running BPFIND on the PDB File: {pdb}")
    folder = pdb.split('.')[0]
    os.system("mkdir scripts/bpfind/output/"+folder)
    os.system("cp media/input/"+ pdb +" scripts/bpfind/output/"+folder+"/")
    os.chdir("scripts/bpfind/")
    print(f"running BPFIND on {folder}")
    os.system("./bpfind-linux "+"output/"+folder+"/"+pdb) #REMEMBER TO CHANGE to bpfind-linux2
    run_quadScripts(folder)

# Run the scripts for extracting the quartets
def run_quadScripts(pdb):
    os.chdir("..")
    os.system("pwd")
    print(f"Extracting quartets from {pdb}")
    os.system("python quad_scripts/main.py "+pdb)
    os.chdir("bpfind/output/")
    os.system("zip "+pdb+" "+pdb+"/*")
    os.chdir("../../..")
    os.system("mv scripts/bpfind/output/"+pdb+".zip media/output/")
    print(f"Output files is ready: {pdb}")

# Find the quartets containing the specifically mentioned residues in different topologies
def specific_residue(request):
    if request.method=="POST":
        res = request.POST['residues'].upper().split(',')
        if len(res)!=4:
            alert_msg3 = "Please enter 4 residues"
            print(alert_msg3)
            return render(request,'quartet_finder/index.html',{'alert_msg3':alert_msg3})            
        topology = request.POST['topology']
        database = request.POST['database']
        check_res = ['A','U','G','C']
        if res[0] not in check_res or res[1] not in check_res or res[2] not in check_res or res[3] not in check_res:
            alert_msg4 = "Residues must be A or C or G or U."
            print(alert_msg4)
            return render(request,'quartet_finder/index.html',{'alert_msg4':alert_msg4})
        else:
            print("The input given by the user is correct....")
            file_name = res
            file_name.sort()
            temp = ''.join(file_name)
            file_name = temp + '_' + topology + '_' + database + ".txt"
            script_path = "scripts/specific_residue/" + topology + ".py"
            args = res[0] + ' ' +res[1] + ' '+res[2] + ' ' +res[3] + ' ' + database
            file_path = "media/output/specific_residue/" + file_name
            os.system("python "+ script_path + " " + args + " > " + file_path)
            if os.stat(file_path).st_size == 0:
                print("file is empty.")
                file_empty = "There are no results to show."
                os.system("rm " + file_path)
                return render(request,'quartet_finder/index.html',{'file_empty':file_empty})
            return render(request,'quartet_finder/index.html',{'download_path_sr':file_path,'file_name':file_name})
    else:
        return HttpResponseRedirect('/')

#Find the linear quartets with specific base pairs 
def linear(request):
    if request.method == 'POST':
        b1 = request.POST['b1']
        b2 = request.POST['b2']
        geometry = request.POST['geometry'].upper().split(':')
        if len(geometry)!=2:
            alert_msg5 = "Please enter a valid geometry."
            print(alert_msg5)
            return render(request,'quartet_finder/linear.html',{'alert_msg5':alert_msg5})            
        orient = request.POST['orient']
        pos = request.POST['pos']
        dataset = request.POST['dataset']
        temp = [b1+geometry[0],b2+geometry[1]]
        temp.sort()
        file_name = pos + '_' + temp[0][0] + temp[1][0] + temp[0][1] + temp[1][1] +orient + '_' + dataset
        file_path = "media/output/linear/"+ file_name + ".txt"
        args = temp[0] + ' ' + temp[1] + ' ' + orient + ' ' + dataset
        script_path = "scripts/linear/" + pos + ".py"
        os.system("python " + script_path + " " + args + " > " + file_path)
        if os.stat(file_path).st_size == 0:
            print("file is empty.")
            file_empty = "There are no results to show."
            os.system("rm " + file_path)
            return render(request,'quartet_finder/linear.html',{'file_empty':file_empty})
        return render(request,'quartet_finder/linear.html',{'download_path':file_path,'file_name':file_name+".txt"})
    else:
        return render(request,'quartet_finder/linear.html')

#Find the star quartets with specific base pairs
def star(request):
    if request.method=='POST':
        cb = request.POST['b1']
        b1 = request.POST['b2']
        geometry = request.POST['geometry'].upper().split(':')
        if len(geometry)!=2:
            alert_msg6 = "Please enter a valid geometry."
            print(alert_msg6)
            return render(request,'quartet_finder/star.html',{'alert_msg6':alert_msg6})
        orient = request.POST['orient']
        dataset = request.POST['dataset']
        temp = [cb+geometry[0],b1+geometry[1]]
        file_name = temp[0][0] + temp[1][0] + temp[0][1] + temp[1][1] +orient + '_' + dataset
        file_path = "media/output/star/"+ file_name + ".txt"
        args = temp[0] + ' ' + temp[1] + ' ' + orient + ' ' + dataset
        script_path = "scripts/star/bp.py"
        os.system("python " + script_path + " " + args + " > " + file_path)
        if os.stat(file_path).st_size == 0:
            print("file is empty.")
            file_empty = "There are no results to show."
            os.system("rm " + file_path)
            return render(request,'quartet_finder/star.html',{'file_empty':file_empty})
        return render(request,'quartet_finder/star.html',{'download_path':file_path,'file_name':file_name+".txt"})
    else:
        return render(request,'quartet_finder/star.html')

def cyclic(request):
    if request.method=='POST':
        b1 = request.POST['b1']
        b2 = request.POST['b2']
        geometry = request.POST['geometry'].upper().split(':')
        if len(geometry)!=2:
            alert_msg7 = "Please enter a valid geometry."
            print(alert_msg7)
            return render(request,'quartet_finder/cyclic.html',{'alert_msg7':alert_msg7})
        orient = request.POST['orient']
        dataset = request.POST['dataset']
        temp = [b1+geometry[0],b2+geometry[1]]
        file_name = temp[0][0] + temp[1][0] + temp[0][1] + temp[1][1] +orient + '_' + dataset
        file_path = "media/output/cyclic/"+ file_name + ".txt"
        args = temp[0] + ' ' + temp[1] + ' ' + orient + ' ' + dataset
        script_path = "scripts/cyclic/bp.py"
        os.system("python " + script_path + " " + args + " > " + file_path)
        if os.stat(file_path).st_size == 0:
            print("file is empty.")
            file_empty = "There are no results to show."
            os.system("rm " + file_path)
            return render(request,'quartet_finder/cyclic.html',{'file_empty':file_empty})
        return render(request,'quartet_finder/cyclic.html',{'download_path':file_path,'file_name':file_name+".txt"})
    else:
        return render(request,'quartet_finder/cyclic.html')

def semi_cyclic(request):
    if request.method=='POST':
        cb = request.POST['b1']
        b1 = request.POST['b2']
        geometry = request.POST['geometry'].upper().split(':')
        if len(geometry)!=2:
            alert_msg8 = "Please enter a valid geometry."
            print(alert_msg8)
            return render(request,'quartet_finder/semi_cyclic.html',{'alert_msg8':alert_msg8})
        orient = request.POST['orient']
        dataset = request.POST['dataset']
        temp = [cb+geometry[0],b1+geometry[1]]
        file_name = temp[0][0] + temp[1][0] + temp[0][1] + temp[1][1] +orient + '_' + dataset
        file_path = "media/output/semi_cyclic/"+ file_name + ".txt"
        args = temp[0] + ' ' + temp[1] + ' ' + orient + ' ' + dataset
        script_path = "scripts/semi_cyclic/bp.py"
        os.system("python " + script_path + " " + args + " > " + file_path)
        if os.stat(file_path).st_size == 0:
            print("file is empty.")
            file_empty = "There are no results to show."
            os.system("rm " + file_path)
            return render(request,'quartet_finder/semi_cyclic.html',{'file_empty':file_empty})
        return render(request,'quartet_finder/semi_cyclic.html',{'download_path':file_path,'file_name':file_name+".txt"})
    else:
        return render(request,'quartet_finder/semi_cyclic.html')

def jsmol(request,pdb_name):
	file_path = "scripts/bpfind/output/" + pdb_name + "/linear.txt"
	linear_list = get_linear_quartet(file_path,pdb_name)
	file_path = "scripts/bpfind/output/" + pdb_name + "/star.txt"
	star_list = get_star_quartet(file_path,pdb_name)
	file_path = "scripts/bpfind/output/" + pdb_name + "/cyclic-4.txt"
	cyclic_list = get_cyclic_quartet(file_path,pdb_name)
	file_path = "scripts/bpfind/output/" + pdb_name + "/cyclic-3.txt"
	semicyclic_list = get_semicyclic_quartet(file_path,pdb_name)
	
	dataset = check_xray(pdb_name)
	print(f"Running JSMOL applet to display the PDB File: {pdb_name}")
	return render(request,'jsmol/pdb_view.html',{'pdb_name':pdb_name,"linear_list":linear_list[0],"star_list":star_list[0],"cyclic_list":cyclic_list[0],"semicyclic_list":semicyclic_list[0],"dataset":dataset})

def view_linear(request,file_path,file_name):
	fo = open(file_path,'ro+')
	a = fo.readlines()
	a = [x for x in a if x!='\n']
	if request.method == 'POST':
		pdb_name = request.POST.get('pdb_name',None)
	elif request.method == 'GET':
		pdb_name = request.GET.get('pdb_name')

	if not pdb_name:
		for line in a:
			if '-----------' in line:
				if not pdb_name:
					pdb_name = line.split('-----------')[1]
					break
	required_list = get_linear_quartet(file_path,pdb_name) #to extract the quartets from the output file
	dataset = check_xray(pdb_name)
	print(f"Viewing linear quartets in the file: {file_name}....")
	return render(request,'jsmol/linear_view.html',{'quartet_list':required_list[0],'pdb_list':required_list[1],'pdb_name':pdb_name,'file_name':file_name,"dataset":dataset})

def view_star(request,file_path,file_name):
    fo = open(file_path,'ro+')
    a = fo.readlines()
    a = [x for x in a if x!='\n']
    if request.method == 'POST':
        pdb_name = request.POST.get('pdb_name',None)
    elif request.method == 'GET':
        pdb_name = request.GET.get('pdb_name')

    if not pdb_name:
        for line in a:
            if '-----------' in line:
                if not pdb_name:
                    pdb_name = line.split('-----------')[1]
                    break
    required_list = get_star_quartet(file_path,pdb_name)
    dataset = check_xray(pdb_name)
    print(f"Viewing star quartets in the file: {file_name}.....")
    return render(request,'jsmol/star_view.html',{'quartet_list':required_list[0],'pdb_list':required_list[1],'pdb_name':pdb_name,'file_name':file_name,'dataset':dataset})

def view_cyclic(request,file_path,file_name):
    fo = open(file_path,'ro+')
    a = fo.readlines()
    a = [x for x in a if x!='\n']
    if request.method == 'POST':
        pdb_name = request.POST.get('pdb_name',None)
    elif request.method == 'GET':
        pdb_name = request.GET.get('pdb_name')

    if not pdb_name:
        for line in a:
            if '-----------' in line:
                if not pdb_name:
                    pdb_name = line.split('-----------')[1]
                    break
    required_list = get_cyclic_quartet(file_path,pdb_name)
    dataset = check_xray(pdb_name)
    print(f"Viewing cyclic quartets in the file: {file_name}.....")
    return render(request,'jsmol/cyclic_view.html',{'quartet_list':required_list[0],'pdb_list':required_list[1],'pdb_name':pdb_name,'file_name':file_name,'dataset':dataset})

def view_semicyclic(request,file_path,file_name):
    fo = open(file_path,'ro+')
    a = fo.readlines()
    a = [x for x in a if x!='\n']
    if request.method == 'POST':
        pdb_name = request.POST.get('pdb_name',None)
    elif request.method == 'GET':
        pdb_name = request.GET.get('pdb_name')

    if not pdb_name:
        for line in a:
            if '-----------' in line:
                if not pdb_name:
                    pdb_name = line.split('-----------')[1]
                    break
    required_list = get_semicyclic_quartet(file_path,pdb_name)
    dataset = check_xray(pdb_name)
    print(f"Viewing semi-cyclic quartets in the file: {file_name}.....")
    return render(request,'jsmol/semicyclic_view.html',{'quartet_list':required_list[0],'pdb_list':required_list[1],'pdb_name':pdb_name,'file_name':file_name,'dataset':dataset})

def get_linear_quartet(file_path,pdb_name):
	fo = open(file_path,'ro+')
	a = fo.readlines()
	a = [x for x in a if x!='\n']
	key = ''
	item = ''
	quartet_list = {}
	pdb_list = []	
	pdb_checker = ''
	for i in range(len(a)):
		if '-----------' in a[i]:
			pdb_list.append(a[i].split('-----------')[1])
			pdb_checker = a[i].split('-----------')[1]
		if (pdb_name==pdb_checker) and ('Linear:' not in a[i]) and ('-----------' not in a[i]) and (len(a[i])>20):
			quad_list = a[i].split('\t')
			quad_list = list(filter(None,quad_list))
			key = quad_list[0] + ':' + quad_list[2] + ',' + quad_list[3] + ':' + quad_list[5] + ',' + quad_list[7] + ':' + quad_list[9] + ',' + quad_list[11] + ':' + quad_list[13] + ',' + quad_list[14] + ':' + quad_list[16] + ','
			item = linear_nomenclature.nomenclature(a[i])
		elif pdb_name==pdb_checker and 'Linear:' in a[i]:
			quartet_list[key] = item
			item = ''
	return [quartet_list,pdb_list]

def get_star_quartet(file_path,pdb_name):
	fo = open(file_path,'ro+')
	a = fo.readlines()
	a = [x for x in a if x!='\n']
	item = ''
	key = ''
	quartet_list = {}
	pdb_list = []	
	pdb_checker = ''
	for i in range(len(a)):
		if '-----------' in a[i]:
			pdb_list.append(a[i].split('-----------')[1].split('.')[0])
			pdb_checker = a[i].split('-----------')[1].split('.')[0]
		if (pdb_name==pdb_checker) and ('Star:' not in a[i]) and ('-----------' not in a[i]) and (len(a[i]) > 20):
			quad_list = a[i].split('\t')
			key = quad_list[0]+':'+quad_list[2] + ',' + quad_list[3] + ':' + quad_list[5] + ',' + quad_list[7] + ':' + quad_list[9] + ',' + quad_list[11] + ':' + quad_list[13] + ','
			item = star_nomenclature.nomenclature(a[i])
		elif pdb_name==pdb_checker and 'Star:' in a[i]:
			quartet_list[key] = item
			item = ''
	return [quartet_list,pdb_list]

def get_cyclic_quartet(file_path,pdb_name):
	fo = open(file_path,'ro+')
	a = fo.readlines()
	a = [x for x in a if x!='\n']
	item = ''
	key = ''
	quartet_list = {}
	pdb_list = []	
	quartet = []
	pdb_checker = ''
	for i in range(len(a)):
		if '-----------' in a[i]:
			pdb_list.append(a[i].split('-----------')[1])
			pdb_checker = a[i].split('-----------')[1]
		if (pdb_checker==pdb_name) and ('Cyclic-4:' not in a[i]) and ('-----------' not in a[i]) and (len(a[i])>20):
			quad_list = a[i].split('\t')
			key += quad_list[0]+':'+quad_list[2]+','+quad_list[3]+':'+quad_list[5]+','+quad_list[7]+':'+quad_list[9]+','
			quartet.append(a[i])
		elif (pdb_name==pdb_checker) and ('Cyclic-4:' in a[i]):
			item = cyclic_nomenclature.nomenclature(quartet)
			quartet_list[key] = item
			item = ''
			quartet = []
			key = ''
	return [quartet_list,pdb_list]

def get_semicyclic_quartet(file_path,pdb_name):
	fo = open(file_path,'ro+')
	a = fo.readlines()
	a = [x for x in a if x!='\n']
	item = ''
	key = ''
	quartet_list = {}  
	pdb_list = []	
	pdb_checker = ''
	for i in range(len(a)):
		if '-----------' in a[i]:
			pdb_list.append(a[i].split('-----------')[1])
			pdb_checker = a[i].split('-----------')[1]
		if pdb_checker==pdb_name and 'quad:' in a[i]:
			quad_list = a[i][5:].strip().split('\t')
			key = quad_list[0]+':'+quad_list[2]+','+quad_list[3]+':'+quad_list[5]+','+quad_list[7]+':'+quad_list[9]+','+quad_list[11]+':'+quad_list[13]+','
			quad = a[i][6:].strip()
		elif pdb_checker==pdb_name and 'triplet:' in a[i]:
			trip_list = a[i][8:].strip().split('\t')
			key += trip_list[0]+':'+trip_list[2]+','+trip_list[3]+':'+trip_list[5]+','+trip_list[7]+':'+trip_list[9]+','
			link = a[i][8:].strip()
		elif pdb_checker==pdb_name and 'Cyclic-3:' in a[i]:
			item = semicyclic_nomenclature.nomenclature(quad,link)
			quartet_list[key] = item
			item = ''
			key = ''
	return [quartet_list,pdb_list]

def get_path(request,file_name,topo):
	section = None
	topo_checker = ['linear','star','cyclic','semicyclic']
	if file_name.split('_')[1] in topo_checker:
		section = 'specific_residue'
		topo = file_name.split('_')[1]		
	if topo == 'linear':
		file_path = 'media/output/linear/'+file_name
		if section == 'specific_residue':
			file_path = 'media/output/specific_residue/'+file_name
		return view_linear(request,file_path,file_name)
	elif topo == 'star':
		file_path = 'media/output/star/'+file_name
		if section == 'specific_residue':
			file_path = 'media/output/specific_residue/'+file_name
		return view_star(request,file_path,file_name)
	elif topo == 'cyclic':
		file_path = 'media/output/cyclic/'+file_name
		if section == 'specific_residue':
			file_path = 'media/output/specific_residue/'+file_name
		return view_cyclic(request,file_path,file_name)
	elif topo == 'semicyclic':
		file_path = 'media/output/semi_cyclic/'+file_name
		if section == 'specific_residue':
			file_path = 'media/output/specific_residue/'+file_name
		return view_semicyclic(request,file_path,file_name)

def check_xray(pdb_name):
	pdb_list = os.listdir('static/jsmol/total/')
	for pdb in pdb_list:
		pdb = pdb.split('.')[0]
		if pdb_name == pdb:
			dataset = '/static/jsmol/total/' + pdb_name + '.pdb'
			return dataset
			break
	return 'http://www.rcsb.org/pdb/files/XXXX.pdb'