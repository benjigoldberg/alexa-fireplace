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

