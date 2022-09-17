def choice(request, pk, compid):
    #get competition Id
    get_comp = Competition.objects.get(id=compid)

    if get_comp.active == True:
        #extract price
        cost_of_one_vote = int(get_comp.price_per_vote)

        #get contestant and code
        get_contestant = Contestant.objects.get(id=pk)
        con_code = get_contestant.contestant_code


        #recieve form
        if request.method == 'POST':
            form = PaymentForm(request.POST)

            if form.is_valid():
                #convert number of votes to Int
                number = int(form.cleaned_data['number_of_votes'])
                email = str(form.cleaned_data['email'])

                # create the ref 
                global reference
                reference = secrets.token_urlsafe(17)

                # calculate cost
                amt = cost_of_one_vote * number * 100

                #save form data
                pause = form.save(commit=False)

                pause.contestant_code = con_code
                pause.verified = False
                pause.ref = reference
                pause.amount = amt
                pause.number_of_votes = number
                pause.email = email

                pause.save()

                # initialize transaction Url
                url = "https://api.paystack.co/transaction/initialize"

                #define payload parameters
                payload = json.dumps({
                "email": email,
                "amount": amt,
                "reference": reference,
                "callback_url": "http://127.0.0.1:8000/verifypayment/",      
                })

                #define header paramters
                headers = {
                    'Authorization': 'Bearer sk_test_f9a07560f35fb80005c478eaeb633e4867c7ca90',
                    'Content-Type': 'application/json',
                }

                #initialize or open connection
                response = requests.request("POST", url, headers=headers, data=payload)

                #convert response to json 
                package = json.loads(response.text)

                #extract redirection link
                link = package["data"]["authorization_url"]

                #redirect to payment 
                return redirect(link)

        form = PaymentForm()
        return render(request, 'main/choice.html', {'contestant': get_contestant, 'form': form, 'compid': get_comp})
        
    else:
        return HttpResponse('This competition is not available')












def verifypayment(request):
 
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    zuve = Payment.objects.get(ref=reference)

    payload={}
    files={}
    headers = {'Authorization': 'Bearer sk_test_f9a07560f35fb80005c478eaeb633e4867c7ca90'}

    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    package = json.loads(response.text)
    message = package['data']['status']

    if message == "success":
        zuve.verified = True

        #this is to get the number of votes
        vote_count = zuve.number_of_votes

        #get the contestant code
        contestant_iden = zuve.contestant_code

        #inititate a number of votes Update
        initiate_update = Contestant.objects.get(contestant_code=contestant_iden)

        #effect update Here
        initiate_update.number_of_votes += vote_count

        #save the effect
        initiate_update.save()
        
        #verify
        zuve.save(update_fields=['verified'])
        
        return render(request, 'main/portal.html', {'package': package})
    else:
        return render(request, 'main/failed_pay.html', {'package': package})

