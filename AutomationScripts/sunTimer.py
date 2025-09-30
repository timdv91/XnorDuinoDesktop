import datetime
from datetime import timedelta

import requests
from dateutil import tz
from suntime import Sun, SunTimeException

class requestTest():
    def __init__(self, pURL):
        self.URL = pURL

    def get(self, pData, pPath=""):
        # GET request:
        r = requests.get(str(self.URL + "/" + pPath), data=(pData))
        return r.text

    def post(self, pData, pPath=""):
        # POST request:
        r = requests.post(str(self.URL + "/" + pPath), data=(pData))
        return r.text

class SunInfo():
    def __init__(self, lat, lon):
        # Set location & init sun library:
        self.SUN = Sun(lat, lon)
        self.BRUSSELS_TZ = tz.gettz('Europe/Brussels')

    def getSunSet(self, pDate, pOffsetHours=0):   # Note: Offsethours fixes bug in sunset library.
        sunset_utc = self.SUN.get_sunset_time(pDate)
        sunset_brussels = sunset_utc.astimezone(self.BRUSSELS_TZ)
        today_ss = sunset_brussels + datetime.timedelta(hours=pOffsetHours)
        return today_ss

    def getSunRise(self, pDate, pOffsetHours=0):
        sunrise_utc = self.SUN.get_sunrise_time(pDate)
        sunrise_brussels = sunrise_utc.astimezone(self.BRUSSELS_TZ)
        today_sr = sunrise_brussels + datetime.timedelta(hours=pOffsetHours)
        return today_sr


class LightControl():
    def __init__(self):
        self.REQ = requestTest("http://192.168.0.62:8081")

    def turnLightOn(self):
        print("Turning lights on!")
        #return

        # Light gardenshed terasse:
        r = self.REQ.get('["' + "0013A20041A885C0" + '","set_io_configuration()","IOLine.DIO10_PWM0", "IOMode.DIGITAL_OUT_HIGH"]', "W")
        r = self.REQ.get('["' + "0013A20041A885C0" + '","set_io_configuration()","IOLine.DIO11_PWM1", "IOMode.DIGITAL_OUT_HIGH"]', "W")

        # Light pump terasse
        r = self.REQ.get('["' + "0013A20041A885A4" + '","set_io_configuration()","IOLine.DIO10_PWM0", "IOMode.DIGITAL_OUT_HIGH"]', "W")
        r = self.REQ.get('["' + "0013A20041A885A4" + '","set_io_configuration()","IOLine.DIO11_PWM1", "IOMode.DIGITAL_OUT_HIGH"]', "W")

        # Light chickencoop
        r = self.REQ.get('["' + "0013A200409A0E7C" + '","set_io_configuration()","IOLine.DIO3_AD3", "IOMode.DIGITAL_OUT_HIGH"]', "W")
        #r = self.REQ.get('["' + "0013A200409A0E7C" + '","set_io_configuration()","IOLine.DIO3_AD2", "IOMode.DIGITAL_OUT_HIGH"]', "W")

    def turnLightOff(self):
        print("Turning lights off!")
        #return

        r = self.REQ.get('["' + "0013A20041A885C0" + '","set_io_configuration()","IOLine.DIO10_PWM0", "IOMode.DIGITAL_OUT_LOW"]', "W")
        r = self.REQ.get('["' + "0013A20041A885C0" + '","set_io_configuration()","IOLine.DIO11_PWM1", "IOMode.DIGITAL_OUT_LOW"]', "W")

        r = self.REQ.get('["' + "0013A20041A885A4" + '","set_io_configuration()","IOLine.DIO10_PWM0", "IOMode.DIGITAL_OUT_LOW"]', "W")
        r = self.REQ.get('["' + "0013A20041A885A4" + '","set_io_configuration()","IOLine.DIO11_PWM1", "IOMode.DIGITAL_OUT_LOW"]', "W")

        r = self.REQ.get('["' + "0013A200409A0E7C" + '","set_io_configuration()","IOLine.DIO3_AD3", "IOMode.DIGITAL_OUT_LOW"]', "W")
        #r = self.REQ.get('["' + "0013A200409A0E7C" + '","set_io_configuration()","IOLine.DIO3_AD2", "IOMode.DIGITAL_OUT_LOW"]', "W")


# ======================== Main ==========================

