from .forms import CreateCompetitionForm, ContestantCreationForm, RequestPayForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Competitions, Contestants, RequestPay
import secrets
from accounts.models import ExtraUserData
from voting.models import Payments
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
# Create your views here.
# Create your views here.

@login_required(redirect_field_name='login_zuvote')
def create_competition(request):
    if request.method == 'POST':
        form = CreateCompetitionForm(request.POST, request.FILES)
        
        if form.is_valid():
            print(form.cleaned_data)
            hold = form.save(commit=False)
            hold.Competition_slug = secrets.token_urlsafe(14)
            hold.competition_creator = request.user

            hold.save()
            messages.add_message(request, messages.INFO, 'Competition Successfully created')
            return redirect('set_managing')

    form = CreateCompetitionForm(request.POST or None)
    return render(request, 'engine/create_competition.html', {'form': form})


@login_required(redirect_field_name='login_zuvote')
def panel(request):
    return render(request, 'engine/first_panel_page.html')

@login_required(redirect_field_name='login_zuvote')
def set_managing(request):
    get_all_competitions = Competitions.objects.filter(competition_creator=request.user)
    return render(request, 'engine/choose_managing.html', {'competitions': get_all_competitions})

@login_required(redirect_field_name='login_zuvote')
def set_managing_b(request, slug):
    get_user = ExtraUserData.objects.get(user=request.user)
    get_user.currently_managing = slug
    get_user.save()
    return redirect('add_contestant')

@login_required(redirect_field_name='login_zuvote')
def add_contestant(request):
    #get the user and currently managed competition
    get_user = ExtraUserData.objects.get(user=request.user)
    get_currently_managing = get_user.currently_managing

    if get_currently_managing == None:
        return redirect('set_managing')

    if request.method == 'POST':
        form = ContestantCreationForm(request.POST, request.FILES)
        print('request files', request.FILES)

        #get the competition currently managed
        contestant_comp = Competitions.objects.get(Competition_slug=get_currently_managing)

        #validate form and save
        if form.is_valid():
            holder = form.save(commit=False)
            
            holder.competition_involved = contestant_comp
            holder.save()
            messages.add_message(request, messages.INFO, 'Contestant Successfully added')
            return redirect('add_contestant')
            #take actions

    form = ContestantCreationForm(request.POST or None)
    return render(request, 'engine/create_contestant.html', {'form':form})


@login_required(redirect_field_name='login_zuvote')
def view_all_contestants(request):
    get_hold_of_user = ExtraUserData.objects.get(user=request.user)
    get_currently_managing = get_hold_of_user.currently_managing

    if get_currently_managing == None:
        return redirect('set_managing')

    #pick competition
    hold_competition = Competitions.objects.get(Competition_slug=get_currently_managing)

    #get contestants in those competitions
    get_all_contestants = Contestants.objects.filter(competition_involved=hold_competition)
    return render(request, 'engine/view_all_contestants.html', {'contestants':get_all_contestants})



@login_required(redirect_field_name='login_zuvote')
def delete_contestant(request, pk):
    # get contestant
    get_contestant = Contestants.objects.get(id=pk)
    #get competiton engaged
    competition_engaged = get_contestant.competition_involved
    #get the creator
    get_creator = competition_engaged.competition_creator

    if get_creator == request.user:

        if request.method == 'POST':
           get_contestant.delete()
           messages.add_message(request, messages.INFO, 'Contestant Successfully deleted')
           return redirect('view_all_contestants')
        else:
            return render(request, 'engine/confirm_delete_contestant.html', {'contestant': get_contestant})

    else:
        return HttpResponse('I no send u')



@login_required(redirect_field_name='login_zuvote')
def edit_contestant(request, pk):
    get_contestant = Contestants.objects.get(id=pk)
    competition_engaged = get_contestant.competition_involved
    #get the creator
    get_creator = competition_engaged.competition_creator
    #get_curently managing 
    
    if get_creator == request.user:   

        if request.method == 'POST':
           form = ContestantCreationForm(request.POST, request.FILES, instance=get_contestant)

           if form.is_valid():

               hold = form.save(commit=False)
               hold.competition_involved = competition_engaged
               hold.save()

               messages.add_message(request, messages.INFO, 'Contestant Successfully Updated')
               return redirect('view_all_contestants')

        else:
            form = ContestantCreationForm(request.POST, request.FILES, instance=get_contestant)
            return render(request, 'engine/create_contestant.html', {'form': form})
    else:
        return HttpResponse('I no send u')



