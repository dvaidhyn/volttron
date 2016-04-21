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
#            Harry Sorensen, National Renewable Energy Laboratory
# Version: 0.1
# Date: April 20, 2016
#
# National Renewable Energy Laboratory is a national laboratory of the
# U.S. Department of Energy, Office of Energy Efficiency and Renewable Energy,
# operated by the Alliance for Sustainable Energy, LLC
# under Contract No. DE-AC36-08GO28308.
#



import unittest
import json
import time
import thermostat_api
from thermostat_api import ThermostatInterface, FakeThermostat

class CEA2045TestCase(unittest.TestCase):
    def test_tcool(self):
        '''Test  t_cool() interface'''
        obj = thermostat_api.Thermostat_API("Fake")
        self.assertEqual(obj.t_cool(79.0),{'success': 0})

    def test_theat(self):
        '''Test  t_heat() interface'''
        obj = thermostat_api.Thermostat_API("Fake")
        self.assertEqual(obj.t_cool(79.0),{'success': 0})

    def test_mode(self):
       '''Test  mode() interface'''
       obj = thermostat_api.Thermostat_API("Fake")
       self.assertEqual(obj.t_cool(0),{'success': 0})

    def test_tstat(self):
        '''Test the tstat() interface'''
        obj = thermostat_api.Thermostat_API("Fake")
        expected_dict = {
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
        tstat_value = obj.tstat()
        self.assertTrue(45 <=  json.loads(tstat_value)['temp'] <= 99)
        self.assertTrue(0 <=  json.loads(tstat_value)['tmode'] <= 3)
