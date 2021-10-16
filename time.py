k=1
t=0
a=[0]*6
#312651-312614
for i in range(12,15+1):#312614,312651
    if (i%k==0 and k<=i/2 and t<=4):
        a.append(k)
        a.append(i/k)
        k+=1
        t+=2
       
    else:
        if(k>i/2):
            for i in range(t):
                print(a[i])
                a=[]
                k=1
                t=0
            
        
        
        
        
