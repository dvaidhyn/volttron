#
# THIS SOFTWARE IS PROVIDED BY Alliance for Sustainable Energy, LLC ''AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL  Alliance for Sustainable Energy, LLC
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
#
# This software is an extension of VOLTTRON. The FreeBSD license of the
# VOLTTRON distribution applies to this software.
#
# Author(s): Deepthi Vaidhynathan, National Renewable Energy Laboratory
# Version:
# Date:
#
# National Renewable Energy Laboratory is a national laboratory of the
# U.S. Department of Energy, Office of Energy Efficiency and Renewable Energy,
# operated by the Alliance for Sustainable Energy, LLC
# under Contract No. DE-AC36-08GO28308.
#



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

    def get_heat_pgm(self,day=''):
        ''' get heat program for a week or a specific day
            day = {'mon','tue','wed','thu','fri','sat','sun'}

            for a specific day, say thursday:
            t.get_heat_pgm('thu')

            for a week:
            t.get_heat_pgm()

        '''
        if day =='':
            url = self.urladdress+"/program/heat"
        else:
            url = self.urladdress+"/program/heat/"+str(day)
        try:
            mode =  (urllib2.urlopen(url))
            parsed = json.loads(mode.read().decode("utf-8"))
            print json.dumps(parsed)
            return json.dumps(parsed)

        except Exception as parsed:
            return parsed


    def get_cool_pgm(self,day=''):
        ''' get cool program for a week or a specific day
            day = {'mon','tue','wed','thu','fri','sat','sun'}

            for a specific day, say thursday:
            t.get_cool_pgm('thu')

            for a week:
            t.get_cool_pgm()

        '''
        if day =='':
            url = self.urladdress+"/program/cool"
        else:
            url = self.urladdress+"/program/cool/"+str(day)
        try:
            mode =  (urllib2.urlopen(url))
            parsed = json.loads(mode.read().decode("utf-8"))
            print json.dumps(parsed)
            return json.dumps(parsed)

        except Exception as parsed:
            return parsed

    def set_cool_pgm(self,schedule,day=''):
        ''' set cool program for a week or a specific day
            day = {'mon','tue','wed','thu','fri','sat','sun'}

            for a spefic day, say 'thu'
            t.set_cool_pgm('{"3":[360, 80, 480, 80, 1080, 80, 1320 , 80]}','thu')

            t.set_cool_pgm('{\
                        "1": [360, 70, 480, 70, 1080, 70, 1320, 70],\
                        "0": [360, 66, 480, 58, 1080, 66, 1320, 58], \
                        "3": [360, 66, 480, 58, 1080, 66, 1320, 58],\
                        "2": [360, 66, 480, 58, 1080, 66, 1320, 58],\
                        "5": [360, 66, 480, 58, 1080, 66, 1320, 58],\
                        "4": [360, 66, 480, 58, 1080, 66, 1320, 58],\
                        "6": [360, 66, 480, 58, 1080, 66, 1320, 58]
                 }')
        '''
        if day =='':
            url = self.urladdress+"/program/cool"
        else:
            url = self.urladdress+"/program/cool/"+str(day)
        try:
            mode =  (urllib2.urlopen(url,schedule))
            parsed = json.loads(mode.read().decode("utf-8"))
            print json.dumps(parsed)
            return json.dumps(parsed)

        except Exception as parsed:
            return parsed


    def set_heat_pgm(self,schedule,day=''):
        ''' set heat program for a week or a specific day
            day = {'mon','tue','wed','thu','fri','sat','sun'}

            for a spefic day, say 'thu'
            t.set_heat_pgm('{"3":[360, 80, 480, 80, 1080, 80, 1320 , 80]}','thu')

            for a week
            t.set_heat_pgm('{\
                        "1": [360, 70, 480, 70, 1080, 70, 1320, 70],\
                        "0": [360, 66, 480, 58, 1080, 66, 1320, 58], \
                        "3": [360, 66, 480, 58, 1080, 66, 1320, 58],\
                        "2": [360, 66, 480, 58, 1080, 66, 1320, 58],\
                        "5": [360, 66, 480, 58, 1080, 66, 1320, 58],\
                        "4": [360, 66, 480, 58, 1080, 66, 1320, 58],\
                        "6": [360, 66, 480, 58, 1080, 66, 1320, 58]
                 }')
        '''
        if day =='':
            url = self.urladdress+"/program/heat"
        else:
            url = self.urladdress+"/program/heat/"+str(day)
        try:
            mode =  (urllib2.urlopen(url,schedule))
            parsed = json.loads(mode.read().decode("utf-8"))
            print json.dumps(parsed)
            return json.dumps(parsed)

        except Exception as parsed:
            return parsed
