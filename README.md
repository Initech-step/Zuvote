# PROJECT NAME: Zuvote
Project type: Prototype i.e it can only run on local environment and not production.

## Reason/Purpose why this project was developed
Beauty pageantries are common among Nigerian youngsters. Sometimes votes are made by payment either cash or transfer. Organizers pass through a lot to receive, compute and keep track of votes.Organizers have to sort through the stress of knowing which vote is meant for who.
This software takes such burden off their hands.

Developed by: Ini-abasi Sebastian Etim

### How does this work ?

I will like to approach this based on a step-by-step procedure.
1. A pageantry organizer registers and signs into the platform.
2. The organizer can then create a competition.
3. The organizer can register contestants for the competition.
5. After adding contestants and being satisfied, the competition can be set to active to permit voting.
7. the user can apply for withdrawal of vote proceeds.

### Technical Structure
This is a monolithic application

#### The frontend stack
- HTML -CSS -Bootstrap 
#### The backend stack
- Python -DJango -Paystack-api

# How to set up this project.

- Clone the repository
- Install all requirements using 'pip install -r requirements.txt'
- navigate into the 'zuvote_prod' folder
- run 'python manage.py makemigrations'
- run 'python manage.py migrate'
- You can view the app at the localhost it opens up

NOTE: This application uses Bootstrap CDN so you need to be connected to the internet in order to see a presentable gui 