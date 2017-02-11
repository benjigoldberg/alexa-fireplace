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
1. Go to Let's Encrypt (and donate if you want!)
  a. https://letsencrypt.org/getting-started
2. Follow the instructions there to determine how to configure the cert for your system.
3. For Raspbian 8 Jessie
  a. $ vim /etc/apt/sources.list
  b. Add the line: deb http://ftp.debian.org/debian jessie-backports main
  c. $ sudo apt-get update
4. Install CertBot
  a. $ sudo apt-get install certbot -t jessie-backports
5. Create the Certificate
  a. $ certbot certonly --webroot -w /var/www/alexa-fireplace -d <yourdomain>
