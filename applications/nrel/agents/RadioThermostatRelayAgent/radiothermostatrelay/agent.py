
from __future__ import absolute_import
import logging
import sys
import json
import time
import ast
from datetime import datetime
from volttron.platform.vip.agent import Agent, Core, PubSub, RPC
from volttron.platform.agent import utils
from volttron.platform.messaging import headers as headers_mod
from . import  thermostat_api

utils.setup_logging()
_log = logging.getLogger(__name__)

def thermostat_agent(config_path, **kwargs):
    """
        Thermostat Relay Agent

        Subscribes:
          For Control signals:
          TOPIC:  datalogger/log/esif/spl/set_THERMOSTAT_1
          POINTS: tstat_cool_sp [60.9,90.0] float
                  tstat_mode [0,2] int
          For synchronization:
          TOPIC:  datalogger/log/volttime
          POINTS: timestamp [<%Y-%m-%d %H:%M:%S>] string
        Publishes:
          TOPIC:  datalogger/log/esif/spl/state_THERMOSTAT_1
          POINTS: tstat_cool_sp [60.9,90.0] float
                  tstat_mode [0,2] int,"Thermostat operating mode"
                  tstat_temp [60.0,90.0] float
                  timestamp [<volttime>] float
    """
    config = utils.load_config(config_path)
    vip_identity = config.get("vip_identity", "radiothermostat")
    #pop off the uuid based identity
    kwargs.pop('identity', None)

    class ThermostatRelayAgent(Agent):
        '''
            Thermostat class, serves as a relay sending control
            signals to the hardware
        '''

        def __init__(self, **kwargs):
            '''
                Initialize class from config file
            '''
            super(ThermostatRelayAgent, self).__init__(**kwargs)
            self.config = utils.load_config(config_path)
            self.volttime = None
            self.task = 0
            # points of interest for demo
            self.point_name_map = {
                    'tstat_mode' : "tmode",
                    'tstat_temp_sensor' : "temp",
                    'tstat_heat_sp' : 't_heat',
                    'tstat_cool_sp' : "t_cool",
                    'tstat_fan_mode' : 'fmode',
                    'tstat_hvac_state' : 'tstate'
            }
            self.units_map = {
                    'tstat_mode' : "state",
                    'tstat_temp_sensor' : "F",
                    'tstat_heat_sp' : 'F',
                    'tstat_cool_sp' : "F",
                    'tstat_fan_mode' : 'state',
                    'tstat_hvac_state' : 'state'
            }


            self.query_point_name = {
                    'tstat_mode',
                    'tstat_temp_sensor',
                    'tstat_heat_sp',
                    'tstat_cool_sp',
                    'tstat_fan_mode',
                    'tstat_hvac_state',
                    'override',
                    'hold'
            }
            self.program_name = {
                'heat_pgm_week',
                'heat_pgm_mon',
                'heat_pgm_tue',
                'heat_pgm_wed',
                'heat_pgm_thu',
                'heat_pgm_fri',
                'heat_pgm_sat',
                'heat_pgm_sun',
                'cool_pgm_week',
                'cool_pgm_mon',
                'cool_pgm_tue',
                'cool_pgm_wed',
                'cool_pgm_thu',
                'cool_pgm_fri',
                'cool_pgm_sat',
                'cool_pgm_sun'
            }

        @Core.receiver('onsetup')
        def setup(self, sender, **kwargs):
            '''
                Setup the class and export RPC methods
            '''
            # Demonstrate accessing a value from the config file
            _log.info(self.config['message'])
            self._agent_id = self.config['agentid']
            self.vip.rpc.export(self.set_point)
            self.vip.rpc.export(self.get_point)
            self.vip.rpc.export(self.ping_thermostat)
            url = self.config['url_address']
            #  Inistantiate Real or Virtual applicance based on info in config file
            if url == "Fake":
                self.thermostat = thermostat_api.FakeThermostat()
            else:
                self.thermostat = thermostat_api.ThermostatInterface(url)

        @RPC.export
        def get_point(self, device, point_map):
            '''
                Get value of a point_name on a device
            '''
            result = {}
            query = {}
            point_map_obj = {}
            for point_name, properties in point_map.iteritems():
                query = json.loads(self.thermostat.tstat())
                if point_name in self.query_point_name:
                    try:
                        b = query[self.point_name_map[point_name]]
                        result.update({point_name : str(b) })
                    except:
                        result.update({point_name : str("NA") })
                else:
                    pgm,day = point_name.rsplit('_',1)
                    if pgm == 'heat_pgm':
                        if day == 'week':
                            query = self.thermostat.get_heat_pgm()
                        else:
                            query = self.thermostat.get_heat_pgm(day)
                    elif pgm == 'cool_pgm':
                        if day == 'week':
                            query = self.thermostat.get_cool_pgm()
                        else:
                            query = self.thermostat.get_cool_pgm(day)
                    result.update({point_name : str(query)})

            return result

        @RPC.export
        def set_point(self, device, point_map, value):
            '''
                Set value of a point_name on a device
            '''
            result = {}
            for point_name, properties in point_map.iteritems():
                if point_name in self.program_name:
                    pgm,day = point_name.rsplit('_',1)
                    if pgm == 'heat_pgm':
                        if day == 'week':
                            result = self.thermostat.set_heat_pgm(str(value))
                        else:
                            result = self.thermostat.set_heat_pgm(str(value), day)
                    elif pgm == 'cool_pgm':
                        if day == 'week':
                            result = self.thermostat.set_cool_pgm(str(value))
                        else:
                            result = self.thermostat.set_cool_pgm(str(value), day)
                elif point_name == "tstat_mode":
                    result = self.thermostat.mode(int(value))
                elif point_name == "tstat_cool_sp":
                    result = self.thermostat.t_cool(value)
                elif point_name == "tstat_heat_sp":
                    result = self.thermostat.t_heat(value)
                else:
                    _log.debug("No such writable point found")
            return (str(result))


        @RPC.export
        def ping_thermostat(self,device):
            host = self.config['url_address']
            print "Ping Thermostat agent!"


        @PubSub.subscribe('pubsub', 'datalogger/log/esif/spl/set_THERMOSTAT_1')
        def match_ctl_set(self, peer, sender, bus, topic, headers, message):
            '''
                Subscribe to Control signals from Supervisory controller
            '''
            # print "subscribe to control signals"
            path,point_name = topic.rsplit('/',1)
            value = message['Readings']

            if point_name == "tstat_mode":
                self.thermostat.mode(int(value))
            elif point_name == "tstat_cool_sp":
                self.thermostat.t_cool(float(value))
            else:
                _log.debug("No such writable point found")


        @PubSub.subscribe('pubsub', 'datalogger/log/volttime')
        def match_all(self, peer, sender, bus, topic, headers, message):
            '''
                Subscribe to volttime and synchronize
            '''
            self.task = self.task + 1
            str_time = message['timestamp']['Readings']
            timestamp = time.strptime(str_time, "%Y-%m-%d %H:%M:%S")
            self.volttime = message['timestamp']['Readings']




    return ThermostatRelayAgent(identity=vip_identity, **kwargs)

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(thermostat_agent)
    except Exception as exception:
        _log.exception('unhandled exception')

if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
