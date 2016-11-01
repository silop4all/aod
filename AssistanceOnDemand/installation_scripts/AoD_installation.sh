#!/bin/bash

#=======================================
#   AssistanceOnDemand Infrastructure
#
#           SingularLogic SA
#   
#              Ubuntu 14.04
#=======================================

echo "#=======================================#"
echo "#       Prosperity4All EU Project       #"
echo "#   AssistanceOnDemand Infrastructure   #"
echo "#   Installation file for Ubuntu 14.04  #"
echo "#=======================================#"
echo " "


#=======================================
#   DECLARE VARIABLES
#=======================================
APP_USER="aod"
APP_GROUP="aod"
CREATE_DB_PATH="/tmp/create_db.sql"
DB_USER="aod"
DB_USER_PWD="aod"
DB_SCHEMA_NAME="aod"
#GIT_REPOSITORY="pass as argument the HTTP url"
GIT_REPOSITORY=$1
#GIT_AOD_DIR="name of parent direcory i.e.: aod"
GIT_AOD_DIR=$2
AOD_PROJECT_PATH="/opt/prosperity"
AOD_TEMP_CONF_PATH="/tmp/aod.conf"
APACHE_PATH="/etc/apache2"
AOD_CONF_PATH="/etc/apache2/sites-available/aod.conf"
AOD_TEMP_HTTP_CONF="/tmp/http.conf"
AOD_HTTP_CONF="/etc/apache2/http.conf"

#=======================================
#   PRINT SYSTEM INFO
#=======================================
echo " "
echo "[INFO] VM info..."
cat /etc/os-release
echo " "
echo "[INFO] VM Architecture..."
arch
echo " "

#=======================================
#   RESOLVE HOST
#=======================================
echo "[URGENT] Do you execute this bash script first time? [y/n]"
read FIRST_EXECUTE 
echo ""
if [ $FIRST_EXECUTE == "y" ];then
    echo "[INFO] Resolve host..."
    echo ""
    sudo sh -c "echo \"127.0.0.1\" $HOSTNAME >> /etc/hosts"
fi

#=======================================
#   CREATE GROUP & USER
#=======================================
echo " "
sudo groupadd $APP_USER
sudo useradd $APP_USER -g $APP_GROUP -s /bin/bash
echo " "

#=======================================
#   DO UPDATES
#=======================================
echo " "
sudo apt-get update
sudo apt-get upgrade
echo " "

#=======================================
#   INSTALL BASIC PACKAGES
#=======================================
sudo apt-get install python-pip
sudo apt-get install git
sudo apt-get install unzip
sudo apt-get install vim
sudo apt-get install git

#=======================================
#   INSTALL MySQL SERVER & DATABASE
#=======================================
echo ""
echo "Proceed to installation of MySQL server? [y/n] "
read MYSQL_INSTALL
if [ $MYSQL_INSTALL == "y" ]; then
    sudo apt-get install mysql-server
    sudo apt-get install python-mysqldb
    sudo apt-get install libmysqlclient-dev      
    sudo mysql_secure_installation   
    sudo service mysql restart       
    sudo service mysql status 
    
    sudo rm $CREATE_DB_PATH
    sudo touch $CREATE_DB_PATH
    sudo chmod 777 $CREATE_DB_PATH
    sudo chown $APP_USER:$APP_GROUP $CREATE_DB_PATH
    echo "DROP database if exists "$DB_SCHEMA_NAME";" >> $CREATE_DB_PATH
    echo "CREATE database aod DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_unicode_ci; " >> $CREATE_DB_PATH
    
    if [ $FIRST_EXECUTE == "n" ]; then
        #echo "DELETE FROM mysql.user WHERE user.user='"$DB_USER"' AND user.host='localhost';" >> $CREATE_DB_PATH
        echo "DROP USER '"$DB_USER"'@localhost;" >> $CREATE_DB_PATH
    fi

    echo "flush privileges;" >> $CREATE_DB_PATH
    echo "CREATE user '"$DB_USER"'@'localhost' identified by '"$DB_USER_PWD"';" >> $CREATE_DB_PATH
    echo "grant all privileges on "$DB_SCHEMA_NAME".* to '"$DB_USER"'@'localhost' IDENTIFIED BY '"$DB_USER_PWD"';" >> $CREATE_DB_PATH
    echo "flush privileges;" >> $CREATE_DB_PATH

    echo "Enter current password for (MySQL) root, again:"
    read DB_ROOT_PWD
    sudo mysql -uroot -p$DB_ROOT_PWD < $CREATE_DB_PATH    
    echo ""
    echo "--------------------------------------------------"
    echo "[INFO] Database scheme 'aod' has created"
    echo "[INFO] Dedicated user has grant with privileges..."
    echo "[INFO] user -> aod"
    echo "[INFO] password -> aod"
    echo "[INFO] Use cmd: mysql -u aod -p"
    echo "--------------------------------------------------"
    echo ""
    echo ""
