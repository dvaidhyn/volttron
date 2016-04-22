
from __future__ import absolute_import
from datetime import datetime
import logging
import sys
import time
import random
import json
from volttron.platform.vip.agent import Agent, Core, PubSub, compat
from volttron.platform.agent import utils
from volttron.platform.messaging import headers as headers_mod
from . import settings


utils.setup_logging()
_log = logging.getLogger(__name__)

class SCHouseAgent(Agent):
    '''
    Publishes example control signals to control the Thermostat and CEA2045
    Relays
    '''
    def __init__(self, config_path, **kwargs):
        ''' SCHouseAgent initialization function'''
        super(SCHouseAgent, self).__init__(**kwargs)
        self.config = utils.load_config(config_path)
        self.volttime = None

    @Core.receiver('onsetup')
    def setup(self, sender, **kwargs):
        '''SCHouse setup function'''
        # Demonstrate accessing a value from the config file
        _log.info(self.config['message'])
        self._agent_id = self.config['agentid']
        self.cea_ctl = ['emergency','normal','shed']



    @Core.receiver('onstart')
    def begining(self, sender, **kwargs):
        '''on start'''
        start_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        timestamp=time.strptime(start_time,"%Y-%m-%d %H:%M:%S")
        end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.mktime(timestamp) + 600))
        msgs = [
                    ["esif/spl/THERMOSTAT_1", #First time slot.
                     str(start_time),     #Start of time slot.
                     str(end_time)]   #End of time slot.

                ]
        print json.dumps(self.vip.rpc.call('platform.actuator','request_new_schedule','rpc_ctl',"007",'HIGH',msgs).get())

    @Core.receiver('onstop')
    def ending(self, sender, **kwargs):
        ''' at the end'''
        print self.vip.rpc.call('platform.actuator','revert_point','rpc_ctl',"esif/spl/THERMOSTAT_1/tstat_cool_sp").get()
        self.vip.rpc.call('platform.actuator','request_cancel_schedule','rpc_ctl',"007")

    @PubSub.subscribe('pubsub', 'datalogger/log/volttime')
    def on_match_volttime(self, peer, sender, bus,  topic, headers, message):
        '''Subscribe to Volttime and send control signals '''
        str_time = message['timestamp']['Readings']
        timestamp=time.strptime(str_time,"%Y-%m-%d %H:%M:%S")
        self.volttime = message['timestamp']['Readings']
        if timestamp.tm_sec % 40 == 0 and timestamp.tm_min % 1 == 0:
            now = datetime.now().isoformat(' ') + 'Z'
            headers = {
                'AgentID': self._agent_id,
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            setpoint = random.randrange(75,85,1)
            print self.vip.rpc.call('platform.actuator','set_point','rpc_ctl',"esif/spl/THERMOSTAT_1/tstat_cool_sp", setpoint).get()
            print self.vip.rpc.call('platform.actuator','get_point',"esif/spl/THERMOSTAT_1/tstat_cool_sp").get()


        if timestamp.tm_sec % 33 == 0 and timestamp.tm_min % 1 == 0:
            now = datetime.now().isoformat(' ') + 'Z'
            headers = {
                'AgentID': self._agent_id,
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
            }
            value = {}
            setpoint = random.randrange(75,85,1)
            value = {"4":[360,setpoint,480,setpoint+2,1080,setpoint-2,1320,setpoint+3]}
            print self.vip.rpc.call('platform.actuator','set_point','rpc_ctl',"esif/spl/THERMOSTAT_1/heat_pgm_fri",str(value)).get()
            print self.vip.rpc.call('platform.actuator','get_point',"esif/spl/THERMOSTAT_1/heat_pgm_fri").get()



def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(SCHouseAgent)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
