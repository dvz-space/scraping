from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import os
import sys

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
            print('url1==url2 OK')
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
    title=title.replace('\\\\',"")
    title=title.replace('\\',"")
    title=title.replace('/','')
    title=title.replace('.txt','')
    title=title.replace('\r','')
    title=title.replace('\t','')
    title=title.replace('|',"")
    title=title.replace(':',"")
    title=title.replace('*',"")
    title=title.replace('"',"")
    title=title.replace('<',"")
    title=title.replace('>',"")
    title=title+'.txt'
    print('title after rewqork: '+title)

    if(check_if_exists(title)==False):
        print(check_if_exists(title))
        print("prepare work on title:  "+title)
        if isinstance(title,type(None)) or title=="" or title==" ":
            title="no name : "+time.ctime()
        print("title ok, creating file..")
        file=open(os.getcwd()+'\\workspace\\'+str(title),'w')
        print("file created at "+time.ctime())
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
        


    
    
    










