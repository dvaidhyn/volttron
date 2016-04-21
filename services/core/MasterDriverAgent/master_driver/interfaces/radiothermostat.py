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
# Author: Deepthi Vaidhynathan, National Renewable Energy Laboratory
# Version:
# Date:
#
# National Renewable Energy Laboratory is a national laboratory of the
# U.S. Department of Energy, Office of Energy Efficiency and Renewable Energy,
# operated by the Alliance for Sustainable Energy, LLC
# under Contract No. DE-AC36-08GO28308.
#

import csv
from master_driver.interfaces import BaseInterface, BaseRegister, DriverInterfaceError
from csv import DictReader
from StringIO import StringIO


class Register(BaseRegister):
    def __init__(self, read_only, pointName, units, default_value):
        super(Register, self).__init__("byte", read_only, pointName, units, default_value)
        self.default_value = default_value


class Interface(BaseInterface):
    def __init__(self, **kwargs):
        super(Interface, self).__init__(**kwargs)

    def configure(self, config_dict, registry_config_str):
        self.parse_config(registry_config_str)
        self.target_address = config_dict["device_address"]
        self.proxy_address = config_dict.get("proxy_address", "cea2045")
        self.ping_target(self.target_address)

    def get_point(self, point_name):
        register = self.get_register_by_name(point_name)
        point_map = {}
        point_map = {point_name:[register.default_value]}
        result = self.vip.rpc.call('radiothermostat', 'get_point',
                                       self.target_address,point_map).get()
        return str(result)


    def set_point(self, point_name, value):
        register = self.get_register_by_name(point_name)
        point_map = {}
        point_map = {point_name:[register.default_value]}
        if register.read_only:
            raise  IOError("Trying to write to a point configured read only: "+point_name)
        result = self.vip.rpc.call('radiothermostat', 'set_point',
                                       self.target_address,point_map,value).get()
        return result


    def revert_point(self,point_name):
        register = self.get_register_by_name(point_name)
        value = register.default_value
        self.set_point(point_name,value)


    def revert_all(self):
        write_registers = self.get_registers_by_type("byte", False)
        for register in write_registers:
            self.set_point(register.point_name, register.default_value)

    def scrape_all(self):
        point_map = {}
        read_registers = self.get_registers_by_type("byte", True)
        write_registers = self.get_registers_by_type("byte", False)
        for register in read_registers + write_registers:
            point_map[register.point_name] = [register.default_value]
        # print point_map
        result = self.vip.rpc.call('radiothermostat', 'get_point',
                                       self.target_address,point_map).get()
        print "SCRAPED RESULT"
        print result
        return result

    def ping_target(self, address):
        print("ping_target not implemented in radiothermostat interface")

    def parse_config(self, config_string):
        if config_string is None:
            return
        f = StringIO(config_string)
        configDict = csv.DictReader(open("/home/parallels/Desktop/dvaidhyn_pnnl/volttron/services/core/MasterDriverAgent/master_driver/thermostat_dev.csv", 'rU'))
        for regDef in configDict:

            read_only = regDef['Writable'] == 'FALSE'
            point_name = regDef['Volttron Point Name']
            units = regDef['Units']
            default_value = regDef['Default']
            print default_value
            print units
            register = Register(
                                read_only,
                                point_name,
                                units,
                                default_value)
            self.insert_register(register)
