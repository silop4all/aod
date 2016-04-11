import os
import subprocess
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone


class Command(BaseCommand):
    args = 'Arguments is not needed. Insert only the username of MySQL scheme owner when it required'
    help = 'Extract both the scheme and data from AoD MySQL database in format <backup_yyyy-mm-dd.sql.gz>'

    def handle(self, *args, **options):
        dir_path = "/db_backup"
        curr_date = str(datetime.date.today())

        try:
            print "=============== START (%s) ===============" % str(datetime.datetime.now())
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
                subprocess.call("chmod 644 "+dir_path, shell=True)
            else:
                pass

            #cmd = "mysqldump -u%s -p%s %s" % ("root", "", "pros4all")
            cmd = "mysqldump -u%s -p%s %s" % (settings.DATABASES['default']['USER'], settings.DATABASES['default']['PASSWORD'], settings.DATABASES['default']['NAME'])
            if settings.DEBUG:
                print cmd
            filename_sql = "backup_"+ curr_date +".sql"
            filename_gz = "backup_"+ curr_date +".sql.gz"

            # mysqldump -uroot -proot testdb > backup_yyyy-mm-dd.sql
            subprocess.call(cmd +" > "+ filename_sql , shell=True)
            if settings.DEBUG:
                print "Backup %s is completed." % filename_sql

            # gzip -c backup_yyyy-mm-dd.sql > backup_yyyy-mm-dd.sql.gz
            subprocess.call("gzip -c "+ filename_sql +" > "+filename_gz, shell=True)
            if settings.DEBUG:
                print "Gzip of %s is completed in %s." % (filename_sql, filename_gz)

            # mv backup_yyyy-mm-dd.gz /db_backup
            subprocess.call("mv "+ filename_gz + dir_path, shell=True)
            if settings.DEBUG:
                print "The %s is moved to %s" % (filename_gz, dir_path)

            # rm backup_yyyy-mm-dd.sql
            #subprocess.call("rm "+ filename_sql, shell=True)
            #print "Deletion of .sql is completed!"

            print "=============== END (%s) ===============" % str(datetime.datetime.now())		
        except:
            print "*** Database backup error! ***" 