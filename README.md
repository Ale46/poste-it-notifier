#Poste.it Notifier


Simple tool that send you an **email** when the status of your package, that should be delivered by [Poste Italiane] (http://poste.it), change.

##Install

###Run on Heroku
First clone the repository
```
git clone https://github.com/Ale46/poste-it-notifier.git
```
Create your heroku app and then add postmark addon
```
heroku addons:add postmark
```
Configure postmark (rember to define sender signature)
```
heroku addons:open postmark
```
Set heroku variables
```
heroku config:set POSTMARK_API_TOKEN=API
heroku config:set TRACKING_CODE=RS0000000 #package tracking code
heroku config:set RECV_EMAIL=joesmith@mail.com #receiver email
heroku config:set SENDER_EMAIL=notifier@mail.com
heroku config:set SLEEP_TIME=60 #sleep time (in minutes) before each check
```
Deploy on heroku and scale your worker
```
heroku ps:scale worker=1
```

###Run locally

First signup at [postmark](http://postmark.it), than clone the repository
```
git clone https://github.com/Ale46/poste-it-notifier.git
```
Install dependencies
```
(sudo) pip install -r requirements.txt
```
Define env variables (or use foreman with .env file, as you prefer)
```
export POSTMARK_API_TOKEN=API
export TRACKING_CODE=RS0000000 #package tracking code
export RECV_EMAIL=joesmith@mail.com #receiver email
export SENDER_EMAIL=notifier@mail.com
export SLEEP_TIME=60 #sleep time (in minutes) before each check
```
Run
```
python worker.py
```
