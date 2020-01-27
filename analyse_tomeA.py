#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:59:59 2020

@author: jules
"""
import numpy as np
from collections import Counter
from natsort import natsorted
import epub
import os
import bs4

#%%

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
        while(x1[i2]!="\n"):
            i2 = i2 - 1
        names.append(x1[i2+1:i1[i]])
        
    names2 = remove_parent(names) # remove didascalies
    
    names2 = remove_backlash(names2) # remove backslash (end)
    
    
    counts = Counter(names2)
    tab = np.array(list(counts.items()))
    wj  = np.sum(tab[::,1].astype(float))/np.size(tab[::,0])
    tab = np.column_stack((tab,np.ones(len(tab[::,0]))*wj)) 
    
    var_x.append(tab)
   
#%%

var_x    
#var_y = np.asarray(var_x)
