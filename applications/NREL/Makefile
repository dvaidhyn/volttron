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
# Version: 0.1
# Date:    April 20, 2016
#
# National Renewable Energy Laboratory is a national laboratory of the
# U.S. Department of Energy, Office of Energy Efficiency and Renewable Energy,
# operated by the Alliance for Sustainable Energy, LLC
# under Contract No. DE-AC36-08GO28308.
#


all: radiothermostatrelay  API_test_radiothermostatrelay cea2045relay API_test_cea2045relay schouse_controller vtime_now

radiothermostatrelay:
		volttron-ctl remove --force --tag radiothermostatrelay
		volttron-pkg package $(AGENTS_HOME)/RadioThermostatRelayAgent/
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/radiothermostatrelayagent-3.0-py2-none-any.whl $(AGENTS_HOME)/RadioThermostatRelayAgent/config
		volttron-ctl install radiothermostatrelay=$(VOLTTRON_HOME)/packaged/radiothermostatrelayagent-3.0-py2-none-any.whl

API_test_radiothermostatrelay:
		volttron-ctl remove --force --tag API_test_radiothermostatrelay
		volttron-pkg package $(AGENTS_HOME)/RadioThermostatRelayAgent/
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/radiothermostatrelayagent-3.0-py2-none-any.whl $(AGENTS_HOME)/RadioThermostatRelayAgent/config_api_test
		volttron-ctl install API_test_radiothermostatrelay=$(VOLTTRON_HOME)/packaged/radiothermostatrelayagent-3.0-py2-none-any.whl

cea2045relay:
		volttron-ctl remove --force --tag cea2045relay
		volttron-pkg package $(AGENTS_HOME)/CEA2045RelayAgent/
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/cea2045relayagent-3.0-py2-none-any.whl $(AGENTS_HOME)/CEA2045RelayAgent/config
		volttron-ctl install cea2045relay=$(VOLTTRON_HOME)/packaged/cea2045relayagent-3.0-py2-none-any.whl

schouse_controller:
		volttron-ctl remove --force --tag schouse_controller
		volttron-pkg package $(AGENTS_HOME)/SC_HouseAgent/
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/schouseagent-3.0-py2-none-any.whl $(AGENTS_HOME)/SC_HouseAgent/config
		volttron-ctl install schouse_controller=$(VOLTTRON_HOME)/packaged/schouseagent-3.0-py2-none-any.whl


API_test_cea2045relay:
		volttron-ctl remove --force --tag API_test_cea2045relay
		volttron-pkg package $(AGENTS_HOME)/CEA2045RelayAgent/
		volttron-pkg configure $(VOLTTRON_HOME)/packaged/cea2045relayagent-3.0-py2-none-any.whl $(AGENTS_HOME)/CEA2045RelayAgent/config_api_test
		volttron-ctl install API_test_cea2045relay=$(VOLTTRON_HOME)/packaged/cea2045relayagent-3.0-py2-none-any.whl


vtime_now:
	volttron-ctl remove --force --tag vtime_now
	volttron-pkg package $(AGENTS_HOME)/VolttimeAgent
	volttron-pkg configure $(VOLTTRON_HOME)/packaged/volttimeagent-3.0-py2-none-any.whl $(AGENTS_HOME)/VolttimeAgent/config
	volttron-ctl install vtime_now=$(VOLTTRON_HOME)/packaged/volttimeagent-3.0-py2-none-any.whl
