'''

Thermostat Interface:

API to set and get values for the thermostat over WiFi

FakeThermostat - creates a fake thermostat object
ThermostatInterface - creates a real thermostat obect based on address

-Used with RadioThermostatAgent

'''

import json
import sys
import time
import urllib2


class FakeThermostat(object):
    ''' Fake Thermostat: Class that implements the functions used to get
        and set values in a thermostat
    '''
    def __init__(self, url=None):
        self.query = {
            "temp":70.50,
            "tmode":0,
            "fmode":0,
            "override":0,
            "hold":0,
            "t_cool":85.00,
            "t_heat":70.00,
            "time":
                {
                    "day": time.localtime().tm_wday,
                    "hour": time.localtime().tm_hour,
                    "minute": time.localtime().tm_min
                }
        }
        self.success = {"success": 0}
        print "Initialized a Fake Thermostat object"

    def t_cool(self,data):
        ''' Sets cooling setpoint'''
        self.query["t_cool"] = float(data)
        self.query["time"] = {
            "day": time.localtime().tm_wday,
            "hour": time.localtime().tm_hour,
            "minute": time.localtime().tm_min
        }
        return self.success

    def t_heat(self,data):
        ''' Sets heating setpoint'''
        self.query["t_heat"] = float(data)
        self.query["time"] = {
            "day": time.localtime().tm_wday,
            "hour": time.localtime().tm_hour,
            "minute": time.localtime().tm_min
        }
        return self.success

    def tstat(self,):
        ''' Returns current paraments'''

        self.query["time"] = {
            "day": time.localtime().tm_wday,
            "hour": time.localtime().tm_hour,
            "minute": time.localtime().tm_min
        }
        return json.dumps(self.query)
        # return json.loads(query.read().decode("utf-8"))

    def mode(self,data):
        ''' Sets operating mode'''
        self.query["t_mode"] = int(data)
        self.query["time"] = {
            "day": time.localtime().tm_wday,
            "hour": time.localtime().tm_hour,
            "minute": time.localtime().tm_min
        }
        return self.success

def Thermostat_API(url):
    ''' Chooses a Fake device or real device based on url'''
    if url == "Fake":
        return FakeThermostat()
    else :
        return ThermostatInterface(url)


class ThermostatInterface(object):
    '''Base interface to get and set values on the thermostat
    '''
    def __init__(self, url):
        self.urladdress = url

        print "Initialized a REAL Thermostat object"

    def t_cool(self,data):
        ''' Sets cooling setpoint'''
        msg = {"tmode":2,"t_cool":data}
        value = json.dumps(msg)
        try:
            mode =  (urllib2.urlopen(self.urladdress,value))
            parsed = json.loads(mode.read().decode("utf-8"))
            return json.dumps(parsed)
        except Exception as parsed:
            return parsed

    def t_heat(self,data):
        ''' Sets heating setpoint'''
        msg = {"tmode":1,"t_heat":data}
        value = json.dumps(msg)
        try:
            mode =  (urllib2.urlopen(self.urladdress,value))
            parsed = json.loads(mode.read().decode("utf-8"))
            return json.dumps(parsed)
        except Exception as parsed:
            return parsed

    def over(self,data):
        ''' Sets override controls'''
        msg = {"override":data}
        value = json.dumps(msg)
        try:
            mode =  (urllib2.urlopen(self.urladdress,value))
            parsed = json.loads(mode.read().decode("utf-8"))
            return json.dumps(parsed)
        except Exception as parsed:
            return parsed

    def hold(self,data):
        ''' Sets  hold controls'''
        msg = {"hold":data}
        value = json.dumps(msg)
        try:
            mode =  (urllib2.urlopen(self.urladdress,value))
            parsed = json.loads(mode.read().decode("utf-8"))
            return json.dumps(parsed)
        except Exception as parsed:
            return parsed

    def model(self):
        ''' Returns device model'''
        address= self.address+"/model"
        try:
            mode =  (urllib2.urlopen(address))
            parsed = json.loads(mode.read().decode("utf-8"))
            return json.dumps(parsed)
        except Exception as parsed:
            return parsed


    def tstat(self):
        ''' Returns current deive paramenters'''
        try:
            mode =  (urllib2.urlopen(self.urladdress))
            parsed = json.loads(mode.read().decode("utf-8"))
            print json.dumps(parsed)
            return json.dumps(parsed)

        except Exception as parsed:
            return parsed

    def fmode_on(self):
        ''' Turns on the fan : DEMO specific  '''
        msg = {"fmode":2}
        value = json.dumps(msg)
        try:
            mode =  (urllib2.urlopen(self.urladdress,value))
            parsed = json.loads(mode.read().decode("utf-8"))
            print json.dumps(parsed)
            return json.dumps(parsed)
        except Exception as parsed:
            return parsed

    def mode(self,data):
        ''' Sets  operating mode'''
        msg = {"tmode":data}
        value = json.dumps(msg)
        try:
            mode =  (urllib2.urlopen(self.urladdress,value))
            parsed = json.loads(mode.read().decode("utf-8"))
            print json.dumps(parsed)
            return json.dumps(parsed)
        except Exception as parsed:
            return parsed
