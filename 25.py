
temp=0
delMin=0
delMax=0
while (temp!=5):
    for i in range (2,x):
        if(x%i==0):
            delMin=i
            delMax=x//i
            break
    a=delMin + delMax
    if (a%10==8):
        temp+=1
        print(x, a)
    x+=1
