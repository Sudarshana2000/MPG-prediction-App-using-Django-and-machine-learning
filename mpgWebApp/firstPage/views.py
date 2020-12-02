from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import pickle
import sqlite3

loaded_model=pickle.load(open('../MLmodel/mpgmodel.pkl','rb'))
keys=['carID','cylinders', 'displacement', 'horsepower', 'weight','acceleration', 'model_year', 'origin']

# Create your views here.
def index(request):
    #print(request) -- GET
    context={'a':'Welcome to the first page'}
    return render(request,'index.html',context)
    #return HttpResponse({'Welcome to the first page':1})

def predictMPG(request):
    #print(request) -- POST
    if request.method == 'POST':
        temp=[]
        temp.append(request.POST.get('cylinderVal'))
        temp.append(request.POST.get('dispVal'))
        temp.append(request.POST.get('hrsPwrVal'))
        temp.append(request.POST.get('weightVal'))
        temp.append(request.POST.get('accVal'))
        temp.append(request.POST.get('modelVal'))
        orig = request.POST.get('originVal')
        if orig == 1:
            temp.extend([1,0])
        elif orig == 2:
            temp.extend([0,1])
        else:
            temp.extend([0,0])
        sample=pd.DataFrame(temp).transpose()
        scoreval=loaded_model.predict(sample)[0,0]
        temp=temp[:-2]
        temp.append(orig)
        temp.insert(0,request.POST.get('carID'))
        temp=dict(zip(keys,temp))
    context={'scoreval':scoreval,'temp':temp}
    return render(request,'index.html',context)

def viewDatabase(request):
    conn=sqlite3.connect('../MPGDatabase.db')
    cur=conn.execute("SELECT * FROM MPGTABLE")
    countRows=len(cur.fetchall())
    conn.close()
    context={'countRows':countRows}
    return render(request,'viewDB.html',context)

def updateDatabase(request):
    temp=[]
    temp.append(request.POST.get('carID'))
    temp.append(request.POST.get('cylinderVal'))
    temp.append(request.POST.get('dispVal'))
    temp.append(request.POST.get('hrsPwrVal'))
    temp.append(request.POST.get('weightVal'))
    temp.append(request.POST.get('accVal'))
    temp.append(request.POST.get('modelVal'))
    temp.append(request.POST.get('originVal'))
    temp.append(request.POST.get('mpgVal'))
    conn=sqlite3.connect('../MPGDatabase.db')
    p=conn.execute("INSERT INTO MPGTABLE VALUES {}".format(tuple(temp)))
    conn.commit()
    cur=conn.execute("SELECT * FROM MPGTABLE")
    countRows=len(cur.fetchall())
    conn.close()
    context={'countRows':countRows}
    return render(request,'viewDB.html',context)

def searchDatabase(request):
    carDetails=None
    ID=''
    if request.method == 'POST':
        ID=request.POST.get('car_ID')
        conn=sqlite3.connect('../MPGDatabase.db')
        cur=conn.execute('SELECT * FROM MPGTABLE WHERE carID="'+str(ID)+'";')
        if(len(cur.fetchall())>0):
            cur=conn.execute('SELECT * FROM MPGTABLE WHERE carID="'+str(ID)+'";')
            k=keys[:]
            k.append('mpg')
            for r in cur:
                carDetails=dict(zip(k,r))
        conn.close() 
    context={'ID':ID,'carDetails':carDetails}
    return render(request,'searchDB.html',context)