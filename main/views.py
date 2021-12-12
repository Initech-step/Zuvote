from django.shortcuts import render, redirect
from django.http import HttpResponse
from main.forms import RegisterForm, CreateCompetitionForm, ContestantsForm, PaymentForm
#import Login
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from main.models import Contestants, Competitions
from django.views.decorators.http import require_http_methods
# Create your views here.



def index(request):
    return render(request, 'main/index.html', {})

def payment(request):
    form = PaymentForm()
    return render(request, 'main/payment.html', {'form': form})


def choice(request, pk):
    get_contestant = Contestants.objects.get(id=pk)
    return render(request, 'main/choice.html', {'contestant': get_contestant})


def voting(request):
    get_contestants = Contestants.objects.all
    return render(request, 'main/choose.html', {'packages':get_contestants})

@login_required(redirect_field_name = 'signin')
def setall(request):
    get_competitions = Competitions.objects.filter(creator=request.user.id)
    return render(request, 'main/setall.html', {'packages':get_competitions})


@login_required(redirect_field_name = 'signin')
def panel(request):
    return render(request, 'main/welcome_admin.html', {})


@login_required(redirect_field_name = 'signin')
def addcontestant(request):

    if request.method == 'POST':
        form = ContestantsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('Candidate Successfully registered')
        else:
            return HttpResponse('Candidate Not registered')
    form = ContestantsForm()
    return render(request, 'main/register_contestants.html', {'form':form})


@login_required(redirect_field_name = 'signin')
def updel(request):
    getall = Contestants.objects.all
    return render(request, 'main/updel.html', {'packages':getall})



@login_required(redirect_field_name = 'signin')
def create(request):
    if request.method == 'POST':
        form = CreateCompetitionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('Competition Successfully Created')
        else:
            return HttpResponse('Did Not Create Competion, Please Obey all validation Rules')
        
    form = CreateCompetitionForm()
    return render(request, 'main/create_competition.html', {'form':form})



def signin(request):

    if request.method == 'POST':
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('panel')
        else:
            return HttpResponse("<h1>An error occured</h1>")

    login_form = AuthenticationForm()
    return render(request, 'main/login.html', {'form':login_form})



def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("You Have been registered")
        else:
            return HttpResponse("Invalid Form")

    form = RegisterForm()
    return render(request, 'main/register.html', {'form':form})

def update(request, pk):

    getcontestant = Contestants.objects.get(id=pk)
    form = ContestantsForm(instance=getcontestant)

    if request.method == "POST":
        form = ContestantsForm(request.POST, request.FILES, instance=getcontestant)
        if form.is_valid():
            form.save()
            return redirect('updel')
        else:
            return HttpResponse("<h1> An Error Ocured</h1>")

    return render(request, 'main/register_contestants.html', {'form':form})