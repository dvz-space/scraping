from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import os
import sys
import hashlib

defined_undefined_mark="@@@"

#creaza un loc de lucru daca nu exista
if os.path.isdir('workspace')==False:
    os.mkdir(os.getcwd()+"\\workspace")


def help():
    print("*********************")
    print("grab(url)                           -return html content in soup object")
    print("get_all(url_string,boolean )        - return a list with content of all <a> tags")
    print("get_urls(url)                       -return valid urls")
    print("urlize(url)                         - append http://www.to regular url")
    print("save,name,lista)                    -save links to a txt file")
    print("*********************")

def check_if_exists(file):
    file=os.getcwd()+'\\workspace\\'+file
    return os.path.isfile(file) #bool



#trateaza exceptiile 
def grab(url):
    try:
        page=urlopen(url)
        soup=BeautifulSoup(page, 'html.parser')
        return soup.title.get_text(),soup,url
    except Exception:
        print("Unexpected error:", sys.exc_info())
        return None ,None,url

#trateaza exceptiile
def get_all_atributes(url):
    lista=[]
    try:
        title,page,url_1=grab(url)
        if(url==url_1):
            pass
        else:
            print("wrong url")
        if(isinstance(title,type(None))==True or isinstance(page,type(None))==True):
            return None , None ,url
        else:
            for link in page.find_all('a'):
                repo=link.get('href')
                if isinstance(repo,str)==True:
                    lista.append(repo)
            return title,lista,url
    except Exception:
        print("Unexpected error:", sys.exc_info())
        return None , None,url

#trateaza unele exceptii
def filtru_atribute(lista,url):
    defined=[]
    undefined=[]
    for x in lista:
        if len(x)==0:
            pass
        elif x[0:4]=='http':
            defined.append(x)
        elif x[0]=='#' and len(x)>1:
            defined.append(url+x)
        elif x[0:5]=='//www':
            defined.append('http:'+x)
        else:
            undefined.append(x)
    return defined ,undefined,url
        
        
    


#nu trateaza toate expresiile
def save(defined,undefined,url,title):
    global defined_undefined_mark
    repo=defined_undefined_mark
    title=title.replace('\n',"")
    prepare_md5=url+title
    md5=prepare_md5.encode()
    md5=hashlib.md5(md5)
    md5=md5.hexdigest()
    md5=md5+'.txt'
 

    if(check_if_exists(md5)==False):
        print(check_if_exists(md5))
        print("prepare work on title:  "+md5)
        if isinstance(md5,type(None)) or md5=="" or md5==" ":
            md5="no name : "+time.ctime()
        print("md5 ok, creating file..")
        file=open(os.getcwd()+'\\workspace\\'+md5,'w')
        file.write(url+'\n')
        file.write(title+'\n')
        file.write(time.ctime()+'\n')
        file.write("*****\n")
        for x in defined:
            file.write(x+"\n")
        file.write(repo+"\n")
        for y in undefined:
            file.write(y+"\n")
        file.close()
        print("succes")
    else:
        print('file exists')


def save_url(url):
    title ,lista ,url=get_all_atributes(url)
    if (type(title)==type(None) or type(lista)==type(None) or len(lista)==0):
        print("sequest inposibil sau lista goala")
    else:
        defined ,undefined,url=filtru_atribute(lista,url)
        save(defined,undefined,url,title)
        
        
    
    


def grab_file(file):
    #presupunem ca fisierul e in working directory os.getcwd()
    file=open(os.getcwd()+'\\workspace\\'+file,'r')
    print("debug open file OK")
    for x in file:
        save_url(x)
        print("working on:"+x) 
        


    
    
    










