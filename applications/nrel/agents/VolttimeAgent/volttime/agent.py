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
#            Wesley Jones, National Renewable Energy Laboratory
# Version: 0.1
# Date: April 20, 2016
#
# National Renewable Energy Laboratory is a national laboratory of the
# U.S. Department of Energy, Office of Energy Efficiency and Renewable Energy,
# operated by the Alliance for Sustainable Energy, LLC
# under Contract No. DE-AC36-08GO28308.
#


from __future__ import absolute_import
from datetime import datetime
import logging
import sys
from volttron.platform.vip.agent import Agent, Core, PubSub, compat
from volttron.platform.agent import utils
from volttron.platform.messaging import headers as headers_mod
import time
from . import settings

utils.setup_logging()
_log = logging.getLogger(__name__)

class VolttimeAgent(Agent):
    """
        This agent will publish a current timestamp on the bus every second
        Template to enable faster tha realtime simulation in volttorn.
        Agents subscribe to this timestamp and synchronize accordingly

    """

    def __init__(self, config_path, **kwargs):
        """Initialize the calss and get config information"""
        super(VolttimeAgent, self).__init__(**kwargs)
        self.config = utils.load_config(config_path)

    @Core.receiver('onsetup')
    def setup(self, sender, **kwargs):
        """Setup the class and log agent information """
        _log.info(self.config['message'])
        self._agent_id = self.config['agentid']

    @Core.periodic(settings.HEARTBEAT_PERIOD)
    def publish_heartbeat(self):
        """Publish the current timestamp every second on the bus """
        headers = {
            'AgentID': self._agent_id,
            headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
            headers_mod.DATE: datetime.utcnow().isoformat(' ') + 'Z',
        }
        value = {}
        value['timestamp'] = {
            'Readings': str(time.strftime("%Y-%m-%d %H:%M:%S",
                                          time.localtime())), 'Units':'ts'
        }
        self.vip.pubsub.publish('pubsub', 'datalogger/log/volttime',
                                headers, value)

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(VolttimeAgent)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        pass
