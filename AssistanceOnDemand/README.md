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
$ sudo useradd aod -g aod -s /bin/bash
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
$ sudo apt-get install libmysqlclient-dev      
$ sudo mysql_secure_installation   
$ sudo service mysql restart       
$ sudo service mysql status  
```

```bash
$ mysql –uroot -p
```
```sql
create database `pros4all`; -- create db
create user 'aod'@'localhost' identified by 'aod';       
grant all privileges on `pros4all`.* to 'aod'@'localhost'; 
flush privileges;
quit
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

To check the version of the python as well as the installed python packages, the VM administrator can use:
```bash
$ sudo python –V
$ sudo pip freeze
```

#### Install and configurate the AoD project

Deploy the AoD project, let's suppose _AssistanceOnDemand_, including its applications:
```bash
$ cd /opt/
$ sudo mkdir /opt/prosperity/
$ sudo apt-get install git
$ sudo apt-get install unzip
$ sudo git clone https://github.com/silop4all/aod.git
# You could also download the code in a zipped format and extract it using the unzip command
$ cd /opt/prosperity/
$ sudo mv aod/* .
$ sudo rm -rf aod/
$ sudo chown aod:aod -R /opt/prosperity/
$ sudo find AssistanceOnDemand/ -type d -exec chmod 755 {} \;
$ sudo find AssistanceOnDemand/ -type f -exec chmod 644 {} \;
```

Then, install the packages included in _requirements.txt_ using the command:
```bash
$ cd /opt/prosperity/AssistanceOnDemand/
$ sudo pip install -r requirements.txt 
```

Configurate the project _settings_ (database and email account for notifications) and the _wsgi.py_ file as following :
```bash
$ cd /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand

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

$ vim wsgi.py
import os
import sys
sys.path.append('/opt/prosperity/AssistanceOnDemand')
sys.path.append('/opt/prosperity/AssistanceOnDemand/AssistanceOnDemand')
...
```

Populate tha database and enter the superuser credentials, if required:
```bash
#$ sudo python manage.py syncdb(only if .sql is not provided)
$ mysql -uaod -paod pros4all < pros4all.sql
$ sudo python manage.py migrate
```

Collect static files:
```bash
$ sudo python manage.py collectstatic --noinput
```

Execute the command to check the success installation of AoD project:
```bash
$ cd /opt/prosperity/AssistanceOnDemand/
$ sudo python manage.py runserver 0.0.0.0:8080
```

> You can check the correct installation of AoD using the command: 
> - curl -vvv http://localhost:8080 from another terminal

#### Configurate the Apache web server

As aforementioned, the Django runserver should be used only for testing or during the development phase. To solve it, the Apache web server must be configured as so AoD platform be accessible. In principle, disable the default configuration and create a new one.

```bash
$ cd /etc/apache2/sites-available/
$ sudo cp 000-default.conf aod.conf
$ sudo a2dissite 000-default.conf
$ sudo service apache2 restart

$ sudo vim aod.conf
<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        
        ServerName www.example.com
        ServerAdmin root@localhost.com
        DocumentRoot /opt/prosperity/AssistanceOnDemand

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
</VirtualHost>

$ cd /etc/apache2/
$ sudo vim http.conf
WSGIScriptAlias / /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/wsgi.py
WSGIPythonPath /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/

<Directory /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand>
    <Files wsgi.py>
        Order deny,allow
        Require all granted
    </Files>
</Directory>

$ sudo vim apache2.conf
# Include aod configuration at the end of file
Include /etc/apache2/http.conf

$ sudo a2ensite aod.conf
$ sudo apt-get install libapache2-mod-wsgi
$ sudo a2enmod wsgi
$ sudo service apache2 restart
```

