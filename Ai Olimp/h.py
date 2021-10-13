import re
'''import sys
from importlib import reload
reload(sys)
sys.setdefaultencoding('UTF-8')'''
new=str()
pattern=re.compile(r"[-!#$%&'()* ,./:;<=>?@_`{|}~а-я0-9\s+]")
x=str(input())
a=["cp866","cp1251","koi8_r","iso8859_5","mac_cyrillic"]
for i in range(0,5):
    file=open(x,encoding=a[i]).read(11)
    file=file.encode('utf_8').decode('utf_8')
    if len(pattern.findall(file)) == 11:
        break
#print(a[i])
q=open(x,encoding=a[i])
file1=q.read()
for i in range(len(file1)-2):
    if file1[i]=='\n':
        if file1[i+1]==file1[i+1]==' ':
            new=new+file1[i]
        else:
            new = new + ' '
    else:
        new = new + file1[i]
a = re.sub(r' +', ' ', new)
new1=a[0:2047]
print(new1.encode('utf_8').decode('utf_8'))
    
