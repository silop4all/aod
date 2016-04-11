# Prosperity 4 All project

## Assistance On Demand service Infrastructure

### Hardware requirements
    __Operating System__: Linux (Ubuntu 14.04)
    __RAM__: 2 GB
    __CPU cores__: > 2
    __Disk space__: > 20 GB

### Software dependencies

    Relational Database Management system (MySQL or PostgreSQL)
    Apache web server
    Python 2.7

#### Create Account
    # sudo groupadd aod
    # sudo useradd -g aod -s /bin/bash

#### Update Virtual Machine (VM)
    # sudo apt-get update
    # sudo apt-get dist-upgrade

#### Install MySQL server and create a database
    # sudo apt-get install mysql-server
    # sudo apt-get install python-mysqldb
    # sudo mysql_secure_installation   
    # sudo service mysql restart       
    # sudo service mysql status        

    # mysql –uroot -p
    $ create database pros4all; // create db
    $ create user 'aod'@'localhost' identified by 'aod';       
    $ grant all privileges on pros4all.* to 'aod'@'localhost'; 
    $ flush privileges;
    $ quit

#### Install Apache web server
    $ sudo apt-get install apache2
    $ sudo apt-get install libapache2-mod-python
    $ sudo apt-get install libapache2-mod-wsgi
    $ sudo apt-get install rcconf
    $ sudo apt-get install dialog
    $ sudo apachectl status 
    $ sudo service apache2 restart 

#### Install pillow
    # sudo apt-get build-dep python-imaging
    # sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev

##### Install python packages
The python packages must be installed given that python with version 2.7 has already pre-installed in Ubuntu 14.04. The VM administrator needs to install the python pip package.

    # sudo apt-get install python-pip

Then, install the packages included in _requirements.txt_ using the command:

    # sudo pip install {package} 

To check the version of the python as well as the installed python packages, the VM administrator can use:

    # sudo python –V
    # sudo pip freeze

