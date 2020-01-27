#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 21:59:59 2020

@author: jules
"""

import epub
import os


def check(s):
    out = False
    if (s.find('book_') != -1): 
        print ("Contains given substring ") 
        out = True
    else: 
        print ("Doesn't contains given substring") 
    
    return out

def open_ebook(file,file_out=""):
    if file_out != "":
        f = open(file_out,encoding='ascii',mode='w')
    
    book = epub.open_epub(file)
    for item_id, linear in book.opf.spine.itemrefs:
        item = book.get_item(item_id)
        # Check if linear or not
        if linear:
            print ('Linear item "%s"' % item.href)
            if check : 
                data = book.read_item(item)
                data = data.decode('ascii', errors='ignore')
                print(data)
                if file_out != "":
                    f.write(data)
        else:
            print ('Non-linear item "%s"' % item.href)
            
    if file_out != "":
        f.close()
    

path = os.getcwd()+'/'
file = 'Kaamelott_Tome_1.epub'
fileOut = 'Tome_1.txt'
book = epub.open_epub(path+file)


episode_tag = "<p class=\"amanuansis-renamed-style1\">"

open_ebook(file,fileOut)


#file = open("Tome2.txt", encoding="ascii", mode="w+")

#for item in book.opf.manifest.values():
#    if 
#    data = book.read_item(item)
#    data = data.decode('ascii', errors='ignore')
#    
#    print(data)
#    
#    file.write(data)
#    
#file.close()
#    

