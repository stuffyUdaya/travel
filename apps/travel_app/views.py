from django.shortcuts import render,redirect
from .models import User,Trip,Join
from django.urls import reverse
from django.contrib import messages
# Create your views here.
def index(request):

    # join =  Join.objects.filter(trip_id = 3)
    # print join[1].user.name
    # join = Join.objects.all()
    # Accessing individual tuples from a query set
    # print join[0].trip.datefrom
    # join =  Join.objects.filter(user_id = 1 )
    # print join[0].trip.dateto

    return render(request,'travel_app/index.html')
def process(request):
    results = User.objects.userValidator(request.POST['name'],request.POST['u_name'],request.POST['password'],request.POST['confpassword'])
    if results[0]:
        for err in results[1]:
            print err
            messages.error(request,err)
    else:
        request.session ['loggedin'] = results[1].id
        return redirect('/success')
    return redirect('/')
def login(request):
        postData ={
        'u_name': request.POST['u_name'],
        'password': request.POST['password']
        }
        results = User.objects.loginValidator(postData)
        if results[0]:
            request.session['loggedin'] = results[1].id
            return redirect('/success')
        else:
            messages.error(request,results[1])
            return redirect('/')
def success(request):
    trip = Trip.objects.filter(owner_id = request.session['loggedin'])
    # print trip[0].destination
    print '$'* 35
    # print Join.objects.filter(user_id = request.session['loggedin'] )
    trip =  Trip.objects.filter(owner_id = request.session['loggedin'] )
    join = Join.objects.filter(user_id = request.session['loggedin'] )
    trip_other = Trip.objects.exclude(owner_id = request.session['loggedin'] )

    for x in join :
        print x.trip_id
        trip_other = trip_other.exclude(id = x.trip_id)
        print trip_other

    context={
    'user':  User.objects.filter(id = request.session['loggedin']),
    'join':  join,
    'trips1':  trip,
    'trip_other': trip_other
    # exclude(user_id = request.session['loggedin'] ),
    # 'views1': Trip.objects.exclude(owner = request.session['loggedin'] ),
    }

    return render(request,'travel_app/success.html',context)
def addtravelplan(request,id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request,'travel_app/addtravel.html',context)


def addtrip(request,id):
    # print '*'*34
    user = User.objects.get(id=id)
    # userid =  user.id
    # print userid
    # print '*'*34
    trip= Trip.objects.create(destination = request.POST['destination'], description = request.POST['description'],datefrom = request.POST['datefrom'], dateto = request.POST['dateto'],owner = user )
    Join.objects.create(user = user, trip = trip)
    return redirect('/success')


def viewtrip(request,id):
    # views = Join.objects.filter(trip_id = id)

    user= User.objects.get(id = request.session['loggedin'])
    context={
     'views1': Trip.objects.get(id = id),
     'views' : Join.objects.filter(trip_id = id)
    }
    # print Trip.owner.fi(id=id)
    #
    return render(request,'travel_app/viewtravel.html',context)

def jointrip(request,id,uid):
    print '$'*32
    print id
    trip = Join.objects.filter(trip_id = id)
    print trip
    views = Join.objects.create(user_id = uid , trip_id = id )
    # print views
    print '$' * 32
    return redirect('/success')

def logout(request):
    return redirect('/')
