#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:59:59 2020

@author: jules
"""
import numpy as np
import networkx as nx
from collections import Counter
from natsort import natsorted
import epub
import os
import bs4

#%%

def upper_list(z):
    for i in range(len(z)):
        z[i] = z[i].upper()
    return z

def remove_backlash(z):
    for i in range(len(z)):
        z[i] = z[i].rstrip()
    return z

def remove_parent(li):
    for i in range(len(li)):
        l = li[i]
        if l.find(")")!=-1:
            i2 = l.find(")")
            i1 = i2
            while(l[i1]!="("):
                i1 = i1 - 1
            li[i] = l[:i1:]
    
    return li 

def remove_span(data):
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    for match in soup1.findAll('span'):
        match.unwrap()
    return str(soup1)

def remove_p(data):
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    for match in soup1.findAll('p'):
        match.unwrap()
    return str(soup1)

def remove_h2(data):
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    for match in soup1.findAll('h2'):
        match.unwrap()
    return str(soup1)

def remove_a(data):
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    for match in soup1.findAll('a'):
        match.unwrap()
    return str(soup1)

def remove_br(data):
    soup1 = bs4.BeautifulSoup(data, 'html.parser')
    for match in soup1.findAll('br'):
        match.unwrap()
    return str(soup1)

def check(s):
    out = False
    if (s.find('book_') != -1): 
        print ("Contains given substring ") 
        out = True
    else: 
        print ("Doesn't contains given substring") 
    
    return out

def find_all_id(input_str, search_str):
    l1 = []
    length = len(input_str)
    index = 0
    while index < length:
        i = input_str.find(search_str, index)
        if i == -1:
            return l1
        l1.append(i)
        index = i + 1
    return l1

def open_ebook(file,file_out=""):
    if file_out != "":
        f = open(file_out,encoding=encod2,mode='w')
    
    book = epub.open_epub(file)
    for item_id, linear in book.opf.spine.itemrefs:
        item = book.get_item(item_id)
        # Check if linear or not
        if linear:
            print ('Linear item "%s"' % item.href)
            if check : 
                data = book.read_item(item)
                data = data.decode(encod2, errors='ignore')
                #print(data)
                if file_out != "":
                    f.write(data)
        else:
            print ('Non-linear item "%s"' % item.href)
            
    if file_out != "":
        f.close()
    
#%%
        
global encod1
encod1  = 'ascii'
global encod2 
encod2 = 'latin1'

path = os.getcwd()+'/'
Tnum = '1'

file = 'Kaamelott_Tome_'+Tnum+'.epub'
fileOut = 'Tome_'+Tnum+'.txt'
book = epub.open_epub(path+file)

episode_tag = '<p class="amanuansis-renamed-style1">'

tagT0 = '<?xml version="1.0" encoding="UTF-8"?>' 

open_ebook(file,fileOut)

file = open(fileOut,'r')
data = file.read()
file.close()

#%%
res = find_all_id(data,tagT0)

N = len(res)

directory = 'subfiles_Tome_'+Tnum
if not os.path.exists(directory):
    os.makedirs(directory)
    
for n in range(N-1):
    ftemp = open(directory+"/subfile_"+str(n)+".txt","w")
    
    d1 = data[res[n]+len(tagT0)+1:res[n+1]]
    d1 = remove_span(d1)
    d1 = remove_p(d1)
    d1 = remove_a(d1)
    d1 = remove_h2(d1)
    d1 = remove_br(d1)
    ftemp.write(d1)
    
    ftemp.close()
    
#%%

li =  [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
li = natsorted(li)

#%%
tagT1 = ' — '

var_x = list()

M = len(li)

for j in range(7,M,1):

    file_1 = directory+"/"+li[j]
    
    f1 = open(file_1, mode='r')
    x1 = f1.read()
    f1.close()
    
    i1 = find_all_id(x1," — ")
    
    names = list()
    for i in range(len(i1)):
        i2 = i1[i]
        flag = False
        while(x1[i2]!="\n"):
            i2 = i2 - 1
            if abs(i2-i1[i]) > 18:
                flag = True
        if(not flag):
            names.append(x1[i2+1:i1[i]])
        
    names2 = remove_parent(names) # remove didascalies
    
    names2 = remove_backlash(names2) # remove backslash (end)
    
    names2 = upper_list(names2)
    
    counts = Counter(names2)
    tab = np.array(list(counts.items()))
    wj  = np.sum(tab[::,1].astype(float))/np.size(tab[::,0])
    tab = np.column_stack((tab,np.ones(len(tab[::,0]))*wj)) 
    
    var_x.append(tab)
   
#%%
K = len(var_x)  
all_names = list()
for k in range(K):
    y = var_x[k]
    for j in range(np.size(y[::,0])):
        all_names.append(str(y[j,0]))

ct = Counter(all_names)
nodes = np.array(list(ct.items()))


source = list()
target = list()

for k in range(K):
    y = var_x[k]
    for j in range(np.size(y[::,0])-1):
        source.append(str(y[0,0]))
        target.append(str(y[j+1,0]))

edges_ = []
edges_ = np.column_stack((np.asarray(source),np.asarray(target)))

for n in range(np.size(edges_[::,0])):
    a = np.copy(edges_[n,0])
    b = np.copy(edges_[n,1])
    
    ia = int(np.where(nodes[::,0]==a)[0])
    ib = int(np.where(nodes[::,0]==b)[0])
    
    if ib < ia : 
        edges_[n,0] = b
        edges_[n,1] = a

edges = list()
poids  = list()

for n in range(np.size(edges_[::,0])):
    a = np.copy(edges_[n,0])
    b = np.copy(edges_[n,1])
    ic = len(np.where(np.logical_and(edges_[::,0] == a, edges_[::,1] == b))[0])
    if (a,b,{'value':int(ic)}) not in edges: 
        edges.append((str(a),str(b),{'value':int(ic)}))



G = nx.Graph()

for i in range(np.size(nodes[::,0])):
    G.add_nodes_from([(nodes[i,0],{'value':float(nodes[i,1])})]) #(nodes[::,0],{'value':nodes[::,1].astype(float)}))

G.add_edges_from(edges)

nx.write_gexf(G,"GephiFileT"+Tnum+".gexf")
#%%
#K = len(var_x)    
#node_name   = list()
#node_weight = list()
#
#for k in range(K):
#    xx = var_x[k]
#    for l in range(np.size(xx[::,0])):
#        if xx[::,l] not in node_name : 
#            node_name.append()
