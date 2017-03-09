# Installation in windows 8/10

You need to install the following:
- xampp (incl. apache web server, MySQL server, phpmyadmin)
- python 2.7.x (it is recommended to install it in virtual environment)
- IDE (Visual studio 2013/2015 community edition is suggested)

## Step 1: Install dependencies and AoD

Create the Assistance on Demand database and its relevant MySQL user from the phpmyadmin (toad, MySQL workbench), or directly from cmd:
```sql
create database `aod` DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_unicode_ci; 
create user 'aod'@'localhost' identified by 'aod';       
grant all privileges on `aod`.* to 'aod'@'localhost'; 
flush privileges;
quit
```

You need to create an empty Django project (using any IDE you have selected) with name `AssistanceOnDemand` in virtualenv, python 2.7.x; a path will be built such as `\path-to-project\AssistanceOnDemand\`. 

Since you have already downloaded or cloned the source code from the github repository,  overwrite the common contents of the `\path-to-project\AssistanceOnDemand\AssistanceOnDemand\` with the contents of the `\path-to-aod-code\aod-master\aod-master\AssistanceOnDemand\`, clean the solution and build it again.

Afterwards, you need to install the python packages/dependencies; check the file requirements.txt. You can perform it from the IDE (Visual studio) or using the `pip install -r ../../requirements.txt` ( in `\path-to-project\AssistanceOnDemand\AssistanceOnDemand\<virtual-environment-name>\Scripts` path since you have activated the vitual environment). The installation of some python packages will be failed (i.e. the MySQL-python==1.2.5); in this case you need to download and install the corresponding wheel package (remind python version 2.7.x).


#### Step 2: AoD project settings

This step is the same for ubuntu and windows deployment apart from the `wsgi.py` modification. It is not required to modify this file.


#### Step 3: Generate & populate the AoD database

```bash
# the path-to-env-scripts/ will be something like venv/Scripts/
$ cd /path-to-project/AssistanceOnDemand/AssistanceOnDemand/path-to-env-scripts/
$ python ../../manage.py makemigrations
$ python ../../manage.py migrate
$ python ../../manage.py update_translation_fields
$ python /../../manage.py makemigrations
$ python ../../manage.py migrate
$ python ../../manage.py collectstatic --noinput
```

Afterwards, fill in the AoD database with the required data. Import the sql file located in path `/path-to-project/AssistanceOnDemand/AssistanceOnDemand/sql/aod_data.sql`.

Execute the command and  detect if the installation of AoD project has been performed successfully or not by tyeping in your browser the url `http://localhost:8080/en/`:
```bash
$ cd /path-to-project/AssistanceOnDemand/AssistanceOnDemand/path-to-env-scripts/
$ python ../../manage.py runserver 0.0.0.0:8080
```


# Usage

Type the URL `http://<host_ip>:<host_port>/<language_code>/` from your browser to access the AoD platform (i.e. http://127.0.0.1:80/en/). 

Type the URL `http://<host_ip>:<host_port>/<language_code>/docs` from your browser to access the web services that AoD provides.

Type the URL `http://<host_ip>:<host_port>/<language_code>/admin/` from your browser to access the management panel of the AoD platform.