else 
    echo "[WARNING] Installation was terminated!!!"
    echo ""
    exit 0
fi
echo ""

#=======================================
#   INSTALL APACHE SERVER
#=======================================
echo ""
echo "Proceed to installation of Apache server? [y/n] "
read APACHE_INSTALL
if [ $APACHE_INSTALL == "y" ]; then
    sudo apt-get install apache2
    sudo apt-get install libapache2-mod-python
    sudo apt-get install libapache2-mod-wsgi
    sudo apt-get install rcconf
    sudo apt-get install dialog
    sudo apachectl status 
    sudo service apache2 restart 
    echo ""
    echo ""
else 
    echo "[WARNING] Installation was terminated!!!"
    echo ""
    exit 0
fi
echo ""

#=======================================
#   APACHE CONF FOR AOD PROJECT
#=======================================
echo ""
echo "Proceed to configure the Apache server for the AoD project? [y/n] "
read APACHE_CONF
if [ $APACHE_CONF == "y" ]; then
    # aod.conf
    echo ""
    echo "Create a temporary file for VirtualHost in "$AOD_TEMP_CONF_PATH
    sudo rm $AOD_TEMP_CONF_PATH
    sudo touch $AOD_TEMP_CONF_PATH
    sudo chmod 777 $AOD_TEMP_CONF_PATH
    sudo chown $APP_USER:$APP_GROUP $AOD_TEMP_CONF_PATH
    echo "<VirtualHost *:80>" >> $AOD_TEMP_CONF_PATH
    echo "  ServerName www.example.com" >> $AOD_TEMP_CONF_PATH
    echo "  ServerAdmin root@localhost.com" >> $AOD_TEMP_CONF_PATH
    echo "  DocumentRoot "$AOD_PROJECT_PATH"/AssistanceOnDemand" >> $AOD_TEMP_CONF_PATH
    echo "  ErrorLog \${APACHE_LOG_DIR}/error.log" >> $AOD_TEMP_CONF_PATH
    echo "  CustomLog \${APACHE_LOG_DIR}/access.log combined" >> $AOD_TEMP_CONF_PATH
    echo "</VirtualHost>" >> $AOD_TEMP_CONF_PATH

    sudo cp /etc/apache2/sites-available/000-default.conf $AOD_CONF_PATH
    sudo a2dissite 000-default.conf
    sudo cp $AOD_TEMP_CONF_PATH $AOD_CONF_PATH
    echo ""
    echo "[INFO] "$AOD_CONF_PATH" file has created..."
    echo ""
    sudo service apache2 restart

    # http.conf
    sudo rm $AOD_TEMP_HTTP_CONF
    sudo touch $AOD_TEMP_HTTP_CONF
    sudo chmod 777 $AOD_TEMP_HTTP_CONF
    sudo chown $APP_USER:$APP_GROUP $AOD_TEMP_HTTP_CONF
    echo "WSGIScriptAlias / /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/wsgi.py" >> $AOD_TEMP_HTTP_CONF    
    echo "WSGIPythonPath /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/" >> $AOD_TEMP_HTTP_CONF 
    echo "">> $AOD_TEMP_HTTP_CONF 
    echo "# Used only for production" >> $AOD_TEMP_HTTP_CONF 
    echo "# " >> $AOD_TEMP_HTTP_CONF 
    echo "# Alias /prosperity/assistance-on-demand/static /opt/prosperity/AssistanceOnDemand/static" >> $AOD_TEMP_HTTP_CONF   
    echo "# Alias /prosperity/assistance-on-demand/media /opt/prosperity/AssistanceOnDemand/media" >> $AOD_TEMP_HTTP_CONF   
    echo "# " >> $AOD_TEMP_HTTP_CONF   
    echo "# <Directory /opt/prosperity/AssistanceOnDemand/static>" >> $AOD_TEMP_HTTP_CONF   
    echo "#     Require all granted" >> $AOD_TEMP_HTTP_CONF   
    echo "# </Directory>" >> $AOD_TEMP_HTTP_CONF   
    echo "# " >> $AOD_TEMP_HTTP_CONF   
    echo "# <Directory /opt/prosperity/AssistanceOnDemand/media>" >> $AOD_TEMP_HTTP_CONF   
    echo "#     Require all granted" >> $AOD_TEMP_HTTP_CONF   
    echo "# </Directory>" >> $AOD_TEMP_HTTP_CONF   
    echo "#" >> $AOD_TEMP_HTTP_CONF    
    echo "" >> $AOD_TEMP_HTTP_CONF    
    echo "<Directory /opt/prosperity/AssistanceOnDemand/AssistanceOnDemand>" >> $AOD_TEMP_HTTP_CONF    
    echo "    <Files wsgi.py>" >> $AOD_TEMP_HTTP_CONF    
    echo "        #Order deny,allow" >> $AOD_TEMP_HTTP_CONF    
    echo "        Require all granted" >> $AOD_TEMP_HTTP_CONF    
    echo "    </Files>" >> $AOD_TEMP_HTTP_CONF    
    echo "</Directory>" >> $AOD_TEMP_HTTP_CONF   

    sudo cp $AOD_TEMP_HTTP_CONF $AOD_HTTP_CONF
    echo ""
    echo "[INFO] "$AOD_HTTP_CONF" file has created..."
    echo ""

    if [ $FIRST_EXECUTE == "y" ]; then
        sudo sh -c "echo \"Include \"$AOD_HTTP_CONF >> $APACHE_PATH/apache2.conf"
    fi

    sudo a2ensite aod.conf    
    sudo apt-get install libapache2-mod-wsgi
    sudo a2enmod wsgi
    sudo service apache2 restart

