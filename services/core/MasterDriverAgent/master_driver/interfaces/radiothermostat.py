

from master_driver.interfaces import BaseInterface, BaseRegister, BasicRevert, DriverInterfaceError
from csv import DictReader
from StringIO import StringIO

import csv

class Register(BaseRegister):
    def __init__(self, read_only, pointName, units, default_value):
        super(Register, self).__init__("byte", read_only, pointName, units)
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
        point_map = {point_name:[register.default_value]}
        result = self.vip.rpc.call('radiothermostat', 'get_point',
                                       self.target_address,point_name).get()
        # result_db = ast.literal_eval(result)
        return str(result)
    #
    # def set_default(self,default):
    #
    #     return str(result)

    def set_point(self, point_name, value):
        register = self.get_register_by_name(point_name)
        if register.read_only:
            raise  IOError("Trying to write to a point configured read only: "+point_name)
        args = [self.target_address, value,
                register.object_type,
                register.instance_number,
                register.property]
        result = self.vip.rpc.call('radiothermostat', 'set_point',
                                       self.target_address,point_name,value).get()
        return result


    def revert_point(self,point_name):
        self.set_point(point_name,default_value)

    def revert_all(self):
        write_registers = self.get_registers_by_type("byte", False)
        for register in write_registers:
            self.set_point(register.point_name,default_value)

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
            #Skip lines that have no address yet.

            read_only = regDef['Writable'].lower() != 'true'
            point_name = regDef['Volttron Point Name']
            units = regDef['Units']
            default_value = regDef['Default']
            register = Register(
                                read_only,
                                point_name,
                                units,
                                default_value)
            self.insert_register(register)
