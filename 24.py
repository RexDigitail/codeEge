f=open('24.txt')
temp=1
max=0
x=f.read()
for i in range(len(x)):
    if ((x[i]!='P')):
        temp+=1
    elif((x[i]=='P')):
        if(temp>=max):
            max=temp
        temp = 0
print(max)