class Main():
    def __init__(self):
        wichelen_lat = 51.0060797
        wichelen_lon = 3.9742524
        SI = SunInfo(wichelen_lat,wichelen_lon)

        # Get sunset and sunrise timestamps:
        sunRiseTime = SI.getSunRise(datetime.datetime.now()) + datetime.timedelta(days=1)
        sunSetTime = SI.getSunSet(datetime.datetime.now()) + datetime.timedelta(days=1)

        print("Auto sunrise/sunset calculation: ")
        print("\t- Sunrise today: " + str(sunRiseTime) + " (epoch:" + str(sunRiseTime.timestamp()) + ")")
        print("\t- Sunset today: " + str(sunSetTime) + " (epoch:" + str(sunSetTime.timestamp()) + ")")

        # Perform light actions:
        print("Sunrise auto configuration: ")
        self.setLightsOnTimer(onTimeHour=6, pSummerStartMonth=3, pSummerEndMonth=10)
        self.setLightsOffSunRise(pSunRiseTime=sunRiseTime, pSummerStartMonth=3, pSummerEndMonth=10)            # Turn lights off when sun goes up

        print("Sunset auto configuration: ")
        self.setLightsOnSunSet(sunSetTime)      # Turn lights on when sun goes under
        self.setLightsOffTimer(00)              # Turn lights of at static time, for example midnight


    # Turn lights on in the morning:
    def setLightsOnTimer(self, onTimeHour, pTransmitTimeout=15, pSummerStartMonth=3, pSummerEndMonth=10):
        curMonth = datetime.datetime.now().month
        curHour = datetime.datetime.now().hour
        curMin = datetime.datetime.now().minute

        # Do not turn lights on in morning, during summer months:
        if curMonth > pSummerStartMonth and curMonth < pSummerEndMonth:  # Summer months only
            print("\t- Sunrise on-time disabled from april to september! Now: " + str(curMonth))
            return False

        print("\t- Turn lights on at " + str(onTimeHour) + ":00! Time now: " + str(curHour) + ":" + str(curMin))
        print("\t- Turn lights on-timeout at " + str(onTimeHour) + ":" + str(pTransmitTimeout))
        if curHour == onTimeHour and curMin < pTransmitTimeout:
            print("\t- Morning, turn lights on!")
            LC = LightControl()
            LC.turnLightOn()
            return True
        return False

    # Turn lights off, in the morning
    def setLightsOffSunRise(self, pSunRiseTime, pTurnOffDelay=15, pTransmitTimeout=15, pSummerStartMonth=3, pSummerEndMonth=10):
        # Do turn lights off during sunrise, in the winter months:
        epoch_time_now = datetime.datetime.now().timestamp()
        epoch_time_off = (pSunRiseTime + datetime.timedelta(minutes=pTurnOffDelay)).timestamp()
        epoch_time_out = (pSunRiseTime + datetime.timedelta(minutes=pTurnOffDelay + pTransmitTimeout)).timestamp()

        print("\t- Lights configured off-time: " + str(pSunRiseTime + datetime.timedelta(minutes=pTurnOffDelay)))
        print("\t- Transmit timeout off-time: " + str(pSunRiseTime + datetime.timedelta(minutes=pTurnOffDelay + pTransmitTimeout)))
        print("\t- Current time: " + str(datetime.datetime.fromtimestamp(epoch_time_now)))

        # Do not turn lights on in morning, during summer months:
        curMonth = datetime.datetime.now().month
        if curMonth > pSummerStartMonth and curMonth < pSummerEndMonth:   # Summer
            print("\t- Sunrise off-time disabled from april to september!")
            return False

        if epoch_time_now > epoch_time_off and epoch_time_now < epoch_time_out:
            print("Sunrise: Turn lights off!")
            LC = LightControl()
            LC.turnLightOff()
            return True
        return False



    # Turn lights on in the evening:
    def setLightsOnSunSet(self, pSunSetTime, pTurnOnDelay=15, pTransmitTimeout=15):
        epoch_time_now = datetime.datetime.now().timestamp()
        epoch_time_on = (pSunSetTime + datetime.timedelta(minutes=pTurnOnDelay)).timestamp()
        epoch_time_out = (pSunSetTime + datetime.timedelta(minutes=pTurnOnDelay + pTransmitTimeout)).timestamp()

        print("\t- Lights configured on-time: " + str(pSunSetTime + datetime.timedelta(minutes=pTurnOnDelay)))
        print("\t- Transmit timeout on-time: " + str(pSunSetTime + datetime.timedelta(minutes=pTurnOnDelay + pTransmitTimeout)))

        if epoch_time_now > epoch_time_on and epoch_time_now < epoch_time_out:
            print("\t- Sunset: Turn lights on!")
            LC = LightControl()
            LC.turnLightOn()
            return True
        return False

    # Turn lights off in the evening:
    def setLightsOffTimer(self, offTimeHour, pTransmitTimeout=15):
        curHour = datetime.datetime.now().hour
        curMin = datetime.datetime.now().minute
        print("\t- Turn lights off at " + str(offTimeHour) + ":00")
        print("\t- Turn lights off-timeout at " + str(offTimeHour) + ":" + str(pTransmitTimeout))
        if curHour == offTimeHour and curMin < pTransmitTimeout:
            print("\t- Sunset/Sunrise over: Turn lights off!")
            LC = LightControl()
            LC.turnLightOff()
            return True
        return False

Main()