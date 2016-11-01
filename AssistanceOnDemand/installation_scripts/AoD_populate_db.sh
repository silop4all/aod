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
AOD_PROJECT_PATH="/opt/prosperity"

#=======================================
#  POPULATE AOD DATABASE
#=======================================
echo ""
echo "Do you want to populate the AoD project database? [y/n] "
read AOD_POPULATE_DB
if [ $AOD_POPULATE_DB == "y" ]; then
    cd $AOD_PROJECT_PATH/AssistanceOnDemand/
    sudo python manage.py makemigrations
    sudo python manage.py migrate
    sudo python manage.py update_translation_fields
    sudo python manage.py makemigrations
    sudo python manage.py migrate
    sudo python manage.py collectstatic --noinput
    sudo chown $APP_USER:$APP_GROUP -R $AOD_PROJECT_PATH/AssistanceOnDemand/
    echo "Populate the AoD project"
    mysql -u$DB_USER -p$DB_USER_PWD $DB_SCHEMA_NAME < $AOD_PROJECT_PATH/AssistanceOnDemand/sql/aod_data.sql
else 
    echo "[WARNING] Database population has been skipped!!!"
    echo "[WARNING] You have to populate the database schema manually..."
    echo ""
fi

echo ""  