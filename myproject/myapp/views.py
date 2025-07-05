from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score

def home(request):
    result2=None
    df=pd.read_csv('data.csv')
    

    x=df[['temp','humidity','ph']]
    y=df['rain']

    x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=7)

    model=LogisticRegression()
    model.fit(x_train,y_train)

    y_pred=model.predict(x_test)
    result=r2_score(y_test,y_pred)
    if (request.method == 'POST'):
        a = int(request.POST.get('temp'))
        b = int(request.POST.get('humi'))
        c = int(request.POST.get('ph'))
        p=model.predict([[a,b,c]])
        if(p<50):
            result2="no rain"
        else:
            result2="rain"    

    
    return render(request, 'home.html', {
        'result2': result2
})

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('num1')
        password = request.POST.get('num2')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,'login.html')
    
def registerpage(request):
    if request.method == 'POST':
        username = request.POST.get('num1')
        password = request.POST.get('num2')
        conform = request.POST.get('num3')
        if password != conform:
            return render(request,'register.html',{'result':'ERROR'})
        user=User.objects.create_user(username=username,password=password)
        return redirect('login')
    return render(request,'register.html')

def logoutpage(request):
    logout(request)
    return redirect('login')
