import re
pattern=re.compile(r"[-!#$%&'()* ,./:;<=>?@_`{|}~а-я0-9\s+]")
x=input()
a=["cp866","cp1251","koi8-r","iso8859-5","mac-cyrillic"]
for i in range(0,5):
    file=open(x,'r',encoding=a[i]).read(11)
    file1=file.encode('utf_8').decode('utf_8')
    if len(pattern.findall(file1)) == 11:
           #print(a[i])
           break
q=open(x,'r',encoding=a[i])
file2=q.read(2048)
print(file2.encode('utf_8'))
q.close()   
