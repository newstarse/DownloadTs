#这是一个用于下载ts的小程序
#它首先下载index.m3u8文件，分析出其中的key文件和所有的小ts文件
#然后分别下载key文件和ts文件
#再利用key文件中的密钥解密ts文件
#最后将所有的ts文件合并成一个大视频文件

import re
import urllib.request
import sys
import os
from Crypto.Cipher import AES
def downFile(url, sFile):
    try:
        fp = urllib.request.urlopen(url,data=None, timeout=10)
        data = fp.read()
        fp.close()
        fout = open(sFile,"wb")
        fout.write(data)
        fout.close()
        return True
    except:
        return False  
 
def saveFile(lines, saveFile):
    try:
        fout = open(saveFile, "w")
        for line in lines:
            if(len(line)>0):
                fout.writelines(line+"\n")
        fout.close()
        return True
    except:
        return False
    
def downTs(baseurl, urlFile,start, end):
    fin = open(urlFile,"r")
    data = fin.read()
    fin.close()
    lines = data.split('\n')
    cnt = 1
    for line in lines[start:end+1] :
        sFile = ".\\orgvideo\\"+f"{cnt:04d}.ts"
        if line.startswith('http'):
            fullurl = line
        else:
            fullurl = baseurl+line
        if downFile(fullurl, sFile):
            print(f'{line[-12:]} {cnt:04d}........OK')
            cnt += 1
        else:
            print(f'{line[-12:]} {cnt:04d}...failure')
    return cnt-1

def decryptTs(cnt,keyFile):
    fin = open(keyFile, "r")
    key = fin.read()
    cipher = AES.new(bytes(key.encode()), AES.MODE_CBC)
    for i in range(1,cnt+1):
        finname = f'.\\orgvideo\\{i:04d}.ts'
        fin = open(finname,"rb")
        data = fin.read()
        fin.close()
        msg = cipher.decrypt(data)
        fout = open(f".\\decrypt\\{i:04d}.ts","wb")
        fout.write(msg)
        fout.close()
        print(finname)

def mergeTs(start, end, source):
    fout = open(".\\merge\\merge.ts","wb")
    for i in range(start,end+1):
        finname = f'{source}{i:04d}.ts'  #.\\decrypt\\
        fin = open(finname,"rb")
        data = fin.read()
        fin.close()
        fout.write(data)
    fout.close() 

def delFiles(path):
    fileList = os.listdir(path)
    for filename in fileList:
        os.remove(path+'\\'+filename)
        #print(filename)

def getRealM3u8(baseurl):  
    #判断这个index.m3u8文件中是否还包含了m3u8文件
    url = ""
    fileSize = os.stat("index.m3u8").st_size
    if fileSize < 500 :  #文件太小，应该是包含了另外一个m3u8下载路径
        fin = open("index.m3u8","r")
        for line in fin :
            if line.endswith("index.m3u8\n") :
                url = baseurl + line[:-1]
                print("找到了一个新的m3u8文件: " + url + " 准备开始下载")
                fin.close()
                break
        if len(url) > 0 :
            if downFile(url, "index.m3u8") :
                print(url + " 下载成功，重新开始分析")
            else :
                print(url + " 下载失败，请打开原文件分析失败原因")
                sys.exit()
    #到目前这一步，要么重新下载了新的m3u8文件，要么还是使用原来的m3u8文件，开始读取数据
    fin = open("index.m3u8","r")
    data = fin.read()
    fin.close()
    return data
      

def interactive():
    m3u8url=input("请输入index.m3u8的下载地址。注意最后的文件名必须是index.m3u8，可以用视频下载工具分析得到这个url\n")
    idx=m3u8url.find("/",8)
    baseurl=m3u8url[:idx]     #从index.m3u8文件的下载地址中获取主网址
    print("主网址为："+baseurl+" , 开始下载index.m3u8")
    if downFile(m3u8url, "index.m3u8"):
        print("index.m3u8下载成功")
    else:
        print("index.m3u8下载不成功，请检查网址是否正确")
        sys.exit()
    print("开始分析index.m3u8文件......")
    data = getRealM3u8(baseurl)
    matchObj = re.findall(r'.+key.key', data, re.M)
    idx = -1
    if len(matchObj) > 0 :
        for obj in matchObj :
            print(obj)
        idx=int(input("准备下载哪一个key文件?(最后一个可以用0表示) "))
        if idx>=0 :
            whichkey = baseurl+matchObj[idx-1][1:-1]
            print("选取的key文件是："+whichkey)
            print("开始下载key文件")
            if downFile(whichkey, "key.key"):
                print("key.key下载成功")
            else:
                print("key.key下载不成功，请检查网址是否正确")
            print("正在保存所有ts文件的url到url.txt中")
            which=data.index(matchObj[idx-1])  #定位到key文件所在位置
            remaind=data[which+len(matchObj[idx-1]) : ]
            lines=remaind.split('\n')[::2]
    else:
        print("不是加密ts文件，正在保存所有ts文件的url到url.txt中")
        remaind=data.split('\n')
        lines=[line for line in remaind if line.endswith(".ts")]
    if saveFile(lines, "url.txt"):
        print("url.txt保存成功")
    else:
        print("url.txt保存失败，请检查原因")
        sys.exit()
    print(f"一共有{len(lines)}个ts文件，准备从第几个下载到第几个？")
    start,end=map(int, input().split())
    cnt = downTs(baseurl, "url.txt",start,end)
    if idx>=0:
        print("下载完成，开始解密ts文件：")
        decryptTs(cnt,"key.key")
        print(f"解密完成，准备合并ts文件，请输入起始编号和结束编号:1~{cnt}")
        start,end=map(int,input().split())
        mergeTs(start,end,".\\decrypt\\")
    else:
        print(f"下载完成，准备合并ts文件，请输入起始编号和结束编号:1~{cnt}")
        start,end=map(int,input().split())
        mergeTs(start,end,".\\orgvideo\\")
    print("合并完成，文件在merge目录下面。是否要删除临时文件？(Y/N)")
    flag=input()
    if flag=='Y' or flag=='y' :
        delFiles('orgvideo')
        if idx>=0:
            delFiles("decrypt")
        print('删除成功')

if __name__=='__main__':
   interactive() 

