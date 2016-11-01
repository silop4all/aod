# Prosperity4All project (Funded from EU)

## Instructions

### Step 1
As first step, execute the installation script (as the usual ubuntu user; not root) as follows:
```shell
    $ cd /opt
    $ sudo chmod 777 AoD_installation.sh
    $ ./AoD_installation.sh {git_repository_url} {git_repository_folder_name}
    # i.e: AoD_installation.sh https://github.com/silop4all/aod aod
```


### Step 2
Set the variables in the ```/opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/settings.py``` file:
- PRODUCTION
- SECRET_KEY
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD
- GOOGLE_ANALYTICS_PROPERTY_ID
- ANALYTICAL_INTERNAL_IPS
- GOOGLE_MAPS_KEY
- OPENAM_INTEGRATION
    + CLIENT_ID* (if OPENAM_INTEGRATION = True)
    + CLIENT_SECRET* (if OPENAM_INTEGRATION = True)
    + OAUTH_SERVER* (if OPENAM_INTEGRATION = True)
- SOCIAL_NETWORK_URL
- SOCIAL_NETWORK_WEB_SERVICES
- SOCIAL_NETWORK_WEB_SERVICES_AUTH
- CROWD_FUNDING


Set the variables in the ```/opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/development_settings.py``` file:
- DEVELOPER_EMAIL
- AOD_HOST
- DATABASES


Set the variables in the ```/opt/prosperity/AssistanceOnDemand/AssistanceOnDemand/production_settings.py``` file:
- DEVELOPER_EMAIL
- EVALUATOR_EMAIL
- AOD_HOST
- DATABASES


### STEP 3
Setup the AoD database (translations fields are generated) and then, populate it using a set of required data. 
```shell
    $ cd /opt
    $ sudo chmod 777 AoD_populated_db
    $ ./AoD_populated_db.sh
```


### STEP 4 
Restart apache web server.

```shell
    $ sudo service apache2 restart
```