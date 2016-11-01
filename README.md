![Prosperity4All logo](P4A.png "")

# Prosperity4All project (EU)

## Assistance On Demand service Infrastructure (AoD)

- [Minumum hardware requirements](#minumum-hardware-requirements)
- [Step 1: Install dependencies and AoD project](#step-1-install-dependencies-and-aod)
- [Step 2: AoD project settings](#step-2-aod-project-settings)
- [Step 3: Generate & populate the AoD database](#step-3-generate-populate-the-aod-database)
- [Step 4: Enable Apache configuration of AoD project](#step-4-enable-apache-configuration-of-aod-project)

---------

### Minumum hardware requirements

- `RAM`: 2 GB
- `CPU cores`: > 1
- `Disk space`: > 20 GB

The AoD project has been deployed and tested in both linux environment (`Ubuntu 14.04`) and `Windows 8/10`.


### Step 1: Install dependencies and AoD

- Relational Database Management system (MySQL or PostgreSQL)
- Apache web server
- Python 2.7

<!-- In case that you plan to deploy the AoD project in a __Ubuntu VM 14.04__, you can skip this step by executing the [installation script](""). Otherwise, follow the instructions below. -->


#### Resolve host
```shell
$ sudo sh -c "echo \"127.0.0.1\" $HOSTNAME >> /etc/hosts"
```

#### Create group & user
```bash
$ sudo groupadd aod
$ sudo useradd aod -g aod -s /bin/bash
```

#### Update VM
```bash
$ sudo apt-get update
$ sudo apt-get upgrade
```

#### Install basic packages
```shell
$ sudo apt-get install python-pip
$ sudo apt-get install git
$ sudo apt-get install unzip
$ sudo apt-get install vim
$ sudo apt-get install git
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


#### Install image packages
```bash
$ sudo apt-get build-dep python-imaging
$ sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
```


#### Install python packages
The python packages must be installed given that python with version 2.7 has already pre-installed in Ubuntu 14.04. The VM administrator needs to install the python pip package. To check the version of the python as well as the installed python packages, the VM administrator can use:
```bash
$ sudo python –V
$ sudo pip freeze
```


#### Install the AoD project
Deploy the AoD project including its applications:
```bash
$ sudo mkdir /opt/prosperity/
$ cd /home/ubuntu/
$ sudo git clone https://github.com/silop4all/aod.git
$ cd /opt/prosperity/
$ sudo cp /home/ubuntu/aod/* /opt/prosperity/
$ sudo chown aod:aod -R /opt/prosperity/
$ sudo find /opt/prosperity/AssistanceOnDemand/ -type d -exec chmod 755 {} \;
$ sudo find /opt/prosperity/AssistanceOnDemand/ -type f -exec chmod 644 {} \;
```

Then, install the packages included in ```requirements.txt``` using the command:
```bash
$ cd /opt/prosperity/AssistanceOnDemand/
$ sudo pip install -r requirements.txt 
```


#### Configurate the Apache web server
As aforementioned, the Django runserver should be used only for testing or during the development phase. To solve it, the Apache web server must be configured as so AoD platform be accessible. In principle, disable the default configuration and create a new one.

```shell
$ cd /etc/apache2/sites-available/
$ sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/aod.conf
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
```


```shell
$ cd /etc/apache2/
$ sudo vim http.conf
# If the debug mode is True:
WSGIScriptAlias / /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/wsgi.py
WSGIPythonPath /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/

# In production mode the media must be served from apache web server. Therefore, uncomment the next block if configuration.
# In case of path /prosperity/assistance-on-demand, see below:  
#
# Alias /prosperity/assistance-on-demand/static /opt/prosperity/ AssistanceOnDemand/static
# Alias /prosperity/assistance-on-demand/media /opt/prosperity/AssistanceOnDemand/media
# 
# <Directory /opt/prosperity/AssistanceOnDemand/static>
#     Require all granted
# </Directory>
# 
# <Directory /opt/prosperity/AssistanceOnDemand/media>
#     Require all granted
# </Directory>
#
# End of block

<Directory /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand>
    <Files wsgi.py>
        #Order deny,allow
        Require all granted
    </Files>
</Directory>
```

```shell
$ cd /etc/apache2/
$ sudo vim apache2.conf
# Include aod configuration at the end of file
Include /etc/apache2/http.conf
```




#### Step 2: AoD project settings

You need to modify the ```wsgi.py``` as follows:
```bash
$ cd /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/
$ vim wsgi.py
import os
# Uncomment the following lines
import sys
sys.path.append('/opt/prosperity/AssistanceOnDemand')
sys.path.append('/opt/prosperity/AssistanceOnDemand/AssistanceOnDemand')
...
```

The settings of the AoD project consists of the main file called ```settings.py``` and two others files, the ```development_settings.py``` and the ```production_settings.py```. Since you have set the operation mode fo the project (see ```PRODUCTION``` variable in the settings.py file), you need to set a few variables. All files are located to the path ```/opt/prosperity/AssistanceOnDemand/AssistanceOnDemand```.

The __variables__ that you must define in `settings.py` are the following:

##### PRODUCTION
Define if you plan to use the AoD project for production or development purpose. 

__Type__: `Boolean`

__Default__: `False`

> Note: If you set `True`, you need to modify the variable in the `production_settings.py`. Otherwise, you need to modify the variable in the `development_settings.py`.

---

##### SECRET_KEY
A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.

__Type__: `String`

> Note: This key is a hash (like salt). You can use the  [generator](http://www.miniwebtool.com/django-secret-key-generator/).

---

###### EMAIL_HOST_USER
Set the email account for AoD application. AoD uses to send notifications where it's needed.

__Type__: `String`

> Note: It is required to use only `gmail` accounts.

---

###### EMAIL_HOST_PASSWORD
Set the password of the above email account.

__Type__: `String`

---

###### GOOGLE_ANALYTICS_PROPERTY_ID
AoD project is integrated with `Google Analytics` to monitor the traffic analysis. 

__Type__: `String`

__Format__: `UA-XXXXXX-X`

> Note: To create one, follow the instructions [here](https://support.google.com/analytics/answer/1032385?hl=en).

---

###### ANALYTICAL_INTERNAL_IPS
A list or tuple of internal IP addresses. Tracking code will be commented out for visitors from any of these addresses. 

__Type__: `List of strings`

__Example__: `['192.168.1.1, '192.168.1.32]`

---

###### GOOGLE_MAPS_KEY
Set the key of the Google Maps JavaScript API.

__Type__: `String`

> Note: Follow the instruction [here](https://developers.google.com/maps/documentation/javascript/get-api-key) to get a key.

---

##### OPENAM_INTEGRATION
Integrate or not the AoD with the Identity & Access Management component (part of the Prosperity4All project) that is used as an authentication infrastructure. 

__Type__: `Boolean`

__Default__: `False`

> Note: It is required to declare the variables `CLIENT_ID`, `CLIENT_SECRET` and `OAUTH_SERVER` if you set it as `True`.

---

##### CLIENT_ID
Declare the AoD client id (application username in OAuth2 protocol) that the `Identity & Access Management` component provides on you after the registration of the current AoD instance on it. It is required if `OPENAM_INTEGRATION` is `True`.

__Type__: `String`

__Format__: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

> Note: Send me email me for more details.

---

##### CLIENT_SECRET
Declare the AoD client secret (application password in OAuth2 protocol) that the `Identity & Access Management` component provides on you after the registration of the current AoD instance on it. It is required if `OPENAM_INTEGRATION` is `True`.

__Type__: `String`

__Format__: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

> Note: Send me email me for more details.

---

##### OAUTH_SERVER
Define the IP and PORT in which the `Identity & Access Management` component is running. It is required if `OPENAM_INTEGRATION` is `True`.

__Type__: `String`

__Format__: `IP:PORT`

> Note: Send me email me for more details.

---

##### SOCIAL_NETWORK_URL
Define the base URL of the Social Network component in case of integration among AoD and Social Network.

__Type__: `URL`

__Format__: `http://IP:PORT/PATH/#/home`

> Note: By default, the integration among AoD project and Social network is disabled.

---

##### SOCIAL_NETWORK_WEB_SERVICES
Define the API details of the Social Network component in case of integration among AoD and Social Network.

__Type__: `Dictionary`

__Format__: 
```python
{
    "url": "IP:PORT",
    "base": "http://IP:PORT",
    "services": {
        "insert": "/api/jsonws/aodsocial-portlet.aodsocial/on-register-aod-service/service-id/",
        "delete": "/api/jsonws/aodsocial-portlet.aodsocial/on-delete-aod-service/service-id/"
    },
    "users": {
        "insert": "/api/jsonws/aodsocial-portlet.aodsocial/login-with-register"
    },
    "sessions":{
        "logout": "/api/jsonws/aodsocial-portlet.aodsocial/propagate-logout/aod-user-id/"
    }
}
```

> Note: By default, the integration among AoD project and Social network is disabled. Send me email me for more details.

--- 

##### SOCIAL_NETWORK_WEB_SERVICES_AUTH
Define the authentication key that is used to invoke the Social Network API (in case of integration among AoD and Social Network).

__Type__: `String`

> Note: By default, the integration among AoD project and Social network is disabled. Send me email me for more details.

---

##### CROWD_FUNDING
Define the Crowd funding API details in case of integration among AoD and Crowd funding.

__Type__: `Dictionary`

__Format__: 
```shell
{
    "base": "http://IP:PORT",
    "projects": {
        "insert": "/proposal/new"
    }
}
```

> Note: By default, the integration among AoD project and Crowd funding platform is disabled. Send me email me for more details.

---


The __variables__ that you must define both in `development_settings.py` and `production_settings.py` are the following:

##### DEVELOPER_EMAIL
Define the email of the AoD admininstrator.  

__Type__: `String`

> Note: Aod informs AoD administrator via emails when an internal server error occurs.

---

##### AOD_HOST
Define the details of the VM in which AoD has been deployed such as the public IP, the used protocol (http or https), the public port in which apache server is running as well as the public PATH. The accepted values to the AOD_HOST['PATH'] variable is an empty string or a string that starts
 with `/` character and ends without `/` i.e.: `/prosperity/assistance-on-demand`.

__Type__: `Dictionary`

__Format__: 
```shell
{
    'PROTOCOL': "Enum (http||https)",
    'IP': "String", 
    'PORT': 'Number',
    'PATH': 'String'
}
```

__Default__: 
```shell
{
    'PROTOCOL': "http",
    'IP': "127.0.0.1", 
    'PORT': 80,
    'PATH': ''
}
```

> Note: AoD project has been tested over HTTP protocol.

---

##### DATABASES
Define the database settings such as the engine, the name of the database, the user credentials, its host and port as well as the used charset.

__Type__: `Dictionary`

__Default__: 
```shell
{
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aod',
        'USER': 'aod',
        'PASSWORD': 'aod',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8',
            'use_unicode': True, 
        },
    }
}
```

> Note: 

---


##### EVALUATOR_EMAIL*
In case of `production_settings.py`, the EVALUATOR_EMAIL variable must be defined. For simplicity, the DEVELOPER_EMAIL value can be the same with the EVALUATOR_EMAIL value.

__Type__: `String`

---


#### Step 3: Generate & populate the AoD database
Populate tha database and enter the superuser credentials following the commands.

```bash
$ cd /opt/prosperity/AssistanceOnDemand/
$ sudo python manage.py makemigrations
$ sudo python manage.py migrate
$ sudo python manage.py update_translation_fields
$ sudo python manage.py makemigrations
$ sudo python manage.py migrate
$ sudo python manage.py collectstatic --noinput
$ sudo chown aod:aod -R /opt/prosperity/AssistanceOnDemand/
$ sudo mysql -uaod -paod aod < /opt/prosperity/AssistanceOnDemand/sql/aod_data.sql
```

Execute the command to detect if the installation of AoD project has been performed successfully or not:
```bash
$ cd /opt/prosperity/AssistanceOnDemand/
$ sudo python manage.py runserver 0.0.0.0:8080
```

> You can check the correct installation of AoD using the command: 
> - curl -vvv http://localhost:8080/en/ from another terminal or via the browser (Chrome, Firefox)


#### Step 4: Enable Apache configuration of AoD project

```shell
$ sudo a2ensite aod.conf
$ sudo apt-get install libapache2-mod-wsgi
$ sudo a2enmod wsgi
$ sudo service apache2 restart
```


## Install PhpMyAdmin (optional)

Use the following commands to install the PhpMyAdmin (served by Apache web server). 

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

