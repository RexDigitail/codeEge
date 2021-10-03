k=0
l=0
s=0
m=0
for i in range(120115000,120200000+1):
    for j in range(1,int(i**0.5)+1):
        if int(i**0.5)**2==i:
            m=1
        if (i%j)==0:
            l+=2
    if l-m>=k:
        k=l
        s=i
    l=0
    m=0
print(k,s)



