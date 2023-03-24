from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from .models import seats, trains, person

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from .models import trains, person




def index(request):
    t1 = trains.objects.filter(tid=1)
    t2 = trains.objects.filter(tid=2)
    t3 = trains.objects.filter(tid=3)
    t3 = trains.objects.filter(tid=4)
    # lis = trains.objects.filter('tid').distinct()
    return render(request, './viewtrains.html', {"t1": t1,
    "t2":t2,"t3":t3,"t4":t4})


def loginform(request):
    return render(request, './login.html')


def login(request):
    u = request.POST
    user = authenticate(request, username=u['name'], password=u['password'])
    if user is not None:
        auth_login(request, user)
        context = {
            'msg': "Login Successsful"
        }
    else:
        context = {
            'msg': "Error User is not registered/invalid"
        }
    return render(request, './error.html', context)


def registerform(request):
    return render(request, './register.html')


def register(request):
    user = request.POST
    u = User.objects.create_user(user['name'], user['email'], user['password'])
    u.save()
    context = {
        'msg': "Registeration Successsful"
    }
    return render(request, './error.html', context)


def logout(request):
    auth_logout(request)

    context = {
        'msg': "Logout Successful"
    }
    return render(request, './error.html', context)


def trainform(request):
    if request.user.is_superuser:
        return render(request, './addtrain.html')
    else:
        return render(request, './error.html', {'msg': "Not an Admin"})


def addtrain(request):
    l = trains(source=request.POST['source'], destination=request.POST['destination'],Coach=request.POST['Coach'], Seat=request.POST['Seat'],
               time=request.POST['time'], seats_available=request.POST['seats_available'],train_name=request.POST['train_name'],price=request.POST['price'])
    l.save()
    return render(request, './error.html', {'msg': "Successfully Added"})


def train_id(request, train_id):
    if not request.user.is_superuser:
        return render(request, './error.html', {'msg': "Not an Admin"})

    l = trains.objects.get(pk=train_id)
    persons = l.person_set.all()
    context = {
        'train': l,
        'persons': persons
    }
    return render(request, './viewperson.html', context)

temp={}
def book(request):

    global temp
    if request.user.is_authenticated:
        t = trains.objects.filter(
            source=request.POST['source'], destination=request.POST['destination'],datee=request.POST['rdate'],Coach=request.POST['coach'],status='y')
        if len(t):
            temp['name']=request.user.username
            return render(request, './trainsavailable.html', {'trains': t,})
        else:
            return render(request, './error.html', {'msg': "Not Found"})
    else:
        return render(request, './error.html', {'msg': "Not a valid user. Please Login to continue"})


# def booking(request, train_id):
#
#     tt = trains.objects.get(pk=train_id)
#     if tt.seats_available == 0:
#         return render(request, './error.html', {'msg': "Seats full"})
#     tt.seats_available -= 1
#
#     p = person(train=tt, name=request.user.username, email=request.user.email)
#     p.save()
#     tt.save()

    # render(request,'./mybooking')

def booking(request, train_id):
    tt = trains.objects.get(pk=train_id)
    if tt.seats_available == 0:
        return render(request, './error.html', {'msg': "Seats full"})
    tt.seats_available -= 1

    p = person(train=tt, name=request.user.username, email=request.user.email)
    p.save()
    tt.save()

    if request.user.is_authenticated:
        p = person.objects.filter(email=request.user.email)
        return render(request, './mybooking.html', {'persons': p})
    else:
        return render(request, './error.html', {'msg': "User not authenticated"})


def pay(request, r_id):

    p = person.objects.get(id=r_id)

    if request.user.is_authenticated:
        return render(request, './pay.html', {'p': p})
    else:
        return render(request, './error.html', {'msg': "User not authenticated"})


def bookform(request):
    t = trains.objects.all()
    sources = []
    destinations = []
    Coach = []
    Seat = []
    Date= []
    for i in t:
        sources.append(i.source)
        destinations.append(i.destination)
        Coach.append(i.Coach)
        Seat.append(i.Seat)

    sources = list(set(sources))
    destinations = list(set(destinations))
    Coach = list(set(Coach))
    Seat = list(set(Seat))


    if request.user.is_authenticated:
        return render(request, './booking.html', {'sources': sources, 'destinations':destinations, 'Coach': Coach, 'Seat':Seat})
    else:
        return render(request, './error.html', {'msg': "User not authenticated"})


def mybooking(request):
    if request.user.is_authenticated:
        p = person.objects.filter(email=request.user.email)
        return render(request, './mybooking.html', {'persons': p})
    else:
        return render(request, './error.html', {'msg': "User not authenticated"})



def delete(request, r_id):
    person.objects.get(id=r_id).delete()

    p2 = person.objects.filter(email=request.user.email)
    if request.user.is_authenticated:
        # return redirect('./../mybooking', {'persons': p2})
        return render(request, './mybooking.html', {'persons': p2})
    else:
        return render(request, './error.html', {'msg': "User not authenticated"})


# Generate a PDF
def get_ticket(request, r_id):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    #Add some lines of text
    # lines = [
	# 	"This is line 1",
	# 	"This is line 2",
	# 	"This is line 3",
	# ]

    p = person.objects.get(id = r_id)

	# # Designate The Model
	# train = trains.objects.all()
	# Create blank list
    lines = ['Ticket Details', '']

    # lines.append('a')
    # lines.append('b')
    # lines.append('c')
    # lines.append('d')

    lines.append('Passenger Details')
    lines.append('Passenger Name : ' + p.name)
    # lines.append('Passenger Age : ' + str(p.age))
    # lines.append('Passenger Gender : ' + p.gender)
    lines.append('Passenger Email : ' + p.email)
    lines.append('')
    lines.append('Train Details')
    lines.append('Train Name : ' + p.train.train_name)
    lines.append('From : ' + p.train.source)
    lines.append('To : ' + p.train.destination)
    lines.append('Depurture Time : ' + '')
    lines.append('Depurture Date : ' + '')
    lines.append('Coach Type : ' + p.train.Coach)
    lines.append('Seat No. : ' + p.train.Seat)




    # lines.append(p.date_and_time_of_booking)
    # lines.append(p.train.price)


	# Loop
    for line in lines:
        textob.textLine(line)

	# Finish Up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
	# Return something
    return FileResponse(buf, as_attachment=True, filename='ticket.pdf')

def payupdate(request, r_id):
    p = person.objects.get(id=r_id)
    p.pay_check = 1
    p.save()

    p2 = person.objects.filter(email=request.user.email)
    if request.user.is_authenticated:
        # return redirect('./../mybooking', {'persons': p2})
        return render(request, './mybooking.html', {'persons': p2})
    else:
        return render(request, './error.html', {'msg': "User not authenticated"})