@login_required(redirect_field_name='login_zuvote')
def set_active_state(request):
    get_user = ExtraUserData.objects.get(user=request.user)
    get_currently_managing = get_user.currently_managing

    #check if he has a competition he is managing
    if get_currently_managing == None:
        return redirect('set_managing')

    get_the_competition = Competitions.objects.get(Competition_slug=get_currently_managing)

    if request.method == 'POST':

        if get_the_competition.active == True:

            get_the_competition.active = False
            get_the_competition.save(update_fields=['active'])
            return redirect('set_active_state')
        else:

            get_the_competition.active = True
            get_the_competition.save(update_fields=['active'])
            return redirect('set_active_state')

    if get_the_competition.active == True:
        state = 'This competition is open for votes'
    else:
        state = 'This competition is closed for votes'

    return render(request, 'engine/set_active_state.html', {'competition_details': get_the_competition, 'state':state})



@login_required(redirect_field_name='login_zuvote')
def view_stat(request):
    get_hold_of_user = ExtraUserData.objects.get(user=request.user)
    get_currently_managing = get_hold_of_user.currently_managing
     
    if get_currently_managing != None:
        #pick competition
        hold_competition = Competitions.objects.get(Competition_slug=get_currently_managing)

        #get contestants in those competitions
        get_all_contestants = Contestants.objects.filter(competition_involved=hold_competition)
        return render(request, 'engine/view_contestants_stat.html', {'contestants':get_all_contestants})
    else:
        return redirect('set_managing')

@login_required(redirect_field_name='login_zuvote')
def view_transactions(request):
    get_hold_of_user = ExtraUserData.objects.get(user=request.user)
    #get the currently managed competition
    get_currently_managing = get_hold_of_user.currently_managing

    #check if he has set the managing
    if get_currently_managing == None:
        return redirect('set_managing')
        
    #get the competition
    get_competition = Competitions.objects.get(Competition_slug=get_currently_managing)
     
    if get_currently_managing != None:
        get_all_payments = Payments.objects.filter(competition=get_competition)
        return render(request, 'engine/view_transactions.html', {'transactions': get_all_payments})
    else:
        return redirect('set_managing')




@login_required(redirect_field_name='login_zuvote')
def main_panel(request):
    get_hold_of_user = ExtraUserData.objects.get(user=request.user)
    #get the currently managed competition
    get_currently_managing = get_hold_of_user.currently_managing
    #get the competition
    get_competition = Competitions.objects.get(Competition_slug=get_currently_managing)
  
    return render(request, 'engine/base_panel.html', {'competition_currently_managed': get_competition})



@login_required(redirect_field_name='login_zuvote')
def take_pay(request):
    get_hold_of_user = ExtraUserData.objects.get(user=request.user)
    get_currently_managing = get_hold_of_user.currently_managing
     
    if get_currently_managing != None:
        #get the competition
        get_competition = Competitions.objects.get(Competition_slug=get_currently_managing)
        #get all verified votes in that competition #aggregate the amount
        balance1 = Payments.objects.filter(competition=get_competition).filter(verified=True).aggregate(Sum('amount'))
        bal2 = balance1['amount__sum']
        #this is to counter the none error in case balance is non
        if bal2 != None:
            bal2 = balance1['amount__sum']/100
        else:
            bal2 = balance1['amount__sum']

        #check form data
        if request.method == 'POST':
            form = RequestPayForm(request.POST)
            hold = form.save(commit=False)

            #process variables
            hold.user = request.user
            hold.competition = get_competition
            hold.amount = bal2
            hold.save()

            messages.add_message(request, messages.INFO, 'Application submitted, We will reach out to you')
            return redirect('take_pay')

        #send the form and data
        form = RequestPayForm(request.POST or None)
        return render(request, 'engine/apply_for_pay.html', {'form':form, 'balance':bal2})
    else:
        return redirect('set_managing')
    