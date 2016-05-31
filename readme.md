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

#### Install AoD

Deploy the AoD project including its applications:
```bash
$ mkdir /opt/prosperity/
$ sudo mv /home/ubuntu/{AoD} /opt/prosperity/
$ chown –R aod:aod /opt/prosperity/
$ cd /opt/prosperity/{AoD}/{AoD}
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

Update the wsgi.py file as following:
```bash
import sys
sys.path.append('/opt/prosperity/{AoD}')
sys.path.append('/opt/ prosperity /{AoD}/{AoD}')
```




