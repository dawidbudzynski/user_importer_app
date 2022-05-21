# User importer app

## General info

A web application made using Python 3, Django 4.  
<br/>Application allows to import users from Subscriber and SubscriberSMS models.

## Main functions

* importing users from Subscriber and SubscriberSMS models
* generating csv file with conflicts

## Technologies

* Python 3.8
* Django 4.0

## Setup
To run this project:
1. Create virtualenv
```
python3 -m venv venv
```
2. Activate virtualenv
```
source venv/bin/activate
```
3. Install required libraries using pip
```
pip install -r requirements.txt
```
4. Make database migrations:
```
python manage.py migrate
```
5. Import test data from fixtures
```
python manage.py loaddata user_data.json && \
python manage.py loaddata client_data.json && \
python manage.py loaddata subscriber_data.json && \
python manage.py loaddata subscribersms_data.json
```
