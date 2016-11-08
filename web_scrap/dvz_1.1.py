from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import os

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
    return os.path.isfile(file)




def grab(url):
    try:
        page=urlopen(url)
        soup=BeautifulSoup(page, 'html.parser')
        return soup.title,soup 
    except Exception:
        return None

def urlize(url):
    return "http://www."+url

def get_all(url):
    lista=[]
    try:
        page,title=urlopen(url)
        soup=BeautifulSoup(page,'html.parser')
    except Exception:
        pass
    for link in soup.find_all('a'):
        lista.append(link.get('href'))
    return title,lista

def get_urls(url):
    lista=[]
    try:
        page=urlopen(url)
        print("debug open url ok "+url)
        soup=BeautifulSoup(page,'html.parser')
        print("debug soup ok "+url)
        title=soup.title
        title=title.get_text()
        print("debug get title2 ok "+title)
        if url[-1]=='/':
            url=url[:-1]
            print("debug___url ends with/")
        for link in soup.find_all('a'):
            repo=link.get('href')
            if isinstance(repo,str):
                if len(repo)>4:
                    if repo[0:4]=='http':
                        lista.append(repo)
                    elif repo[0:4]=='/www':
                            lista.append("http:/"+repo)
                    elif repo[0:5]=='//www':
                            lista.append("http:"+repo)
                    elif repo[0]=='/' and repo[1]!='/' and repo[0:4]!='/www':
                            lista.append(url+repo)
                    elif repo[0]=='/' and repo[1]=='/' and repo[0:5]!='//www':
                            lista.append(url+repo[1:])
        if isinstance(title,type(None))==True:
            print("debug title is none string !!!!!!!!!!!!!! ")
            title="no title "+time.ctime() 
    except Exception:
        print ("exception entered on link "+url)
        title='invalid link:'+url
        title.replace('\'','_')
        title.replace('/','_')
        title.replace(':','_')
        title=title[0:20]
    print ("exit ok returned: title"+str(type(title))+" len array "+str(len(lista)))
    return  title,lista

def save(name,lista):
    name=name.replace('\n',"")
    name=name.replace('/','')
    name=name+'.txt'
    print('name: '+name)
    if(check_if_exists(name)==False):
        print(check_if_exists(name))
        print("just saved file  "+name)
        if isinstance(name,type(None)) or name=="":
            name="no name : "+time.ctime()
        file=open('workspace\\'+str(name)+".txt",'w')
        for x in lista:
            file.write(x+"\n")
        file.close()
    else:
        print('file exists')




def grab_file(file):
    #presupunem ca fisierul e in working directory os.getcwd()
    file=open('workspace\\'+file,'r')
    print("debug open file OK")
    for x in file:
        title,repo=get_urls(x)
        print("working on:"+title) 
        save(title,repo)
        


    
    
    










