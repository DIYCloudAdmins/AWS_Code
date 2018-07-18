from datetime import datetime
import pytz


class evaluateSchedule:

    def is_dst(self):
        # Determine whether or not Daylight Savings Time (DST) is currently in effect

        x = datetime(datetime.now().year, 1, 1, 0, 0, 0, tzinfo=pytz.timezone('US/Eastern')) # Jan 1 of this year
        y = datetime.now(pytz.timezone('US/Eastern'))

        # if DST is in effect, their offsets will be different
        return not (y.utcoffset() == x.utcoffset())

    def doesTimeMatch(self,suppliedHour):
        if self.getCurrentTimestamp("US/Eastern").strftime("%H") == suppliedHour:
            return True
        if self.getCurrentTimestamp("US/Eastern").strftime("%H") == suppliedHour:
            return False

    def adjustedDay(self,day):
        if self.getCurrentTimestamp("US/Eastern").strftime("%w") == str(day):
            return True
        if self.getCurrentTimestamp("US/Eastern").strftime("%w") == str(day):
            return False

    def runToday(self,rundays):
        runToday = False

        days = rundays.split(",")
        for day in days:
            if day == "mon":
                if self.adjustedDay(1) == True:
                    runToday = True
            if day == "tue":
                if self.adjustedDay(2) == True:
                    runToday = True
            if day == "wed":
                if self.adjustedDay(3) == True:
                    runToday = True
            if day == "thur":
                if self.adjustedDay(4) == True:
                    runToday = True
            if day == "fri":
                if self.adjustedDay(5) == True:
                    runToday = True
            if day == "sat":
                if self.adjustedDay(6) == True:
                    runToday = True
            if day == "sun":
                if self.adjustedDay(0) == True:
                    runToday = True
            
        return runToday
    
    def getCurrentTimestamp(self, timezone):

        utct = datetime.utcnow()
        tz = pytz.timezone(timezone)

        utct = utct.replace(tzinfo=pytz.UTC)
        return utct.astimezone(tz)

    def __init__(self, commandLineArgs):
        for items in commandLineArgs:
            curItem=items.split(":")
            if curItem[0]=="shutdown":
                if curItem[1] == "yes":
                    self.shutdown = True
                if curItem[1] != "yes":
                    self.shutdown = False
            if curItem[0]=="shutdownHour":
                self.shutdownHourMatch = self.doesTimeMatch(curItem[1])
            if curItem[0]=="shutdownDays":
               self.shutdownToday = self.runToday(curItem[1])
            if curItem[0]=="startup":
                if curItem[1] == "yes":
                    self.startup = True
                if curItem[1] != "yes":
                    self.startup = False
            if curItem[0]=="startupHour":
                self.startupHourMatch = self.doesTimeMatch(curItem[1])
            if curItem[0]=="startupDays":
                self.startupToday = self.runToday(curItem[1])
