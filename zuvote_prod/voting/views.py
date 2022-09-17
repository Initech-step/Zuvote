from django.shortcuts import render, redirect
from django.http import HttpResponse
from engine.models import ExtraUserData, Competitions, Contestants
from django.shortcuts import get_object_or_404
from .forms import VotingForm
from .models import Payments
import secrets
import requests
import json
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(redirect_field_name='login_zuvote')
def voting_preview(request):
    #first step get user
    #get currently managed competition
    #check competition active state
    get_user = ExtraUserData.objects.get(user=request.user)
    get_currently_managing = get_user.currently_managing

    if get_currently_managing != None:
        check_active_a = Competitions.objects.get(Competition_slug=get_currently_managing)
        check_active_b = check_active_a.active

        if check_active_b == True:
            your_competition_url = check_active_a.unique_competition_code
            return render(request, 'voting/get_competition_url.html', {'pack': your_competition_url})
        else:
            return redirect('set_active_state')

    else:      
        return redirect('set_managing')


def voting_page(request, pubcode):
    get_competition = get_object_or_404(Competitions, unique_competition_code=pubcode)
    #check active state

    if get_competition.active == True:
        get_contestants = Contestants.objects.filter(competition_involved=get_competition)
        return render(request, 'voting/event_page.html', {'contestants': get_contestants, 'competition': get_competition})
    else:
        return HttpResponse('This competition is not currently available')



def vote(request, pubcode, pk):
    #get contestant id 
    get_contestant = get_object_or_404(Contestants, id=pk)
    #get competition
    get_competition = get_contestant.competition_involved
    #get the price of one vote
    price_of_one_vote = int(get_competition.price_per_vote)

    if request.method == 'POST':
        #get the form
        form = VotingForm(request.POST)
        if form.is_valid():

            #get form values
            numberofvotes = int(form.cleaned_data['number_of_votes'])
            email = str(form.cleaned_data['email'])

            #generate a reference for the payment
            global reference
            reference = secrets.token_urlsafe(18)

            #calculate total cost of voting
            amount_to_charge = price_of_one_vote * numberofvotes * 100

            # arrange and save form data
            pause = form.save(commit=False)

            pause.contestant = get_contestant
            pause.competition = get_competition
            pause.amount = amount_to_charge
            pause.number_of_votes = numberofvotes
            pause.ref = reference
            pause.email = email
            pause.verified = False

            pause.save()

            #begin processing payment
            url = "https://api.paystack.co/transaction/initialize"
            #define payload parameters
            payload = json.dumps({
                "email": email,
                "amount": amount_to_charge,
                "reference": reference,
                "callback_url": "http://127.0.0.1:8000/voting/verifypayment/", 
                })

            #define authorization headers
            headers = {
                    'Authorization': 'Bearer sk_test_f9a07560f35fb80005c478eaeb633e4867c7ca90',
                    'Content-Type': 'application/json',
            }

            #make a request
            response = requests.request("POST", url, headers=headers, data=payload)

            #get response data
            package = json.loads(response.text)

            #extract redirection link
            link = package["data"]["authorization_url"]

            #redirect to payment 
            return redirect(link)

    if get_competition.active == True:
        form = VotingForm(request.POST or None)
        return render(request, 'voting/contestant.html', {'form': form, 'contestant':get_contestant, 'get_competition': get_competition})
    else:
        return HttpResponse('Competition is not open for votes')



#verify payment for votes
def verifypayment(request):

    #paystack verification link
    url = f"https://api.paystack.co/transaction/verify/{reference}"

    #make a db query 
    zuve = Payments.objects.get(ref=reference)
    numberofvotes = zuve.number_of_votes

    #define data variables
    payload={}
    files={}
    headers = {'Authorization': 'Bearer sk_test_f9a07560f35fb80005c478eaeb633e4867c7ca90'}

    #make verification request
    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    #get response 
    package = json.loads(response.text)
    message = package['data']['status']
    refe = package['data']['reference']
    date = package['data']['paid_at']

    if message == "success":
        zuve.verified = True

        #this is to get the number of votes
        vote_count = zuve.number_of_votes
        competion = zuve.competition

        #get the contestant
        contestant_iden = zuve.contestant.id
        contestant_name = zuve.contestant.contestant_name
        #inititate a number of votes Update
        initiate_update = Contestants.objects.get(id=contestant_iden)
        #effect update Here
        initiate_update.number_of_votes += vote_count
        #save the effect
        initiate_update.save()
        
        #verify
        zuve.save(update_fields=['verified'])

        return render(request, 'voting/verified_pay.html', {'date':date,
                                                             'competition_name':competion,
                                                              'contestant':contestant_name,
                                                              'message': message,
                                                              'ref': refe,
                                                              'numberofvotes': vote_count
                                                              })
    else:
        return render(request, 'voting/unverified_pay.html', {'date':date,
                                                             'competition_name':competion,
                                                              'contestant':contestant_name,
                                                              'message': message,
                                                              'ref': refe,
                                                              'numberofvotes': vote_count
                                                              })

