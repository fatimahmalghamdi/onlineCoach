from multiprocessing import context
from django.shortcuts import render,redirect, HttpResponse
from .models import User, Coach
from django.contrib import messages
import bcrypt

# Create your views here.

def mainPage(request):
        return render(request, 'registration.html')

def welcome(request):
    context = {
        'coaches': Coach.objects.all()
    }
    return render(request, 'welcomePage.html', context)

def new_fun(request):
    return render(request, 'correct.html')



def registeration(request):
    if request.method == 'POST':
        any_errors = User.objects.basic_validate(request.POST)
        if len(any_errors) > 0:
            for key, value in any_errors.items():
                messages.error(request, value)
            return redirect('/mainPage/registration')
        else:
            print(request.POST['password'])
            print(request.POST['conf_password'])
            first_name= request.POST['first_name']
            last_name= request.POST['last_name']
            email= request.POST['email']
            passw= request.POST['password']
            birthdate= request.POST['birthdate']
            height= request.POST['height']
            weight= request.POST['weight']
            pass_hash= bcrypt.hashpw(passw.encode(), bcrypt.gensalt()).decode()
            # check if the user is a Trainee
            if request.POST['check'] == 'Register_Trainee':
                new_trainee= User.objects.create(first_name= first_name, last_name= last_name, email= email, birthdate= birthdate, height= height, weight= weight, password= pass_hash)
                request.session['trainee_id']= new_trainee.id
                messages.success(request, 'The Trainee has been added successfully :)')
            # check if the user is a Coach
            elif request.POST['check'] == 'Register_Coach':
                any_errors = User.objects.basic_validate_coach(request.POST)
                if len(any_errors) > 0:
                    for key, value in any_errors.items():
                        messages.error(request, value)
                    return redirect('/mainPage/registration')
                else:
                    desc= request.POST['desc']
                    img= request.FILES['coach_img']
                    new_coach= Coach.objects.create(first_name= first_name, last_name= last_name, email= email, birthdate= birthdate, height= height, weight= weight, profile_pic= img, brief= desc, password= pass_hash)
                    request.session['coach_id']= new_coach.id
                    messages.success(request, 'The Coach has been added successfully :)')
            # ///////////// Need to change route /////////////////////////////////////////
            return redirect('/mainPage/registration/change_here')
    else:
        return render(request, 'registration.html')


def login(request):
    if request.method == "POST":
            any_errors = User.objects.validate_login(request.POST)
            if len(any_errors) > 0:
                for key, value in any_errors.items():
                    messages.error(request, value)
                return redirect('/mainPage/login')
            else:
                email = request.POST["email"]
                password = request.POST["password"]
                try:
                    # fetch user by his email
                    fetch_user= User.objects.get(email= email)
                    if bcrypt.checkpw(password.encode(), fetch_user.password.encode()):
                        # check if he is a coach or not by ID in Coach table
                        if Coach.objects.filter(id=fetch_user.id):
                            request.session["coach_id"] = fetch_user.id
                            messages.success(request, "Coach is logged in!")
                        else:
                            request.session["trainee_id"] = fetch_user.id
                            messages.success(request, "Trainee is logged in!")
                        # ///////////// Need to change route ///////////////////
                        return redirect('//mainPage/registration/change_here')
                    else:
                        messages.error(request, "the password does not match your record, try again!")
                        return redirect('/mainPage/login')
                except User.DoesNotExist:
                        messages.error(request, "User not found")
                        return redirect('/mainPage/login')
    else:
        return render(request, 'login.html')


def logout(request):
    request.session.clear()
    messages.success(request, "You are logged out!")
    return redirect("/")

