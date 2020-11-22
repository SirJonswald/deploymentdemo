from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import *
def index(request):
    return render(request, "login.html")

def register(request):
    print(request.POST)
    errorsFromValidator = User.objects.registrationValidator(request.POST)
    print("ERRORS FROM VALIDATOR BELOW")
    print(errorsFromValidator)
    if len(errorsFromValidator) > 0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hashedPassword = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(first_name = request.POST['fname'], last_name= request.POST['lname'], email = request.POST['email'], password = hashedPassword)
        # use session to store ID of the logged in user
        request.session['loggedInId']= newUser.id
    return redirect("/success")

def success(request):
    if 'loggedInId' not in request.session:
        messages.error(request, "You must be logged in first!")
        return redirect("/")
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
        'allTrips': Travel.objects.all(),
        'favTrips': Travel.objects.filter(favoritors= User.objects.get(id=request.session['loggedInId'])),
        'nonFavTrips': Travel.objects.exclude(favoritors= User.objects.get(id=request.session['loggedInId']))
    }
    return render(request, 'success.html', context)

def login(request):
    print(request.POST)
    errorsFromValidator = User.objects.loginValidator(request.POST)
    print("ERRORS FROM VALIDATOR BELOW")
    print(errorsFromValidator)
    if len(errorsFromValidator) > 0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/")
    else:
        usersWithSameEmail = User.objects.filter(email = request.POST['email'])
        request.session['loggedInId']= usersWithSameEmail[0].id
    return redirect("/success")

def logout(request):
    request.session.clear()
    return redirect("/")

def createTrip(request):
    return render(request, "newTrip.html")

def uploadTrip(request):
    print(request.POST)
    errorsFromValidator = Travel.objects.createTripValidator(request.POST)
    print(errorsFromValidator)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect("/trips/create")
    else:
        Travel.objects.create(description= request.POST['tripName'], plan= request.POST['disc'],
        creator = User.objects.get(id=request.session['loggedInId']), start_date= request.POST['startDate'], end_date= request.POST['endDate'])
    return redirect("/success")

def tripInfo(request, tripId):
    context = {
        'oneTrip': Travel.objects.get(id= tripId)
    }
    return render(request, "tripInfo.html", context)

def addFav(request, tripId):
    Travel.objects.get(id=tripId).favoritors.add(User.objects.get(id=request.session['loggedInId']))
    return redirect("/success")

def removeFav(request, tripId):
    Travel.objects.get(id=tripId).favoritors.remove(User.objects.get(id=request.session['loggedInId']))
    return redirect("/success")