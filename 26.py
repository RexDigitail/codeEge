f=open("26.txt")#открыли файл
x,y=map(int,f.readline().split())#длина архива + колво элементов
a=[0]*y#создали массив для пользователей
u=0
b=x
n=0
g=0
for i in range(y):
    p=int(f.readline())
    a[i]=p#забили массив
a.sort()#отсортировали от мин к максимуму файлы
for i in range(y):
    if(x-a[i]>=0):
        x=x-a[i]
        n+=a[i]
        u+=1#счётчик файлов
g=a[u-1]
for i in range (y-1,0,-1):
    if (n-g+a[i]<=b):
        g=a[i]
        break

print(u,g)

