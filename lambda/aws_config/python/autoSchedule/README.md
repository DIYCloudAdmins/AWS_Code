#AutoSchedule

Auto schedule stops and starts EC2 instances based on a schedule defined in the "autoSchedule" tag applied to the resources where the stop and start are desired.

The autoSchedule key value must be in the form of
 "shutdown:yes;shutdownHour:09;shutdownDays:mon,tue,wed,thur,fri,sat,sun;startup:yes;startupHour:23;startupDays:mon,tue,wed,thur,fri,sat"

* shutdown:yes/no
* shutdownHour:24 hour based (two digit format) hour the instance will be stopped (03 = 03:00am, 15 = 03:00pm)
* shutdownDays:days that shutdown should take place (mon=Monday,tue=Tuesday,wed=Wednesday,thur=Thursday,fri=Friday,sat=Saturday,sun=Sunday).  It is Ok to leave any days out that a shutdown is not desired.
* startup:yes/no
*startupHour: 24 hour based (two digit format) hour the instance will be started (03 = 03:00am, 15 = 03:00pm)
startupDays: days that startup should take place (mon=Monday,tue=Tuesday,wed=Wednesday,thur=Thursday,fri=Friday,sat=Saturday,sun=Sunday).  It is Ok to leave any days out that a shutdown is not desired.

###To deploy
this scrip relies on the pytz package. install the package to the same folder you are devloping the scrip in: "pip install -t "c:\directory\structure\where\script\exists" pytz
 
 * rename AutoScheduleInstances.py to lambda_function.py*
 * zip the following into a zip file: lambda_function.py, AS_Helper.py, pytz (directory), and upload to a lambda function.
 * create a cloudwatch cron job to run the function every hour
 * add the tag autoSchedule with the appropriate value to any instance you would like to schedule
