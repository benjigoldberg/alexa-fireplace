# Introduction
Alexa Fireplace is a project to control a fireplace via Alexa Skills Kit (ASK). The code in this repository
provides the lambda function for interacting with ASK as well as a server capable of providing OAuth2 and
controlling a fireplace flame and blower fan via a GPIO two-channel relay. The Server and GPIO controls were
built on a Raspberry Pi 3 on Raspbian 8. I have not tested this on other boards or Operating Systems.

Once you have this up and running in your home, you can say "Hey Alexa, turn on the fireplace" and your 
fireplace will turn on. Likewise, you can say "Hey Alexa, turn off the fireplace" and Alexa will turn 
off your fireplace.

# Getting Started

Before beginning, you'll want to make sure you have a couple of prerequisites:

1. A domain name with an SSL certificate, or the ability to obtain one via Let's Encrypt (see below)
2. A Raspberry Pi Running Raspbian 8
3. Male to Female Jumper cables
4. [A two-channel Relay Controller](https://www.amazon.com/gp/product/B00TGUH99U/ref=oh_aui_detailpage_o05_s00?ie=UTF8&psc=1)
5. Electrical components and tools to wire your fireplace
  * [Wire nuts](https://www.amazon.com/Hilitchi-Electrical-Connection-Connector-Assortment/dp/B01CXOCLHU/ref=sr_1_1?s=automotive&ie=UTF8&qid=1486844418&sr=1-1&keywords=wire+nuts) or [soldering iron](https://www.amazon.com/Weller-SP80NUS-Heavy-Soldering-Black/dp/B00B3SG796/ref=sr_1_1?s=hi&ie=UTF8&qid=1486844517&sr=1-1&keywords=weller+soldering+iron)
    * Personally, I think soldering is overkill. Just buy a box of wirenuts that will last the rest of your 
       life and be useful all over your home.
  * [Wire stripping, cutting and crimping tool](https://www.amazon.com/heavy-duty-electrical-wire-crimping/dp/B01I8GUVKG/ref=sr_1_1?s=automotive&ie=UTF8&qid=1486844315&sr=1-1&keywords=wire+stripping+and+crimping+tool)

## Create your Application on Amazon Developer Services
1. [Create an account or login](https://developer.amazon.com/)

## Configure your Raspberry Pi Running Raspbian 8
1. 

## Configure your Lambda Function in AWS

# Configuring your System
1. Install Dependencies
  a. `$ sudo apt-get install nginx uwsgi python3-dev python3-virtualenv python3-pip`
2. Install Python Packages
  a. `$ pip install -r requirements.txt`
3. Link the project to `/var/www/`
  a. `$ sudo ln -s `pwd` /var/www/alexa-fireplace`
4. Configure nginx
  a. ```$ sudo ln -s `pwd`/alexa-fireplace-nginx.conf /etc/nginx/sites-enabled/alexa-fireplace-nginx.conf```
  b. `$ sudo systemctl enable nginx`
5. Configure uwsgi
  a. ```$ sudo ln -s `pwd`/emperor.ini /etc/uwsgi/emperor.ini```
  b. ```$ sudo ln -s `pwd`/alexa-fireplace-uwsgi.ini /etc/uwsgi/vassals/alexa-fireplace-uwsgi.ini```
  c. `$ sudo systemctl enable uwsgi`
6. Add www-data to group gpio
  a. sudo adduser www-data gpio

# Setting up your Free SSL Certificate
### Note that before doing this you should have your server running via NGINX and Uwsgi.
1. Go to [Let's Encrypt (and donate if you want!)](https://letsencrypt.org/getting-started)
2. Follow the instructions there to determine how to configure the cert for your system.
3. For Raspbian 8 Jessie
  b. Add the line: `deb http://ftp.debian.org/debian jessie-backports main` to `/etc/apt/sources.list`
  c. $ sudo apt-get update
4. Install CertBot
  a. $ sudo apt-get install certbot -t jessie-backports
5. Create the Certificate
  a. $ certbot certonly --webroot -w /var/www/alexa-fireplace -d <yourdomain>
  b. CertBot will need permissions to write to this directory. The Nginx config
     is already configured to server the CertBot http://{{ HOSTNAME }}/.well-known directory
     for verification by CertBot.
