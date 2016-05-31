# Prosperity4All project
## Assistance On Demand service Infrastructure (AoD)

### Hardware requirements
- __Operating System__: Linux (Ubuntu 14.04)
- __RAM__: 2 GB
- __CPU cores__: > 2
- __Disk space__: > 20 GB

### Software dependencies

- Relational Database Management system (MySQL or PostgreSQL)
- Apache web server
- Python 2.7

#### Create account

```bash
$ sudo groupadd aod
$ sudo useradd -g aod -s /bin/bash
```

#### Update Virtual Machine (VM)

```bash
$ sudo apt-get update
$ sudo apt-get dist-upgrade
```

#### Install MySQL server and create a database

```bash
$ sudo apt-get install mysql-server
$ sudo apt-get install python-mysqldb
$ sudo mysql_secure_installation   
$ sudo service mysql restart       
$ sudo service mysql status        
```

```sql
$ mysql –uroot -p
$ create database `pros4all`; // create db
$ create user 'aod'@'localhost' identified by 'aod';       
$ grant all privileges on `pros4all`.* to 'aod'@'localhost'; 
$ flush privileges;
$ quit
```

#### Install Apache web server

```bash
$ sudo apt-get install apache2
$ sudo apt-get install libapache2-mod-python
$ sudo apt-get install libapache2-mod-wsgi
$ sudo apt-get install rcconf
$ sudo apt-get install dialog
$ sudo apachectl status 
$ sudo service apache2 restart 
```

#### Install pillow

```bash
$ sudo apt-get build-dep python-imaging
$ sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
```

#### Install python packages
The python packages must be installed given that python with version 2.7 has already pre-installed in Ubuntu 14.04. The VM administrator needs to install the python pip package.

```bash
$ sudo apt-get install python-pip
```

Then, install the packages included in _requirements.txt_ using the command:
```bash
$ sudo pip install -r requirements.txt 
```

To check the version of the python as well as the installed python packages, the VM administrator can use:
```bash
$ sudo python –V
$ sudo pip freeze
```

#### Install and configurate the AoD project

Deploy the AoD project, let's suppose {AoD}, including its applications:
```bash
$ mkdir /opt/prosperity/
$ sudo mv /home/ubuntu/{AoD} /opt/prosperity/
$ chown –R aod:aod /opt/prosperity/
$ cd /opt/prosperity/{AoD}/{AoD}
```

Configurate the project database and email account for notifications:
```bash
$ sudo vim settings.py
...
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pros4all',
        'USER': 'aod',
        'PASSWORD': 'aod',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

...
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = {gmail_account}
EMAIL_HOST_PASSWORD = {gmail_account_password}
EMAIL_PORT = 587
EMAIL_USE_TLS = True
...
```

Update the _wsgi.py_ file as following:
```bash
$ vim wsgi.py

import sys
sys.path.append('/opt/prosperity/{AoD}')
sys.path.append('/opt/prosperity/{AoD}/{AoD}')
```

Populate tha database and enter the superuser credentials, if required:
```bash
$ sudo python manage.py syncdb
#sudo python manage.py migrate (only if the initial .sql file is provided) 
```

Collect static files:
```bash
$ sudo python manage.py collectstatic --noinput
```

Execute the command to check the success installation of AoD project:
```bash
$ cd /opt/prosperity/{AoD}/
$ sudo python manage.py runserver 0.0.0.0:8080
```

#### Configurate the Apache web server

As aforementioned, the Django runserver should be used only for testing or during the development phase. To solve it, the Apache web server must be configured as so AoD platform be accessible. In principle, disable the default configuration and create a new one.

```bash
$ sudo -i 
$ cd /etc/apache2/sites-available/
$ cp 000-default.conf aod.conf
$ a2dissite 000-default.conf
$ service apache2 restart

$ vim aod.conf
<VirtualHost *:80>
    ServerAdmin root@localhost.com
    ServerName 127.0.0.1
    WSGIScriptAlias / /opt/prosperity/{AoD}/{AoD}/wsgi.py

    <Directory /opt/prosperity/{AoD}/{AoD}>
        <Files wsgi.py>
            Order deny,allow
            Require all granted
        </Files>

        Options FollowSymLinks
        AllowOverride None
    </Directory>
</VirtualHost>

$ a2ensite aod.conf
$ service apache2 restart
```

