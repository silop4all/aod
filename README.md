# Prosperity4All project

[Prosperity4All logo](https://github.com/silop4all/aod/tree/master/P4A.png "")

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
create database `aod` DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_unicode_ci; 
create user 'aod'@'localhost' identified by 'aod';       
grant all privileges on `aod`.* to 'aod'@'localhost'; 
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

The settings of the AoD could be found in the files settings.py, production_settings.py and development_settings.py. In the settings.py file, you can set if you are in deveploment or production mode by settings the "PRODUCTION" variable. This file include the corresponding setting in any case.

```bash
$ cd /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand
$ sudo vim settings.py
...
PRODUCTION = False #(True)
...
```

In both development_settings.py and production_settings.py, you can define the settings related to the:
- debug state, 
- developer email account, 
- aod details and prefix URL, 
- allowed hosts, 
- database configuration,
- configuration for the IAM/OPENAM authentication services,
- multilingual features and configuration (rosetta),
- media files URL,
- static files URL,
- installed applications,
- swagger configuration,
- email account for notification purposes,
- rest framework configuration,
- grappelli admin template configuration,
- google analytics configuration,
- cors origin configuration


```bash
$ cd /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand
$ sudo vim production_settings.py # development_settings
...
# Set debug state 
DEBUG = False
TEMPLATE_DEBUG = DEBUG
...

# Set developer email account
DEVELOPER_EMAIL = {email_account}
...

# Set aod details and prefix URL
AOD_HOST = {
    'PROTOCOL': "http",
    'IP': "127.0.0.1", 
    'PORT': 80,
    'PATH': '/your_prefix_path' # valid format is "/mypath" or ""
}
...

# Set database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aod',
        'USER': 'aod',
        'PASSWORD': 'aod',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
...

# Set the configuration for IAM/OPENAM authentication services
LOGIN_URL = '/callback/openam'
OPENAM_INTEGRATION = True
CLIENT_ID = {iam_client_id}
CLIENT_SECRET = {iam_client_secret}
OAUTH_SERVER = {ip:port}
REDIRECT_URL = AOD_HOST['PROTOCOL'] + "://" + AOD_HOST['IP'] + AOD_HOST['PATH'] + LOGIN_URL
...

# Set the mulitlingual and localization settings
TIME_ZONE = 'Europe/Athens'
LANGUAGES = (
    ('el', _('Greek')),
    ('en', _('English')),
    ('it', _('Italian')),
    ('es', _('Spanish')),
    ('fr', _('French')),
    ('de', _('German')),
    ...
)
LANGUAGE_CODE = 'en'
# cookie name for language
LANGUAGE_COOKIE_NAME = "aod_language"
SITE_ID = 1
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True
# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True
...

# Set the email account for notification purposes
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = {gmail_account}
EMAIL_HOST_PASSWORD = {gmail_account_password}
EMAIL_PORT = 587
EMAIL_USE_TLS = True
...

# Set the google analytics details
GOOGLE_ANALYTICS_PROPERTY_ID = {google_analytics_id}
ANALYTICAL_INTERNAL_IPS = {your_IPs_as_a_list}
ANALYTICAL_AUTO_IDENTIFY = False
GOOGLE_ANALYTICS_DISPLAY_ADVERTISING = True
...

```


Also, you must modify the wsi.py as follows:
```bash
$ vim wsgi.py
import os
import sys
sys.path.append('/opt/prosperity/AssistanceOnDemand')
sys.path.append('/opt/prosperity/AssistanceOnDemand/AssistanceOnDemand')
...
```

Populate tha database and enter the superuser credentials, if required:
```bash
$ cd /opt/prosperity/AssistanceOnDemand/
$ sudo python manage.py makemigrations
$ sudo python manage.py migrate
$ sudo python manage.py update_translation_fields
$ sudo python manage.py makemigrations
$ sudo python manage.py migrate
$ sudo python manage.py collectstatic --noinput
$ sudo chown aod:aod -R /opt/prosperity/AssistanceOnDemand/
$ sudo mysql -uaod -paod aod < sql/aod_data.sql
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
# If the debug mode is True:
WSGIScriptAlias / /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/wsgi.py
WSGIPythonPath /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/

<Directory /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand>
    <Files wsgi.py>
        #Order deny,allow
        Require all granted
    </Files>
</Directory>

# Else, in production mode the media must be served from apache web server
# In case of path /prosperity/assistance-on-demand, see below:
WSGIScriptAlias / /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/wsgi.py
WSGIPythonPath /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/

Alias /prosperity/assistance-on-demand/static /opt/prosperity/AssistanceOnDemand/static
Alias /prosperity/assistance-on-demand/media /opt/prosperity/AssistanceOnDemand/media

<Directory /opt/prosperity/AssistanceOnDemand/static>
    Require all granted
</Directory>

<Directory /opt/prosperity/AssistanceOnDemand/media>
    Require all granted
</Directory>

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



### Install PhpMyAdmin (optional)

```bash
$ sudo apt-get install phpmyadmin
$ sudo service apache2 restart
$ sudo php5enmod mcrypt
$ sudo ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf
$ sudo a2enconf phpmyadmin.conf
$ sudo service apache2 restart
```

```bash
$ sudo vim /etc/phpmyadmin/apache.conf
# phpMyAdmin default Apache configuration

# add prefix i.e. /prosperity/assistance-on-demand
Alias /prosperity/assistance-on-demand/phpmyadmin /usr/share/phpmyadmin

<Directory /usr/share/phpmyadmin>
        Options FollowSymLinks
        DirectoryIndex index.php

        <IfModule mod_php5.c>
                AddType application/x-httpd-php .php

                php_flag magic_quotes_gpc Off
                php_flag track_vars On
                php_flag register_globals Off
                php_admin_flag allow_url_fopen Off
                php_value include_path .
                php_admin_value upload_tmp_dir /var/lib/phpmyadmin/tmp
                php_admin_value open_basedir /usr/share/phpmyadmin/:/etc/phpmyadmin/:/var/lib/phpmyadmin/:/usr/share/php/php-gettext/:/usr/share/javascript/
        </IfModule>

</Directory>

# Authorize for setup
<Directory /usr/share/phpmyadmin/setup>
    <IfModule mod_authn_file.c>
    AuthType Basic
    AuthName "phpMyAdmin Setup"
    AuthUserFile /etc/phpmyadmin/htpasswd.setup
    </IfModule>
    Require valid-user
</Directory>

# Disallow web access to directories that don't need it
<Directory /usr/share/phpmyadmin/libraries>
    Order Deny,Allow
    Deny from All
</Directory>
<Directory /usr/share/phpmyadmin/setup/lib>
    Order Deny,Allow
    Deny from All
</Directory>
```

```bash
$ sudo service apache2 reload
```


In phppmyadmin UI must have access only authenticated users; to achieve it, the folder must be password protected as follows:

```bash
$ cd /usr/share/phpmyadmin/
$ sudo vim .htaccess
    AuthType Basic
    AuthName "Password Protected Area"
    AuthUserFile /etc/phpmyadmin/.htpasswd
    Require valid-user


$ sudo apt-get install apache2-utils
$ cd /etc/phpmyadmin/
$ sudo htpasswd -c /etc/phpmyadmin/.htpasswd {username}
$ (enter password)
$ sudo vim /etc/phpmyadmin/apache.conf

Alias /prosperity/assistance-on-demand/phpmyadmin /usr/share/phpmyadmin

<Directory /usr/share/phpmyadmin>
    AllowOverride AuthConfig
    Options FollowSymLinks
    DirectoryIndex index.php
    ....
</Directory>

$ sudo service apache2 restart
```

