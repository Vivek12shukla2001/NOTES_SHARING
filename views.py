from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from.models import *
from django.contrib.auth import authenticate,logout,login
from datetime import date

# Create your views here.
def about(request):
    return render(request,'about.html')

def index(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'contact.html')

def userlogin(request):
    error = ''
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['pass']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = 'no'
            else:
                error = 'yes'
        except:
            error = 'yes'
    d = {'error': error}
    return render(request, 'login.html',d)


def login_admin(request):
    error = ''
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = 'no'
            else:
                error = 'yes'
        except:
            error = 'yes'
    d = {'error': error}
    return render(request, 'login_admin.html', d)


def signup1(request):
    error = ""
    if request.method == "POST":
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        e = request.POST['email']
        p = request.POST['password']
        b = request.POST['branch']
        r = request.POST['role']
        try:
            user = User.objects.create_user(username=e,password=p,first_name=f,last_name=l)
            Signup.objects.create(user=user, contact=c, branch=b, role=r)
            error = "no"
        except:
            error = "yes"
    d={'error':error}

    return render(request,'signup.html',d)


def admin_home(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    return render(request,'admin_home.html')


def Logout(request):
    logout(request)
    return redirect('index')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)
    d = {'data':data,'user':user}
    return render(request,'profile.html',d)

def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error=''
    if request.method=="POST":
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c==n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error='no'
        else:
            error='yes'
    d = {'error':error}
    return render(request,'changepassword.html')

def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user=user)
    error = False
    if request.method == "POST":
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        b = request.POST['branch']
        user.first_name = f
        user.last_name = l
        data.contact = c
        data.branch = b
        user.save()
        data.save()
        error = True

    d = {'data':data, 'user':user,'error':error}
    return render(request,'edit_profile.html', d)

def upload_notes(request):
    error = ""
    if request.method == "POST":
        b = request.POST['branch']
        s = request.POST['subject']
        n = request.POST['notesfile']
        f = request.POST['filetype']
        d = request.POST['description']
        u = User.objects.filter(username=request.user.username)
        try:
            user = Notes.objects.create_user(user=u,uploadinggate=date.today(),branch=b,subject=s,
                                             notesfile=n,filetype=f,description=d,status='Pending')
            error = "no"
        except:
            error = "yes"
    d={'error':error}

    return render(request,'upload_notes.html',d)