else 
    echo "[WARNING] Apache configuration has skipped!!!"
    echo ""
fi
echo ""


#=======================================
#   INSTALL PILLOW
#=======================================
echo ""
echo "Proceed to installation of image packages? [y/n] "
read IMG_PACKAGE_INSTALL
if [ $IMG_PACKAGE_INSTALL == "y" ]; then
    sudo apt-get build-dep python-imaging
    sudo apt-get install libjpeg8 libjpeg62-dev libfreetype6 libfreetype6-dev
else 
    printf "[WARNING] Installation was terminated!!!"
    echo ""
    exit 0
fi
echo ""

#=======================================
#   INSTALL PYTHON
#=======================================
echo ""
sudo apt-get install python-pip
#sudo python –V
sudo pip freeze



#=======================================
#   INSTALL AOD PROJECT
#=======================================
echo ""
echo "Proceed to AoD project installation? [y/n] "
read AOD_INSTALL
if [ $AOD_INSTALL == "y" ]; then
    sudo rm -rf $AOD_PROJECT_PATH
    sudo rm -rf $HOME/$GIT_AOD_DIR
    sudo mkdir $AOD_PROJECT_PATH
    cd $HOME
    sudo git clone $GIT_REPOSITORY
    echo ""
    echo "[INFO] AoD project has been downloaded in path "$HOME
    cd $AOD_PROJECT_PATH
    echo ""
    echo "[INFO] Copy AoD project to path "$AOD_PROJECT_PATH
    sudo cp -R $HOME/$GIT_AOD_DIR/* $AOD_PROJECT_PATH
    echo ""
    echo "[INFO] Change user:group of AoD project files"
    sudo chown $APP_USER:$APP_GROUP -R $AOD_PROJECT_PATH
    echo ""
    echo "[INFO] Change AoD project files permissions dirs->755, files->644"
    sudo find $AOD_PROJECT_PATH/AssistanceOnDemand/ -type d -exec chmod 755 {} \;
    sudo find $AOD_PROJECT_PATH/AssistanceOnDemand/ -type f -exec chmod 644 {} \;
    cd $AOD_PROJECT_PATH/AssistanceOnDemand/
    echo ""
    echo "[INFO] Install AoD project dependencies..."
    sudo pip install -r requirements.txt 
    echo "[INFO] AoD project dependencies have been installed"
    sudo pip freeze
else 
    echo "[WARNING] Installation has skipped!!!"
    echo "[WARNING] Follow the provided instructions to download and install the AoD project..."
    echo ""
    exit 0
fi
  
